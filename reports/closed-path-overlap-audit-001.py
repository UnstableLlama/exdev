import json,hashlib
from pathlib import Path
from teacher.closed_discussions import select,task_terms,task_paths,message_terms
from teacher.recover_github import parent_tree_paths
from teacher.evidence import timestamp
repo=Path('.sources/exllamav3.git');directory=Path('data/evidence/github')
inputs=Path('reports/closed-path-overlap-inputs-001.json')
if not inputs.exists():inputs.write_text(json.dumps([json.loads(p.read_text()) for p in sorted(directory.glob('discussion-*-history.json'))],indent=2)+'\n')
histories=json.loads(inputs.read_text());audit=[]
for n in range(2,152):
 r=json.loads(next(Path('data/exllamav3-v5/records').glob(f'{n:06d}_*.json')).read_text())
 paths=parent_tree_paths(repo,r['sha']);changed=task_paths(repo,r['sha']);kwargs=dict(message=message_terms(repo,r['sha']))
 import re
 excluded=set();bundle=directory/f'{n:06d}-eligible.json'
 if bundle.exists():
  for obj in json.loads(bundle.read_text())['items']:
   m=re.match(r'(https://github\.com/[^/]+/[^/]+/(?:issues|pull)/\d+)',obj.get('url',''))
   if m:excluded.add(m[1])
 args=(histories,r['commit_date'],task_terms(repo,r['sha']),paths,excluded)
 old=select(*args,**kwargs);new=select(*args,**kwargs,changed_paths=changed)
 oldids={(i['kind'],i['number']) for i in old['items']};newids={(i['kind'],i['number']) for i in new['items']}
 for row in new['items']:
  assert row['url'] not in excluded
  assert set(row['matched_paths'])<=set(changed)
  for o in json.loads(row['content'])['objects']:
   assert timestamp(o['created_at'])<=timestamp(r['commit_date']) and timestamp(o['revision_at'])<=timestamp(r['commit_date'])
 audit.append(dict(position=n,old_count=len(old['items']),new_count=len(new['items']),old_qualified=old['qualified_count'],new_qualified=new['qualified_count'],added=sorted(newids-oldids),removed=sorted(oldids-newids),truncated=new['truncated'],path_rows=[dict(number=i['number'],kind=i['kind'],matched_paths=i['matched_paths']) for i in new['items'] if i['matched_paths']]))
 if n==150:
  pr=next(i for i in new['items'] if i['kind']=='pull_request' and i['number']==35)
  assert ('pull_request',35) not in oldids and pr['matched_paths']==['eval/humaneval.py']
  objects=json.loads(pr['content'])['objects'];assert any(o['created_at']=='2025-05-11T20:41:37Z' for o in objects)
  assert not any(timestamp(o['created_at'])>timestamp(r['commit_date']) for o in objects)
  new.update(task_sha=r['sha'],cutoff=r['commit_date'],complete=True)
  Path('reports/closed-path-overlap-150-proposed-bundle-001.json').write_text(json.dumps(new,indent=2)+'\n')
report=dict(scope='administrative audit only; no historical bundle/packet/run writes',input_sha256=hashlib.sha256(inputs.read_bytes()).hexdigest(),positions=audit,positions_changed=sum(bool(r['added'] or r['removed']) for r in audit),added_rows=sum(len(r['added']) for r in audit),removed_rows=sum(len(r['removed']) for r in audit),truncated_positions=[r['position'] for r in audit if r['truncated']],cutoff_and_exclusions_verified=True)
Path('reports/closed-path-overlap-audit-001.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='positions'})
