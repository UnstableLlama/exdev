from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from teacher.author import write_json
from ledger.retrospectives import append
base=Path('reports/defect-ledger');ev=base/'evidence';bundle=Path('data/evidence/github/000039-references.json');raw=bundle.read_bytes();assert hashlib.sha256(raw).hexdigest()=='4849f07bafae2218c58b69856fa7f68bfe5c536a366758601658a9bb36c4704e'
b=json.loads(raw);selected=[];comparisons=[]
for repo in ['nvidia/Llama-3_1-Nemotron-51B-Instruct','nvidia/Llama-3_1-Nemotron-Ultra-253B-v1']:
 items=[x for x in b['items'] if x['repo_id']==repo];config=next(x for x in items if x['path']=='config.json');c=json.loads(config['content']);headers={}
 selected.append(config)
 for x in items:
  if x['kind']=='safetensors_header':
   selected.append(x)
   for name,value in json.loads(x['content']).items():
    if name!='__metadata__':headers[name]=value
 q=c['num_attention_heads'];dim=c.get('head_dim') or c['hidden_size']//q;rows=[]
 for i,block in enumerate(c['block_configs']):
  a=block['attention']
  if a.get('no_op') or a.get('replace_with_linear'):continue
  g=a['n_heads_in_group'];width=headers[f'model.layers.{i}.self_attn.k_proj.weight']['shape'][0]
  rows.append({'block':i,'query_heads':q,'group_size':g,'head_dim':dim,'header_k_width':width,'original_width':g*dim,'fixed_width':q//g*dim})
 comparisons.append({'repo':repo,'blocks':rows,'original_matches':sum(x['original_width']==x['header_k_width'] for x in rows),'fixed_matches':sum(x['fixed_width']==x['header_k_width'] for x in rows)})
assert [(x['original_matches'],x['fixed_matches']) for x in comparisons]==[(44,54),(0,64)]
objects=ev/'decilm-r002-reference-objects.json';write_json(objects,{'source_bundle_sha256':hashlib.sha256(raw).hexdigest(),'items':selected})
check=ev/'decilm-r002-comparison.json';write_json(check,{'acquisition':'Administrative computation prompted by known fix and reviewer; never backdated.','models':comparisons,'limits':'Header dimensional correspondence only; no model/GPU execution.'})
v=ev/'decilm-r002-review-verdict.md';v.write_bytes(Path('reviews/verdicts/commit-000044-001.md').read_bytes())
record=json.loads((base/'exllamav3-decilm-kv-head-count--r001.json').read_text());record.update(revision_id='r002',supersedes='r001',status='confirmed',recorded_at=datetime.now(timezone.utc).isoformat(),reviewed_at=None,reviewer=None)
record['verification']={'method':'source_inspection_and_checkpoint_header_comparison','checks':[{k:v for k,v in x.items() if k!='blocks'} for x in comparisons],'acquisition':'Fix-derived; comparison motivated by later fix and reviewer recommendation. Fix dependency retained.','limits':'No model loading or GPU execution; new revision pending review.'}
for x in selected:record['dependencies'].append({'url':x['url'],'source_id':x['source_id'],'content_sha256':x['content_sha256'],'available_at':x['revision_at']})
for f in [objects,check,v,Path('/tmp/exdev-confirm44.py')]:
 if f.parent==Path('/tmp'):
  dest=ev/'decilm-r002-comparison.py';dest.write_bytes(f.read_bytes());f=dest
 record['evidence'].append({'file':str(f.relative_to(base)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
print(append(base,record));print([(x['repo'],x['original_matches'],x['fixed_matches']) for x in comparisons])
