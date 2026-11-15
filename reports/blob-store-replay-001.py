import json,hashlib,platform,subprocess
from pathlib import Path
from teacher.runner import Runner,command
from teacher.approval_policy import assess
from teacher.blob_store import store_root
rows=[]
for number in [75,98,103,126,127]:
 run=Path(f'.teacher/runs/commit-{number:06d}-001');packet=Path(f'.teacher/retrieval/{number:06d}-001')
 transcript=json.loads((run/'raw-transcript.json').read_text());calls={c['id']:c for t in transcript if t.get('role')=='assistant' for c in t.get('calls',[])}
 runner=Runner(packet);n=0
 for t in transcript:
  if t.get('role')!='tool':continue
  c=calls[t['call_id']];actual=runner.invoke(c['tool'],c['arguments']);expected=json.loads(t['content'])
  assert actual==expected,(number,c['tool'],actual,expected)
  n+=1
 assess(run,packet,Path('.sources/exllamav3.git'))
 rows.append({'run':str(run),'identical_tool_calls':n,'render_and_coverage_identical':True});print(rows[-1],flush=True)
p=Path('.teacher/retrieval/000127-001');blob=next((p/'blobs').iterdir());before=hashlib.sha256(blob.read_bytes()).hexdigest()
code=f'''import os,json
p='/packet/blobs/{blob.name}'
checks=[]
for op in [lambda:open(p,'wb'),lambda:os.chmod(p,0o644),lambda:os.unlink(p)]:
 try:op()
 except OSError:checks.append(True)
 else:checks.append(False)
assert all(checks)
assert not os.path.exists({str(store_root(p))!r})
print(json.dumps(checks))
'''
cmd=command(p.resolve());cmd[-1:]=['-c',code];r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0,r.stderr
assert hashlib.sha256(blob.read_bytes()).hexdigest()==before
report={'status':'passed','replays':rows,'actual_packet_sandbox_denials':json.loads(r.stdout),'store_hidden':True,'machine_architecture':platform.machine(),'python_version':platform.python_version(),'live_teacher_run':False}
Path('reports/blob-store-boundary-001.json').write_text(json.dumps(report,indent=2)+'\n')
