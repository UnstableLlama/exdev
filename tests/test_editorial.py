# SPDX-License-Identifier: MIT
import copy
import json
import unittest
from teacher.editorial import validate_annotation, assemble_draft, render


def fixture():
    claim={'text':'TEST FIXTURE ONLY: inspected change.', 'basis':'source', 'evidence':['read-1']}
    return {'schema_version':2,'type':'feature','problem':[claim], 'reasoning':[],
            'impact':[], 'source_notes':[], 'limitations':['TEST FIXTURE: performance not measured.'],
            'links':[], 'chapters':[]}


class EditorialTests(unittest.TestCase):
    def setUp(self):
        self.manifest={'task_sha':'a'*40,'task_parents':[], 'cutoff_date':'2025-01-01T00:00:00Z',
                       'commits':{}, 'ancestor_entries':[]}
        self.transcript=[{'role':'assistant','calls':[{'id':'read-1','tool':'git_show','arguments':{'commit':'a'*40}}]},
                         {'role':'tool','call_id':'read-1','name':'git_show','content':json.dumps({'ok':True,'result':{'text':'fixture'}})}]

    def test_source_and_inference_are_distinct(self):
        annotation=fixture()
        annotation['reasoning']=[{'text':'TEST inference','basis':'inference','evidence':['read-1']}]
        validate_annotation(annotation,self.manifest,self.transcript)
        entry,review=assemble_draft(annotation,self.manifest,self.transcript)
        self.assertEqual(review['status'],'pending')
        self.assertFalse(review['training_eligible'])
        self.assertNotIn('review_log',entry)
        self.assertIn('inference',render(entry))

    def test_execution_requires_successful_run_evidence(self):
        annotation=fixture();annotation['problem'][0]['basis']='execution'
        with self.assertRaises(ValueError):validate_annotation(annotation,self.manifest,self.transcript)
        self.transcript[0]['calls'][0]['tool']='run'; self.transcript[1].update(name='run',content=json.dumps({'ok':True,'result':{'returncode':0,'timed_out':False}}))
        validate_annotation(annotation,self.manifest,self.transcript)
        self.transcript[1]['content']=json.dumps({'ok':True,'result':{'returncode':1}})
        with self.assertRaises(ValueError):validate_annotation(annotation,self.manifest,self.transcript)

    def test_fabricated_evidence_and_protected_fields_fail(self):
        for field in ['sha','reviewed','training_eligible','merge_policy','review_log']:
            annotation=fixture();annotation[field]=True
            with self.assertRaises(ValueError):validate_annotation(annotation,self.manifest,self.transcript)
        annotation=fixture();annotation['problem'][0]['evidence']=['invented']
        with self.assertRaises(ValueError):validate_annotation(annotation,self.manifest,self.transcript)

    def test_links_require_approved_ancestor_prose(self):
        annotation=fixture();annotation['links']=['b'*40]
        self.manifest['commits']['b'*40]={}
        with self.assertRaises(ValueError):validate_annotation(annotation,self.manifest,self.transcript)
        self.manifest['ancestor_entries']=[{'sha':'b'*40}]
        validate_annotation(annotation,self.manifest,self.transcript)

    def test_canonical_root_can_have_chapters_and_unique_ids(self):
        annotation=fixture();annotation['chapters']=[{'id':'loading','title':'Loading','claims':annotation['problem']}]
        validate_annotation(annotation,self.manifest,self.transcript)
        annotation['chapters']*=2
        with self.assertRaises(ValueError):validate_annotation(annotation,self.manifest,self.transcript)

    def test_schema_rejects_wrong_types_and_empty_claims(self):
        for bad in [dict(fixture(),schema_version=True),dict(fixture(),limitations='text')]:
            with self.assertRaises(ValueError):validate_annotation(bad,self.manifest,self.transcript)
        bad=fixture();bad['problem'][0]['text']=''
        with self.assertRaises(ValueError):validate_annotation(bad,self.manifest,self.transcript)

    def test_provider_schema_constrains_links_to_supplied_ancestors(self):
        from teacher.editorial import output_schema
        self.assertEqual(output_schema(self.manifest)['properties']['links']['maxItems'],0)
        self.manifest['commits']['b'*40]={}
        self.manifest['ancestor_entries']=[{'sha':'b'*40}]
        self.assertEqual(output_schema(self.manifest)['properties']['links']['items']['enum'],['b'*40])

    def test_chapter_references_are_catalog_bound_and_render_when_assembled(self):
        self.manifest['authoring_task']={'kind':'chapter','id':'quantizer','required_sections':[],
            'required_evidence':[],'chapter_catalog':[{'id':'quantizer'},{'id':'gemm'}]}
        annotation=fixture();annotation['chapters']=[{'id':'quantizer','title':'Quantizer',
            'claims':annotation['problem'],'related_chapters':['gemm']}]
        entry,_=assemble_draft(annotation,self.manifest,self.transcript)
        self.assertIn('assembly link pending',render(entry))
        entry['annotation']['chapters'].append({'id':'gemm','title':'GEMM','claims':[],'related_chapters':[]})
        self.assertIn('[GEMM](#gemm)',render(entry))
        annotation['chapters'][0]['related_chapters']=['future']
        with self.assertRaises(ValueError):validate_annotation(annotation,self.manifest,self.transcript)
        annotation['chapters'][0]['related_chapters']=['gemm','gemm']
        with self.assertRaises(ValueError):validate_annotation(annotation,self.manifest,self.transcript)
        annotation['chapters'][0]['related_chapters']=['quantizer']
        with self.assertRaises(ValueError):validate_annotation(annotation,self.manifest,self.transcript)
