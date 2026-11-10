# SPDX-License-Identifier: MIT
"""Trusted walk input preparation; missing eligible evidence fails before inference."""
import hashlib
import json
from pathlib import Path
from .ancestor_context import read_regular
from .author import write_json
from .packet import build_packet


def signatures(items):
    return sorted((item['source_id'],item['content_sha256']) for item in items)


def validate_contract(manifest):
    contract=manifest['walk_input_contract']
    if not isinstance(manifest.get('task_commit_message'),str):
        raise ValueError('Walk packet lacks task commit message')
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
    validate_contract(manifest)


def prepare(repo,sha,position,packet,evidence_directory):
    bundle_path=Path(evidence_directory)/f'{position:06d}-eligible.json'
    raw=read_regular(bundle_path) if bundle_path.exists() else None
    evidence=json.loads(raw) if raw is not None else None
    if evidence is not None and not evidence.get('items'):
        raise ValueError('Eligible bundle exists but contains no evidence')
    manifest=build_packet(repo,sha,packet,evidence=evidence)
    manifest.update(editorial_schema_version=5,ancestor_context_mode='retrieval_v1',ancestor_matches_version=1,
        walk_input_contract={'version':1,'bundle_present':raw is not None,
            'bundle_sha256':hashlib.sha256(raw).hexdigest() if raw is not None else None,
            'expected_evidence':signatures(evidence['items']) if evidence else []})
    write_json(Path(packet)/'manifest.json',manifest)
    validate_bundle(packet,bundle_path)
    return manifest
