# SPDX-License-Identifier: MIT
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import test_teacher_packet
from teacher.root_evidence import recover_hf, MAX_HEADER_BYTES
from teacher.worker import dispatch, MAX_HEADER_BYTES as RUNTIME_MAX
from teacher.packet import build_packet
from teacher.runner import Runner


class HeaderRecoveryTests(unittest.TestCase):
    def recover(self, length, body):
        calls=[]
        def fetch(url, byte_range=None):
            calls.append(byte_range)
            return (length.to_bytes(8,'little') if byte_range==(0,7) else body), {}
        with tempfile.TemporaryDirectory() as tmp, patch('teacher.root_evidence.pages',side_effect=[
            iter([[{'id':'a'*40,'date':'2020-01-01T00:00:00Z'}]]),
            iter([[{'type':'file','path':'model.safetensors'}]])]), patch('teacher.root_evidence.fetch',side_effect=fetch):
            entries, report=recover_hf('Demo',Path(tmp),repo='org/demo',cutoff='2021-01-01T00:00:00Z',reference_only=True)
        return entries,report,calls

    def test_large_header_exact_ranges_and_upper_bound(self):
        self.assertEqual(MAX_HEADER_BYTES,RUNTIME_MAX)
        body=b'{}'+b' '*(MAX_HEADER_BYTES-2)
        entries,report,calls=self.recover(len(body),body)
        self.assertEqual(len(entries),1)
        self.assertEqual(report['failures'],[])
        self.assertEqual(calls,[(0,7),(8,7+len(body))])
        for size in (1,MAX_HEADER_BYTES+1):
            entries,report,calls=self.recover(size,b'')
            self.assertEqual(entries,[])
            self.assertEqual(calls,[(0,7)])
            self.assertEqual(len(report['failures']),1)

    def test_normalized_header_must_fit_runtime_budget(self):
        body=json.dumps({'__metadata__':{'x':'é'*3_000_000}},ensure_ascii=False).encode()
        self.assertLess(len(body),MAX_HEADER_BYTES)
        entries,report,_=self.recover(len(body),body)
        self.assertFalse(entries)
        self.assertIn('Normalized',report['failures'][0]['message'])


class LargeHeaderPacketTests(unittest.TestCase):
    setUp=test_teacher_packet.PacketTests.setUp
    tearDown=test_teacher_packet.PacketTests.tearDown

    def packet(self,body,name):
        cutoff=json.loads((self.packet/'manifest.json').read_text())['cutoff_date']
        item=dict(kind='safetensors_header',repo_id='org/model',revision='a'*40,path='model.safetensors',artifact_role='tensor_header',
                  url='https://huggingface.co/org/model/resolve/'+('a'*40)+'/model.safetensors',source_id='TEST',
                  created_at=cutoff,revision_at=cutoff,content=body,content_sha256=hashlib.sha256(body.encode()).hexdigest())
        target=self.root/name
        build_packet(self.repo,self.task,target,dict(task_sha=self.task,cutoff=cutoff,items=[item]))
        return target

    def test_large_header_paginates_and_over_budget_fails(self):
        body=json.dumps({f'w{i:06d}':dict(dtype='F16',shape=[1],data_offsets=[2*i,2*i+2]) for i in range(120000)})
        self.assertGreater(len(body),9_080_000)
        self.assertLess(len(body),MAX_HEADER_BYTES)
        packet=LargeHeaderPacketTests.packet(self,body,'large')
        args=dict(repo_id='org/model',revision='a'*40,path='model.safetensors',offset=119999,limit=1)
        result=dispatch(packet,'safetensors_header',args)
        self.assertEqual(list(result['header']),['w119999'])
        self.assertFalse(result['has_more'])
        if os.environ.get('EXDEV_SANDBOX_TESTS')=='1':
            actual=Runner(packet).invoke('safetensors_header',args)
            self.assertTrue(actual['ok'],actual)
            self.assertEqual(actual['result'],result)
        oversized=LargeHeaderPacketTests.packet(self,'{}'+' '*(MAX_HEADER_BYTES-1),'oversized')
        with self.assertRaisesRegex(ValueError,'runtime budget'):dispatch(oversized,'safetensors_header',args)
        if os.environ.get('EXDEV_SANDBOX_TESTS')=='1':
            self.assertFalse(Runner(oversized).invoke('safetensors_header',args)['ok'])
