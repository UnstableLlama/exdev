# SPDX-License-Identifier: MIT
import json
from pathlib import Path
import unittest
from teacher.root_tasks import validate_plan, task_for, validate_task
from teacher.session import FreshSession
from teacher.codex_adapter import thread_parameters
import test_teacher_packet

ROOT=Path(__file__).resolve().parents[1]

class RootTaskTests(unittest.TestCase):
    setUp=test_teacher_packet.PacketTests.setUp
    tearDown=test_teacher_packet.PacketTests.tearDown

    def test_assignment_cannot_omit_or_duplicate_files(self):
        manifest=json.loads((self.packet/'manifest.json').read_text())
        paths=[s['header'].split(' b/',1)[1] for s in manifest['task_change_sections']]
        plan={'chapters':[{'id':'test','files':paths,'required_evidence':[],'focus':'Explain design.'}], 'excluded':[]}
        validate_plan(plan,manifest)
        plan['chapters'][0]['files']=[]
        with self.assertRaises(ValueError):validate_plan(plan,manifest)
        plan['chapters'][0]['files']=paths+paths
        with self.assertRaises(ValueError):validate_plan(plan,manifest)

    def test_chapter_requires_nonempty_assignments_and_high_effort(self):
        p=self.packet/'manifest.json'; manifest=json.loads(p.read_text())
        paths=[s['header'].split(' b/',1)[1] for s in manifest['task_change_sections']]
        chapter={'id':'test','files':paths,'required_evidence':[],'focus':'Explain design.'}
        manifest['authoring_task']=task_for(chapter,manifest)
        p.write_text(json.dumps(manifest));session=FreshSession(self.packet)
        self.assertEqual(thread_parameters(session,'/tmp')['config']['model_reasoning_effort'],'high')
        self.assertEqual(json.loads(session.initial[1]['content'])['authoring_task']['id'],'test')
        manifest['authoring_task']['required_sections']=[]
        with self.assertRaises(ValueError):validate_task(manifest)

    def test_root_without_assignment_is_blocked(self):
        p=self.packet/'manifest.json';manifest=json.loads(p.read_text())
        manifest['task_parents']=[];p.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError,'subsystem assignment'):FreshSession(self.packet).require_authoring_context()
