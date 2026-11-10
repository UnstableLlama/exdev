# SPDX-License-Identifier: MIT
"""Validate draft annotations against recorded tool evidence; never mark a draft reviewed."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

SCHEMA = json.loads((Path(__file__).resolve().parents[1]/'schema/editorial-annotation-v2.json').read_text())


def output_schema(manifest):
    """Constrain generation as well as post-validation to the actual supplied prose."""
    schema=deepcopy(SCHEMA)
    allowed=sorted({e['sha'] for e in manifest.get('ancestor_entries',[])} & set(manifest['commits']))
    if allowed:
        schema['properties']['links']['items']['enum']=allowed
    else:
        schema['properties']['links']['maxItems']=0
    if manifest.get('authoring_task',{}).get('kind')=='chapter':
        schema['properties']['chapters']['minItems']=1
        schema['properties']['chapters']['maxItems']=1
        schema['properties']['chapters']['items']['properties']['id']['enum']=[manifest['authoring_task']['id']]
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
        if len(value)>schema['maxItems']:
            raise ValueError(path+': too many items')
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
    validate_shape(annotation,SCHEMA)
    from .coverage import require_coverage
    require_coverage(manifest,transcript)
    task=manifest.get('authoring_task')
    if task and task['kind']=='chapter':
        if len(annotation['chapters'])!=1 or annotation['chapters'][0]['id']!=task['id']:
            raise ValueError('Chapter output does not match assigned subsystem')
    ledger=evidence_ledger(transcript)
    context={'ancestor:'+e['sha']:{'kind':'approved_ancestor_context','sha':e['sha'],'content_sha256':e['blob']}
             for e in manifest.get('ancestor_entries',[]) if 'blob' in e and e['sha'] in manifest['commits']}
    claims=[claim for field in ('problem','reasoning','impact','source_notes') for claim in annotation[field]]
    chapter_ids=set()
    for chapter in annotation['chapters']:
        if chapter['id'] in chapter_ids:
            raise ValueError('Duplicate chapter ID')
        chapter_ids.add(chapter['id']);claims.extend(chapter['claims'])
    for claim in claims:
        refs=claim['evidence']
        if not refs:
            raise ValueError('Claims, including inferences, need evidence anchors')
        if len(set(refs))!=len(refs):
            raise ValueError('Duplicate evidence anchor')
        for ref in refs:
            if ref not in context and (ref not in ledger or ledger[ref]['result'].get('ok') is not True):
                raise ValueError('Unknown or unsuccessful evidence call')
        if claim['basis']=='execution':
            runs=[ledger[ref] for ref in refs if ref in ledger and ledger[ref]['tool']=='run']
            if not any(r['result'].get('result',{}).get('returncode')==0 and
                       not r['result']['result'].get('timed_out',False) for r in runs):
                raise ValueError('Execution claims require successful run evidence')
    approved={e['sha'] for e in manifest.get('ancestor_entries',[])}
    if len(set(annotation['links']))!=len(annotation['links']):
        raise ValueError('Duplicate ancestor link')
    if not set(annotation['links']) <= approved & set(manifest['commits']):
        raise ValueError('Links require approved, supplied ancestor prose')
    return dict(ledger,**context)


def assemble_draft(annotation, manifest, transcript):
    ledger=validate_annotation(annotation,manifest,transcript)
    entry={'schema_version':2,'sha':manifest['task_sha'],'parent_shas':manifest['task_parents'],
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
    if annotation['chapters']:
        parts.append('\n'.join(f"- [{c['title']}](#{c['id']})" for c in annotation['chapters']))
    for field in ('problem','reasoning','impact','source_notes'):
        if annotation[field]:
            parts.append('## '+field.replace('_',' ').title())
            parts.extend(c['text']+' ['+c['basis']+'; '+', '.join(c['evidence'])+']' for c in annotation[field])
    for chapter in annotation['chapters']:
        parts.append(f'<a id="{chapter["id"]}"></a>\n\n## {chapter["title"]}')
        parts.extend(c['text']+' ['+c['basis']+'; '+', '.join(c['evidence'])+']' for c in chapter['claims'])
    if annotation['limitations']:
        parts.extend(['## Uncertainty and limits',*annotation['limitations']])
    return '\n\n'.join(parts)+'\n'
