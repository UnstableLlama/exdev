import json,sys,hashlib,platform
from pathlib import Path
sys.path.insert(0,'tests')
from test_large_headers import LargeHeaderPacketTests
from teacher.runner import Runner
from teacher.worker import dispatch
fixture=LargeHeaderPacketTests();fixture.setUp();checks=[]
try:
 for i in (2,6):
  obj=json.loads(Path(f'data/evidence/hf/000141-002/{i}/recovered.json').read_text())
  for n,e in enumerate(obj['items']):
   if e['kind']!='safetensors_header':continue
   body=e['content'];header=json.loads(body);count=len([x for x in header if x!='__metadata__'])
   packet=LargeHeaderPacketTests.packet(fixture,body,f'live-{i}-{n}')
   for offset in (0,count-1):
    args=dict(repo_id='org/model',revision='a'*40,path='model.safetensors',offset=offset,limit=1)
    expected=dispatch(packet,'safetensors_header',args);result=Runner(packet).invoke('safetensors_header',args)
    assert result['ok'] and result['result']==expected,result
    checks.append(dict(repo=obj['report']['repo'],revision=obj['report']['revision'],path=e['path'],normalized_header_bytes=len(body.encode()),tensor_count=count,offset=offset,returned_tensors=len(expected['header']),result_sha256=hashlib.sha256(json.dumps(result,sort_keys=True).encode()).hexdigest(),passed=True))
finally:fixture.tearDown()
Path('reports/header-budget-live-audit-001.json').write_text(json.dumps(dict(status='passed',purpose='Pinned real header content in isolated administrative fixture packets; synthetic locator, no teacher',checks=checks,machine_architecture=platform.machine(),python_version=platform.python_version(),live_model_invoked=False),indent=2)+'\n')
print('passed',len(checks))
