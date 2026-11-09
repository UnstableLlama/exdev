# SPDX-License-Identifier: MIT
from copy import deepcopy
import hashlib
import json
import unittest
from teacher.ancestor_context import approve_run, attach_entries
from teacher.editorial import assemble_draft
from teacher.packet import build_packet
from teacher.session import FreshSession
import test_teacher_packet


class AncestorContextTests(unittest.TestCase):
    setUp=test_teacher_packet.PacketTests.setUp
    tearDown=test_teacher_packet.PacketTests.tearDown

    def run_fixture(self, sha=None):
        sha=sha or self.first
        packet=self.root/('source-'+sha)
        manifest=build_packet(self.repo,sha,packet)
        run=self.root/('run-'+sha);run.mkdir()
        claim={'text':'APPROVED TEST FIXTURE explanation','basis':'source','evidence':['read']}
        annotation={'schema_version':2,'type':'feature','problem':[claim],'reasoning':[],
                    'impact':[],'source_notes':[],'limitations':[],'links':[],'chapters':[]}
        transcript=[{'role':'assistant','calls':[{'id':'read','tool':'git_show','arguments':{'commit':sha}}]},
            {'role':'tool','name':'git_show','call_id':'read','content':json.dumps({'ok':True,'result':{'text':'TEST FIXTURE'}})}]
        draft,review=assemble_draft(annotation,manifest,transcript)
        provenance={'model':'gpt-6-astra','reasoning_effort':'medium','input_mode':'entry_analysis','published':False,
            'packet_manifest_sha256':hashlib.sha256((packet/'manifest.json').read_bytes()).hexdigest()}
        for name,value in [('draft',draft),('review',review),('provenance',provenance),('raw-transcript',transcript),('status',{'status':'draft','published':False})]:
            (run/(name+'.json')).write_text(json.dumps(value))
        return run,packet

    def test_approval_binds_exact_artifacts_and_exports_only_safe_projection(self):
        run,source=self.run_fixture()
        approve_run(run,source,'TEST REVIEWER','ADMIN_REVIEW_SECRET')
        attach_entries(self.packet,[run])
        session=FreshSession(self.packet)
        context=json.loads(session.initial[1]['content'])['ancestor_entries']
        self.assertEqual(context[0]['sha'],self.first)
        self.assertIn('APPROVED TEST FIXTURE',json.dumps(context))
        self.assertNotIn('ADMIN_REVIEW_SECRET',json.dumps(context))
        self.assertNotIn('TEST REVIEWER',json.dumps(context))
        packet_bytes=b''.join(p.read_bytes() for p in self.packet.rglob('*') if p.is_file())
        self.assertNotIn(b'ADMIN_REVIEW_SECRET',packet_bytes)
        self.assertNotIn('provenance',context[0])
        self.assertTrue(json.loads((self.packet/'manifest.json').read_text())['ancestor_context_complete'])

    def test_pending_or_tampered_drafts_are_rejected(self):
        run,source=self.run_fixture()
        with self.assertRaises(ValueError):attach_entries(self.packet,[run])
        approve_run(run,source,'reviewer','note')
        for filename in ('draft.json','raw-transcript.json','provenance.json'):
            path=run/filename;old=path.read_bytes();path.write_bytes(old+b' ')
            with self.assertRaises(ValueError):attach_entries(self.packet,[run])
            path.write_bytes(old)
        self.assertEqual(json.loads((self.packet/'manifest.json').read_text())['ancestor_entries'],[])

    def test_missing_duplicate_and_nonancestor_entries_fail_closed(self):
        run,source=self.run_fixture();approve_run(run,source,'reviewer','note')
        for supplied in ([],[run,run]):
            with self.assertRaises(ValueError):attach_entries(self.packet,supplied)
        sibling,source=self.run_fixture(self.side);approve_run(sibling,source,'reviewer','note')
        with self.assertRaises(ValueError):attach_entries(self.packet,[run,sibling])

    def test_approval_revalidates_transcript_and_identity(self):
        run,source=self.run_fixture()
        path=run/'draft.json';draft=json.loads(path.read_text());draft['sha']=self.future
        path.write_text(json.dumps(draft))
        with self.assertRaises(ValueError):approve_run(run,source,'reviewer','note')

    def test_root_needs_no_prior_prose_and_context_size_is_bounded(self):
        run,source=self.run_fixture()
        attach_entries(source,[])
        # Source manifest changed by attachment, so record the preparation fingerprint again.
        p=run/'provenance.json';v=json.loads(p.read_text());v['packet_manifest_sha256']=hashlib.sha256((source/'manifest.json').read_bytes()).hexdigest();p.write_text(json.dumps(v))
        approve_run(run,source,'reviewer','note')
        with self.assertRaises(ValueError):attach_entries(self.packet,[run],max_bytes=10)
        self.assertEqual(json.loads((self.packet/'manifest.json').read_text())['ancestor_entries'],[])

    def test_tampered_packet_context_blob_is_rejected_before_session(self):
        run,source=self.run_fixture();approve_run(run,source,'reviewer','note');attach_entries(self.packet,[run])
        manifest=json.loads((self.packet/'manifest.json').read_text())
        (self.packet/'blobs'/manifest['ancestor_entries'][0]['blob']).write_text('corrupt')
        with self.assertRaises(ValueError):FreshSession(self.packet)

    def test_approved_context_can_support_claim_but_not_execution(self):
        from teacher.editorial import validate_annotation
        run,source=self.run_fixture();approve_run(run,source,'reviewer','note');attach_entries(self.packet,[run])
        manifest=json.loads((self.packet/'manifest.json').read_text())
        annotation=json.loads((run/'draft.json').read_text())['annotation']
        annotation['problem'][0]['evidence']=['ancestor:'+self.first]
        ledger=validate_annotation(annotation,manifest,[])
        self.assertEqual(ledger['ancestor:'+self.first]['kind'],'approved_ancestor_context')
        annotation['problem'][0]['basis']='execution'
        with self.assertRaises(ValueError):validate_annotation(annotation,manifest,[])

    def test_author_rejects_incomplete_context_before_provider_launch(self):
        from unittest.mock import Mock
        from teacher.author import author
        transport=Mock()
        with self.assertRaises(ValueError):author(self.packet,self.root/'out',self.root/'unused',transport)
        transport.assert_not_called()
