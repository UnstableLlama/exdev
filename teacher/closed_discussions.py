# SPDX-License-Identifier: MIT
"""Task-only, cutoff-bound closed discussion navigation (salience-v2)."""
import hashlib
import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path
from .evidence import discussion_snapshot, timestamp
from .packet import git

MIN_LENGTH = 4
THRESHOLD = Fraction(1)
CAP = 20
STOP = frozenset('this that with from into have has been were will would could should does then than when where which their there these those only also some more most such each other same using used use add added adds remove removed update change changed changes fix fixes fixed test tests true false none self return import class void const auto else elif error model models tensor tensors torch cuda exllamav3 file files code function value values input output'.split())
INSTRUCTION = ('The closed_discussion_catalog lists closed discussions whose cutoff-bound text shares terms with the task (matched terms expose words from that text), not established relationships; apply the existing catalog reading rule to these rows, fetch bodies with web_fetch, page navigation with evidence_index(index_id="closed_discussions"), label any task link as inference with its concrete basis, and report each item’s own title and framing faithfully.')


# General prose/scaffolding stop list, extended after inspecting the positions 2–68 audit.
STOP = STOP | frozenset('about above after again against always anyone anything around because before being below between both cannot come didn does doesn doing done down during either enough even every first forward found further getting here however init__ just keep know last later less line lines little look made make making many might much must need never next nothing once overall over own part pass please point really same seems should since small something still stuff sure take than them they through time under until upon very want well what when while whole without work working would your args kwargs module modules directory directories example examples readme http https github issue issues pull requests version'.split())


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def terms(text):
    return {s.lower() for s in re.findall(r'[A-Za-z][A-Za-z0-9_]*',text)
            if len(s)>=MIN_LENGTH and s.lower() not in STOP}


def task_terms(repo, sha):
    message=git(repo,'show','-s','--format=%B',sha).decode()
    paths=git(repo,'diff-tree','--root','-m','--no-commit-id','--name-only','-r',sha).decode()
    diff=git(repo,'show','--format=','--first-parent','--no-ext-diff','--unified=0',sha).decode(errors='replace')
    lines=[];code=False
    for line in diff.splitlines():
        if line.startswith('diff --git '):
            code=line.rsplit('.',1)[-1] in ('py','cu','cuh','c','cpp','h','hpp','js','ts','sh','rs')
        elif code and line[:1] in ('+','-') and not line.startswith(('+++','---')):
            # Lexical identifiers, excluding quoted literals and line comments.
            cleaned=re.sub(r"\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|//.*|\#.*|/\*.*?\*/", ' ', line[1:])
            lines.append(cleaned)
    return terms(message+'\n'+paths+'\n'+'\n'.join(lines))


def message_terms(repo, sha):
    return terms(git(repo,'show','-s','--format=%B',sha).decode())


def select(histories, cutoff, task, paths, excluded=(), cap=CAP, *, message):
    from .recover_github import repo_path_hints, discussion_text
    candidates=[];closed_count=0;unknown_state_count=0
    for bundle in histories:
        try:
            if timestamp(bundle['createdAt'])>timestamp(cutoff):continue
            if not bundle.get('timeline_complete'):raise ValueError('Unknown state')
            state='open'
            for event in sorted(bundle.get('state_events',[]),key=lambda e:timestamp(e['createdAt'])):
                if timestamp(event['createdAt'])>timestamp(cutoff):break
                if event['kind'] not in ('closed','reopened'):raise ValueError('Unknown state')
                state='closed' if event['kind']=='closed' else 'open'
            if state!='closed':continue
            closed_count+=1
        except (KeyError,ValueError,TypeError):
            unknown_state_count+=1;continue
        try: row=discussion_snapshot(bundle,cutoff,closed=True)
        except (KeyError,ValueError,TypeError): continue
        if not row or not row.get('available'):continue
        # Edit-event diffs are summaries, not established historical bodies.
        objects=json.loads(row['content'])['objects']
        if not any(o['url']==bundle['url'] for o in objects) or any(o['representation']!='body' for o in objects):continue
        words=terms(row['title']+'\n'+discussion_text(row))
        candidates.append((row,words))
    frequencies=Counter(t for _,words in candidates for t in words)
    ranked=[]
    for row,words in candidates:
        matched=sorted(task & words)
        score=sum((Fraction(1,frequencies[t]**2) for t in message & words),Fraction())
        if score<THRESHOLD or row['url'] in excluded:continue
        row.update(repo_path_hints(row,paths));row['matched_terms']=matched;row['state']='closed'
        ranked.append((score,row))
    ranked.sort(key=lambda x:(-x[0],x[1]['kind'],x[1]['number']))
    return {'rule':'salience-v2','limit':cap,'truncated':len(ranked)>cap,
            'items':[r for _,r in ranked[:cap]],'closed_at_cutoff':closed_count,'unknown_state_count':unknown_state_count,'eligible_candidates':len(candidates),
            'qualified_count':len(ranked)}


def attach(packet, manifest, bundle):
    if (bundle['task_sha']!=manifest['task_sha'] or timestamp(bundle['cutoff'])!=timestamp(manifest['cutoff_date'])
        or bundle.get('complete') is not True or bundle.get('rule')!='salience-v2'):
        raise ValueError('Invalid closed discussion recovery')
    if bundle['limit']!=CAP or not isinstance(bundle['truncated'],bool) or len(bundle['items'])>CAP:
        raise ValueError('Invalid closed discussion cap')
    rows=[]
    for item in bundle['items']:
        if (item['state']!='closed' or not item['available'] or
            any(timestamp(item[k])>timestamp(manifest['cutoff_date']) for k in ('created_at','closed_at','revision_at'))):
            raise ValueError('Invalid closed discussion cutoff')
        if not item['matched_terms'] or item['matched_terms']!=sorted(set(item['matched_terms'])) or any(t not in terms(t) for t in item['matched_terms']):
            raise ValueError('Invalid closed discussion matched terms')
        data=item['content'].encode();sha=hashlib.sha256(data).hexdigest()
        if sha!=item['content_sha256']:raise ValueError('Closed discussion checksum mismatch')
        (Path(packet)/'blobs'/sha).write_bytes(data)
        fields=('number','kind','title','author_login','created_at','closed_at','state','url','available',
                'repo_paths_mentioned','repo_paths_mentioned_truncated','matched_terms')
        rows.append({k:item[k] for k in fields})
        obj={k:item[k] for k in ('author_login','url','source_id','created_at','revision_at','retrieved_at','representation','content_sha256')}
        obj.update(blob=sha,kind='web',content_bytes=len(data),catalog_origin='closed_discussion')
        manifest['evidence'].append(obj)
    manifest['closed_discussion_catalog']={'rows':rows,'limit':bundle['limit'],'truncated':bundle['truncated']}
    manifest['walk_input_contract']['closed_discussions_sha256']=binding(manifest)


def binding(manifest):
    return digest({'catalog':manifest.get('closed_discussion_catalog'),
                   'objects':[i for i in manifest['evidence'] if i.get('catalog_origin')=='closed_discussion']})


def validate(manifest, packet=None):
    if binding(manifest)!=manifest['walk_input_contract'].get('closed_discussions_sha256'):
        raise ValueError('Closed discussion catalog or objects changed')
    if packet is not None:
        from .worker import load_blob
        for obj in manifest['evidence']:
            if obj.get('catalog_origin')=='closed_discussion':load_blob(Path(packet),obj['blob'])


def page(manifest,args):
    from .worker import excerpt
    if 'closed_discussion_catalog' not in manifest:raise ValueError('No closed discussion catalog')
    return excerpt(json.dumps(manifest['closed_discussion_catalog']['rows'],sort_keys=True).encode(),args)
