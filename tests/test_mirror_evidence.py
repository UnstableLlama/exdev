# SPDX-License-Identifier: MIT
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from teacher.mirror_evidence import (recover_modelscope, validate_selection, git_blob,
    digest, file_set_revision, SCHEME, NOTICE)


class MirrorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.cache=Path(self.tmp.name);self.calls=[]
        self.header=b'{"w":{"dtype":"F16","shape":[1],"data_offsets":[0,2]}}'
        self.data={'config.json':b'{"architectures":["Demo"]}', 'tokenizer_config.json':b'{}',
                   'model.safetensors':len(self.header).to_bytes(8,'little')+self.header+b'xx'}
        self.official=dict(id='official/demo',gated='auto',sha='a'*40,createdAt='2020-01-01T00:00:00Z',siblings=[])
        self.mirror=dict(Code=200,Data={'Files':[]})
        for name,data in self.data.items():
            row=dict(rfilename=name,size=len(data),blobId=git_blob(data))
            if name.endswith('.safetensors'):row['lfs']={'sha256':digest(data)}
            self.official['siblings'].append(row)
            self.mirror['Data']['Files'].append(dict(Type='blob',Path=name,Revision='b'*40,Sha256=digest(data),Size=len(data),CommittedDate=1577923200))
        # Weight payloads and executable files outside the reference allowlist are not fetched.
        self.official['siblings'] += [dict(rfilename='weights.bin'),dict(rfilename='model.py')]

    def fetch(self,url,byte_range=None,**kwargs):
        from urllib.parse import urlsplit,parse_qs
        self.calls.append((url,byte_range))
        if '?blobs=true' in url:return json.dumps(self.official).encode(),{}
        if '/repo/files?' in url:return json.dumps(self.mirror).encode(),{}
        query=parse_qs(urlsplit(url).query);self.assertEqual(query['Revision'],['b'*40])
        data=self.data[query['FilePath'][0]]
        if query['FilePath'][0].endswith('.safetensors'):self.assertIsNotNone(byte_range)
        if byte_range:data=data[byte_range[0]:byte_range[1]+1]
        return data,{}

    def recover(self):
        with patch('teacher.mirror_evidence.fetch',side_effect=self.fetch):
            return recover_modelscope('Demo',self.cache,repo='official/demo',mirror_repo='mirror/demo',historical_repo='old/demo',cutoff='2021-01-01T00:00:00Z')

    def test_identity_dates_file_set_and_header_only(self):
        entries,report=self.recover();self.assertEqual(len(entries),3)
        self.assertEqual(report['revision'],file_set_revision(entries));self.assertEqual(len(report['revision']),64)
        self.assertEqual(report['weight_payload_bytes_downloaded'],0)
        for e in entries:
            self.assertEqual(e['repo_id'],'official/demo');self.assertEqual(e['created_at'],self.official['createdAt'])
            self.assertEqual(e['mirror_provenance']['historical_repo'],'old/demo')
        self.assertEqual([r for u,r in self.calls if 'FilePath=model.safetensors' in u],[(0,7),(8,7+len(self.header))])
        self.assertFalse(any('weights.bin' in u or 'model.py' in u for u,_ in self.calls))
        self.assertEqual(entries[0]['mirror_provenance']['official_hash'],git_blob(self.data['config.json']))

    def test_fail_closed_for_mismatch_missing_and_future(self):
        for what in ['blob','weight','masked','date','creation','missing','bytes']:
            with self.subTest(what=what):
                self.setUp()
                if what=='blob':self.official['siblings'][0]['blobId']='0'*40
                if what=='weight':self.official['siblings'][2]['lfs']['sha256']='0'*64
                if what=='masked':self.official['siblings'][2]['lfs']['sha256']='*'*64
                if what=='date':self.mirror['Data']['Files'][0]['CommittedDate']=1893456000
                if what=='creation':self.official['createdAt']='2030-01-01T00:00:00Z'
                if what=='missing':self.mirror['Data']['Files'].pop(0)
                if what=='bytes':self.data['config.json']=b'altered'
                with self.assertRaises(ValueError):self.recover()

    def test_proofs_and_header_metadata_revalidated(self):
        entries,report=self.recover()
        for what in ['hash','date','url','revision','range','proof','missing']:
            with self.subTest(what=what):
                es=copy.deepcopy(entries);r=copy.deepcopy(report)
                if what=='hash':es[0]['mirror_provenance']['official_hash']='0'*40
                if what=='date':es[0]['mirror_provenance']['mirror_committed_at']='2030-01-01T00:00:00Z'
                if what=='url':es[0]['url']='https://modelscope.cn/mutable'
                if what=='revision':r['revision']='0'*64
                if what=='range':es[2]['mirror_provenance']['ranges']=[[0,999999]]
                if what=='proof':es[0].pop('mirror_provenance')
                if what=='missing':es.pop()
                with self.assertRaises(ValueError):validate_selection(r,es,'2021-01-01T00:00:00Z')

    def test_mirror_notice_in_bound_index(self):
        from teacher.evidence_index import build,validate
        entries,_=self.recover();packet=self.cache/'packet';(packet/'blobs').mkdir(parents=True)
        for e in entries:
            data=e.pop('content').encode();e['blob']=digest(data);e['content_bytes']=len(data)
            (packet/'blobs'/e['blob']).write_bytes(data)
        m=dict(task_sha='c'*40,cutoff_date='2021-01-01T00:00:00Z',commits={},evidence=entries,walk_input_contract={'version':8})
        build(packet,m,[]);validate(m,packet)
        row=m['evidence_index']['sources'][0]
        self.assertEqual(row['repo_id'],'official/demo');self.assertEqual(row['retrieval_note'],NOTICE)
        self.assertEqual(row['historical_repo'],'old/demo');self.assertEqual(row['architectures'],['Demo'])
        self.assertEqual(row['objects'][0]['mirror_provenance']['scheme'],SCHEME)
        row['retrieval_note']='altered'
        with self.assertRaises(ValueError):validate(m,packet)

    def test_architecture_bundle_enforces_mirror_proofs(self):
        from teacher.architecture_evidence import load_bundle
        entries,report=self.recover()
        report.update(reason='Official fixture',candidates_considered=['official/demo'])
        bundle=dict(task_sha='c'*40,cutoff='2021-01-01T00:00:00Z',
                    trigger={'architectures':['Demo'],'class_files':[]},items=entries,selections=[report])
        path=self.cache/'bundle.json'
        with patch('teacher.architecture_evidence.trigger',return_value=bundle['trigger']),patch('teacher.architecture_evidence.trigger_details',return_value={'unresolved_class_files':[]}),patch('teacher.architecture_evidence.git',return_value=b'2021-01-01T00:00:00Z'):
            path.write_text(json.dumps(bundle));load_bundle(self.cache,'c'*40,path)
            entries[0]['mirror_provenance']['mirror_hash']='0'*40
            path.write_text(json.dumps(bundle))
            with self.assertRaises(ValueError):load_bundle(self.cache,'c'*40,path)
