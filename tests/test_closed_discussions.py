# SPDX-License-Identifier: MIT
import copy
import json
import tempfile
import unittest
from pathlib import Path
from teacher.closed_discussions import select,terms,attach,validate,page,task_terms
from teacher.evidence import discussion_snapshot
from teacher.worker import dispatch
from teacher.session import FreshSession
import test_evidence

CUTOFF='2025-01-02T00:00:00Z'
class ClosedDiscussionTests(unittest.TestCase):
    def bundle(self,n=1,text='rareterm'):
        b=test_evidence.EvidenceTests().discussion(number=n,title='Discussion',state_events=[{'kind':'closed','createdAt':'2025-01-01T12:00:00Z'}])
        b['url']=f'https://github.com/a/b/issues/{n}';b['objects'][0].update(body=text,url=b['url'],id=str(n));return b
    def selected(self,bs,task='rareterm',cap=20):return select(bs,CUTOFF,terms(task),[],cap=cap,message=terms(task))
    def test_rare_term_and_stop_terms(self):
        r=self.selected([self.bundle(1,'rareterm model error'),self.bundle(2,'model error')], 'rareterm model error')
        self.assertEqual([i['number'] for i in r['items']],[1]);self.assertEqual(r['items'][0]['matched_terms'],['rareterm'])
    def test_frequent_terms_discounted(self):
        bs=[self.bundle(i,'sharedterm') for i in range(4)]
        self.assertEqual(self.selected(bs,'sharedterm')['items'],[])
        bs[0]['objects'][0]['body']+=' rareterm'
        self.assertEqual([r['number'] for r in self.selected(bs,'sharedterm rareterm')['items']],[0])
    def test_future_comment_and_title_do_not_match(self):
        b=self.bundle(text='nothing');o=copy.deepcopy(b['objects'][0]);o.update(createdAt='2025-01-03T00:00:00Z',body='rareterm');b['objects'].append(o)
        b['title']='rareterm';b['title_events']=[{'createdAt':'2025-01-03T00:00:00Z','previousTitle':'old','currentTitle':'rareterm'}]
        self.assertEqual(self.selected([b])['items'],[])
    def test_closed_after_cutoff_remains_open(self):
        b=self.bundle();b['state_events'][0]['createdAt']='2025-01-03T00:00:00Z'
        self.assertEqual(self.selected([b])['items'],[]);self.assertIsNotNone(discussion_snapshot(b,CUTOFF))
    def test_fail_closed_unknown_or_summary_content(self):
        for change in ['timeline','missing','summary']:
            b=self.bundle()
            if change=='timeline':b['timeline_complete']=False
            else:
                b['objects'][0]['lastEditedAt']='2025-01-03T00:00:00Z'
                if change=='summary':b['objects'][0]['edits']=[{'id':'edit','editedAt':'2025-01-01T01:00:00Z','diff':'rareterm','deletedAt':None}]
            self.assertEqual(self.selected([b])['items'],[])
    def test_no_time_limit_and_reopened_not_closed(self):
        b=self.bundle();self.assertEqual(len(self.selected([b])['items']),1)
        b['state_events'].append({'kind':'reopened','createdAt':'2025-01-01T13:00:00Z'})
        self.assertEqual(self.selected([b])['items'],[])
    def test_cap_pages_binding_fetch_and_legacy(self):
        bs=[self.bundle(i,'uniqueterm'+str(i)) for i in range(25)]
        result=self.selected(bs,' '.join('uniqueterm'+str(i) for i in range(25)))
        self.assertTrue(result['truncated']);self.assertEqual(len(result['items']),20)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'blobs').mkdir();m={'task_sha':'b'*40,'task_parents':['a'*40],'base_commit':'a'*40,'cutoff_date':CUTOFF,'commits':{},'evidence':[],'evidence_index':{'sources':[]},'walk_input_contract':{'version':8}}
            attach(p,m,dict(result,task_sha=m['task_sha'],cutoff=CUTOFF,complete=True));validate(m,p)
            chunks=[];offset=0
            while True:
                x=page(m,{'offset':offset,'max_bytes':128});chunks.append(x['text'])
                if not x['truncated']:break
                offset=x['next_offset']
            self.assertEqual(json.loads(''.join(chunks)),m['closed_discussion_catalog']['rows'])
            (p/'manifest.json').write_text(json.dumps(m))
            fetched=dispatch(p,'web_fetch',{'url':bs[0]['url']});self.assertIn('uniqueterm0',fetched['text'])
            initial=FreshSession(p).initial;opening=json.loads(initial[1]['content']);self.assertIn('closed_discussion_catalog',opening)
            self.assertNotIn('score',opening['closed_discussion_catalog']['text']);self.assertNotIn('objects',opening['closed_discussion_catalog']['text'])
            for field in ['catalog','object']:
                bad=copy.deepcopy(m)
                if field=='catalog':bad['closed_discussion_catalog']['rows'][0]['matched_terms']=['changed']
                else:bad['evidence'][0]['url']='changed'
                with self.assertRaises(ValueError):validate(bad)
            old=copy.deepcopy(m);old.pop('closed_discussion_catalog');old['evidence']=[];old['walk_input_contract']={'version':7};(p/'manifest.json').write_text(json.dumps(old))
            self.assertNotIn('closed_discussion_catalog',json.loads(FreshSession(p).initial[1]['content']))
            self.assertNotIn('matched terms expose',FreshSession(p).initial[0]['content'])
            with self.assertRaises(ValueError):page(old,{})
    def test_task_terms_use_only_task_message_paths_and_code_identifiers(self):
        from unittest.mock import patch
        responses=[b'Fix RareMessage',b'pkg/rare_path.py\n',b'diff --git a/pkg/rare_path.py b/pkg/rare_path.py\n-old_identifier = "literalword" # commentword\n+new_identifier = callname()\n']
        with patch('teacher.closed_discussions.git',side_effect=responses):
            result=task_terms(None,'sha')
        self.assertTrue({'raremessage','rare_path','old_identifier','new_identifier','callname'}<=result)
        self.assertFalse({'literalword','commentword','futureterm'}&result)
    def test_no_age_limit(self):
        self.assertEqual(len(select([self.bundle()],'2050-01-01T00:00:00Z',terms('rareterm'),[],message=terms('rareterm'))['items']),1)

    def test_only_message_terms_qualify_but_other_matches_remain_visible(self):
        b=self.bundle(text='uniquediff uniquemessage')
        task=terms('uniquediff uniquemessage')
        self.assertEqual(select([b],CUTOFF,task,[],message=terms('Cleanup'))['items'],[])
        rows=select([b],CUTOFF,task,[],message=terms('uniquediff'))['items']
        self.assertEqual(rows[0]['matched_terms'],['uniquediff','uniquemessage'])
    def test_audit_reports_closed_and_eligible_counts_separately(self):
        good=self.bundle(1);bad=self.bundle(2);bad['objects'][0].pop('lastEditedAt')
        future=self.bundle(3);future['state_events'][0]['createdAt']='2025-01-03T00:00:00Z'
        r=self.selected([good,bad,future])
        self.assertEqual(r['closed_at_cutoff'],2);self.assertEqual(r['eligible_candidates'],1)
