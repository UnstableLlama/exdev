# SPDX-License-Identifier: MIT
"""Worker for a single tool invocation inside an allowlisted, networkless container."""
from datetime import datetime
import hashlib
import base64
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile


def safe_path(value, root_allowed=False):
    if not isinstance(value, str) or '\x00' in value or '\\' in value:
        raise ValueError('Invalid repository path')
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or '.git' in p.parts:
        raise ValueError('Path is outside the allowed repository view')
    clean = str(p)
    if clean == '.':
        if root_allowed:
            return ''
        raise ValueError('File path required')
    return clean


def args_for(name, args):
    schema_path = Path(__file__).resolve().parents[1]/'schema/repo-tools-v1.json'
    schemas = {t['name']:t['parameters'] for t in json.loads(schema_path.read_text())['tools']}
    if name not in schemas and name in ('graph_search','graph_trace','graph_query','symbol_history','repo_map'):
        from graph.tools import arguments
        return arguments(name, args)
    if name not in schemas or not isinstance(args, dict):
        raise ValueError('Unknown tool or invalid arguments')
    schema = schemas[name]
    props = schema['properties']
    if set(args)-set(props) or set(schema['required'])-set(args):
        raise ValueError('Missing or unknown tool arguments')
    result = {k:v['default'] for k,v in props.items() if 'default' in v}
    result.update(args)
    for key, value in result.items():
        rule = props[key]
        kind = rule['type']
        if kind == 'integer':
            if type(value) is not int or not rule['minimum'] <= value <= rule['maximum']:
                raise ValueError('Invalid ' + key)
        elif kind == 'string':
            if not isinstance(value, str) or len(value) < rule.get('minLength', 0):
                raise ValueError('Invalid ' + key)
        elif kind == 'array':
            if not isinstance(value, list) or not rule['minItems'] <= len(value) <= rule['maxItems'] or any(not isinstance(x,str) for x in value):
                raise ValueError('Invalid ' + key)
        elif kind == 'object':
            if not isinstance(value, dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in value.items()):
                raise ValueError('Invalid ' + key)
    return result


def load_blob(packet, digest):
    if not isinstance(digest, str) or re.fullmatch('[0-9a-f]{64}', digest) is None:
        raise ValueError('Invalid blob identity')
    path = packet/'blobs'/digest
    if path.is_symlink():
        raise ValueError('Packet blobs must not be symlinks')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != digest:
        raise ValueError('Packet blob checksum mismatch')
    return data


def excerpt(data, args):
    start = args.get('offset', 0)
    end = start + args.get('max_bytes', 16384)
    chunk = data[start:end]
    result = {'offset': start, 'next_offset': min(end, len(data)), 'truncated': end < len(data)}
    try:
        result.update(text=chunk.decode('utf-8'), encoding='utf-8')
    except UnicodeDecodeError:
        result.update(base64=base64.b64encode(chunk).decode('ascii'), encoding='base64')
    return result


def single_process_filter():
    # Applied only to the run child, before exec. It persists across exec and cannot
    # be removed by source code. This basic runtime intentionally disallows threads.
    import ctypes
    import errno
    seccomp = ctypes.CDLL('libseccomp.so.2', use_errno=True)
    seccomp.seccomp_init.argtypes = [ctypes.c_uint32]
    seccomp.seccomp_init.restype = ctypes.c_void_p
    seccomp.seccomp_syscall_resolve_name.argtypes = [ctypes.c_char_p]
    seccomp.seccomp_syscall_resolve_name.restype = ctypes.c_int
    seccomp.seccomp_rule_add.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_int, ctypes.c_uint]
    seccomp.seccomp_load.argtypes = [ctypes.c_void_p]
    seccomp.seccomp_release.argtypes = [ctypes.c_void_p]
    context = seccomp.seccomp_init(0x7fff0000)
    if not context:
        raise RuntimeError('Cannot allocate run syscall filter')
    try:
        for name in (b'clone', b'clone3', b'fork', b'vfork', b'unshare', b'setns', b'ptrace'):
            number = seccomp.seccomp_syscall_resolve_name(name)
            if number < 0 or seccomp.seccomp_rule_add(context, 0x00050000 | errno.EPERM, number, 0):
                raise RuntimeError('Cannot configure run syscall filter')
        if seccomp.seccomp_load(context):
            raise RuntimeError('Cannot install run syscall filter')
    finally:
        seccomp.seccomp_release(context)


def evidence_item(manifest, args, kind):
    matches=[]
    for e in manifest['evidence']:
        if e['kind'] != kind:
            continue
        fields = ('url',) if kind == 'web' else ('repo_id','revision','path')
        if all(e.get(k) == args[k] for k in fields):
            matches.append(e)
    if len(matches) != 1:
        raise ValueError('No unique approved evidence object at this cutoff; curator retrieval required')
    return matches[0]


def dispatch(packet, name, supplied):
    packet=Path(packet)
    args=args_for(name,supplied)
    manifest=json.loads((packet/'manifest.json').read_text())
    if name in ('graph_search','graph_trace','graph_query','symbol_history','repo_map'):
        from teacher.graph_worker import invoke
        return invoke(packet, manifest, name, args)
    commits=manifest['commits']
    if name in ('repo_read','repo_list','repo_grep'):
        if args['commit'] not in commits:
            raise ValueError('Commit is outside the strict-ancestor allowlist')
        tree=commits[args['commit']]['tree']
        path=safe_path(args.get('path',''),root_allowed=name!='repo_read')
        if name=='repo_read':
            if path not in tree:
                raise ValueError('File is not in this historical tree')
            return dict(excerpt(load_blob(packet,tree[path]['blob']),args),mode=tree[path]['mode'])
        paths=sorted(p for p in tree if not path or p==path or p.startswith(path+'/'))
        if name=='repo_list':
            end=args['offset']+args['limit']
            return {'paths':paths[args['offset']:end],'has_more':end<len(paths)}
        found=[]
        for p in paths:
            data=load_blob(packet,tree[p]['blob'])
            if b'\x00' in data:
                continue
            for line,text in enumerate(data.decode(errors='replace').splitlines(),1):
                if args['query'] in text:
                    if len(found)>=args['limit']:
                        return {'matches':found,'truncated':True}
                    found.append({'path':p,'line':line,'text':text[:4096]})
        return {'matches':found,'truncated':False}
    if name=='git_show':
        if args['commit'] not in manifest['shows']:
            raise ValueError('Commit is outside the supplied change/history allowlist')
        data=load_blob(packet,manifest['shows'][args['commit']])
        if args['commit']==manifest['task_sha']:
            for index,section in enumerate(manifest.get('task_change_sections',[])):
                end=section['offset']+section['bytes']
                if section['offset']<=args['offset']<end:
                    result=excerpt(data[:end],args)
                    result['section']={'index':index,'start':section['offset'],'end':end}
                    result['commit_truncated']=result['next_offset']<len(data)
                    return result
        return dict(excerpt(data,args),scope='commit')
    if name=='git_log':
        path=safe_path(args['path'],True)
        cutoff=datetime.fromisoformat(manifest['cutoff_date'].replace('Z','+00:00'))
        until=datetime.fromisoformat(args.get('until',manifest['cutoff_date']).replace('Z','+00:00'))
        if until.tzinfo is None or until>cutoff:
            raise ValueError('Log date exceeds the trusted cutoff')
        selected=[{k:c[k] for k in ('sha','parents','date','message')} for c in commits.values()
                  if datetime.fromisoformat(c['date'])<=until and
                  (not path or any(p==path or p.startswith(path+'/') for p in c['files']))]
        # Manifest order is not relied on: sort by the supplied ancestor traversal.
        order={sha:i for i,sha in enumerate(manifest.get('history_order',list(commits)))}
        selected.sort(key=lambda c:order[c['sha']],reverse=True)
        end=args['offset']+args['limit']
        return {'commits':selected[args['offset']:end],'has_more':end<len(selected)}
    if name in ('web_fetch','hf_fetch','safetensors_header'):
        kind={'web_fetch':'web','hf_fetch':'hf_file','safetensors_header':'safetensors_header'}[name]
        if name!='web_fetch':
            safe_path(args['path'])
            if name=='hf_fetch' and args['path'].lower().endswith(('.safetensors','.bin','.pt','.pth','.gguf','.ckpt','.h5','.hdf5','.npz','.npy','.msgpack','.onnx')):
                raise ValueError('Weight payloads are not exposed by hf_fetch')
        item=evidence_item(manifest,args,kind)
        data=load_blob(packet,item['blob'])
        if name=='safetensors_header':
            if len(data)>4*1024**2:
                raise ValueError('Approved header exceeds runtime budget')
            header=json.loads(data)
            if not isinstance(header,dict) or any(k!='__metadata__' and (not isinstance(v,dict) or not {'dtype','shape','data_offsets'}<=set(v)) for k,v in header.items()):
                raise ValueError('Invalid approved safetensors header')
            names=sorted(k for k in header if k!='__metadata__')
            end=args['offset']+args['limit']
            selected={k:header[k] for k in names[args['offset']:end]}
            return {'header':selected,'has_more':end<len(names),'source':{k:v for k,v in item.items() if k!='blob'}}
        return dict(excerpt(data,args),source={k:v for k,v in item.items() if k!='blob'})
    if name=='run':
        # Direct library use is not an execution boundary. Only the isolated worker can run code.
        if str(packet)!='/packet' or not Path('/app/teacher/worker.py').exists():
            raise ValueError('run requires the isolated runner')
        if args['argv'][0] not in ('python3','/usr/bin/python3'):
            raise ValueError('This runtime permits Python commands only')
        work=Path('/work/repo');work.mkdir(parents=True,exist_ok=False)
        base=manifest['base_commit']
        if base:
            for path,entry in commits[base]['tree'].items():
                target=work/safe_path(path)
                if entry['mode']=='120000':
                    raise ValueError('Runtime checkout contains an unsupported symlink')
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(load_blob(packet,entry['blob']))
        replacements=args.get('files',{})
        if sum(len(v.encode()) for v in replacements.values())>1048576:
            raise ValueError('Scratch file budget exceeded')
        for path,text in replacements.items():
            target=work/safe_path(path)
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
        with tempfile.TemporaryFile() as stdout,tempfile.TemporaryFile() as stderr:
            try:
                process=subprocess.run(['/usr/bin/python3','-I','-S',*args['argv'][1:]],cwd=work,
                                       stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,
                                       timeout=args['timeout_seconds'],preexec_fn=single_process_filter,env={'PATH':'/usr/bin','HOME':'/work','TMPDIR':'/tmp'})
                code=process.returncode;timed_out=False
            except subprocess.TimeoutExpired:
                code=None;timed_out=True
            stdout.seek(0);stderr.seek(0)
            out,err=stdout.read(65537),stderr.read(65537)
        return {'returncode':code,'timed_out':timed_out,'stdout':out[:65536].decode(errors='replace'),
                'stderr':err[:65536].decode(errors='replace'),'truncated':len(out)>65536 or len(err)>65536,
                'runtime':'python-stdlib-no-network'}
    raise ValueError('Unknown tool')


def main():
    try:
        raw=sys.stdin.buffer.read(1048577)
        if len(raw)>1048576:
            raise ValueError('Request budget exceeded')
        request=json.loads(raw)
        if set(request)!={'tool','arguments'}:
            raise ValueError('Invalid tool request envelope')
        result={'ok':True,'result':dispatch(Path('/packet'),request['tool'],request['arguments'])}
    except Exception as exc:
        result={'ok':False,'error':str(exc)}
    serialized=json.dumps(result)
    if len(serialized.encode())>1048576:
        serialized=json.dumps({'ok':False,'error':'Response budget exceeded; request a smaller page'})
    print(serialized)


if __name__=='__main__':
    # Only the supervisor's read-only application mounts are importable here.
    sys.path.insert(0, '/app')
    main()
