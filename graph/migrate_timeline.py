# SPDX-License-Identifier: MIT
"""Explicit v1 to v2 migration: reference verified compressed snapshots instead of duplicating JSON."""
import argparse
from contextlib import closing
import fcntl
import hashlib
import json
from pathlib import Path
import sqlite3
from .timeline import read_snapshot
from .validate import ROOT


def migrate(path):
    path = Path(path).resolve()
    backup = path.with_name(path.stem + '-v1-backup.sqlite')
    with (path.parent / 'index.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with closing(sqlite3.connect(path)) as db:
            db.execute('PRAGMA foreign_keys=ON')
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if version == 2:
                return {'status': 'already_migrated'}
            if version != 1:
                raise ValueError('Expected timeline schema v1')
            before = path.stat().st_size
            # Verify every existing archive before changing any database rows.
            count = 0
            for sha, serialized, fingerprint in db.execute('SELECT sha,snapshot,fingerprint FROM commits'):
                if hashlib.sha256(serialized.encode()).hexdigest() != fingerprint:
                    raise ValueError('Existing timeline fingerprint mismatch')
                archived = read_snapshot(path.parent, f'graphs/{sha}.json.gz', fingerprint)
                if json.loads(serialized) != archived:
                    raise ValueError('Existing archive does not match timeline')
                count += 1
            if backup.exists():
                raise ValueError('Migration backup already exists; inspect it before retrying')
            with closing(sqlite3.connect(backup)) as saved:
                db.backup(saved)
            with db:
                db.execute('BEGIN IMMEDIATE')
                db.execute('ALTER TABLE commits RENAME COLUMN snapshot TO snapshot_path')
                db.execute("UPDATE commits SET snapshot_path='graphs/' || sha || '.json.gz'")
                db.execute('PRAGMA user_version=2')
                if db.execute('PRAGMA foreign_key_check').fetchall():
                    raise ValueError('Migration foreign-key failure')
            db.execute('VACUUM')
            if db.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                raise ValueError('Migrated database integrity check failed')
    return {'status': 'migrated', 'commits': count, 'before_bytes': before,
            'after_bytes': path.stat().st_size, 'backup': str(backup)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, default=ROOT / 'store/timeline.sqlite')
    args = parser.parse_args()
    result = migrate(args.database)
    (ROOT / 'reports/timeline-storage-migration.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
