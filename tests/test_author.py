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

    def test_coverage_request_is_verbatim_and_marks_provenance_and_review(self):
        import hashlib
        from teacher.coverage_request import attach
        from teacher.evidence_index import build
        from teacher.session import FreshSession
        m=json.loads((self.packet/'manifest.json').read_text())
        # Use the fixture's existing evidence as the directly attached bundle.
        from teacher.walk_inputs import signatures
        m['guidance_version']=3
        m['walk_input_contract']={'version':6,'reference_source_ids':[], 'reference_signatures':[],
            'bundle_present':False,'expected_evidence':signatures(m['evidence']),
            'discussion_truncated':False,'expected_discussions':[]}
        m['unreferenced_discussion_catalog']=[];m['unreferenced_discussion_truncated']=False
        build(self.packet,m,[])
        request=self.root/'commit-000002-002.coverage.md';request.write_text('1. Inspect the parent file and explain the changed caller.\n')
        sha=hashlib.sha256(request.read_bytes()).hexdigest();attach(m,request,sha)
        (self.packet/'manifest.json').write_text(json.dumps(m))
        session=FreshSession(self.packet)
        self.assertEqual(json.loads(session.initial[1]['content'])['reviewer_coverage_request'],request.read_text())
        self.assertIn("The reviewer_coverage_request field holds a reviewer's requests for coverage, not statements of fact.",session.initial[0]['content'])
        self.assertIn("read every model's config.json",session.initial[0]['content'])
        out=self.root/'commit-000002-002'
        with self.assertRaisesRegex(ValueError,'another attempt'):
            author(self.packet,self.root/'wrong-attempt',self.root/'unused')
        with patch('teacher.runner.Runner.invoke',return_value={'ok':True,'result':{'text':'TEST FIXTURE ONLY'}}):
            author(self.packet,out,self.root/'unused',transport_factory=lambda _:nullcontext(FakeTransport()))
        provenance=json.loads((out/'provenance.json').read_text());review=json.loads((out/'review.json').read_text())
        self.assertEqual(provenance['coverage_request'],{'path':str(request),'sha256':sha})
        self.assertTrue(provenance['reviewer_assisted']);self.assertTrue(review['reviewer_assisted'])
