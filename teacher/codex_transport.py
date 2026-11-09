# SPDX-License-Identifier: MIT
"""Bounded JSON-RPC transport to a fresh, filesystem-isolated Codex app-server."""
from collections import deque
import json
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import tempfile
import time
from .codex_adapter import DISABLED_FEATURES

SUPPORTED_VERSION = 'codex-cli 0.167.0'


def configuration():
    lines=['model = "gpt-6-astra"','model_reasoning_effort = "medium"',
           'web_search = "disabled"','project_doc_max_bytes = 0',
           'include_environment_context = false','model_catalog_json = "/state/model.json"',
           '[agents]','enabled = false','[skills]','include_instructions = false',
           '[skills.bundled]','enabled = false','[tools.experimental_request_user_input]','enabled = false','[features]']
    lines += [name+' = false' for name in DISABLED_FEATURES]
    lines += ['skip_host_skill_discovery = true','omit_skill_descriptions = true']
    return '\n'.join(lines)+'\n'


class CodexTransport:
    cwd='/work'

    def __init__(self, auth_file, executable=None, timeout=1200):
        self.auth_file=Path(auth_file)
        self.executable=Path(executable or shutil.which('codex') or '').resolve()
        self.timeout=timeout
        self.pending=deque(); self.buffer=b''; self.sequence=0; self.received=0

    def __enter__(self):
        version=subprocess.check_output([str(self.executable),'--version'],stderr=subprocess.DEVNULL,text=True).strip()
        if version!=SUPPORTED_VERSION:
            raise ValueError('Codex version has not been boundary-tested: '+version)
        if not self.auth_file.is_file():
            raise ValueError('A Codex auth file is required; authenticate outside the authoring runner')
        self.temporary=tempfile.TemporaryDirectory(prefix='exdev-provider-')
        root=Path(self.temporary.name)
        try:
            state=root/'state';state.mkdir(mode=0o700)
            auth=state/'auth.json';auth.write_bytes(self.auth_file.read_bytes());auth.chmod(0o600)
            (state/'config.toml').write_text(configuration())
            catalog=Path(__file__).resolve().parents[1]/'schema/codex-teacher-model.json'
            (state/'model.json').write_bytes(catalog.read_bytes())
            command=['/usr/bin/bwrap','--unshare-all','--share-net','--die-with-parent',
                '--new-session','--cap-drop','ALL','--clearenv',
                '--setenv','HOME','/work','--setenv','CODEX_HOME','/state',
                '--setenv','PATH','/app','--setenv','LANG','C.UTF-8',
                '--ro-bind',str(self.executable),'/app/codex',
                '--bind',str(state),'/state','--proc','/proc','--dev','/dev',
                '--tmpfs','/tmp','--tmpfs','/work','--chdir','/work']
            for path in ('/etc/ssl/certs','/etc/resolv.conf','/etc/hosts','/etc/nsswitch.conf',
                         '/usr/lib/x86_64-linux-gnu','/lib64/ld-linux-x86-64.so.2'):
                if Path(path).exists():command += ['--ro-bind',path,path]
            command += ['--symlink','usr/lib','/lib','/app/codex','app-server','--stdio','--strict-config']
            self.stderr=tempfile.TemporaryFile()
            self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                stderr=self.stderr,start_new_session=True,env={'PATH':'/usr/bin:/bin'})
            self.selector=selectors.DefaultSelector();self.selector.register(self.process.stdout,selectors.EVENT_READ)
            self.deadline=time.monotonic()+self.timeout
            return self
        except BaseException:
            self.__exit__(None,None,None)
            raise

    def __exit__(self,*_):
        if hasattr(self,'process'):
            if self.process.poll() is None:
                os.killpg(self.process.pid,signal.SIGKILL)
            self.process.wait()
            self.process.stdin.close();self.process.stdout.close()
        if hasattr(self,'selector'):self.selector.close()
        if hasattr(self,'stderr'):self.stderr.close()
        if hasattr(self,'temporary'):self.temporary.cleanup()

    def send(self, value):
        encoded=json.dumps(value).encode()+b'\n'
        if len(encoded)>4*1024**2:raise ValueError('Provider request budget exceeded')
        self.process.stdin.write(encoded);self.process.stdin.flush()

    def notify(self, method, params):self.send({'method':method,'params':params})
    def reply(self, identity, result):self.send({'id':identity,'result':result})

    def _receive(self):
        while b'\n' not in self.buffer:
            remaining=self.deadline-time.monotonic()
            if remaining<=0 or not self.selector.select(min(remaining,30)):
                if remaining>30:continue
                raise TimeoutError('Codex provider deadline exceeded')
            chunk=os.read(self.process.stdout.fileno(),65536)
            if not chunk:raise RuntimeError('Codex provider closed its protocol stream')
            self.buffer+=chunk;self.received+=len(chunk)
            if len(self.buffer)>4*1024**2 or self.received>64*1024**2:
                raise ValueError('Provider response budget exceeded')
        line,self.buffer=self.buffer.split(b'\n',1)
        return json.loads(line)

    def receive(self):
        return self.pending.popleft() if self.pending else self._receive()

    def request(self, method, params):
        self.sequence+=1; identity=self.sequence
        self.send({'id':identity,'method':method,'params':params})
        while True:
            event=self._receive()
            if event.get('id')==identity and 'method' not in event:
                if 'error' in event:
                    raise RuntimeError('Codex RPC failed for '+method+': '+str(event['error'].get('code')))
                return event['result']
            if 'id' in event:
                raise ValueError('Unexpected provider request during setup')
            self.pending.append(event)
