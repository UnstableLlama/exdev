# SPDX-License-Identifier: MIT
"""Trusted approval/export; packet-only reads live in the isolated worker."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from .ancestor_context import read_regular
from .author import write_json

ASSEMBLY_ARTIFACTS = ('entry.json', 'entry.md', 'provenance.json')


def hashes(directory, names):
    return {n: hashlib.sha256(read_regular(directory/n)).hexdigest() for n in names}


def approve_assembly(directory, selection, packets, plan, reviewer, note, root=None):
    from .assembly import build, render, ROOT
    directory = Path(directory)
    root = Path(root) if root is not None else ROOT
    if not reviewer.strip() or not note.strip():
        raise ValueError('Reviewer and rationale are required')
    review = json.loads(read_regular(directory/'review.json'))
    if review.get('status') != 'pending':
        raise ValueError('Assembly must be pending review')
    bound = hashes(directory, ASSEMBLY_ARTIFACTS)
    provenance = json.loads(read_regular(directory/'provenance.json'))
    configs = [read_regular(Path(p)) for p in (selection, packets, plan)]
    for key, raw in zip(('selection_sha256','packets_map_sha256','plan_sha256'), configs):
        if hashlib.sha256(raw).hexdigest() != provenance[key]:
            raise ValueError('Assembly configuration fingerprint mismatch')
    entry, sources = build(*(json.loads(c) for c in configs), root=root)
    if (entry != json.loads(read_regular(directory/'entry.json')) or
        render(entry).encode() != read_regular(directory/'entry.md') or
        sources != provenance['sources'] or review.get('sha') != entry['sha'] or
        provenance['artifacts_sha256'] != {n:bound[n] for n in ('entry.json','entry.md')}):
        raise ValueError('Assembly does not replay exactly')
    if hashes(directory, ASSEMBLY_ARTIFACTS) != bound:
        raise ValueError('Assembly changed during approval')
    review.update(status='approved', ancestor_context_approved=True,
                  canonical_approved=False, training_eligible=False,
                  approved_artifacts=bound, reviewer=reviewer,
                  chapter_files={c['id']:c['files'] for c in json.loads(configs[2])['chapters']},
                  chapter_plan_sha256=provenance['plan_sha256'],
                  reviewed_at=datetime.now(timezone.utc).isoformat(), review_log=[note])
    write_json(directory/'review.json', review)
    return review


def prose(value):
    """Retain authored text and basis labels; discard old-session citation pointers."""
    if isinstance(value, dict):
        return {k:prose(v) for k,v in value.items()
                if k not in ('evidence','source_evidence','schema_version')}
    if isinstance(value, list):
        return [prose(v) for v in value]
    return value


def attach(packet, runs, manifest):
    from .worker import load_blob
    entries = {}
    assignments = {}
    for run in map(Path, runs):
        review = json.loads(read_regular(run/'review.json'))
        assembly = (run/'entry.json').exists()
        names = ASSEMBLY_ARTIFACTS if assembly else ('draft.json','raw-transcript.json','provenance.json')
        bound = hashes(run, names)
        if (review.get('status') != 'approved' or not review.get('reviewer') or
            not review.get('reviewed_at') or review.get('approved_artifacts') != bound or
            (assembly and review.get('ancestor_context_approved') is not True)):
            raise ValueError('Ancestor lacks hash-bound approval')
        entry = json.loads(read_regular(run/('entry.json' if assembly else 'draft.json')))
        sha = entry['sha']
        if sha not in manifest['commits'] or sha in entries or review.get('sha') != sha:
            raise ValueError('Duplicate or non-ancestor entry')
        source = manifest['commits'][sha]
        if entry['parent_shas'] != source['parents'] or entry['cutoff_date'] != source['date']:
            raise ValueError('Ancestor identity/date differs from Git history')
        if assembly:
            if entry.get('format') != 'root_chapter_assembly_v1' or entry['parent_shas']:
                raise ValueError('Invalid root assembly')
            chapters = {c['id']:prose(c['annotation']) for c in entry['chapters']}
            provenance=json.loads(read_regular(run/'provenance.json'))
            if review.get('chapter_plan_sha256') != provenance['plan_sha256'] or set(review.get('chapter_files',{})) != set(chapters):
                raise ValueError('Root search requires approved chapter file assignments')
            assignments[sha] = review['chapter_files']
            projected = {'sha':sha,'chapters':chapters}
            summary = 'Root implementation: ' + ', '.join(chapters)
        else:
            projected = {'sha':sha,'annotation':prose(entry['annotation'])}
            chapters = {c['id']:prose(c) for c in entry['annotation']['chapters']}
            summary = entry['annotation'].get('summary', '')
        if hashes(run, names) != bound:
            raise ValueError('Approved artifacts changed during export')
        entries[sha] = (projected, chapters, summary)
    if set(entries) != set(manifest['commits']) or set(manifest['history_order']) != set(entries) or len(manifest['history_order']) != len(entries):
        raise ValueError('Every strict ancestor needs exactly one approved entry')
    def store(value):
        raw = json.dumps(value, ensure_ascii=False).encode()
        digest = hashlib.sha256(raw).hexdigest()
        (packet/'blobs'/digest).write_bytes(raw)
        return digest
    refs, catalog, search = [], [], []
    graph_coverage = []
    def index(sha, chapter, file, symbol, basis):
        search.append({'sha':sha,'chapter':chapter,'file':file,'symbol':symbol,'match_basis':basis})
    for sha in manifest['history_order']:
        projected, chapters, summary = entries[sha]
        refs.append({'sha':sha,'prose_blob':store(projected),
                     'chapters':{key:store(value) for key,value in chapters.items()}})
        source = manifest['commits'][sha]
        files = source.get('files', [])
        mapping = assignments.get(sha,{})
        for file in files:
            targets=[chapter for chapter,paths in mapping.items() if file in paths] or ['']
            for chapter in targets:
                index(sha,chapter,file,'','root_file_assignment' if chapter else 'git_changed_file')
        if sha in manifest.get('graphs',{}):
            graph_coverage.append(sha)
            graph=manifest['graphs'][sha]
            if not source['parents']:
                snapshot=json.loads(load_blob(packet,graph['snapshot']))
                if snapshot['sha']!=sha or snapshot['parents']!=source['parents']:
                    raise ValueError('Search graph identity mismatch')
                for node in snapshot['nodes']:
                    for chapter,paths in mapping.items():
                        if node['file'] in paths:
                            index(sha,chapter,node['file'],node['qn'],'root_graph_symbol_file_join')
            else:
                for event in json.loads(load_blob(packet,graph['events'])):
                    if event['sha']!=sha:
                        raise ValueError('Search graph event identity mismatch')
                    index(sha,'',event['file'],event['qn'],'graph_symbol_event')
        annotations = chapters.items() if sha in assignments else [('',projected['annotation'])]
        for chapter,annotation in annotations:
            for finding in annotation.get('findings',[]):
                for location in finding['locations']:
                    if location['commit'] not in manifest['commits']:
                        raise ValueError('Finding location outside strict ancestry')
                    index(sha,chapter,location['path'],location['symbol'],'authored_finding_location')
        chapter_info=[]
        for key,value in chapters.items():
            ch = value.get('chapters',[value])[0]
            title = ch.get('title', key)
            claims = ch.get('claims',[]) or value.get('problem',[])
            focus = claims[0]['text'] if claims else ''
            chapter_info.append({'id':key,'title':title,'focus':focus[:400],
                                 'focus_source':'authored_claim_excerpt' if focus else 'unavailable',
                                 'focus_truncated':len(focus)>400})
        catalog.append({'sha':sha,'title':source.get('message','').split('\n')[0],
                        'summary':summary,'chapters':chapter_info,
                        'files_touched_count':len(files),'file_examples':files[:3],
                        'file_examples_truncated':len(files)>3})
    manifest.update(ancestor_entries=refs, ancestor_catalog_blob=store(list(reversed(catalog))),
                    ancestor_search_blob=store(search), ancestor_search_graph_commits=graph_coverage,
                    ancestor_context_complete=True)
    write_json(packet/'manifest.json', manifest)
    return len(refs)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assembly',type=Path,required=True)
    p.add_argument('--selection',type=Path,required=True)
    p.add_argument('--packets',type=Path,required=True)
    p.add_argument('--plan',type=Path,required=True)
    p.add_argument('--reviewer',required=True)
    p.add_argument('--note',required=True)
    a=p.parse_args()
    result=approve_assembly(a.assembly,a.selection,a.packets,a.plan,a.reviewer,a.note)
    print(json.dumps({'sha':result['sha'],'status':result['status'],'training_eligible':False}))


if __name__=='__main__':main()
