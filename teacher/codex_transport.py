# SPDX-License-Identifier: MIT
"""Bounded JSON-RPC transport to a fresh, filesystem-isolated Codex app-server."""
from collections import deque
import json
import os
from pathlib import Path
import selectors
import shutil
import signal
import stat
import subprocess
import tempfile
import time
from .codex_adapter import DISABLED_FEATURES, MODEL, LEGACY_MODEL, checked_model
from .codex_diagnostics import LIMIT, Redactor, auth_secrets

SUPPORTED_VERSION = 'codex-cli 0.167.0'


def configuration(model=MODEL):
    checked_model(model)
    lines=['model = '+json.dumps(model),'model_reasoning_effort = "medium"',
           'web_search = "disabled"','project_doc_max_bytes = 0',
           'include_environment_context = false','model_catalog_json = "/state/model.json"',
           '[agents]','enabled = false','[skills]','include_instructions = false',
           '[skills.bundled]','enabled = false','[tools.experimental_request_user_input]','enabled = false','[features]']
    lines += [name+' = false' for name in DISABLED_FEATURES]
    lines += ['skip_host_skill_discovery = true','omit_skill_descriptions = true']
    return '\n'.join(lines)+'\n'


class CodexTransport:
    cwd='/work'

    def __init__(self, auth_file, executable=None, timeout=1200, *, model=MODEL):
        self.model=checked_model(model)
        self.auth_file=Path(auth_file)
        self.executable=Path(executable or shutil.which('codex') or '').resolve()
        self.timeout=timeout
        self.pending=deque(); self.buffer=b''; self.sequence=0; self.received=0
        self.failure_diagnostics = None
        self._error_events = []
        self._error_bytes = 0
        self._omitted_errors = 0

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
            self._sandbox_auth = state/'auth.json'
            self._initial_auth = self.auth_file.read_bytes()
            self._sandbox_auth.write_bytes(self._initial_auth)
            self._sandbox_auth.chmod(0o600)
            (state/'config.toml').write_text(configuration() if self.model==MODEL else configuration(self.model))
            catalog=Path(__file__).resolve().parents[1]/'schema/codex-teacher-model.json'
            if self.model == LEGACY_MODEL:
                (state/'model.json').write_bytes(catalog.read_bytes())
            else:
                profile=json.loads(catalog.read_text())
                profile['models'][0]['slug']=self.model
                profile['models'][0]['display_name']=self.model
                (state/'model.json').write_text(json.dumps(profile))
            command=['/usr/bin/bwrap','--unshare-all','--share-net','--die-with-parent',
                '--new-session','--cap-drop','ALL','--clearenv',
                '--setenv','HOME','/work','--setenv','CODEX_HOME','/state',
                '--setenv','PATH','/app','--setenv','LANG','C.UTF-8',
                '--ro-bind',str(self.executable),'/app/codex',
                '--bind',str(state),'/state','--proc','/proc','--dev','/dev',
                '--tmpfs','/tmp','--tmpfs','/work','--chdir','/work']
            for path in ('/etc/ssl/certs','/etc/resolv.conf','/etc/hosts','/etc/nsswitch.conf',
                         '/usr/lib/x86_64-linux-gnu','/lib64/ld-linux-x86-64.so.2',
                         '/usr/lib/aarch64-linux-gnu'):
                if Path(path).exists():command += ['--ro-bind',path,path]
            command += ['--symlink','usr/lib','/lib','/app/codex','app-server','--stdio','--strict-config']
            self.stderr=tempfile.TemporaryFile()
            self.process=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                stderr=self.stderr,start_new_session=True,env={'PATH':'/usr/bin:/bin'})
            self.selector=selectors.DefaultSelector();self.selector.register(self.process.stdout,selectors.EVENT_READ)
            self.deadline=time.monotonic()+self.timeout
            return self
        except BaseException as error:
            self.__exit__(type(error), error, error.__traceback__)
            raise

    def __exit__(self, exc_type, _error, _traceback):
        try:
            if hasattr(self, 'process'):
                if self.process.poll() is None:
                    try:
                        os.killpg(self.process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                self.process.wait()
                self.process.stdin.close()
                self.process.stdout.close()
        finally:
            if exc_type is not None and hasattr(self, 'stderr'):
                self._collect_failure()
            self._initial_auth = None
            self._error_events.clear()
            if hasattr(self, 'selector'):
                self.selector.close()
            if hasattr(self, 'stderr'):
                self.stderr.close()
            if hasattr(self, 'temporary'):
                self.temporary.cleanup()

    def _collect_failure(self):
        try:
            # The server can refresh credentials in its private state during a run.
            fd = os.open(self._sandbox_auth, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(fd, 'rb') as auth:
                if not stat.S_ISREG(os.fstat(auth.fileno()).st_mode):
                    raise ValueError('Expected a regular Codex auth file')
                current_auth = auth.read(LIMIT + 1)
            if len(current_auth) > LIMIT or len(self._initial_auth) > LIMIT:
                raise ValueError('Codex auth exceeds diagnostics budget')
            secrets = auth_secrets(self._initial_auth)
            if current_auth != self._initial_auth:
                secrets.update(auth_secrets(current_auth))
            redactor = Redactor(secrets)
            stderr = os.pread(self.stderr.fileno(), LIMIT + 1, 0)
            stderr_oversize = len(stderr) > LIMIT
            self.failure_diagnostics = {
                'error_events': redactor.payload(self._error_events),
                'omitted_error_events': self._omitted_errors,
                'stderr': None if stderr_oversize else redactor.text(stderr.decode('utf-8', errors='replace')),
                'stderr_omitted': 'size_limit' if stderr_oversize else None,
            }
        except Exception:
            # Redaction or read failures must never expose raw data or replace the run error.
            self.failure_diagnostics = {'unavailable': 'capture_or_redaction_failed'}

    def _remember_error(self, event, size):
        if len(self._error_events) >= 8 or self._error_bytes + size > LIMIT:
            self._omitted_errors += 1
            return
        self._error_bytes += size
        self._error_events.append(event)

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
        event = json.loads(line)
        if isinstance(event, dict) and (event.get('method') == 'error' or 'error' in event):
            self._remember_error(event, len(line))
        return event

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
