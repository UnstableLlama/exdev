# SPDX-License-Identifier: MIT
import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import test_closed_discussions as fixtures
CUTOFF=fixtures.CUTOFF
from teacher.closed_discussions import select,terms,attach,validate,page,task_paths,PATH_RULE
from teacher.session import FreshSession


class ClosedPathOverlapTests(unittest.TestCase):
    bundle=fixtures.ClosedDiscussionTests.bundle

    def selected(self,bundles,paths=('eval/humaneval.py',),changed=('eval/humaneval.py',),cap=20):
        return select(bundles,CUTOFF,terms('ordinary'),list(paths),message=terms('ordinary'),changed_paths=list(changed),cap=cap)

    def test_unique_filename_title_qualifies_without_lexical_score(self):
        b=self.bundle(text='No matching words');b['title']='humaneval.py: correction'
        r=self.selected([b]);self.assertEqual(r['rule'],PATH_RULE)
        self.assertEqual(r['items'][0]['matched_paths'],['eval/humaneval.py'])
        self.assertEqual(r['items'][0]['matched_terms'],[])
        self.assertEqual(select([b],CUTOFF,terms('ordinary'),['eval/humaneval.py'],message=terms('ordinary'))['items'],[])

    def test_ambiguous_and_foreign_paths_do_not_qualify(self):
        for text,paths in [('humaneval.py',['eval/humaneval.py','other/humaneval.py']),
                           ('other/humaneval.py',['eval/humaneval.py']),
                           ('myhumaneval.py',['eval/humaneval.py']),
                           ('humaneval.py.bak',['eval/humaneval.py'])]:
            self.assertEqual(self.selected([self.bundle(text=text)],paths=paths)['items'],[])
        self.assertEqual(self.selected([self.bundle(text='eval/humaneval.py')],paths=['eval/humaneval.py','other/humaneval.py'])['items'][0]['matched_paths'],['eval/humaneval.py'])

    def test_cutoff_title_comments_state_and_unavailable_stay_closed(self):
        b=self.bundle(text='unrelated');b['title']='humaneval.py';b['title_events']=[dict(createdAt='2025-01-03T00:00:00Z',previousTitle='unrelated',currentTitle='humaneval.py')]
        o=copy.deepcopy(b['objects'][0]);o.update(id='future',url=b['url']+'#future',createdAt='2025-01-03T00:00:00Z',body='eval/humaneval.py');b['objects'].append(o)
        self.assertEqual(self.selected([b])['items'],[])
        for variant in ('reopened','unknown','missing_body'):
            b=self.bundle(text='eval/humaneval.py')
            if variant=='reopened':b['state_events'].append(dict(kind='reopened',createdAt='2025-01-01T13:00:00Z'))
            elif variant=='unknown':b['timeline_complete']=False
            else:b['objects'][0].pop('lastEditedAt')
            self.assertEqual(self.selected([b])['items'],[])

    def test_cap_exclusions_and_order(self):
        bs=[self.bundle(i,text='eval/humaneval.py') for i in reversed(range(25))]
        r=self.selected(bs);self.assertEqual([x['number'] for x in r['items']],list(range(20)));self.assertTrue(r['truncated']);self.assertEqual(r['qualified_count'],25)
        r=select(bs,CUTOFF,set(),['eval/humaneval.py'],excluded=[bs[0]['url']],message=set(),changed_paths=['eval/humaneval.py'])
        self.assertEqual(r['qualified_count'],24)

    def test_first_parent_paths_and_rename_sides(self):
        with patch('teacher.closed_discussions.git',side_effect=[b'p1 p2',b'old.py\nnew.py\n']) as g:
            self.assertEqual(task_paths(None,'merge'),['new.py','old.py'])
            self.assertEqual(g.call_args.args[1:],('diff-tree','--no-commit-id','--name-only','--no-renames','-r','p1','merge'))
        r=self.selected([self.bundle(text='new.py')],paths=[],changed=['new.py'])
        self.assertEqual(r['items'][0]['matched_paths'],['new.py'])

    def test_attachment_binding_and_versioned_instruction(self):
        result=self.selected([self.bundle(text='eval/humaneval.py')])
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'blobs').mkdir();m=dict(task_sha='b'*40,task_parents=['a'*40],base_commit='a'*40,cutoff_date=CUTOFF,commits={},evidence=[],evidence_index={'sources':[]},walk_input_contract={'version':8},task_changed_files=['eval/humaneval.py'])
            b=dict(result,task_sha=m['task_sha'],cutoff=CUTOFF,complete=True)
            bad=copy.deepcopy(b);bad['task_changed_paths']=['elsewhere.py']
            with self.assertRaisesRegex(ValueError,'changed paths'):attach(p,m,bad)
            bad=copy.deepcopy(b);bad['items'][0]['matched_paths']=['elsewhere.py']
            with self.assertRaisesRegex(ValueError,'matched paths'):attach(p,m,bad)
            attach(p,m,b);validate(m,p);(p/'manifest.json').write_text(json.dumps(m))
            self.assertIn('matched_paths',page(m,{'max_bytes':8192})['text'])
            self.assertIn('bare filename',FreshSession(p).initial[0]['content'])
            if os.environ.get('EXDEV_SANDBOX_TESTS')=='1':
                from teacher.runner import Runner
                result=Runner(p).invoke('evidence_index',dict(index_id='closed_discussions',offset=0,max_bytes=128))
                self.assertTrue(result['ok'],result)
                self.assertEqual(result['result'],page(m,dict(offset=0,max_bytes=128)))
            bad=copy.deepcopy(m);bad['closed_discussion_catalog']['rows'][0]['matched_paths']=[]
            with self.assertRaises(ValueError):validate(bad)
