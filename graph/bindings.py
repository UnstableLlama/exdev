# SPDX-License-Identifier: MIT
"""Conservative direct pybind function links, with call-site and binding evidence."""
import ast
from collections import defaultdict
import hashlib
import re

VERSION = 1


def definitions(files):
    result = defaultdict(list)
    for path, source in sorted(files.items()):
        if not path.endswith(('.cpp', '.cc', '.cu')):
            continue
        # Preserve strings and line numbers while masking comments.
        pattern = r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/'
        clean = re.sub(pattern, lambda m: re.sub(r'[^\n]', ' ', m[0]) if m[0].startswith(('/',)) else m[0], source)
        for match in re.finditer(r'\bm\.def\s*\(\s*"(\w+)"\s*,\s*&([A-Za-z_]\w*)\s*[,)]', clean):
            result[match[1]].append(dict(target=match[2], file=path, line=source.count('\n', 0, match.start())+1,
                                          source_hash=hashlib.sha256(source.encode()).hexdigest()))
    return result


def supplement(snapshot, files):
    bindings = definitions(files)
    native, owners = defaultdict(list), defaultdict(list)
    for n in snapshot['nodes']:
        if n['kind'] in ('Function', 'Method'):
            if n['file'].endswith(('.cu', '.cpp', '.c', '.cc')):
                native[n['name']].append(n)
            if n['file'].endswith('.py'):
                owners[n['file']].append(n)
    backend = {(a, b) for a, kind, b in snapshot['edges'] if kind == 'CALLS'}
    sites, errors, added = [], [], {}
    for path, source in sorted(files.items()):
        if not path.endswith('.py'):
            continue
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            errors.append(dict(file=path, line=e.lineno, message=e.msg))
            continue
        aliases = set()
        for n in tree.body:
            if isinstance(n, ast.ImportFrom) and n.module and (n.module == 'ext' or n.module.endswith('.ext')):
                aliases.update(a.asname or a.name for a in n.names if a.name == 'exllamav3_ext')
        # Conservative: any reassignment or argument with this name makes its identity uncertain.
        shadowed = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del))}
        shadowed.update(n.arg for n in ast.walk(tree) if isinstance(n, ast.arg))
        for n in ast.walk(tree):
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                for a in n.names:
                    if a.name != 'exllamav3_ext':
                        shadowed.add(a.asname or a.name.split('.')[0])
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                shadowed.add(n.name)
        for c in ast.walk(tree):
            if not (isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) and isinstance(c.func.value, ast.Name)
                    and c.func.value.id in aliases):
                continue
            candidates = sorted([n for n in owners[path] if n['start'] <= c.lineno <= n['end']], key=lambda n:n['end']-n['start'])
            owner = candidates[0]['qn'] if candidates else None
            defs = bindings.get(c.func.attr, [])
            names = {d['target'] for d in defs}
            targets = sorted({n['qn'] for name in names for n in native[name]})
            site = dict(sha=snapshot['sha'], file=path, line=c.lineno, binding=c.func.attr, source=owner,
                        candidates=targets, target=None, status='unresolved')
            if c.func.value.id in shadowed:
                site['status'] = 'shadowed_alias'
            elif not owner:
                site['status'] = 'no_indexed_caller'
            elif not defs:
                site['status'] = 'no_direct_binding'
            elif len(names) != 1 or len(targets) > 1:
                site['status'] = 'ambiguous_native_target'
            elif not targets:
                site['status'] = 'missing_native_target'
            else:
                target = targets[0]
                site['target'] = target
                site['status'] = 'backend_present' if (owner,target) in backend else 'supplemented'
                if site['status'] == 'supplemented':
                    edge = added.setdefault((owner,target),dict(source=owner,target=target,type='CALLS',
                              origin='pybind-direct-v1',sha=snapshot['sha'],evidence=[]))
                    for d in defs:
                        edge['evidence'].append(dict(file=path,line=c.lineno,binding=c.func.attr,
                             source_hash=hashlib.sha256(source.encode()).hexdigest(), binding_file=d['file'],
                             binding_line=d['line'],binding_source_hash=d['source_hash']))
            sites.append(site)
    return dict(version=VERSION,sha=snapshot['sha'],edges=[added[k] for k in sorted(added)],sites=sites,parse_errors=errors)
