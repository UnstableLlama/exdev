# SPDX-License-Identifier: MIT
import unittest
from test_timeline import symbol, snap
import test_timeline
from graph.link_entries import load_links

class EntryLinkTests(unittest.TestCase):
    setUp = test_timeline.TimelineTests.setUp
    tearDown = test_timeline.TimelineTests.tearDown
    def test_removed_symbol_links_to_parent_and_is_idempotent(self):
        self.db.ingest(snap('root',nodes=[symbol()]))
        self.db.ingest(snap('child',['root'],[],2))
        seeds={'entries':[{'entry_id':'2','symbols':[{'qn':'p.a.f','revision':'first_parent'}]}]}
        entries={'2':{'sha':'child','parent_shas':['root']}}
        result=load_links(self.db,seeds,entries)
        load_links(self.db,seeds,entries)
        self.assertEqual(result['entries'][0]['symbols'][0]['source_sha'],'root')
        self.assertEqual(self.db.db.execute('SELECT count(*) FROM entry_links').fetchone()[0],1)
        self.assertEqual(self.db.db.execute('PRAGMA foreign_key_check').fetchall(),[])

    def test_bad_reference_does_not_replace_existing_links(self):
        self.db.ingest(snap('root',nodes=[symbol()]))
        entries={'1':{'sha':'root','parent_shas':[]}}
        good={'entries':[{'entry_id':'1','symbols':[{'qn':'p.a.f','revision':'entry'}]}]}
        load_links(self.db,good,entries)
        bad={'entries':[{'entry_id':'1','symbols':[{'qn':'missing','revision':'entry'}]}]}
        with self.assertRaises(ValueError):load_links(self.db,bad,entries)
        self.assertEqual(self.db.db.execute('SELECT qn FROM entry_links').fetchone()[0],'p.a.f')
