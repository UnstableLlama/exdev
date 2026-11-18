# SPDX-License-Identifier: MIT
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from orchestration import notify as n


class RunAheadNotifyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state = self.root/'state.json'
        self.state.write_text(json.dumps({'next_position': 162}))

    def run_cycle(self, data, code=0):
        def launch(*args, **kwargs):
            self.assertEqual(args[0][1:4], ['-m','orchestration.run_ahead','cycle'])
            kwargs['stdout'].write(data); kwargs['stdout'].flush()
            return Mock(wait=Mock(return_value=code))
        with patch.object(n.subprocess, 'Popen', side_effect=launch), patch.object(n, 'notify', return_value=True) as notification:
            result = n.supervise(self.state, 'thread', self.root/'auth', self.root)
            notification.assert_called_once()
        saved = json.loads(Path(result['result_path']).read_text())
        self.assertEqual(saved['status'], result['status'])
        return result

    def test_success_and_named_stop(self):
        for data in [{'status':'awaiting_review_request','run':'.teacher/runs/commit-000162-001','snapshot':'snapshot.json'},
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

    def test_interruption_terminates_child_and_notifies(self):
        child=Mock(pid=123,poll=Mock(return_value=None),wait=Mock(side_effect=[InterruptedError('signal'),0]))
        with patch.object(n.subprocess,'Popen',return_value=child),patch.object(n.os,'killpg') as kill,patch.object(n,'notify',return_value=True) as notification:
            r=n.supervise(self.state,'thread',self.root/'auth',self.root)
        kill.assert_called_once_with(123,n.signal.SIGTERM)
        notification.assert_called_once();self.assertEqual(r['status'],'supervisor_failed')
