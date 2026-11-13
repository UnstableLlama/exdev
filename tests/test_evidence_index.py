# SPDX-License-Identifier: MIT
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from teacher.evidence_index import build,validate
from teacher.coverage_request import attach,validate as validate_coverage
from teacher.worker import dispatch,evidence_index_page
from teacher.session import FreshSession


class EvidenceIndexTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.sha='a'*40;self.task='b'*40
        self.packet=self.root/'task';self.packet.mkdir();(self.packet/'blobs').mkdir()
        self.m={'task_sha':self.task,'task_parents':[self.sha],'base_commit':self.sha,'cutoff_date':'2025-02-01T00:00:00Z','commits':{self.sha:{}},'evidence':[], 'walk_input_contract':{'version':6},'guidance_version':3}
    def tearDown(self):self.temp.cleanup()
    def source(self,name,sha=None,date='2025-01-01T00:00:00Z',count=1):
        p=self.root/name;p.mkdir();(p/'blobs').mkdir();items=[]
        for n in range(count):
            raw=json.dumps({'n':n}).encode();h=hashlib.sha256(raw).hexdigest();(p/'blobs'/h).write_bytes(raw)
            items.append({'kind':'hf_file','artifact_role':'non_weight','repo_id':'org/'+str(n),'revision':'c'*40,'path':'config.json','source_id':str(n),'created_at':date,'revision_at':date,'content_sha256':h,'blob':h})
        (p/'manifest.json').write_text(json.dumps({'task_sha':sha or self.sha,'evidence':items}))
        return p
    def save(self): (self.packet/'manifest.json').write_text(json.dumps(self.m))
    def test_ancestor_only_cutoff_and_fetch(self):
        yes=self.source('yes');no=self.source('no',sha='d'*40);future=self.source('future',date='2025-03-01T00:00:00Z')
        build(self.packet,self.m,[yes,no,future]);validate(self.m,self.packet);self.save()
        rows=self.m['evidence_index']['sources'];self.assertEqual(len(rows),1);self.assertEqual(rows[0]['attached_by'],[self.sha])
        result=dispatch(self.packet,'hf_fetch',{'repo_id':'org/0','revision':'c'*40,'path':'config.json'})
        self.assertEqual(json.loads(result['text']),{'n':0})
        self.assertNotIn('objects',json.loads(evidence_index_page(self.m,{'max_bytes':8192})['text'])[0])
    def test_paging_reaches_all_sources_and_objects(self):
        build(self.packet,self.m,[self.source('many',count=60)])
        chunks=[];offset=0
        while True:
            page=evidence_index_page(self.m,{'offset':offset,'max_bytes':512});chunks.append(page['text']);self.assertLessEqual(len(page['text'].encode()),512)
            if not page['truncated']:break
            offset=page['next_offset']
        rows=json.loads(''.join(chunks));self.assertEqual(len(rows),60)
        obj=json.loads(evidence_index_page(self.m,{'index_id':rows[0]['index_id']})['text']);self.assertEqual(obj[0]['path'],'config.json')
    def test_mutation_and_missing_blob_fail(self):
        build(self.packet,self.m,[self.source('yes')]);original=json.loads(json.dumps(self.m))
        self.m['evidence_index']['sources'][0]['counts']['configuration_files']=99
        with self.assertRaisesRegex(ValueError,'index'):validate(self.m)
        self.m=original;obj=self.m['evidence_index']['sources'][0]['objects'][0];(self.packet/'blobs'/obj['blob']).unlink()
        with self.assertRaises(FileNotFoundError):validate(self.m,self.packet)
    def test_current_evidence_compact_and_deduplicated(self):
        source=self.source('current');old=json.loads((source/'manifest.json').read_text());self.m['evidence']=old['evidence']
        for b in (source/'blobs').iterdir():(self.packet/'blobs'/b.name).write_bytes(b.read_bytes())
        build(self.packet,self.m,[source]);row=self.m['evidence_index']['sources'][0]
        self.assertEqual(row['counts']['configuration_files'],1);self.assertEqual(set(row['attached_by']),{self.sha,self.task})
    def test_coverage_hash_scope_and_verbatim(self):
        p=self.root/'commit-000045-002.coverage.md';p.write_text('1. Inspect the parent loader and report what it reads.\n')
        h=hashlib.sha256(p.read_bytes()).hexdigest();attach(self.m,p,h);validate_coverage(self.m)
        self.assertEqual(self.m['coverage_request']['text'],p.read_text())
        self.m['coverage_request']['text']+='changed'
        with self.assertRaises(ValueError):validate_coverage(self.m)
        with self.assertRaises(ValueError):attach(self.m,p,'wrong')
        verdict=self.root/'commit-000045-002.md';verdict.write_text('conclusions')
        with self.assertRaises(ValueError):attach(self.m,verdict,hashlib.sha256(verdict.read_bytes()).hexdigest())
        p.write_text('Inspect '+ 'd'*40)
        with self.assertRaisesRegex(ValueError,'non-ancestor'):attach(self.m,p,hashlib.sha256(p.read_bytes()).hexdigest())

    def test_indexed_web_and_header_fetch_and_title_cutoff(self):
        p=self.source('mixed');m=json.loads((p/'manifest.json').read_text());m['evidence']=[]
        url='https://github.com/o/r/pull/3'
        for kind,raw,extra in [('web',b'eligible body',{'url':url}),('safetensors_header',b'{"w":{"dtype":"F16","shape":[1],"data_offsets":[0,2]}}',{'repo_id':'org/model','revision':'c'*40,'path':'model.safetensors','artifact_role':'tensor_header'})]:
            h=hashlib.sha256(raw).hexdigest();(p/'blobs'/h).write_bytes(raw)
            m['evidence'].append(dict(kind=kind,source_id=kind,created_at='2025-01-01T00:00:00Z',revision_at='2025-01-01T00:00:00Z',blob=h,content_sha256=h,**extra))
        (p/'manifest.json').write_text(json.dumps(m))
        history={'url':url,'timeline_complete':True,'title':'FUTURE TITLE','title_events':[{'createdAt':'2025-03-01T00:00:00Z','previousTitle':'Eligible title'}]}
        (self.root/'discussion-pull_request-3-history.json').write_text(json.dumps(history))
        build(self.packet,self.m,[p],self.root);self.save()
        self.assertNotIn('FUTURE TITLE',json.dumps(self.m['evidence_index']))
        self.assertIn('Eligible title',json.dumps(self.m['evidence_index']))
        self.assertEqual(dispatch(self.packet,'web_fetch',{'url':url,'source_id':'web'})['text'],'eligible body')
        result=dispatch(self.packet,'safetensors_header',{'repo_id':'org/model','revision':'c'*40,'path':'model.safetensors'})
        self.assertEqual(result['header']['w']['shape'],[1])

    def test_root_web_documents_are_not_discussion_objects(self):
        p=self.source('paper');m=json.loads((p/'manifest.json').read_text())
        obj=m['evidence'][0];obj.update(kind='web',url='https://arxiv.org/html/example')
        (p/'manifest.json').write_text(json.dumps(m))
        build(self.packet,self.m,[p])
        self.assertEqual(self.m['evidence_index']['sources'][0]['counts'],{'documents':1})

    def test_architectures_copied_from_pinned_config_and_bound_v7(self):
        p=self.source('architecture');old=json.loads((p/'manifest.json').read_text());obj=old['evidence'][0]
        raw=b'{"architectures":["ExampleModel","OtherModel"]}';h=hashlib.sha256(raw).hexdigest()
        (p/'blobs'/h).write_bytes(raw);obj.update(blob=h,content_sha256=h);(p/'manifest.json').write_text(json.dumps(old))
        self.m['walk_input_contract']['version']=7;build(self.packet,self.m,[p]);validate(self.m,self.packet)
        row=self.m['evidence_index']['sources'][0];self.assertEqual(row['architectures'],['ExampleModel','OtherModel'])
        row['architectures']=['WrongModel']
        with self.assertRaisesRegex(ValueError,'index'):validate(self.m,self.packet)
        from teacher.evidence_index import digest
        self.m['walk_input_contract']['evidence_index_sha256']=digest(self.m['evidence_index'])
        with self.assertRaisesRegex(ValueError,'pinned config'):validate(self.m,self.packet)

    def test_architectures_missing_key_empty_and_legacy_unchanged(self):
        p=self.source('no-architecture');build(self.packet,self.m,[p])
        self.assertNotIn('architectures',self.m['evidence_index']['sources'][0])
        self.m['walk_input_contract']['version']=7;build(self.packet,self.m,[p])
        self.assertEqual(self.m['evidence_index']['sources'][0]['architectures'],[])
        validate(self.m,self.packet)
