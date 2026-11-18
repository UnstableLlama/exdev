# SPDX-License-Identifier: MIT
"""Revision isolation, provenance and replay with an offline transport."""
from contextlib import ExitStack, nullcontext
from copy import deepcopy
import json
from pathlib import Path
import shutil
import threading
import unittest
from unittest.mock import patch

from orchestration import run_ahead as queue
from teacher import cycle
from teacher.ancestor_context import approve_run, attach_entries
from teacher.author import author, author_revision, write_json
from teacher.editorial import validate_annotation
from teacher.revision import ARTIFACTS, INSTRUCTION, prepare, restore, sha256
from teacher.runner import Runner
from teacher.session import FreshSession
from test_codex_teacher import FakeTransport
from test_editorial import fixture
from test_run_ahead import state
import test_ancestor_context
import test_teacher_packet


class Transport(FakeTransport):
    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass


def usage_event(input_tokens, cached, output):
    return dict(method='thread/tokenUsage/updated', params=dict(
        threadId='fresh', turnId='turn', tokenUsage={'total': {
            'inputTokens': input_tokens, 'cachedInputTokens': cached, 'outputTokens': output,
        }}))


class RevisionTests(unittest.TestCase):
    def setUp(self):
        test_teacher_packet.PacketTests.setUp(self)
        root, root_packet = test_ancestor_context.AncestorContextTests.run_fixture(self)
        approve_run(root, root_packet, 'TEST', 'ROOT')
        attach_entries(self.packet, [root])
        manifest = self.packet/'manifest.json'
        write_json(manifest, dict(cycle.read(manifest), unreferenced_discussion_catalog=[],
                                  unreferenced_discussion_truncated=False,
                                  closed_discussion_catalog={'rows': [], 'limit': 20, 'truncated': False}))
        self.source = self.root/'commit-000002-001'
        self.target = self.root/'commit-000002-002'
        self.coverage = self.root/'commit-000002-002.coverage.md'
        self.coverage.write_text('- What does `a.py` at lines 1 define?\n')
        transport = self.transport(fixture())
        transport.events.insert(0, usage_event(5, 0, 1))
        transport.events.insert(-1, usage_event(12, 6, 4))
        author(self.packet, self.source, 'unused', transport_factory=lambda _: transport)
        self.assertEqual(json.loads(transport.requests[2][1]['input'][0]['text']),
                         json.loads(FreshSession(self.packet).initial[1]['content']))
        self.assertNotIn(INSTRUCTION, transport.requests[1][1]['baseInstructions'])
        self.bind()

    tearDown = test_teacher_packet.PacketTests.tearDown

    def bind(self):
        self.binding = dict(
            revision_of_run=str(self.source), position=2, task_sha=self.task,
            packet=str(self.packet), packet_manifest_sha256=queue.digest(self.packet/'manifest.json'),
            prior_artifacts={name: queue.digest(self.source/name) for name in ARTIFACTS},
            coverage_path=str(self.coverage), coverage_sha256=queue.digest(self.coverage),
        )

    def transport(self, annotation, identity='read-1'):
        transport = Transport()
        transport.events[0]['params'].update(callId=identity, arguments={'commit': self.task})
        transport.events[1]['params']['item']['text'] = json.dumps(annotation)
        return transport

    def test_projection_and_full_mock_revision(self):
        path = self.source/'raw-transcript.json'
        transcript = json.loads(path.read_text())
        transcript[1]['content'] = 'PRIOR PROMPT SECRET'
        transcript.insert(-1, {'role': 'assistant', 'content': 'PRIOR COMMENTARY SECRET'})
        transcript.insert(-1, {'role': 'assistant', 'reasoning': 'PRIOR REASONING SECRET'})
        write_json(path, transcript)
        for name in ('review.json', 'verdict.md', 'ledger.json'):
            (self.source/name).write_text(name + ' SECRET')
        (self.root/'commit-000002-003').mkdir()
        (self.root/'commit-000002-003'/'draft.json').write_text('OTHER ATTEMPT SECRET')
        self.bind()
        before = {p: p.read_bytes() for p in self.source.iterdir()}
        prepared = prepare(self.packet, self.target, self.binding)
        identity = prepared.records[0]['id']
        self.assertEqual(identity, 'prior:' + queue.digest(path) + ':read-1')
        annotation = fixture()
        annotation['problem'][0]['text'] = 'Fresh teacher output for the revision.'
        annotation['problem'][0]['evidence'] = [identity, 'new-read']
        transport = self.transport(annotation, 'new-read')
        transport.events.insert(-1, usage_event(30, 20, 8))
        author_revision(self.packet, self.target, 'unused', revision=self.binding,
                        transport_factory=lambda _: transport)
        self.assertEqual(before, {p: p.read_bytes() for p in before})
        wire = json.dumps(transport.requests)
        self.assertNotIn('SECRET', wire)
        self.assertIn(INSTRUCTION, transport.requests[1][1]['baseInstructions'])
        provenance = cycle.read(self.target/'provenance.json')
        raw = cycle.read(self.target/'raw-transcript.json')
        self.assertEqual([m['call_id'] for m in raw if m['role'] == 'tool'], ['new-read'])
        self.assertEqual(provenance['token_usage'], {'input': 30, 'cached_input': 20, 'output': 8})
        self.assertTrue(provenance['reviewer_assisted'])
        self.assertEqual(cycle.read(self.target/'draft.json')['annotation'], annotation)
        self.assertEqual(cycle.read(self.target/'coverage.json')['revision_reads']['prior']['tool_calls'], 1)
        with self.assertRaisesRegex(ValueError, 'through the review queue'):
            approve_run(self.target, self.packet, 'reviewer', 'note')
        evidence = self.root/'evidence'
        evidence.mkdir()
        from teacher.approval_policy import assess
        self.assertEqual(assess(self.target, self.packet, self.repo)['tier'], 'full_review')
        with patch.object(cycle, 'validate_bundle'):
            report = cycle.validate_run(self.target, self.packet, self.repo, evidence, 2)
        self.assertEqual(report['prior_token_usage'], {'input': 12, 'cached_input': 6, 'output': 4})
        self.assertEqual((report['prior_identical_replayed_calls'], report['identical_replayed_calls']), (1, 1))
        review = approve_run(self.target, self.packet, 'reviewer', 'note', revision_validation=report)
        self.assertTrue(review['ancestor_context_approved'])
        self.assertFalse(review['training_eligible'] or review['canonical_approved'])
        (self.target/'prior-evidence.json').write_text('[]')
        with self.assertRaisesRegex(ValueError, 'artifact digest'):
            restore(self.target, self.packet, provenance, raw)

    def test_refuses_changed_or_missing_sources(self):
        for name in ARTIFACTS:
            with self.subTest(name=name):
                path = self.source/name
                original = path.read_bytes()
                path.unlink()
                with self.assertRaises(ValueError):
                    prepare(self.packet, self.target, self.binding)
                path.write_bytes(original + b' ')
                with self.assertRaisesRegex(ValueError, 'artifact digest'):
                    prepare(self.packet, self.target, self.binding)
                path.write_bytes(original)

    def test_wrong_position_task_manifest_or_packet(self):
        with self.assertRaisesRegex(ValueError, 'same position'):
            prepare(self.packet, self.root/'commit-000003-002', self.binding)
        with self.assertRaisesRegex(ValueError, 'task SHA'):
            prepare(self.packet, self.target, dict(self.binding, task_sha=self.future))
        alternate = self.root/'alternate-packet'
        shutil.copytree(self.packet, alternate)
        with self.assertRaisesRegex(ValueError, 'identical original packet'):
            prepare(alternate, self.target, self.binding)
        manifest = self.packet/'manifest.json'
        manifest.write_bytes(manifest.read_bytes() + b' ')
        with self.assertRaisesRegex(ValueError, 'identical original packet'):
            prepare(self.packet, self.target, self.binding)

    def test_coverage_exact_bytes_and_fact_rejected(self):
        self.coverage.write_text('- What does `a.py` define?\n- a.py returns 2.\n')
        with self.assertRaisesRegex(ValueError, 'coverage digest'):
            prepare(self.packet, self.target, self.binding)
        self.bind()
        with self.assertRaisesRegex(ValueError, 'only questions'):
            prepare(self.packet, self.target, self.binding)
        manifest = self.packet/'manifest.json'
        value = cycle.read(manifest)
        write_json(manifest, dict(value, coverage_request={}))
        self.bind()
        with self.assertRaisesRegex(ValueError, 'attempt-specific coverage'):
            prepare(self.packet, self.target, self.binding)

    def test_ambiguous_finals_and_trial_source_rejected(self):
        raw = self.source/'raw-transcript.json'
        original = cycle.read(raw)
        for transcript in (original[:-1], [*original, original[-1]],
                           [*original[:-1], {'role': 'assistant', 'content': '{}'}]):
            write_json(raw, transcript)
            self.bind()
            with self.assertRaisesRegex(ValueError, 'final annotation'):
                prepare(self.packet, self.target, self.binding)
        write_json(raw, original)
        provenance = self.source/'provenance.json'
        write_json(provenance, dict(cycle.read(provenance), trial_only=True))
        self.bind()
        with self.assertRaisesRegex(ValueError, 'non-trial'):
            prepare(self.packet, self.target, self.binding)

    def test_forged_prior_id_and_exact_replay(self):
        revision = prepare(self.packet, self.target, self.binding)
        annotation = deepcopy(revision.annotation)
        prior = revision.prior
        validate_annotation(annotation, cycle.read(self.packet/'manifest.json'), [], prior=prior)
        with self.assertRaisesRegex(ValueError, 'Reserved prior'):
            validate_annotation(annotation, cycle.read(self.packet/'manifest.json'), prior)
        annotation['problem'][0]['evidence'] = ['prior:' + '0' * 64 + ':read-1']
        with self.assertRaisesRegex(ValueError, 'Unknown or unsuccessful'):
            validate_annotation(annotation, cycle.read(self.packet/'manifest.json'), [], prior=prior)
        call, result = prior[0]['calls'][0], prior[1]
        runner = Runner(self.packet)
        cycle.replay_result(runner, call, result, exact=True)
        for wrong_call, wrong_result in ((call, dict(result, content=result['content'] + ' ')),
                                        (dict(call, arguments={'commit': self.future}), result)):
            with self.assertRaisesRegex(ValueError, 'replay mismatch'):
                cycle.replay_result(runner, wrong_call, wrong_result, exact=True)

    def test_request_discloses_comparison_replays_and_first_three_usage(self):
        item = {'revision_of_run': str(self.source), 'revision_number': 1,
                'revision_source': self.binding, 'completed_record': {'validation': 'validation.json'},
                'revision_admin': {}, 'spec': 'spec.json'}
        report = dict(status='validated', revision={'source': self.binding},
                      prior_identical_replayed_calls=12, identical_replayed_calls=2,
                      prior_token_usage=None, token_usage={'input': 30, 'cached_input': 20, 'output': 8})
        write_json(self.root/'validation.json', report)
        write_json(self.root/'spec.json', {})
        item['spec_sha256'] = queue.digest(self.root/'spec.json')
        disclosure = queue.revision_disclosure(item, report)
        for expected in ('First live revision', 'Line-by-line comparison requested', 'Prior calls replayed: 12',
                         'New calls replayed: 2', 'Fresh attempt tokens: unavailable', '"cached_input": 20'):
            self.assertIn(expected, disclosure)
        self.assertIn('Revision tokens:', queue.revision_disclosure(dict(item, revision_number=3), report))
        self.assertNotIn('Revision tokens:', queue.revision_disclosure(dict(item, revision_number=4), report))
        text = disclosure + '\n' + '\n'.join(f'### {heading}\n\nObserved change.' for heading in
                                                ('Kept', 'Added', 'Removed', 'Corrected'))
        with patch.object(queue, 'ROOT', self.root), patch.object(queue, 'revision_request_files', return_value=[]):
            queue.validate_revision_request(item, text)
            with self.assertRaisesRegex(ValueError, 'side-by-side'):
                queue.validate_revision_request(item, text.replace('### Corrected', '### Other'))
            with self.assertRaisesRegex(ValueError, 'disclosure'):
                queue.validate_revision_request(item, text.replace('New calls replayed: 2', 'New calls replayed: 1'))
            report['revision']['source'] = {}
            write_json(self.root/'validation.json', report)
            with self.assertRaisesRegex(ValueError, 'validated reserved source'):
                queue.validate_revision_request(item, text)

    def test_prepared_revision_requires_explicit_mode_and_reaches_review(self):
        root = self.root
        run = '.teacher/runs/commit-000002-002'
        packet = '.teacher/retrieval/000002-001'
        (root/run).parent.mkdir(parents=True)
        (root/packet).parent.mkdir(parents=True)
        (root/'reviews/verdicts').mkdir(parents=True)
        (root/'reports').mkdir()
        self.packet.rename(root/packet)
        store = root/'.teacher/blob-store'
        store.mkdir()
        for blob in (root/packet/'blobs').iterdir():
            (store/blob.name).hardlink_to(blob)
        authorization = root/'reviews/verdicts/recovery.md'
        authorization.write_text('Authorise revision')
        verdict = root/'reviews/verdicts/previous.md'
        verdict.write_text('Rejected')
        catalog = root/'reports/commit-000002-catalog-selection-001.json'
        write_json(catalog, {})
        self.coverage = root/'reviews/verdicts/commit-000002-002.coverage.md'
        self.coverage.write_text('- What does `a.py` define?\n')
        def relative(path):
            return str(Path(path).relative_to(root))
        source = dict(self.binding, coverage_path=str(self.coverage),
                      coverage_sha256=queue.digest(self.coverage))
        spec = dict(run=run, packet=packet, position=2, kind='forward',
                    revision_of_run=self.source.name,
                    authorization={'path': relative(authorization), 'sha256': queue.digest(authorization)})
        descriptor = root/'spec.json'
        write_json(descriptor, spec)
        journal = root/'journal.json'
        current = state()
        current['history_tip'] = self.task
        current['review_queue'].append(dict(run=self.source.name, status='rejected', position=2,
                                            verdict=relative(verdict), verdict_sha256=queue.digest(verdict)))
        current['retry_only'] = {'position': 2, 'kind': 'forward'}
        write_json(journal, current)
        report = dict(status='validated', revision={'source': source}, prior_identical_replayed_calls=1,
                      identical_replayed_calls=2, prior_token_usage=None, token_usage=None)
        with ExitStack() as stack:
            stack.enter_context(patch.object(queue, 'ROOT', root))
            stack.enter_context(patch.object(cycle, 'relative', side_effect=relative))
            stack.enter_context(patch.object(cycle, 'git', return_value=('root\n'+self.task).encode()))
            stack.enter_context(patch.object(cycle, 'validate_bundle'))
            stack.enter_context(patch.object(queue, 'changed_files', return_value=['a.py']))
            stack.enter_context(patch.object(queue, 'verify_selection', return_value=[]))
            stack.enter_context(patch.object(queue, 'revision_source', return_value=source))
            stack.enter_context(patch.object(queue, 'provenance_binding', return_value=nullcontext()))
            stack.enter_context(patch.object(cycle, 'validate_run', return_value=report))
            stack.enter_context(patch.object(cycle, 'make_summary', return_value={'hashes': {}}))
            stack.enter_context(patch.object(cycle, 'skeleton', return_value='request skeleton'))
            stack.enter_context(patch.object(queue, 'revision_request_files', return_value=[]))
            mock_teacher = stack.enter_context(patch('teacher.author.author_revision'))
            with self.assertRaisesRegex(ValueError, 'explicit author_revision'):
                queue.prepared(journal, 'unused', descriptor)
            result = queue.prepared(journal, 'unused', descriptor, revision=True)
            mock_teacher.assert_called_once_with(root/packet, root/run, 'unused', revision=source)
        self.assertEqual(result['status'], 'awaiting_review_request')
        recorded = cycle.read(journal)
        self.assertEqual(recorded['queue_stop'], {'outcome': 'retry_awaiting_verdict', 'run': run})
        self.assertEqual(recorded['review_queue'][-1]['revision_source'], source)

    def test_revision_failure_leaves_reservation_under_concurrent_attempts(self):
        path = self.root/'state.json'
        prior = '.teacher/runs/commit-000002-001'
        packet = '.teacher/retrieval/000002-001'
        verdict = self.root/'verdict.md'
        verdict.write_text('Rejected')
        spec = dict(self.binding, run='.teacher/runs/commit-000002-002', revision_of_run=prior,
                    packet=packet, kind='forward', coverage={
                        'path': 'reviews/verdicts/commit-000002-002.coverage.md',
                        'sha256': self.binding['coverage_sha256'],
                    }, authorization={'path': 'verdict.md', 'sha256': queue.digest(verdict)})
        journal = state()
        journal['review_queue'].append(dict(
            run=prior, status='rejected', position=2, kind='forward', packet=packet, token='rejected',
            verdict='verdict.md', verdict_sha256=queue.digest(verdict),
            packet_manifest_sha256=spec['packet_manifest_sha256']))
        journal.update(retry_only=dict(kind='forward', position=2, stopped_token='rejected'),
                       recovery_log=[dict(stop={'run': prior}, **spec['authorization'])])
        journal['recovery_log'][0]['authorization'] = journal['recovery_log'][0].pop('path')
        write_json(path, journal)
        errors = []
        ready = threading.Barrier(2)
        def reserve():
            ready.wait()
            try:
                with queue.transaction(path) as current:
                    queue.revision_source(current, spec, {'task_sha': self.task})
                    item = queue.reserve(current, position=2, kind='forward', files=[], run=spec['run'], packet=packet)
                    current['review_queue'][-1]['revision_of_run'] = prior
                    queue.finish(current, item['token'], stop={'run': spec['run']})
            except ValueError as error:
                errors.append(str(error))

        with patch.object(queue, 'ROOT', self.root), patch.object(queue, 'check_verdict'):
            threads = [threading.Thread(target=reserve) for _ in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.assertEqual(errors, ['A revision is already reserved for this rejection'])
            final = cycle.read(path)
            self.assertEqual(final['review_queue'][-1]['status'], 'failed')
            self.assertEqual(final['review_queue'][-1]['revision_of_run'], prior)
