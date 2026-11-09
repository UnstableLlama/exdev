# SPDX-License-Identifier: MIT
import json
import unittest
from unittest.mock import Mock
from teacher.codex_adapter import CodexTeacher, thread_parameters
from teacher.session import FreshSession
import test_teacher_packet
from test_editorial import fixture


class FakeTransport:
    cwd='/empty-test-workspace'
    def __init__(self, mode=None):
        self.mode=mode; self.requests=[]; self.replies=[]
        annotation=fixture()
        self.events=[{'id':100,'method':'item/tool/call','params':{'threadId':'fresh','turnId':'turn','callId':'read-1','tool':'git_show','arguments':{'commit':'a'*40}}},
            {'method':'item/completed','params':{'threadId':'fresh','turnId':'turn','item':{'type':'agentMessage','phase':'final_answer','text':json.dumps(annotation)}}},
            {'method':'turn/completed','params':{'threadId':'fresh','turn':{'id':'turn','status':'completed'}}}]
    def request(self, method, params):
        self.requests.append((method,params))
        if method=='thread/start':
            return {'thread':{'id':'fresh'},'model':'wrong' if self.mode=='model' else 'gpt-6-astra',
                    'reasoningEffort':'medium','instructionSources':['/bad/AGENTS.md'] if self.mode=='instructions' else []}
        if method=='turn/start':return {'turn':{'id':'turn'}}
        return {}
    def notify(self, method, params):pass
    def receive(self):return self.events.pop(0)
    def reply(self, identity, result):self.replies.append((identity,result))


class CodexTeacherTests(unittest.TestCase):
    setUp=test_teacher_packet.PacketTests.setUp
    tearDown=test_teacher_packet.PacketTests.tearDown

    def test_exact_model_and_fresh_context_with_dynamic_tools(self):
        session=FreshSession(self.packet);transport=FakeTransport()
        session.runner.invoke=Mock(return_value={'ok':True,'result':{'text':'TEST FIXTURE ONLY'}})
        result=CodexTeacher().run(session,transport)
        self.assertFalse(result['published'])
        self.assertEqual(result['review']['status'],'pending')
        start=transport.requests[1][1]
        self.assertEqual(start['model'],'gpt-6-astra')
        self.assertEqual(start['config']['model_reasoning_effort'],'medium')
        self.assertTrue(start['ephemeral']); self.assertFalse(start['allowProviderModelFallback'])
        self.assertEqual(start['environments'],[])
        self.assertEqual(len(start['dynamicTools']),9)
        self.assertFalse(any('resume' in method or 'fork' in method for method,_ in transport.requests))
        self.assertNotIn('ADMIN_SECRET',json.dumps(transport.requests))
        self.assertEqual(result['transcript'][-1]['role'],'assistant')
        with self.assertRaises(ValueError):CodexTeacher().run(session,transport)

    def test_model_fallback_or_inherited_instructions_abort(self):
        for mode in ['model','instructions']:
            with self.assertRaises(ValueError):CodexTeacher().run(FreshSession(self.packet),FakeTransport(mode))

    def test_unknown_tool_never_reaches_runner(self):
        session=FreshSession(self.packet);session.runner.invoke=Mock()
        transport=FakeTransport();transport.events[0]['params']['tool']='exec_command'
        with self.assertRaises(ValueError):CodexTeacher().run(session,transport)
        session.runner.invoke.assert_not_called()

    def test_foreign_thread_and_native_tool_events_abort(self):
        for event in [ {'id':100,'method':'item/tool/call','params':{'threadId':'old','turnId':'turn'}},
                       {'method':'item/started','params':{'threadId':'fresh','turnId':'turn','item':{'type':'commandExecution'}}}]:
            transport=FakeTransport();transport.events=[event]
            with self.assertRaises(ValueError):CodexTeacher().run(FreshSession(self.packet),transport)

    def test_failed_turn_cannot_publish_draft(self):
        transport=FakeTransport();transport.events=[{'method':'turn/completed','params':{'threadId':'fresh','turn':{'id':'turn','status':'failed'}}}]
        with self.assertRaises(ValueError):CodexTeacher().run(FreshSession(self.packet),transport)
