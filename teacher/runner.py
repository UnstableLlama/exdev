# SPDX-License-Identifier: MIT
"""Trusted supervisor: run each author tool in a fresh Bubblewrap namespace."""
import argparse
from functools import partial
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import tempfile
from .worker import args_for

ROOT = Path(__file__).resolve().parents[1]


def limits(graph=False):
    resource.setrlimit(resource.RLIMIT_CPU, (25, 25))
    memory = (4096 if graph else 768) * 1024**2
    resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
    file_size = (256 if graph else 2) * 1024**2
    resource.setrlimit(resource.RLIMIT_FSIZE, (file_size, file_size))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def command(packet, graph=False):
    # Linux runtime allowlist, not a bind mount of the host root or /home.
    python = Path('/usr/bin/python3').resolve()
    stdlib = Path('/usr/lib') / f'python{sys.version_info.major}.{sys.version_info.minor}'
    libraries = Path('/usr/lib/x86_64-linux-gnu')
    loader = Path('/lib64/ld-linux-x86-64.so.2').resolve()
    required = (python, stdlib, libraries, loader, Path('/usr/bin/bwrap'))
    if any(not p.exists() for p in required):
        raise RuntimeError('Unsupported runtime: this profile requires Linux amd64 and system Python')
    extra = []
    if graph:
        from graph.validate import BIN, PIN
        import hashlib
        if hashlib.sha256(BIN.read_bytes()).hexdigest() != PIN:
            raise ValueError('Graph backend binary checksum mismatch')
        for relative in ('teacher/graph_worker.py', 'graph/tools.py', 'graph/timeline.py',
                         'graph/validate.py', 'schema/graph-tools-v1.json'):
            extra.extend(['--ro-bind', str(ROOT/relative), '/app/'+relative])
        extra.extend(['--ro-bind', str(BIN), '/app/.tools/cbm-v0.12.1/codebase-memory-mcp'])
    return ['/usr/bin/bwrap', '--unshare-all', '--die-with-parent', '--new-session',
            '--cap-drop', 'ALL', '--clearenv', '--setenv', 'PATH', '/usr/bin',
            '--setenv', 'HOME', '/work', '--setenv', 'TMPDIR', '/tmp',
            '--setenv', 'LANG', 'C.UTF-8', '--setenv', 'TZ', 'UTC',
            '--ro-bind', str(python), '/usr/bin/python3',
            '--ro-bind', str(stdlib), str(stdlib),
            '--ro-bind', str(libraries), str(libraries),
            '--symlink', 'usr/lib', '/lib', '--ro-bind', str(loader), '/lib64/ld-linux-x86-64.so.2',
            *(['--tmpfs', str(stdlib/'site-packages')] if (stdlib/'site-packages').exists() else []),
            '--ro-bind', str(ROOT/'teacher/worker.py'), '/app/teacher/worker.py',
            '--ro-bind', str(ROOT/'schema/repo-tools-v1.json'), '/app/schema/repo-tools-v1.json',
            *extra,
            '--ro-bind', str(packet), '/packet',
            '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp', '--tmpfs', '/work',
            '--chdir', '/work', '/usr/bin/python3', '-I', '-S', '/app/teacher/worker.py']


class Runner:
    """Packet selection is trusted configuration, never a model tool argument."""
    def __init__(self, packet):
        self.packet = Path(packet).resolve()
        if not (self.packet/'manifest.json').is_file():
            raise ValueError('Missing prepared packet')
        # The curator must publish regular files only. No links to host data are allowed.
        if any(p.is_symlink() for p in self.packet.rglob('*')):
            raise ValueError('Packet contains a symlink')

    def invoke(self, tool, arguments):
        graph = tool in ('graph_search','graph_trace','graph_query','symbol_history','repo_map')
        if graph and 'graphs' not in json.loads((self.packet/'manifest.json').read_text()):
            raise ValueError('No approved graph packet')
        args_for(tool, arguments)
        request = json.dumps({'tool': tool, 'arguments': arguments}).encode()
        if len(request) > 1048576:
            raise ValueError('Request budget exceeded')
        with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
            process = subprocess.Popen(command(self.packet, graph=graph), stdin=subprocess.PIPE, stdout=stdout,
                                       stderr=stderr, preexec_fn=partial(limits, graph=graph), start_new_session=True)
            try:
                process.communicate(request, timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                return {'ok': False, 'error': 'Isolated tool exceeded wall-time budget'}
            stdout.seek(0); stderr.seek(0)
            output = stdout.read(1048577)
            error = stderr.read(4096).decode(errors='replace')
        if process.returncode != 0:
            # Never fall back to executing a tool on the host.
            raise RuntimeError('Isolated worker failed: ' + error)
        if len(output) > 1048576:
            raise RuntimeError('Isolated tool exceeded response budget')
        return json.loads(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True, help='Trusted packet selection, not model arguments')
    args = parser.parse_args()
    request = json.load(sys.stdin)
    if set(request) != {'tool', 'arguments'}:
        raise ValueError('Invalid request envelope')
    print(json.dumps(Runner(args.packet).invoke(request['tool'], request['arguments']), indent=2))


if __name__ == '__main__':
    main()
