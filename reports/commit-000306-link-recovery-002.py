"""One-off link restoration and validation; no author invocation. Await authorization."""
import sys, json, os, hashlib, copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from teacher import cycle
from teacher.blob_store import put
from orchestration.ancestor_selection import installed
from orchestration.run_ahead import transaction, finish, verify_selection
state_path=ROOT/'reports/teacher-walk-001.json'
audit_path=ROOT/'reports/commit-000306-link-recovery-002.json'
digest=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    authorization=ROOT/'reviews/verdicts/commit-000306-link-recovery-002.md'
    assert len(sys.argv)==2 and digest(authorization)==sys.argv[1]
    assert '.teacher/runs/commit-000306-002' in authorization.read_text()
    assert digest(audit_path)=='0110cff761ba82ca7f464d703a8326de2c2ebd8712a3b25715feead45a6487cf'
    audit=json.loads(audit_path.read_text())
    packet=ROOT/audit['packet'];run=ROOT/audit['run']
    state=json.loads(state_path.read_text())
    assert state['active_session'] is None and state['queue_stop']==audit['queue_stop']
    item=next(q for q in state['review_queue'] if q.get('run')==audit['run'])
    assert item['status']=='failed' and state['retry_only']['position']==306
    assert not any(r.get('run')==audit['run'] for r in state['runs'])
    assert digest(packet/'manifest.json')==audit['packet_manifest_sha256']
    for path,expected in audit['authored_run_files_sha256'].items():assert digest(ROOT/path)==expected
    for name in audit['not_shared_hardlink_names']:
        blob=packet/'blobs'/name;store=ROOT/'.teacher/blob-store'/name
        assert digest(blob)==digest(store)==name
        assert not blob.stat().st_mode&0o222 and not store.stat().st_mode&0o222
        put(packet,blob.read_bytes())
        assert os.path.samefile(blob,store)
    verify_selection(packet,state['approved_entries'])
    with installed():validation=cycle.validate_run(run,packet,ROOT/'.sources/exllamav3.git',ROOT/'data/evidence/github',306)
    for path,expected in audit['authored_run_files_sha256'].items():assert digest(ROOT/path)==expected
    assert digest(packet/'manifest.json')==audit['packet_manifest_sha256']
    report=ROOT/'reports/commit-000306-002-queue-validation.json'
    assert not report.exists();cycle.write_json(report,validation)
    with transaction(state_path) as live:
        assert live['active_session'] is None and live['queue_stop']==audit['queue_stop']
        current=next(q for q in live['review_queue'] if q.get('run')==audit['run'])
        assert current['status']=='failed' and current['token']==item['token']
        assert not any(r.get('run')==audit['run'] for r in live['runs'])
        live.setdefault('recovery_log',[]).append(dict(stop=copy.deepcopy(live['queue_stop']),authorization=str(authorization.relative_to(ROOT)),sha256=sys.argv[1],action='Restore byte-identical blob links and validate completed attempt; no author invocation',audit_sha256=digest(audit_path)))
        current['status']='reserved';live['active_session']=item['token']
        row=dict(position=306,run=audit['run'],packet=audit['packet'],status='awaiting_review_request',validation=str(report.relative_to(ROOT)),spec_sha256=item['spec_sha256'])
        finish(live,item['token'],row=row)
        assert live['queue_stop']==dict(outcome='retry_awaiting_verdict',run=audit['run'])
    return dict(status='awaiting_review_request',position=306,run=audit['run'],validation=str(report.relative_to(ROOT)),teacher_reinvoked=False)
if __name__=='__main__':
    with cycle.locked(state_path):
        print(json.dumps(main()),flush=True)
