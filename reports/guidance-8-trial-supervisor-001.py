"""One-shot administrative trial runner; never teacher input."""
import collections
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import traceback

ROOT = Path('/home/brandonrabe/git/exdev')
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)
from teacher.author import author
from teacher.session import FreshSession
from teacher.codex_transport import CodexTransport
from teacher.cycle_notify import notify
BASE = ROOT/'.teacher/trials/guidance-8-001'
REPORT = ROOT/'reports/guidance-8-trial-001.json'

def write(path, obj):
    path.write_text(json.dumps(obj, indent=2)+'\n')

class UsageTransport(CodexTransport):
    """Observe existing wire events only; sends and teacher inputs are unchanged."""
    def _receive(self):
        event = super()._receive()
        if event.get('method') == 'thread/tokenUsage/updated':
            self.usage_events.append(event)
            write(self.usage_path, {'events': self.usage_events})
        return event

def transport_factory_for(output):
    def factory(auth_file):
        transport = UsageTransport(auth_file)
        transport.usage_events = []
        transport.usage_path = output/'token-usage.json'
        write(transport.usage_path, {'events': []})
        return transport
    return factory

def snapshot():
    cache = {}
    files = {}
    for root in (ROOT/'.teacher/retrieval', ROOT/'.teacher/runs'):
        for path in sorted(root.rglob('*')):
            if not path.is_file():
                continue
            st = path.stat()
            key = (st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns)
            if key not in cache:
                cache[key] = hashlib.sha256(path.read_bytes()).hexdigest()
            files[str(path.relative_to(ROOT))] = [cache[key], st.st_mode & 0o777]
    journal = json.loads((ROOT/'reports/teacher-walk-001.json').read_text())
    return {'files': files, 'runs': journal['runs'], 'approved_entries': journal['approved_entries']}

def metrics(run):
    t = json.loads((run/'raw-transcript.json').read_text())
    calls = [c for m in t for c in m.get('calls', [])]
    return {'run': str(run.relative_to(ROOT)), 'tool_counts': dict(collections.Counter(c['tool'] for c in calls)),
            'total_calls': len(calls), 'assistant_transcript_records': sum(m['role']=='assistant' for m in t),
            'model_turns': 1, 'model_turn_definition': 'One app-server turn/start per author invocation; tool calls occur within that turn. Inference-step counts are not retained.',
            'token_usage': json.loads((run/'token-usage.json').read_text()) if (run/'token-usage.json').exists() else {'status': 'unavailable', 'reason': 'Historical authoring did not retain usage events; no estimate substituted.'},
            'coverage': json.loads((run/'coverage.json').read_text()),
            'hashes': {name: hashlib.sha256((run/name).read_bytes()).hexdigest() for name in
                       ('draft.json','draft.md','raw-transcript.json','coverage.json','provenance.json')}}

result = {'status': 'running', 'trial': 'guidance-8-001', 'result_path': str(REPORT.relative_to(ROOT)), 'sessions': []}
try:
    journal = json.loads((ROOT/'reports/teacher-walk-001.json').read_text())
    assert journal['status'] == 'awaiting_full_review', 'Run trials between walk commits after filing the current request'
    BASE.mkdir(parents=True, exist_ok=False)
    before = snapshot()
    write(BASE/'walk-before.json', before)
    write(REPORT, result)
    for position in (154,140,157,156):
        source = ROOT/f'.teacher/retrieval/{position:06d}-001'
        packet = BASE/f'packet-{position:06d}'
        packet.mkdir()
        shutil.copytree(source/'blobs', packet/'blobs', copy_function=os.link)
        original = json.loads((source/'manifest.json').read_text())
        assert original['guidance_version']==5 and not original.get('coverage_request')
        trial = dict(original, guidance_version=8)
        write(packet/'manifest.json',trial)
        assert {k:v for k,v in trial.items() if k!='guidance_version'} == {k:v for k,v in original.items() if k!='guidance_version'}
        FreshSession(packet).require_authoring_context()
        row = {'position': position, 'source_packet': str(source.relative_to(ROOT)),
               'trial_packet': str(packet.relative_to(ROOT)), 'manifest_differing_fields': ['guidance_version'],
               'source_manifest_sha256': hashlib.sha256((source/'manifest.json').read_bytes()).hexdigest(),
               'trial_manifest_sha256': hashlib.sha256((packet/'manifest.json').read_bytes()).hexdigest(),
               'reviewer_assisted': False, 'attempt': 1}
        result['sessions'].append(row)
        write(REPORT,result)
        output = BASE/f'run-{position:06d}-001'
        author(packet, output, Path.home()/'.codex/auth.json', transport_factory=transport_factory_for(output))
        row['trial_metrics'] = metrics(output)
        approved = ROOT/f'.teacher/runs/commit-{position:06d}-{1:03d}'
        row['approved_metrics'] = metrics(approved)
        write(REPORT,result)
    result['status']='trials_complete_awaiting_request'
except BaseException as e:
    result.update(status='trial_failed_needs_inspection', error_type=type(e).__name__, detail=str(e), traceback=traceback.format_exc())
finally:
    try:
        after=snapshot()
        write(BASE/'walk-after.json',after)
        result['walk_snapshot_equal']=before==after
        result['walk_files_equal']=before['files']==after['files']
        result['journal_runs_equal']=before['runs']==after['runs']
        result['journal_approved_entries_equal']=before['approved_entries']==after['approved_entries']
        if before!=after: result['status']='trial_isolation_mismatch'
    except BaseException:
        result['snapshot_error']=traceback.format_exc()
    write(REPORT,result)
    notify(sys.argv[1], {k:result[k] for k in ('status','trial','result_path')}, ROOT/'reports', 'guidance-8-001')
