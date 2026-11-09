# SPDX-License-Identifier: MIT
import unittest
from unittest.mock import patch
from teacher.session import FreshSession
import test_teacher_packet


class FreshSessionTests(unittest.TestCase):
    setUp=test_teacher_packet.PacketTests.setUp
    tearDown=test_teacher_packet.PacketTests.tearDown

    def test_only_nine_tools_and_no_previous_conversation(self):
        for _ in range(2):
            session=FreshSession(self.packet)
            def model(messages,tools):
                self.assertEqual(len(messages),2)
                self.assertEqual({t['name'] for t in tools},{'repo_read','repo_list','repo_grep','git_show','git_log','hf_fetch','safetensors_header','web_fetch','run'})
                self.assertNotIn('ADMIN_SECRET',str(messages))
                self.assertNotIn(self.future,str(messages))
                return {'text':'TEST FIXTURE ONLY'}
            self.assertFalse(session.run(model)['published'])
            with self.assertRaisesRegex(ValueError,'reused'):session.run(model)

    def test_unapproved_model_tool_is_rejected_before_launch(self):
        session=FreshSession(self.packet);step=0
        def model(messages,tools):
            nonlocal step
            step+=1
            if step==1:return {'calls':[{'id':'test','tool':'exec_command','arguments':{'cmd':'cat /etc/passwd'}}]}
            self.assertIn('Unknown tool',messages[-1]['content'])
            return {'text':'TEST FIXTURE ONLY'}
        with patch('teacher.runner.subprocess.Popen') as process:
            session.run(model)
            process.assert_not_called()
