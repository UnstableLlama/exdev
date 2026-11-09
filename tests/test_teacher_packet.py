# SPDX-License-Identifier: MIT
import tempfile
import subprocess
import unittest
from pathlib import Path
from teacher.packet import build_packet
from teacher.worker import dispatch

class PacketTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.repo=self.root/'repo';self.repo.mkdir()
        def git(*args):return subprocess.check_output(['git','-C',str(self.repo),*args],stderr=subprocess.DEVNULL).decode().strip()
        self.git=git;git('init','-b','main');git('config','user.name','Test');git('config','user.email','test@example.test')
        (self.repo/'a.py').write_text('value = 1\n');git('add','.');git('commit','-m','Root');self.first=git('rev-parse','HEAD')
        git('checkout','-b','side');(self.repo/'branch.txt').write_text('UNRELATED');git('add','.');git('commit','-m','Other branch');self.side=git('rev-parse','HEAD')
        git('checkout','main');(self.repo/'a.py').write_text('value = 2\n');git('commit','-am','Task');self.task=git('rev-parse','HEAD')
        (self.repo/'future.txt').write_text('FUTURE');git('add','.');git('commit','-m','Future');self.future=git('rev-parse','HEAD')
        (self.repo/'astra-review.md').write_text('ADMIN_SECRET')
        self.packet=self.root/'packet';build_packet(self.repo,self.task,self.packet)
    def tearDown(self):self.tmp.cleanup()

    def test_packet_excludes_future_sibling_and_admin_files(self):
        r=dispatch(self.packet,'repo_read',dict(commit=self.first,path='a.py'))
        self.assertEqual(r['text'],'value = 1\n')
        for commit in [self.task,self.future,self.side]:
            with self.assertRaises(ValueError):dispatch(self.packet,'repo_list',dict(commit=commit))
        for path in ['../astra-review.md','/etc/passwd','astra-review.md','.git/config']:
            with self.assertRaises(ValueError):dispatch(self.packet,'repo_read',dict(commit=self.first,path=path))
        contents=b''.join(p.read_bytes() for p in self.packet.rglob('*') if p.is_file())
        self.assertNotIn(b'ADMIN_SECRET',contents);self.assertNotIn(b'UNRELATED',contents);self.assertNotIn(b'FUTURE',contents)

    def test_task_diff_is_explicit_input_but_future_show_is_blocked(self):
        self.assertIn('+value = 2',dispatch(self.packet,'git_show',dict(commit=self.task))['text'])
        with self.assertRaises(ValueError):dispatch(self.packet,'git_show',dict(commit=self.future))

    def test_model_cannot_override_cutoff_or_request_unknown_source(self):
        with self.assertRaises(ValueError):dispatch(self.packet,'repo_list',dict(commit=self.first,cutoff=self.future))
        with self.assertRaises(ValueError):dispatch(self.packet,'web_fetch',dict(url='https://example.com/future'))

    def test_grep_and_log_are_bounded(self):
        r=dispatch(self.packet,'repo_grep',dict(commit=self.first,query='value',limit=1))
        self.assertEqual(len(r['matches']),1)
        self.assertEqual([x['sha'] for x in dispatch(self.packet,'git_log',{})['commits']],[self.first])

    def test_pinned_hf_file_and_header_are_cache_only(self):
        import json,hashlib
        cutoff=json.loads((self.packet/'manifest.json').read_text())['cutoff_date']
        def item(kind,path,content,role):
            return dict(kind=kind,repo_id='org/model',revision='a'*40,path=path,artifact_role=role,
                        url='https://huggingface.co/org/model/blob/'+('a'*40)+'/'+path,
                        source_id='TEST_FIXTURE',created_at=cutoff,revision_at=cutoff,
                        content=content,content_sha256=hashlib.sha256(content.encode()).hexdigest())
        header=json.dumps({'weight':{'dtype':'F16','shape':[2,2],'data_offsets':[0,8]}})
        evidence={'task_sha':self.task,'cutoff':cutoff,'items':[
            item('hf_file','config.json','{"test":true}','non_weight'),
            item('safetensors_header','model.safetensors',header,'tensor_header')]}
        packet=self.root/'with-evidence';build_packet(self.repo,self.task,packet,evidence)
        r=dispatch(packet,'hf_fetch',dict(repo_id='org/model',revision='a'*40,path='config.json'))
        self.assertEqual(r['text'],'{"test":true}')
        r=dispatch(packet,'safetensors_header',dict(repo_id='org/model',revision='a'*40,path='model.safetensors'))
        self.assertEqual(r['header']['weight']['shape'],[2,2])
        with self.assertRaises(ValueError):dispatch(packet,'hf_fetch',dict(repo_id='org/model',revision='main',path='config.json'))
        with self.assertRaises(ValueError):dispatch(packet,'hf_fetch',dict(repo_id='org/model',revision='a'*40,path='model.safetensors'))

    def test_future_evidence_prevents_packet_publication(self):
        import json,hashlib
        cutoff=json.loads((self.packet/'manifest.json').read_text())['cutoff_date']
        evidence={'task_sha':self.task,'cutoff':cutoff,'items':[dict(url='https://example.test',source_id='TEST',
                  created_at='2999-01-01T00:00:00Z',revision_at='2999-01-01T00:00:00Z',
                  content='FUTURE',content_sha256=hashlib.sha256(b'FUTURE').hexdigest())]}
        target=self.root/'invalid'
        with self.assertRaisesRegex(ValueError,'newer'):build_packet(self.repo,self.task,target,evidence)
        self.assertFalse((target/'manifest.json').exists())
