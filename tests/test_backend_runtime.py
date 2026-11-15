# SPDX-License-Identifier: MIT
import unittest
from unittest.mock import patch
from pathlib import Path
from graph.validate import backend
from teacher.runner import command


class BackendRuntimeTests(unittest.TestCase):
    def test_machine_selection_and_legacy_pin(self):
        amd, pin = backend('x86_64')
        arm, arm_pin = backend('aarch64')
        self.assertEqual(amd.parent.name, 'cbm-v0.12.1')
        self.assertEqual(pin, '77745491f0a9c346d6da23eed4d92b5feaa31a27a883c9faa4fa9f47c8183705')
        self.assertEqual(arm.parent.name, 'cbm-v0.12.1-arm64')
        self.assertNotEqual(pin, arm_pin)
        with self.assertRaisesRegex(RuntimeError, 'Unsupported graph backend'):
            backend('unknown')

    def test_runner_rejects_modified_binary(self):
        with patch('pathlib.Path.exists', return_value=True), patch('pathlib.Path.read_bytes', return_value=b'corrupt'):
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                command(Path('/packet'), graph=True)
