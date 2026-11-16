# SPDX-License-Identifier: MIT
"""Task-only, cutoff-bound closed discussion navigation (salience-v2)."""
from .blob_store import put
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
PATH_RULE = 'salience-v3-paths'
PATH_INSTRUCTION = ('The closed_discussion_catalog lists closed discussions qualified by shared terms or by paths named in cutoff-bound text that overlap the task change. matched_paths exposes those repository paths; a bare filename qualifies only when it resolves uniquely. These are navigation hints, not established relationships; fetch bodies with web_fetch, page with evidence_index(index_id="closed_discussions"), label task links as inference with their concrete basis, and report each item’s own title and framing faithfully.')


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


def task_paths(repo, sha):
    """Exact first-parent changed paths, including both sides of a rename."""
    parents=git(repo,'show','-s','--format=%P',sha).decode().split()
    revisions=[parents[0],sha] if parents else ['--root',sha]
    return sorted(set(git(repo,'diff-tree','--no-commit-id','--name-only','--no-renames','-r',*revisions).decode().splitlines()))


def path_mentions(row, paths):
    """Resolve full paths or unambiguous bare filenames in cutoff title/body text."""
    from .recover_github import repo_path_hints, discussion_text
    text=row['title']+'\n'+discussion_text(row)
    probe=dict(row,content=json.dumps({'objects':[{'content':text}]}))
    found=set(repo_path_hints(probe,paths,limit=len(paths))['repo_paths_mentioned'])
    names={}
    for path in paths:names.setdefault(Path(path).name,set()).add(path)
    for name, matches in names.items():
        # A bare filename is not a fragment of a different qualified path.
        if len(matches)==1 and re.search(r'(?<![A-Za-z0-9_./+\\-])'+re.escape(name)+r'(?![A-Za-z0-9_./+\\-])',text):
            found.update(matches)
    return found


def select(histories, cutoff, task, paths, excluded=(), cap=CAP, *, message, changed_paths=None):
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
    changed=set(changed_paths or [])
    universe=sorted(set(paths)|changed)
    for row,words in candidates:
        matched=sorted(task & words)
        score=sum((Fraction(1,frequencies[t]**2) for t in message & words),Fraction())
        overlap=sorted(changed & path_mentions(row,universe)) if changed_paths is not None else []
        if (score<THRESHOLD and not overlap) or row['url'] in excluded:continue
        row.update(repo_path_hints(row,paths));row['matched_terms']=matched;row['state']='closed'
        if changed_paths is not None:row['matched_paths']=overlap
        # Path overlap independently qualifies at the existing threshold; retain
        # lexical ordering above it, then the existing deterministic tie break.
        ranked.append((max(score,THRESHOLD) if overlap else score,row))
    ranked.sort(key=lambda x:(-x[0],x[1]['kind'],x[1]['number']))
    return {'rule':PATH_RULE if changed_paths is not None else 'salience-v2',
            **({'task_changed_paths':sorted(changed)} if changed_paths is not None else {}),
            'limit':cap,'truncated':len(ranked)>cap,
            'items':[r for _,r in ranked[:cap]],'closed_at_cutoff':closed_count,'unknown_state_count':unknown_state_count,'eligible_candidates':len(candidates),
            'qualified_count':len(ranked)}


def attach(packet, manifest, bundle):
    if (bundle['task_sha']!=manifest['task_sha'] or timestamp(bundle['cutoff'])!=timestamp(manifest['cutoff_date'])
        or bundle.get('complete') is not True or bundle.get('rule') not in ('salience-v2',PATH_RULE)):
        raise ValueError('Invalid closed discussion recovery')
    with_paths=bundle['rule']==PATH_RULE
    if with_paths and bundle.get('task_changed_paths')!=sorted(set(manifest['task_changed_files'])):
        raise ValueError('Closed discussion changed paths differ from task')
    if bundle['limit']!=CAP or not isinstance(bundle['truncated'],bool) or len(bundle['items'])>CAP:
        raise ValueError('Invalid closed discussion cap')
    rows=[]
    for item in bundle['items']:
        if (item['state']!='closed' or not item['available'] or
            any(timestamp(item[k])>timestamp(manifest['cutoff_date']) for k in ('created_at','closed_at','revision_at'))):
            raise ValueError('Invalid closed discussion cutoff')
        overlap=item.get('matched_paths',[]) if with_paths else []
        if with_paths and (not isinstance(overlap,list) or overlap!=sorted(set(overlap)) or not set(overlap)<=set(bundle['task_changed_paths'])):
            raise ValueError('Invalid closed discussion matched paths')
        if (not item['matched_terms'] and not overlap) or item['matched_terms']!=sorted(set(item['matched_terms'])) or any(t not in terms(t) for t in item['matched_terms']):
            raise ValueError('Invalid closed discussion matched terms')
        data=item['content'].encode();sha=hashlib.sha256(data).hexdigest()
        if sha!=item['content_sha256']:raise ValueError('Closed discussion checksum mismatch')
        put(packet, data)
        fields=('number','kind','title','author_login','created_at','closed_at','state','url','available',
                'repo_paths_mentioned','repo_paths_mentioned_truncated','matched_terms')
        if with_paths:fields+=('matched_paths',)
        rows.append({k:item[k] for k in fields})
        obj={k:item[k] for k in ('author_login','url','source_id','created_at','revision_at','retrieved_at','representation','content_sha256')}
        obj.update(blob=sha,kind='web',content_bytes=len(data),catalog_origin='closed_discussion')
        manifest['evidence'].append(obj)
    manifest['closed_discussion_catalog']={'rows':rows,'limit':bundle['limit'],'truncated':bundle['truncated']}
    if with_paths:manifest['closed_discussion_catalog']['rule']=PATH_RULE
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
