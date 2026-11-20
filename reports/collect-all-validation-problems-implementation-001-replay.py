# SPDX-License-Identifier: MIT
"""Reproduce validator feedback from the two archived first finals."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

from teacher.editorial import assemble_draft
from teacher.validation_repair import (
    CLAIM_DIAGNOSTICS_POLICY, POLICY, digest, eligible, refusal_fields, repair_feedback,
)


def refusal(final, manifest, prefix, policy):
    try:
        assemble_draft(json.loads(final), manifest, prefix, collect_problems=policy == POLICY)
    except ValueError as error:
        if not eligible(error):
            raise
        return refusal_fields(error, policy)
    raise ValueError('Archived annotation now validates')


def replay(root, position):
    name = f'{position:06d}-001'
    run = root / '.teacher/runs' / f'commit-{name}'
    manifest_path = root / '.teacher/retrieval' / name / 'manifest.json'
    paths = [manifest_path, run / 'raw-transcript.json', run / 'provenance.json', run / 'status.json']
    blobs = [path.read_bytes() for path in paths]
    manifest, transcript, provenance, status = map(json.loads, blobs)
    artifacts = {str(path.relative_to(root)): sha256(blob).hexdigest() for path, blob in zip(paths, blobs)}
    if artifacts[str(manifest_path.relative_to(root))] != provenance['packet_manifest_sha256']:
        raise ValueError('Archived manifest hash mismatch')
    (index, event), = [(i, item) for i, item in enumerate(transcript) if item['role'] == 'validation']
    if event['prefix_end'] != index or event['policy'] != CLAIM_DIAGNOSTICS_POLICY:
        raise ValueError('Unexpected archived refusal boundary or policy')
    original = transcript[event['refused_index']]['content']
    if digest(original) != event['refused_sha256']:
        raise ValueError('Archived first final hash mismatch')
    old = refusal(original, manifest, transcript[:index], CLAIM_DIAGNOSTICS_POLICY)
    if any(event[key] != value for key, value in old.items()):
        raise ValueError('Archived refusal mismatch')
    old_feedback = repair_feedback(old['error'], CLAIM_DIAGNOSTICS_POLICY)
    if (transcript[index + 1] != {'role': 'user', 'content': old_feedback}
            or digest(old_feedback) != provenance['validation_repair_input_sha256']):
        raise ValueError('Archived feedback mismatch')
    new = refusal(original, manifest, transcript[:index], POLICY)
    new_feedback = repair_feedback(new['error'], POLICY)
    terminal = transcript[-1]
    if (status['status'] != 'failed' or event['selected_final_index'] is not None
            or terminal['role'] != 'assistant' or terminal['turn_id'] != event['repair_turn_id']):
        raise ValueError('Unexpected archived terminal state')
    return {
        'run': run.name,
        'artifact_sha256': artifacts,
        'refused_final_index': event['refused_index'],
        'refused_final_sha256': event['refused_sha256'],
        'recorded_feedback_exact': old_feedback,
        'candidate_feedback_on_same_prefix': new_feedback,
        'candidate_feedback_bytes': len(new_feedback.encode()),
        'candidate_feedback_sha256': digest(new_feedback),
        'recorded_second_final_refusal': refusal(terminal['content'], manifest, transcript, CLAIM_DIAGNOSTICS_POLICY),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    print(json.dumps({'archived_policy': CLAIM_DIAGNOSTICS_POLICY, 'candidate_policy': POLICY,
                      'results': [replay(args.root, position) for position in (345, 346)]}, indent=2))
