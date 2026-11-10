# SPDX-License-Identifier: MIT
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from teacher.assembly import build, render, save, scope_annotation
from teacher.editorial import assemble_draft, render as render_chapter
from teacher.coverage import require_coverage


class AssemblyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.sha='a'*40
        self.plan={'task_sha':self.sha,'chapters':[{'id':key,'files':[key+'.py'],'required_evidence':[],'focus':'TEST FIXTURE ONLY'} for key in ('one','two')],'excluded':[]}
        sections=[{'header':f'diff --git a/{key}.py b/{key}.py','offset':i*4,'bytes':4,'binary':False} for i,key in enumerate(('one','two'))]
        self.packets={};self.selection={'status':'accepted_chapter_set_pending_assembly','chapters':[]}
        for i,key in enumerate(('one','two')):
            other='two' if key=='one' else 'one'
            packet=self.root/'packets'/key;packet.mkdir(parents=True)
            self.packets[key]='packets/'+key
            m={'task_sha':self.sha,'task_parents':[],'base_commit':None,'commits':{},'cutoff_date':'2025-01-01T00:00:00Z',
               'shows':{self.sha:'b'*64},'task_change_sections':sections,'evidence':[],
               'authoring_task':{'kind':'chapter','id':key,'focus':'TEST FIXTURE ONLY','reasoning_effort':'high','required_sections':[i],'required_evidence':[],
                                 'chapter_catalog':[{'id':'one'},{'id':'two'}]}}
            if key=='two':m['editorial_schema_version']=3
            self.write(packet/'manifest.json',m)
            claim={'text':'TEST FIXTURE ONLY '+key,'basis':'source','evidence':['same-read-id']}
            a={'schema_version':3 if key=='two' else 2,'type':'feature','problem':[claim], 'reasoning':[], 'impact':[],
               'source_notes':[],'limitations':['TEST SCOPE LIMIT '+key],'links':[],
               'chapters':[{'id':key,'title':'TEST '+key,'claims':[claim],'related_chapters':[other]}]}
            if key=='two':a['findings']=[]
            t=[{'role':'assistant','calls':[{'id':'same-read-id','tool':'git_show','arguments':{'commit':self.sha,'offset':i*4}}]},
               {'role':'tool','name':'git_show','call_id':'same-read-id','content':json.dumps({'ok':True,'result':{'encoding':'utf-8','offset':i*4,'next_offset':i*4+4,'text':'TEST'}})},
               {'role':'assistant','content':json.dumps(a)}]
            d,review=assemble_draft(a,m,t);run=self.root/'runs'/key;run.mkdir(parents=True)
            for name,value in [('draft.json',d),('raw-transcript.json',t),('coverage.json',require_coverage(m,t)),
                ('status.json',{'status':'draft','published':False}),('review.json',review),
                ('provenance.json',{'input_mode':'entry_analysis','published':False,'packet_manifest_sha256':self.digest(packet/'manifest.json')})]:self.write(run/name,value)
            (run/'draft.md').write_text(render_chapter(d))
            self.selection['chapters'].append({'chapter':key,'run':'runs/'+key,'disposition':'accepted_as_chapter','artifacts_sha256':{n:self.digest(run/n) for n in ('draft.json','draft.md','raw-transcript.json','provenance.json')}})

    def write(self,p,v):p.write_text(json.dumps(v))
    def digest(self,p):return hashlib.sha256(p.read_bytes()).hexdigest()
    def build(self):return build(self.selection,self.packets,self.plan,self.root)

    def test_mixed_versions_preserve_prose_and_scope_colliding_calls(self):
        entry,sources=self.build()
        self.assertEqual(set(entry['evidence']),{'one::same-read-id','two::same-read-id'})
        for chapter in entry['chapters']:
            original=json.loads((self.root/'runs'/chapter['id']/'draft.json').read_text())['annotation']
            self.assertEqual(chapter['annotation'],scope_annotation(original,chapter['id']))
        text=render(entry)
        self.assertIn('[TEST two](#two)',text);self.assertNotIn('assembly link pending',text)
        self.assertNotIn('review_source',json.dumps(entry))
        self.assertEqual([s['source_annotation_version'] for s in sources],[2,3])

    def test_missing_duplicate_or_unaccepted_selection_rejected(self):
        original=deepcopy(self.selection)
        for rows in (original['chapters'][:1],original['chapters']+[original['chapters'][0]]):
            self.selection['chapters']=rows
            with self.assertRaises(ValueError):self.build()
        self.selection=original;self.selection['chapters'][0]['disposition']='pending'
        with self.assertRaises(ValueError):self.build()

    def test_tampered_accepted_artifact_rejected(self):
        p=self.root/'runs/one/draft.md';p.write_text(p.read_text()+'tampered')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):self.build()

    def test_changed_packet_rejected(self):
        p=self.root/'packets/one/manifest.json';p.write_text(p.read_text()+' ')
        with self.assertRaisesRegex(ValueError,'fingerprint'):self.build()

    def test_final_response_must_match_draft_even_if_selection_hash_updated(self):
        p=self.root/'runs/one/raw-transcript.json';t=json.loads(p.read_text());t[-1]['content']='{}';self.write(p,t)
        self.selection['chapters'][0]['artifacts_sha256']['raw-transcript.json']=self.digest(p)
        with self.assertRaisesRegex(ValueError,'final model response'):self.build()

    def test_changed_root_source_rejected_even_with_refingerprinted_packet(self):
        p=self.root/'packets/two/manifest.json';m=json.loads(p.read_text());m['shows'][self.sha]='c'*64;self.write(p,m)
        p=self.root/'runs/two/provenance.json';v=json.loads(p.read_text());v['packet_manifest_sha256']=self.digest(self.root/'packets/two/manifest.json');self.write(p,v)
        self.selection['chapters'][1]['artifacts_sha256']['provenance.json']=self.digest(p)
        with self.assertRaisesRegex(ValueError,'identical root source'):self.build()

    def test_dangling_navigation_and_path_escape_rejected(self):
        entry,_=self.build();entry['chapters'][0]['annotation']['chapters'][0]['related_chapters']=['missing']
        with self.assertRaisesRegex(ValueError,'navigation'):render(entry)
        self.selection['chapters'][0]['run']='../outside'
        with self.assertRaises(ValueError):self.build()

    def test_saved_candidate_is_pending_and_output_cannot_be_overwritten(self):
        for name,v in [('selection',self.selection),('packets',self.packets),('plan',self.plan)]:self.write(self.root/(name+'.json'),v)
        args=[self.root/(n+'.json') for n in ('selection','packets','plan')]+[self.root/'out']
        save(*args,root=self.root)
        review=json.loads((self.root/'out/review.json').read_text())
        self.assertEqual(review['status'],'pending');self.assertFalse(review['ancestor_context_approved'])
        with self.assertRaises(FileExistsError):save(*args,root=self.root)
