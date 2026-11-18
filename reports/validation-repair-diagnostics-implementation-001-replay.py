# SPDX-License-Identifier: MIT
"""Recheck archived repair transcripts using the isolated candidate source tree."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from orchestration.ancestor_selection import installed
from teacher.cycle import replay_result
from teacher.editorial import assemble_draft, render
from teacher.runner import Runner
from teacher.validation_repair import POLICY, eligible, refusal_fields, repair_feedback, verify_final


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def refusal(message, manifest, transcript, policy):
    try:
        assemble_draft(json.loads(message['content']), manifest, transcript)
    except ValueError as error:
        if not eligible(error):
            raise
        return refusal_fields(error, policy)
    raise ValueError('The archived refused final now validates')


def replay(root, run, provenance):
    packet = root / '.teacher/retrieval' / run.name.removeprefix('commit-')
    manifest_path = packet / 'manifest.json'
    transcript_path = run / 'raw-transcript.json'
    manifest, transcript = read(manifest_path), read(transcript_path)
    if digest(manifest_path) != provenance['packet_manifest_sha256']:
        raise ValueError('Archived manifest hash mismatch')
    index, event = next((i, m) for i, m in enumerate(transcript) if m['role'] == 'validation')
    if event['prefix_end'] != index:
        raise ValueError('Archived prefix boundary mismatch')
    original = transcript[event['refused_index']]
    if sha256(original['content'].encode()).hexdigest() != event['refused_sha256']:
        raise ValueError('Archived first final hash mismatch')
    old_refusal = refusal(original, manifest, transcript[:index], event['policy'])
    expected_feedback = repair_feedback(old_refusal['error'], event['policy'])
    if any(event[key] != value for key, value in old_refusal.items()):
        raise ValueError('Archived refusal mismatch')
    if transcript[index+1] != {'role': 'user', 'content': expected_feedback}:
        raise ValueError('Archived feedback mismatch')
    if sha256(expected_feedback.encode()).hexdigest() != provenance['validation_repair_input_sha256']:
        raise ValueError('Archived feedback hash mismatch')

    artifacts = [manifest_path, transcript_path, run / 'provenance.json', run / 'status.json']
    draft_path = run / 'draft.json'
    status = read(run / 'status.json')['status']
    result = {
        'run': run.name, 'status': status, 'recorded_policy': event['policy'],
        'original_feedback': expected_feedback,
        'candidate_feedback_on_original_final': repair_feedback(refusal(
            original, manifest, transcript[:index], POLICY)['error']),
    }
    if draft_path.exists():
        draft = read(draft_path)
        replayed, _ = verify_final(draft['annotation'], manifest, transcript, provenance)
        draft_md = run / 'draft.md'
        if replayed != draft or render(replayed) != draft_md.read_text():
            raise ValueError('Archived draft or rendering mismatch')
        artifacts.extend((draft_path, draft_md))
        result['selected_final_verified'] = True
    else:
        if status != 'failed' or event['selected_final_index'] is not None:
            raise ValueError('Unexpected failed-run state')
        terminal = transcript[-1]
        if terminal['role'] != 'assistant' or terminal['turn_id'] != event['repair_turn_id']:
            raise ValueError('Failed retry is missing its terminal final')
        result['terminal_refusal'] = refusal(terminal, manifest, transcript, event['policy'])
        result['candidate_diagnostic_on_terminal_final'] = refusal(terminal, manifest, transcript, POLICY)

    with installed():
        runner = Runner(packet)
        calls = {c['id']: c for m in transcript for c in m.get('calls', [])}
        counts = Counter()
        for message in transcript:
            if message['role'] == 'tool':
                replay_result(runner, calls[message['call_id']], message)
                counts[message['name']] += 1
        result.update(replayed_calls=sum(counts.values()), tool_counts=dict(counts))
    result['artifact_sha256'] = {str(path.relative_to(root)): digest(path) for path in artifacts}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    results = []
    for path in sorted((args.root / '.teacher/runs').glob('*/provenance.json')):
        provenance = read(path)
        if provenance.get('validation_repair') is True:
            try:
                results.append(replay(args.root, path.parent, provenance))
            except Exception as error:
                raise RuntimeError(f'Replay failed for {path.parent.name}: {error}') from error
    print(json.dumps({'candidate_policy': POLICY, 'tool_reexecution': 'original packet via accepted queue adapter',
                      'results': results}, indent=2))


if __name__ == '__main__':
    main()
