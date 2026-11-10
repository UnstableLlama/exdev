# SPDX-License-Identifier: MIT
"""Validate draft annotations against recorded tool evidence; never mark a draft reviewed."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

SCHEMA = json.loads((Path(__file__).resolve().parents[1]/'schema/editorial-annotation-v2.json').read_text())
SCHEMA_V4 = json.loads((Path(__file__).resolve().parents[1]/'schema/editorial-annotation-v4.json').read_text())
SCHEMA_V3 = json.loads((Path(__file__).resolve().parents[1]/'schema/editorial-annotation-v3.json').read_text())


def output_schema(manifest):
    """Constrain generation as well as post-validation to the actual supplied prose."""
    version=manifest.get('editorial_schema_version',2)
    if type(version) is not int or version not in (2,3,4):
        raise ValueError('Unsupported editorial schema version')
    schema=deepcopy(SCHEMA if version==2 else SCHEMA_V3 if version==3 else SCHEMA_V4)
    if version>=3:
        schema['properties']['findings']['items']['properties']['locations']['items']['properties']['commit']['enum']=sorted(set(manifest['commits'])|{manifest['task_sha']})
    allowed=sorted({e['sha'] for e in manifest.get('ancestor_entries',[])} & set(manifest['commits']))
    if allowed:
        schema['properties']['links']['items']['enum']=allowed
    else:
        schema['properties']['links']['maxItems']=0
    if manifest.get('authoring_task',{}).get('kind')=='chapter':
        schema['properties']['chapters']['minItems']=1
        schema['properties']['chapters']['maxItems']=1
        schema['properties']['chapters']['items']['properties']['id']['enum']=[manifest['authoring_task']['id']]
    task=manifest.get('authoring_task',{})
    if 'chapter_catalog' in task:
        chapter=schema['properties']['chapters']['items']
        allowed=[c['id'] for c in task['chapter_catalog'] if c['id']!=task['id']]
        refs={'type':'array','items':{'type':'string','minLength':1},'maxItems':len(allowed)}
        if allowed:refs['items']['enum']=allowed
        chapter['properties']['related_chapters']=refs
        chapter['required'].append('related_chapters')
    return schema


def validate_shape(value, schema, path='annotation'):
    """Small validator for this schema's deliberately bounded JSON Schema subset."""
    kind = schema['type']
    valid = {'object':isinstance(value,dict), 'array':isinstance(value,list),
             'string':isinstance(value,str), 'integer':type(value) is int}[kind]
    if not valid:
        raise ValueError(path+': wrong type')
    if 'const' in schema and value != schema['const']:
        raise ValueError(path+': incorrect version')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(path+': unknown value')
    if kind == 'object':
        if set(value) != set(schema['required']):
            raise ValueError(path+': missing or protected fields')
        for key, item in value.items():
            validate_shape(item,schema['properties'][key],path+'.'+key)
    elif kind == 'array':
        if not schema.get('minItems',0)<=len(value)<=schema['maxItems']:
            raise ValueError(path+': invalid number of items')
        for item in value:
            validate_shape(item,schema['items'],path+'[]')
    elif kind == 'string':
        if len(value.strip())<schema.get('minLength',0) or len(value)>schema.get('maxLength',1000000):
            raise ValueError(path+': invalid length')
        if 'pattern' in schema and not re.fullmatch(schema['pattern'],value):
            raise ValueError(path+': invalid format')


def evidence_ledger(transcript):
    calls, results = {}, {}
    for message in transcript:
        if message['role']=='assistant':
            for call in message.get('calls',[]):
                if call['id'].startswith('ancestor:') or call['id'] in calls:
                    raise ValueError('Duplicate evidence call ID')
                calls[call['id']] = call
        elif message['role']=='tool':
            identity=message['call_id']
            if identity not in calls or identity in results or message['name']!=calls[identity]['tool']:
                raise ValueError('Unmatched evidence result')
            result=json.loads(message['content'])
            results[identity]={'tool':message['name'],'arguments':calls[identity]['arguments'],
                               'result':result,'result_sha256':hashlib.sha256(message['content'].encode()).hexdigest()}
    return results


def validate_annotation(annotation, manifest, transcript):
    validate_shape(annotation,output_schema(manifest))
    from .coverage import require_coverage
    require_coverage(manifest,transcript)
    task=manifest.get('authoring_task')
    if task and task['kind']=='chapter':
        if len(annotation['chapters'])!=1 or annotation['chapters'][0]['id']!=task['id']:
            raise ValueError('Chapter output does not match assigned subsystem')
    ledger=evidence_ledger(transcript)
    if manifest.get('ancestor_context_mode') == 'retrieval_v1':
        for item in ledger.values():
            if item['tool'] == 'ancestor_read' and item['arguments'].get('mode') != 'content':
                item['catalog_only'] = True
    context={'ancestor:'+e['sha']:{'kind':'approved_ancestor_context','sha':e['sha'],'content_sha256':e['blob']}
             for e in manifest.get('ancestor_entries',[]) if 'blob' in e and e['sha'] in manifest['commits'] and manifest.get('ancestor_context_mode') != 'retrieval_v1'}
    claims=[claim for field in ('problem','reasoning','impact','source_notes') for claim in annotation[field]]
    chapter_ids=set()
    for chapter in annotation['chapters']:
        if chapter['id'] in chapter_ids:
            raise ValueError('Duplicate chapter ID')
        chapter_ids.add(chapter['id']);claims.extend(chapter['claims'])
        refs=chapter.get('related_chapters',[])
        if len(refs)!=len(set(refs)):raise ValueError('Duplicate chapter reference')
    for claim in claims:
        refs=claim['evidence']
        if not refs:
            raise ValueError('Claims, including inferences, need evidence anchors')
        if len(set(refs))!=len(refs):
            raise ValueError('Duplicate evidence anchor')
        for ref in refs:
            if ref not in context and (ref not in ledger or (ledger[ref]['result'].get('ok') is not True or ledger[ref].get('catalog_only'))):
                raise ValueError('Unknown or unsuccessful evidence call')
        if claim['basis']=='execution':
            runs=[ledger[ref] for ref in refs if ref in ledger and ledger[ref]['tool']=='run']
            if not any(r['result'].get('result',{}).get('returncode')==0 and
                       not r['result']['result'].get('timed_out',False) for r in runs):
                raise ValueError('Execution claims require successful run evidence')
    finding_ids=set()
    source_tools={'repo_read','git_show','git_diff','web_fetch','hf_fetch','safetensors_header'}
    def checked_refs(refs):
        if len(refs)!=len(set(refs)):
            raise ValueError('Duplicate finding evidence')
        if any(ref not in ledger or (ledger[ref]['result'].get('ok') is not True or ledger[ref].get('catalog_only')) for ref in refs):
            raise ValueError('Findings require successful current-session evidence')
        return [ledger[ref] for ref in refs]
    for finding in annotation.get('findings',[]):
        if finding['id'] in finding_ids:raise ValueError('Duplicate finding ID')
        finding_ids.add(finding['id'])
        sources=checked_refs(finding['source_evidence'])
        if not any(s['tool'] in source_tools for s in sources):
            raise ValueError('Findings require inspected source evidence')
        for location in finding['locations']:
            path=location['path']
            if path.startswith('/') or '\\' in path or any(p in ('','..','.') for p in path.split('/')):
                raise ValueError('Finding locations require repository-relative paths')
        for check in finding['verification']:
            evidence=checked_refs(check['evidence'])
            if check['method']=='source_inspection':
                if not any(e['tool'] in source_tools for e in evidence):
                    raise ValueError('Source inspection requires source evidence')
            elif not any(e['tool']=='run' and e['result'].get('result',{}).get('returncode')==0 and
                         not e['result']['result'].get('timed_out',False) for e in evidence):
                raise ValueError('Computational verification requires successful run evidence')
    approved={e['sha'] for e in manifest.get('ancestor_entries',[])}
    if len(set(annotation['links']))!=len(annotation['links']):
        raise ValueError('Duplicate ancestor link')
    if not set(annotation['links']) <= approved & set(manifest['commits']):
        raise ValueError('Links require approved, supplied ancestor prose')
    if manifest.get('ancestor_context_mode') == 'retrieval_v1':
        read_entries=set()
        for item in ledger.values():
            args=item['arguments']; result=item['result']
            content=result.get('result',{})
            if (item['tool']=='ancestor_read' and args.get('mode')=='content' and result.get('ok') is True
                and content.get('kind')=='ancestor_prose' and content.get('sha')==args.get('commit')
                and content.get('chapter','')==args.get('chapter','')
                and content.get('next_offset',0)>content.get('offset',0)):
                read_entries.add(args['commit'])
        if not set(annotation['links']) <= read_entries:
            raise ValueError('Ancestor links require a successful nonempty prose read in this session')
    return dict(ledger,**context)


def assemble_draft(annotation, manifest, transcript):
    ledger=validate_annotation(annotation,manifest,transcript)
    entry={'schema_version':annotation['schema_version'],'sha':manifest['task_sha'],'parent_shas':manifest['task_parents'],
           'cutoff_date':manifest['cutoff_date'],'annotation':deepcopy(annotation),
           'evidence':{key:{k:v for k,v in value.items() if k!='result'} for key,value in ledger.items()}}
    review={'schema_version':1,'sha':manifest['task_sha'],'status':'pending',
            'training_eligible':False,'checks':[],'review_log':[]}
    return entry,review


def render(entry):
    annotation=entry['annotation']
    parts=[f"# {entry['sha']}\n",'Draft — pending review.\n',
           'An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.',
           f"[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/{entry['sha']}) · [Evidence ledger](draft.json)"]
    if 'summary' in annotation:
        parts.append(annotation['summary'])
    if annotation['chapters']:
        parts.append('\n'.join(f"- [{c['title']}](#{c['id']})" for c in annotation['chapters']))
    for field in ('problem','reasoning','impact','source_notes'):
        if annotation[field]:
            parts.append('## '+field.replace('_',' ').title())
            parts.extend(c['text']+' ['+c['basis']+'; '+', '.join(c['evidence'])+']' for c in annotation[field])
    for chapter in annotation['chapters']:
        parts.append(f'<a id="{chapter["id"]}"></a>\n\n## {chapter["title"]}')
        parts.extend(c['text']+' ['+c['basis']+'; '+', '.join(c['evidence'])+']' for c in chapter['claims'])
        titles={c['id']:c['title'] for c in annotation['chapters']}
        refs=chapter.get('related_chapters',[])
        if refs:
            parts.append('Related chapters: '+', '.join(f'[{titles[r]}](#{r})' if r in titles else r+' (assembly link pending)' for r in refs))
    if annotation.get('findings'):
        parts.append('## Authoring-time findings — pending review')
        for finding in annotation['findings']:
            parts.append('### '+finding['id']+' ('+finding['status']+'; '+finding['classification']+')')
            parts.extend([finding['description'],'Trigger: '+finding['trigger'],
                          'Expected: '+finding['expected_behavior'],'Actual: '+finding['actual_behavior'],
                          'Locations: '+', '.join(loc['commit']+':'+loc['path']+' — '+loc['symbol'] for loc in finding['locations']),
                          'Source evidence: '+', '.join(finding['source_evidence'])])
            for check in finding['verification']:
                parts.append(check['method']+': '+check['description']+' ['+', '.join(check['evidence'])+']. Limits: '+check['limits'])
    if annotation['limitations']:
        parts.extend(['## Uncertainty and limits',*annotation['limitations']])
    return '\n\n'.join(parts)+'\n'
