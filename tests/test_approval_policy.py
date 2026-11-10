# SPDX-License-Identifier: MIT
import json
from pathlib import Path
import tempfile
import unittest
from teacher.approval_policy import tier, sampled, reject_sample, assess, approve_mechanical
from teacher.coverage import run_coverage
from teacher.author import write_json
import test_ancestor_context


class PolicyTests(unittest.TestCase):
    def test_paths_and_mixed_commit(self):
        annotation={'findings':[],'chapters':[]}
        for path in ('README.md','doc/page.txt','image.png','.gitignore','.github/workflows/test.yml','LICENSE','NOTICE'):
            self.assertEqual(tier(['parent'],[path],annotation,True)['tier'],'mechanical',path)
        for path in ('requirements.txt','doc/requirements-dev.txt','setup.py','doc/example.py','.github/test.json','a.cu','a.cuh','a.cpp','a.h','a.json'):
            self.assertEqual(tier(['parent'],['README.md',path],annotation,True)['tier'],'full_review',path)
        for parents,a,valid in (([],annotation,True),(['a','b'],annotation,True),(['a'],{'findings':[{}]},True),
                                 (['a'],{'findings':[],'chapters':[{'claims':[{'basis':'execution'}]}]},True),(['a'],annotation,False)):
            self.assertEqual(tier(parents,['README.md'],a,valid)['tier'],'full_review')

    def test_sample_threshold(self):
        self.assertTrue(sampled('19'+'0'*38));self.assertTrue(sampled('00'+'f'*38))
        self.assertFalse(sampled('1a'+'0'*38));self.assertFalse(sampled('ff'+'0'*38))

    def test_rejection_invalidates_every_later_run_and_blocks_resume(self):
        from teacher.walk import resume
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);records=[]
            for i in range(4):
                run=root/str(i);run.mkdir();write_json(run/'review.json',{'status':'approved','ancestor_context_approved':True})
                records.append({'run':str(run),'tier':'mechanical','sampled':i==1})
            p=root/'state.json';write_json(p,{'status':'ready','runs':records})
            result=reject_sample(p,records[1]['run'],'Rejected by reviewer')
            self.assertEqual(result['status'],'stopped_rejection')
            self.assertEqual(json.loads((root/'0/review.json').read_text())['status'],'approved')
            for i in (2,3):
                r=json.loads((root/str(i)/'review.json').read_text())
                self.assertEqual(r['status'],'needs_reauthoring');self.assertFalse(r['ancestor_context_approved'])
            with self.assertRaises(ValueError):resume(p,root/'unused-auth')


class MetricsTests(unittest.TestCase):
    setUp=test_ancestor_context.AncestorContextTests.setUp
    tearDown=test_ancestor_context.AncestorContextTests.tearDown
    run_fixture=test_ancestor_context.AncestorContextTests.run_fixture

    def test_report_only_targets_and_multiple_read_pages(self):
        import hashlib
        m=json.loads((self.packet/'manifest.json').read_text())
        rows=[{'sha':self.first,'chapter':'one','file':'a.py'}, {'sha':self.first,'chapter':'one','file':'a.py'},
              {'sha':self.first,'chapter':'two','file':'unrelated.py'}]
        raw=json.dumps(rows).encode();digest=hashlib.sha256(raw).hexdigest();(self.packet/'blobs'/digest).write_bytes(raw);m['ancestor_search_blob']=digest
        t=[]
        for i in range(2):
            t.extend([{'role':'assistant','calls':[{'id':str(i),'tool':'ancestor_read','arguments':{'mode':'content','commit':self.first,'chapter':'one'}}]},
                      {'role':'tool','name':'ancestor_read','call_id':str(i),'content':json.dumps({'ok':True})}])
        report=run_coverage(self.packet,m,t)['retrieval_usage']
        self.assertTrue(report['report_only']);self.assertEqual(report['matching_target_count'],1)
        self.assertEqual(report['ancestor_prose_read_count'],2)
        self.assertEqual(run_coverage(self.packet,m,[])['retrieval_usage']['ancestor_prose_read_count'],0)

    def mechanical_fixture(self):
        import hashlib
        from teacher.worker import dispatch
        from teacher.editorial import assemble_draft,render
        (self.repo/'README.md').write_text('Documentation fixture\n');self.git('add','README.md');self.git('commit','-m','Docs')
        sha=self.git('rev-parse','HEAD');run,packet=self.run_fixture(sha)
        m=json.loads((packet/'manifest.json').read_text());m['editorial_schema_version']=4;write_json(packet/'manifest.json',m)
        a=json.loads((run/'draft.json').read_text())['annotation'];a.update(schema_version=4,findings=[],summary='Test overview')
        t=json.loads((run/'raw-transcript.json').read_text());t[1]['content']=json.dumps({'ok':True,'result':dispatch(packet,'git_show',{'commit':sha})})
        d,r=assemble_draft(a,m,t);write_json(run/'draft.json',d);write_json(run/'review.json',r);write_json(run/'raw-transcript.json',t)
        (run/'draft.md').write_text(render(d));write_json(run/'coverage.json',run_coverage(packet,m,t))
        provenance=json.loads((run/'provenance.json').read_text());provenance['packet_manifest_sha256']=hashlib.sha256((packet/'manifest.json').read_bytes()).hexdigest();write_json(run/'provenance.json',provenance)
        return run,packet

    def test_mechanical_approval_uses_policy_identity_and_scoped_flags(self):
        run,packet=self.mechanical_fixture()
        self.assertEqual(assess(run,packet,self.repo)['tier'],'mechanical')
        approve_mechanical(run,packet,self.repo)
        review=json.loads((run/'review.json').read_text())
        self.assertEqual(review['reviewer'],'exdev-mechanical-ancestor/v1')
        self.assertTrue(review['ancestor_context_approved']);self.assertFalse(review['canonical_approved']);self.assertFalse(review['training_eligible'])
        self.assertEqual(review['approval_kind'],'mechanical')

    def test_mechanical_approval_rejects_coverage_or_replay_tampering(self):
        run,packet=self.mechanical_fixture()
        p=run/'coverage.json';old=p.read_bytes();write_json(p,{'task_read_complete':True})
        with self.assertRaises(ValueError):approve_mechanical(run,packet,self.repo)
        p.write_bytes(old);p=run/'draft.md';p.write_text('Changed prose')
        with self.assertRaises(ValueError):approve_mechanical(run,packet,self.repo)
        self.assertEqual(json.loads((run/'review.json').read_text())['status'],'pending')
