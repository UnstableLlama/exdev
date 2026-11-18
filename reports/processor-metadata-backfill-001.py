"""Administrative pinned-only backfill; never teacher input."""
import sys,json,copy,hashlib
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from teacher.root_evidence import fetch,pages,item
from teacher.mirror_evidence import mirror_files,file_url,git_blob,digest,file_set_revision,validate_item
from teacher.architecture_evidence import load_bundle
from teacher.evidence import timestamp
OUT=Path('data/evidence/processor-metadata-backfill-001');OUT.mkdir(parents=True,exist_ok=True)
FILES=['preprocessor_config.json','processor_config.json']
report={'sources':[],'files':[],'bundles':[]}

def recover(arg):
 n,s,entries,cutoff=arg
 repo=s['repo'];first=entries[0];proof=first.get('mirror_provenance');cache=OUT/repo.replace('/','--');cache.mkdir(exist_ok=True)
 result=[];added=[]
 try:
  if proof:
   pin=proof['official_revision'];url=f'https://huggingface.co/api/models/{repo}/revision/{pin}?blobs=true'
   raw,_=fetch(url);official=json.loads(raw);assert official['sha']==pin
   (cache/'official.json').write_bytes(raw)
   rows,mirror_raw=mirror_files(proof['mirror_repo'],proof['mirror_revision']);(cache/'mirror.json').write_bytes(mirror_raw)
   published={r['rfilename']:r for r in official['siblings']};mirrors={r['Path']:r for r in rows if r['Type']=='blob'}
  else:
   pin=s['revision'];rows=[r for page in pages(f'https://huggingface.co/api/models/{repo}/tree/{pin}?recursive=true') for r in page]
   (cache/'tree.json').write_text(json.dumps(rows,indent=2));published={r['path']:r for r in rows if r['type']=='file'}
  for path in FILES:
   rec={'position':n,'repo':repo,'pin':pin,'path':path}
   try:
    if path not in published:rec['status']='absent_at_pin';result.append(rec);continue
    r=published[path]
    if proof:
     row=mirrors[path];date=datetime.fromtimestamp(row['CommittedDate'],timezone.utc).isoformat();assert timestamp(date)<=timestamp(cutoff)
     url=file_url(proof['mirror_repo'],row['Revision'],path);data,_=fetch(url)
     assert len(data)==r['size']==row['Size'];assert digest(data)==row['Sha256'];assert git_blob(data)==r['blobId']
     p=copy.deepcopy(proof);p.update(path=path,official_metadata_sha256=digest(raw),mirror_listing_sha256=digest(mirror_raw),mirror_revision=row['Revision'],mirror_committed_at=date,file_size=len(data),mirror_file_sha256=digest(data),hash_algorithm='git_blob_sha1',official_hash=r['blobId'],mirror_hash=git_blob(data));p.pop('ranges',None)
     e=item(first['source_id'].rsplit(':',1)[0]+':'+path,url,data,date,kind='hf_file',artifact_role='non_weight',repo_id=repo,path=path,created_at=proof['official_created_at'],representation='hash_verified_mirror_file',mirror_provenance=p)
     validate_item(e,data,cutoff)
    else:
     url=f'https://huggingface.co/{repo}/resolve/{pin}/{path}';data,_=fetch(url);assert git_blob(data)==r['oid']
     e=item(first['source_id'].rsplit(':',1)[0]+':'+path,url,data,s['date'],kind='hf_file',artifact_role='non_weight',repo_id=repo,revision=pin,path=path)
    json.loads(data);(cache/path).write_bytes(data);added.append(e);rec.update(status='recovered',sha256=digest(data),url=url,revision_at=e['revision_at'])
   except Exception as exc:rec.update(status='inaccessible',error_type=type(exc).__name__,error=str(exc))
   result.append(rec)
 except Exception as exc:
  result=[{'position':n,'repo':repo,'path':path,'status':'inaccessible','error_type':type(exc).__name__,'error':str(exc)} for path in FILES]
 print(repo,[(r['path'],r['status']) for r in result],flush=True)
 return n,repo,added,result
bundles={}
args=[]
for n in [164,234]:
 p=Path(f'data/evidence/github/{n:06d}-references.json');raw=p.read_bytes();b=json.loads(raw);bundles[n]=b
 report['sources'].append({'path':str(p),'sha256':digest(raw)})
 for s in b['selections']:args.append((n,s,[e for e in b['items'] if e['repo_id']==s['repo']],b['cutoff']))
with ThreadPoolExecutor(max_workers=4) as pool:
 for n,repo,added,rows in pool.map(recover,args):
  report['files'].extend(rows);b=bundles[n];s=next(s for s in b['selections'] if s['repo']==repo);b['items'].extend(added)
  if added and s.get('retrieval_source'):
   entries=[e for e in b['items'] if e['repo_id']==repo];revision=file_set_revision(entries)
   for e in entries:e['revision']=revision
   s.update(revision=revision,date=max((e['revision_at'] for e in entries),key=timestamp),verified_files=sorted(e['path'] for e in entries))
  elif added:s['non_weight_files']=sorted(set(s['non_weight_files'])|{e['path'] for e in added})
for n,b in bundles.items():
 p=OUT/f'{n:06d}-references.json';p.write_text(json.dumps(b,indent=2)+'\n');load_bundle(Path('.sources/exllamav3.git'),b['task_sha'],p)
 report['bundles'].append({'path':str(p),'sha256':digest(p.read_bytes()),'validated':True,'original_task_sha':b['task_sha'],'cutoff':b['cutoff']})
for source in report['sources']:assert digest(Path(source['path']).read_bytes())==source['sha256']
report['original_bundles_unchanged']=True
report['status']='complete' if all(r['status']!='inaccessible' for r in report['files']) else 'incomplete'
Path('reports/processor-metadata-backfill-001.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],flush=True)
