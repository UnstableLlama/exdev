"""Administrative reference discovery resolution; never teacher input."""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from teacher.root_evidence import pages,fetch
base=Path('reports/commit-000234-reference-discovery-001.json')
j=json.loads(base.read_text());proofs=[]
oldpath=Path('reports/commit-000158-reference-discovery-004.json')
old=json.loads(oldpath.read_text())
for r in j['candidates']:
 if r['status']!='unavailable':continue
 if r.get('http_status')==404 and r.get('revision'):
  url='https://huggingface.co/api/models/'+r['repo']+'/tree/'+r['revision']+'?recursive=true'
  rows=[x for pg in pages(url) for x in pg]
  assert not any(x['path']=='config.json' for x in rows)
  proofs.append(dict(repo=r['repo'],revision=r['revision'],url=url,tree=rows))
  r.update(status='missing_root_config_at_pin',reason='Pinned recursive tree confirms no root config.json; no architecture inferred.',published_files=[x['path'] for x in rows])
 elif r['repo']=='mistralai/Mistral-Large-Instruct-2407':
  prior=next(x for p in old['reports'] for x in p['candidates'] if x['repo']==r['repo'])
  url='https://huggingface.co/api/models/'+r['repo']+'/tree/main?recursive=true'
  rows=[x for pg in pages(url) for x in pg];cfg=next(x for x in rows if x['path']=='config.json')
  assert cfg['oid']==prior['official_blob_id']
  for key in ('mirror_used','agreeing_mirror'):
   proof=prior[key];raw=Path(proof['config_file']).read_bytes()
   assert hashlib.sha256(raw).hexdigest()==proof['config_sha256']
   assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==cfg['oid']
  proofs.append(dict(repo=r['repo'],url=url,current_official_config=cfg))
  r.clear();r.update(prior,matched=False,reused_proof=str(oldpath),reused_proof_sha256=hashlib.sha256(oldpath.read_bytes()).hexdigest(),revalidation='Current official config blob equals both retained pre-cutoff mirror copies; both local config hashes rechecked.')
 else:raise ValueError(r)
j.update(unavailable=[r['repo'] for r in j['candidates'] if r['status']=='unavailable'])
j['complete']=not j['unavailable'];j['organizations']=[dict(name='mistralai',reason='Original Mistral model publisher; no other official publisher identified for Mistral3ForConditionalGeneration.')]
j['resolution_proofs']='reports/commit-000234-discovery-proofs-001.json'
for path,data in [('reports/commit-000234-discovery-proofs-001.json',proofs),('reports/commit-000234-reference-discovery-002.json',j)]:
 with open(path,'x') as f:json.dump(data,f,indent=2);f.write('\n')
print(json.dumps(dict(complete=j['complete'],candidates=len(j['candidates']),matches=[r['repo'] for r in j['candidates'] if r.get('matched')],unavailable=j['unavailable'])))
