# SPDX-License-Identifier: MIT
import tempfile
import unittest
from pathlib import Path
from graph.timeline import Timeline, symbol_diff


def symbol(qn='p.a.f', body='one', line=1):
    return dict(qn=qn, name=qn.rsplit('.', 1)[-1], kind='Function', file='a.py', start=line, end=line+2, body_hash=body)


def snap(sha, parents=(), nodes=None, position=1):
    return dict(sha=sha, parents=list(parents), position=position, nodes=nodes or [], edges=[], backend='test')


class TimelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Timeline(Path(self.tmp.name) / 'timeline.sqlite')

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_body_edit_but_not_line_shift(self):
        self.assertEqual(symbol_diff([symbol()], [symbol(line=9)]), [])
        events = symbol_diff([symbol()], [symbol(body='two')])
        self.assertEqual([e['event'] for e in events], ['changed'])

    def test_unique_move_and_ambiguous_move(self):
        self.assertEqual(symbol_diff([symbol()], [symbol('p.b.f')])[0]['event'], 'moved')
        events = symbol_diff([symbol(), symbol('p.c.f')], [symbol('p.b.f')])
        self.assertEqual(sorted(e['event'] for e in events), ['added', 'removed', 'removed'])

    def test_parent_required_and_no_partial_import(self):
        with self.assertRaisesRegex(ValueError, 'parent'):
            self.db.ingest(snap('child', ['missing']))
        self.assertEqual(self.db.db.execute('SELECT count(*) FROM commits').fetchone()[0], 0)

    def test_idempotent_and_conflicting_rerun(self):
        self.assertTrue(self.db.ingest(snap('root', nodes=[symbol()])))
        self.assertFalse(self.db.ingest(snap('root', nodes=[symbol()])))
        with self.assertRaisesRegex(ValueError, 'different'):
            self.db.ingest(snap('root', nodes=[symbol(body='two')] ))
        self.assertEqual(self.db.db.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_branch_history_excludes_other_branch_and_future(self):
        for s in [snap('root', nodes=[symbol()]), snap('left',['root'],[symbol(body='left')],2),
                  snap('right',['root'],[symbol(body='right')],3),snap('future',['left'],[symbol(body='later')],4)]:
            self.db.ingest(s)
        self.assertEqual([r['sha'] for r in self.db.history('p.a.f','left')], ['root','left'])
        with self.assertRaisesRegex(ValueError, 'ancestor'):
            self.db.authorize('right', 'left')
        self.db.authorize('root', 'left')

    def test_merge_diffs_first_parent_and_retains_all_parents(self):
        for s in [snap('root',nodes=[symbol()]),snap('a',['root'],[symbol(body='a')],2),
                  snap('b',['root'],[symbol(body='b')],3),snap('merge',['a','b'],[symbol(body='a')],4)]:
            self.db.ingest(s)
        self.assertEqual(self.db.db.execute("SELECT count(*) FROM symbol_events WHERE sha='merge'").fetchone()[0],0)
        self.assertEqual(self.db.parents('merge'), ['a','b'])

    def test_reintroduced_symbol_has_new_added_event(self):
        for s in [snap('root',nodes=[symbol()]),snap('gone',['root'],[],2),snap('back',['gone'],[symbol()],3)]:
            self.db.ingest(s)
        self.assertEqual([e['event'] for e in self.db.history('p.a.f','back')], ['added','removed','added'])

    def test_merge_events_are_preserved_with_arrival_provenance(self):
        for s in [snap('root', nodes=[symbol()]),
                  snap('a', ['root'], [symbol(body='a')], 2),
                  snap('b', ['root'], [symbol(body='b')], 3),
                  snap('merge', ['a', 'b'], [symbol(body='b')], 4)]:
            self.db.ingest(s)
        event = self.db.history('p.a.f', 'merge')[-1]
        self.assertEqual(event['event'], 'changed')
        self.assertEqual(event['origin'], 'merge_arrival')
        self.assertEqual(event['parents'], ['a', 'b'])
