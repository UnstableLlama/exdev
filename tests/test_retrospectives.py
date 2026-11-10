# SPDX-License-Identifier: MIT
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from copy import deepcopy
from ledger.retrospectives import append, eligible_revisions,validate


class RetrospectiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        (self.root/'evidence.txt').write_text('TEST SOURCE FIXTURE')
        self.record={k:[] for k in ('introductions','observations','verification','affected_revisions')}
        self.record.update(defect_id='fixture-defect',revision_id='r001',supersedes=None,origin='fix_derived',classification='defect',status='confirmed',
            description='fixture',trigger='fixture',expected_behavior='fixture',actual_behavior='fixture',
            fixes=[{'repository':'fixture','sha':'a'*40}],dependencies=[{'repository':'fixture','sha':'a'*40,'available_at':'2025-01-02T00:00:00+00:00'}],
            recorded_at='2026-11-10T00:00:00+00:00',reviewed_at='2026-11-10T00:00:00+00:00',reviewer='TEST REVIEWER',
            evidence=[{'file':'evidence.txt','sha256':hashlib.sha256((self.root/'evidence.txt').read_bytes()).hexdigest()}])

    def test_append_only_and_evidence_integrity(self):
        append(self.root,self.record)
        with self.assertRaises((ValueError,FileExistsError)):append(self.root,self.record)
        revision=deepcopy(self.record);revision.update(revision_id='r002',supersedes='r001',status='refuted')
        append(self.root,revision)
        self.assertEqual(json.loads((self.root/'fixture-defect--r001.json').read_text())['status'],'confirmed')
        revision.update(revision_id='r003',supersedes='r002');(self.root/'evidence.txt').write_text('Changed')
        with self.assertRaises(ValueError):append(self.root,revision)

    def test_full_closure_cutoff_branch_and_eligible_correction(self):
        a=self.record;b=deepcopy(a);b.update(revision_id='r002',supersedes='r001',status='refuted')
        b['dependencies'].append({'repository':'fixture','sha':'b'*40,'available_at':'2025-01-03T00:00:00+00:00'})
        allowed={('fixture','a'*40),('fixture','b'*40)}
        self.assertEqual(eligible_revisions([a,b],'2025-01-01T00:00:00+00:00',allowed),[])
        self.assertEqual(eligible_revisions([a,b],'2025-01-02T12:00:00+00:00',allowed),[a])
        self.assertEqual(eligible_revisions([a,b],'2025-01-04T00:00:00+00:00',{('fixture','a'*40)}),[a])
        self.assertEqual(eligible_revisions([a,b],'2025-01-04T00:00:00+00:00',allowed),[b])
        c=deepcopy(a);c['defect_id']='other-defect'
        self.assertEqual(len(eligible_revisions([a,b,c],'2025-01-04T00:00:00+00:00',allowed)),2)

    def test_fix_dependency_cannot_be_omitted(self):
        self.record['dependencies'][0]['sha']='c'*40
        with self.assertRaises(ValueError):validate(self.record)

    def test_external_dependency_requires_hash_allowlist_and_cutoff(self):
        dep={'url':'https://example.test/issues/2','source_id':'issue-edit','content_sha256':'b'*64,'available_at':'2025-01-03T00:00:00+00:00'}
        self.record['dependencies'].append(dep)
        allowed={('fixture','a'*40)}
        self.assertEqual(eligible_revisions([self.record],'2025-01-04T00:00:00+00:00',allowed),[])
        allowed.add((dep['url'],dep['content_sha256']))
        self.assertEqual(eligible_revisions([self.record],'2025-01-02T00:00:00+00:00',allowed),[])
        self.assertEqual(eligible_revisions([self.record],'2025-01-04T00:00:00+00:00',allowed),[self.record])
