"""Offline scratch rebuild comparison: approved packets versus cycle builders."""
import hashlib,json,platform
from pathlib import Path
from teacher.cycle import prepare_packet
from teacher.session import FreshSession
root=Path('.');state=json.loads(Path('reports/teacher-walk-001.json').read_text());rows=[]
for n in (156,157):
 old=Path(f'.teacher/retrieval/{n:06d}-001');new=Path(f'.teacher/retrieval/token-cost-rebuild-{n:06d}-001')
 m=json.loads((old/'manifest.json').read_text())
 prepare_packet(Path('.sources/exllamav3.git'),m['task_sha'],n,new,Path('data/evidence/github'),Path('store'),[Path(p) for p in state['approved_entries']])
 old_bytes=(old/'manifest.json').read_bytes();new_bytes=(new/'manifest.json').read_bytes()
 before=FreshSession(old);after=FreshSession(new)
 row=dict(position=n,manifest_bytes_equal=old_bytes==new_bytes,manifest_sha256=hashlib.sha256(old_bytes).hexdigest(),new_manifest_sha256=hashlib.sha256(new_bytes).hexdigest(),opening_equal=before.initial==after.initial,tools_equal=before.tools==after.tools,blob_names_equal=sorted(p.name for p in (old/'blobs').iterdir())==sorted(p.name for p in (new/'blobs').iterdir()))
 rows.append(row)
 if old_bytes!=new_bytes:
  a=json.loads(old_bytes);b=json.loads(new_bytes);row['different_keys']=[k for k in set(a)|set(b) if a.get(k)!=b.get(k)]
Path('reports/token-cost-rebuild-001.json').write_text(json.dumps(dict(checks=rows,python_version=platform.python_version(),machine_architecture=platform.machine(),teacher_invoked=False),indent=2)+'\n')
print(json.dumps(rows))
assert all(r['manifest_bytes_equal'] and r['opening_equal'] and r['tools_equal'] and r['blob_names_equal'] for r in rows)
