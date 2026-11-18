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
verdict=ROOT/'reviews/verdicts/commit-000271-architecture-recovery-001.md'
packet=ROOT/'.teacher/retrieval/000271-001'
run=ROOT/'.teacher/runs/commit-000271-001'
result_path=ROOT/'reports/commit-000271-prepared-001.result.json'
result=dict(position=271,result_path=str(result_path))
try:
    assert not packet.exists() and not run.exists() and not result_path.exists()
    request=ROOT/'reviews/requests/commit-000271-architecture-recovery-001.md'
    import re
    for file,h in re.findall(r'- `([^`]+)`: `([0-9a-f]{64})`',request.read_text()):
        assert digest(ROOT/file)==h,file
    state=json.loads(state_path.read_text())
    assert '.teacher/runs/commit-000270-001' in state['approved_entries']
    assert state['next_position']==271 and state['active_session'] is None
    backup=ROOT/'reports/commit-000271-before-recovery-001.json'
    assert not backup.exists()
    backup.write_bytes(state_path.read_bytes())
    recover(state_path,verdict,retry_position=271)
    sha='2d1ce8910339ce3f10b3c46ee0b92cff23df71da'
    repo=ROOT/'.sources/exllamav3.git';evidence=ROOT/'data/evidence/github'
    guard_disk(ROOT)
    bundle=load_bundle(repo,sha,evidence/'000271-references.json')
    catalog=recover_inputs(repo,sha,271,evidence,ROOT/'reports')
    index_parent(271,ROOT/'data/exllamav3-v5/records',ROOT/'store')
    state=json.loads(state_path.read_text())
    with installed():
        manifest=prepare_packet(repo,sha,271,packet,evidence,ROOT/'store',[ROOT/p for p in state['approved_entries']])
    assert manifest['guidance_version']==12
    assert any(e['sha']=='b8c830c17f53cf0d4caf7b774fe458b2f31cb85c' for e in manifest['ancestor_entries'])
    headers=[i for i in bundle['items'] if i['kind']=='safetensors_header']
    # Probe each selected checkpoint through the isolated teacher-facing tool.
    probes=[]
    session=FreshSession(packet)
    for selection in bundle['selections']:
        candidates=[i for i in headers if i['repo_id']==selection['repo']]
        item=max(candidates,key=lambda i:len(i['content']))
        args={k:item[k] for k in ('repo_id','revision','path','source_id')}
        args.update(offset=0,limit=100)
        response=session.runner.invoke('safetensors_header',args)
        assert response['ok'],response
        assert response['result']['source']['content_sha256']==item['content_sha256']
        probes.append(dict(source_id=item['source_id'],sha256=item['content_sha256'],args=args))
    write_json(ROOT/'reports/commit-000271-header-preflight-001.json',dict(status='passed',packet=str(packet.relative_to(ROOT)),bundle_sha256=digest(evidence/'000271-references.json'),validated_headers=len(headers),isolated_probes=probes,limitation='One page of the largest header per checkpoint probed in isolation; complete bundle validation covers all header objects.'))
    spec_path=ROOT/'reports/commit-000271-prepared-spec-001.json'
    write_json(spec_path,dict(kind='forward',position=271,run=str(run.relative_to(ROOT)),packet=str(packet.relative_to(ROOT)),original_packet=str(packet.relative_to(ROOT)),authorization=dict(path=str(verdict.relative_to(ROOT)),sha256=digest(verdict))))
    result.update(prepared(state_path,Path.home()/'.codex/auth.json',spec_path),returncode=0)
except BaseException as error:
    traceback.print_exc()
    result.update(status='prepared_failed',returncode=1,error_type=type(error).__name__,detail=str(error))
finally:
    write_json(result_path,result)
    notify('01a1da07-7653-7b81-8507-f69683828acb',result,ROOT/'reports',271)
print(json.dumps(result),flush=True)
