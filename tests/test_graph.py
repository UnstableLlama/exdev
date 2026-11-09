# SPDX-License-Identifier: MIT
import unittest
from graph.validate import stable_symbols, binding_definitions

class GraphValidationTests(unittest.TestCase):
    def test_stability_ignores_line_shifts_but_detects_name_drift(self):
        a = dict(file='a.py', kind='Function', name='f', body_hash='abc', qn='p.a.f')
        b = dict(a, qn='p.changed.f')
        self.assertEqual(stable_symbols([a], [b]), {'comparable': 1, 'stable': 0, 'drift': [['p.a.f', 'p.changed.f']]})

    def test_ambiguous_identical_symbols_are_not_matched(self):
        a = dict(file='a.py', kind='Function', name='f', body_hash='abc', qn='p.a.f')
        self.assertEqual(stable_symbols([a, dict(a, qn='p.a.C.f')], [a])['comparable'], 0)

    def test_binding_definition_requires_direct_function_reference(self):
        self.assertEqual(binding_definitions('m.def("foo", &foo); m.def("x", []() {});'), {'foo': {'foo'}})

    def test_export_follows_truncated_pages(self):
        from pathlib import Path
        from unittest.mock import patch
        from graph.validate import export
        with patch('graph.validate.call', side_effect=[
            {'rows': [[1]], 'has_more': True},
            {'rows': [[2]], 'has_more': False},
        ]) as backend:
            self.assertEqual(export('query', Path('/cache'), Path('/logs'), 'nodes'), [[1], [2]])
            self.assertEqual(backend.call_args_list[1].args[1]['offset'], 1)

    def test_export_rejects_truncation_without_progress(self):
        from pathlib import Path
        from unittest.mock import patch
        from graph.validate import export
        with patch('graph.validate.call', return_value={'rows': [], 'truncated': True}):
            with self.assertRaisesRegex(RuntimeError, 'without progress'):
                export('query', Path('/cache'), Path('/logs'), 'nodes')
