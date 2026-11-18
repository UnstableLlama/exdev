"""One authorized reviewer-assisted attempt; only pointer coverage supplied."""
import os,sys,traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from teacher.cycle import ROOT,locked,read,write_json,digest,tracking_status,validate_run,make_summary,skeleton,write_new
from teacher.author import author
from teacher.session import FreshSession
from teacher.cycle_notify import notify
os.chdir(ROOT)
state_path=ROOT/'reports/teacher-walk-001.json'
packet=ROOT/'.teacher/retrieval/000255-003'
run=ROOT/'.teacher/runs/commit-000255-003'
reports=ROOT/'reports'
result_path=reports/'commit-000255-manual-003.result.json'
result=dict(position=255,result_path=str(result_path),status='manual_failed',returncode=1)
try:
 with locked(state_path):
  state=read(state_path)
  assert state['status']=='stopped_failure' and state['next_position']==255
  assert not state.get('advancement_pause') and not state.get('handover')
  assert not run.exists()
  assert read(packet/'manifest.json')['guidance_version']==12
  assert read(packet/'manifest.json')['coverage_request']['sha256']==digest(ROOT/'reviews/verdicts/commit-000255-003.coverage.md')
  record=dict(position=255,sha=read(packet/'manifest.json')['task_sha'],packet=str(packet.relative_to(ROOT)),run=str(run.relative_to(ROOT)),status='authoring',reviewer_assisted=True,recovery_verdict='reviews/verdicts/commit-000255-002.md',recovery_verdict_sha256=digest(ROOT/'reviews/verdicts/commit-000255-002.md'))
  state['runs'].append(record);state['status']='running';state.pop('error_type',None)
  write_json(state_path,state);tracking_status(state)
  try:
   author(packet,run,Path.home()/'.codex/auth.json')
   validation=validate_run(run,packet,ROOT/'.sources/exllamav3.git',ROOT/'data/evidence/github',255)
   vp=reports/'commit-000255-validation-003.json';write_new(vp,validation)
   summary=make_summary(run,packet,ROOT/'.sources/exllamav3.git',255,vp,reports/'commit-000255-catalog-selection-001.json',ROOT/'data/evidence/github')
   sp=reports/'commit-000255-cycle-003.json';write_new(sp,summary)
   sk=reports/'commit-000255-003.skeleton.md'
   with sk.open('x') as f:f.write(skeleton(summary,os.environ['CODEX_THREAD_ID']))
   record.update(validation['assessment']);record['status']='awaiting_review_request'
   state['status']='awaiting_review_request';state['handover']=dict(full_review=record['run'],sampled_mechanical=[])
   write_json(state_path,state);tracking_status(state)
   result.update(status='awaiting_review_request',returncode=0,summary=str(sp.relative_to(ROOT)),skeleton=str(sk.relative_to(ROOT)),draft=str((run/'draft.md').relative_to(ROOT)))
  except BaseException as e:
   record['status']='failed';state.update(status='stopped_failure',error_type=type(e).__name__)
   write_json(state_path,state);tracking_status(state)
   raise
except BaseException as e:
 result.update(error_type=type(e).__name__,detail=str(e));traceback.print_exc()
finally:
 write_json(result_path,result)
 notify(os.environ['CODEX_THREAD_ID'],result,reports,255)
