"""One-off authorised retry supervisor; administrative only."""
import json
import sys
import traceback
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from teacher.cycle import digest, write_json
from teacher.cycle_notify import notify
from orchestration.run_ahead import recover, prepared
state_path = ROOT / 'reports/teacher-walk-001.json'
verdict = ROOT / 'reviews/verdicts/commit-000277-retry-recovery-002.md'
spec_path = ROOT / 'reports/commit-000277-prepared-002-retry.spec.json'
result_path = ROOT / 'reports/commit-000277-prepared-002-retry.result.json'
result = dict(position=277, result_path=str(result_path))
try:
    assert not (ROOT / '.teacher/runs/commit-000277-002').exists()
    assert not result_path.exists()
    spec = json.loads(spec_path.read_text())
    assert digest(verdict) == spec['authorization']['sha256']
    state = json.loads(state_path.read_text())
    assert state['active_session'] is None
    assert state['queue_stop']['run'] == '.teacher/runs/commit-000277-001'
    queue = state.get('review_queue', state.get('queue', []))
    assert any(q['position'] == 278 and q['status'] == 'pending_full_review' for q in queue)
    backup = ROOT / 'reports/commit-000277-before-recovery-002-retry.json'
    assert not backup.exists()
    backup.write_bytes(state_path.read_bytes())
    recover(state_path, verdict, retry_position=277)
    result.update(prepared(state_path, Path.home() / '.codex/auth.json', spec_path), returncode=0)
except BaseException as error:
    traceback.print_exc()
    result.update(status='prepared_failed', returncode=1, error_type=type(error).__name__, detail=str(error))
finally:
    write_json(result_path, result)
    notify('01a1da07-7653-7b81-8507-f69683828acb', result, ROOT / 'reports', 277)
print(json.dumps(result), flush=True)
