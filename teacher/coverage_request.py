# SPDX-License-Identifier: MIT
"""Explicitly authorized pointer-only coverage input, separate from verdicts."""
import hashlib
import re
from pathlib import Path

INSTRUCTION = "The reviewer_coverage_request field holds a reviewer's requests for coverage, not statements of fact."


def attach(manifest, path, expected_sha256):
    """Caller must inspect semantics before supplying the exact approved digest.

    Mechanical gates cannot decide whether prose implies a conclusion. The
    trusted author must refuse conclusions, hindsight, and length quotas.
    """
    path=Path(path)
    if path.is_symlink() or not re.fullmatch(r'commit-\d{6}-\d{3}\.coverage\.md',path.name):
        raise ValueError('Only a separate coverage request is permitted')
    raw=path.read_bytes()
    if not raw or len(raw)>16384 or hashlib.sha256(raw).hexdigest()!=expected_sha256:
        raise ValueError('Coverage request missing, oversized or not explicitly approved')
    text=raw.decode('utf-8')
    allowed=set(manifest['commits'])|{manifest['task_sha']}
    for sha in re.findall(r'\b[0-9a-f]{40}\b',text):
        if sha not in allowed:raise ValueError('Coverage request names a non-ancestor commit')
    record={'path':str(path),'sha256':expected_sha256,'text':text}
    manifest['coverage_request']=record
    manifest['walk_input_contract']['coverage_request_sha256']=expected_sha256
    manifest['walk_input_contract']['coverage_request_path']=str(path)


def validate(manifest):
    contract=manifest['walk_input_contract'];record=manifest.get('coverage_request')
    if record is None:
        if contract.get('coverage_request_sha256') or contract.get('coverage_request_path'):
            raise ValueError('Coverage request disappeared')
        return
    if (hashlib.sha256(record['text'].encode()).hexdigest()!=contract.get('coverage_request_sha256')
        or record['sha256']!=contract.get('coverage_request_sha256')
        or record['path']!=contract.get('coverage_request_path')):
        raise ValueError('Coverage request changed')
