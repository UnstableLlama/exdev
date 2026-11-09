# SPDX-License-Identifier: MIT
"""Four-snapshot feasibility check. Does not author entries or walk full history."""
import ast
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.graph-work/exllamav3'
BIN = ROOT / '.tools/cbm-v0.12.1/codebase-memory-mcp'
PIN = '77745491f0a9c346d6da23eed4d92b5feaa31a27a883c9faa4fa9f47c8183705'
OUT = ROOT / 'data/graph/validation'


def stable_symbols(before, after):
    def grouped(nodes):
        groups = collections.defaultdict(list)
        for n in nodes:
            if n.get('body_hash'):
                groups[tuple(n[k] for k in ('file', 'kind', 'name', 'body_hash'))].append(n['qn'])
        return groups
    a, b = grouped(before), grouped(after)
    pairs = [(a[k][0], b[k][0]) for k in a.keys() & b.keys() if len(a[k]) == len(b[k]) == 1]
    drift = sorted([list(p) for p in pairs if p[0] != p[1]])
    return dict(comparable=len(pairs), stable=len(pairs)-len(drift), drift=drift)


def binding_definitions(source):
    found = collections.defaultdict(set)
    for name, target in re.findall(r'\bm\.def\s*\(\s*"(\w+)"\s*,\s*&([\w:]+)', source):
        found[name].add(target)
    return dict(found)


def call(tool, args, cache, log):
    env = dict(os.environ, CBM_CACHE_DIR=str(cache), CBM_WORKERS='4')
    p = subprocess.run([str(BIN), 'cli', '--json', tool], input=json.dumps(args), text=True,
                       capture_output=True, env=env, timeout=600)
    log.write_text(p.stdout + '\nSTDERR\n' + p.stderr)
    if p.returncode:
        raise RuntimeError(f'{tool} failed; see {log}')
    result = json.loads(p.stdout)
    if result.get('isError'):
        raise RuntimeError(f'{tool} error; see {log}')
    return result.get('structuredContent') or json.loads(result['content'][0]['text'])


def export(query, cache, folder, name):
    rows, offset = [], 0
    while True:
        r = call('query_graph', dict(project='exllamav3', query=query, format='json',
                 max_rows=1000, offset=offset, max_output_tokens=100000), cache, folder / f'{name}-{offset}.log')
        batch = r['rows']
        rows.extend(batch)
        if not r.get('has_more') and not r.get('truncated'):
            break
        if not batch:
            raise RuntimeError('Export truncated without progress')
        offset += len(batch)
    return rows


def analyze(nodes, edges):
    calls = {(a, b) for a, t, b in edges if t == 'CALLS'}
    byfile = collections.defaultdict(list)
    native = collections.defaultdict(list)
    for n in nodes:
        byfile[n['file']].append(n)
        if n['kind'] in ('Function', 'Method') and Path(n['file']).suffix in ('.cpp', '.cu', '.c'):
            native[n['name']].append(n)
    bindings = collections.defaultdict(set)
    for p in WORK.rglob('*bindings*.cpp'):
        for k, v in binding_definitions(p.read_text()).items():
            bindings[k].update(v)
    sites, python_calls, parse_errors = [], [], []
    for p in WORK.rglob('*.py'):
        rel = str(p.relative_to(WORK))
        try:
            tree = ast.parse(p.read_text())
        except (SyntaxError, UnicodeError) as e:
            parse_errors.append(dict(file=rel, error=str(e)))
            continue
        aliases = {a.asname or a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)
                   for a in n.names if a.name == 'exllamav3_ext'}
        funcs = [n for n in byfile[rel] if n['kind'] in ('Function', 'Method')]
        for c in ast.walk(tree):
            if not isinstance(c, ast.Call):
                continue
            owners = sorted([n for n in funcs if n['start'] <= c.lineno <= n['end']], key=lambda n: n['end']-n['start'])
            owner = owners[0]['qn'] if owners else None
            if isinstance(c.func, ast.Name) and owner:
                targets = [n for n in funcs if n['name'] == c.func.id]
                if len(targets) == 1:
                    python_calls.append(dict(source=owner, target=targets[0]['qn'], file=rel, line=c.lineno,
                                             found=(owner, targets[0]['qn']) in calls))
            if not (isinstance(c.func, ast.Attribute) and isinstance(c.func.value, ast.Name) and c.func.value.id in aliases):
                continue
            targets = [n['qn'] for target in bindings.get(c.func.attr, ()) for n in native.get(target, ())]
            target = targets[0] if len(targets) == 1 else None
            sites.append(dict(file=rel, line=c.lineno, binding=c.func.attr, source=owner, target=target,
                              candidates=targets, backend_found=bool(owner and target and (owner, target) in calls)))
    resolved = [s for s in sites if s['source'] and s['target']]
    return dict(binding_sites=sites, resolved_binding_sites=len(resolved),
                missing_binding_sites=sum(not s['backend_found'] for s in resolved),
                unresolved_binding_sites=len(sites)-len(resolved),
                python_direct_calls=python_calls, python_direct_found=sum(s['found'] for s in python_calls),
                python_parse_errors=parse_errors)


def main():
    if hashlib.sha256(BIN.read_bytes()).hexdigest() != PIN:
        raise RuntimeError('Backend binary does not match pin')
    records = sorted((ROOT / 'data/exllamav3-v5/records').glob('*.json'))
    selected = [records[i] for i in (0, (len(records)-1)//3, 2*(len(records)-1)//3, len(records)-1)]
    snapshots = []
    for record in selected:
        rec = json.loads(record.read_text())
        sha = rec['sha']
        folder = OUT / sha
        folder.mkdir(parents=True, exist_ok=True)
        complete = folder / 'result.json'
        if complete.exists():
            snapshots.append(json.loads(complete.read_text()))
            print(f'Reused {rec["position"]}: {sha}', flush=True)
            continue
        if subprocess.check_output(['git', '-C', str(WORK), 'status', '--porcelain'], text=True).strip():
            raise RuntimeError('Validation worktree has local changes')
        subprocess.run(['git', '-C', str(WORK), 'checkout', '--detach', sha], check=True, capture_output=True)
        # Unique clean cache per attempt; no stale symbols from an earlier checkout.
        cache = folder / f'cache-{time.time_ns()}'
        start = time.monotonic()
        index = call('index_repository', dict(repo_path=str(WORK), name='exllamav3', mode='full'), cache, folder / 'index.log')
        print(f'Indexed {rec["position"]}: {sha}', flush=True)
        nr = export('MATCH (n) RETURN n.qualified_name, n.name, n.label, n.file_path, n.start_line, n.end_line ORDER BY n.qualified_name', cache, folder, 'nodes')
        edges = export('MATCH (a)-[r]->(b) RETURN a.qualified_name, type(r), b.qualified_name ORDER BY a.qualified_name, b.qualified_name', cache, folder, 'edges')
        nodes = []
        for qn, name, kind, file, first, last in nr:
            n = dict(qn=qn, name=name, kind=kind, file=file, start=int(first or 0), end=int(last or 0))
            path = WORK / file
            if file and path.is_file() and n['start'] > 0 and n['end'] >= n['start']:
                lines = path.read_bytes().splitlines(keepends=True)
                n['body_hash'] = hashlib.sha256(b''.join(lines[n['start']-1:n['end']])).hexdigest()
            nodes.append(n)
        with sqlite3.connect(f'file:{cache}/exllamav3.db?mode=ro', uri=True) as db:
            counts = [db.execute(f"SELECT count(*) FROM {table} WHERE project = 'exllamav3'").fetchone()[0] for table in ('nodes', 'edges')]
            if counts != [len(nodes), len(edges)]:
                raise RuntimeError(f'Incomplete export: {counts} != {[len(nodes), len(edges)]}')
            with sqlite3.connect(folder / 'snapshot.db') as dest:
                db.backup(dest)
        analysis = analyze(nodes, edges)
        # Trace source-verified direct Python calls; store full backend response for review.
        examples = list(dict.fromkeys(s['source'] for s in analysis['python_direct_calls']))[:5]
        traces = []
        for i, qn in enumerate(examples):
            traces.append(dict(source=qn, result=call('trace_path', dict(project='exllamav3', function_name=qn,
                          direction='outbound', depth=2, limit=100, format='json', include_tests=True), cache, folder / f'trace-{i}.log')))
        result = dict(sha=sha, position=rec['position'], parents=rec['parent_shas'], backend='0.12.1',
                      nodes=nodes, edges=edges, index=index, analysis=analysis, traces=traces,
                      seconds=round(time.monotonic()-start, 2))
        complete.write_text(json.dumps(result, indent=2)+'\n')
        snapshots.append(result)
        print(f'Validated {len(nodes)} nodes, {len(edges)} edges; {analysis["missing_binding_sites"]} missing binding call sites', flush=True)
    summary = []
    for s in snapshots:
        a = s['analysis']
        summary.append(dict(sha=s['sha'], position=s['position'], nodes=len(s['nodes']), edges=len(s['edges']),
                            seconds=s['seconds'], resolved_binding_sites=a['resolved_binding_sites'],
                            missing_binding_sites=a['missing_binding_sites'], unresolved_binding_sites=a['unresolved_binding_sites'],
                            python_direct_calls=len(a['python_direct_calls']), python_direct_found=a['python_direct_found'],
                            python_parse_errors=a['python_parse_errors'], index=s['index']))
    stability = [dict(before=a['sha'], after=b['sha'], **stable_symbols(a['nodes'], b['nodes']))
                 for a, b in zip(snapshots, snapshots[1:])]
    (ROOT / 'reports/graph-validation.json').write_text(json.dumps(dict(snapshots=summary, stability=stability), indent=2)+'\n')

if __name__ == '__main__':
    main()
