# SPDX-License-Identifier: MIT
"""Wait for the existing walk, then audit all requested commits without changing source data."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import time
from .validate import ROOT
from .verify import audit


def final_audit(store,state):
    if state.get('status')!='complete':raise ValueError('Walk did not complete: '+str(state.get('status')))
    result=audit(store,state['target_position'])
    if result['through_position']!=state['target_position']:raise ValueError('Audit did not reach requested final position')
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--store',type=Path,default=ROOT/'store')
    a=p.parse_args();status=a.store/'final-audit-status.json'
    state=dict(status='waiting',pid=os.getpid(),started_at=datetime.now(timezone.utc).isoformat())
    def save():
        tmp=status.with_suffix('.tmp');tmp.write_text(json.dumps(state,indent=2)+'\n');tmp.replace(status)
    save()
    try:
        walk=json.loads((a.store/'walk-status.json').read_text())
        run_started=walk['started_at']
        while walk['status'] in ('running','stopping'):
            # This watcher follows one specific run; it never restarts or edits it.
            os.kill(walk['pid'],0)
            time.sleep(10)
            walk=json.loads((a.store/'walk-status.json').read_text())
            if walk['started_at']!=run_started:raise ValueError('Walk was replaced; restart final auditor for the new run')
        state['status']='auditing';save()
        result=final_audit(a.store,walk)
        (a.store/'final-graph-audit.json').write_text(json.dumps(result,indent=2)+'\n')
        state.update(status='passed',through_position=result['through_position'],through_sha=result['through_sha'])
    except Exception as e:
        state.update(status='failed',error=str(e));raise
    finally:
        state['updated_at']=datetime.now(timezone.utc).isoformat();save()

if __name__=='__main__':main()
