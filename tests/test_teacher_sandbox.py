# SPDX-License-Identifier: MIT
import json
import os
import unittest
from pathlib import Path
from teacher.runner import Runner
import test_teacher_packet


@unittest.skipUnless(os.environ.get('EXDEV_SANDBOX_TESTS')=='1', 'Host namespace tests require EXDEV_SANDBOX_TESTS=1')
class SandboxTests(unittest.TestCase):
    setUp = test_teacher_packet.PacketTests.setUp
    tearDown = test_teacher_packet.PacketTests.tearDown

    def execute(self, code, **kwargs):
        return Runner(self.packet).invoke('run', {'argv':['python3','-c',code], **kwargs})

    def test_worker_reads_only_exported_history(self):
        r=Runner(self.packet).invoke('repo_read',{'commit':self.first,'path':'a.py'})
        self.assertTrue(r['ok'],r)
        self.assertEqual(r['result']['text'],'value = 1\n')
        r=Runner(self.packet).invoke('repo_list',{'commit':self.future})
        self.assertFalse(r['ok'])

    def test_host_repo_review_credentials_and_environment_are_hidden(self):
        secret=self.root/'secret.txt';secret.write_text('PRIVATE_CANARY')
        paths=[str(secret),str(Path('/home/unstable/git/exdev/astra-review.md')),
               '/home/unstable/.config/gh/hosts.yml','/home/unstable/git/exdev/reports','/etc/passwd']
        code='import os,json; print(json.dumps({"visible": [p for p in '+repr(paths)+' if os.path.exists(p)], "token":os.environ.get("EXDEV_CANARY")}))'
        old=os.environ.get('EXDEV_CANARY');os.environ['EXDEV_CANARY']='SECRET_ENV'
        try:r=self.execute(code)
        finally:
            if old is None:os.environ.pop('EXDEV_CANARY',None)
            else:os.environ['EXDEV_CANARY']=old
        self.assertTrue(r['ok'],r)
        self.assertEqual(json.loads(r['result']['stdout']),{'visible':[],'token':None})

    def test_network_unavailable_and_packet_readonly(self):
        code='''import socket,json
out={}
s=socket.socket();s.settimeout(1)
try:s.connect(("1.1.1.1",443));out["network"]=True
except OSError:out["network"]=False
try:open("/packet/manifest.json","w").write("bad");out["writable"]=True
except OSError:out["writable"]=False
print(json.dumps(out))'''
        r=self.execute(code);self.assertTrue(r['ok'],r)
        self.assertEqual(json.loads(r['result']['stdout']),{'network':False,'writable':False})

    def test_scratch_changes_do_not_persist(self):
        r=self.execute('print(open("a.py").read())',files={'a.py':'changed'})
        self.assertEqual(r['result']['stdout'],'changed\n')
        r=self.execute('print(open("a.py").read())')
        self.assertEqual(r['result']['stdout'],'value = 1\n\n')
        self.assertEqual((self.repo/'a.py').read_text(),'value = 2\n')

    def test_timeout_and_path_escape_are_rejected(self):
        r=self.execute('import time; time.sleep(5)',timeout_seconds=1)
        self.assertTrue(r['result']['timed_out'])
        r=self.execute('pass',files={'../../escape':'no'})
        self.assertFalse(r['ok'])

    def test_run_cannot_fork(self):
        r=self.execute('import os\ntry:\n os.fork(); print("FORKED")\nexcept PermissionError:\n print("DENIED")')
        self.assertTrue(r['ok'],r)
        self.assertEqual(r['result']['stdout'],'DENIED\n')

    def test_proc_root_alias_does_not_expose_host_file(self):
        secret=self.root/'host-canary';secret.write_text('HOST_SECRET')
        code='import os,json; print(json.dumps([os.path.exists(p) for p in '+repr(['/proc/1/root'+str(secret),'/proc/self/root'+str(secret)])+']))'
        r=self.execute(code)
        self.assertEqual(json.loads(r['result']['stdout']),[False,False])

    def test_large_output_is_bounded(self):
        r=self.execute('print("x"*131072)')
        self.assertTrue(r['result']['truncated'])
        self.assertEqual(len(r['result']['stdout']),65536)
