"""Administrative gate verification; no teacher/provider invoked."""
import hashlib,json,os,shutil,tempfile
from pathlib import Path
from teacher.session import FreshSession,GUIDANCE_8_ADDITION
from teacher.walk_inputs import validate_bundle
baseline=json.loads(Path('reports/guidance-8-v7-before.json').read_text())
s=FreshSession(baseline['packet'])
assert baseline==dict(packet=baseline['packet'],initial=s.initial,tools=s.tools,reasoning_effort=s.reasoning_effort)
validate_bundle(Path(baseline['packet']),Path('data/evidence/github/000174-eligible.json'))
d=Path('reviews/verdicts/guidance-8-trial.decision.md').read_text()
expected=d.split('**D. Existing mechanisms called from a new place.**\n')[1].split('\n\n')[0]
assert GUIDANCE_8_ADDITION==expected
with tempfile.TemporaryDirectory(prefix='guidance8-',dir='reports') as tmp:
 p=Path(tmp)/'packet';shutil.copytree(baseline['packet'],p,copy_function=os.link)
 mp=p/'manifest.json';m=json.loads(mp.read_text());assert m['guidance_version']==7
 m['guidance_version']=8;mp.unlink();mp.write_text(json.dumps(m))
 validate_bundle(p,Path('data/evidence/github/000174-eligible.json'))
 trial=FreshSession(p)
 assert trial.initial[0]['content']==s.initial[0]['content']+'\n\n'+expected
 assert trial.initial[1:]==s.initial[1:]
 assert trial.tools==s.tools and trial.reasoning_effort==s.reasoning_effort
# Also preserve previously recorded legacy openings exactly.
for v in (5,6):
 b=json.loads(Path(f'reports/guidance-7-v{v}-before.json').read_text());old=FreshSession(b['packet'])
 assert b==dict(packet=b['packet'],initial=old.initial,tools=old.tools,reasoning_effort=old.reasoning_effort)
r=dict(v7_byte_identical=True,legacy_v5_v6_byte_identical=True,v8_exact_decision=True,v8_bundle_validated=True,non_system_inputs_identical=True,walk_default=7,provider_invoked=False,original_packets_modified=False,paragraph_sha256=hashlib.sha256(expected.encode()).hexdigest(),v7_system_sha256=hashlib.sha256(s.initial[0]['content'].encode()).hexdigest())
Path('reports/guidance-8-implementation-001.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
