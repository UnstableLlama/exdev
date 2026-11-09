# SPDX-License-Identifier: MIT
import gzip
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from graph.timeline import Timeline
from test_timeline import snap,symbol


class ExternalSnapshotTests(unittest.TestCase):
    def test_sqlite_stores_path_and_checks_archive_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);db=Timeline(root/'timeline.sqlite')
            s=snap('root',nodes=[symbol()]);db.ingest(s)
            columns=[r[1] for r in db.db.execute('PRAGMA table_info(commits)')]
            self.assertNotIn('snapshot',columns)
            self.assertIn('snapshot_path',columns)
            self.assertEqual(db.snapshot('root')['nodes'],s['nodes'])
            path=root/db.db.execute('SELECT snapshot_path FROM commits').fetchone()[0]
            with gzip.open(path,'wt') as f:json.dump(dict(s,nodes=[]),f)
            with self.assertRaisesRegex(ValueError,'fingerprint'):db.snapshot('root')
            db.close()

    def test_failed_import_does_not_publish_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);db=Timeline(root/'timeline.sqlite')
            with self.assertRaises(ValueError):db.ingest(snap('child',['missing']))
            self.assertFalse((root/'graphs/child.json.gz').exists());db.close()

    def legacy_store(self, root):
        db = Timeline(root/'timeline.sqlite')
        db.ingest(snap('root', nodes=[symbol()]))
        serialized = json.dumps(db.snapshot('root'), sort_keys=True, separators=(',', ':'))
        with db.db:
            db.db.execute('ALTER TABLE commits RENAME COLUMN snapshot_path TO snapshot')
            db.db.execute('UPDATE commits SET snapshot=?', (serialized,))
            db.db.execute('PRAGMA user_version=1')
        db.close()

    def test_migration_keeps_fingerprints_and_makes_backup(self):
        from graph.migrate_timeline import migrate
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.legacy_store(root)
            result = migrate(root/'timeline.sqlite')
            self.assertEqual(result['commits'], 1)
            self.assertTrue(Path(result['backup']).exists())
            db = Timeline(root/'timeline.sqlite')
            self.assertEqual(db.snapshot('root')['nodes'], [symbol()])
            self.assertEqual(db.db.execute('PRAGMA foreign_key_check').fetchall(), [])
            db.close()
            self.assertEqual(migrate(root/'timeline.sqlite')['status'], 'already_migrated')

    def test_migration_rejects_corrupt_archive_before_schema_change(self):
        from graph.migrate_timeline import migrate
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.legacy_store(root)
            with gzip.open(root/'graphs/root.json.gz', 'wt') as f:
                f.write('{}')
            with self.assertRaisesRegex(ValueError, 'fingerprint'):
                migrate(root/'timeline.sqlite')
            db = sqlite3.connect(root/'timeline.sqlite')
            self.assertEqual(db.execute('PRAGMA user_version').fetchone()[0], 1)
            db.close()
