#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 UnstableLlama and exdev contributors
"""Sequential review packets and provenance-preserving entry authoring."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from mine import git, text, atomic_json, parent_checkout
from history_policy import eligible_ancestors, merge_policy, validate_entry_links

DATA = Path('data/exllamav3-v5')
ENTRIES = Path('encyclopedia/entries')
REPO = Path('.sources/exllamav3.git')

def record(position):
    paths = list((DATA / 'records').glob(f'{position:06d}_*.json'))
    if len(paths) != 1: raise ValueError('Expected one raw record')
    return paths[0], json.loads(paths[0].read_text())

def entry_context(raw):
    """Return only completed strict-ancestor entries; no ordinal-only context."""
    allowed = eligible_ancestors(REPO, raw['sha'])
    positions = {p.name.split('_', 1)[1].removesuffix('.json'): int(p.name.split('_', 1)[0])
                 for p in (DATA / 'records').glob('*.json')}
    entries = {}
    for sha in allowed:
        if sha not in positions:
            raise ValueError('Ancestor is absent from the pinned mined history')
        position = positions[sha]
        path = ENTRIES / f'{position:06d}.json'
        if not path.exists():
            raise ValueError(f'Ancestor entry missing: {position:06d}')
        entry = json.loads(path.read_text())
        if entry['sha'] != sha:
            raise ValueError('Ancestor entry identity mismatch')
        entries[position] = entry
    return entries


def write(position, annotation):
    path, raw = record(position)
    context = entry_context(raw)
    target = ENTRIES / f'{position:06d}.json'
    if target.exists(): raise ValueError('Entry already exists; review explicitly before editing')
    required = {'problem','reasoning','impact','source_notes','confidence','links','type','status'}
    if not required <= annotation.keys(): raise ValueError('Missing fields: ' + str(required - annotation.keys()))
    allowed_fields = required | {'external_sources', 'review_log', 'merge_analysis'}
    if set(annotation) - allowed_fields:
        raise ValueError('Unknown or protected annotation fields')
    validate_entry_links(REPO, raw['sha'], annotation['links'], context)
    policy = merge_policy(REPO, raw['sha'])
    if policy['is_merge']:
        policy['introduced_entry_positions'] = sorted(i for i, e in context.items() if e['sha'] in policy['introduced_shas'])
        if annotation.get('merge_analysis', {}).get('independent_training_example'):
            raise ValueError('Merge examples require separate resolution review; cannot override integration policy')
    entry = {k: raw[k] for k in ('position','sha','parent_sha','parent_shas','author','author_date','commit_date','message','files_touched','noise')}
    entry.update({'rights':raw.get('rights'), 'raw_record':str(path),'raw_record_sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'diff_sha256':raw['diff_sha256'],
                  'created_at':datetime.now(timezone.utc).isoformat(), 'reviewed':False, 'external_reference_candidates':raw['references']})
    entry.update(annotation)
    entry['merge_policy'] = policy
    atomic_json(target,entry)
    content = f"# {position:06d} — {raw['message'].splitlines()[0]}\n\n"
    content += f"Commit `{raw['sha']}` · {raw['commit_date']} · {raw['author']}\n\nParent: `{raw['parent_sha'] or 'empty tree (root)'}`. Type: **{entry['type']}**. Status: **{entry['status']}**.\n\n"
    content += f"[Full identity, files and source ledger]({position:06d}.json) · [Upstream commit](https://github.com/turboderp-org/exllamav3/commit/{raw['sha']}) · [Local raw message and complete binary-capable diff](../../{path})\n\n"
    for key in ('problem','reasoning','impact','source_notes','confidence'):
        content += f"## {key.replace('_',' ').title()}\n\n{entry[key]}\n\n"
    content += '## Earlier entries\n\n' + (', '.join(f'[{i:06d}]({i:06d}.md)' for i in entry['links']) or 'None (root).') + '\n'
    target.with_suffix('.md').write_text(content)
    db=sqlite3.connect(DATA/'index.sqlite3'); db.execute('PRAGMA foreign_keys=ON')
    db.execute('UPDATE commits SET encyclopedia_status=? WHERE sha=?',(entry['status'],raw['sha'])); db.commit(); db.close()

def show(position):
    path,r=record(position)
    context = entry_context(r)
    print('ELIGIBLE_ANCESTOR_ENTRIES:', sorted(context))
    print('MERGE_POLICY:', json.dumps(merge_policy(REPO, r['sha'])))
    print(json.dumps({k:v for k,v in r.items() if k not in ('diff','references')},indent=2))
    print('REFERENCES',json.dumps({k:v for k,v in r['references'].items() if k!='embedded_data_urls'}))
    for block in r['diff'].split('diff --git '):
        if not block: continue
        if 'GIT binary patch' in block or '/standard_cal_data/' in block:
            print('OMITTED from display only:', block.splitlines()[0]); continue
        print('diff --git '+block)
    dest=Path('worktrees')/f'{position:06d}-parent'
    if not dest.exists(): parent_checkout(REPO,r['sha'],dest)
    print('PARENT_FILES:',dest)

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['show','write']); p.add_argument('position',type=int); p.add_argument('--annotation',type=Path); a=p.parse_args()
    if a.command=='show': show(a.position)
    else: write(a.position,json.loads(a.annotation.read_text()))
