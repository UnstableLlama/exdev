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
packet = ROOT/'.teacher/retrieval/000141-003'
run = ROOT/'.teacher/runs/commit-000141-003'
preflight = ROOT/'reports/commit-000141-replacement-preflight-003.json'
validation = ROOT/'reports/commit-000141-validation-003.json'
result_path = ROOT/'reports/commit-000141-replacement-003.result.json'
result = dict(position=141, replacement=True, result_path=relative(result_path))
row = None
try:
    with locked(state_path):
        state = read(state_path)
        assert state['status'] == 'ready' and state['next_position'] == 250
        assert state['handover'] is None
        assert not state.get('advancement_pause') and not state.get('replacement_pause')
        assert not run.exists() and not result_path.exists()
        assert all(r['status'] in ('approved_reviewed', 'rejected') for r in state.get('replacement_reviews', []))
        from teacher.session import FreshSession
        pf = read(preflight)
        assert pf['status'] == 'local_passed_pending_isolated_probe'
        probe = max(pf['headers'], key=lambda h:h['pages'])
        response = FreshSession(packet).runner.invoke('safetensors_header', probe['args'])
        assert response['ok'], response
        assert response['result']['source']['content_sha256'] == probe['sha256']
        pf.update(status='passed', isolated_header_probe=True, isolated_probe_source=probe['source_id'])
        write_json(preflight,pf)
        from teacher.coverage_request import attach
        old = read(ROOT/'.teacher/retrieval/000141-002/manifest.json')
        coverage = ROOT/'reviews/verdicts/commit-000141-003.coverage.md'
        attach(old, Path('reviews/verdicts/commit-000141-003.coverage.md'), digest(coverage))
        assert old == read(packet/'manifest.json')
        validate_bundle(packet, ROOT/'data/evidence/github/000141-eligible.json')
        for blob in (packet/'blobs').iterdir():
            assert digest(blob) == blob.name and not blob.stat().st_mode & 0o222
            assert os.path.samefile(blob, store_root(packet)/blob.name)
        row = dict(position=141, supersedes_run='.teacher/runs/commit-000141-001',
                   candidate_run=relative(run), packet=relative(packet), status='authoring',
                   reviewer_assisted=True, coverage_request='reviews/verdicts/commit-000141-003.coverage.md', coverage_request_sha256=digest(coverage), preflight=relative(preflight), guidance_jump='5->12', tier='full_review')
        for key, file in [('decision','reviews/verdicts/guidance-11-reauthoring.decision.md'),
                          ('plan_verdict','reviews/verdicts/guidance-11-reauthoring-plan-001.md'), ('adoption_decision','reviews/verdicts/guidance-12-adoption.decision.md'), ('adoption_verdict','reviews/verdicts/guidance-12-adoption-001.md')]:
            row[key] = dict(path=file, sha256=digest(ROOT/file))
        state.setdefault('replacement_reviews', []).append(row)
        write_json(state_path, state)
        try:
            author(packet, run, Path.home()/'.codex/auth.json')
            write_json(validation, validate_run(run, packet, ROOT/'.sources/exllamav3.git',
                                               ROOT/'data/evidence/github', 141))
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
    notify('01a1da07-7653-7b81-8507-f69683828acb', result, ROOT/'reports', 141)
print(result, flush=True)
