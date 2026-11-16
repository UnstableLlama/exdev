"""Administrative discovery; never teacher input."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError
from teacher.root_evidence import pages,fetch,choose_revision
from teacher.evidence import timestamp
cut='2025-06-01T17:13:26+02:00';arch='Gemma3ForCausalLM'
oldpath=Path('reports/commit-000164-reference-discovery-003.json');old=json.loads(oldpath.read_text());prior={r['repo']:r for r in old['candidates']}
metaold={r['id']:r for r in json.load(open('reports/commit-000164-public-metadata-001.json'))['models']}
url='https://huggingface.co/api/models?author=google&limit=100&full=true&config=true'
models=[r for page in pages(url) for r in page]
Path('reports/commit-000214-public-metadata-001.json').write_text(json.dumps(dict(url=url,models=models),indent=2)+'\n')
def inspect(m):
 repo=m['id'];r=dict(repo=repo)
 if timestamp(m['createdAt'])>timestamp(cut):return dict(r,status='created_after_cutoff',created_at=m['createdAt'])
 p=prior.get(repo);om=metaold.get(repo,{})
 if p and m['sha']==om.get('sha') and (p['status'].startswith('mirror_inspected') or timestamp(m['lastModified'])<=timestamp(old['cutoff'])):
  r=dict(p);r['matched']=arch in r.get('architectures',[]);r['reused_proof']=str(oldpath);r['reused_proof_sha256']=hashlib.sha256(oldpath.read_bytes()).hexdigest();return r
 try:
  if m['gated']:return dict(r,status='unavailable',reason='Gated metadata changed or no prior proof; requires fresh mirror proof')
  pin={'id':m['sha'],'date':m['lastModified']} if timestamp(m['lastModified'])<=timestamp(cut) else choose_revision([x for pg in pages('https://huggingface.co/api/models/'+repo+'/commits/main') for x in pg],cut)
  r.update(revision=pin['id'],revision_date=pin['date'])
  b,_=fetch('https://huggingface.co/'+repo+'/resolve/'+pin['id']+'/config.json');a=json.loads(b).get('architectures',[])
  return dict(r,status='inspected_pinned_config',architectures=a,matched=arch in a,config_sha256=hashlib.sha256(b).hexdigest())
 except HTTPError as e:return dict(r,status='missing_root_config_at_pin' if e.code==404 and 'revision' in r and e.headers.get('X-Error-Code')=='EntryNotFound' else 'unavailable',reason=str(e))
 except ValueError as e:return dict(r,status='no_eligible_revision' if 'revision' in str(e).lower() else 'unavailable',reason=str(e))
 except Exception as e:return dict(r,status='unavailable',reason=str(e))
with ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(inspect,models))
unavailable=[r['repo'] for r in rows if r['status']=='unavailable']
out=dict(organization='google',architecture=arch,cutoff=cut,enumeration_url=url,enumerated_repositories=[m['id'] for m in models],candidates=rows,unavailable=unavailable,complete=not unavailable,basis='Full original publisher enumeration. Reuse previously validated config/absence proof only with unchanged official repository SHA and either pre-cutoff latest revision or accepted hash-verified mirror proof. Otherwise inspect latest pre-cutoff revision. Deleted/private repositories cannot be enumerated.')
Path('reports/commit-000214-reference-discovery-001.json').write_text(json.dumps(out,indent=2)+'\n')
from collections import Counter
print(Counter(r['status'] for r in rows));print('unavailable',unavailable);print('matches',[r['repo'] for r in rows if r.get('matched')])
