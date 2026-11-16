import json,os,shutil,tempfile
from pathlib import Path
from teacher.closed_discussions import attach,validate
from teacher.runner import Runner
bundle=json.loads(Path('reports/closed-path-overlap-150-proposed-bundle-001.json').read_text())
with tempfile.TemporaryDirectory(dir=".teacher",prefix="catalog-audit-") as tmp:
 p=Path(tmp)/'packet';shutil.copytree('.teacher/retrieval/000150-001',p,copy_function=os.link)
 m=json.loads((p/'manifest.json').read_text());m['evidence']=[e for e in m['evidence'] if e.get('catalog_origin')!='closed_discussion'];m.pop('closed_discussion_catalog')
 attach(p,m,bundle);validate(m,p);(p/'manifest.json').unlink();(p/'manifest.json').write_text(json.dumps(m))
 runner=Runner(p);chunks=[];offset=0;n=0
 while True:
  result=runner.invoke('evidence_index',dict(index_id='closed_discussions',offset=offset,max_bytes=512));assert result['ok'],result
  r=result['result'];chunks.append(r['text']);n+=1
  if not r['truncated']:break
  offset=r['next_offset']
 rows=json.loads(''.join(chunks));pr=next(x for x in rows if x['number']==35 and x['kind']=='pull_request');assert pr['matched_paths']==['eval/humaneval.py']
 result=runner.invoke('web_fetch',dict(url=pr['url']));assert result['ok'],result
Path('reports/closed-path-overlap-live-001.json').write_text(json.dumps(dict(status='passed',purpose='Administrative clone of packet 150 with proposed closed catalog, not a teacher packet or replacement run',catalog_pages=n,matched_paths=pr['matched_paths'],web_fetch_succeeded=True,live_model_invoked=False),indent=2)+'\n');print('passed',n)
