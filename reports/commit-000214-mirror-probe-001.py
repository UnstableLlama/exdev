import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import json,hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from teacher.mirror_evidence import mirror_files,json_fetch,file_url,git_blob
from teacher.root_evidence import fetch
from teacher.evidence import timestamp
from datetime import datetime,timezone
meta=json.load(open('reports/commit-000214-public-metadata-001.json'))['models'];d=json.load(open('reports/commit-000214-reference-discovery-001.json'));unknown={x['repo'] for x in d['candidates'] if x['status']=='unavailable'}
def inspect(m):
 repo=m['id'];out={'repo':repo,'attempts':[]};base=Path('reports/commit-000214-nonmatch-mirror-probes')/repo.replace('/','--');base.mkdir(parents=True,exist_ok=True)
 try:o,b=json_fetch('https://huggingface.co/api/models/'+repo+'?blobs=true');(base/'official.json').write_bytes(b);official=next(x for x in o['siblings'] if x['rfilename']=='config.json')
 except Exception as e:return dict(out,error=str(e))
 for ns in ['google','LLM-Research','AI-ModelScope']:
  mr=ns+'/'+repo.split('/')[1];r={'mirror':mr};out['attempts'].append(r)
  try:
   rows,b=mirror_files(mr);(base/(ns+'-files.json')).write_bytes(b);s=next(x for x in rows if x['Path']=='config.json');date=datetime.fromtimestamp(s['CommittedDate'],timezone.utc).isoformat();r.update(date=date,revision=s['Revision'])
   b,_=fetch(file_url(mr,s['Revision'],'config.json'));(base/(ns+'-config.json')).write_bytes(b);r.update(official_blob=official['blobId'],mirror_blob=git_blob(b),architectures=json.loads(b).get('architectures',[]),config_sha256=hashlib.sha256(b).hexdigest())
   if git_blob(b)==official['blobId'] and timestamp(date)<=timestamp(d['cutoff']):out['status']='mirror_inspected_config';out['proof']=r;return out
   r['error']='Identity or cutoff mismatch'
  except Exception as e:r['error']=str(e) or type(e).__name__
 out['status']='unresolved';return out
with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(inspect,[x for x in meta if x['id'] in unknown]))
Path('reports/commit-000214-nonmatch-mirror-probe-001.json').write_text(json.dumps(rows,indent=2)+'\n')
for x in rows:print(x['repo'],x['status'],flush=True)
