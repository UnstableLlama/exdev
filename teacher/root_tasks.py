# SPDX-License-Identifier: MIT
"""Prepare independently scoped root chapters with exhaustive source assignments."""
import argparse
from collections import Counter
import json
from pathlib import Path
from .packet import build_packet, ROOT
from .root_evidence import TASK


def section_path(section):
    return section['header'].split(' b/',1)[1]


def validate_plan(plan, manifest):
    paths=[section_path(s) for s in manifest['task_change_sections']]
    assigned=[p for c in plan['chapters'] for p in c['files']]
    excluded=[e['path'] for e in plan['excluded']]
    if Counter(assigned+excluded)!=Counter(paths):
        raise ValueError('Plan must assign or explicitly exclude every file exactly once')
    ids=[c['id'] for c in plan['chapters']]
    if len(set(ids))!=len(ids):raise ValueError('Duplicate chapter assignment')
    for c in plan['chapters']:
        if not c['files'] or not c['focus']:raise ValueError('Empty chapter assignment')
    for e in plan['excluded']:
        s=manifest['task_change_sections'][paths.index(e['path'])]
        if not e['reason'] or not (s['binary'] or '/standard_cal_data/' in e['path'] or '/hadamard_data/' in e['path']):
            raise ValueError('Code and documentation cannot be excluded')


def task_for(chapter, manifest):
    paths=[section_path(s) for s in manifest['task_change_sections']]
    return {'kind':'chapter','id':chapter['id'],'focus':chapter['focus'],
            'required_sections':[paths.index(p) for p in chapter['files']],
            'required_evidence':chapter['required_evidence'],'reasoning_effort':'high'}


def validate_task(manifest):
    task=manifest.get('authoring_task')
    if task is None:
        if not manifest['task_parents']:
            raise ValueError('Root authoring requires a subsystem assignment')
        return
    if task['kind']!='chapter' or task['reasoning_effort']!='high' or not task['focus']:
        raise ValueError('Invalid chapter assignment')
    indices=task['required_sections']
    if not indices or len(set(indices))!=len(indices) or any(type(i) is not int or not 0<=i<len(manifest['task_change_sections']) for i in indices):
        raise ValueError('Invalid required source sections')
    available={e['source_id'] for e in manifest['evidence']}
    if not set(task['required_evidence'])<=available:
        raise ValueError('Assigned external evidence missing from packet')


def prepare(plan, bundle, destination):
    if not bundle.get('complete') or bundle['task_sha']!=TASK:
        raise ValueError('Complete root evidence recovery is required before authoring')
    destination=Path(destination)
    if destination.exists():raise ValueError('Destination already exists')
    # Build once before accepting assignments; builder validates every evidence hash/date.
    base=destination/'source'
    manifest=build_packet(ROOT/'.sources/exllamav3.git',TASK,base,bundle)
    validate_plan(plan,manifest)
    import shutil
    for chapter in plan['chapters']:
        packet=destination/chapter['id']
        shutil.copytree(base,packet)
        scoped=dict(manifest,authoring_task=task_for(chapter,manifest),graphs={},ancestor_context_complete=True)
        validate_task(scoped)
        (packet/'manifest.json').write_text(json.dumps(scoped,indent=2)+'\n')
    return len(plan['chapters'])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan',type=Path,default=ROOT/'schema/root-chapters-v1.json')
    p.add_argument('--evidence',type=Path,default=ROOT/'data/evidence/root/bundle.json')
    p.add_argument('--destination',type=Path,required=True)
    a=p.parse_args()
    print(prepare(json.loads(a.plan.read_text()),json.loads(a.evidence.read_text()),a.destination))

if __name__=='__main__':main()
