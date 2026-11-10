# SPDX-License-Identifier: MIT
"""Administrative append-only findings; no teacher or training integration."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re

REQUIRED={'defect_id','revision_id','supersedes','origin','classification','status','description',
          'trigger','expected_behavior','actual_behavior','introductions','observations','fixes',
          'verification','evidence','recorded_at','reviewed_at','reviewer','affected_revisions','dependencies'}


def dependency_identity(dep):
    if 'sha' in dep:
        if not re.fullmatch('[0-9a-f]{40}',dep['sha']):raise ValueError('Invalid evidence revision')
        return dep['repository'],dep['sha']
    if not dep.get('source_id') or not dep.get('url') or not re.fullmatch('[0-9a-f]{64}',dep.get('content_sha256','')):
        raise ValueError('Invalid external evidence dependency')
    return dep['url'],dep['content_sha256']


def validate(record):
    if not REQUIRED<=record.keys():raise ValueError('Missing retrospective fields')
    for key in ('defect_id','revision_id'):
        if not re.fullmatch('[a-z0-9][a-z0-9-]*',record[key]):raise ValueError('Unsafe record identity')
    if record['origin'] not in ('authoring_observation','fix_derived'):raise ValueError('Unknown origin')
    if record['status'] not in ('suspected','confirmed','disputed','refuted'):raise ValueError('Unknown status')
    if record['classification'] not in ('defect','behavior_change','new_requirement','external_compatibility','unresolved'):raise ValueError('Unknown classification')
    if not record['dependencies'] or not record['evidence']:raise ValueError('Evidence closure required')
    for dep in record['dependencies']:
        dependency_identity(dep)
        if datetime.fromisoformat(dep['available_at']).tzinfo is None:raise ValueError('Timezone required')
    if record['origin']=='fix_derived':
        dependencies={dependency_identity(d) for d in record['dependencies']}
        if not record['fixes'] or any((f['repository'],f['sha']) not in dependencies for f in record['fixes']):
            raise ValueError('Fix-derived record must depend on its fixing revisions')


def append(directory, record):
    validate(record);directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    for item in record['evidence']:
        path=directory/item['file']
        if path.is_symlink() or not path.resolve().is_relative_to(directory.resolve()):raise ValueError('Unsafe evidence path')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Evidence hash mismatch')
    existing=sorted(directory.glob(record['defect_id']+'--*.json'))
    previous=[json.loads(p.read_text()) for p in existing]
    leaves={r['revision_id'] for r in previous}-{r['supersedes'] for r in previous if r['supersedes']}
    if (previous and leaves!={record['supersedes']}) or (not previous and record['supersedes'] is not None):
        raise ValueError('Revision must supersede the current leaf')
    target=directory/(record['defect_id']+'--'+record['revision_id']+'.json')
    with target.open('x') as stream:stream.write(json.dumps(record,indent=2)+'\n')
    return target


def eligible_revisions(records, cutoff, allowed_revisions):
    """Select by full evidence closure before applying revisions; not a sample engine."""
    cutoff=datetime.fromisoformat(cutoff)
    if cutoff.tzinfo is None:raise ValueError('Timezone required')
    eligible=[]
    for record in records:
        validate(record)
        if all(dependency_identity(d) in allowed_revisions and datetime.fromisoformat(d['available_at'])<=cutoff for d in record['dependencies']):
            eligible.append(record)
    superseded={(r['defect_id'],r['supersedes']) for r in eligible if r['supersedes']}
    return [r for r in eligible if (r['defect_id'],r['revision_id']) not in superseded]
