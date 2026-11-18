# SPDX-License-Identifier: MIT
"""Verified inputs to a teacher revision. Admission records stay on the supervisor side."""
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

ARTIFACTS = ('draft.json', 'draft.md', 'raw-transcript.json', 'provenance.json')
REVISION_FILES = ('prior-evidence.json', 'revision-input.json', 'revision.coverage.md')
ID_MAP_VERSION = 1
INSTRUCTION = (
    "You are revising your own previous annotation for this position. The historical packet is unchanged. "
    "The supplied previous annotation and tool records belong only to the named prior attempt. "
    "Write a complete replacement annotation using the ordinary editorial schema; do not return a patch. "
    "Keep the mechanisms and supported findings that the previous annotation established, examine the supplied "
    "pointer-only coverage request, and correct any claims you find unsupported. Cite every retained or added "
    "statement using a supplied prior evidence ID or a new tool evidence ID. Previous prose itself is not evidence. "
    "Prior tool records describe checks performed in the previous attempt, not checks newly executed in this session; "
    "preserve their source/execution distinctions and limitations. New findings and changes must be supported by "
    "permitted historical evidence. Nobody else will edit your prose. Do not mark this entry approved, canonical, "
    "or training eligible."
)
# The literal phrasing is fixed. Only exact pointers into the historical task are admitted.
POINTER = re.compile(
    r'- What does `(?P<path>[A-Za-z0-9_.+/-]+)`'
    r'(?: at lines (?P<start>[1-9][0-9]*)(?:–(?P<end>[1-9][0-9]*))?)?'
    r'(?: in `(?P<symbol>[A-Za-z_][A-Za-z0-9_:.-]*)`)?'
    r' (?:define|return|check|change)\?'
)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def regular(path):
    from .ancestor_context import read_regular
    return read_regular(path)


def position_of(run):
    match = re.fullmatch(r'commit-([0-9]{6})-[0-9]{3}', Path(run).name)
    if not match:
        raise ValueError('Revision requires a named commit attempt')
    return int(match[1])


def coverage_bytes(path, expected, manifest):
    raw = regular(path)
    if sha256(raw) != expected:
        raise ValueError('Revision coverage digest mismatch')
    if len(raw) > 4096:
        raise ValueError('Revision coverage exceeds 4096 bytes')
    lines = raw.decode('utf-8').removesuffix('\n').split('\n')
    if not 1 <= len(lines) <= 12:
        raise ValueError('Revision coverage must contain 1–12 bounded pointer questions')
    paths = set(manifest['task_changed_files'])
    for parent in manifest['task_parents']:
        paths.update(manifest['commits'][parent]['files'])
    for line in lines:
        match = POINTER.fullmatch(line)
        if (not match or match['path'] not in paths
                or match['end'] and int(match['end']) < int(match['start'])):
            raise ValueError('Revision coverage must contain only questions pointing to task or parent paths')
    return raw


def pairs(transcript):
    """Extract completed call/result pairs without retaining any surrounding messages."""
    from .editorial import evidence_ledger
    ledger = evidence_ledger(transcript, complete=True)
    return [
        {'id': message['call_id'], 'tool': message['name'],
         'arguments': ledger[message['call_id']]['arguments'],
         'result': message['content'], 'result_sha256': ledger[message['call_id']]['result_sha256']}
        for message in transcript if message['role'] == 'tool'
    ]


def prior_messages(records):
    messages = []
    for record in records:
        identity = record['id']
        messages.extend((
            {'role': 'assistant', 'calls': [
                {'id': identity, 'tool': record['tool'], 'arguments': record['arguments']}]},
            {'role': 'tool', 'call_id': identity, 'name': record['tool'], 'content': record['result']},
        ))
    return messages


def selected_annotation(transcript, provenance):
    """Historic runs lack phase tags; require one structured final in the selected turn."""
    repair = provenance.get('validation_repair')
    events = [row for row in transcript if row['role'] == 'validation']
    if repair:
        if len(events) != 1:
            raise ValueError('Missing or ambiguous revision source repair')
        candidates = range(events[0]['prefix_end'] + 2, len(transcript))
    else:
        candidates = range(len(transcript))
    finals = []
    last_text = None
    for index in candidates:
        message = transcript[index]
        if message['role'] != 'assistant' or 'content' not in message:
            continue
        last_text = index
        try:
            value = json.loads(message['content'])
        except json.JSONDecodeError:
            continue  # Historical commentary can be plain text.
        if isinstance(value, dict) and 'schema_version' in value:
            finals.append((index, value))
    if (len(finals) != 1 or finals[0][0] != last_text
            or repair and finals[0][0] != events[0]['selected_final_index']):
        raise ValueError('Missing or ambiguous final annotation')
    return finals[0][1]


def remap(annotation, identities):
    result = deepcopy(annotation)
    claims = [claim for field in ('problem', 'reasoning', 'impact', 'source_notes') for claim in result[field]]
    claims.extend(claim for chapter in result['chapters'] for claim in chapter['claims'])
    for claim in claims:
        claim['evidence'] = [identities.get(ref, ref) for ref in claim['evidence']]
    for finding in result.get('findings', []):
        finding['source_evidence'] = [identities[ref] for ref in finding['source_evidence']]
        for check in finding['verification']:
            check['evidence'] = [identities[ref] for ref in check['evidence']]
    return result


@dataclass
class Revision:
    binding: dict
    annotation: dict
    records: list
    coverage: bytes

    @property
    def prior(self):
        return prior_messages(self.records)

    def extend(self, session):
        session.initial[0]['content'] += '\n\n' + INSTRUCTION
        task = json.loads(session.initial[1]['content'])
        task['revision'] = {
            'prior_annotation': self.annotation,
            'prior_evidence': self.records,
            'coverage_questions': self.coverage.decode(),
        }
        session.initial[1]['content'] = json.dumps(task, sort_keys=True)
        session.revision_prior = self.prior


def prepare(packet, output, binding):
    """Read exactly the bound source, project it to data, and revalidate it."""
    from .codex_adapter import require_approval_model
    from .editorial import render
    from .validation_repair import verify_final

    packet, output = Path(packet), Path(output)
    source = Path(binding['revision_of_run'])
    position = binding['position']
    if (position_of(output) != position or position_of(source) != position
            or output.resolve() == source.resolve()):
        raise ValueError('Revision source and destination must be distinct attempts at the same position')
    raw_manifest = regular(packet/'manifest.json')
    manifest = json.loads(raw_manifest)
    if (packet.resolve() != Path(binding['packet']).resolve()
            or sha256(raw_manifest) != binding['packet_manifest_sha256']):
        raise ValueError('Revision requires the identical original packet')
    if manifest['task_sha'] != binding['task_sha']:
        raise ValueError('Revision task SHA mismatch')
    if 'coverage_request' in manifest:
        raise ValueError('Original packet has attempt-specific coverage; review required')
    originals = {name: regular(source/name) for name in ARTIFACTS}
    if {name: sha256(raw) for name, raw in originals.items()} != binding['prior_artifacts']:
        raise ValueError('Revision source artifact digest mismatch')
    provenance = json.loads(originals['provenance.json'])
    require_approval_model(source, provenance)
    if (provenance.get('attempt_kind') == 'revision'
            or provenance.get('packet_manifest_sha256') != binding['packet_manifest_sha256']
            or provenance.get('input_mode') != 'entry_analysis' or provenance.get('published') is not False):
        raise ValueError('Revision source must be a fresh historical annotation on the same packet')
    transcript = json.loads(originals['raw-transcript.json'])
    annotation = selected_annotation(transcript, provenance)
    draft, _ = verify_final(annotation, manifest, transcript, provenance)
    if (draft != json.loads(originals['draft.json'])
            or render(draft).encode() != originals['draft.md']):
        raise ValueError('Revision source annotation does not reproduce its draft and rendering')

    if provenance.get('token_usage') != transcript[0].get('teacher_token_usage'):
        raise ValueError('Prior token usage does not match its transcript')
    records = pairs(transcript)
    prefix = 'prior:' + binding['prior_artifacts']['raw-transcript.json'] + ':'
    identities = {record['id']: prefix + record['id'] for record in records}
    for record in records:
        record['id'] = identities[record['id']]
    coverage = coverage_bytes(Path(binding['coverage_path']), binding['coverage_sha256'], manifest)
    return Revision(binding, remap(annotation, identities), records, coverage)


def initial_input(session):
    from .codex_adapter import thread_parameters
    instructions = thread_parameters(session, '.')
    return {**{key: instructions[key] for key in ('baseInstructions', 'developerInstructions')},
            'user': session.initial[1]['content']}


def restore(run, packet, provenance, transcript):
    """Rebuild revision context from originals and verify the saved wire input."""
    from .session import FreshSession
    if provenance.get('attempt_kind') != 'revision':
        return None
    metadata = provenance['revision']
    if (provenance.get('reviewer_assisted') is not True
            or provenance.get('guidance_version') != json.loads(regular(Path(packet)/'manifest.json')).get('guidance_version', 1)
            or metadata['id_map_version'] != ID_MAP_VERSION):
        raise ValueError('Invalid revision provenance')
    revision = prepare(packet, run, metadata['source'])
    artifacts = {name: regular(run/name) for name in REVISION_FILES}
    if {name: sha256(raw) for name, raw in artifacts.items()} != metadata['artifacts']:
        raise ValueError('Revision input artifact digest mismatch')
    session = FreshSession(packet)
    revision.extend(session)
    if (json.loads(artifacts['prior-evidence.json']) != revision.records
            or artifacts['revision.coverage.md'] != revision.coverage
            or json.loads(artifacts['revision-input.json']) != initial_input(session)
            or [row['content'] for row in transcript[:2]] != [row['content'] for row in session.initial]):
        raise ValueError('Revision inputs differ from the verified source')
    return revision
