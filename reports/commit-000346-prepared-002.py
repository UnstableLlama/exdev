"""Supervise the single fresh 346/002 authorized by the recovery verdict."""
import json
import os
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from orchestration.run_ahead import prepared, recover, verify_selection
from teacher.codex_adapter import MODEL, EFFORT
from teacher.cycle import digest, read, validate_packet_blobs, write_new
from teacher.cycle_notify import notify

REPORTS = ROOT/'reports'
STATE = REPORTS/'teacher-walk-001.json'
SPEC = REPORTS/'commit-000346-prepared-002.spec.json'
RESULT = REPORTS/'commit-000346-prepared-002.result.json'
VERDICT = ROOT/'reviews/verdicts/commit-000346-recovery-001.md'
VERDICT_HASH = 'de39257721aae29fb6417dab3f0cb2df6de68c34b4e91299ac5a2cf9a00b47d8'

def preflight():
    spec = read(SPEC)
    audit_path = ROOT/spec['application_audit']['path']
    audit = read(audit_path)
    state = read(STATE)
    assert state['status']=='stopped_failure' and state['next_position']==346
    assert state['queue_stop']['position']==346
    assert not any(state.get(key) for key in ('active_session','retry_only','handover','advancement_pause'))
    assert state['approved_entries'][-1]=='.teacher/runs/commit-000345-002'
    assert digest(VERDICT)==VERDICT_HASH==spec['authorization']['sha256']
    assert ROOT/spec['authorization']['path']==VERDICT
    assert digest(audit_path)==spec['application_audit']['sha256']
    assert spec['run']=='.teacher/runs/commit-000346-002' and not (ROOT/spec['run']).exists()
    assert spec['position']==346 and spec['kind']=='forward'
    assert spec['packet']==spec['original_packet']=='.teacher/retrieval/000346-002'
    assert (MODEL, EFFORT)==('gpt-6.2-sol','medium')
    for path, expected in audit['verified_unchanged_recovery_bindings'].items():
        assert digest(ROOT/path)==expected, path
    packet = ROOT/spec['packet']
    assert digest(packet/'manifest.json')==audit['new_manifest_sha256']
    assert validate_packet_blobs(packet)==audit['read_only_shared_blob_links']
    assert len(verify_selection(packet, state['approved_entries']))==342
    with (REPORTS/'commit-000346-before-prepared-002.json').open('xb') as backup:
        backup.write(STATE.read_bytes())

def main():
    assert not RESULT.exists()
    result = dict(position=346, result_path=str(RESULT))
    try:
        preflight()
        recover(STATE, VERDICT, retry_position=346)
        result.update(prepared(STATE, Path.home()/'.codex/auth.json', SPEC), returncode=0)
    except Exception as error:
        traceback.print_exc()
        result.update(status='prepared_failed', returncode=1, error_type=type(error).__name__, detail=str(error))
    write_new(RESULT, result)
    print(json.dumps(result), flush=True)
    notify(os.environ['CODEX_THREAD_ID'], result, REPORTS, 346)
    return result['returncode']

if __name__=='__main__':
    sys.exit(main())
