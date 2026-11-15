# SPDX-License-Identifier: MIT
"""Trusted architecture triggers and cutoff-bound reference recovery."""
import argparse
import base64
import re
import ast
import hashlib
import json
from pathlib import Path
from .packet import git
from .evidence import timestamp
from .author import write_json
from .root_evidence import recover_hf


def inventory(repo, revision):
    keys=set(); classes={}
    if not revision:return keys,classes
    paths=git(repo,'ls-tree','-r','--name-only',revision,'exllamav3/models','exllamav3/architecture').decode().splitlines()
    for path in paths:
        if not path.endswith('.py'):continue
        tree=ast.parse(git(repo,'show',revision+':'+path).decode())
        found={n.name for n in ast.walk(tree) if isinstance(n,ast.ClassDef) and n.name.endswith(('Model','Config'))}
        if found:classes[path]=sorted(found)
        for node in ast.walk(tree):
            if isinstance(node,ast.Dict):
                for k,v in zip(node.keys,node.values):
                    if isinstance(k,ast.Constant) and isinstance(k.value,str) and isinstance(v,ast.Dict):
                        fields={x.value for x in v.keys if isinstance(x,ast.Constant)}
                        if {'config_class','model_class'}<=fields:keys.add(k.value)
    return keys,classes


def source_identities(repo, revision, files):
    """Read declarations, never execute upstream code or guess from class names."""
    result={}
    for path in files:
        tree=ast.parse(git(repo,'show',revision+':'+path).decode());names=set()
        for cls in (n for n in ast.walk(tree) if isinstance(n,ast.ClassDef) and n.name.endswith('Config')):
            for n in ast.walk(cls):
                if isinstance(n,(ast.Assign,ast.AnnAssign)):
                    targets=n.targets if isinstance(n,ast.Assign) else [n.target]
                    if any(isinstance(t,ast.Name) and t.id=='arch_string' for t in targets):
                        if isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):names.add(n.value.value)
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='__init__':
                    receiver=n.func.value
                    if not (isinstance(receiver,ast.Call) and isinstance(receiver.func,ast.Name) and receiver.func.id=='super'):continue
                    values=[k.value for k in n.keywords if k.arg=='arch_string']
                    if len(n.args)>1:values.append(n.args[1])
                    for value in values:
                        if isinstance(value,ast.Constant) and isinstance(value.value,str):names.add(value.value)
                        elif (isinstance(value,ast.Call) and isinstance(value.func,ast.Attribute) and value.func.attr=='get'
                              and len(value.args)==2 and isinstance(value.args[0],ast.Constant) and value.args[0].value=='arch_string'
                              and isinstance(value.args[1],ast.Constant) and isinstance(value.args[1].value,str)):
                            names.add(value.args[1].value)
        result[path]=sorted(names)
    return result


def renamed_paths(repo, parent, sha):
    fields=git(repo,'diff-tree','--no-commit-id','--name-status','-r','-M','-z',parent,sha).decode().strip('\0').split('\0')
    result={};i=0
    while i<len(fields) and fields[i]:
        status=fields[i];i+=1
        if status.startswith(('R','C')):
            old,new=fields[i:i+2];i+=2
            if status.startswith('R'):result[new]=old
        else:i+=1
    return result


def trigger_details(repo,sha):
    parents=git(repo,'show','-s','--format=%P',sha).decode().split()
    before,files=inventory(repo,parents[0] if parents else None);after,newfiles=inventory(repo,sha)
    if parents and not newfiles:
        raise ValueError('Architecture location unknown: no model/config classes in known directories')
    old_ids=source_identities(repo,parents[0],files) if parents else {}
    new_ids=source_identities(repo,sha,newfiles)
    prior_names=set(before)|{n for ns in old_ids.values() for n in ns}
    # Merge branch additions are still triggers relative to first parent. An
    # administrative outcome needs separate evidence of prior branch coverage.
    registry_added=sorted(after-before)
    derived_added=sorted({n for ns in new_ids.values() for n in ns}-prior_names)
    class_files=sorted(p for p,cs in newfiles.items() if p not in files or set(cs)-set(files[p]))
    renames=renamed_paths(repo,parents[0],sha) if parents else {}
    recognized={p:old for p,old in renames.items() if p in class_files and old in files
                and newfiles[p]==files[old] and new_ids[p]==old_ids[old]}
    unresolved=sorted(p for p in class_files if not new_ids[p] and p not in recognized)
    return dict(version=2,registry_architectures=registry_added,derived_architectures=derived_added,
                class_files=class_files,file_architectures={p:new_ids[p] for p in class_files},
                identity_files=sorted(p for p,ns in new_ids.items() if set(ns)&set(derived_added)),
                unresolved_class_files=unresolved,renames=recognized,parents=parents)


def trigger(repo,sha):
    d=trigger_details(repo,sha)
    return {'architectures':sorted(set(d['registry_architectures'])|set(d['derived_architectures'])),
            'class_files':d['class_files']}


def administrative_outcome(repo,sha,*,reason=None,covered_by=None):
    """Automatic rename proof, or explicit, reviewable administrative attestation."""
    d=trigger_details(repo,sha)
    if d['registry_architectures']:raise ValueError('Registry-key trigger cannot be waived')
    if covered_by:
        if len(d['parents'])<2:raise ValueError('Prior branch coverage requires a merge')
        expected=set(d['derived_architectures']);covered=set();covered_files=set()
        required_files=set(d['class_files'])|set(d['identity_files'])
        cutoff=git(repo,'show','-s','--format=%cI',sha).decode().strip()
        for proof in covered_by:
            path=Path(proof['bundle_path'])
            if path.is_symlink() or not path.is_file():raise ValueError('Covered bundle must be a regular file')
            raw=path.read_bytes()
            if hashlib.sha256(raw).hexdigest()!=proof['bundle_sha256']:raise ValueError('Covered bundle changed')
            previous=json.loads(raw);old=previous['task_sha']
            if old==sha or old not in git(repo,'rev-list',*d['parents'][1:]).decode().split():raise ValueError('Coverage is not on a merged branch')
            prior=load_bundle(repo,old,path)
            if not prior or prior.get('administrative_outcome'):raise ValueError('Branch lacks reference coverage')
            if timestamp(prior['cutoff'])>timestamp(cutoff):raise ValueError('Branch coverage exceeds merge cutoff')
            covered.update(r['architecture'] for r in prior['selections'])
            for p in required_files:
                paths=git(repo,'ls-tree','-r','--name-only',old,'--',p).decode().splitlines()
                if p in paths and git(repo,'show',old+':'+p)==git(repo,'show',sha+':'+p):covered_files.add(p)
        if not expected<=covered or not required_files<=covered_files:raise ValueError('Incomplete merged-branch coverage')
        basis='covered_merge'
    else:
        if d['derived_architectures']:raise ValueError('Source-derived new architecture cannot be waived')
        if d['class_files'] and set(d['class_files'])==set(d['renames']):
            basis='git_renames';reason=reason or 'Git-detected rename/move preserving declared classes and architecture identities.'
        else:basis='curator_attestation'
    if not reason or not reason.strip():raise ValueError('Non-architecture outcome requires a reason')
    return dict(status='not_new_architecture',basis=basis,reason=reason,renames=d['renames'],covered_by=covered_by or [])


def load_bundle(repo,sha,path):
    expected=trigger(repo,sha)
    if not any(expected.values()):return None
    if not path.is_file():raise ValueError('Architecture reference recovery required before authoring')
    bundle=json.loads(path.read_text());cutoff=git(repo,'show','-s','--format=%cI',sha).decode().strip()
    if bundle.get('task_sha')!=sha or bundle.get('cutoff')!=cutoff or bundle.get('trigger')!=expected:
        raise ValueError('Architecture reference task/cutoff/trigger mismatch')
    details=trigger_details(repo,sha)
    if 'trigger_details' in bundle and bundle['trigger_details']!=details:raise ValueError('Trigger analysis changed')
    if details['unresolved_class_files']:
        if bundle.get('unresolved_architecture_files')!=details['unresolved_class_files']:
            raise ValueError('Cannot derive architecture identity; record unresolved files in bundle')
    outcome=bundle.get('administrative_outcome')
    if outcome is not None:
        checked=administrative_outcome(repo,sha,reason=outcome.get('reason'),covered_by=outcome.get('covered_by'))
        if outcome!=checked or bundle.get('items') or bundle.get('selections'):raise ValueError('Invalid non-architecture outcome')
        return bundle
    reports=bundle.get('selections',[])
    if not reports:raise ValueError('Architecture reference selection report required')
    covered=set()
    for report in reports:
        if not report.get('reason') or not report.get('candidates_considered'):raise ValueError('Reference selection provenance required')
        if report['status'] not in ('complete','complete_with_absences','mirror_historical_unverified_identity','no_eligible_revision'):raise ValueError('Incomplete reference recovery')
        covered.add(report['architecture'])
        if report['status'] in ('complete','complete_with_absences','mirror_historical_unverified_identity'):
            if timestamp(report['date'])>timestamp(cutoff):raise ValueError('Reference revision after cutoff')
            items=[x for x in bundle['items'] if x.get('repo_id')==report['repo'] and x.get('revision')==report['revision']]
            paths={x['path'] for x in items if x.get('kind')=='hf_file'}
            missing={'config.json','tokenizer_config.json'}-paths
            if not any(x.get('kind')=='safetensors_header' for x in items):missing.add('safetensors headers')
            if report['status']=='complete_with_absences':
                published=report.get('published_files')
                if not isinstance(published,list) or not all(isinstance(p,str) for p in published):raise ValueError('Pinned tree required for absent references')
                absent=set(report.get('absent_at_revision',[]))
                if report.get('failures') or not report.get('absence_reason') or 'config.json' not in paths or absent!=missing or set(report.get('missing',[]))!=missing:raise ValueError('Invalid absent reference roles')
                for role in absent:
                    if (any(p.endswith('.safetensors') for p in published) if role=='safetensors headers' else role in published):raise ValueError('Published reference was not recovered')
                if not {x['path'] for x in items}<=set(published):raise ValueError('Reference absent from pinned tree')
            elif missing:raise ValueError('Incomplete reference roles')
            config=json.loads(next(x['content'] for x in items if x['path']=='config.json'))
            if report['architecture'] not in config.get('architectures',[]):raise ValueError('Reference architecture mismatch')
    if not set(expected['architectures'])<=covered:raise ValueError('Missing architecture reference selection')
    for item in bundle['items']:
        if not re.fullmatch('[0-9a-f]{40}|[0-9a-f]{64}',item.get('revision','')):raise ValueError('Immutable reference revision required')
        if timestamp(item['revision_at'])>timestamp(cutoff) or timestamp(item['created_at'])>timestamp(cutoff):raise ValueError('Reference object after cutoff')
        data=base64.b64decode(item['content_base64'],validate=True) if 'content_base64' in item else item['content'].encode()
        if hashlib.sha256(data).hexdigest()!=item['content_sha256']:raise ValueError('Reference checksum mismatch')
        if item.get('kind')=='safetensors_header':
            header=json.loads(data)
            if not isinstance(header,dict) or not header:raise ValueError('Invalid tensor header')
            for name,value in header.items():
                if name!='__metadata__' and (not isinstance(value,dict) or set(value)!={'dtype','shape','data_offsets'}):raise ValueError('Only tensor header metadata allowed')
        if not any(r['status'] in ('complete','complete_with_absences','mirror_historical_unverified_identity') and r['repo']==item.get('repo_id') and r['revision']==item.get('revision') for r in reports):raise ValueError('Unselected reference object')
        if item.get('kind')=='hf_file':
            if Path(item['path']).name not in ('config.json','tokenizer_config.json','tokenizer.json','special_tokens_map.json','added_tokens.json','generation_config.json'):raise ValueError('Non-reference file or weight payload forbidden')
        elif item.get('kind')!='safetensors_header' or item.get('artifact_role')!='tensor_header':raise ValueError('Weight payload forbidden')
    from .mirror_evidence import SCHEME, validate_selection
    for report in reports:
        selected=[i for i in bundle['items'] if i.get('repo_id')==report.get('repo') and i.get('revision')==report.get('revision')]
        if any(i.get('mirror_provenance',{}).get('scheme')==SCHEME for i in selected) and report.get('retrieval_source')!=SCHEME:
            raise ValueError('Mirror selection provenance missing')
        validate_selection(report,selected,cutoff)
    return bundle


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path('.sources/exllamav3.git'))
    parser.add_argument('--task',required=True);parser.add_argument('--selection',type=Path,required=True)
    parser.add_argument('--not-new-architecture-reason')
    parser.add_argument('--covered-by',type=Path,help='JSON list of prior branch bundle paths and SHA256s')
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--cache',type=Path,required=True)
    a=parser.parse_args();a.cache.mkdir(parents=True,exist_ok=True)
    cutoff=git(a.repo,'show','-s','--format=%cI',a.task).decode().strip();items=[];reports=[]
    details=trigger_details(a.repo,a.task);choices=json.loads(a.selection.read_text());outcome=None
    if a.not_new_architecture_reason or a.covered_by or (details['class_files'] and set(details['class_files'])==set(details['renames']) and not details['registry_architectures'] and not details['derived_architectures']):
        if choices:raise ValueError('Non-architecture outcome must not attach selections')
        outcome=administrative_outcome(a.repo,a.task,reason=a.not_new_architecture_reason,
            covered_by=json.loads(a.covered_by.read_text()) if a.covered_by else None)
    for i,choice in enumerate(choices):
        if not choice.get('reason') or not choice.get('candidates_considered'):raise ValueError('Explain selection using cutoff-eligible sources')
        if choice.get('retrieval_source')=='modelscope_hash_verified_v1':
            from .mirror_evidence import recover_modelscope
            evidence,report=recover_modelscope(choice['architecture'],a.cache/str(i),repo=choice['repo'],
                mirror_repo=choice['mirror_repo'],historical_repo=choice['historical_repo'],cutoff=cutoff,historical_copies=choice.get('historical_copies'))
        elif choice.get('retrieval_source') is None:
            evidence,report=recover_hf(choice['architecture'],a.cache,repo=choice['repo'],cutoff=cutoff,reference_only=True)
        else:raise ValueError('Unknown reference retrieval source')
        # Distinct IDs if multiple repositories represent the same architecture.
        for item in evidence:item['source_id']=f'reference:{i}:'+item['source_id']
        items.extend(evidence);reports.append(dict(report,reason=choice['reason'],candidates_considered=choice['candidates_considered']))
    bundle={'task_sha':a.task,'cutoff':cutoff,'trigger':trigger(a.repo,a.task),'items':items,'selections':reports,'trigger_details':details,
            'unresolved_architecture_files':details['unresolved_class_files']}
    if outcome is not None:bundle['administrative_outcome']=outcome
    if a.output.exists():raise ValueError('Use a new recovery output')
    write_json(a.output,bundle);load_bundle(a.repo,a.task,a.output)
    print(json.dumps({'path':str(a.output),'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'objects':len(items)}))


if __name__=='__main__':main()
