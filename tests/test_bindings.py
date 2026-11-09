# SPDX-License-Identifier: MIT
import unittest
from graph.bindings import supplement

NODES = [dict(qn='p.a.f',name='f',kind='Function',file='a.py',start=2,end=9),
         dict(qn='p.native.foo',name='foo',kind='Function',file='native.cu',start=1,end=3)]

class BindingTests(unittest.TestCase):
    def run_pass(self, source, native='m.def("foo", &foo);', nodes=None, edges=()):
        return supplement(dict(sha='abc',nodes=nodes or NODES,edges=list(edges)),
                          {'a.py':source,'bindings.cpp':native})

    def test_adds_evidence_and_deduplicates_call_sites(self):
        r=self.run_pass('from .ext import exllamav3_ext as ext\ndef f():\n ext.foo()\n ext.foo()\n')
        self.assertEqual(len(r['edges']),1)
        self.assertEqual(len(r['edges'][0]['evidence']),2)
        self.assertEqual(r['edges'][0]['target'],'p.native.foo')
        self.assertEqual(r['edges'][0]['evidence'][0]['binding_line'],1)

    def test_does_not_duplicate_backend_edge(self):
        r=self.run_pass('from .ext import exllamav3_ext as ext\ndef f():\n ext.foo()\n',edges=[['p.a.f','CALLS','p.native.foo']])
        self.assertEqual(r['edges'],[])
        self.assertEqual(r['sites'][0]['status'],'backend_present')

    def test_shadowed_alias_and_ambiguous_native_are_unresolved(self):
        r=self.run_pass('from .ext import exllamav3_ext as ext\ndef f(ext):\n ext.foo()\n')
        self.assertEqual(r['edges'],[])
        self.assertEqual(r['sites'][0]['status'],'shadowed_alias')
        r=self.run_pass('from .ext import exllamav3_ext as ext\ndef f():\n ext.foo()\n',nodes=NODES+[dict(NODES[1],qn='p.other.foo')])
        self.assertEqual(r['edges'],[])
        self.assertEqual(r['sites'][0]['status'],'ambiguous_native_target')

    def test_comments_are_not_binding_definitions(self):
        r=self.run_pass('from .ext import exllamav3_ext as ext\ndef f():\n ext.foo()\n',native='// m.def("foo", &foo);')
        self.assertEqual(r['edges'],[])

    def test_unrelated_import_is_not_extension_alias(self):
        r=self.run_pass('from unrelated import exllamav3_ext as ext\ndef f():\n ext.foo()\n')
        self.assertEqual(r['sites'],[])
