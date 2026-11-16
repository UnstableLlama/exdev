"""Administrative verification; no teacher/provider invocation."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()/'tests'))
from test_walk_inputs import WalkInputTests
from teacher.session import FreshSession, GUIDANCE_8_ADDITION
from teacher.walk_inputs import prepare, validate_bundle

report = {'historical': []}
for before in json.loads(Path('reports/guidance-8-adoption-before.json').read_text()):
    p = Path(before['packet'])
    session = FreshSession(p)
    after = dict(packet=str(p),initial=session.initial,tools=session.tools,reasoning_effort=session.reasoning_effort)
    assert before == after
    manifest = json.loads((p/'manifest.json').read_text())
    position = 171 if '171' in str(p) else 177 if '177' in str(p) else 154
    validate_bundle(p, Path(f'data/evidence/github/{position:06d}-eligible.json'))
    report['historical'].append(dict(packet=str(p),version=manifest['guidance_version'],unchanged=True,validated=True,
        system_sha256=hashlib.sha256(session.initial[0]['content'].encode()).hexdigest()))
text = Path('reviews/verdicts/guidance-8-adoption.decision.md').read_text()
expected = text.split('**D.**\n')[1].split('\n\n')[0]
assert expected == GUIDANCE_8_ADDITION
fixture = WalkInputTests()
fixture.setUp()
try:
    directory = fixture.bundle()
    packet = fixture.root/'adoption-fresh'
    m = prepare(fixture.repo,fixture.task,9,packet,directory)
    assert m['guidance_version'] == 8
    validate_bundle(packet,directory/'000009-eligible.json')
    fresh = FreshSession(packet)
    m['guidance_version'] = 7
    (packet/'manifest.json').write_text(json.dumps(m))
    prior = FreshSession(packet)
    assert fresh.initial[0]['content'] == prior.initial[0]['content']+'\n\n'+expected
    assert fresh.initial[1:] == prior.initial[1:]
    assert fresh.tools == prior.tools
    assert fresh.reasoning_effort == prior.reasoning_effort
    report['fresh_prepare'] = dict(version=8,validated=True,exact_decision_addition=True,non_system_inputs_unchanged=True)
finally:
    fixture.tearDown()
Path('reports/guidance-8-adoption-verification-001.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
