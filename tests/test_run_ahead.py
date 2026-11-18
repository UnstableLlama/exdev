"""Administrative queue and sparse approved-prose boundary regression tests."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from orchestration import run_ahead as q
from orchestration.ancestor_selection import installed, selected_manifest, sparse_attach
from teacher.ancestor_context import approve_run, attach_entries
from teacher.author import author, write_json
from teacher.packet import build_packet
from teacher.session import FreshSession
from teacher import runner, worker
import test_ancestor_context


def state():
    return dict(status='ready',next_position=2,runs=[],approved_entries=[],review_queue=[],
                active_session=None,run_ahead={'enabled':True})


def complete(s, position=2, kind='forward', files=('a.py',)):
    item=q.reserve(s,position=position,kind=kind,files=files)
    if kind=='replacement':
        s['review_queue'][-1]['supersedes_run']='old'
    row=dict(position=position,run=f'run-{position}',packet=f'packet-{position}',status='awaiting_review_request')
    q.finish(s,item['token'],row=row)
    return s['review_queue'][-1]


class QueueTests(unittest.TestCase):
    def test_provenance_binding_persists_selection_on_each_write_and_restores_writer(self):
        import importlib
        module = importlib.import_module('teacher.author')
        original = module.write_json
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); packet = root/'packet'; packet.mkdir()
            output = root/'run'; output.mkdir()
            manifest = dict(history_order=['a','b'], ancestor_entries=[{'sha':'a'}])
            write_json(packet/'manifest.json',manifest)
            hashes = {'orchestration/run_ahead.py':'bound'}
            with patch.object(q,'implementation_hashes',return_value=hashes), patch.object(q,'verify_selection',return_value=['approved-a']) as verify:
                with self.assertRaisesRegex(RuntimeError,'provider failure'):
                    with q.provenance_binding(packet,output,['approved-a'],hashes):
                        for phase in ('initial','final'):
                            module.write_json(output/'provenance.json',{'phase':phase})
                        module.write_json(output/'other.json',{'unrelated':True})
                        raise RuntimeError('provider failure')
                verify.assert_called_once_with(packet,['approved-a'])
            self.assertIs(module.write_json,original)
            p=json.loads((output/'provenance.json').read_text())
            self.assertEqual(p['phase'],'final')
            self.assertEqual(p['orchestration'],dict(implementation_sha256=hashes,
                selected_approved_entries=['approved-a'],ancestor_entries=manifest['ancestor_entries'],
                packet_manifest_sha256=q.digest(packet/'manifest.json'),visible_ancestor_count=1,
                strict_ancestor_count=2,sparse=True))
            self.assertEqual(json.loads((output/'other.json').read_text()),{'unrelated':True})

    def test_provenance_binding_refuses_changed_code_or_unapproved_selection(self):
        with patch.object(q,'implementation_hashes',return_value={'changed':'hash'}), patch.object(q,'verify_selection') as verify:
            with self.assertRaisesRegex(ValueError,'changed after reservation'):
                with q.provenance_binding('packet','output',[],{}): pass
            verify.assert_not_called()
        with patch.object(q,'implementation_hashes',return_value={}), patch.object(q,'verify_selection',side_effect=ValueError('Unapproved')):
            with self.assertRaisesRegex(ValueError,'Unapproved'):
                with q.provenance_binding('packet','output',[],{}): pass

    def test_migration_preserves_forward_and_replacement_pending(self):
        s=state();s.pop('review_queue');s.pop('active_session')
        s.update(status='awaiting_full_review',handover={'full_review':'r2','sampled_mechanical':['r1']},
                 runs=[dict(run='r2',packet='p2',position=2,status='pending_full_review')],
                 replacement_reviews=[dict(candidate_run='replacement',packet='oldpacket',position=1,
                     supersedes_run='old',status='awaiting_review_request')])
        migrated=q.migrate(s)
        self.assertEqual(migrated['next_position'],3)
        self.assertEqual([r['kind'] for r in migrated['review_queue']],['forward','replacement'])
        self.assertEqual(migrated['review_queue'][0]['sampled_mechanical'],['r1'])
        self.assertEqual(s['next_position'],2)
        with self.assertRaises(ValueError):q.migrate(migrated)
        s['status']='running'
        with self.assertRaises(ValueError):q.migrate(s)

    def test_enable_is_opt_in_and_completed_verdict_required(self):
        s=state();s.pop('run_ahead')
        with self.assertRaises(ValueError):q.reserve(s,position=2,kind='forward',files=[])
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):q.enable(Path(d)/'state',Path(d)/'design.md')

    def test_mixed_capacity_counts_reservation_and_captures_overlap(self):
        s=state();a=complete(s);a['status']='pending_full_review'
        b=complete(s,position=1,kind='replacement',files=('b.py',));b['status']='pending_full_review'
        c=q.reserve(s,position=3,kind='forward',files=['a.py','a.py','c.py'])
        self.assertEqual(len(s['review_queue']),3)
        self.assertEqual([(d['position'],d['touches_same_file'],d['overlapping_files']) for d in c['ran_ahead_of']],
                         [(2,True,['a.py']),(1,False,[])])
        with self.assertRaises(ValueError):q.reserve(s,position=3,kind='forward',files=[])
        s['active_session']=None;s['status']='ready'
        with self.assertRaisesRegex(ValueError,'Three'):q.reserve(s,position=3,kind='forward',files=[])

    def test_unpublished_draft_and_pause_block_start(self):
        s=state();complete(s)
        with self.assertRaisesRegex(ValueError,'File'):q.reserve(s,position=3,kind='forward',files=[])
        for key in ('advancement_pause','queue_stop'):
            s=state();s[key]={'reason':'review'}
            with self.assertRaises(ValueError):q.reserve(s,position=2,kind='forward',files=[])
        s=state();s['replacement_pause']=True
        with self.assertRaises(ValueError):q.reserve(s,position=1,kind='replacement',files=[])
        q.reserve(s,position=2,kind='forward',files=[])

    def test_finish_preserves_rejection_arriving_during_session(self):
        s=state();i=q.reserve(s,position=2,kind='forward',files=[])
        s['queue_stop']={'outcome':'rejected','run':'earlier'}
        q.finish(s,i['token'],row=dict(position=2,run='r2',packet='p2'))
        self.assertEqual(s['status'],'stopped_recovery')
        self.assertEqual(s['next_position'],3)
        with self.assertRaises(ValueError):q.finish(s,i['token'],row={})
        with self.assertRaises(ValueError):q.reserve(s,position=3,kind='forward',files=[])

    def test_failed_reservation_does_not_advance_and_stale_completion_refused(self):
        s=state();i=q.reserve(s,position=2,kind='forward',files=[])
        q.finish(s,i['token'],stop={'kind':'error','position':2})
        self.assertEqual(s['next_position'],2)
        self.assertEqual(s['status'],'stopped_failure')
        with self.assertRaises(ValueError):q.finish(s,i['token'],row={})

    def test_publication_binds_request_and_requires_ahead_note(self):
        with tempfile.TemporaryDirectory() as d, patch.object(q,'ROOT',Path(d)), patch.object(q.legacy,'ROOT',Path(d)):
            s=state();a=complete(s);a['status']='pending_full_review'
            b=complete(s,3);request=Path(d)/'reviews/requests/run-3.md';request.parent.mkdir(parents=True);request.write_text('run-3')
            with self.assertRaises(ValueError):q.publish(s,'run-3',request)
            request.write_text('run-3\nRan ahead of: 2.\n')
            q.publish(s,'run-3',request)
            self.assertEqual(b['request_sha256'],q.digest(request))
            with self.assertRaises(ValueError):q.publish(s,'run-3',request)

    def test_forward_approval_order_including_failed_and_mechanical(self):
        s=state();a=complete(s);a['status']='pending_full_review'
        b=complete(s,3);b['status']='pending_full_review'
        with self.assertRaises(ValueError):q.approval_guard(s,b)
        a['status']='approved_reviewed';s['runs'][0]['status']='approved_mechanical'
        q.approval_guard(s,b)
        s['runs'][0]['status']='failed'
        with self.assertRaises(ValueError):q.approval_guard(s,b)

    def test_legacy_superseded_attempts_require_an_approved_successor(self):
        for status in ('superseded_missing_inputs', 'superseded_for_future_retrieval'):
            with self.subTest(status=status):
                s=state();a=complete(s);a['status']='approved_reviewed'
                s['runs'][0]['status']='approved_reviewed'
                s['runs'].append(dict(position=2,run='legacy-attempt',status=status))
                b=complete(s,3);b['status']='pending_full_review'
                q.approval_guard(s,b)
                s['runs'][0]['status']='failed'
                with self.assertRaisesRegex(ValueError,'Earlier failed/rejected position still unresolved'):
                    q.approval_guard(s,b)

    def test_legacy_position_approved_only_in_replacement_reviews(self):
        s=state();a=complete(s);a['status']='approved_reviewed'
        s['runs'][0]['status']='superseded_for_future_retrieval'
        s['replacement_reviews']=[dict(position=2,candidate_run='replacement',status='approved_reviewed')]
        b=complete(s,3);b['status']='pending_full_review'
        q.approval_guard(s,b)
        s['replacement_reviews'][0]['status']='rejected'
        with self.assertRaisesRegex(ValueError,'Earlier failed/rejected position still unresolved'):
            q.approval_guard(s,b)

    def test_transaction_serializes_updates_and_rolls_back_exception(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'state.json';write_json(path,dict(counter=0,status='running',active_session='teacher'))
            def update():
                for _ in range(10):
                    with q.transaction(path) as s:s['counter']+=1
            threads=[threading.Thread(target=update) for _ in range(4)]
            for t in threads:t.start()
            for t in threads:t.join()
            s=json.loads(path.read_text());self.assertEqual(s['counter'],40)
            self.assertEqual(s['active_session'],'teacher')
            with self.assertRaises(RuntimeError):
                with q.transaction(path) as s:s['counter']=100;raise RuntimeError()
            self.assertEqual(json.loads(path.read_text())['counter'],40)

    def test_recover_requires_bound_run_and_retry_blocks_other_work(self):
        with tempfile.TemporaryDirectory() as d, patch.object(q,'ROOT',Path(d)),patch.object(q.legacy,'ROOT',Path(d)):
            root=Path(d);(root/'reviews/verdicts').mkdir(parents=True)
            decision=root/'reviews/verdicts/recovery.md';decision.write_text('r2 recovery')
            s=state();i=q.reserve(s,position=2,kind='forward',files=[],run='r2',packet='p2')
            q.finish(s,i['token'],stop={'run':'r2','position':2})
            path=root/'state.json';write_json(path,s)
            decision.write_text('wrong')
            with self.assertRaises(ValueError):q.recover(path,decision,retry_position=2)
            decision.write_text('r2 recovery')
            q.recover(path,decision,retry_position=2)
            s=json.loads(path.read_text())
            for position,kind in [(3,'forward'),(2,'replacement')]:
                with self.assertRaises(ValueError):q.reserve(s,position=position,kind=kind,files=[],run='retry',packet='p2')
            q.reserve(s,position=2,kind='forward',files=[],run='retry',packet='p2')

    def test_approval_during_session_preserves_active_and_next_position(self):
        with tempfile.TemporaryDirectory() as d,patch.object(q,'ROOT',Path(d)),patch.object(q.legacy,'ROOT',Path(d)):
            root=Path(d);s=state();a=complete(s);a['status']='pending_full_review'
            active=q.reserve(s,position=3,kind='forward',files=[])
            path=root/'state.json';write_json(path,s)
            verdict=root/'verdict.md';verdict.write_text('approved')
            with patch.object(q,'check_verdict'),patch.object(q.legacy,'validate_run'),patch.object(q.legacy,'approve_run'):
                q.approve(path,'run-2',verdict)
            s=json.loads(path.read_text())
            self.assertEqual(s['next_position'],3)
            self.assertEqual(s['active_session'],active['token'])
            self.assertEqual(s['status'],'running')
            self.assertIn('run-2',s['approved_entries'])

    def test_private_worker_forces_full_review_and_restores_globals(self):
        original,tracking,original_author=q.legacy.assess,q.legacy.TRACKING,q.legacy.author
        def cycle(*args):
            self.assertEqual(q.legacy.assess()['tier'],'full_review')
            raise RuntimeError('test failure')
        snapshot=json.dumps({'review_queue':[{'status':'reserved','approved_entries_snapshot':[], 'implementation_sha256':{}}]})
        with patch.object(q.legacy,'assess',return_value={'tier':'mechanical'}),patch.object(q.legacy,'cycle',side_effect=cycle),patch.object(Path,'read_text',return_value=snapshot):
            with self.assertRaises(RuntimeError):q.worker(Path('private.json'),Path('auth'))
        self.assertIs(q.legacy.assess,original);self.assertEqual(q.legacy.TRACKING,tracking)
        self.assertIs(q.legacy.author,original_author)


    def test_verdict_binds_run_request_artifacts_and_explicit_decision(self):
        with tempfile.TemporaryDirectory() as d, patch.object(q,'ROOT',Path(d)), patch.object(q.legacy,'ROOT',Path(d)):
            root=Path(d);run='.teacher/runs/commit-000002-001';packet='.teacher/retrieval/000002-001'
            names=[run+'/'+f for f in ('draft.json','draft.md','raw-transcript.json','provenance.json')]+[packet+'/manifest.json']
            for name in names:
                path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('{}')
            request=root/'reviews/requests/commit-000002-001.md';request.parent.mkdir(parents=True)
            request.write_text(run+'\n'+'\n'.join('- '+n+': `'+q.digest(root/n)+'`' for n in names))
            item=dict(run=run,packet=packet,request=str(request.relative_to(root)),request_sha256=q.digest(request))
            verdict=root/'reviews/verdicts/commit-000002-001.md';verdict.parent.mkdir(parents=True)
            good='# '+run+'\n## Decision\nAPPROVED for ancestor retrieval only\n'
            verdict.write_text(good);q.check_verdict(item,verdict)
            for decision in ('REJECTED','HELD','NOT approved for ancestor retrieval only'):
                verdict.write_text(good.replace('APPROVED for ancestor retrieval only',decision))
                with self.assertRaises(ValueError):q.check_verdict(item,verdict)
            verdict.write_text(good)
            (root/names[0]).write_text('changed')
            with self.assertRaisesRegex(ValueError,'artifact changed'):q.check_verdict(item,verdict)
            (root/names[0]).write_text('{}');request.write_text(request.read_text()+'\nchanged')
            with self.assertRaisesRegex(ValueError,'Request changed'):q.check_verdict(item,verdict)
            with self.assertRaisesRegex(ValueError,'filename'):q.check_verdict(item,root/'wrong.md')

    def test_hold_and_rejection_recorded_during_teacher_preserve_active(self):
        for outcome in ('held','rejected'):
            with tempfile.TemporaryDirectory() as d,patch.object(q,'ROOT',Path(d)),patch.object(q.legacy,'ROOT',Path(d)):
                root=Path(d);s=state();a=complete(s);a['status']='pending_full_review'
                active=q.reserve(s,position=3,kind='forward',files=[])
                path=root/'state.json';write_json(path,s);verdict=root/'verdict.md';verdict.write_text(outcome)
                with patch.object(q,'check_verdict'):q.record_stop(path,'run-2',verdict,outcome)
                s=json.loads(path.read_text());self.assertEqual(s['active_session'],active['token'])
                self.assertEqual(s['status'],'running');self.assertEqual(s['review_queue'][0]['status'],outcome)
                q.finish(s,active['token'],row=dict(position=3,run='later',packet='p3'))
                self.assertEqual(s['status'],'stopped_recovery');self.assertEqual(s['next_position'],4)
                with self.assertRaises(ValueError):q.reserve(s,position=4,kind='forward',files=[])

    def test_replacement_approval_switches_active_without_forward_advancement(self):
        with tempfile.TemporaryDirectory() as d,patch.object(q,'ROOT',Path(d)),patch.object(q.legacy,'ROOT',Path(d)):
            root=Path(d);s=state();s['approved_entries']=['old'];s['runs']=[dict(position=1,run='old',status='approved_reviewed')]
            item=complete(s,position=1,kind='replacement');item['status']='pending_full_review'
            path=root/'state.json';write_json(path,s);verdict=root/'verdict.md';verdict.write_text('approved')
            with patch.object(q,'check_verdict'),patch.object(q.legacy,'validate_run'),patch.object(q.legacy,'approve_run'):
                q.approve(path,'run-1',verdict)
            s=json.loads(path.read_text());self.assertEqual(s['approved_entries'],['run-1'])
            self.assertEqual(s['next_position'],2);self.assertEqual(s['runs'][0]['status'],'superseded')

    def test_failed_deep_validation_rolls_back_approval(self):
        with tempfile.TemporaryDirectory() as d,patch.object(q,'ROOT',Path(d)),patch.object(q.legacy,'ROOT',Path(d)):
            root=Path(d);s=state();item=complete(s);item['status']='pending_full_review'
            path=root/'state.json';write_json(path,s);before=path.read_bytes();verdict=root/'verdict.md';verdict.write_text('approved')
            with patch.object(q,'check_verdict'),patch.object(q.legacy,'validate_run',side_effect=ValueError('approval model refused')),patch.object(q.legacy,'approve_run') as approve:
                with self.assertRaises(ValueError):q.approve(path,'run-2',verdict)
                approve.assert_not_called()
            self.assertEqual(path.read_bytes(),before)


class SparseBoundaryTests(unittest.TestCase):
    setUp=test_ancestor_context.AncestorContextTests.setUp
    tearDown=test_ancestor_context.AncestorContextTests.tearDown
    run_fixture=test_ancestor_context.AncestorContextTests.run_fixture

    def packet_mode(self,packet):
        p=packet/'manifest.json';m=json.loads(p.read_text());m['ancestor_context_mode']='retrieval_v1';p.write_text(json.dumps(m))

    def test_sparse_context_omits_pending_but_keeps_full_git_source(self):
        run,source=self.run_fixture();approve_run(run,source,'reviewer','fixture')
        packet=self.root/'ahead';build_packet(self.repo,self.future,packet);self.packet_mode(packet)
        sparse_attach(packet,[run]);m=json.loads((packet/'manifest.json').read_text())
        self.assertIn(self.task,m['commits']);self.assertNotIn(self.task,m['approved_ancestor_selection'])
        with installed(),patch.object(q,'ROOT',self.root):
            self.assertEqual(q.verify_selection(packet,[str(run)]),[str(run)])
            session=FreshSession(packet);session.require_authoring_context()
            catalog=worker.dispatch(packet,'ancestor_read',{'mode':'catalog'})
            self.assertIn(self.first,json.dumps(catalog));self.assertNotIn(self.task,json.dumps(catalog))
            with self.assertRaises(ValueError):worker.dispatch(packet,'ancestor_read',{'mode':'content','commit':self.task})
            self.assertIn('text',worker.dispatch(packet,'git_show',{'commit':self.task}))
            if os.environ.get('EXDEV_SANDBOX_TESTS')=='1':
                isolated=runner.Runner(packet).invoke('ancestor_read',{'mode':'catalog'})
                self.assertEqual(isolated,{'ok':True,'result':catalog})
        # The original source ancestry is never narrowed on disk.
        self.assertEqual(json.loads((packet/'manifest.json').read_text())['commits'],m['commits'])

    def test_pending_entry_cannot_be_attached(self):
        run,source=self.run_fixture();self.packet_mode(self.packet)
        with self.assertRaises(ValueError):sparse_attach(self.packet,[run])

    def test_sparse_selection_order_and_duplicates_fail_closed(self):
        m=dict(history_order=['a','b'],commits={'a':{},'b':{}},ancestor_entries=[],approved_ancestor_selection=['a'])
        with self.assertRaises(ValueError):selected_manifest(m)
        m['ancestor_entries']=[{'sha':'a'}];selected_manifest(m)
        for selection in (['a','a'],['b','a'],['c']):
            with self.assertRaises(ValueError):selected_manifest(dict(m,approved_ancestor_selection=selection))

    def test_ordinary_packets_prompts_commands_and_provenance_identical(self):
        run,source=self.run_fixture();approve_run(run,source,'reviewer','fixture')
        a=self.root/'ordinary';b=self.root/'adapted'
        build_packet(self.repo,self.task,a);build_packet(self.repo,self.task,b)
        self.packet_mode(a);self.packet_mode(b)
        attach_entries(a,[run]);sparse_attach(b,[run])
        self.assertEqual((a/'manifest.json').read_bytes(),(b/'manifest.json').read_bytes())
        self.assertEqual({p.name:p.read_bytes() for p in (a/'blobs').iterdir()},
                         {p.name:p.read_bytes() for p in (b/'blobs').iterdir()})
        initial=FreshSession(a).initial;command=runner.command(a)
        def fail(*args,**kwargs):raise RuntimeError('before provider launch')
        with self.assertRaises(RuntimeError):author(a,self.root/'baseline',self.root/'auth',fail)
        with installed():
            self.assertEqual(FreshSession(a).initial,initial)
            self.assertEqual(runner.command(a),command)
            with self.assertRaises(RuntimeError):author(a,self.root/'with-adapter',self.root/'auth',fail)
        p1=json.loads((self.root/'baseline/provenance.json').read_text())
        p2=json.loads((self.root/'with-adapter/provenance.json').read_text())
        self.assertEqual(p1,p2)
        self.assertFalse(any(name.startswith('orchestration/') for name in p1['implementation_sha256']))
