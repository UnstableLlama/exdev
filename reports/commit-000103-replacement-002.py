"""Administrative one-shot replacement supervisor; never teacher input."""
import os
from pathlib import Path
import sys
import traceback
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from teacher.cycle import read, digest, relative, locked, write_json, validate_run, tracking_status
from teacher.author import author
from teacher.walk_inputs import validate_bundle
from teacher.blob_store import store_root
from teacher.cycle_notify import notify

state_path = ROOT/'reports/teacher-walk-001.json'
packet = ROOT/'.teacher/retrieval/000103-002'
run = ROOT/'.teacher/runs/commit-000103-002'
preflight = ROOT/'reports/commit-000103-replacement-preflight-002.json'
validation = ROOT/'reports/commit-000103-validation-002.json'
result_path = ROOT/'reports/commit-000103-replacement-002.result.json'
result = dict(position=103, replacement=True, result_path=relative(result_path))
row = None
try:
    with locked(state_path):
        state = read(state_path)
        assert state['status'] == 'awaiting_full_review' and state['next_position'] == 244
        assert state['handover']['full_review'] == '.teacher/runs/commit-000244-001'
        assert not state.get('advancement_pause')
        assert not run.exists() and not result_path.exists()
        assert all(r['status'] in ('approved_reviewed', 'rejected') for r in state.get('replacement_reviews', []))
        assert read(preflight)['status'] == 'passed'
        old = read(ROOT/'.teacher/retrieval/000103-001/manifest.json')
        new = read(packet/'manifest.json')
        assert old['guidance_version'] == 5 and new['guidance_version'] == 11
        assert {k:v for k,v in old.items() if k!='guidance_version'} == {k:v for k,v in new.items() if k!='guidance_version'}
        validate_bundle(packet, ROOT/'data/evidence/github/000103-eligible.json')
        for blob in (packet/'blobs').iterdir():
            assert digest(blob) == blob.name and not blob.stat().st_mode & 0o222
            assert os.path.samefile(blob, store_root(packet)/blob.name)
        row = dict(position=103, supersedes_run='.teacher/runs/commit-000103-001',
                   candidate_run=relative(run), packet=relative(packet), status='authoring',
                   preflight=relative(preflight), guidance_jump='5->11', tier='full_review')
        for key, file in [('decision','reviews/verdicts/guidance-11-reauthoring.decision.md'),
                          ('plan_verdict','reviews/verdicts/guidance-11-reauthoring-plan-001.md')]:
            row[key] = dict(path=file, sha256=digest(ROOT/file))
        state.setdefault('replacement_reviews', []).append(row)
        write_json(state_path, state)
        try:
            author(packet, run, Path.home()/'.codex/auth.json')
            write_json(validation, validate_run(run, packet, ROOT/'.sources/exllamav3.git',
                                               ROOT/'data/evidence/github', 103))
            row['status'] = 'awaiting_review_request'
            row['validation'] = relative(validation)
            result.update(status='awaiting_review_request', returncode=0,
                          draft=relative(run/'draft.md'), validation=relative(validation))
        except BaseException:
            row['status'] = 'failed'
            raise
        finally:
            write_json(state_path, state)
            tracking_status(state)
except BaseException as error:
    traceback.print_exc()
    result.update(status='replacement_failed', returncode=1, error_type=type(error).__name__, detail=str(error))
finally:
    write_json(result_path, result)
    notify('01a1da07-7653-7b81-8507-f69683828acb', result, ROOT/'reports', 103)
print(result, flush=True)
