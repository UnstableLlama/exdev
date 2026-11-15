import copy
import json
from unittest.mock import patch
from urllib.parse import urlsplit,parse_qs
import unittest
from tests import test_mirror_evidence
from teacher.mirror_evidence import recover_modelscope,validate_selection,digest,git_blob,HISTORICAL,HISTORICAL_NOTICE


class HistoricalMirrorTests(unittest.TestCase):
    setUp = test_mirror_evidence.MirrorTests.setUp
    def setup_historical(self):
        self.setUp()
        self.old=copy.deepcopy(self.mirror)
        self.later=b'{"architectures":["Demo"],"changed":true}'
        self.official['siblings'][0].update(blobId=git_blob(self.later),size=len(self.later))
        self.mirror['Data']['Files'][0].update(Revision='d'*40,CommittedDate=1640995200,Sha256=digest(self.later),Size=len(self.later))
        self.second=copy.deepcopy(self.old)
        self.copies=[dict(repo='mirror/demo',revision='b'*40),dict(repo='second/demo',revision='c'*40)]
    def historical_fetch(self,url,byte_range=None,**kwargs):
        q=parse_qs(urlsplit(url).query)
        if '?blobs=true' in url:return json.dumps(self.official).encode(),{}
        if '/repo/files?' in url:
            obj=self.mirror if q['Revision']==['master'] else self.second if 'second/demo' in url else self.old
            return json.dumps(obj).encode(),{}
        if q['Revision']==['d'*40]:return self.later,{}
        data=self.data[q['FilePath'][0]]
        if q['FilePath'][0].endswith('.safetensors'):self.assertIsNotNone(byte_range)
        if byte_range:data=data[byte_range[0]:byte_range[1]+1]
        return data,{}
    def historical(self):
        with patch('teacher.mirror_evidence.fetch',side_effect=self.historical_fetch),patch('teacher.historical_mirror.fetch',side_effect=self.historical_fetch):
            return recover_modelscope('Demo',self.cache,repo='official/demo',mirror_repo='mirror/demo',historical_repo='old/demo',cutoff='2021-01-01T00:00:00Z',historical_copies=self.copies)
    def test_historical_status_and_separation(self):
        self.setup_historical();es,r=self.historical()
        self.assertEqual(r['status'],HISTORICAL)
        p=es[0]['mirror_provenance'];self.assertEqual(p['notice'],HISTORICAL_NOTICE)
        self.assertNotIn(git_blob(self.later),json.dumps(es));self.assertNotIn('2022-',json.dumps(es))
        self.assertIn(git_blob(self.later),json.dumps(r))
        for mutation in ['duplicate','future','changed','companion','status','leak','weight']:
            a=copy.deepcopy(es);b=copy.deepcopy(r)
            if mutation=='duplicate':b['historical_identity']['witnesses'][1]['repo']='mirror/demo'
            if mutation=='future':b['historical_identity']['witnesses'][1]['committed_at']='2023-01-01T00:00:00Z'
            if mutation=='changed':b['historical_identity']['shared_blob_id']='0'*40
            if mutation=='companion':a.pop()
            if mutation=='status':b['status']='complete'
            if mutation=='leak':a[0]['mirror_provenance']['later_date']='2022-01-01'
            if mutation=='weight':a[0]['kind']='safetensors_header'
            with self.subTest(mutation=mutation),self.assertRaises((ValueError,KeyError)):
                validate_selection(b,a,'2021-01-01T00:00:00Z')
    def test_recovery_requires_all_conditions(self):
        for mutation in ['duplicate','future','different','later','weight','companion']:
            self.setup_historical()
            if mutation=='duplicate':self.copies[1]['repo']='mirror/demo'
            if mutation=='future':self.second['Data']['Files'][0]['CommittedDate']=1893456000
            if mutation=='different':self.second['Data']['Files'][0]['Sha256']='0'*64
            if mutation=='later':self.mirror['Data']['Files'][0]['CommittedDate']=1577923200
            if mutation=='weight':self.official['siblings'][2]['lfs']['sha256']='0'*64
            if mutation=='companion':self.old['Data']['Files'].pop(1)
            with self.subTest(mutation=mutation),self.assertRaises((ValueError,KeyError)):
                self.historical()
    def test_index_labels_exception_without_administrative_proof(self):
        from teacher.evidence_index import build,validate
        self.setup_historical();es,r=self.historical()
        packet=self.cache/'packet';(packet/'blobs').mkdir(parents=True)
        for e in es:
            data=e.pop('content').encode();e.update(blob=digest(data),content_bytes=len(data));(packet/'blobs'/e['blob']).write_bytes(data)
        m=dict(task_sha='f'*40,cutoff_date='2021-01-01T00:00:00Z',commits={},evidence=es,walk_input_contract={'version':8})
        build(packet,m,[]);validate(m,packet)
        row=m['evidence_index']['sources'][0]
        self.assertEqual(row['retrieval_note'],HISTORICAL_NOTICE)
        self.assertEqual(row['historical_identity_files'],['config.json'])
        self.assertNotIn(git_blob(self.later),json.dumps(m));self.assertNotIn('2022-',json.dumps(m))
        row['retrieval_note']='verified'
        with self.assertRaises(ValueError):validate(m,packet)
