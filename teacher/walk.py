# SPDX-License-Identifier: MIT
"""Author sequentially until a full-review draft or failure; never auto-resume a stop."""
import argparse
import json
from pathlib import Path
from .author import author, write_json
from .packet import git
from .walk_inputs import prepare, validate_bundle
from .graph_packet import attach_graphs
from .ancestor_context import attach_entries
from .approval_policy import assess, approve_mechanical

ROOT=Path(__file__).resolve().parents[1]


def publish_review_request(state_path, request_path):
    """Expose a full-review stop only after its mailbox request is durable."""
    state_path,request_path=Path(state_path),Path(request_path)
    state=json.loads(state_path.read_text())
    if state.get('status')!='awaiting_review_request':
        raise ValueError('Walk is not waiting for a review request')
    handover=state.get('handover') or {};run=handover.get('full_review')
    if not run or not request_path.is_file() or request_path.is_symlink() or not request_path.read_text().strip():
        raise ValueError('A nonempty regular review request is required')
    record=next((r for r in reversed(state['runs']) if r.get('run')==run),None)
    if record is None or record.get('status')!='awaiting_review_request':
        raise ValueError('Review request does not match the pending run')
    record['status']='pending_full_review';state['status']='awaiting_full_review'
    handover['request']=str(request_path);write_json(state_path,state)
    return state


def resume(state_path, auth_file):
    state_path=Path(state_path);state=json.loads(state_path.read_text())
    if state.get('advancement_pause'):raise ValueError('Walk advancement is paused by user decision')
    if state['status']!='ready':raise ValueError('Walk is stopped; explicit review/recovery is required')
    repo=ROOT/'.sources/exllamav3.git'
    order=git(repo,'rev-list','--reverse','--topo-order',state['history_tip']).decode().split()
    while state['next_position']<=len(order):
        position=state['next_position'];sha=order[position-1]
        attempt=1
        while True:
            packet=ROOT/f'.teacher/retrieval/{position:06d}-{attempt:03d}'
            run=ROOT/f'.teacher/runs/commit-{position:06d}-{attempt:03d}'
            if not packet.exists() and not run.exists():break
            attempt+=1
        record={'position':position,'sha':sha,'run':str(run.relative_to(ROOT)),
                'packet':str(packet.relative_to(ROOT)),'status':'preparing'}
        state['runs'].append(record);state['status']='running';write_json(state_path,state)
        try:
            evidence_directory=ROOT/'data/evidence/github'
            m=prepare(repo,sha,position,packet,evidence_directory)
            attach_graphs(packet,ROOT/'store')
            sources=[ROOT/p for p in state['approved_entries']]
            # Merge ancestry may exclude entries on another branch. Filter by packet allowlist.
            selected=[]
            for source in sources:
                filename='entry.json' if (source/'entry.json').exists() else 'draft.json'
                if json.loads((source/filename).read_text())['sha'] in m['commits']:selected.append(source)
            attach_entries(packet,selected)
            record['status']='authoring';write_json(state_path,state)
            validate_bundle(packet,evidence_directory/f'{position:06d}-eligible.json')
            author(packet,run,auth_file)
            decision=assess(run,packet,repo);record.update(decision)
            if decision['tier']=='full_review':
                record['status']='awaiting_review_request';state['status']='awaiting_review_request'
                state['handover']={'full_review':record['run'],
                    'sampled_mechanical':[r['run'] for r in state['runs'] if r.get('tier')=='mechanical' and r.get('sampled') and not r.get('sample_handed_over')]}
                for r in state['runs']:
                    if r['run'] in state['handover']['sampled_mechanical']:r['sample_handed_over']=True
                write_json(state_path,state);return state
            approve_mechanical(run,packet,repo)
            record['status']='approved_mechanical';state['approved_entries'].append(record['run'])
            state['next_position']=position+1;state['status']='ready';write_json(state_path,state)
        except BaseException as error:
            record['status']='failed';state['status']='stopped_failure';state['error_type']=type(error).__name__
            write_json(state_path,state);raise
    state['status']='complete';write_json(state_path,state);return state


def main():
    p=argparse.ArgumentParser();p.add_argument('--state',type=Path,required=True)
    p.add_argument('--auth-file',type=Path,default=Path.home()/'.codex/auth.json')
    p.add_argument('--publish-review-request',type=Path);a=p.parse_args()
    result=(publish_review_request(a.state,a.publish_review_request)
            if a.publish_review_request else resume(a.state,a.auth_file))
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
