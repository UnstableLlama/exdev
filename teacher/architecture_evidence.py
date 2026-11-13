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


def trigger(repo,sha):
    parents=git(repo,'show','-s','--format=%P',sha).decode().split()
    before,files=inventory(repo,parents[0] if parents else None);after,newfiles=inventory(repo,sha)
    if parents and not newfiles:
        raise ValueError('Architecture location unknown: no model/config classes in known directories')
    return {'architectures':sorted(after-before),'class_files':sorted(set(newfiles)-set(files))}


def load_bundle(repo,sha,path):
    expected=trigger(repo,sha)
    if not any(expected.values()):return None
    if not path.is_file():raise ValueError('Architecture reference recovery required before authoring')
    bundle=json.loads(path.read_text());cutoff=git(repo,'show','-s','--format=%cI',sha).decode().strip()
    if bundle.get('task_sha')!=sha or bundle.get('cutoff')!=cutoff or bundle.get('trigger')!=expected:
        raise ValueError('Architecture reference task/cutoff/trigger mismatch')
    reports=bundle.get('selections',[])
    if not reports:raise ValueError('Architecture reference selection report required')
    covered=set()
    for report in reports:
        if not report.get('reason') or not report.get('candidates_considered'):raise ValueError('Reference selection provenance required')
        if report['status'] not in ('complete','no_eligible_revision'):raise ValueError('Incomplete reference recovery')
        covered.add(report['architecture'])
        if report['status']=='complete':
            if timestamp(report['date'])>timestamp(cutoff):raise ValueError('Reference revision after cutoff')
            items=[x for x in bundle['items'] if x.get('repo_id')==report['repo'] and x.get('revision')==report['revision']]
            paths={x['path'] for x in items if x.get('kind')=='hf_file'}
            if not {'config.json','tokenizer_config.json'}<=paths or not any(x.get('kind')=='safetensors_header' for x in items):raise ValueError('Incomplete reference roles')
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
        if not any(r['status']=='complete' and r['repo']==item.get('repo_id') and r['revision']==item.get('revision') for r in reports):raise ValueError('Unselected reference object')
        if item.get('kind')=='hf_file':
            if Path(item['path']).name not in ('config.json','tokenizer_config.json','tokenizer.json','special_tokens_map.json','added_tokens.json','generation_config.json'):raise ValueError('Non-reference file or weight payload forbidden')
        elif item.get('kind')!='safetensors_header' or item.get('artifact_role')!='tensor_header':raise ValueError('Weight payload forbidden')
    return bundle


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=Path('.sources/exllamav3.git'))
    parser.add_argument('--task',required=True);parser.add_argument('--selection',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--cache',type=Path,required=True)
    a=parser.parse_args();a.cache.mkdir(parents=True,exist_ok=True)
    cutoff=git(a.repo,'show','-s','--format=%cI',a.task).decode().strip();items=[];reports=[]
    for i,choice in enumerate(json.loads(a.selection.read_text())):
        if not choice.get('reason') or not choice.get('candidates_considered'):raise ValueError('Explain selection using cutoff-eligible sources')
        evidence,report=recover_hf(choice['architecture'],a.cache,repo=choice['repo'],cutoff=cutoff,reference_only=True)
        # Distinct IDs if multiple repositories represent the same architecture.
        for item in evidence:item['source_id']=f'reference:{i}:'+item['source_id']
        items.extend(evidence);reports.append(dict(report,reason=choice['reason'],candidates_considered=choice['candidates_considered']))
    bundle={'task_sha':a.task,'cutoff':cutoff,'trigger':trigger(a.repo,a.task),'items':items,'selections':reports}
    if a.output.exists():raise ValueError('Use a new recovery output')
    write_json(a.output,bundle);load_bundle(a.repo,a.task,a.output)
    print(json.dumps({'path':str(a.output),'sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'objects':len(items)}))


if __name__=='__main__':main()
