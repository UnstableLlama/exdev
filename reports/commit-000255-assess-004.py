"""Post-author assessment, authorized by the two bound recovery verdicts; no teacher session."""
import os,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from teacher.cycle import *
from teacher.codex_adapter import require_approval_model
from teacher.validation_repair import disclosure
os.chdir(ROOT)
run=ROOT/'.teacher/runs/commit-000255-004';packet=ROOT/'.teacher/retrieval/000255-004'
state_path=ROOT/'reports/teacher-walk-001.json'
old='08ee8fa35a6dbf1cb2e3fddeea9ab89f92652d95668f5cfeedc1581cc0e9b8c3'
new='d6ce4f8944287bd1ef9cf42fbddba342597efa8122c19761e3ce66b4f44e27a4'
with locked(state_path):
 state=read(state_path)
 assert state['status']=='stopped_failure' and state['next_position']==255 and not state.get('handover')
 before={str(p.relative_to(ROOT)):digest(p) for p in [*(run/n for n in ('draft.json','draft.md','raw-transcript.json','provenance.json','coverage.json','review.json','status.json')),packet/'manifest.json']}
 expected=dict(re.findall(r'^- ([^:]+): `([0-9a-f]{64})`',(ROOT/'reviews/requests/commit-000255-004.md').read_text(),re.M))
 assert all(expected[p]==h for p,h in before.items())
 m=read(packet/'manifest.json');p=read(run/'provenance.json');t=read(run/'raw-transcript.json')
 validate_bundle(packet,ROOT/'data/evidence/github/000255-eligible.json')
 decision=assess(run,packet,ROOT/'.sources/exllamav3.git')
 require_approval_model(run,p)
 assert p['packet_manifest_sha256']==digest(packet/'manifest.json')
 differences=[]
 for file,expected_hash in p['implementation_sha256'].items():
  actual=digest(ROOT/file)
  if actual!=expected_hash:
   assert (file,expected_hash,actual)==('teacher/validation_repair.py',old,new)
   differences.append(dict(path=file,authored_sha256=expected_hash,assessment_sha256=actual,acceptance='reviews/verdicts/validation-repair-implementation-003.md'))
 assert len(differences)==1
 cov=m['coverage_request'];assert p['reviewer_assisted'] and p['coverage_request']=={k:cov[k] for k in ('path','sha256')}
 blobs=list((packet/'blobs').iterdir())
 for b in blobs:assert digest(b)==b.name and not b.stat().st_mode&0o222 and os.path.samefile(b,store_root(packet)/b.name)
 calls={c['id']:c for x in t if x.get('role')=='assistant' for c in x.get('calls',[])}
 counts=Counter();runner=Runner(packet)
 for result in t:
  if result.get('role')=='tool':
   replay_result(runner,calls[result['call_id']],result);counts[result['name']]+=1
 coverage=read(run/'coverage.json')
 validation=dict(status='validated',assessment=decision,validation_repair_details=disclosure(t),packet_implementation_blob_hashes_verified=True,accepted_implementation_differences=differences,teacher_model=p['model'],reasoning_effort=p['reasoning_effort'],reviewer_assisted=True,tool_counts=dict(counts),identical_replayed_calls=sum(counts.values()),shared_readonly_blob_links_verified=len(blobs),open_catalog_rows=len(m['unreferenced_discussion_catalog']),closed_catalog_rows=len(m['closed_discussion_catalog']['rows']),task_sections_total=coverage['task_sections_total'],fully_read_task_sections=coverage['fully_read_task_sections'],ancestor_prose_read_count=coverage.get('retrieval_usage',{}).get('ancestor_prose_read_count'),runtime={k:p[k] for k in ('codex_version','python_version','machine_architecture','operating_system')})
 after={file:digest(ROOT/file) for file in before};assert before==after
 validation['run_artifacts_before']=before;validation['run_artifacts_after']=after;validation['assessment_written_run_files']=[]
 vp=ROOT/'reports/commit-000255-validation-004.json';write_new(vp,validation)
 summary=make_summary(run,packet,ROOT/'.sources/exllamav3.git',255,vp,ROOT/'reports/commit-000255-catalog-selection-001.json',ROOT/'data/evidence/github')
 write_new(ROOT/'reports/commit-000255-cycle-004.json',summary)
 (ROOT/'reports/commit-000255-004.skeleton.md').write_text(skeleton(summary,'01a1da07-7653-7b81-8507-f69683828acb'))
 record=next(r for r in reversed(state['runs']) if r['run']==str(run.relative_to(ROOT)))
 record.update(decision);record['status']='awaiting_review_request'
 record['post_author_assessment_acceptance']='reviews/verdicts/validation-repair-implementation-003.md'
 record['post_author_assessment_acceptance_sha256']=digest(ROOT/record['post_author_assessment_acceptance'])
 state.update(status='awaiting_review_request',handover=dict(full_review=record['run'],sampled_mechanical=[]));state.pop('error_type',None)
 write_json(state_path,state);tracking_status(state)
 print('Assessment and replay passed; all eight run/manifest bindings unchanged; awaiting review request.')
