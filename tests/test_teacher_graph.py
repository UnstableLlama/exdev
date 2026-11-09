# SPDX-License-Identifier: MIT
import hashlib
import json
import unittest
from teacher.graph_packet import attach_graphs
from teacher.worker import dispatch
from graph.timeline import Timeline
import test_teacher_packet


class GraphPacketTests(unittest.TestCase):
    setUp = test_teacher_packet.PacketTests.setUp
    tearDown = test_teacher_packet.PacketTests.tearDown

    def prepare(self):
        store = self.root / 'store'
        timeline = Timeline(store / 'timeline.sqlite')
        try:
            for i, sha in enumerate([self.first, self.side], 1):
                archive = b'TEST DATABASE ONLY'
                (store / 'graphs').mkdir(exist_ok=True)
                (store / 'graphs' / (sha + '.db.gz')).write_bytes(archive)
                timeline.ingest(dict(sha=sha, position=i, parents=[] if i==1 else [self.first],
                    nodes=[dict(qn='a.f', name='f', kind='Function', file='a.py', start=1, end=1, body_hash=sha)],
                    edges=[], backend='fixture', provenance=dict(teacher_ready=True,
                    backend_db_sha256=hashlib.sha256(archive).hexdigest(),
                    index_diagnostics={'logfile':'ADMIN_SECRET', 'parse_partial_count':0})))
        finally:
            timeline.close()
        attach_graphs(self.packet, store)

    def test_export_and_tools_exclude_other_branches(self):
        self.prepare()
        manifest = json.loads((self.packet/'manifest.json').read_text())
        self.assertEqual(set(manifest['graphs']), {self.first})
        contents = b''.join(p.read_bytes() for p in self.packet.rglob('*') if p.is_file())
        self.assertNotIn(b'ADMIN_SECRET', contents)
        for tool in ['graph_search', 'repo_map', 'symbol_history', 'graph_trace']:
            args = {'commit':self.first}
            if tool in ['symbol_history','graph_trace']: args['symbol']='a.f'
            self.assertTrue(dispatch(self.packet, tool, args))
            for sha in [self.side,self.future,self.task]:
                with self.assertRaises(ValueError): dispatch(self.packet, tool, dict(args, commit=sha))
        result=dispatch(self.packet,'symbol_history',dict(commit=self.first,symbol='a.f'))
        self.assertEqual([e['sha'] for e in result['events']], [self.first])

    def test_missing_graphs_fail_closed(self):
        with self.assertRaises(ValueError):
            dispatch(self.packet, 'graph_search', dict(commit=self.first))

    def test_corrupt_archive_does_not_publish_graph_manifest(self):
        self.prepare()
        manifest=json.loads((self.packet/'manifest.json').read_text())
        del manifest['graphs']
        (self.packet/'manifest.json').write_text(json.dumps(manifest))
        (self.root/'store/graphs'/ (self.first+'.db.gz')).write_bytes(b'corrupt')
        with self.assertRaises(ValueError):attach_graphs(self.packet,self.root/'store')
        self.assertNotIn('graphs',json.loads((self.packet/'manifest.json').read_text()))

    def test_graph_tools_are_advertised_only_with_prepared_graphs(self):
        from teacher.session import FreshSession
        self.assertEqual(len(FreshSession(self.packet).tools), 9)
        self.prepare()
        self.assertEqual(len(FreshSession(self.packet).tools), 14)

    def test_graph_blob_tampering_is_rejected(self):
        self.prepare()
        manifest=json.loads((self.packet/'manifest.json').read_text())
        (self.packet/'blobs'/manifest['graphs'][self.first]['snapshot']).write_bytes(b'{}')
        with self.assertRaisesRegex(ValueError,'checksum'):
            dispatch(self.packet,'graph_search',dict(commit=self.first))
