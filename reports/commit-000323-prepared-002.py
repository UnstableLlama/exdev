"""Supervise the single authorised 323 assisted retry and notify the author."""
import os
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestration.run_ahead import implementation_hashes, prepared, recover
from teacher.cycle import digest, read, write_json
from teacher.cycle_notify import notify


def main():
    thread = os.environ['CODEX_THREAD_ID']
    state_path = ROOT / 'reports/teacher-walk-001.json'
    base = ROOT / 'reports/commit-000323-prepared-002'
    spec_path = base.with_suffix('.spec.json')
    result_path = base.with_suffix('.result.json')
    assert not result_path.exists()
    result = dict(position=323, result_path=str(result_path))
    try:
        assert thread == '01a1eac6-cc72-7af3-9172-36689bd69fc9'
        state = read(state_path)
        spec = read(spec_path)
        old_run = '.teacher/runs/commit-000323-001'
        previous = next(row for row in state['review_queue'] if row.get('run') == old_run)
        assert previous['status'] == 'rejected' and state['queue_stop']['run'] == old_run
        assert state['next_position'] == 324 and not any(
            state.get(key) for key in ('active_session', 'advancement_pause', 'retry_only')
        )
        assert state['approved_entries'] == previous['approved_entries_snapshot']
        assert implementation_hashes() == previous['implementation_sha256']
        for path, expected in read(ROOT / old_run / 'provenance.json')['implementation_sha256'].items():
            assert digest(ROOT / path) == expected, path
        assert spec['position'] == 323 and spec['kind'] == 'forward'
        assert spec['run'] == '.teacher/runs/commit-000323-002' and not (ROOT / spec['run']).exists()
        assert spec['packet'] == spec['original_packet'] == '.teacher/retrieval/000323-002'
        decision = ROOT / spec['authorization']['path']
        assert decision == ROOT / 'reviews/verdicts/commit-000323-001.md'
        assert digest(decision) == spec['authorization']['sha256'] == previous['verdict_sha256']
        comparison_file = ROOT / spec['comparison']['path']
        assert digest(comparison_file) == spec['comparison']['sha256']
        comparison = read(comparison_file)
        assert comparison['original_packet'] == previous['packet']
        assert comparison['packet'] == spec['packet']
        assert digest(ROOT / previous['packet'] / 'manifest.json') == comparison['original_manifest_sha256']
        assert digest(ROOT / spec['packet'] / 'manifest.json') == comparison['manifest_sha256']
        coverage = comparison['coverage_request']
        assert digest(ROOT / coverage['path']) == coverage['sha256']
        assert comparison['approved_selection_verified'] and comparison['original_files_preserved']
        assert comparison['shared_readonly_blob_links_verified'] == 4570
        with (ROOT / 'reports/commit-000323-before-recovery-002.json').open('xb') as snapshot:
            snapshot.write(state_path.read_bytes())
        recover(state_path, decision, retry_position=323)
        print('323/002 retry reserved for prepared execution', flush=True)
        result.update(prepared(state_path, Path.home() / '.codex/auth.json', spec_path), returncode=0)
    except BaseException as error:
        traceback.print_exc()
        result.update(status='prepared_failed', returncode=1, error_type=type(error).__name__, detail=str(error))
    write_json(result_path, result)
    print(result, flush=True)
    notify(thread, result, ROOT / 'reports', 323)
    return result['returncode']


if __name__ == '__main__':
    sys.exit(main())
