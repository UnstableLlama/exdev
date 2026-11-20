"""Run the single authorized 336/002 prepared attempt and notify the author."""
import json
import os
import re
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestration.run_ahead import prepared, recover, verify_selection
from teacher.codex_adapter import EFFORT, MODEL
from teacher.cycle import digest, locked, read, write_new
from teacher.cycle_notify import notify


def main():
    reports = ROOT / 'reports'
    state_path = reports / 'teacher-walk-001.json'
    spec_path = reports / 'commit-000336-prepared-002.spec.json'
    result_path = reports / 'commit-000336-prepared-002.result.json'
    request = ROOT / 'reviews/requests/commit-000336-recovery-002.md'
    verdict = ROOT / 'reviews/verdicts/commit-000336-recovery-002.md'
    packet = ROOT / '.teacher/retrieval/000336-002'
    run = ROOT / '.teacher/runs/commit-000336-002'
    audit_path = reports / 'commit-000336-002-packet-verification.json'
    verdict_hash = '0f16d70f714f3d40f7d1907da10709863f92c1dce8882d6b8520ce8b27a874ff'
    audit_hash = 'b31bdc22d57d069872f2c53bcf2c0d4bf88836b39902e807679dfd890f61800f'
    thread = os.environ['CODEX_THREAD_ID']
    assert thread == '01a1eac6-cc72-7af3-9172-36689bd69fc9'
    assert not result_path.exists()
    result = dict(position=336, result_path=str(result_path))
    try:
        assert digest(request) == '7b5e8a26d4e9726e2fe104ca2dc72fbf467ffe1eeef3dd460a57a7514ead0ad6'
        bindings = re.findall(r'^- ([^:\n]+): `([a-f0-9]{64})`$', request.read_text(), re.M)
        assert len(bindings) == 7
        for path, expected in bindings:
            assert digest(ROOT / path) == expected, path
        assert digest(verdict) == verdict_hash and digest(audit_path) == audit_hash
        audit = read(audit_path)
        manifest = read(packet / 'manifest.json')
        assert str(packet.relative_to(ROOT)) == audit['packet']
        assert digest(packet / 'manifest.json') == audit['manifest_sha256']
        assert manifest['guidance_version'] == 12 and manifest['walk_input_contract']['version'] == 8
        assert not manifest.get('coverage_request') and (MODEL, EFFORT) == ('gpt-6.2-sol', 'medium')
        assert not run.exists()
        with locked(state_path):
            state = read(state_path)
            assert state['status'] == 'stopped_failure' and state['next_position'] == 336
            assert not any(state.get(k) for k in ('active_session', 'advancement_pause', 'handover', 'retry_only'))
            stop = state['queue_stop']
            assert stop['position'] == 336 and '406120de17d241248245c251a6accfce.log' in stop['detail']
            assert len(verify_selection(packet, state['approved_entries'])) == 332
            assert state['approved_entries'][-1] == '.teacher/runs/commit-000335-001'
            with (reports / 'commit-000336-before-prepared-002.json').open('xb') as backup:
                backup.write(state_path.read_bytes())
            write_new(spec_path, dict(
                kind='forward', position=336, run=str(run.relative_to(ROOT)),
                packet=audit['packet'], original_packet=audit['packet'],
                authorization=dict(path=str(verdict.relative_to(ROOT)), sha256=verdict_hash),
                packet_verification=dict(path=str(audit_path.relative_to(ROOT)), sha256=audit_hash),
            ))
            recover(state_path, verdict, retry_position=336)
        result.update(prepared(state_path, Path.home() / '.codex/auth.json', spec_path), returncode=0)
    except Exception as error:
        traceback.print_exc()
        result.update(status='prepared_failed', returncode=1, error_type=type(error).__name__, detail=str(error))
    write_new(result_path, result)
    print(json.dumps(result), flush=True)
    notify(thread, result, reports, 336)
    return result['returncode']


if __name__ == '__main__':
    sys.exit(main())
