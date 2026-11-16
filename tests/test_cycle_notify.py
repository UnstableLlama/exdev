# SPDX-License-Identifier: MIT
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from teacher import cycle_notify as n


class NotifyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state = self.root/'state.json'
        self.state.write_text(json.dumps({'next_position': 162}))

    def run_cycle(self, data, code=0):
        def launch(*args, **kwargs):
            kwargs['stdout'].write(data); kwargs['stdout'].flush()
            return Mock(wait=Mock(return_value=code))
        with patch.object(n.subprocess, 'Popen', side_effect=launch), patch.object(n, 'notify', return_value=True) as notification:
            result = n.supervise(self.state, 'thread', self.root/'auth', self.root)
            notification.assert_called_once()
        saved = json.loads(Path(result['result_path']).read_text())
        self.assertEqual(saved['status'], result['status'])
        return result

    def test_success_and_named_stop(self):
        for data in [{'status':'awaiting_review_request','summary':'reports/summary.json'},
                     {'status':'architecture_trigger','detail':'manual recovery'}]:
            r = self.run_cycle(json.dumps(data))
            for k,v in data.items():self.assertEqual(r[k],v)

    def test_child_crash_notifies(self):
        self.assertEqual(self.run_cycle('traceback', 1)['status'], 'cycle_failed')

    def test_bad_output_and_missing_state_notify(self):
        self.assertEqual(self.run_cycle('invalid')['status'], 'supervisor_failed')
        self.state.unlink()
        with patch.object(n, 'notify', return_value=True) as notification:
            r=n.supervise(self.state,'thread',self.root/'auth',self.root)
        notification.assert_called_once();self.assertEqual(r['error_type'],'FileNotFoundError')

    def test_queue_success_exact_arguments(self):
        with patch.object(n.subprocess,'run',return_value=Mock(returncode=0,stderr='',stdout='Queued message id')) as run:
            self.assertTrue(n.notify('thread',{'status':'busy'},self.root,162))
        args=run.call_args.args[0]
        self.assertEqual(args[:6],['codex','queue','--thread','thread','--resume','--message'])

    def test_queue_failure_timeout_and_missing_confirmation_saved(self):
        for failure in [Mock(returncode=1,stdout='',stderr='failed'),Mock(returncode=0,stdout='',stderr='Warning: failed resume'),TimeoutError('timeout')]:
            kwargs={'side_effect':failure} if isinstance(failure,Exception) else {'return_value':failure}
            with patch.object(n.subprocess,'run',**kwargs):
                self.assertFalse(n.notify('thread',{'status':'busy'},self.root,162))
            self.assertIn('busy',(self.root/'cycle-notify-failed-162.txt').read_text())

    def test_queue_resume_warning_with_confirmation_succeeds(self):
        with patch.object(n.subprocess, 'run', return_value=Mock(
                returncode=0, stdout='Queued message id', stderr='Warning: could not resume thread')):
            self.assertTrue(n.notify('thread', {'status': 'busy'}, self.root, 162))
        self.assertFalse((self.root/'cycle-notify-failed-162.txt').exists())

    def test_interruption_terminates_child_and_notifies(self):
        child=Mock(pid=123,poll=Mock(return_value=None),wait=Mock(side_effect=[InterruptedError('signal'),0]))
        with patch.object(n.subprocess,'Popen',return_value=child),patch.object(n.os,'killpg') as kill,patch.object(n,'notify',return_value=True) as notification:
            r=n.supervise(self.state,'thread',self.root/'auth',self.root)
        kill.assert_called_once_with(123,n.signal.SIGTERM)
        notification.assert_called_once();self.assertEqual(r['status'],'supervisor_failed')
