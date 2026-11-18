"""Administrative detached preflight handoff; never teacher input."""
from pathlib import Path
import sys,time,runpy,traceback
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from teacher.cycle_notify import notify
from teacher.cycle import write_json
preflight=ROOT/'reports/commit-000225-replacement-preflight-002.json'
supervisor=ROOT/'reports/commit-000225-replacement-002.py'
try:
    deadline=time.monotonic()+7200
    while not (preflight.exists() and supervisor.exists()):
        if time.monotonic()>deadline:raise TimeoutError('Header preflight did not finish; no teacher started by launcher')
        time.sleep(10)
    runpy.run_path(str(supervisor),run_name='__main__')
except BaseException as e:
    traceback.print_exc()
    r=dict(position=225,replacement=True,status='replacement_launch_failed',returncode=1,detail=str(e))
    write_json(ROOT/'reports/commit-000225-replacement-launch-002.result.json',r)
    notify('01a1da07-7653-7b81-8507-f69683828acb',r,ROOT/'reports',225)
