import hashlib,json,subprocess
from pathlib import Path
from teacher.runner import Runner
from teacher.session import FreshSession
from teacher.approval_policy import assess
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files=[p for p in Path('.teacher/runs').glob('*/**/*') if p.is_file()]+list(Path('.teacher').glob('**/manifest.json'))
before={str(p):H(p) for p in files};rows=[]
for n in [148,150,151]:
 run=Path(f'.teacher/runs/commit-{n:06d}-001');packet=Path(f'.teacher/retrieval/{n:06d}-001');t=json.loads((run/'raw-transcript.json').read_text());calls={c['id']:c for x in t if x.get('role')=='assistant' for c in x.get('calls',[])}
 for x in t:
  if x.get('role')!='tool':continue
  c=calls[x['call_id']];assert Runner(packet).invoke(c['tool'],c['arguments'])==json.loads(x['content']),c['id']
 initial=FreshSession(packet).initial
 assert t[:len(initial)]==initial
 assess(run,packet,Path('.sources/exllamav3.git'))
 rows.append(dict(position=n,identical_tool_calls=len(calls),initial_messages_identical=True,render_and_coverage_identical=True))
assert before=={str(p):H(p) for p in files}
original=[]
provenance=json.loads(Path('.teacher/runs/commit-000151-001/provenance.json').read_text())
for name in ['teacher/closed_discussions.py','teacher/session.py','teacher/worker.py']:
 data=(Path(name).read_text().replace("        if 'closed_discussion_catalog' not in manifest:\n            raise ValueError('No closed discussion catalog')\n        return excerpt(json.dumps(manifest['closed_discussion_catalog']['rows'],sort_keys=True).encode(),args)","        from .closed_discussions import page\n        return page(manifest,args)").encode() if name=='teacher/worker.py' else subprocess.check_output(['git','show','HEAD:'+name]));assert hashlib.sha256(data).hexdigest()==provenance['implementation_sha256'][name]
 target=Path('reports/closed-path-overlap-original-'+Path(name).name);target.write_bytes(data);original.append(dict(source=name,snapshot=str(target),sha256=H(target)))
Path('reports/closed-path-overlap-replay-001.json').write_text(json.dumps(dict(status='passed',replays=rows,historical_files_verified_unchanged=len(files),original_151_implementation=original,live_model_invoked=False),indent=2)+'\n');print(rows)
