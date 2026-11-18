"""Administrative compatibility check; no provider or teacher invoked."""
import importlib.util,json,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tests'))
from test_walk_inputs import WalkInputTests
from teacher.session import FreshSession,GUIDANCE_11_ADDITION,GUIDANCE_10_ADDITION
from teacher.walk_inputs import prepare,validate_bundle
spec=importlib.util.spec_from_file_location('teacher._guidance11_before','reports/guidance-11-before-session.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
f=WalkInputTests();f.setUp();report={}
try:
 directory=f.bundle();packet=f.root/'trial-gate';m=prepare(f.repo,f.task,9,packet,directory)
 assert m['guidance_version']==9
 report['default']=9;report['versions']={}
 for v in range(5,11):
  m['guidance_version']=v;(packet/'manifest.json').write_text(json.dumps(m))
  a=old.FreshSession(packet);b=FreshSession(packet)
  assert (a.initial,a.tools,a.reasoning_effort)==(b.initial,b.tools,b.reasoning_effort)
  report['versions'][v]={'byte_identical':True,'system_sha256':hashlib.sha256(b.initial[0]['content'].encode()).hexdigest()}
  if v==9:nine=b
 m['guidance_version']=11;(packet/'manifest.json').write_text(json.dumps(m));validate_bundle(packet,directory/'000009-eligible.json');eleven=FreshSession(packet)
 expected=Path('reviews/verdicts/guidance-11-trial.decision.md').read_text().split('**F (proposed).**\n')[1].split('\n\n')[0]
 assert GUIDANCE_11_ADDITION==expected
 assert eleven.initial[0]['content']==nine.initial[0]['content']+'\n\n'+expected
 assert GUIDANCE_10_ADDITION not in eleven.initial[0]['content']
 assert (eleven.initial[1:],eleven.tools,eleven.reasoning_effort)==(nine.initial[1:],nine.tools,nine.reasoning_effort)
 report['eleven']={'exact_nine_plus_f':True,'non_system_unchanged':True,'validated':True}
finally:f.tearDown()
Path('reports/guidance-11-verification-001.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
