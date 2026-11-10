# SPDX-License-Identifier: MIT
"""Trusted packet builder. Only strict-ancestor Git objects and curated dated evidence are exported."""
import argparse
import base64
import re
import hashlib
import json
from pathlib import Path
import subprocess
from .evidence import timestamp

ROOT = Path(__file__).resolve().parents[1]


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], stdin=subprocess.DEVNULL)


def build_packet(repo, task, destination, evidence=None):
    repo, destination = Path(repo), Path(destination)
    if destination.exists():
        raise ValueError('Packet destination must not already exist')
    task = git(repo, 'rev-parse', '--verify', task + '^{commit}').decode().strip()
    parents = git(repo, 'show', '-s', '--format=%P', task).decode().split()
    cutoff = git(repo, 'show', '-s', '--format=%cI', task).decode().strip()
    allowed = git(repo, 'rev-list', '--reverse', '--topo-order', *parents).decode().split() if parents else []
    destination.mkdir(parents=True)
    blobs = destination / 'blobs'
    blobs.mkdir()
    def store(data):
        digest = hashlib.sha256(data).hexdigest()
        path = blobs / digest
        if not path.exists():
            path.write_bytes(data)
        return digest
    manifest = {'schema_version': 1, 'task_sha': task, 'cutoff_date': cutoff,
                'base_commit': parents[0] if parents else None, 'task_parents': parents,
                'commits': {}, 'shows': {}, 'evidence': [], 'history_order': allowed,
                'mode': 'entry_analysis', 'ancestor_entries': []}
    seen_blobs = {}
    for sha in [*allowed, task]:
        fields = git(repo, 'show', '-s', '--format=%P%x00%cI%x00%B', sha).decode(errors='replace').split('\0', 2)
        ps, date, message = fields[0].split(), fields[1], fields[2].rstrip('\n')
        base = ps[0] if ps else git(repo, 'hash-object', '-t', 'tree', '--stdin').decode().strip()
        patch = git(repo, 'diff', '--binary', '--full-index', '--no-ext-diff', '--no-textconv', base, sha, '--')
        show = f'Commit: {sha}\nParents: {" ".join(ps)}\nDate: {date}\n\n{message}\n\n'.encode() + patch
        manifest['shows'][sha] = store(show)
        if sha == task:
            boundaries=list(re.finditer(rb'^diff --git .*$',show,re.MULTILINE))
            manifest['task_change_sections']=[]
            for i,match in enumerate(boundaries):
                end=boundaries[i+1].start() if i+1<len(boundaries) else len(show)
                manifest['task_change_sections'].append({
                    'header':match.group().decode(errors='replace'),'offset':match.start(),
                    'bytes':end-match.start(),'binary':b'GIT binary patch' in show[match.start():end]})
            continue  # Task diff is explicit input; its solved tree is not a repo-tool target.
        tree = {}
        for line in git(repo, 'ls-tree', '-rz', '--full-tree', sha).split(b'\0'):
            if not line:
                continue
            meta, raw_path = line.split(b'\t', 1)
            mode, kind, blob = meta.decode().split()
            path = raw_path.decode('utf-8')
            if kind != 'blob':
                continue  # No submodule traversal or external repository access.
            if blob not in seen_blobs:
                seen_blobs[blob] = store(git(repo, 'cat-file', 'blob', blob))
            tree[path] = {'blob': seen_blobs[blob], 'mode': mode}
        files = git(repo, 'diff', '--name-only', '-z', base, sha, '--').decode().strip('\0').split('\0') if patch else []
        manifest['commits'][sha] = {'sha': sha, 'parents': ps, 'date': date, 'message': message,
                                    'files': files, 'tree': tree}
    if evidence:
        if evidence['task_sha'] != task or timestamp(evidence['cutoff']) != timestamp(cutoff):
            raise ValueError('Evidence bundle belongs to a different task/cutoff')
        for item in evidence['items']:
            if timestamp(item['created_at']) > timestamp(cutoff) or timestamp(item['revision_at']) > timestamp(cutoff):
                raise ValueError('Evidence is newer than task cutoff')
            data = (base64.b64decode(item['content_base64'], validate=True)
                    if 'content_base64' in item else item['content'].encode())
            if item.get('kind') in ('hf_file','safetensors_header'):
                if not re.fullmatch('[0-9a-f]{40}|[0-9a-f]{64}', item.get('revision','')):
                    raise ValueError('HF evidence requires an immutable commit revision')
                required_role = 'non_weight' if item['kind']=='hf_file' else 'tensor_header'
                if item.get('artifact_role') != required_role:
                    raise ValueError('HF artifact role has not been approved by the curator')
            if hashlib.sha256(data).hexdigest() != item['content_sha256']:
                raise ValueError('Evidence checksum mismatch')
            allowed_keys = ('url', 'source_id', 'created_at', 'revision_at', 'retrieved_at', 'representation',
                            'content_sha256', 'kind', 'repo_id', 'revision', 'path', 'artifact_role', 'mirror_provenance')
            exported = {k:item[k] for k in allowed_keys if k in item}
            exported.update(blob=store(data), kind=item.get('kind', 'web'),content_bytes=len(data))
            if exported['kind']=='safetensors_header':
                exported['tensor_count']=len([k for k in json.loads(data) if k!='__metadata__'])
            manifest['evidence'].append(exported)
    (destination/'manifest.json').write_text(json.dumps(manifest, sort_keys=True, indent=2)+'\n')
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task', required=True)
    p.add_argument('--destination', type=Path, required=True)
    p.add_argument('--evidence', type=Path)
    p.add_argument('--editorial-schema-version', type=int, choices=(2,3), default=3)
    a = p.parse_args()
    evidence = json.loads(a.evidence.read_text()) if a.evidence else None
    manifest = build_packet(ROOT/'.sources/exllamav3.git', a.task, a.destination, evidence)
    manifest['editorial_schema_version']=a.editorial_schema_version
    (a.destination/'manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'task_sha': manifest['task_sha'], 'ancestor_commits': len(manifest['commits']),
                      'eligible_evidence': len(manifest['evidence'])}))


if __name__ == '__main__':
    main()
