"""Run the single authorized fresh 336/004 using the unchanged 336/002 packet."""
import json
import re
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestration.run_ahead import prepared, recover, verify_selection
from teacher.codex_adapter import EFFORT, MODEL
from teacher.cycle import digest, locked, read, relative, validate_packet_blobs, write_new

REPORTS = ROOT/'reports'
STATE = REPORTS/'teacher-walk-001.json'
SPEC = REPORTS/'commit-000336-prepared-004-path.spec.json'
RESULT = REPORTS/'commit-000336-prepared-004-path.result.json'
AUDIT = REPORTS/'commit-000336-recovery-004-path-application.json'
VERDICT = ROOT/'reviews/verdicts/commit-000336-recovery-004-path.md'
VERDICT_HASH = '0ee33cf7e3a0c22c36689bdc0de9de9877e8d3516ac954e32fcde0897f9e2236'
PACKET = ROOT/'.teacher/retrieval/000336-002'
RUN = ROOT/'.teacher/runs/commit-000336-004'
PREVIOUS = ROOT/'reviews/requests/commit-000336-repeated-failure-002.md'
PREVIOUS_AUDIT = REPORTS/'commit-000336-recovery-003-application.json'
PATCH = REPORTS/'codex-output-schema-implementation-001.patch'
HASHES = REPORTS/'codex-output-schema-implementation-001.hashes.json'
TESTS = REPORTS/'codex-output-schema-implementation-001-live-suite.log'


def require_idle_processes():
    for process in Path('/proc').iterdir():
        if not process.name.isdecimal():
            continue
        try:
            args = (process/'cmdline').read_bytes().split(b'\0')
        except (FileNotFoundError, PermissionError, ProcessLookupError):
            continue
        if any(arg in (b'orchestration.run_ahead', b'orchestration.notify', b'teacher.cycle',
                       b'teacher.cycle_notify', b'teacher.author') for arg in args[1:]):
            raise ValueError('A cycle supervisor or worker is alive')
        if any(re.fullmatch(rb'(?:.*/)?commit-000336-prepared-00[23]\.py', arg) for arg in args[1:]):
            raise ValueError('The previous prepared supervisor is alive')


def verify_and_recover():
    assert digest(VERDICT) == VERDICT_HASH
    assert digest(PATCH) == 'adcf1f27015b62ad90cf8368fac91c62c1be98733d283f5d71616470cfb91287'
    assert digest(HASHES) == '93ccfd8127eb3fda07359be9cc15793f921f14c57321eedbdde79dd14f67bfe9'
    assert re.search(r'Ran 355 tests.*\n\nOK\s*\Z', TESTS.read_text())
    hashes = read(HASHES)
    for name, expected in (hashes['candidate_production'] | hashes['candidate_changed_files']).items():
        assert digest(ROOT/name) == expected, name
    assert digest(PREVIOUS) == 'e55b3788a73a0f4373a15fcb9f15627fa64c67cd4570264fbcc468697936da2c'
    previous_files = dict(re.findall(r'^- (\.teacher/runs/[^:]+): `([a-f0-9]{64})`$', PREVIOUS.read_text(), re.M))
    assert len(previous_files) == 4
    assert digest(PREVIOUS_AUDIT) == 'b25c7a55fcb7667e0ef0e861c38f36a229bc2e79a09708e9407a7e46f21e6e60'
    previous_audit = read(PREVIOUS_AUDIT)
    previous_files.update(previous_audit['verified_previous_attempt_artifacts'])
    assert len(previous_files) == 10
    for name, expected in previous_files.items():
        assert digest(ROOT/name) == expected, name

    manifest_path = PACKET/'manifest.json'
    assert {p.name for p in PACKET.iterdir()} == {'manifest.json', 'blobs'}
    assert not any(p.is_symlink() for p in (PACKET, manifest_path, PACKET/'blobs'))
    manifest = read(manifest_path)
    assert digest(manifest_path) == 'a500a120a3563fb87c45f8bfc54a853410e28d00ce1efd9535326ac7c4c64de9'
    assert manifest['guidance_version'] == 12 and manifest['walk_input_contract']['version'] == 8
    assert not manifest.get('coverage_request') and (MODEL, EFFORT) == ('gpt-6.2-sol', 'medium')
    assert not RUN.exists()
    require_idle_processes()
    with locked(STATE):
        state = read(STATE)
        assert state['status'] == 'stopped_failure' and state['next_position'] == 336
        assert not any(state.get(key) for key in ('active_session', 'advancement_pause', 'handover'))
        assert state['queue_stop']['run'] == '.teacher/runs/commit-000336-003'
        assert state['queue_stop']['position'] == 336
        # A failed prepared run retains the prior retry restriction. Recovery
        # binds its replacement to the current stopped reservation.
        retry = state.get('retry_only')
        if retry is not None:
            assert retry['position'] == 336 and retry['kind'] == 'forward'
            assert any(item.get('token') == retry['stopped_token'] and item['position'] == 336
                       and item['status'] == 'failed' for item in state['review_queue'])
        assert state['approved_entries'][-1] == '.teacher/runs/commit-000335-001'
        assert len(verify_selection(PACKET, state['approved_entries'])) == 332
        count = validate_packet_blobs(PACKET)
        assert count == previous_audit['verified_readonly_blob_links'] == 4655
        backup = REPORTS/'commit-000336-before-prepared-004-path.json'
        with backup.open('xb') as handle:
            handle.write(STATE.read_bytes())
        write_new(AUDIT, {
            'authorization': {relative(VERDICT): VERDICT_HASH},
            'original_authorization': {'reviews/verdicts/commit-000336-recovery-004.md':
                '34aaf6b4eb248c9b1471871c52859efaa2d737715534cb1d44cd49e81308e059'},
            'path_correction_request': {relative(ROOT/'reviews/requests/commit-000336-recovery-004-path.md'):
                digest(ROOT/'reviews/requests/commit-000336-recovery-004-path.md')},
            'implementation': {relative(path): digest(path) for path in (PATCH, HASHES, TESTS)},
            'manifest_sha256': digest(manifest_path), 'packet': relative(PACKET),
            'comparison': 'Reused the exact immutable 336/002 packet directory.',
            'verified_readonly_blob_links': count, 'verified_approved_ancestors': 332,
            'verified_previous_attempt_artifacts': previous_files,
            'preflight_state_sha256': digest(backup),
        })
        write_new(SPEC, {
            'kind': 'forward', 'position': 336, 'run': relative(RUN),
            'packet': relative(PACKET), 'original_packet': relative(PACKET),
            'authorization': {'path': relative(VERDICT), 'sha256': VERDICT_HASH},
            'application_audit': {'path': relative(AUDIT), 'sha256': digest(AUDIT)},
        })
        recover(STATE, VERDICT, retry_position=336)


def main():
    assert not RESULT.exists() and not SPEC.exists()
    result = dict(position=336, result_path=str(RESULT))
    try:
        verify_and_recover()
        result.update(prepared(STATE, Path.home()/'.codex/auth.json', SPEC), returncode=0)
    except Exception as error:
        state = read(STATE)
        detail = str(error)
        if detail != 'Codex reported an authoring error':
            detail = 'See queue state for failure stage'
        result.update(status='prepared_failed', returncode=1, error_type=type(error).__name__,
                      detail=detail, queue_status=state['status'], run_created=RUN.exists(),
                      failure_location=[f'{Path(frame.filename).name}:{frame.lineno}'
                                        for frame in traceback.extract_tb(error.__traceback__)])
    write_new(RESULT, result)
    print(json.dumps(result), flush=True)
    return result['returncode']


if __name__ == '__main__':
    sys.exit(main())
