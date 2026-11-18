"""Administrative compatibility check; no provider or teacher invoked."""
import importlib.util,json,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'tests'))
from test_walk_inputs import WalkInputTests
from teacher.session import FreshSession,GUIDANCE_11_ADDITION,GUIDANCE_12_ADDITION,GUIDANCE_10_ADDITION
from teacher.walk_inputs import prepare,validate_bundle
spec=importlib.util.spec_from_file_location('teacher._guidance12_before','reports/guidance-12-before-session.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
f=WalkInputTests();f.setUp();report={}
try:
 directory=f.bundle();packet=f.root/'trial-gate';m=prepare(f.repo,f.task,9,packet,directory)
 assert m['guidance_version']==11
 report['default']=11;report['versions']={}
 for v in range(5,12):
  m['guidance_version']=v;(packet/'manifest.json').write_text(json.dumps(m))
  a=old.FreshSession(packet);b=FreshSession(packet)
  assert (a.initial,a.tools,a.reasoning_effort)==(b.initial,b.tools,b.reasoning_effort)
  report['versions'][v]={'byte_identical':True,'system_sha256':hashlib.sha256(b.initial[0]['content'].encode()).hexdigest()}
  if v==11:eleven=b
 m['guidance_version']=12;(packet/'manifest.json').write_text(json.dumps(m));validate_bundle(packet,directory/'000009-eligible.json');twelve=FreshSession(packet)
 expected=Path('reviews/verdicts/guidance-12-trial.decision.md').read_text().split('**F (revised; the added sentence is the third).**\n')[1].split('\n\n')[0]
 assert GUIDANCE_12_ADDITION==expected
 assert twelve.initial[0]['content']==eleven.initial[0]['content'].removesuffix(GUIDANCE_11_ADDITION)+expected
 assert GUIDANCE_10_ADDITION not in twelve.initial[0]['content']
 assert (twelve.initial[1:],twelve.tools,twelve.reasoning_effort)==(eleven.initial[1:],eleven.tools,eleven.reasoning_effort)
 report['twelve']={'exact_eleven_revised_f':True,'non_system_unchanged':True,'validated':True}
finally:f.tearDown()
Path('reports/guidance-12-verification-001.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
