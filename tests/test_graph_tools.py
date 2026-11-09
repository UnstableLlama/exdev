# SPDX-License-Identifier: MIT
import tempfile
import unittest
from pathlib import Path
from graph.timeline import Timeline
from graph.tools import GraphTools

class GraphToolTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'t.sqlite'
        self.db=Timeline(self.path)
        nodes=[dict(qn='p.'+name,name=name,kind='Function',file='a.py',start=i+1,end=i+1,body_hash=name) for i,name in enumerate(['f','g','h'])]
        self.root=dict(sha='root',position=1,parents=[],backend='test',nodes=nodes,edges=[['p.f','CALLS','p.g']],
             supplemental_edges=[dict(source='p.g',target='p.h',type='CALLS',origin='pybind-direct-v1',evidence=[{'line':2}])],
             provenance={'teacher_ready':True})
        self.db.ingest(self.root)
        self.db.ingest(dict(self.root,sha='future',parents=['root'],position=2))
        self.tools=GraphTools(self.db,'root')
    def tearDown(self):self.db.close();self.tmp.cleanup()

    def test_every_tool_rejects_future_before_access(self):
        requests=[('graph_search',{}),('graph_trace',{'symbol':'p.f'}),('graph_query',{'query':'MATCH (n) RETURN n'}),
                  ('symbol_history',{'symbol':'p.f'}),('repo_map',{})]
        for name,args in requests:
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'ancestor'):
                self.tools.invoke(name,dict(commit='future',**args))

    def test_trace_includes_binding_edges_and_respects_depth(self):
        r=self.tools.invoke('graph_trace',dict(commit='root',symbol='p.f',depth=2))
        self.assertEqual({e['target'] for e in r['edges']},{'p.g','p.h'})
        r=self.tools.invoke('graph_trace',dict(commit='root',symbol='p.f',depth=1))
        self.assertEqual(len(r['edges']),1)

    def test_bounded_search_and_map(self):
        r=self.tools.invoke('graph_search',dict(commit='root',name_pattern='*',limit=1))
        self.assertEqual(len(r['nodes']),1);self.assertTrue(r['has_more'])
        r=self.tools.invoke('repo_map',dict(commit='root',token_budget=60))
        self.assertLessEqual(len(r['text'].encode()),60)

    def test_rejects_missing_commit_unknown_args_and_invalid_limits(self):
        for args in [{},{'commit':'root','cutoff':'future'},{'commit':'root','limit':0}]:
            with self.assertRaises(ValueError):self.tools.invoke('graph_search',args)

    def test_validation_only_snapshot_is_not_teacher_context(self):
        self.db.ingest(dict(self.root,sha='unsafe',parents=['future'],position=3,provenance={'teacher_ready':False}))
        with self.assertRaisesRegex(ValueError,'teacher'):
            GraphTools(self.db,'unsafe').invoke('graph_search',{'commit':'unsafe'})
