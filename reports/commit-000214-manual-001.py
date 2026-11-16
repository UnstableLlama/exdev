"""Administrative single-run supervisor; never supplied to the teacher."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from teacher.cycle import *
from teacher.architecture_evidence import load_bundle
from teacher.cycle_notify import notify

THREAD = '01a1da07-7653-7b81-8507-f69683828acb'
POSITION = 214
SHA = '42afcd7e6cd361b2be9aef1072f26ffccffb92db'
state_path = ROOT/'reports/teacher-walk-001.json'
reports = ROOT/'reports'
evidence = ROOT/'data/evidence/github'
repo = ROOT/'.sources/exllamav3.git'
packet = ROOT/'.teacher/retrieval/000214-001'
run = ROOT/'.teacher/runs/commit-000214-001'
result_path = reports/'commit-000214-manual-001.result.json'
result = dict(position=POSITION, result_path=relative(result_path))
record = None
try:
    with locked(state_path):
        state = read(state_path)
        assert state['next_position'] == POSITION and state['status'] == 'stopped_cycle'
        assert state.get('cycle_stop', {}).get('status') == 'architecture_trigger'
        assert not state.get('advancement_pause') and not state.get('handover')
        assert not any(r['position'] == POSITION for r in state['runs'])
        assert not packet.exists() and not run.exists()
        discovery = read(reports/'commit-000214-reference-discovery-003.json')
        assert discovery['complete'] and not discovery['unavailable']
        load_bundle(repo, SHA, evidence/'000214-references.json')
        catalog = reports/'commit-000214-catalog-selection-001.json'
        guard_catalog(read(catalog))
        guard_disk(ROOT)
        record = dict(position=POSITION, sha=SHA, run=relative(run), packet=relative(packet), status='preparing')
        state['runs'].append(record)
        state['status'] = 'running'
        state['architecture_resolution'] = dict(position=POSITION, discovery='reports/commit-000214-reference-discovery-003.json', bundle='data/evidence/github/000214-references.json', note='Google discovery complete for authoring under decision 98 point 5; medgemma-4b-it not inspected at pin, no files attached; five validated reference bundles. Resolution recorded in discovery 003; administrative only.')
        write_json(state_path, state)
        prepare_packet(repo, SHA, POSITION, packet, evidence, ROOT/'store', [ROOT/p for p in state['approved_entries']])
        assert read(packet/'manifest.json')['guidance_version'] == 9
        record['status'] = 'authoring'
        write_json(state_path, state)
        author(packet, run, Path.home()/'.codex/auth.json')
        validation = validate_run(run, packet, repo, evidence, POSITION)
        report = reports/'commit-000214-validation-001.json'
        write_new(report, validation)
        summary = make_summary(run, packet, repo, POSITION, report, catalog, evidence)
        summary_path = reports/'commit-000214-cycle-001.json'
        write_new(summary_path, summary)
        skel = reports/'commit-000214-001.skeleton.md'
        with skel.open('x') as f:
            f.write(skeleton(summary, THREAD))
        record.update(validation['assessment'])
        assert record['tier'] == 'full_review'
        record['status'] = state['status'] = 'awaiting_review_request'
        state['handover'] = dict(full_review=relative(run), sampled_mechanical=[])
        write_json(state_path, state)
        tracking_status(state)
        result.update(status=state['status'], returncode=0, summary=relative(summary_path), skeleton=relative(skel), draft=relative(run/'draft.md'))
except BaseException as error:
    import traceback
    traceback.print_exc()
    if record is not None:
        record['status'] = 'failed'
        state.update(status='stopped_failure', error_type=type(error).__name__)
        write_json(state_path, state)
        tracking_status(state)
    result.update(status='manual_failed', returncode=1, error_type=type(error).__name__, detail=str(error))
finally:
    write_json(result_path, result)
    notify(THREAD, result, reports, POSITION)
