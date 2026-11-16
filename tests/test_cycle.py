# SPDX-License-Identifier: MIT
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch, Mock
from teacher import cycle


class CycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.state=self.root/'state.json'
        tracking=patch('teacher.cycle.TRACKING',self.root/'tracking.md');tracking.start();self.addCleanup(tracking.stop)
        register=patch('teacher.cycle.REGISTER',self.root/'register.md');register.start();self.addCleanup(register.stop)
        self.ready=dict(status='ready',next_position=2,history_tip='a'*40,runs=[],approved_entries=[])
        self.state.write_text(json.dumps(self.ready))

    def stop(self,status,function,*args):
        with self.assertRaises(cycle.Stop) as caught:function(*args)
        self.assertEqual(caught.exception.status,status)

    def test_state_and_pause(self):
        self.stop('state_not_ready',cycle.guard_state,dict(status='awaiting_full_review'))
        self.stop('advancement_paused',cycle.guard_state,dict(status='ready',advancement_pause={'reason':'user'}))

    def test_disk_guard(self):
        with patch('teacher.cycle.shutil.disk_usage',return_value=Mock(free=1)):
            self.stop('low_disk',cycle.guard_disk,self.root)

    def test_architecture_guards(self):
        bundle=self.root/'reference.json';bundle.write_text('{}')
        with patch('teacher.architecture_evidence.trigger_details',return_value={'unresolved_class_files':['x.py']}):
            self.stop('unresolved_architecture',cycle.architecture_gate,self.root,'a'*40,bundle)
        for value,status in [({'unresolved_architecture_files':['x']},'unresolved_reference_bundle'),
                             ({'administrative_outcome':{'basis':'curator_attestation'}},'curator_attestation')]:
            with patch('teacher.architecture_evidence.trigger_details',return_value={}),patch('teacher.architecture_evidence.load_bundle',return_value=value):
                self.stop(status,cycle.architecture_gate,self.root,'a'*40,bundle)
        with patch('teacher.architecture_evidence.trigger_details',return_value={'derived_architectures':['New']}),patch('teacher.architecture_evidence.load_bundle',return_value={}):
            self.stop('architecture_trigger',cycle.architecture_gate,self.root,'a'*40,bundle)
        with patch('teacher.architecture_evidence.trigger_details',return_value={}),patch('teacher.architecture_evidence.load_bundle',side_effect=ValueError('invalid')):
            self.stop('invalid_reference_bundle',cycle.architecture_gate,self.root,'a'*40,bundle)

    def test_truncation_gate(self):
        self.stop('path_catalog_truncated',cycle.guard_catalog,dict(path_qualified_cut=[{'number':21}],authoring_allowed=False))
        cycle.guard_catalog(dict(path_qualified_cut=[],authoring_allowed=True))

    def test_existing_preparation_is_immutable(self):
        p=self.root/'000002-closed.json';p.write_text('old')
        self.stop('existing_preparation',cycle.write_new,p,{})
        self.assertEqual(p.read_text(),'old')

    def test_cycle_stops_never_invoke_teacher(self):
        for status in ['low_disk','architecture_trigger','unresolved_architecture','unresolved_reference_bundle','curator_attestation','invalid_reference_bundle','path_catalog_truncated','reference_needs_judgement','existing_preparation']:
            self.state.write_text(json.dumps(self.ready))
            with patch('teacher.cycle.ROOT',self.root),patch('teacher.cycle.git',return_value=('a'*40+'\n'+'b'*40+'\n').encode()),patch('teacher.cycle.guard_disk'),patch('teacher.cycle.architecture_gate'),patch('teacher.cycle.recover_inputs',side_effect=cycle.Stop(status,'test')),patch('teacher.cycle.author') as author:
                result=cycle.cycle(self.state,self.root/'auth')
                self.assertEqual(result['status'],status);author.assert_not_called()
                self.assertEqual(cycle.read(self.state)['runs'],[])

    def test_half_started_no_retry(self):
        state=copy.deepcopy(self.ready);state['runs']=[dict(position=2,status='authoring')];self.state.write_text(json.dumps(state))
        with patch('teacher.cycle.ROOT',self.root),patch('teacher.cycle.git',return_value=('a'*40+'\n'+'b'*40+'\n').encode()),patch('teacher.cycle.author') as author:
            self.assertEqual(cycle.cycle(self.state,self.root/'auth')['status'],'half_started_run');author.assert_not_called()

    def test_lock_prevents_concurrent_work(self):
        with cycle.locked(self.state):
            with self.assertRaises(cycle.Stop) as caught:
                with cycle.locked(self.state):pass
            self.assertEqual(caught.exception.status,'busy')

    def test_references_need_judgement_before_recovery(self):
        outputs=[b'2025-01-01T00:00:00Z',b'Change https://github.com/another/repo/issues/1']
        with patch('teacher.cycle.git',side_effect=outputs),patch('teacher.recover_github.recover') as recover:
            self.stop('reference_needs_judgement',cycle.recover_inputs,self.root,'a'*40,2,self.root,self.root);recover.assert_not_called()

    def test_approval_requires_pending_verdict(self):
        self.stop('approval_state_mismatch',cycle.approval,self.state,self.root/'verdict.md')
        state=copy.deepcopy(self.ready);state.update(status='awaiting_full_review',handover={'full_review':'commit-000002-001','request':'request.md'},runs=[{'run':'commit-000002-001','position':2}]);self.state.write_text(json.dumps(state))
        run=self.root/'commit-000002-001';run.mkdir();(run/'provenance.json').write_text('{}')
        v=self.root/'commit-000002-001.md';v.write_text('## Decision\n\n**HELD**\n')
        with patch('teacher.cycle.ROOT',self.root):self.stop('verdict_needs_judgement',cycle.approval,self.state,v)

    def test_skeleton_has_all_hashes_counts_and_explicit_judgement(self):
        summary=dict(run='run',packet='packet',sha='a'*40,title='Exact title',hashes={'draft':'b'*64},catalog=dict(qualified_count=23,selected_count=20,path_only_qualified_count=7,path_only_selected_count=6,cap=20,truncated=True,path_qualified_cut=[{}]),validation=dict(reviewer_assisted=False,identical_replayed_calls=9,shared_readonly_blob_links_verified=31,fully_read_task_sections=[0],task_sections_total=2,ancestor_prose_read_count=0,tool_counts={'repo_read':1},runtime={'python_version':'3.14.4'},open_catalog_rows=13))
        text=cycle.skeleton(summary,'thread');self.assertIn('7 by path alone, 6 selected by path alone',text);self.assertIn('AUTHOR JUDGEMENT REQUIRED',text);self.assertIn('b'*64,text);self.assertIn('1/2',text)

    def test_approval_checks_hashes_preserves_pause_and_tracks_followups(self):
        run=self.root/'commit-000002-001';run.mkdir();packet=self.root/'packet';packet.mkdir()
        files=[run/name for name in ('draft.json','draft.md','raw-transcript.json','provenance.json')]+[packet/'manifest.json']
        for p in files:p.write_text('{}')
        request=self.root/'request.md';request.write_text('\n'.join(f'- {p.relative_to(self.root)}: `{cycle.digest(p)}`' for p in files))
        verdict=self.root/'commit-000002-001.md';verdict.write_text('Run: `commit-000002-001`\n\n## Decision\n\n**APPROVED for ancestor retrieval only.**\n\n## Follow-ups\n\n1. Keep this obligation.\n')
        state=copy.deepcopy(self.ready);state.update(status='awaiting_full_review',advancement_pause={'reason':'implementation'},handover={'full_review':'commit-000002-001','request':'request.md'},runs=[dict(run='commit-000002-001',packet='packet',position=2)])
        self.state.write_text(json.dumps(state))
        with patch('teacher.cycle.ROOT',self.root),patch('teacher.cycle.TRACKING',self.root/'tracking.md'),patch('teacher.cycle.approve_run') as approve:
            result=cycle.approval(self.state,verdict);approve.assert_called_once()
        self.assertEqual(result['next_position'],3);self.assertEqual(result['advancement_pause'],{'reason':'implementation'})
        self.assertIn('Keep this obligation',(self.root/'register.md').read_text())
        self.assertNotIn('Keep this obligation',(self.root/'tracking.md').read_text())
        self.state.write_text(json.dumps(state));files[0].write_text('changed')
        with patch('teacher.cycle.ROOT',self.root),patch('teacher.cycle.approve_run') as approve:
            with self.assertRaisesRegex(ValueError,'hash mismatch'):cycle.approval(self.state,verdict)
            approve.assert_not_called()

    def test_failure_after_authoring_never_files_or_approves(self):
        from contextlib import ExitStack
        with ExitStack() as stack:
            stack.enter_context(patch('teacher.cycle.ROOT',self.root))
            stack.enter_context(patch('teacher.cycle.git',return_value=('a'*40+'\n'+'b'*40+'\n').encode()))
            for name in ('guard_disk','architecture_gate','recover_inputs','index_parent','prepare_packet','author'):
                stack.enter_context(patch('teacher.cycle.'+name))
            stack.enter_context(patch('teacher.cycle.validate_run',side_effect=ValueError('replay mismatch')))
            approve=stack.enter_context(patch('teacher.cycle.approve_mechanical'))
            with self.assertRaisesRegex(ValueError,'replay mismatch'):cycle.cycle(self.state,self.root/'auth')
            approve.assert_not_called()
        self.assertEqual(cycle.read(self.state)['status'],'stopped_failure')
        self.assertEqual(cycle.read(self.state)['runs'][-1]['status'],'failed')
        self.assertFalse((self.root/'reviews/requests').exists())

    def test_replay_compares_error_envelopes_without_masking_mismatches(self):
        call = {'tool': 'evidence_index', 'arguments': {'max_bytes': 24000}}
        result = {'call_id': 'invalid-size', 'content': json.dumps({'ok': False, 'error': 'Invalid max_bytes'})}
        for error in (ValueError, RuntimeError):
            runner = Mock()
            runner.invoke.side_effect = error('Invalid max_bytes')
            cycle.replay_result(runner, call, result)
            runner.invoke.side_effect = error('different error')
            with self.assertRaisesRegex(ValueError, 'Tool replay mismatch: invalid-size'):
                cycle.replay_result(runner, call, result)
        runner.invoke.side_effect = None
        runner.invoke.return_value = {'ok': True, 'result': {}}
        with self.assertRaisesRegex(ValueError, 'Tool replay mismatch'):
            cycle.replay_result(runner, call, result)
        success = dict(result, content=json.dumps(runner.invoke.return_value))
        cycle.replay_result(runner, call, success)
        runner.invoke.side_effect = ValueError('Invalid max_bytes')
        with self.assertRaisesRegex(ValueError, 'Tool replay mismatch'):
            cycle.replay_result(runner, call, success)
        runner.invoke.side_effect = OSError('host failure')
        with self.assertRaises(OSError):
            cycle.replay_result(runner, call, result)

    def test_tracking_status_updates_without_erasing_obligations(self):
        cycle.TRACKING.write_text('# Tracking\n\nOwed obligation.\n')
        cycle.tracking_status(self.ready)
        state=dict(self.ready,status='awaiting_full_review',next_position=3)
        cycle.tracking_status(state)
        text=cycle.TRACKING.read_text();self.assertEqual(text.count('<!-- cycle-status -->'),1)
        self.assertIn('Owed obligation.',text);self.assertIn('Next position: `3`',text)

    def test_approval_refuses_replacement_sibling_and_assisted_without_mutation(self):
        for name, sibling, assisted in [('commit-000002-002',False,False),('commit-000002-001',True,False),('commit-000002-001',False,True)]:
            with self.subTest(name=name,sibling=sibling,assisted=assisted):
                run=self.root/name;run.mkdir(exist_ok=True);(run/'provenance.json').write_text(json.dumps({'reviewer_assisted':assisted}))
                state=copy.deepcopy(self.ready);state.update(status='awaiting_full_review',handover={'full_review':name},runs=[dict(run=name,position=2)])
                if sibling:state['runs'].append(dict(run='prior',position=2,status='rejected'))
                self.state.write_text(json.dumps(state));before=self.state.read_bytes()
                with patch('teacher.cycle.ROOT',self.root),patch('teacher.cycle.approve_run') as approve:
                    self.stop('approval_needs_manual_handling',cycle.approval,self.state,self.root/(name+'.md'))
                    approve.assert_not_called()
                self.assertEqual(self.state.read_bytes(),before)

    def test_preparation_exception_marks_current_run_failed(self):
        from contextlib import ExitStack
        with ExitStack() as stack:
            stack.enter_context(patch('teacher.cycle.ROOT',self.root))
            stack.enter_context(patch('teacher.cycle.git',return_value=('a'*40+'\n'+'b'*40+'\n').encode()))
            for name in ('guard_disk','architecture_gate','recover_inputs','index_parent'):
                stack.enter_context(patch('teacher.cycle.'+name))
            stack.enter_context(patch('teacher.cycle.prepare_packet',side_effect=ValueError('preparation failed')))
            author=stack.enter_context(patch('teacher.cycle.author'))
            with self.assertRaisesRegex(ValueError,'preparation failed'):cycle.cycle(self.state,self.root/'auth')
            author.assert_not_called()
        self.assertEqual(cycle.read(self.state)['runs'][-1]['status'],'failed')

    def test_skeleton_only_full_review_and_outside_mailbox(self):
        from contextlib import ExitStack
        for tier in ('full_review','mechanical'):
            with self.subTest(tier=tier),tempfile.TemporaryDirectory() as tmp,ExitStack() as stack:
                root=Path(tmp);(root/'reports').mkdir();state=root/'state.json';state.write_text(json.dumps(self.ready))
                stack.enter_context(patch('teacher.cycle.ROOT',root))
                stack.enter_context(patch('teacher.cycle.git',return_value=('a'*40+'\n'+'b'*40+'\n').encode()))
                for name in ('guard_disk','architecture_gate','index_parent','prepare_packet','author','tracking_status','approve_mechanical'):
                    stack.enter_context(patch('teacher.cycle.'+name))
                stack.enter_context(patch('teacher.cycle.recover_inputs',return_value=root/'catalog.json'))
                stack.enter_context(patch('teacher.cycle.validate_run',return_value={'assessment':{'tier':tier,'sampled':False}}))
                stack.enter_context(patch('teacher.cycle.make_summary',return_value={'catalog':{},'hashes':{}}))
                writer=stack.enter_context(patch('teacher.cycle.skeleton',return_value='Unfiled skeleton'))
                cycle.cycle(state,root/'auth')
                paths=list(root.rglob('*.skeleton.md'))
                self.assertFalse((root/'reviews/requests').exists())
                if tier=='full_review':
                    self.assertEqual(len(paths),1);self.assertEqual(paths[0].parent,root/'reports');writer.assert_called_once()
                else:self.assertEqual(paths,[]);writer.assert_not_called()

    def test_named_stop_after_preparation_marks_failed(self):
        from contextlib import ExitStack
        with ExitStack() as stack:
            stack.enter_context(patch('teacher.cycle.ROOT',self.root))
            stack.enter_context(patch('teacher.cycle.git',return_value=('a'*40+'\n'+'b'*40+'\n').encode()))
            stack.enter_context(patch('teacher.cycle.guard_disk',side_effect=[None,cycle.Stop('low_disk','test')]))
            for name in ('architecture_gate','recover_inputs','index_parent','prepare_packet'):
                stack.enter_context(patch('teacher.cycle.'+name))
            author=stack.enter_context(patch('teacher.cycle.author'))
            self.assertEqual(cycle.cycle(self.state,self.root/'auth')['status'],'low_disk')
            author.assert_not_called()
        self.assertEqual(cycle.read(self.state)['runs'][-1]['status'],'failed')
