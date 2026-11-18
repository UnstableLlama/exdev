"""Wait for local preflight assets before the authorised detached replacement."""
import json
import runpy
import sys
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from teacher.cycle_notify import notify
ready=[ROOT/'reports/commit-000234-replacement-preflight-002.json',ROOT/'reports/commit-000255-ledger-validation-004.json']
deadline=time.monotonic()+3600
while not all(p.exists() for p in ready):
    if time.monotonic()>=deadline:
        result=dict(position=234,status='preflight_handoff_failed',detail='Local preflight assets did not finish; no teacher started')
        notify('01a1da07-7653-7b81-8507-f69683828acb',result,ROOT/'reports',234)
        raise SystemExit(1)
    time.sleep(5)
assert json.loads(ready[0].read_text())['status']=='local_passed_pending_isolated_probe'
assert json.loads(ready[1].read_text())['status']=='passed'
runpy.run_path(str(ROOT/'reports/commit-000234-replacement-002.py'),run_name='__main__')
