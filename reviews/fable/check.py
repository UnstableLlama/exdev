import json,hashlib,subprocess,os,re,sys,datetime,glob
from pathlib import Path
sys.path.insert(0,'.')
from teacher import editorial, approval_policy
N,A=sys.argv[1],sys.argv[2]
R=f'.teacher/runs/commit-{N}-{A}';P=f'.teacher/retrieval/{N}-{A}'
sha=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest()
for f in ['draft.json','draft.md','raw-transcript.json','provenance.json','coverage.json']: print(f,sha(f'{R}/{f}'))
print('manifest',sha(P+'/manifest.json'))
for f in glob.glob(f'data/evidence/github/{N}-unreferenced.json'): print(f,sha(f))
t=json.load(open(R+'/raw-transcript.json'));d=json.load(open(R+'/draft.json'));p=json.load(open(R+'/provenance.json'));m=json.load(open(P+'/manifest.json'))
print('manifest==prov',p['packet_manifest_sha256']==sha(P+'/manifest.json'), p['model'],p['reasoning_effort'],p['codex_version'])
bad=[k for k,v in p['implementation_sha256'].items() if sha(k)!=v];print('impl',len(p['implementation_sha256']),'bad',bad)
res={x['call_id']:hashlib.sha256(x['content'].encode()).hexdigest() for x in t if x['role']=='tool'}
calls={c['id']:c for x in t if x['role']=='assistant' and 'calls' in x for c in x['calls']}
print('evidence',len(d['evidence']),'calls',len(calls),'bad',[k for k,v in d['evidence'].items() if res.get(k)!=v['result_sha256'] or calls[k]['arguments']!=v['arguments'] or calls[k]['tool']!=v['tool']],'uncited',[k for k in calls if k not in d['evidence']])
print('final==annotation',json.loads(t[-1]['content'])==d['annotation'],'render',editorial.render(d)==open(R+'/draft.md').read())
print('assess',approval_policy.assess(Path(R),Path(P),Path('.sources/exllamav3.git')))
G=['git','--git-dir=.sources/exllamav3.git'];T=m['task_sha']
print(subprocess.check_output(G+['log','-1','--format=%H|%P|%an|%aI|%cI|%s|%b',T]).decode().strip())
anc=set(subprocess.check_output(G+['rev-list']+[x for x in m['task_parents']]).decode().split())
ent=[e['sha'] for e in m['ancestor_entries']]
print('anc',len(anc),'entries',len(ent),set(anc)==set(ent),'commits-extra',set(m['commits'])-anc,'graphs',set(m['graphs'])-anc,'shows',set(m['shows'])-anc-{T},'hist',set(m['history_order'])==anc)
blobs={}
for root,_,fs in os.walk(P+'/blobs'):
    for f in fs: blobs[f]=os.path.join(root,f)
print('blobs',len(blobs),'bad',sum(sha(v)!=k for k,v in blobs.items()))
cat=json.loads(open(blobs[m['ancestor_catalog_blob']]).read());print('catalog',len(cat),[c['sha'] for c in cat if c['sha'] not in anc])
u=json.loads(t[1]['content'])
print('opening: cat==manifest',u['unreferenced_discussion_catalog']==m['unreferenced_discussion_catalog'],'msg',repr(u['task_commit_message']),u['task_author_name'],u['task_parents'],u['cutoff_date'],u['task_sha']==T,'evidence_catalog',len(u['evidence_catalog']))
print('system same as 32-002', t[0]['content']==json.load(open('.teacher/runs/commit-000032-002/raw-transcript.json'))[0]['content'])
cut=datetime.datetime.fromisoformat(m['cutoff_date']);late=[]
for e in m['evidence']:
    b=open(blobs[e['blob']]).read()
    for ts in re.findall(r'20\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ',b):
        if datetime.datetime.fromisoformat(ts.replace('Z','+00:00'))>cut: late.append((e.get('discussion_number'),ts))
print('late',late,'cutoff utc',cut.astimezone(datetime.timezone.utc))
for r in u['unreferenced_discussion_catalog']: print(r['kind'],r['number'],r['state'],r['created_at'],r['title'],r['repo_paths_mentioned'])
# entries for 17 and 32
for e in m['ancestor_entries']:
    if e['sha'][:8] in('11822a55','1d77c052'):
        b=open(blobs[e['prose_blob']]).read(); print(e['sha'][:8],'issue6' if 'Issue #6' in b else '', 'issue8' if 'Issue #8' in b else '')
for i,x in enumerate(t[2:],2):
    if x['role']=='assistant' and 'calls' in x: print(i,json.dumps(x['calls'][0])[:330])
