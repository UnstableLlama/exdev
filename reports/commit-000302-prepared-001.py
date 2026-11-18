"""Authorised administrative architecture recovery; never teacher input."""
import json
import sys
import traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from teacher.cycle import recover_inputs,index_parent,prepare_packet,guard_disk,digest,write_json
from teacher.architecture_evidence import load_bundle
from teacher.session import FreshSession
from teacher.cycle_notify import notify
from orchestration.run_ahead import recover,prepared
from orchestration.ancestor_selection import installed
state_path=ROOT/'reports/teacher-walk-001.json'
verdict=ROOT/'reviews/verdicts/commit-000302-architecture-recovery-001.md'
packet=ROOT/'.teacher/retrieval/000302-001'
run=ROOT/'.teacher/runs/commit-000302-001'
result_path=ROOT/'reports/commit-000302-prepared-001.result.json'
result=dict(position=302,result_path=str(result_path))
try:
    assert not packet.exists() and not run.exists() and not result_path.exists()
    request=ROOT/'reviews/requests/commit-000302-architecture-recovery-001.md'
    import re
    bindings=re.findall(r'^- ([^\n:]+): `([0-9a-f]{64})`',request.read_text(),re.M)
    assert len(bindings)==16
    for file,h in bindings:
        assert digest(ROOT/file)==h,file
    state=json.loads(state_path.read_text())
    assert '.teacher/runs/commit-000301-001' in state['approved_entries']
    assert state['next_position']==302 and state['active_session'] is None
    accepted=json.loads((ROOT/'reports/validation-repair-implementation-004-application.json').read_text())
    for group in ('implementation_sha256','orchestration_sha256'):
        for file,h in accepted[group].items():
            assert digest(ROOT/file)==h,file
    backup=ROOT/'reports/commit-000302-before-recovery-001.json'
    assert not backup.exists()
    backup.write_bytes(state_path.read_bytes())
    recover(state_path,verdict,retry_position=302)
    sha='d42d6238d88151eb837bdf709836d8726759fbd7'
    repo=ROOT/'.sources/exllamav3.git';evidence=ROOT/'data/evidence/github'
    guard_disk(ROOT)
    bundle=load_bundle(repo,sha,evidence/'000302-references.json')
    catalog=recover_inputs(repo,sha,302,evidence,ROOT/'reports')
    index_parent(302,ROOT/'data/exllamav3-v5/records',ROOT/'store')
    state=json.loads(state_path.read_text())
    with installed():
        manifest=prepare_packet(repo,sha,302,packet,evidence,ROOT/'store',[ROOT/p for p in state['approved_entries']])
    assert manifest['guidance_version']==12
    assert any(e['sha']=='4f0414a1e9f76d654204e2bbfefb72074743cfa7' for e in manifest['ancestor_entries'])
    headers=[i for i in bundle['items'] if i['kind']=='safetensors_header']
    assert len(headers)==4 and len(bundle['selections'])==3
    # Probe every header through the isolated teacher-facing tool.
    probes=[]
    session=FreshSession(packet)
    for item in headers:
        args={k:item[k] for k in ('repo_id','revision','path','source_id')}
        args.update(offset=0,limit=100)
        response=session.runner.invoke('safetensors_header',args)
        assert response['ok'],response
        assert response['result']['source']['content_sha256']==item['content_sha256']
        probes.append(dict(source_id=item['source_id'],sha256=item['content_sha256'],args=args))
    write_json(ROOT/'reports/commit-000302-header-preflight-001.json',dict(status='passed',packet=str(packet.relative_to(ROOT)),bundle_sha256=digest(evidence/'000302-references.json'),validated_headers=len(headers),isolated_probes=probes,limitation='First page of every header probed in isolation with its content hash verified; complete bundle validation covers all tensor objects. These administrative probes are not teacher reads.'))
    spec_path=ROOT/'reports/commit-000302-prepared-spec-001.json'
    write_json(spec_path,dict(kind='forward',position=302,run=str(run.relative_to(ROOT)),packet=str(packet.relative_to(ROOT)),original_packet=str(packet.relative_to(ROOT)),authorization=dict(path=str(verdict.relative_to(ROOT)),sha256=digest(verdict))))
    result.update(prepared(state_path,Path.home()/'.codex/auth.json',spec_path),returncode=0)
except BaseException as error:
    traceback.print_exc()
    result.update(status='prepared_failed',returncode=1,error_type=type(error).__name__,detail=str(error))
finally:
    write_json(result_path,result)
    notify('01a1eac6-cc72-7af3-9172-36689bd69fc9',result,ROOT/'reports',302)
print(json.dumps(result),flush=True)
