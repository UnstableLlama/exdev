# SPDX-License-Identifier: MIT
"""Trusted ancestor approval policy and conservative rejection propagation."""
import argparse
import json
from pathlib import Path, PurePosixPath
from .ancestor_context import approve_run, read_regular
from .author import write_json
from .packet import git
from .editorial import assemble_draft, render
from .coverage import run_coverage

POLICY='exdev-mechanical-ancestor'
VERSION=1
DENIED={'.py','.cu','.cuh','.cpp','.h','.json'}
IMAGES={'.png','.jpg','.jpeg','.gif','.svg','.webp','.ico','.bmp','.tif','.tiff','.avif'}


def allowed_path(path):
    p=PurePosixPath(path);suffix=p.suffix.lower();name=p.name.lower()
    if suffix in DENIED or name.startswith('requirements') or name=='setup.py':return False
    return (suffix=='.md' or suffix in IMAGES or path.startswith(('doc/','.github/'))
            or path in ('.gitignore','LICENSE','NOTICE'))


def tier(parents, files, annotation, validated):
    reasons=[]
    if len(parents)!=1:reasons.append('not_single_parent')
    if not files or any(not allowed_path(p) for p in files):reasons.append('nonmechanical_path')
    if annotation.get('findings') != []:reasons.append('findings_present_or_missing')
    def execution(value):
        if isinstance(value,dict):return value.get('basis')=='execution' or any(execution(v) for v in value.values())
        if isinstance(value,list):return any(execution(v) for v in value)
        return False
    if execution(annotation):reasons.append('execution_claim')
    if not validated:reasons.append('validation_incomplete')
    return {'tier':'full_review' if reasons else 'mechanical','reasons':reasons}


def sampled(sha):
    if len(sha)!=40 or any(c not in '0123456789abcdef' for c in sha):raise ValueError('Invalid commit SHA')
    return int(sha[:2],16)<0x1a


def assess(run, packet, repo):
    run,packet=Path(run),Path(packet)
    draft=json.loads(read_regular(run/'draft.json'));m=json.loads(read_regular(packet/'manifest.json'))
    transcript=json.loads(read_regular(run/'raw-transcript.json'))
    expected,_=assemble_draft(draft['annotation'],m,transcript)
    if expected!=draft or render(draft)!=read_regular(run/'draft.md').decode():raise ValueError('Replay mismatch')
    parents=git(repo,'show','-s','--format=%P',m['task_sha']).decode().split()
    if parents!=m['task_parents']:raise ValueError('Git parent mismatch')
    base=parents[0] if parents else git(repo,'hash-object','-t','tree','--stdin').decode().strip()
    files=git(repo,'diff','--no-renames','--name-only','-z',base,m['task_sha'],'--').decode().strip('\0').split('\0')
    if files==['']:files=[]
    if files!=m.get('task_changed_files'):raise ValueError('Changed paths disagree with trusted Git diff')
    coverage=run_coverage(packet,m,transcript)
    if coverage!=json.loads(read_regular(run/'coverage.json')):raise ValueError('Coverage report mismatch')
    decision=tier(parents,files,draft['annotation'],coverage['task_read_complete'])
    return dict(decision,policy=POLICY,version=VERSION,sampled=sampled(m['task_sha']),changed_files=files)


def approve_mechanical(run,packet,repo):
    decision=assess(run,packet,repo)
    if decision['tier']!='mechanical':raise ValueError('Full review required: '+', '.join(decision['reasons']))
    review=approve_run(run,packet,f'{POLICY}/v{VERSION}','Trusted mechanical-tier policy; ancestor retrieval only.')
    review.update(approval_kind='mechanical',approval_policy=decision,sample_review='pending' if decision['sampled'] else 'not_selected')
    write_json(Path(run)/'review.json',review)
    return decision


def reject_sample(state_path,run,note):
    """Conservatively invalidate every later run in the trusted chronological journal."""
    state_path=Path(state_path);state=json.loads(read_regular(state_path))
    indices=[i for i,r in enumerate(state['runs']) if r['run']==str(run)]
    if len(indices)!=1 or not note.strip():raise ValueError('Unknown run or missing rejection rationale')
    index=indices[0];record=state['runs'][index]
    if not record.get('sampled') or record.get('tier')!='mechanical':raise ValueError('Not a sampled mechanical approval')
    # Persist stop before any individual review mutation, so interruption cannot resume authoring.
    state.update(status='stopped_rejection',rejected_run=str(run),rejection_note=note)
    for i,r in enumerate(state['runs']):
        if i>=index:r['status']='rejected' if i==index else 'needs_reauthoring'
    write_json(state_path,state)
    for r in state['runs'][index:]:
        directory=Path(r['run'])
        review=json.loads(read_regular(directory/'review.json')) if (directory/'review.json').exists() else {}
        review.update(status=r['status'],ancestor_context_approved=False,canonical_approved=False,training_eligible=False,
                      invalidated_by=str(run),rejection_note=note)
        write_json(directory/'review.json',review)
    return state


def main():
    p=argparse.ArgumentParser();p.add_argument('--reject-sample',required=True);p.add_argument('--state',type=Path,required=True);p.add_argument('--note',required=True)
    a=p.parse_args();reject_sample(a.state,a.reject_sample,a.note)


if __name__=='__main__':main()
