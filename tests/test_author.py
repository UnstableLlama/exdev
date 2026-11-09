# SPDX-License-Identifier: MIT
from contextlib import nullcontext
import json
import unittest
from unittest.mock import patch
from teacher.author import author
from test_codex_teacher import FakeTransport
import test_teacher_packet
import test_ancestor_context
from teacher.ancestor_context import approve_run, attach_entries


class AuthorTests(unittest.TestCase):
    def setUp(self):
        test_teacher_packet.PacketTests.setUp(self)
        run,source=test_ancestor_context.AncestorContextTests.run_fixture(self)
        approve_run(run,source,'TEST REVIEWER','TEST FIXTURE approval')
        attach_entries(self.packet,[run])
    tearDown=test_teacher_packet.PacketTests.tearDown

    def test_save_draft_with_provenance_and_separate_pending_review(self):
        out=self.root/'output'
        with patch('teacher.runner.Runner.invoke',return_value={'ok':True,'result':{'text':'TEST FIXTURE ONLY'}}):
            author(self.packet,out,self.root/'unused',transport_factory=lambda _:nullcontext(FakeTransport()))
        self.assertEqual(json.loads((out/'status.json').read_text())['status'],'draft')
        self.assertFalse(json.loads((out/'review.json').read_text())['training_eligible'])
        self.assertEqual(json.loads((out/'provenance.json').read_text())['model'],'gpt-6-astra')
        self.assertTrue((out/'raw-transcript.json').exists())
        with self.assertRaises(FileExistsError):author(self.packet,out,self.root/'unused')

    def test_invalid_raw_response_is_preserved_without_publishing_draft(self):
        out=self.root/'invalid';fake=FakeTransport()
        fake.events[1]['params']['item']['text']='INVALID TEST FIXTURE'
        with patch('teacher.runner.Runner.invoke',return_value={'ok':True,'result':{'text':'TEST FIXTURE ONLY'}}):
            with self.assertRaises(ValueError):
                author(self.packet,out,self.root/'unused',transport_factory=lambda _:nullcontext(fake))
        self.assertIn('INVALID TEST FIXTURE',(out/'raw-transcript.json').read_text())
        self.assertEqual(json.loads((out/'status.json').read_text())['status'],'failed')
        self.assertFalse((out/'draft.json').exists())
