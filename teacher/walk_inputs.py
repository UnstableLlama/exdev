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


def validate_contract(manifest):
    contract=manifest['walk_input_contract']
    if not isinstance(manifest.get('task_commit_message'),str):
        raise ValueError('Walk packet lacks task commit message')
    if contract.get('version',1)>=2:
        refs=references(manifest['task_commit_message'])
        if refs and not contract['bundle_present']:
            validate_recovery(contract.get('recovery_marker') or {},manifest['task_sha'],manifest['cutoff_date'],refs)
    actual=signatures(manifest['evidence'])
    expected=[tuple(item) for item in contract['expected_evidence']]
    if actual!=expected or (contract['bundle_present'] and not actual):
        raise ValueError('Walk packet lacks eligible bundle evidence')


def validate_bundle(packet, bundle_path):
    manifest=json.loads(read_regular(Path(packet)/'manifest.json'))
    contract=manifest['walk_input_contract']
    bundle_path=Path(bundle_path)
    if bundle_path.exists():
        raw=read_regular(bundle_path);bundle=json.loads(raw)
        if (not contract['bundle_present'] or hashlib.sha256(raw).hexdigest()!=contract['bundle_sha256']
            or signatures(manifest['evidence'])!=signatures(bundle['items'])):
            raise ValueError('Eligible evidence bundle missing or changed after preparation')
    elif contract['bundle_present']:
        raise ValueError('Eligible evidence bundle disappeared')
    if contract.get('recovery_marker'):
        marker_path=bundle_path.with_name(bundle_path.name.replace('-eligible.json','-recovered-none.json'))
        if hashlib.sha256(read_regular(marker_path)).hexdigest()!=contract['recovery_marker_sha256']:
            raise ValueError('Recovery marker changed after preparation')
    validate_contract(manifest)


def prepare(repo,sha,position,packet,evidence_directory):
    bundle_path=Path(evidence_directory)/f'{position:06d}-eligible.json'
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
    manifest=build_packet(repo,sha,packet,evidence=evidence)
    manifest.update(editorial_schema_version=5,ancestor_context_mode='retrieval_v1',ancestor_matches_version=1,
        walk_input_contract={'version':2,'recovery_marker':marker,
            'recovery_marker_sha256':hashlib.sha256(marker_raw).hexdigest() if marker_raw else None,
            'bundle_present':raw is not None,
            'bundle_sha256':hashlib.sha256(raw).hexdigest() if raw is not None else None,
            'expected_evidence':signatures(evidence['items']) if evidence else []})
    write_json(Path(packet)/'manifest.json',manifest)
    validate_bundle(packet,bundle_path)
    return manifest
