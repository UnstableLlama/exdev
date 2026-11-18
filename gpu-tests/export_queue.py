#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write gpu-tests/queue.json from the latest revision of every defect-ledger identity. Reads only."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT/'reports/defect-ledger'
EXECUTED = {'repository_execution'}
AREAS = (('packaging_ci', ('.github/', 'setup.py', 'requirements', 'pyproject')),
         ('native_ext', ('exllamav3_ext', '.cu', '.cpp', 'kernel')),
         ('conversion', ('conversion/', 'convert', 'quantiz', 'calibrat')),
         ('eval_script', ('eval/', 'science/', 'examples/', 'util/')))


def latest():
    records = {}
    for path in LEDGER.glob('*--r*.json'):
        match = re.fullmatch(r'(.+)--r(\d+)\.json', path.name)
        if match and int(match[2]) >= records.get(match[1], (0, None))[0]:
            records[match[1]] = (int(match[2]), path)
    return [path for _, path in sorted(records.values(), key=lambda item: item[1].name)]


def shas(rows):
    return [row['sha'] for row in rows or [] if isinstance(row, dict) and re.fullmatch(r'[0-9a-f]{40}', row.get('sha', ''))]


def methods(record):
    checks = record.get('verification')
    if isinstance(checks, dict):
        checks = checks.get('checks', [checks])
    return sorted({c.get('method', 'unspecified') for c in checks or [] if isinstance(c, dict)})


def area(record):
    text = json.dumps([record.get(k) for k in ('trigger', 'actual_behavior', 'introductions', 'observations')]).lower()
    return next((name for name, words in AREAS if any(word in text for word in words)), 'runtime')


def item(path):
    raw = path.read_bytes()
    record = json.loads(raw)
    affected = record.get('affected_revisions') or {}
    verified = [s for s in affected.get('verified_shas', []) if re.fullmatch(r'[0-9a-f]{40}', s)]
    fixes, used = shas(record.get('fixes')), methods(record)
    executed = bool(EXECUTED & set(used))
    suspected = record['status'] == 'suspected'
    priority = (1 if suspected and fixes else 2 if suspected and record['classification'] == 'defect' and not executed
                else 3 if suspected else 4)
    return {'priority': priority, 'defect_id': record['defect_id'], 'ledger_revision': record['revision_id'],
            'ledger_file': str(path.relative_to(ROOT)), 'ledger_sha256': hashlib.sha256(raw).hexdigest(),
            'status': record['status'], 'classification': record['classification'], 'area_hint': area(record),
            'description': record['description'], 'trigger': record['trigger'],
            'expected_behavior': record['expected_behavior'], 'actual_behavior': record['actual_behavior'],
            'commits': {'introductions': shas(record.get('introductions')), 'verified_affected': verified,
                        'latest_affected': verified[-1] if verified else None, 'fixes': fixes},
            'affected_limits': affected.get('limits'), 'existing_methods': used, 'already_executed': executed}


def main():
    items = sorted((item(path) for path in latest()), key=lambda i: (i['priority'], i['defect_id']))
    done = {p.name for p in (ROOT/'gpu-tests/results').iterdir() if p.is_dir()} if (ROOT/'gpu-tests/results').is_dir() else set()
    for entry in items:
        entry['has_result'] = entry['defect_id'] in done
    out = {'schema_version': 1, 'source': 'reports/defect-ledger (latest revision per identity)',
           'counts': {str(p): sum(i['priority'] == p for i in items) for p in (1, 2, 3, 4)}, 'items': items}
    (ROOT/'gpu-tests/queue.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps(out['counts']), len(items), 'items;', sum(i['has_result'] for i in items), 'with results')


if __name__ == '__main__':
    main()
