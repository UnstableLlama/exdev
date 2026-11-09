# SPDX-License-Identifier: MIT
from contextlib import closing
import hashlib
import sqlite3
import tempfile
import unittest
from pathlib import Path
from graph.verify import verify_export, verify_source, verify_events


class GraphAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'graph.db'
        with closing(sqlite3.connect(self.path)) as db:
            db.executescript('CREATE TABLE nodes(id INTEGER,project TEXT,qualified_name TEXT,name TEXT,label TEXT,file_path TEXT,start_line INTEGER,end_line INTEGER); CREATE TABLE edges(source_id INTEGER,target_id INTEGER,type TEXT,project TEXT);')
            db.executemany('INSERT INTO nodes VALUES (?,?,?,?,?,?,?,?)',[(1,'exllamav3','p.f','f','Function','a.py',1,2),(2,'exllamav3','p.g','g','Function','a.py',4,5)])
            db.execute("INSERT INTO edges VALUES (1,2,'CALLS','exllamav3')")
            db.commit()
        source=b'def f():\n    g()\n\ndef g():\n    pass\n'
        self.files={'a.py':source}
        self.nodes=[dict(qn=q,name=q[-1],kind='Function',file='a.py',start=start,end=end,
                   body_hash=hashlib.sha256(b''.join(source.splitlines(keepends=True)[start-1:end])).hexdigest())
                   for q,start,end in [('p.f',1,2),('p.g',4,5)]]
        self.snapshot=dict(nodes=self.nodes,edges=[['p.f','CALLS','p.g']],supplemental_edges=[],sha='test')

    def tearDown(self):self.tmp.cleanup()

    def test_matching_exports_and_source_pass(self):
        verify_export(self.snapshot,self.path)
        self.assertEqual(verify_source(self.snapshot,self.files),2)

    def test_equal_count_wrong_edge_is_detected(self):
        self.snapshot['edges']=[['p.g','CALLS','p.f']]
        with self.assertRaisesRegex(ValueError,'edge'):verify_export(self.snapshot,self.path)

    def test_duplicate_nodes_are_detected(self):
        self.snapshot['nodes'][1]=dict(self.snapshot['nodes'][0])
        with self.assertRaisesRegex(ValueError,'node'):verify_export(self.snapshot,self.path)

    def test_changed_source_is_detected(self):
        with self.assertRaisesRegex(ValueError,'source hash'):verify_source(self.snapshot,{'a.py':b'changed\n'})

    def test_wrong_events_are_detected(self):
        with self.assertRaisesRegex(ValueError,'events'):verify_events([],self.nodes,[])

    def test_final_auditor_rejects_incomplete_walk(self):
        from graph.finalize_walk import final_audit
        with self.assertRaisesRegex(ValueError,'did not complete'):
            final_audit(Path('/missing'),{'status':'failed','target_position':2264})

    def test_final_auditor_requires_requested_final_position(self):
        from graph.finalize_walk import final_audit
        from unittest.mock import patch
        with patch('graph.finalize_walk.audit',return_value={'through_position':25}):
            with self.assertRaisesRegex(ValueError,'final position'):
                final_audit(Path('/missing'),{'status':'complete','target_position':2264})
