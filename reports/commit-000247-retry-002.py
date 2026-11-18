"""One authorized administrative retry; no recovery details supplied to teacher."""
import os,sys,traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from teacher.cycle import ROOT,locked,read,write_json,digest,tracking_status,validate_run,make_summary,skeleton,write_new
from teacher.author import author
from teacher.session import FreshSession
from teacher.cycle_notify import notify
os.chdir(ROOT)
state_path=ROOT/'reports/teacher-walk-001.json'
packet=ROOT/'.teacher/retrieval/000247-002'
run=ROOT/'.teacher/runs/commit-000247-002'
reports=ROOT/'reports'
result_path=reports/'commit-000247-manual-002.result.json'
result=dict(position=247,result_path=str(result_path),status='manual_failed',returncode=1)
try:
 with locked(state_path):
  state=read(state_path)
  assert state['status']=='stopped_failure' and state['next_position']==247
  assert not state.get('advancement_pause') and not state.get('handover')
  assert not run.exists()
  from teacher.walk_inputs import prepare,validate_bundle
  from teacher.graph_packet import attach_graphs
  from teacher.ancestor_context import attach_entries
  coverage=ROOT/'reviews/verdicts/commit-000247-002.coverage.md'
  manifest=prepare(ROOT/'.sources/exllamav3.git','dcae5a04be7885ad9dc9a6cfcb135ead75847695',247,packet,ROOT/'data/evidence/github',coverage_request=coverage,coverage_sha256='832c779e41c41902370595e6fcaca0fe5025b6decef9bb06448c673ff30776dc')
  attach_graphs(packet,ROOT/'store')
  sources=[ROOT/p for p in state['approved_entries']]
  selected=[p for p in sources if read(p/('entry.json' if (p/'entry.json').exists() else 'draft.json'))['sha'] in manifest['commits']]
  attach_entries(packet,selected)
  validate_bundle(packet,ROOT/'data/evidence/github/000247-eligible.json')
  assert read(packet/'manifest.json')['guidance_version']==11
  assert read(packet/'manifest.json').get('coverage_request')
  record=dict(position=247,sha=read(packet/'manifest.json')['task_sha'],packet=str(packet.relative_to(ROOT)),run=str(run.relative_to(ROOT)),status='authoring',reviewer_assisted=True,recovery_verdict='reviews/verdicts/commit-000247-001.md',recovery_verdict_sha256=digest(ROOT/'reviews/verdicts/commit-000247-001.md'))
  state['runs'].append(record);state['status']='running';state.pop('error_type',None)
  write_json(state_path,state);tracking_status(state)
  try:
   author(packet,run,Path.home()/'.codex/auth.json')
   validation=validate_run(run,packet,ROOT/'.sources/exllamav3.git',ROOT/'data/evidence/github',247)
   vp=reports/'commit-000247-validation-002.json';write_new(vp,validation)
   summary=make_summary(run,packet,ROOT/'.sources/exllamav3.git',247,vp,reports/'commit-000247-catalog-selection-001.json',ROOT/'data/evidence/github')
   sp=reports/'commit-000247-cycle-002.json';write_new(sp,summary)
   sk=reports/'commit-000247-002.skeleton.md'
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
 notify(os.environ['CODEX_THREAD_ID'],result,reports,247)
