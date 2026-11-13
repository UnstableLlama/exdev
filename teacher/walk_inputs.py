# SPDX-License-Identifier: MIT
"""Trusted walk input preparation; missing eligible evidence fails before inference."""
import hashlib
import json
import re
from pathlib import Path
from .ancestor_context import read_regular
from .author import write_json
from .packet import build_packet, git


def references(message):
    # Conservatively gate all GitHub URLs, including shorthand issue references.
    return sorted(set(re.findall(r'https?://github\.com/[^\s<>]+|#\d+',message,re.IGNORECASE)))


def validate_recovery(marker, sha, cutoff, refs):
    if (marker.get('status')!='recovered_none_eligible' or marker.get('task_sha')!=sha
        or marker.get('cutoff')!=cutoff or marker.get('references')!=refs
        or not marker.get('recovery_report')):
        raise ValueError('Invalid recovered-none marker: task, cutoff, references and recovery report required')


def signatures(items):
    return sorted((item['source_id'],item['content_sha256']) for item in items)


def discussion_signatures(items, with_hints=True):
    rows=[]
    for item in items:
        base=(item['kind'],item['number'],item['url'],item['available'],item.get('content_sha256'))
        rows.append(base+(hint_signature(item),) if with_hints else base)
    return sorted(rows)


def hint_signature(item):
    if 'repo_paths_mentioned' not in item and 'repo_paths_mentioned_truncated' not in item:
        return None
    payload={'repo_paths_mentioned':item.get('repo_paths_mentioned'),
             'repo_paths_mentioned_truncated':item.get('repo_paths_mentioned_truncated')}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def opening_discussions(rows, with_hints):
    result=[]
    for row in rows:
        base=(row['kind'],row['number'],row['url'],row['available'])
        result.append(base+(hint_signature(row),) if with_hints else base)
    return sorted(result)


def discussion_path(bundle_path):
    return bundle_path.with_name(bundle_path.name.replace('-eligible.json','-unreferenced.json'))


def validate_contract(manifest):
    contract=manifest['walk_input_contract']
    if not isinstance(manifest.get('task_commit_message'),str):
        raise ValueError('Walk packet lacks task commit message')
    if contract.get('version',1)>=5:
        if manifest.get('guidance_version')!=2:raise ValueError('Missing dispatch guidance version')
        actual_refs=signatures([i for i in manifest['evidence'] if i['source_id'] in contract['reference_source_ids']])
        if actual_refs!=[tuple(x) for x in contract['reference_signatures']]:raise ValueError('Reference evidence missing or changed')
    if contract.get('version',1)>=2:
        refs=references(manifest['task_commit_message'])
        if refs and not contract['bundle_present']:
            validate_recovery(contract.get('recovery_marker') or {},manifest['task_sha'],manifest['cutoff_date'],refs)
    actual=signatures([item for item in manifest['evidence'] if item.get('catalog_origin')!='unreferenced_discussion' and item['source_id'] not in contract.get('reference_source_ids',[])])
    expected=[tuple(item) for item in contract['expected_evidence']]
    if actual!=expected or (contract['bundle_present'] and not actual):
        raise ValueError('Walk packet lacks eligible bundle evidence')
    if contract.get('version',1)>=3:
        catalog=manifest.get('unreferenced_discussion_catalog')
        if catalog is None or manifest.get('unreferenced_discussion_truncated')!=contract['discussion_truncated']:
            raise ValueError('Walk packet lacks unreferenced discussion catalog')
        with_hints=contract.get('version',1)>=4
        actual_rows=opening_discussions(catalog,with_hints)
        if actual_rows!=[tuple(r) for r in contract['expected_discussions']]:
            raise ValueError('Walk packet unreferenced discussion catalog changed')
        if with_hints:
            for row in catalog:
                if row['available'] and hint_signature(row) is None:
                    raise ValueError('Walk packet lacks repository path hints')
                if not row['available'] and hint_signature(row) is not None:
                    raise ValueError('Unavailable discussion must not expose repository path hints')


def validate_bundle(packet, bundle_path):
    manifest=json.loads(read_regular(Path(packet)/'manifest.json'))
    contract=manifest['walk_input_contract']
    bundle_path=Path(bundle_path)
    if bundle_path.exists():
        raw=read_regular(bundle_path);bundle=json.loads(raw)
        if (not contract['bundle_present'] or hashlib.sha256(raw).hexdigest()!=contract['bundle_sha256']
            or signatures([item for item in manifest['evidence'] if item.get('catalog_origin')!='unreferenced_discussion' and item['source_id'] not in contract.get('reference_source_ids',[])])!=signatures(bundle['items'])):
            raise ValueError('Eligible evidence bundle missing or changed after preparation')
    elif contract['bundle_present']:
        raise ValueError('Eligible evidence bundle disappeared')
    if contract.get('recovery_marker'):
        marker_path=bundle_path.with_name(bundle_path.name.replace('-eligible.json','-recovered-none.json'))
        if hashlib.sha256(read_regular(marker_path)).hexdigest()!=contract['recovery_marker_sha256']:
            raise ValueError('Recovery marker changed after preparation')
    if contract.get('version',1)>=3:
        path=discussion_path(bundle_path)
        raw=read_regular(path)
        if hashlib.sha256(raw).hexdigest()!=contract['discussion_bundle_sha256']:
            raise ValueError('Unreferenced discussion catalog changed after preparation')
        bundle=json.loads(raw)
        if discussion_signatures(bundle.get('items',[]),contract.get('version',1)>=4)!=[tuple(r) for r in contract['discussion_signatures']]:
            raise ValueError('Unreferenced discussion content changed after preparation')
    if contract.get('version',1)>=5:
        ref_path=bundle_path.with_name(bundle_path.name.replace('-eligible.json','-references.json'))
        if contract.get('reference_bundle_sha256'):
            raw=read_regular(ref_path)
            if hashlib.sha256(raw).hexdigest()!=contract['reference_bundle_sha256']:raise ValueError('Reference evidence changed after preparation')
        actual=signatures([i for i in manifest['evidence'] if i['source_id'] in contract['reference_source_ids']])
        if actual!=[tuple(x) for x in contract['reference_signatures']]:raise ValueError('Reference evidence missing or changed')
    validate_contract(manifest)


def prepare(repo,sha,position,packet,evidence_directory):
    bundle_path=Path(evidence_directory)/f'{position:06d}-eligible.json'
    unreferenced_path=Path(evidence_directory)/f'{position:06d}-unreferenced.json'
    if not unreferenced_path.exists():
        raise ValueError('Unreferenced discussion recovery required before authoring')
    unreferenced_raw=read_regular(unreferenced_path);unreferenced=json.loads(unreferenced_raw)
    raw=read_regular(bundle_path) if bundle_path.exists() else None
    evidence=json.loads(raw) if raw is not None else None
    if evidence is not None and not evidence.get('items'):
        raise ValueError('Eligible bundle exists but contains no evidence')
    message=git(repo,'show','-s','--format=%B',sha).decode(errors='replace').rstrip('\n')
    refs=references(message);marker=None;marker_raw=None
    if refs and evidence is None:
        marker_path=Path(evidence_directory)/f'{position:06d}-recovered-none.json'
        if not marker_path.exists():raise ValueError('Referenced issue/PR evidence recovery required before authoring')
        marker_raw=read_regular(marker_path);marker=json.loads(marker_raw)
        validate_recovery(marker,sha,git(repo,'show','-s','--format=%cI',sha).decode().strip(),refs)
    referenced_roots=set()
    for item in (evidence or {}).get('items',[]):
        match=re.match(r'(https://github\.com/[^/]+/[^/]+/(?:issues|pull)/\d+)',item.get('url',''))
        if match:referenced_roots.add(match.group(1))
    filtered=dict(unreferenced,items=[item for item in unreferenced.get('items',[]) if item.get('url') not in referenced_roots])
    from .architecture_evidence import load_bundle
    ref_path=Path(evidence_directory)/f'{position:06d}-references.json'
    ref=load_bundle(repo,sha,ref_path)
    ref_items=ref['items'] if ref else []
    combined=dict(evidence or {'task_sha':sha,'cutoff':unreferenced['cutoff'],'items':[]})
    combined['items']=[*combined['items'],*ref_items]
    if len({i['source_id'] for i in combined['items']})!=len(combined['items']):raise ValueError('Duplicate evidence IDs')
    manifest=build_packet(repo,sha,packet,evidence=combined,discussions=filtered)
    manifest.update(guidance_version=2,editorial_schema_version=5,ancestor_context_mode='retrieval_v1',ancestor_matches_version=1,
        walk_input_contract={'version':5,'reference_source_ids':[i['source_id'] for i in ref_items],
            'reference_signatures':signatures(ref_items),
            'reference_bundle_sha256':hashlib.sha256(ref_path.read_bytes()).hexdigest() if ref else None,'recovery_marker':marker,
            'recovery_marker_sha256':hashlib.sha256(marker_raw).hexdigest() if marker_raw else None,
            'bundle_present':raw is not None,
            'bundle_sha256':hashlib.sha256(raw).hexdigest() if raw is not None else None,
            'expected_evidence':signatures(evidence['items']) if evidence else [],
            'discussion_bundle_sha256':hashlib.sha256(unreferenced_raw).hexdigest(),
            'discussion_signatures':discussion_signatures(unreferenced.get('items',[])),
            'discussion_truncated':unreferenced.get('truncated'),
            'expected_discussions':opening_discussions(manifest['unreferenced_discussion_catalog'],True)})
    write_json(Path(packet)/'manifest.json',manifest)
    validate_bundle(packet,bundle_path)
    return manifest
