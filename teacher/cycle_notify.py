# SPDX-License-Identifier: MIT
"""Detached administrative supervisor; never imported by teacher workers."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import traceback
import uuid

from .cycle import ROOT


def notify(thread, result, reports, position, codex='codex'):
    message = ('Cycle exited: ' + json.dumps(result, sort_keys=True) +
               '. Inspect the result and reports; this is not a reviewer verdict or permission to bypass a stop.')
    try:
        completed = subprocess.run([codex, 'queue', '--thread', thread, '--resume',
                                    '--message', message], capture_output=True, text=True, timeout=60)
        # A queued message succeeds even if immediate resume reports a warning.
        if completed.returncode or 'Queued message' not in completed.stdout:
            raise RuntimeError(f'queue exit {completed.returncode}: {completed.stdout}\n{completed.stderr}')
    except BaseException:
        failure = reports / f'cycle-notify-failed-{position}.txt'
        with failure.open('a') as f:
            f.write(message + '\n' + traceback.format_exc() + '\n')
        return False
    return True


def supervise(state, thread, auth_file, reports, codex='codex'):
    reports = Path(reports)
    reports.mkdir(parents=True, exist_ok=True)
    position = 'unknown'
    result = {'status': 'supervisor_failed'}
    child = None
    handlers = {}
    def interrupted(signum, frame):
        raise InterruptedError(f'Signal {signum}')
    try:
        for sig in (signal.SIGTERM, signal.SIGINT):
            handlers[sig] = signal.signal(sig, interrupted)
        position = json.loads(Path(state).read_text())['next_position']
        prefix = reports / f'cycle-detached-{position:06d}-{uuid.uuid4().hex}'
        log = Path(str(prefix) + '.log')
        result_path = Path(str(prefix) + '.json')
        result.update(log=str(log), result_path=str(result_path), position=position)
        with log.open('x') as output:
            child = subprocess.Popen([sys.executable, '-m', 'teacher.cycle', '--state',
                                      str(Path(state).resolve()), '--auth-file', str(auth_file)],
                                     cwd=ROOT, stdin=subprocess.DEVNULL, stdout=output,
                                     stderr=subprocess.STDOUT, start_new_session=True)
            returncode = child.wait()
        result['returncode'] = returncode
        if returncode:
            result['status'] = 'cycle_failed'
        else:
            data = json.loads(log.read_text())
            result.update({k: data[k] for k in ('status', 'summary', 'skeleton', 'draft', 'detail') if k in data})
    except BaseException as error:
        result.update(status='supervisor_failed', error_type=type(error).__name__, detail=str(error))
        if child is not None and child.poll() is None:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
    finally:
        # Ignore further termination while saving the result and attempting the one notification.
        for sig in handlers:
            signal.signal(sig, signal.SIG_IGN)
        try:
            if 'result_path' in result:
                Path(result['result_path']).write_text(json.dumps(result, indent=2) + '\n')
        finally:
            try:
                result['notification_sent'] = notify(thread, result, reports, position, codex)
            finally:
                for sig, handler in handlers.items():
                    signal.signal(sig, handler)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--notify-thread', required=True)
    parser.add_argument('--auth-file', type=Path, default=Path.home()/'.codex/auth.json')
    args = parser.parse_args()
    result = supervise(args.state, args.notify_thread, args.auth_file, ROOT/'reports')
    print(json.dumps(result, indent=2))
    return 0 if result['notification_sent'] else 1


if __name__ == '__main__':
    sys.exit(main())
