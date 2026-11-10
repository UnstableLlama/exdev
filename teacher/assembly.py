# SPDX-License-Identifier: MIT
"""Deterministically assemble accepted root chapters; never approve or publish them."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from .editorial import assemble_draft, render as render_chapter
from .coverage import require_coverage
from .root_tasks import validate_plan, validate_task, section_path

ROOT = Path(__file__).resolve().parents[1]
BOUND_ARTIFACTS = ('draft.json', 'draft.md', 'raw-transcript.json', 'provenance.json')


def read_bytes(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError('Assembly input must be a regular file: '+str(path))
    return path.read_bytes()


def read_json(path):
    return json.loads(read_bytes(path))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def local_path(root, value):
    path=Path(value)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('Assembly paths must be repository-relative')
    result=(root/path).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError('Assembly path escapes repository')
    return result


def scope_annotation(annotation, chapter):
    """Only identifiers change; every authored prose string remains untouched."""
    result=deepcopy(annotation)
    prefix=chapter+'::'
    claims=[c for field in ('problem','reasoning','impact','source_notes') for c in result[field]]
    for section in result['chapters']:
        claims.extend(section['claims'])
    for claim in claims:
        claim['evidence']=[prefix+ref for ref in claim['evidence']]
    for finding in result.get('findings',[]):
        finding['source_evidence']=[prefix+ref for ref in finding['source_evidence']]
        for check in finding['verification']:
            check['evidence']=[prefix+ref for ref in check['evidence']]
    return result


def build(selection, packets, plan, root=ROOT):
    root=Path(root)
    if selection.get('status')!='accepted_chapter_set_pending_assembly':
        raise ValueError('Selection must record accepted chapters')
    expected=[c['id'] for c in plan['chapters']]
    rows=selection['chapters']; selected={c['chapter']:c for c in rows}
    if len(set(expected))!=len(expected) or len(selected)!=len(rows) or set(selected)!=set(expected) or set(packets)!=set(expected):
        raise ValueError('Exactly one selected chapter and packet required for every assignment')
    entry={'format':'root_chapter_assembly_v1','sha':None,'parent_shas':[], 'cutoff_date':None,
           'chapters':[], 'evidence':{}}
    sources=[]; identity=None
    for assignment in plan['chapters']:
        chapter=assignment['id']; row=selected[chapter]
        if row.get('disposition')!='accepted_as_chapter':
            raise ValueError('Unaccepted chapter: '+chapter)
        run=local_path(root,row['run']); packet=local_path(root,packets[chapter])
        bound={name:read_bytes(run/name) for name in BOUND_ARTIFACTS}
        if any(row['artifacts_sha256'].get(name)!=sha(data) for name,data in bound.items()):
            raise ValueError('Accepted artifact hash mismatch: '+chapter)
        draft=json.loads(bound['draft.json']); transcript=json.loads(bound['raw-transcript.json'])
        provenance=json.loads(bound['provenance.json']); raw_manifest=read_bytes(packet/'manifest.json'); manifest=json.loads(raw_manifest)
        if provenance.get('packet_manifest_sha256')!=sha(raw_manifest):
            raise ValueError('Original packet fingerprint mismatch: '+chapter)
        if provenance.get('input_mode')!='entry_analysis' or provenance.get('published') is not False:
            raise ValueError('Invalid authoring provenance')
        if read_json(run/'status.json')!={'status':'draft','published':False}:
            raise ValueError('Only completed unpublished drafts can be assembled')
        validate_task(manifest); validate_plan(plan,manifest)
        task=manifest['authoring_task']
        paths=[section_path(manifest['task_change_sections'][i]) for i in task['required_sections']]
        if task['id']!=chapter or paths!=assignment['files'] or task['required_evidence']!=assignment['required_evidence']:
            raise ValueError('Chapter assignment differs from plan')
        if manifest['task_parents'] or manifest['commits'] or manifest['base_commit'] is not None or manifest['task_sha']!=plan['task_sha']:
            raise ValueError('Assembly only supports the assigned root commit')
        current=(manifest['task_sha'],manifest['cutoff_date'],manifest['shows'],manifest['task_change_sections'])
        if identity is not None and current!=identity:
            raise ValueError('Chapters do not share identical root source and cutoff')
        identity=current
        finals=[m['content'] for m in transcript if m['role']=='assistant' and 'content' in m]
        if not finals or json.loads(finals[-1])!=draft['annotation']:
            raise ValueError('Draft differs from original final model response')
        replay,_=assemble_draft(draft['annotation'],manifest,transcript)
        if replay!=draft or render_chapter(draft)!=bound['draft.md'].decode():
            raise ValueError('Original chapter cannot be replayed exactly')
        coverage=require_coverage(manifest,transcript)
        if coverage!=read_json(run/'coverage.json'):
            raise ValueError('Saved coverage differs from transcript')
        annotation=draft['annotation']
        if annotation['links']:
            raise ValueError('Root chapter cannot link to ancestors')
        refs=annotation['chapters'][0].get('related_chapters',[])
        if not set(refs)<=set(expected)-{chapter}:
            raise ValueError('Dangling or self chapter reference')
        for key,value in draft['evidence'].items():
            entry['evidence'][chapter+'::'+key]=deepcopy(value)
        entry['chapters'].append({'id':chapter,'annotation':scope_annotation(annotation,chapter)})
        sources.append({'chapter':chapter,'run':row['run'],'packet':packets[chapter],
                        'artifacts_sha256':{name:sha(data) for name,data in bound.items()},
                        'packet_manifest_sha256':sha(raw_manifest),'coverage':coverage,
                        'evidence_id_prefix':chapter+'::','source_annotation_version':annotation['schema_version']})
        # Check the original inputs again before returning a derived artifact.
        if any(read_bytes(run/name)!=data for name,data in bound.items()) or read_bytes(packet/'manifest.json')!=raw_manifest:
            raise ValueError('Input changed during assembly')
    entry['sha'],entry['cutoff_date']=identity[:2]
    return entry, sources


def render(entry):
    titles={c['id']:c['annotation']['chapters'][0]['title'] for c in entry['chapters']}
    parts=[f"# Root Encyclopedia entry — {entry['sha']}",
           'Assembly candidate — pending review. Not published or approved as ancestor context.',
           'An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.',
           f"[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/{entry['sha']}) · [Combined evidence ledger](entry.json)",
           '\n'.join(f'- [{title}](#{key})' for key,title in titles.items())]
    def claims(values):
        return [v['text']+' ['+v['basis']+'; '+', '.join(v['evidence'])+']' for v in values]
    for chapter in entry['chapters']:
        key=chapter['id']; a=chapter['annotation']; section=a['chapters'][0]
        parts.append(f'<a id="{key}"></a>\n\n## {section["title"]}')
        for field in ('problem','reasoning','impact'):
            if a[field]:parts.extend(['### '+field.title(),*claims(a[field])])
        parts.extend(['### Explanation',*claims(section['claims'])])
        if a['source_notes']:parts.extend(['### Source notes',*claims(a['source_notes'])])
        for f in a.get('findings',[]):
            parts.extend(['### Authoring-time finding: '+f['id']+' ('+f['status']+'; '+f['classification']+')',
                          f['description'],'Trigger: '+f['trigger'],'Expected: '+f['expected_behavior'],
                          'Actual: '+f['actual_behavior'],
                          'Locations: '+', '.join(loc['commit']+':'+loc['path']+' — '+loc['symbol'] for loc in f['locations']),
                          'Source evidence: '+', '.join(f['source_evidence'])])
            for check in f['verification']:
                parts.append(check['method']+': '+check['description']+' ['+', '.join(check['evidence'])+']. Limits: '+check['limits'])
        refs=section.get('related_chapters',[])
        if not set(refs)<=set(titles)-{key}:raise ValueError('Unresolved chapter navigation')
        if refs:parts.append('Related chapters: '+', '.join(f'[{titles[r]}](#{r})' for r in refs))
        if a['limitations']:parts.extend(['### Uncertainty and limits',*a['limitations']])
    return '\n\n'.join(parts)+'\n'


def save(selection_path, packets_path, plan_path, output, root=ROOT):
    inputs={Path(p):read_bytes(Path(p)) for p in (selection_path,packets_path,plan_path)}
    selection=json.loads(inputs[Path(selection_path)]); packets=json.loads(inputs[Path(packets_path)]); plan=json.loads(inputs[Path(plan_path)])
    entry,sources=build(selection,packets,plan,root)
    markdown=render(entry)
    if any(read_bytes(p)!=data for p,data in inputs.items()):
        raise ValueError('Assembly configuration changed during validation')
    output=Path(output)
    # New immutable output only. Validation completes before creating it.
    output.mkdir(parents=True,exist_ok=False)
    def write(name,value):
        (output/name).write_text(json.dumps(value,indent=2)+'\n')
    write('entry.json',entry);(output/'entry.md').write_text(markdown)
    write('provenance.json',{'format':'root_chapter_assembly_provenance_v1',
        'selection_sha256':sha(inputs[Path(selection_path)]), 'plan_sha256':sha(inputs[Path(plan_path)]),
        'packets_map_sha256':sha(inputs[Path(packets_path)]), 'assembler_sha256':sha(read_bytes(Path(__file__))),
        'sources':sources,'transformation':'Chapter ordering, navigation and run-scoped evidence IDs only; original prose preserved.',
        'external_findings_inventories_imported':False,
        'artifacts_sha256':{name:sha(read_bytes(output/name)) for name in ('entry.json','entry.md')}})
    write('review.json',{'status':'pending','sha':entry['sha'],'canonical_approved':False,
                        'ancestor_context_approved':False,'training_eligible':False})
    write('validation.json',{'status':'passed','chapters':len(sources),
        'source_sections':sum(len(s['coverage']['fully_read_sections']) for s in sources),
        'evidence_records':len(entry['evidence']),
        'serialized_entry_bytes':len(json.dumps(entry,ensure_ascii=False).encode()),
        'checks':['Accepted hashes verified','Original final responses and saved drafts replay exactly',
                  'Original packet hashes and full source coverage verified','Root source and cutoff agree',
                  'Every planned chapter selected exactly once','Chapter links resolve locally',
                  'Evidence IDs scoped by chapter','Administrative findings inventories excluded'],
        'limitations':['Assembly is not independently approved; canonical and ancestor publication remain blocked.',
                       'Existing ancestor exporter does not support this assembly format; a reviewed integration is still needed.']})
    return entry


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--selection',type=Path,required=True);p.add_argument('--packets',type=Path,required=True)
    p.add_argument('--plan',type=Path,default=ROOT/'schema/root-chapters-v1.json')
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();save(args.selection,args.packets,args.plan,args.output)
    print(args.output/'entry.md')


if __name__=='__main__':main()
