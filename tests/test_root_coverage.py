# SPDX-License-Identifier: MIT
import json
import unittest
from teacher.worker import dispatch
from teacher.coverage import require_coverage
import test_teacher_packet


class CoverageTests(unittest.TestCase):
    setUp=test_teacher_packet.PacketTests.setUp
    tearDown=test_teacher_packet.PacketTests.tearDown

    def call(self, offset, maximum, identity='read'):
        args={'commit':self.task,'offset':offset,'max_bytes':maximum}
        result=dispatch(self.packet,'git_show',args)
        return [{'role':'assistant','calls':[{'id':identity,'tool':'git_show','arguments':args}]},
                {'role':'tool','name':'git_show','call_id':identity,'content':json.dumps({'ok':True,'result':result})}]

    def test_complete_section_is_not_reported_truncated_by_later_files(self):
        p=self.root/'multi';self.git('checkout','main')
        (self.repo/'z.py').write_text('tail=1\n');(self.repo/'a.py').write_text('value=3\n')
        self.git('add','.');self.git('commit','-m','Two files');task=self.git('rev-parse','HEAD')
        from teacher.packet import build_packet
        manifest=build_packet(self.repo,task,p);section=manifest['task_change_sections'][0]
        result=dispatch(p,'git_show',{'commit':task,'offset':section['offset'],'max_bytes':65536})
        self.assertFalse(result['truncated'])
        self.assertTrue(result['commit_truncated'])
        self.assertEqual(result['next_offset'],section['offset']+section['bytes'])
        self.assertEqual(result['section']['index'],0)

    def test_partial_and_overlapping_reads_do_not_satisfy_coverage(self):
        manifest=json.loads((self.packet/'manifest.json').read_text());section=manifest['task_change_sections'][0]
        manifest['authoring_task']={'kind':'chapter','id':'test','required_sections':[0],'required_evidence':[]}
        partial=self.call(section['offset'],10)
        with self.assertRaises(ValueError):require_coverage(manifest,partial)
        repeated=partial+self.call(section['offset'],10,'again')
        with self.assertRaises(ValueError):require_coverage(manifest,repeated)
        complete=partial+self.call(section['offset']+10,section['bytes']-10,'rest')
        report=require_coverage(manifest,complete)
        self.assertEqual(report['fully_read_sections'],[0])

    def test_success_flags_cannot_claim_bytes_not_returned(self):
        manifest=json.loads((self.packet/'manifest.json').read_text());section=manifest['task_change_sections'][0]
        manifest['authoring_task']={'kind':'chapter','id':'test','required_sections':[0],'required_evidence':[]}
        transcript=self.call(section['offset'],10)
        result=json.loads(transcript[-1]['content']);result['result']['next_offset']=section['offset']+section['bytes'];transcript[-1]['content']=json.dumps(result)
        with self.assertRaises(ValueError):require_coverage(manifest,transcript)

    def test_external_evidence_requires_complete_pagination(self):
        manifest=json.loads((self.packet/'manifest.json').read_text())
        manifest['authoring_task']={'kind':'chapter','id':'test','required_sections':[],'required_evidence':['paper']}
        manifest['evidence']=[{'source_id':'paper','kind':'web','url':'https://example.test/paper','content_bytes':8}]
        def read(offset,text,identity):
            return [{'role':'assistant','calls':[{'id':identity,'tool':'web_fetch','arguments':{'url':'https://example.test/paper','offset':offset}}]},
                {'role':'tool','name':'web_fetch','call_id':identity,'content':json.dumps({'ok':True,'result':{'encoding':'utf-8','text':text,'offset':offset,'next_offset':offset+len(text.encode())}})}]
        with self.assertRaises(ValueError):require_coverage(manifest,[])
        first=read(0,'abcd','first')
        with self.assertRaises(ValueError):require_coverage(manifest,first)
        self.assertEqual(require_coverage(manifest,first+read(4,'efgh','second'))['fully_read_evidence'],['paper'])

    def test_tensor_header_pages_require_all_tensors(self):
        manifest=json.loads((self.packet/'manifest.json').read_text())
        manifest['authoring_task']={'kind':'chapter','id':'test','required_sections':[],'required_evidence':['header']}
        locator={'repo_id':'org/model','revision':'a'*40,'path':'model.safetensors'}
        manifest['evidence']=[dict(locator,source_id='header',kind='safetensors_header',tensor_count=2)]
        def page(offset,key,identity):
            return [{'role':'assistant','calls':[{'id':identity,'tool':'safetensors_header','arguments':dict(locator,offset=offset)}]},
                {'role':'tool','name':'safetensors_header','call_id':identity,'content':json.dumps({'ok':True,'result':{'header':{key:{}}}})}]
        first=page(0,'a','first')
        with self.assertRaises(ValueError):require_coverage(manifest,first+page(0,'a','again'))
        self.assertEqual(require_coverage(manifest,first+page(1,'b','rest'))['fully_read_evidence'],['header'])

    def test_required_execution_rejects_no_run_and_failed_run(self):
        manifest=json.loads((self.packet/'manifest.json').read_text())
        manifest['authoring_task']={'required_sections':[],'required_evidence':[],'execution_required':True}
        with self.assertRaises(ValueError):require_coverage(manifest,[])
        calls=[{'role':'assistant','calls':[{'id':'compute','tool':'run','arguments':{}}]},
               {'role':'tool','name':'run','call_id':'compute','content':json.dumps({'ok':True,'result':{'returncode':1}})}]
        with self.assertRaises(ValueError):require_coverage(manifest,calls)
        calls[-1]['content']=json.dumps({'ok':True,'result':{'returncode':0,'timed_out':False}})
        self.assertEqual(require_coverage(manifest,calls)['successful_required_runs'],['compute'])
