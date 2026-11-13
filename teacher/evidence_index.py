# SPDX-License-Identifier: MIT
"""Compact, packet-bound navigation for task and strict-ancestor evidence."""
import hashlib
import json
import re
from pathlib import Path
from .evidence import timestamp
from .worker import load_blob

OPENING_BYTES = 8192


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def build(packet, manifest, ancestor_packets, discussion_directory=None):
    """Copy only evidence bytes/metadata, never prose or administrative artifacts."""
    packet = Path(packet)
    objects = []
    seen = {}
    def add(item, origin, source_packet):
        if any(timestamp(item[k]) > timestamp(manifest['cutoff_date']) for k in ('created_at','revision_at')):
            return
        raw = load_blob(Path(source_packet), item['blob'])
        if hashlib.sha256(raw).hexdigest() != item['content_sha256']:
            raise ValueError('Indexed evidence checksum mismatch')
        # These fields are the packet builder's evidence allowlist. Never copy curator notes.
        fields = ('author_login','url','source_id','created_at','revision_at','retrieved_at',
                  'representation','content_sha256','kind','repo_id','revision','path',
                  'artifact_role','blob','content_bytes','tensor_count')
        obj = {k:item[k] for k in fields if k in item}
        identity={k:obj.get(k) for k in ('kind','repo_id','revision','path','url','content_sha256')}
        key = digest(identity)
        if key in seen:
            if origin not in seen[key]['attached_by']: seen[key]['attached_by'].append(origin)
            return
        obj['attached_by'] = [origin]
        seen[key] = obj
        objects.append(obj)
        (packet/'blobs'/obj['blob']).write_bytes(raw)
    for item in manifest['evidence']:
        if item.get('catalog_origin') not in ('unreferenced_discussion','closed_discussion'): add(item, manifest['task_sha'], packet)
    for source in sorted(map(Path, ancestor_packets)):
        path = source/'manifest.json'
        if path.is_symlink(): raise ValueError('Ancestor manifest must be regular')
        old = json.loads(path.read_bytes())
        if old.get('task_sha') not in manifest['commits']: continue
        # Unreferenced snapshots remain governed by their separate open-discussion policy.
        for item in old['evidence']:
            if item.get('catalog_origin') not in ('unreferenced_discussion','closed_discussion','ancestor_evidence'):
                add(item, old['task_sha'], source)
    groups = {}
    for obj in objects:
        if obj['kind'] in ('hf_file','safetensors_header'):
            key = ('model',obj['repo_id'],obj['revision'])
            row = {'kind':'model','repo_id':obj['repo_id'],'revision':obj['revision'],
                   'revision_at':obj['revision_at']}
        else:
            match = re.match(r'(https://github\.com/[^/]+/[^/]+/(issues|pull)/(\d+))',obj.get('url',''))
            url = match[1] if match else obj['url']
            key = ('discussion',url)
            row = {'kind': ('issue' if match[2]=='issues' else 'pull_request') if match else 'web',
                   'url':url,'number':int(match[3]) if match else None}
            if match and discussion_directory is not None:
                history=Path(discussion_directory)/f"discussion-{row['kind']}-{row['number']}-history.json"
                if history.exists():
                    data=json.loads(history.read_bytes())
                    if data.get('url')!=url or not data.get('timeline_complete'):
                        raise ValueError('Discussion title history is incomplete or mismatched')
                    title=data['title']
                    for event in sorted(data.get('title_events',[]),key=lambda e:timestamp(e['createdAt']),reverse=True):
                        if timestamp(event['createdAt'])>timestamp(manifest['cutoff_date']):title=event['previousTitle']
                    row['title']=title
            # Titles only, if the attached structured object actually supplies one.
            try:
                body=json.loads(load_blob(packet,obj['blob']))
                title=body.get('title') if isinstance(body,dict) else None
                if isinstance(title,str): row['title']=title
            except (ValueError,UnicodeDecodeError): pass
        group=groups.setdefault(key,dict(row,index_id=digest(key),attached_by=[],counts={},objects=[]))
        for origin in obj['attached_by']:
            if origin not in group['attached_by']: group['attached_by'].append(origin)
        role='tensor_headers' if obj['kind']=='safetensors_header' else ('configuration_files' if obj['kind']=='hf_file' else ('discussion_objects' if row['kind'] in ('issue','pull_request') else 'documents'))
        group['counts'][role]=group['counts'].get(role,0)+1
        group['objects'].append(obj)
    sources=[]
    for key in sorted(groups):
        group=groups[key];group['attached_by'].sort();group['objects'].sort(key=lambda o:(o['source_id'],o['content_sha256']))
        if group['kind']=='model' and manifest['walk_input_contract'].get('version',1)>=7:
            group['architectures']=model_architectures(packet,group)
        sources.append(group)
    index={'sources':sources}
    manifest['evidence_index']=index
    manifest['walk_input_contract']['evidence_index_sha256']=digest(index)
    return index


def model_architectures(packet, row):
    configs=[o for o in row['objects'] if o['kind']=='hf_file' and o.get('path')=='config.json']
    if not configs:return []
    values=[]
    for obj in configs:
        config=json.loads(load_blob(Path(packet),obj['blob']))
        architectures=config.get('architectures',[])
        if not isinstance(architectures,list) or any(not isinstance(a,str) for a in architectures):
            raise ValueError('Model architectures must be a list of strings')
        values.append(architectures)
    if any(v!=values[0] for v in values):raise ValueError('Conflicting pinned model configurations')
    return values[0]


def validate(manifest, packet=None):
    index=manifest.get('evidence_index')
    if not isinstance(index,dict) or digest(index)!=manifest['walk_input_contract'].get('evidence_index_sha256'):
        raise ValueError('Evidence index missing or changed')
    for row in index['sources']:
        if row['kind']=='model' and manifest['walk_input_contract'].get('version',1)>=7:
            if not isinstance(row.get('architectures'),list):raise ValueError('Missing model architectures')
            if packet is not None and row['architectures']!=model_architectures(packet,row):
                raise ValueError('Model architectures differ from pinned config')
        for obj in row['objects']:
            if any(timestamp(obj[k])>timestamp(manifest['cutoff_date']) for k in ('created_at','revision_at')):
                raise ValueError('Indexed evidence exceeds cutoff')
            if not set(obj['attached_by']) <= (set(manifest['commits'])|{manifest['task_sha']}):
                raise ValueError('Indexed evidence is not ancestral')
            if packet is not None:
                data=load_blob(Path(packet),obj['blob'])
                if hashlib.sha256(data).hexdigest()!=obj['content_sha256']:raise ValueError('Indexed evidence changed')
