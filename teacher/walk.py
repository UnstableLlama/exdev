# SPDX-License-Identifier: MIT
"""Author sequentially until a full-review draft or failure; never auto-resume a stop."""
import argparse
import json
from pathlib import Path
from .author import author, write_json
from .packet import build_packet, git
from .graph_packet import attach_graphs
from .ancestor_context import attach_entries
from .approval_policy import assess, approve_mechanical

ROOT=Path(__file__).resolve().parents[1]


def resume(state_path, auth_file):
    state_path=Path(state_path);state=json.loads(state_path.read_text())
    if state['status']!='ready':raise ValueError('Walk is stopped; explicit review/recovery is required')
    repo=ROOT/'.sources/exllamav3.git'
    order=git(repo,'rev-list','--reverse','--topo-order',state['history_tip']).decode().split()
    while state['next_position']<=len(order):
        position=state['next_position'];sha=order[position-1]
        packet=ROOT/f'.teacher/retrieval/{position:06d}-001'
        run=ROOT/f'.teacher/runs/commit-{position:06d}-001'
        record={'position':position,'sha':sha,'run':str(run.relative_to(ROOT)),
                'packet':str(packet.relative_to(ROOT)),'status':'preparing'}
        state['runs'].append(record);state['status']='running';write_json(state_path,state)
        try:
            m=build_packet(repo,sha,packet)
            m.update(editorial_schema_version=4,ancestor_context_mode='retrieval_v1',ancestor_matches_version=1)
            write_json(packet/'manifest.json',m);attach_graphs(packet,ROOT/'store')
            sources=[ROOT/p for p in state['approved_entries']]
            # Merge ancestry may exclude entries on another branch. Filter by packet allowlist.
            selected=[]
            for source in sources:
                filename='entry.json' if (source/'entry.json').exists() else 'draft.json'
                if json.loads((source/filename).read_text())['sha'] in m['commits']:selected.append(source)
            attach_entries(packet,selected)
            record['status']='authoring';write_json(state_path,state)
            author(packet,run,auth_file)
            decision=assess(run,packet,repo);record.update(decision)
            if decision['tier']=='full_review':
                record['status']='pending_full_review';state['status']='awaiting_full_review'
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
    p.add_argument('--auth-file',type=Path,default=Path.home()/'.codex/auth.json');a=p.parse_args()
    print(json.dumps(resume(a.state,a.auth_file),indent=2))


if __name__=='__main__':main()
