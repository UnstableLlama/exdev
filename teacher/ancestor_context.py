# SPDX-License-Identifier: MIT
"""Trusted approval and bounded export of reviewed, strict-ancestor explanations."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from .author import write_json
from .editorial import assemble_draft

MAX_CONTEXT_BYTES = 256 * 1024
ARTIFACTS = ('draft.json','raw-transcript.json','provenance.json')


def read_regular(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError('Review artifacts must be regular files')
    return path.read_bytes()


def artifact_hashes(run):
    return {name:hashlib.sha256(read_regular(run/name)).hexdigest() for name in ARTIFACTS}


def approve_run(run, packet, reviewer, note):
    """Administrative operation: a named reviewer accepts a specific draft, never a model tool."""
    run,packet=Path(run),Path(packet)
    if not reviewer.strip() or not note.strip():
        raise ValueError('Reviewer identity and review rationale are required')
    status=json.loads(read_regular(run/'status.json'))
    review=json.loads(read_regular(run/'review.json'))
    if status.get('status')!='draft' or review.get('status')!='pending':
        raise ValueError('Only a pending, completed draft can be approved')
    hashes=artifact_hashes(run)
    draft=json.loads(read_regular(run/'draft.json'))
    transcript=json.loads(read_regular(run/'raw-transcript.json'))
    provenance=json.loads(read_regular(run/'provenance.json'))
    raw_manifest=read_regular(packet/'manifest.json')
    manifest=json.loads(raw_manifest)
    if provenance.get('packet_manifest_sha256')!=hashlib.sha256(raw_manifest).hexdigest():
        raise ValueError('Original authoring packet fingerprint mismatch')
    if provenance.get('input_mode')!='entry_analysis' or provenance.get('published') is not False:
        raise ValueError('Run is not an unpublished historical annotation')
    expected,_=assemble_draft(draft['annotation'],manifest,transcript)
    if draft!=expected or review.get('sha')!=draft['sha']:
        raise ValueError('Draft identity or evidence differs from its recorded inputs')
    if artifact_hashes(run)!=hashes:
        raise ValueError('Artifacts changed during review validation')
    review.update(status='approved',training_eligible=False,approved_artifacts=hashes,
                  packet_manifest_sha256=provenance['packet_manifest_sha256'],
                  reviewer=reviewer,reviewed_at=datetime.now(timezone.utc).isoformat())
    review['review_log']=[*review.get('review_log',[]),note]
    write_json(run/'review.json',review)
    return review


def attach_entries(packet, runs, max_bytes=MAX_CONTEXT_BYTES):
    """Publish all approved strict ancestors atomically; fail rather than silently truncate."""
    packet=Path(packet)
    manifest=json.loads(read_regular(packet/'manifest.json'))
    if manifest.get('ancestor_context_complete'):
        raise ValueError('Ancestor context is already published')
    expected=set(manifest['commits'])
    entries={}
    for run in map(Path,runs):
        review=json.loads(read_regular(run/'review.json'))
        if review.get('status')!='approved' or not review.get('reviewer') or not review.get('reviewed_at'):
            raise ValueError('Ancestor entry lacks explicit reviewer approval')
        if review.get('approved_artifacts')!=artifact_hashes(run):
            raise ValueError('Approved ancestor artifacts changed after review')
        draft=json.loads(read_regular(run/'draft.json'))
        sha=draft.get('sha')
        if sha not in expected or sha in entries or review.get('sha')!=sha:
            raise ValueError('Ancestor identity is duplicate or outside the packet ancestry')
        source=manifest['commits'][sha]
        if draft.get('parent_shas')!=source['parents'] or draft.get('cutoff_date')!=source['date']:
            raise ValueError('Ancestor identity/date differs from Git history')
        # Export explanation and evidence references only. No review comments, raw model
        # messages, status bookkeeping, provider configuration or implementation metadata.
        entries[sha]={k:draft[k] for k in ('schema_version','sha','parent_shas','cutoff_date','annotation','evidence')}
    if set(entries)!=expected:
        raise ValueError('Every strict ancestor needs a reviewed replacement entry')
    ordered=[entries[sha] for sha in manifest['history_order']]
    if len(json.dumps(ordered,ensure_ascii=False).encode())>min(max_bytes,MAX_CONTEXT_BYTES):
        raise ValueError('Approved ancestor prose exceeds the context budget; retrieval support is required')
    references=[]
    for entry in ordered:
        data=json.dumps(entry,sort_keys=True).encode()
        digest=hashlib.sha256(data).hexdigest()
        (packet/'blobs'/digest).write_bytes(data)
        references.append({'sha':entry['sha'],'blob':digest})
    manifest.update(ancestor_entries=references,ancestor_context_complete=True)
    write_json(packet/'manifest.json',manifest)
    return len(references)


def load_entries(packet, manifest):
    """Load only verified published prose into a fresh task's initial context."""
    from .worker import load_blob
    refs=manifest.get('ancestor_entries',[])
    if not refs:
        if manifest.get('ancestor_context_complete') and manifest['commits']:
            raise ValueError('Complete ancestor context is empty')
        return []
    if not manifest.get('ancestor_context_complete'):
        raise ValueError('Ancestor context was not fully published')
    if [r['sha'] for r in refs]!=manifest['history_order']:
        raise ValueError('Ancestor context does not match ordered ancestry')
    result=[]
    for ref in refs:
        entry=json.loads(load_blob(Path(packet),ref['blob']))
        if entry['sha']!=ref['sha'] or entry['sha'] not in manifest['commits']:
            raise ValueError('Ancestor context blob identity mismatch')
        result.append(dict(entry,evidence_id='ancestor:'+entry['sha']))
    if len(json.dumps(result,ensure_ascii=False).encode())>MAX_CONTEXT_BYTES:
        raise ValueError('Ancestor context exceeds the model input budget')
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    approve=commands.add_parser('approve')
    approve.add_argument('--run',type=Path,required=True)
    approve.add_argument('--packet',type=Path,required=True)
    approve.add_argument('--reviewer',required=True)
    approve.add_argument('--note',required=True)
    attach=commands.add_parser('attach')
    attach.add_argument('--packet',type=Path,required=True)
    attach.add_argument('--run',type=Path,action='append',default=[])
    args=parser.parse_args()
    if args.command=='approve':
        result=approve_run(args.run,args.packet,args.reviewer,args.note)
        print(json.dumps({'sha':result['sha'],'status':result['status'],'training_eligible':False}))
    else:
        print(json.dumps({'ancestor_entries':attach_entries(args.packet,args.run)}))


if __name__=='__main__':main()
