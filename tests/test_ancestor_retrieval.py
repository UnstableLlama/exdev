# SPDX-License-Identifier: MIT
import base64
import hashlib
import json
import os
import unittest
from copy import deepcopy
from teacher.ancestor_context import approve_run, attach_entries
from teacher.editorial import validate_annotation, output_schema, validate_shape
from teacher.session import FreshSession
from teacher.worker import dispatch
import test_ancestor_context
import test_assembly


class RetrievalTests(unittest.TestCase):
    setUp=test_ancestor_context.AncestorContextTests.setUp
    tearDown=test_ancestor_context.AncestorContextTests.tearDown
    run_fixture=test_ancestor_context.AncestorContextTests.run_fixture

    def prepare(self):
        run,source=self.run_fixture()
        approve_run(run,source,'TEST REVIEWER','ADMIN_REVIEW_SECRET')
        p=self.packet/'manifest.json';m=json.loads(p.read_text());m['ancestor_context_mode']='retrieval_v1';p.write_text(json.dumps(m))
        attach_entries(self.packet,[run])
        return run,json.loads(p.read_text())

    def test_prose_only_export_and_citable_reads(self):
        run,m=self.prepare()
        result=dispatch(self.packet,'ancestor_read',{'mode':'content','commit':self.first})
        self.assertNotIn('evidence',result['text']);self.assertNotIn('read"',result['text'])
        self.assertIn('APPROVED TEST FIXTURE',result['text'])
        self.assertNotIn(b'ADMIN_REVIEW_SECRET',b''.join(p.read_bytes() for p in self.packet.rglob('*') if p.is_file()))
        a=json.loads((run/'draft.json').read_text())['annotation'];a['problem'][0]['evidence']=['current']
        def transcript(mode):
            return [{'role':'assistant','calls':[{'id':'current','tool':'ancestor_read','arguments':{'mode':mode,'commit':self.first}}]},
                    {'role':'tool','name':'ancestor_read','call_id':'current','content':json.dumps({'ok':True,'result':result})}]
        validate_annotation(a,m,transcript('content'))
        with self.assertRaises(ValueError):validate_annotation(a,m,transcript('catalog'))
        a['problem'][0]['basis']='execution'
        with self.assertRaises(ValueError):validate_annotation(a,m,transcript('content'))
        a['problem'][0].update(basis='source',evidence=['ancestor:'+self.first])
        with self.assertRaises(ValueError):validate_annotation(a,m,[])

    def test_paging_and_closed_boundary(self):
        self.prepare();chunks=[];offset=0
        while True:
            r=dispatch(self.packet,'ancestor_read',{'mode':'content','commit':self.first,'offset':offset,'max_bytes':7})
            chunks.append(r['text'].encode() if r['encoding']=='utf-8' else base64.b64decode(r['base64']))
            offset=r['next_offset']
            if not r['truncated']:break
        self.assertEqual(hashlib.sha256(b''.join(chunks)).hexdigest(),r['content_sha256'])
        for args in ({'mode':'invalid'},{'mode':'content','commit':self.task},
                     {'mode':'content','commit':self.side},{'mode':'content','commit':self.future},
                     {'mode':'content','commit':self.first,'chapter':'../review.json'},
                     {'mode':'content','commit':self.first,'offset':100000000},
                     {'mode':'catalog','max_bytes':16385}):
            with self.assertRaises(ValueError):dispatch(self.packet,'ancestor_read',args)

    def test_catalog_is_bounded_across_full_history(self):
        _,m=self.prepare()
        # Synthetic scale fixture only: 2,264 ancestor refs, never a real approval.
        template=m['ancestor_entries'][0];refs=[];commits={}
        for i in range(2264):
            sha=f'{i:040x}';refs.append(dict(template,sha=sha));commits[sha]=m['commits'][self.first]
        raw=json.dumps([{'sha':r['sha'],'title':'SYNTHETIC TEST CATALOG'} for r in refs]).encode()
        digest=hashlib.sha256(raw).hexdigest();(self.packet/'blobs'/digest).write_bytes(raw)
        m.update(ancestor_entries=refs,commits=commits,history_order=list(commits),ancestor_catalog_blob=digest)
        (self.packet/'manifest.json').write_text(json.dumps(m))
        task=json.loads(FreshSession(self.packet).initial[1]['content'])
        self.assertNotIn('ancestor_entries',task)
        self.assertLessEqual(len(task['ancestor_catalog']['text'].encode()),8192)
        self.assertTrue(task['ancestor_catalog']['truncated'])
        page=dispatch(self.packet,'ancestor_read',{'mode':'catalog','offset':task['ancestor_catalog']['next_offset']})
        self.assertEqual(page['offset'],8192)
        (self.packet/'blobs'/digest).write_text('tampered')
        with self.assertRaises(ValueError):FreshSession(self.packet)

    def test_schema_four_requires_short_summary_and_renders_it(self):
        from teacher.editorial import render
        run,m=self.prepare();a=json.loads((run/'draft.json').read_text())['annotation']
        m['editorial_schema_version']=4;a.update(schema_version=4,findings=[])
        with self.assertRaises(ValueError):validate_shape(a,output_schema(m))
        a['summary']='A concise historical overview.';validate_shape(a,output_schema(m))
        self.assertIn(a['summary'],render({'sha':self.first,'annotation':a}))
        a['summary']='x'*1001
        with self.assertRaises(ValueError):validate_shape(a,output_schema(m))

    def test_later_commit_symbols_come_from_scoped_graph_events(self):
        from teacher.packet import build_packet
        first,source=self.run_fixture();approve_run(first,source,'reviewer','fixture')
        second,source=self.run_fixture(self.task);approve_run(second,source,'reviewer','fixture')
        packet=self.root/'later';m=build_packet(self.repo,self.future,packet);m['ancestor_context_mode']='retrieval_v1'
        events=[{'sha':self.task,'file':'a.py','qn':'Fixture.changed'}]
        raw=json.dumps(events).encode();digest=hashlib.sha256(raw).hexdigest();(packet/'blobs'/digest).write_bytes(raw)
        m['graphs']={self.task:{'events':digest}};(packet/'manifest.json').write_text(json.dumps(m))
        attach_entries(packet,[first,second])
        result=dispatch(packet,'ancestor_read',{'mode':'search','symbol':'Fixture.changed'})
        self.assertEqual([r['sha'] for r in result['matches']],[self.task])
        self.assertEqual(result['matches'][0]['match_basis'],['graph_symbol_event'])
        self.assertEqual(result['graph_indexed_ancestors'],1);self.assertEqual(result['total_ancestors'],2)
        catalog=json.loads(dispatch(packet,'ancestor_read',{'mode':'catalog'})['text'])
        self.assertEqual([r['sha'] for r in catalog],[self.task,self.first])
        page=dispatch(packet,'ancestor_read',{'mode':'search','file':'a.py','limit':1})
        self.assertEqual(page['matches'][0]['sha'],self.task);self.assertTrue(page['truncated'])
        self.assertEqual(page['matches'][0]['match_count'],2)
        next_page=dispatch(packet,'ancestor_read',{'mode':'search','file':'a.py','limit':1,'offset':page['next_offset']})
        self.assertEqual(next_page['matches'][0]['sha'],self.first)


    def test_links_require_successful_nonempty_content_read(self):
        run,m=self.prepare();a=json.loads((run/'draft.json').read_text())['annotation']
        a['problem']=[];a['links']=[self.first]
        with self.assertRaises(ValueError):validate_annotation(a,m,[])
        args={'mode':'content','commit':self.first}
        result=dispatch(self.packet,'ancestor_read',args)
        transcript=[{'role':'assistant','calls':[{'id':'read','tool':'ancestor_read','arguments':args}]},
                    {'role':'tool','name':'ancestor_read','call_id':'read','content':json.dumps({'ok':True,'result':result})}]
        validate_annotation(a,m,transcript)
        for response in ({'ok':False}, {'ok':True,'result':dict(result,next_offset=result['offset'])},
                         {'ok':True,'result':dict(result,kind='ancestor_catalog')}):
            transcript[1]['content']=json.dumps(response)
            with self.assertRaises(ValueError):validate_annotation(a,m,transcript)

    def test_search_is_mechanical_paged_and_not_claim_evidence(self):
        run,m=self.prepare()
        rows=[{'sha':self.first,'chapter':'','file':'a.py','symbol':'Job.receive_sample','match_basis':'graph_symbol_event'},
              {'sha':self.first,'chapter':'','file':'a.py','symbol':'Job.next','match_basis':'graph_symbol_event'}]
        raw=json.dumps(rows).encode();digest=hashlib.sha256(raw).hexdigest();(self.packet/'blobs'/digest).write_bytes(raw)
        m['ancestor_search_blob']=digest;(self.packet/'manifest.json').write_text(json.dumps(m))
        r=dispatch(self.packet,'ancestor_read',{'mode':'search','file':'a.py','symbol':'Job.','limit':1})
        self.assertEqual(len(r['matches']),1);self.assertFalse(r['truncated']);self.assertEqual(r['next_offset'],1)
        self.assertEqual(r['matches'][0]['match_count'],2)
        r2=dispatch(self.packet,'ancestor_read',{'mode':'search','symbol':'Job.','offset':1})
        self.assertEqual(r2['matches'],[])
        self.assertEqual(dispatch(self.packet,'ancestor_read',{'mode':'search','symbol':'Future'})['matches'],[])
        a=json.loads((run/'draft.json').read_text())['annotation'];a['problem'][0]['evidence']=['search']
        transcript=[{'role':'assistant','calls':[{'id':'search','tool':'ancestor_read','arguments':{'mode':'search','file':'a.py'}}]},
                    {'role':'tool','name':'ancestor_read','call_id':'search','content':json.dumps({'ok':True,'result':r})}]
        with self.assertRaises(ValueError):validate_annotation(a,m,transcript)
        rows[0]['sha']=self.future;raw=json.dumps(rows).encode();digest=hashlib.sha256(raw).hexdigest()
        (self.packet/'blobs'/digest).write_bytes(raw);m['ancestor_search_blob']=digest;(self.packet/'manifest.json').write_text(json.dumps(m))
        with self.assertRaises(ValueError):dispatch(self.packet,'ancestor_read',{'mode':'search','file':'a.py'})

    @unittest.skipUnless(os.environ.get('EXDEV_SANDBOX_TESTS')=='1','host sandbox opt-in')
    def test_isolated_retrieval(self):
        from teacher.runner import Runner
        self.prepare();r=Runner(self.packet).invoke('ancestor_read',{'mode':'content','commit':self.first})
        self.assertTrue(r['ok']);self.assertEqual(r['result']['sha'],self.first)


class AssemblyApprovalTests(unittest.TestCase):
    setUp=test_assembly.AssemblyTests.setUp
    write=test_assembly.AssemblyTests.write
    digest=test_assembly.AssemblyTests.digest

    def test_approval_replays_assembly_and_export_binds_artifacts(self):
        from teacher.assembly import save
        from teacher.retrieval import approve_assembly
        for name,value in [('selection',self.selection),('packets',self.packets),('plan',self.plan)]:self.write(self.root/(name+'.json'),value)
        paths=[self.root/(name+'.json') for name in ('selection','packets','plan')]
        out=self.root/'assembled';entry=save(*paths,out,root=self.root)
        md=out/'entry.md';old=md.read_bytes();md.write_bytes(old+b'bad')
        with self.assertRaises(ValueError):approve_assembly(out,*paths,'reviewer','note',root=self.root)
        md.write_bytes(old)
        review=approve_assembly(out,*paths,'reviewer','ADMIN_REVIEW_SECRET',root=self.root)
        self.assertTrue(review['ancestor_context_approved']);self.assertFalse(review['training_eligible'])
        packet=self.root/'retrieval';(packet/'blobs').mkdir(parents=True)
        patch=b'diff --git a/one.py b/one.py';digest=hashlib.sha256(patch).hexdigest();(packet/'blobs'/digest).write_bytes(patch)
        m={'ancestor_context_mode':'retrieval_v1','history_order':[self.sha],
           'commits':{self.sha:{'parents':[],'date':entry['cutoff_date'],'message':'Root','files':['one.py','two.py']}},'shows':{self.sha:digest}}
        snapshot={'sha':self.sha,'parents':[],'nodes':[{'file':'two.py','qn':'TEST.Symbol'}]}
        raw=json.dumps(snapshot).encode();digest=hashlib.sha256(raw).hexdigest();(packet/'blobs'/digest).write_bytes(raw)
        m['graphs']={self.sha:{'snapshot':digest}}
        self.write(packet/'manifest.json',m);attach_entries(packet,[out])
        hits=dispatch(packet,'ancestor_read',{'mode':'search','file':'two.py'})['matches']
        self.assertTrue(hits);self.assertTrue(all(h['chapter']=='two' for h in hits))
        symbol=dispatch(packet,'ancestor_read',{'mode':'search','symbol':'TEST.Symbol'})['matches']
        self.assertEqual(symbol[0]['chapter'],'two')
        self.assertEqual(symbol[0]['match_basis'],['root_graph_symbol_file_join'])
        result=dispatch(packet,'ancestor_read',{'mode':'content','commit':self.sha,'chapter':'two'})
        self.assertIn('TEST FIXTURE ONLY two',result['text']);self.assertNotIn('same-read-id',result['text'])
        m.pop('ancestor_context_complete',None);self.write(packet/'manifest.json',m);md.write_bytes(old+b'bad')
        with self.assertRaises(ValueError):attach_entries(packet,[out])
