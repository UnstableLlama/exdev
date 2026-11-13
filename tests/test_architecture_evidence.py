# SPDX-License-Identifier: MIT
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import test_teacher_packet
from teacher.architecture_evidence import trigger,load_bundle
from teacher.root_evidence import choose_revision,recover_hf
from teacher.walk_inputs import prepare,validate_bundle
from teacher.session import FreshSession


class ArchitectureTests(unittest.TestCase):
    architecture_fixture=True
    setUp=test_teacher_packet.PacketTests.setUp
    tearDown=test_teacher_packet.PacketTests.tearDown

    def add(self,path,text):
        p=self.repo/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
        self.git('add','.');self.git('commit','-m','Add architecture fixture');return self.git('rev-parse','HEAD')

    def test_triggers_registry_successor_class_and_neither(self):
        self.assertEqual(trigger(self.repo,self.task),{'architectures':[],'class_files':[]})
        sha=self.add('exllamav3/models/registry_v2.py','REGISTRY={"Demo": {"config_class": C, "model_class": M}}')
        self.assertEqual(trigger(self.repo,sha)['architectures'],['Demo'])
        sha=self.add('exllamav3/models/demo.py','class DemoConfig: pass\nclass DemoModel: pass\n')
        self.assertEqual(trigger(self.repo,sha)['class_files'],['exllamav3/models/demo.py'])

    def test_trigger_requires_recovery(self):
        sha=self.add('exllamav3/models/demo.py','class DemoModel: pass')
        with self.assertRaisesRegex(ValueError,'recovery required'):load_bundle(self.repo,sha,self.root/'missing')

    def test_cutoff_and_no_eligible_revision(self):
        rows=[{'id':'a'*40,'date':'2020-01-01T00:00:00Z'},{'id':'b'*40,'date':'2022-01-01T00:00:00Z'}]
        self.assertEqual(choose_revision(rows,'2021-01-01T00:00:00Z')['id'],'a'*40)
        with patch('teacher.root_evidence.pages',return_value=iter([rows])):
            items,report=recover_hf('Demo',self.root,repo='org/demo',cutoff='2019-01-01T00:00:00Z',reference_only=True)
        self.assertEqual(items,[]);self.assertEqual(report['status'],'no_eligible_revision')

    def test_recovery_never_fetches_weights(self):
        rows=[{'id':'a'*40,'date':'2020-01-01T00:00:00Z'}]
        tree=[{'type':'file','path':p} for p in ['config.json','tokenizer_config.json','model.bin','model.safetensors','malicious.py']]
        header=b'{}';calls=[]
        def fetch(url,byte_range=None,**kw):
            calls.append((url,byte_range))
            if byte_range==(0,7):return (2).to_bytes(8,'little'),{}
            if byte_range:return header,{}
            return b'{}',{}
        with patch('teacher.root_evidence.pages',side_effect=[iter([rows]),iter([tree])]),patch('teacher.root_evidence.fetch',side_effect=fetch):
            items,_=recover_hf('Demo',self.root,repo='org/demo',cutoff='2021-01-01T00:00:00Z',reference_only=True)
        self.assertFalse(any('model.bin' in u or 'malicious.py' in u for u,_ in calls))
        self.assertTrue(all(r is not None for u,r in calls if 'safetensors' in u))
        self.assertTrue(all(x['artifact_role'] in ('non_weight','tensor_header') for x in items))

    def test_guidance_legacy_and_new_contract(self):
        old=FreshSession(self.packet).initial[0]['content'];self.assertNotIn('read the selected callee',old)
        directory=self.root/'evidence';directory.mkdir()
        cutoff=self.git('show','-s','--format=%cI',self.task)
        (directory/'000001-unreferenced.json').write_text(json.dumps({'task_sha':self.task,'cutoff':cutoff,'complete':True,'limit':100,'truncated':False,'items':[]}))
        (directory/'000001-closed.json').write_text(json.dumps({'task_sha':self.task,'cutoff':cutoff,'complete':True,'rule':'salience-v2','limit':20,'truncated':False,'items':[]}))
        packet=self.root/'new';m=prepare(self.repo,self.task,1,packet,directory)
        self.assertEqual(m['walk_input_contract']['version'],8)
        self.assertIn('read the selected callee',FreshSession(packet).initial[0]['content'])
        self.assertIn("read the config.json of every such model before finalizing",FreshSession(packet).initial[0]['content'])
        self.assertNotIn("If any was not read",FreshSession(packet).initial[0]['content'])
        self.assertNotIn("read every model's config.json",old)
        self.assertNotIn('evidence_index',[t['name'] for t in FreshSession(self.packet).tools])
        validate_bundle(packet,directory/'000001-eligible.json')
        legacy=json.loads(json.dumps(m));legacy['walk_input_contract']['version']=6;legacy['guidance_version']=3
        (packet/'manifest.json').write_text(json.dumps(legacy))
        legacy_system=FreshSession(packet).initial[0]['content']
        self.assertIn("If any was not read",legacy_system)
        self.assertNotIn("read the config.json of every such model before finalizing",legacy_system)
        (packet/'manifest.json').write_text(json.dumps(m))
        m['walk_input_contract']['reference_signatures']=[['lost','a'*64]]
        (packet/'manifest.json').write_text(json.dumps(m))
        with self.assertRaisesRegex(ValueError,'Reference evidence'):validate_bundle(packet,directory/'000001-eligible.json')

    def test_reference_attachment_binding_and_weight_rejection(self):
        from teacher.root_evidence import item
        sha=self.add('exllamav3/models/registry.py','ARCHITECTURES={"Demo": {"config_class": C, "model_class": M}}')
        cutoff=self.git('show','-s','--format=%cI',sha);directory=self.root/'evidence';directory.mkdir()
        (directory/'000001-unreferenced.json').write_text(json.dumps({'task_sha':sha,'cutoff':cutoff,'complete':True,'limit':100,'truncated':False,'items':[]}))
        items=[]
        for name,data,kind,role in [('config.json',b'{"architectures":["Demo"]}','hf_file','non_weight'),('tokenizer_config.json',b'{}','hf_file','non_weight'),('model.safetensors',b'{"w":{"dtype":"F16","shape":[1],"data_offsets":[0,2]}}','safetensors_header','tensor_header')]:
            items.append(item(name,'https://huggingface.co/org/demo/resolve/'+('a'*40)+'/'+name,data,cutoff,kind=kind,artifact_role=role,repo_id='org/demo',revision='a'*40,path=name))
        bundle={'task_sha':sha,'cutoff':cutoff,'trigger':trigger(self.repo,sha),'items':items,'selections':[{'architecture':'Demo','repo':'org/demo','revision':'a'*40,'date':cutoff,'status':'complete','reason':'Task-named fixture','candidates_considered':['org/demo']}]}
        ref=directory/'000001-references.json';ref.write_text(json.dumps(bundle))
        (directory/'000001-closed.json').write_text(json.dumps({'task_sha':sha,'cutoff':cutoff,'complete':True,'rule':'salience-v2','limit':20,'truncated':False,'items':[]}))
        packet=self.root/'references';m=prepare(self.repo,sha,1,packet,directory)
        self.assertEqual(len(m['evidence']),3)
        opening=json.loads(FreshSession(packet).initial[1]['content'])
        self.assertEqual(opening['evidence_catalog'],[])
        self.assertEqual(len(json.loads(opening['evidence_index']['text'])),1)
        validate_bundle(packet,directory/'000001-eligible.json')
        ref.write_text(ref.read_text()+' ')
        with self.assertRaisesRegex(ValueError,'Reference evidence changed'):validate_bundle(packet,directory/'000001-eligible.json')
        bundle['items'][-1]['kind']='hf_file';bundle['items'][-1]['artifact_role']='non_weight'
        ref.write_text(json.dumps(bundle))
        with self.assertRaises(ValueError):load_bundle(self.repo,sha,ref)
        bundle['items']=[];bundle['selections'][0]['status']='no_eligible_revision';ref.write_text(json.dumps(bundle))
        self.assertEqual(load_bundle(self.repo,sha,ref)['items'],[])

    def test_moved_directory_and_unknown_location_fail_closed(self):
        self.git('mv','exllamav3/models','exllamav3/architecture')
        self.git('commit','-m','Move architecture directory')
        moved=self.git('rev-parse','HEAD')
        self.assertEqual(trigger(self.repo,moved)['class_files'],['exllamav3/architecture/base.py'])
        sha=self.add('exllamav3/architecture/extra.py','class ExtraConfig: pass\nclass ExtraModel: pass\n')
        self.assertEqual(trigger(self.repo,sha)['class_files'],['exllamav3/architecture/extra.py'])
        self.git('mv','exllamav3/architecture','exllamav3/unknown_location')
        self.git('commit','-m','Unknown architecture location')
        sha=self.git('rev-parse','HEAD')
        with self.assertRaisesRegex(ValueError,'Architecture location unknown'):trigger(self.repo,sha)
        with self.assertRaisesRegex(ValueError,'Architecture location unknown'):load_bundle(self.repo,sha,self.root/'absent')

    def test_root_without_model_classes_does_not_fail_location_check(self):
        # A root has no historical architecture location to preserve.
        from unittest.mock import patch
        with patch('teacher.architecture_evidence.git',return_value=b''),patch('teacher.architecture_evidence.inventory',return_value=(set(),{})):
            self.assertEqual(trigger(self.repo,'root'),{'architectures':[],'class_files':[]})
