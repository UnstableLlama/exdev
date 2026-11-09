#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 UnstableLlama and exdev contributors
"""Deterministic first-parent diffs over a complete, parent-before-child DAG walk."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import tarfile

VERSION = 5
DEFAULT_URL = 'https://github.com/turboderp-org/exllamav3.git'

def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])

def text(raw):
    return raw.decode('utf-8', errors='surrogateescape')

def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n')
    temp.replace(path)

def references(body):
    urls = sorted(set(u.rstrip('.,;:)]}>\\') for u in re.findall(r'https?://[^\s<>"\x00)\]]+', body)))
    hf = set(re.findall(r'(?:huggingface\.co|hf\.co)/([\w.-]+/[\w.-]+)', body))
    hf.update(re.findall(r'(?:repo_id|model_name_or_path|model_id)\s*[=:]\s*[\'"]([\w.-]+/[\w.-]+)', body))
    hf = {v for v in hf if v.split('/')[0] not in {'collections', 'datasets', 'spaces', 'docs', 'organizations', 'api', 'settings'}}
    qualified = set(re.findall(r'[\w.-]+/[\w.-]+#\d+', body))
    qualified.update(owner + '#' + number for owner, number in re.findall(r'github\.com/([\w.-]+/[\w.-]+)/(?:issues|pull)/(\d+)', body))
    models = sorted(set(re.findall(r'\b(?:Llama|Qwen|Mistral|Mixtral|Gemma|Phi|DeepSeek|GPT|Falcon|Yi|OLMo|Granite|SmolLM|InternLM)(?:[0-9][\w.\-]*|[-.][\w.\-]*|\b)', body, re.I)))
    return {'urls': urls, 'papers': [u for u in urls if any(h in u for h in ('arxiv.org/', 'doi.org/', 'openreview.net/', 'aclanthology.org/'))],
            'hf_repositories': sorted(hf), 'issue_pr_numbers': sorted(set(re.findall(r'(?<![\w])#(\d+)\b', body)), key=int),
            'qualified_issues': sorted(qualified), 'model_name_candidates': models}

def diff_references(message, diff):
    technical, embedded = [message], []
    is_data = False
    binary = False
    for line in diff.splitlines():
        if line.startswith('diff --git '):
            is_data = '/standard_cal_data/' in line
            binary = False
        if line == 'GIT binary patch': binary = True
        if binary or line.startswith(('+++', '---')): continue
        if line[:1] in ('+', '-', ' '):
            (embedded if is_data else technical).append(line[1:])
    result = references('\n'.join(technical))
    result['embedded_data_urls'] = references('\n'.join(embedded))['urls']
    return result

def classify(message, files, diff, whitespace_only):
    low = message.lower()
    if not diff.strip(): return 'noise', True, 'No tree change against first parent (empty root/merge/commit).'
    if files and all(re.search(r'(^|/)(version\.py|version\.txt|VERSION)$', f) for f in files) and re.search('version|bump', low):
        return 'noise', True, 'Version-only paths and version/bump message.'
    if files and all(re.search(r'(^|/)(docs?|readme|license|copying)(/|\.|$)|\.(md|rst)$', f, re.I) for f in files):
        if re.search(r'\bformat(?:ting)?\b', low):
            changed = {'+': [], '-': []}
            for line in diff.splitlines():
                if line[:1] in changed and not line.startswith(('+++', '---')):
                    normalized = re.sub(r'<[^>]+>', '', line[1:])
                    normalized = re.sub(r'^#+\s*', '', normalized).strip()
                    if normalized: changed[line[0]].append(normalized)
            if changed['+'] == changed['-']:
                return 'noise', True, 'Documentation formatting with identical text after stripping headings and HTML tags.'
        return 'docs', False, 'Only documentation paths; heuristic requires review.'
    if re.search(r'\bdocstrings?\b', low): return 'docs', False, 'Docstring change identified in message; requires review.'
    rules = [('bugfix', r'fix|bug|correct|crash|overflow|regression'),
             ('new architecture support', r'(?:support|add|implement).*(?:llama|qwen|mistral|gemma|phi|deepseek|architecture|model)|(?:llama|qwen|mistral|gemma|phi|deepseek).*support'),
             ('performance', r'perf|optim|speed|faster|memory|bandwidth|vram|golden section|skip gc'),
             ('refactor', r'refactor|cleanup|clean up|rename|reorgan|simplif'),
             ('docs', r'^(?:docs?|readme|documentation)\b')]
    for tag, pattern in rules:
        if re.search(pattern, low): return tag, False, 'Commit-message heuristic: ' + pattern
    return 'feature', False, 'Default for substantive changes; requires review.'

def parent_checkout(repo, sha, dest):
    """Export parent files without .git, preventing accidental future-history reads."""
    sha = text(git(repo, 'rev-parse', '--verify', sha + '^{commit}')).strip()
    parents = text(git(repo, 'show', '-s', '--format=%P', sha)).split()
    dest = Path(dest)
    if dest.exists(): raise ValueError('Destination must not exist')
    dest.mkdir(parents=True)
    if parents:
        with tarfile.open(fileobj=io.BytesIO(git(repo, 'archive', parents[0]))) as archive:
            archive.extractall(dest, filter='data')
    return parents[0] if parents else None

def mine(repo, out, ref='HEAD'):
    repo, out = Path(repo).resolve(), Path(out)
    if text(git(repo, 'rev-parse', '--is-shallow-repository')).strip() == 'true':
        raise ValueError('Full history required; shallow repositories are not supported')
    out.mkdir(parents=True, exist_ok=True)
    project = Path(__file__).resolve().parents[1]
    for source, target in [('LICENSE','LICENSE'), ('NOTICE','NOTICE'), ('ATTRIBUTION.md','ATTRIBUTION.md'), ('LICENSES/exllamav3-MIT.txt','LICENSES/exllamav3-MIT.txt')]:
        if (project/source).exists():
            (out/target).parent.mkdir(parents=True, exist_ok=True)
            (out/target).write_bytes((project/source).read_bytes())
    review_path = project / 'seeds/type-reviews.json'
    reviews = json.loads(review_path.read_text()) if review_path.exists() else {}
    review_hash = hashlib.sha256(review_path.read_bytes()).hexdigest() if review_path.exists() else None
    manifest_path = out / 'manifest.json'
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        if manifest['miner_version'] != VERSION: raise ValueError('Miner version changed; use a new output directory')
        if manifest.get('type_reviews_sha256') != review_hash: raise ValueError('Type reviews changed; use a new output directory')
        head = manifest['head']
    else:
        head = text(git(repo, 'rev-parse', '--verify', ref + '^{commit}')).strip()
        manifest = {'type_reviews_sha256': review_hash, 'miner_version': VERSION, 'head': head, 'retrieved_at': datetime.now(timezone.utc).isoformat(),
                    'source_url': text(git(repo, 'config', '--get', 'remote.origin.url')).strip() if (repo / 'config').exists() else str(repo),
                    'order': 'git rev-list --reverse --topo-order: all reachable commits, parents before children; timestamps do not override ancestry',
                    'diff_policy': 'root against empty tree; merge against first parent; all parents retained'}
        atomic_json(manifest_path, manifest)
    commits = text(git(repo, 'rev-list', '--reverse', '--topo-order', head)).splitlines()
    db = sqlite3.connect(out / 'index.sqlite3')
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript('CREATE TABLE IF NOT EXISTS commits(position INTEGER PRIMARY KEY, sha TEXT UNIQUE NOT NULL, record_path TEXT NOT NULL, record_sha256 TEXT NOT NULL, type TEXT NOT NULL, noise INTEGER NOT NULL, encyclopedia_status TEXT NOT NULL DEFAULT "pending");')
    counts, noise_count, all_refs = Counter(), 0, defaultdict(set)
    for pos, sha in enumerate(commits, 1):
        path = out / 'records' / f'{pos:06d}_{sha}.json'
        if path.exists():
            record = json.loads(path.read_text())
            if record['sha'] != sha or record['position'] != pos: raise ValueError('Record identity mismatch')
            old = db.execute('SELECT record_sha256 FROM commits WHERE sha=?', (sha,)).fetchone()
            if old and old[0] != hashlib.sha256(path.read_bytes()).hexdigest(): raise ValueError('Record checksum mismatch: ' + str(path))
        else:
            fields = git(repo, 'show', '-s', '--format=%H%x00%P%x00%an%x00%ae%x00%aI%x00%cI%x00%B', sha).split(b'\0', 6)
            _, parents, author, email, date, committed, message = map(text, fields)
            parents = parents.split()
            base = parents[0] if parents else text(git(repo, 'hash-object', '-t', 'tree', '--stdin')).strip()
            raw_diff = git(repo, 'diff', '--binary', '--full-index', '--no-ext-diff', '--no-textconv', base, sha, '--')
            files = text(git(repo, 'diff', '--name-only', '-z', base, sha, '--')).strip('\0').split('\0') if raw_diff else []
            whitespace_only = bool(raw_diff) and not git(repo, 'diff', '--ignore-all-space', '--ignore-blank-lines', base, sha, '--')
            tag, noise, reason = classify(message, files, text(raw_diff), whitespace_only)
            automatic_type = tag
            if sha in reviews:
                tag, noise, reason = reviews[sha]['type'], reviews[sha]['noise'], reviews[sha]['reason']
            license_tree = text(git(repo, 'ls-tree', sha, '--', 'LICENSE')).strip()
            record = {'rights': {'upstream': DEFAULT_URL.removesuffix('.git'), 'copyright_notice': 'Copyright (c) 2025 Turboderp',
                       'distribution_notice': 'LICENSES/exllamav3-MIT.txt',
                       'license_blob_at_commit': license_tree.split()[2] if license_tree else None,
                       'scope': 'Upstream notice does not relicense separately attributed third-party material; missing historical LICENSE is recorded as null.'},
                      'schema_version': 1, 'position': pos, 'sha': sha, 'parent_sha': parents[0] if parents else None,
                      'parent_shas': parents, 'author': author, 'author_email': email, 'author_date': date, 'commit_date': committed,
                      'message': message.rstrip('\n'), 'diff': text(raw_diff), 'diff_sha256': hashlib.sha256(raw_diff).hexdigest(),
                      'files_touched': files, 'references': diff_references(message, text(raw_diff)),
                      'type': tag, 'noise': noise, 'classification_reason': reason, 'reviewed': sha in reviews, 'automatic_type': automatic_type}
            atomic_json(path, record)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        db.execute('INSERT INTO commits(position,sha,record_path,record_sha256,type,noise) VALUES(?,?,?,?,?,?) ON CONFLICT(sha) DO UPDATE SET record_sha256=excluded.record_sha256', (pos,sha,str(path),digest,record['type'],record['noise']))
        db.commit()
        counts[record['type']] += 1; noise_count += record['noise']
        for kind, vals in record['references'].items():
            for val in vals: all_refs[(kind,val)].add(pos)
    report = {'head': head, 'total_commits': len(commits), 'counts_per_type': dict(sorted(counts.items())), 'noise_count': noise_count,
              'references': [{'kind': k, 'value': v, 'positions': sorted(ps)} for (k,v),ps in sorted(all_refs.items())],
              'limitations': ['References are lexical candidates, not verified entities. Dynamic URLs and unnamed models require manual analysis.', 'Tags are heuristics; noise is conservative.', 'Pinned to manifest head; a later upstream fetch cannot silently expand this run.']}
    atomic_json(out / 'report.json', report)
    assert not db.execute('PRAGMA foreign_key_check').fetchall()
    db.close()
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    p = subs.add_parser('mine'); p.add_argument('--repo', type=Path, default=Path('.sources/exllamav3.git')); p.add_argument('--out', type=Path, default=Path('data/exllamav3-v5')); p.add_argument('--url', default=DEFAULT_URL); p.add_argument('--ref', default='HEAD')
    p = subs.add_parser('parent'); p.add_argument('sha'); p.add_argument('destination', type=Path); p.add_argument('--repo', type=Path, default=Path('.sources/exllamav3.git'))
    args = parser.parse_args()
    if args.command == 'parent': print(parent_checkout(args.repo, args.sha, args.destination)); return
    if not args.repo.exists():
        args.repo.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['git', 'clone', '--bare', args.url, str(args.repo)], check=True)
    report = mine(args.repo, args.out, args.ref)
    print(json.dumps({k:v for k,v in report.items() if k != 'references'}, indent=2))

if __name__ == '__main__': main()
