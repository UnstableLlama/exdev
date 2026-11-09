# SPDX-License-Identifier: MIT
"""Run a long graph walk with persistent status and forwarded termination."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys
from .validate import ROOT


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--stop-position',type=int,required=True);a=p.parse_args()
    store=ROOT/'store';store.mkdir(exist_ok=True)
    state=dict(status='running',target_position=a.stop_position,pid=os.getpid(),
               started_at=datetime.now(timezone.utc).isoformat(),last_position=0)
    path=store/'walk-status.json'
    def save():
        temp=path.with_suffix('.tmp');temp.write_text(json.dumps(state,indent=2)+'\n');temp.replace(path)
    save()
    child=subprocess.Popen([sys.executable,'-m','graph.index_commit','--stop-position',str(a.stop_position)],cwd=ROOT,
                           stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    state['worker_pid']=child.pid;save()
    def stop(signum,frame):
        state['status']='stopping';save();child.terminate()
    signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
    for line in child.stdout:
        print(line,end='',flush=True)
        first=line.split(' ',1)[0]
        if first.isdigit():state['last_position']=int(first);save()
    code=child.wait()
    state['exit_code']=code;state['finished_at']=datetime.now(timezone.utc).isoformat()
    state['status']='complete' if code==0 and state['last_position']==a.stop_position else 'failed'
    if (store/'timeline.sqlite').exists():
        with sqlite3.connect(f'file:{store}/timeline.sqlite?mode=ro',uri=True) as db:
            state['indexed_commits']=db.execute('SELECT count(*) FROM commits').fetchone()[0]
    save()
    return code if code else (0 if state['status']=='complete' else 1)

if __name__=='__main__':sys.exit(main())
