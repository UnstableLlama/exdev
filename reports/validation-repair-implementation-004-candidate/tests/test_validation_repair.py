# SPDX-License-Identifier: MIT
from copy import deepcopy
from contextlib import nullcontext
import json
import unittest
from unittest.mock import Mock, patch
from teacher.author import author
from teacher.codex_adapter import CodexTeacher
from teacher.session import FreshSession
from teacher.validation_repair import repair_metadata, verify_final, disclosure, repair_feedback, POLICY, LEGACY_POLICY, KEEP_REST_SENTENCE, digest
from teacher.ancestor_context import approve_run
import test_codex_teacher as legacy
from test_codex_teacher import FakeTransport
from test_editorial import fixture


class RepairTransport(FakeTransport):
    def __init__(self, first=None, second=None, extra=None):
        super().__init__()
        self.events[1]['params']['item']['text']=first if first is not None else '{'
        second=second if second is not None else json.dumps(fixture())
        self.events += (extra or []) + [
            {'method':'item/completed','params':{'threadId':'fresh','turnId':'repair',
             'item':{'type':'agentMessage','phase':'final_answer','text':second}}},
            {'method':'turn/completed','params':{'threadId':'fresh',
             'turn':{'id':'repair','status':'completed'}}}]
        self.turns=0
    def request(self, method, params):
        result=super().request(method,params)
        if method=='turn/start':
            self.turns+=1
            result={'turn':{'id':'turn' if self.turns==1 else 'repair'}}
        return result


class ValidationRepairTests(unittest.TestCase):
    setUp=legacy.CodexTeacherTests.setUp
    tearDown=legacy.CodexTeacherTests.tearDown

    def run_teacher(self, transport=None, **kwargs):
        session=FreshSession(self.packet)
        session.runner.invoke=Mock(return_value={'ok':True,'result':{'text':'TEST FIXTURE ONLY'}})
        return CodexTeacher().run(session,transport or RepairTransport(),**kwargs)

    def test_feedback_exact_constant_and_provenance(self):
        self.assertEqual(KEEP_REST_SENTENCE, 'Correct only the issue named in the validator message and return the rest of the annotation unchanged.')
        message='annotation.x: wrong type\nverbatim detail'
        self.assertEqual(repair_feedback(message), message+'\n'+KEEP_REST_SENTENCE)
        result=self.run_teacher()
        transcript=result['transcript']
        event=next(m for m in transcript if m.get('role')=='validation')
        metadata=repair_metadata(transcript)
        self.assertEqual(metadata['validation_repair_policy'], POLICY)
        self.assertEqual(metadata['validation_repair_input_sha256'], digest(repair_feedback(event['error'])))

    def test_legacy_repaired_transcript_still_validates(self):
        transcript=self.run_teacher()['transcript']
        i=next(i for i,m in enumerate(transcript) if m.get('role')=='validation')
        transcript[i]['policy']=LEGACY_POLICY
        transcript[i+1]['content']=transcript[i]['error']
        metadata=repair_metadata(transcript)
        self.assertEqual(metadata['validation_repair_input_sha256'], digest(transcript[i]['error']))
        verify_final(fixture(), json.loads((self.packet/'manifest.json').read_text()), transcript, metadata)

    def test_legacy_unrepaired_transcript_still_validates(self):
        transcript=self.run_teacher(FakeTransport())['transcript']
        metadata=repair_metadata(transcript, LEGACY_POLICY)
        self.assertEqual(metadata['validation_repair_policy'], LEGACY_POLICY)
        self.assertEqual(disclosure(transcript, LEGACY_POLICY), metadata)
        verify_final(fixture(), json.loads((self.packet/'manifest.json').read_text()), transcript, metadata)

    def test_feedback_rejects_hints_and_cross_policy_text(self):
        original=self.run_teacher()['transcript']
        i=next(i for i,m in enumerate(original) if m.get('role')=='validation')
        for policy in (LEGACY_POLICY, POLICY):
            for text in (original[i]['error']+'\nextra hint', 'hint\n'+repair_feedback(original[i]['error'],policy),
                         repair_feedback(original[i]['error'], POLICY if policy==LEGACY_POLICY else LEGACY_POLICY)):
                transcript=deepcopy(original)
                transcript[i]['policy']=policy
                transcript[i+1]['content']=text
                with self.assertRaises(ValueError):
                    verify_final(fixture(), json.loads((self.packet/'manifest.json').read_text()), transcript, repair_metadata(transcript))

    def test_unknown_or_mismatched_policy_rejected(self):
        with self.assertRaises(ValueError): repair_feedback('error','unknown')
        transcript=self.run_teacher()['transcript']
        provenance=repair_metadata(transcript)
        provenance['validation_repair_policy']=LEGACY_POLICY
        with self.assertRaises(ValueError): verify_final(fixture(),json.loads((self.packet/'manifest.json').read_text()),transcript,provenance)
        transcript= self.run_teacher(FakeTransport())['transcript']
        with self.assertRaises(ValueError):
            verify_final(fixture(),json.loads((self.packet/'manifest.json').read_text()),transcript,{'validation_repair_policy':'unknown','validation_repair':False})

    def test_first_pass_opening_transcript_and_draft_unchanged(self):
        transport=FakeTransport();result=self.run_teacher(transport)
        initial=deepcopy(FreshSession(self.packet).initial)
        initial[0]['teacher_runtime']={'model':'gpt-6.1-sol','reasoning_effort':'medium'}
        expected=initial+[
            {'role':'assistant','calls':[{'id':'read-1','tool':'git_show','arguments':{'commit':'a'*40}}]},
            {'role':'tool','name':'git_show','call_id':'read-1','content':json.dumps({'ok':True,'result':{'text':'TEST FIXTURE ONLY'}})},
            {'role':'assistant','content':json.dumps(fixture())}]
        self.assertEqual(result['transcript'],expected)
        starts=[p for m,p in transport.requests if m=='turn/start']
        self.assertEqual(len(starts),1)
        self.assertEqual(starts[0]['input'],[{'type':'text','text':initial[1]['content']}])
        from teacher.editorial import assemble_draft
        m=json.loads((self.packet/'manifest.json').read_text())
        self.assertEqual(result['draft'],assemble_draft(fixture(),m,expected)[0])
        self.assertFalse(repair_metadata(expected)['validation_repair'])

    def test_one_verbatim_feedback_same_thread_and_complete_final(self):
        transport=RepairTransport(); result=self.run_teacher(transport)
        transcript=result['transcript'];event=next(x for x in transcript if x['role']=='validation')
        starts=[p for m,p in transport.requests if m=='turn/start']
        self.assertEqual(len(starts),2)
        self.assertEqual(starts[1]['threadId'],starts[0]['threadId'])
        self.assertEqual(starts[1]['input'],[{'type':'text','text':repair_feedback(event['error'])}])
        self.assertNotIn('ADMIN_REVIEW_SECRET',json.dumps(starts))
        self.assertEqual(transcript[event['refused_index']]['content'],'{')
        self.assertEqual(disclosure(transcript)['tool_calls_by_turn'],[1,0])
        m=json.loads((self.packet/'manifest.json').read_text())
        self.assertEqual(verify_final(fixture(),m,transcript,repair_metadata(transcript))[0],result['draft'])

    def test_invalid_annotation_and_more_tools_repair_with_prefix_validation(self):
        a=fixture();a['problem'][0]['evidence']=['read-2']
        extra=[{'id':101,'method':'item/tool/call','params':{'threadId':'fresh','turnId':'repair',
                'callId':'read-2','tool':'git_show','arguments':{'commit':'a'*40}}}]
        transport=RepairTransport(first=json.dumps(a),second=json.dumps(a),extra=extra)
        result=self.run_teacher(transport);t=result['transcript']
        self.assertEqual(disclosure(t)['tool_calls_by_turn'],[1,1])
        # The same annotation becomes valid only after the later read.
        m=json.loads((self.packet/'manifest.json').read_text())
        verify_final(a,m,t,repair_metadata(t))
        from teacher.editorial import assemble_draft
        assemble_draft(a,m,t)
        self.assertEqual(next(x for x in t if x['role']=='validation')['error'],'Unknown or unsuccessful evidence call')

    def test_second_refusal_is_terminal_and_preserved(self):
        saved=[];transport=RepairTransport(second='[')
        with self.assertRaises(ValueError):self.run_teacher(transport,record=saved.append)
        self.assertEqual(transport.turns,2)
        self.assertEqual(saved[-1][-1]['content'],'[')
        self.assertEqual(sum(x['role']=='validation' for x in saved[-1]),1)

    def test_protocol_budget_and_transport_failures_never_repair(self):
        for kind in ('foreign','failed','native','budget','internal'):
            transport=RepairTransport()
            if kind=='foreign':transport.events[0]['params']['threadId']='foreign'
            elif kind=='failed':transport.events[2]['params']['turn']['status']='failed'
            elif kind=='native':transport.events=[{'id':1,'method':'approval','params':{}}]
            elif kind=='internal':transport.receive=Mock(side_effect=RuntimeError('transport'))
            with self.assertRaises((ValueError,RuntimeError)):
                self.run_teacher(transport,max_calls=0 if kind=='budget' else 256)
            self.assertEqual(transport.turns,1)

    def test_duplicate_and_budget_span_turns(self):
        for identity,budget in [('read-1',256),('read-2',1)]:
            extra=[{'id':101,'method':'item/tool/call','params':{'threadId':'fresh','turnId':'repair',
                    'callId':identity,'tool':'git_show','arguments':{'commit':'a'*40}}}]
            with self.assertRaisesRegex(ValueError,'Duplicate tool call or tool budget'):
                self.run_teacher(RepairTransport(extra=extra),max_calls=budget)

    def test_tampering_rejected_by_shared_verifier(self):
        result=self.run_teacher();t=result['transcript'];m=json.loads((self.packet/'manifest.json').read_text())
        i=next(i for i,x in enumerate(t) if x['role']=='validation')
        mutations=[lambda x:x[i].update(error='hint'),lambda x:x[i+1].update(content='hint'),
            lambda x:x[i].update(refused_sha256='0'*64),lambda x:x[i].update(refused_index=0),
            lambda x:x[i].update(prefix_end=0),lambda x:x[i].update(repair_turn_id='turn'),
            lambda x:x[i].update(selected_final_index=i+1),lambda x:x.append(deepcopy(x[i])),
            lambda x:x[-1].update(turn_id='foreign')]
        for mutate in mutations:
            changed=deepcopy(t);mutate(changed)
            with self.assertRaises(ValueError):verify_final(fixture(),m,changed,repair_metadata(t))
        with self.assertRaises(ValueError):verify_final(fixture(),m,t,{})
        with self.assertRaises(ValueError):verify_final(fixture(),m,t,{**repair_metadata(t),'validation_repair':False})
        with self.assertRaises(ValueError):verify_final({},m,t,repair_metadata(t))

    def test_author_failure_and_approval_tamper(self):
        with patch('teacher.runner.Runner.invoke',return_value={'ok':True,'result':{'text':'TEST FIXTURE ONLY'}}):
            out=self.root/'repaired'
            author(self.packet,out,self.root/'unused',transport_factory=lambda _:nullcontext(RepairTransport()))
            provenance=json.loads((out/'provenance.json').read_text())
            self.assertTrue(provenance['validation_repair'])
            self.assertNotIn('reviewer_assisted',provenance)
            approved=approve_run(out,self.packet,'Fable','TEST repaired annotation')
            self.assertFalse(approved['canonical_approved']);self.assertFalse(approved['training_eligible'])
            bad=self.root/'failed-repair'
            with self.assertRaises(ValueError):
                author(self.packet,bad,self.root/'unused',transport_factory=lambda _:nullcontext(RepairTransport(second='[')))
            self.assertEqual(json.loads((bad/'status.json').read_text())['status'],'failed')
            self.assertTrue(json.loads((bad/'provenance.json').read_text())['validation_repair'])
            self.assertFalse((bad/'draft.json').exists())

    def test_repaired_turn_protocol_failures_and_disconnect_are_terminal(self):
        for kind in ('thread','turn','native','failed','missing','disconnect'):
            transport=RepairTransport()
            if kind=='thread':transport.events[3]['params']['threadId']='wrong'
            elif kind=='turn':transport.events[3]['params']['turnId']='wrong'
            elif kind=='native':transport.events[3]['params']['item']['type']='commandExecution'
            elif kind=='failed':transport.events[4]['params']['turn']['status']='failed'
            elif kind=='missing':del transport.events[3]
            else:
                original=transport.receive
                def receive():
                    if transport.turns==2:raise RuntimeError('disconnected')
                    return original()
                transport.receive=receive
            with self.assertRaises((ValueError,RuntimeError)):
                self.run_teacher(transport)
            self.assertEqual(transport.turns,2)

    def test_internal_integrity_errors_packet_changes_and_save_failures_never_feedback(self):
        for message in ('Duplicate evidence call ID','Unmatched evidence result',
                        'Read metadata does not match returned bytes',
                        'Assigned external evidence missing from packet: secret',
                        'Unsupported editorial schema version','unexpected internal failure'):
            transport=RepairTransport(first=json.dumps(fixture()))
            with patch('teacher.codex_adapter.assemble_draft',side_effect=ValueError(message)):
                with self.assertRaises(ValueError):self.run_teacher(transport)
            self.assertEqual(transport.turns,1)
        transport=RepairTransport()
        def record(t):
            if t[-1].get('content')=='{':
                p=self.packet/'manifest.json';p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaisesRegex(ValueError,'Packet changed'):
            self.run_teacher(transport,record=record)
        self.assertEqual(transport.turns,1)
        transport=RepairTransport()
        with self.assertRaisesRegex(OSError,'save failed'):
            self.run_teacher(transport,record=Mock(side_effect=OSError('save failed')))
        self.assertEqual(transport.turns,1)

    def test_failed_catalog_source_execution_and_coverage_gates_remain(self):
        from teacher.editorial import assemble_draft
        from teacher.validation_repair import eligible
        m=json.loads((self.packet/'manifest.json').read_text())
        t=self.run_teacher()['transcript']
        for change in ('unknown','execution','failed','catalog','coverage'):
            a=fixture();transcript=deepcopy(t);manifest=deepcopy(m)
            if change=='unknown':a['problem'][0]['evidence']=['absent']
            elif change=='execution':a['problem'][0]['basis']='execution'
            elif change=='coverage':
                manifest['authoring_task']={'kind':'chapter','id':'test','required_sections':[],
                    'required_evidence':[],'execution_required':True}
            else:
                for msg in transcript:
                    if msg.get('role')=='tool':
                        if change=='failed':msg['content']=json.dumps({'ok':False,'error':'failed'})
                        else:
                            msg['name']='evidence_index'
                            transcript[2]['calls'][0]['tool']='evidence_index'
            with self.assertRaises(ValueError) as caught:assemble_draft(a,manifest,transcript)
            self.assertTrue(eligible(caught.exception))

    def test_replay_includes_both_turns_and_failed_calls(self):
        from teacher.cycle import replay_result
        extra=[{'id':101,'method':'item/tool/call','params':{'threadId':'fresh','turnId':'repair',
            'callId':'read-2','tool':'git_show','arguments':{'commit':'b'*40}}}]
        session=FreshSession(self.packet)
        session.runner.invoke=Mock(side_effect=[{'ok':True,'result':{'text':'fixture'}},ValueError('bounded failure')])
        result=CodexTeacher().run(session,RepairTransport(extra=extra))
        transcript=result['transcript']
        calls={c['id']:c for m in transcript for c in m.get('calls',[])}
        runner=Mock();runner.invoke.side_effect=[{'ok':True,'result':{'text':'fixture'}},ValueError('bounded failure')]
        for m in transcript:
            if m['role']=='tool':replay_result(runner,calls[m['call_id']],m)
        self.assertEqual(runner.invoke.call_count,2)
        runner.invoke.side_effect=None;runner.invoke.return_value={'ok':False,'error':'different'}
        with self.assertRaisesRegex(ValueError,'Tool replay mismatch'):
            replay_result(runner,calls['read-2'],next(m for m in transcript if m.get('call_id')=='read-2'))

    def test_fabricated_refusal_and_render_tamper_refused(self):
        from teacher.validation_repair import digest
        t=self.run_teacher()['transcript'];m=json.loads((self.packet/'manifest.json').read_text())
        event=next(x for x in t if x['role']=='validation')
        t[event['refused_index']]['content']=json.dumps(fixture())
        event['refused_sha256']=digest(json.dumps(fixture()))
        with self.assertRaisesRegex(ValueError,'was valid'):
            verify_final(fixture(),m,t,repair_metadata(t))
        with patch('teacher.runner.Runner.invoke',return_value={'ok':True,'result':{'text':'fixture'}}):
            out=self.root/'render-tamper'
            author(self.packet,out,self.root/'unused',transport_factory=lambda _:nullcontext(RepairTransport()))
        (out/'draft.md').write_text('altered')
        with self.assertRaisesRegex(ValueError,'rendering mismatch'):
            approve_run(out,self.packet,'Fable','test')

    def test_large_integer_json_refusal_and_boolean_metadata(self):
        result=self.run_teacher(RepairTransport(first='1'*5000))
        event=next(m for m in result['transcript'] if m['role']=='validation')
        self.assertEqual(event['error_type'],'ValueError')
        self.assertIn('integer string conversion',event['error'])
        m=json.loads((self.packet/'manifest.json').read_text())
        metadata=repair_metadata(result['transcript']);metadata['validation_repair']=1
        with self.assertRaises(ValueError):
            verify_final(fixture(),m,result['transcript'],metadata)

    def test_explicit_legacy_rules_disable_feedback(self):
        transport=RepairTransport()
        with self.assertRaises(json.JSONDecodeError):
            self.run_teacher(transport,validation_repair=False)
        self.assertEqual(transport.turns,1)
        transcript=self.run_teacher()['transcript']
        manifest=json.loads((self.packet/'manifest.json').read_text())
        provenance={**repair_metadata(transcript),'validation_repair_enabled':False}
        with self.assertRaisesRegex(ValueError,'disabled'):
            verify_final(fixture(),manifest,transcript,provenance)
