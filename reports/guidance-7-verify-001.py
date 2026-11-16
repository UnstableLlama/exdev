"""Administrative verification only; invokes no teacher/provider."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from teacher.session import FreshSession, GUIDANCE_6, GUIDANCE_7
from teacher.walk_inputs import validate_bundle

report = {'legacy': []}
for version in (5, 6):
    before_path = Path(f'reports/guidance-7-v{version}-before.json')
    before = json.loads(before_path.read_text())
    session = FreshSession(before['packet'])
    after = dict(packet=before['packet'], initial=session.initial,
                 tools=session.tools, reasoning_effort=session.reasoning_effort)
    assert before == after
    validate_bundle(Path(before['packet']), Path('data/evidence/github')/('000171-eligible.json' if version == 5 else '000154-eligible.json'))
    report['legacy'].append(dict(version=version, packet=before['packet'],
        unchanged=True, validated=True, baseline_sha256=hashlib.sha256(before_path.read_bytes()).hexdigest(),
        system_sha256=hashlib.sha256(session.initial[0]['content'].encode()).hexdigest()))
text = Path('reviews/verdicts/guidance-6-adoption.decision.md').read_text()
labels = ['A (reworded as proposed to the user).', 'B (unchanged from the trial).', 'C (unchanged from the trial).']
expected = '\n\n'.join(text.split('**'+label+'**\n')[1].split('\n\n')[0] for label in labels)
assert GUIDANCE_7 == expected
assert GUIDANCE_7.split('\n\n')[1:] == GUIDANCE_6.split('\n\n')[1:]
baseline = json.loads(Path('reports/guidance-7-v5-before.json').read_text())
with tempfile.TemporaryDirectory(prefix='guidance7-', dir='reports') as tmp:
    packet = Path(tmp)/'packet'
    shutil.copytree(baseline['packet'], packet, copy_function=os.link)
    manifest_path = packet/'manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['guidance_version'] = 7
    manifest_path.unlink()  # never overwrite the original hardlinked inode
    manifest_path.write_text(json.dumps(manifest))
    validate_bundle(packet, Path('data/evidence/github/000171-eligible.json'))
    session = FreshSession(packet)
    assert session.initial[0]['content'] == baseline['initial'][0]['content']+'\n'+expected
    assert session.initial[1:] == baseline['initial'][1:]
    assert session.tools == baseline['tools']
    assert session.reasoning_effort == baseline['reasoning_effort']
report['adopted'] = dict(verbatim_decision=True, bc_unchanged=True, validated=True,
    replaces_trial_text=True, other_inputs_unchanged=True,
    paragraphs_sha256=hashlib.sha256(expected.encode()).hexdigest())
Path('reports/guidance-7-adoption-001.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
