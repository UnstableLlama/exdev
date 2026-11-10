# SPDX-License-Identifier: MIT
import json
import unittest
import test_editorial as fixtures
from teacher.editorial import validate_annotation, assemble_draft, render, output_schema


class FindingTests(unittest.TestCase):
    setUp = fixtures.EditorialTests.setUp

    def annotation(self):
        self.manifest['editorial_schema_version'] = 3
        a = fixtures.fixture(); a['schema_version'] = 3
        a['findings'] = [{
            'id': 'fixture-boundary', 'origin': 'authoring_observation', 'status': 'suspected',
            'classification': 'defect', 'description': 'TEST FIXTURE ONLY: boundary observation.',
            'trigger': 'Fixture zero input', 'expected_behavior': 'Fixture returns zero',
            'actual_behavior': 'Fixture raises',
            'locations': [{'commit': 'a'*40, 'path': 'fixture.py', 'symbol': 'fixture_function'}],
            'source_evidence': ['read-1'],
            'verification': [{'method': 'source_inspection', 'description': 'Inspected fixture branch',
                              'evidence': ['read-1'], 'limits': 'No implementation execution'}]}]
        return a

    def add_run(self, returncode=0, timed_out=False):
        self.transcript += [
            {'role':'assistant','calls':[{'id':'run-1','tool':'run','arguments':{'argv':['python3','-c','pass']}}]},
            {'role':'tool','call_id':'run-1','name':'run','content':json.dumps(
                {'ok':True,'result':{'returncode':returncode,'timed_out':timed_out}})}]

    def test_findings_are_rendered_with_source_and_verification_scope(self):
        a=self.annotation();entry,review=assemble_draft(a,self.manifest,self.transcript)
        self.assertEqual(entry['schema_version'],3)
        self.assertEqual(review['status'],'pending')
        for text in ('fixture-boundary','Source evidence: read-1','source_inspection','No implementation execution'):
            self.assertIn(text,render(entry))

    def test_missing_empty_failed_and_fabricated_evidence_rejected(self):
        for refs in ([],['invented'],['read-1','read-1']):
            a=self.annotation();a['findings'][0]['source_evidence']=refs
            with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)
        a=self.annotation();a['findings'][0]['verification']=[]
        with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)
        a=self.annotation();self.transcript[1]['content']=json.dumps({'ok':False})
        with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)

    def test_execution_modes_need_successful_run_and_separate_source(self):
        for method in ('scalar_transcription','repository_execution'):
            a=self.annotation();check=a['findings'][0]['verification'][0];check['method']=method
            with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)
        self.add_run();check['evidence']=['run-1']
        validate_annotation(a,self.manifest,self.transcript)
        a['findings'][0]['source_evidence']=['run-1']
        with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)
        a['findings'][0]['source_evidence']=['read-1']
        for result in ({'returncode':1},{'returncode':0,'timed_out':True}):
            self.transcript[-1]['content']=json.dumps({'ok':True,'result':result})
            with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)

    def test_future_locations_and_unsafe_paths_rejected(self):
        a=self.annotation();a['findings'][0]['locations'][0]['commit']='b'*40
        with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)
        for path in ('/host/file','../future.py','a/../b','a\\b'):
            a=self.annotation();a['findings'][0]['locations'][0]['path']=path
            with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)

    def test_teacher_cannot_confirm_or_retroactively_label(self):
        for field,value in (('status','confirmed'),('origin','fix_derived')):
            a=self.annotation();a['findings'][0][field]=value
            with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)
        a=self.annotation();a['findings']*=2
        with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)

    def test_version_is_trusted_packet_choice_and_old_drafts_still_work(self):
        a=self.annotation();self.manifest.pop('editorial_schema_version')
        with self.assertRaises(ValueError):validate_annotation(a,self.manifest,self.transcript)
        validate_annotation(fixtures.fixture(),self.manifest,self.transcript)
        self.manifest['editorial_schema_version']=3
        with self.assertRaises(ValueError):validate_annotation(fixtures.fixture(),self.manifest,self.transcript)
        self.manifest['editorial_schema_version']=6
        with self.assertRaises(ValueError):output_schema(self.manifest)
