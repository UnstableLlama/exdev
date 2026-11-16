"""Administrative verification only; never invokes a teacher/provider."""
import hashlib,json,os,shutil,tempfile
from pathlib import Path
from teacher.session import FreshSession,GUIDANCE_9_ADDITION,GUIDANCE_10_ADDITION
from teacher.walk_inputs import validate_bundle
sessions={}
for v in (8,9):
 b=json.loads(Path(f'reports/guidance-10-v{v}-before.json').read_text())
 s=FreshSession(b['packet'])
 assert b==dict(packet=b['packet'],initial=s.initial,tools=s.tools,reasoning_effort=s.reasoning_effort)
 sessions[v]=s
expected=Path('reviews/verdicts/guidance-10-trial.decision.md').read_text().split('**E, revised.**\n')[1].split('\n\n')[0]
assert GUIDANCE_10_ADDITION==expected
old=Path('reviews/verdicts/guidance-9-trial.decision.md').read_text().split('**E. Removed or bypassed protection.**\n')[1].split('\n\n')[0]
assert GUIDANCE_9_ADDITION==old
b=json.loads(Path('reports/guidance-10-v8-before.json').read_text())
with tempfile.TemporaryDirectory(prefix='guidance10-',dir='reports') as tmp:
 p=Path(tmp)/'packet';shutil.copytree(b['packet'],p,copy_function=os.link)
 mp=p/'manifest.json';m=json.loads(mp.read_text());assert m['guidance_version']==8
 m['guidance_version']=10;mp.unlink();mp.write_text(json.dumps(m))
 validate_bundle(p,Path('data/evidence/github/000195-eligible.json'))
 s=FreshSession(p)
 assert s.initial[0]['content']==sessions[8].initial[0]['content']+'\n\n'+expected
 assert GUIDANCE_9_ADDITION not in s.initial[0]['content']
 assert s.initial[1:]==sessions[8].initial[1:]
 assert s.tools==sessions[8].tools and s.reasoning_effort==sessions[8].reasoning_effort
for v in (5,6):
 b=json.loads(Path(f'reports/guidance-7-v{v}-before.json').read_text());s=FreshSession(b['packet'])
 assert b==dict(packet=b['packet'],initial=s.initial,tools=s.tools,reasoning_effort=s.reasoning_effort)
r=dict(v8_byte_identical=True,v9_byte_identical=True,legacy_v5_v6_byte_identical=True,v10_exact_decision=True,v9_exact_original_decision=True,v10_bundle_validated=True,non_system_inputs_identical=True,walk_default=8,provider_invoked=False,original_packets_modified=False,paragraph_sha256=hashlib.sha256(expected.encode()).hexdigest())
Path('reports/guidance-10-implementation-001.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
