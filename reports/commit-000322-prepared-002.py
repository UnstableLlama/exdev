"""Supervise the one authorised 322/002 attempt and notify the author."""
import json
import os
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestration.run_ahead import prepared, recover
from teacher.cycle import digest, write_json
from teacher.cycle_notify import notify


def main():
    thread = os.environ['CODEX_THREAD_ID']
    state_path = ROOT / 'reports/teacher-walk-001.json'
    base = ROOT / 'reports/commit-000322-prepared-002'
    spec_path = base.with_suffix('.spec.json')
    result_path = base.with_suffix('.result.json')
    backup = ROOT / 'reports/commit-000322-before-recovery-002.json'
    with backup.open('xb') as snapshot:
        state_bytes = state_path.read_bytes()
        snapshot.write(state_bytes)
    result = dict(position=322, result_path=str(result_path))
    try:
        assert not result_path.exists()
        state = json.loads(state_bytes)
        assert state['status'] == 'stopped_failure' and state['next_position'] == 322
        assert not state['active_session'] and not state.get('advancement_pause')
        assert state['queue_stop']['position'] == 322 and not state.get('retry_only')
        spec = json.loads(spec_path.read_text())
        assert spec['position'] == 322 and spec['kind'] == 'forward'
        assert spec['run'] == '.teacher/runs/commit-000322-002'
        assert spec['packet'] == '.teacher/retrieval/000322-002'
        assert spec['original_packet'] == '.teacher/retrieval/000322-001'
        assert not (ROOT / spec['run']).exists()
        decision = ROOT / 'reviews/verdicts/commit-000322-recovery-001.md'
        assert ROOT / spec['authorization']['path'] == decision
        assert digest(decision) == spec['authorization']['sha256'] == (
            'cf75ef0262c80a3b955e79d7bd221bf13bf1c85024d2a169bc573e872acbe5a3'
        )
        assert digest(ROOT / spec['packet'] / 'manifest.json') == digest(
            ROOT / spec['original_packet'] / 'manifest.json'
        )
        recover(state_path, decision, retry_position=322)
        result.update(prepared(state_path, Path.home() / '.codex/auth.json', spec_path), returncode=0)
    except BaseException as error:
        traceback.print_exc()
        result.update(status='prepared_failed', returncode=1, error_type=type(error).__name__, detail=str(error))
    write_json(result_path, result)
    print(json.dumps(result), flush=True)
    notify(thread, result, ROOT / 'reports', 322)
    return result['returncode']


if __name__ == '__main__':
    sys.exit(main())
