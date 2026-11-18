"""Opt-in review queue. No live enablement before implementation review acceptance.

The existing cycle is executed against a private journal. Only administrative
records are merged back; a teacher sees approved entries captured at reservation.
"""
import argparse
from contextlib import contextmanager
from copy import deepcopy
import fcntl
import hashlib
import importlib
import json
import os
import re
from pathlib import Path
import subprocess
import sys
import uuid

from teacher import cycle as legacy
from teacher.author import write_json

ROOT = legacy.ROOT
CAP = 3
PENDING = {'reserved', 'awaiting_review_request', 'pending_full_review'}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@contextmanager
def transaction(path):
    with Path(str(path)+'.queue.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = json.loads(Path(path).read_text())
        yield state
        write_json(Path(path), state)


def require_enabled(state):
    if not state.get('run_ahead', {}).get('enabled'):
        raise ValueError('Run-ahead is not enabled by an accepted implementation verdict')


def migrate(state):
    """Pure migration, called only while both legacy session and queue are locked."""
    state = deepcopy(state)
    if state.get('active_session') or state.get('status') == 'running':
        raise ValueError('Cannot migrate an active session')
    if 'review_queue' in state:
        raise ValueError('Already migrated')
    queue = []
    handover = state.get('handover')
    if handover:
        run = handover['full_review']
        row = next(r for r in state['runs'] if r['run'] == run)
        item = dict(run=run, packet=row['packet'], position=row['position'], kind='forward',
                    status=row['status'], sampled_mechanical=handover.get('sampled_mechanical', []))
        if handover.get('request'):
            item.update(request=handover['request'], request_sha256=digest(ROOT/handover['request']))
        queue.append(item)
        state['next_position'] = max(state['next_position'], row['position']+1)
    for row in state.get('replacement_reviews', []):
        if row.get('status') in ('awaiting_review_request', 'pending_full_review'):
            item = dict(run=row['candidate_run'], packet=row['packet'], position=row['position'],
                        kind='replacement', status=row['status'], supersedes_run=row['supersedes_run'])
            if row.get('request'):
                item.update(request=row['request'], request_sha256=digest(ROOT/row['request']))
            if not any(q['run'] == item['run'] for q in queue):
                queue.append(item)
    if len(queue) > CAP:
        raise ValueError('Existing queue exceeds capacity')
    state.update(review_queue=queue, active_session=None, handover=None)
    if state['status'] in ('awaiting_full_review', 'awaiting_review_request'):
        state['status'] = 'ready'
    return state


def reserve(state, *, position, kind, files, run=None, packet=None):
    require_enabled(state)
    if state.get('advancement_pause') or state.get('replacement_pause') and kind == 'replacement' or state.get('queue_stop') or state['status'] != 'ready':
        raise ValueError('Explicit pause, failure or recovery stop')
    if state.get('active_session'):
        raise ValueError('Teacher session already reserved')
    queue = state['review_queue']
    if sum(q['status'] in PENDING for q in queue) >= CAP:
        raise ValueError('Three review requests/reservations outstanding')
    # Do not silently run past a completed draft whose request is not yet filed.
    if any(q['status'] == 'awaiting_review_request' for q in queue):
        raise ValueError('File the completed request before starting another run')
    if state.get('retry_only') and (position != state['retry_only']['position'] or kind != state['retry_only']['kind'] or not run or not packet):
        raise ValueError('Only the explicitly authorized prepared retry may start')
    if kind not in ('forward', 'replacement'):
        raise ValueError('Unknown work kind')
    if kind == 'forward' and position != state['next_position'] and not state.get('retry_only'):
        raise ValueError('Forward work must use next unstarted position')
    token = uuid.uuid4().hex
    dependencies = []
    for q in queue:
        if q['status'] in PENDING:
            overlap = sorted(set(files) & set(q['files']))
            dependencies.append(dict(position=q['position'], run=q.get('run'),
                                     touches_same_file=bool(overlap), overlapping_files=overlap))
    item = dict(token=token, position=position, kind=kind, status='reserved',
                files=sorted(set(files)), ran_ahead_of=dependencies,
                approved_entries_snapshot=list(state['approved_entries']))
    if run: item['run'] = run
    if packet: item['packet'] = packet
    queue.append(item)
    state.update(active_session=token, status='running')
    return deepcopy(item)


def finish(state, token, *, row=None, stop=None):
    item = next(q for q in state['review_queue'] if q.get('token') == token)
    if state.get('active_session') != token or item['status'] != 'reserved':
        raise ValueError('Stale or duplicate completion')
    state['active_session'] = None
    if stop:
        item['status'] = 'failed'
        state.update(status='stopped_failure', queue_stop=stop)
        return
    item.update(run=row['run'], packet=row['packet'], status='awaiting_review_request')
    row = deepcopy(row)
    row['ran_ahead_of'] = item['ran_ahead_of']
    row['approved_entries_snapshot'] = item['approved_entries_snapshot']
    item['completed_record'] = deepcopy(row)
    if item['kind'] == 'replacement':
        replacement = dict(row, candidate_run=row['run'], supersedes_run=item['supersedes_run'])
        state.setdefault('replacement_reviews', []).append(replacement)
    if item['kind'] == 'forward':
        state['runs'].append(row)
        state['next_position'] = max(state['next_position'], item['position']+1)
    if state.get('retry_only'):
        state.pop('retry_only')
        state['queue_stop'] = dict(outcome='retry_awaiting_verdict', run=row['run'])
    state['status'] = 'stopped_recovery' if state.get('queue_stop') else 'ready'


def publish(state, run, request):
    require_enabled(state)
    item = next(q for q in state['review_queue'] if q.get('run') == run)
    request = Path(request)
    if request.resolve() != ROOT/'reviews/requests'/(Path(run).name+'.md'):
        raise ValueError('Request filename must identify exact run in reviews/requests')
    if item['status'] != 'awaiting_review_request' or request.is_symlink() or not request.is_file():
        raise ValueError('Request is not a new regular file for a completed run')
    text = request.read_text()
    if not text.strip() or run not in text:
        raise ValueError('Request must identify its run')
    positions = sorted({d['position'] for d in item.get('ran_ahead_of', [])})
    if positions and 'Ran ahead of: '+', '.join(map(str, positions))+'.' not in text:
        raise ValueError('Request must disclose ran-ahead positions')
    item.update(status='pending_full_review', request=legacy.relative(request), request_sha256=digest(request))
    for row in state['runs'] + state.get('replacement_reviews', []):
        if row.get('run', row.get('candidate_run')) == run: row['status'] = 'pending_full_review'


def approval_guard(state, item):
    if item['status'] != 'pending_full_review':
        raise ValueError('Run is not awaiting a verdict')
    if item['kind'] == 'forward':
        approved = {r['position'] for r in state['runs'] if r.get('status') in ('approved_reviewed','approved_mechanical')}
        if any(q['kind'] == 'forward' and q['position'] < item['position'] and
               q['status'] != 'approved_reviewed' and q['position'] not in approved for q in state['review_queue']):
            raise ValueError('Earlier forward position has not been approved')
        for row in state['runs']:
            if row['position'] < item['position'] and row.get('status') not in (
                    'approved_reviewed', 'approved_mechanical', 'superseded', 'rejected', 'failed'):
                raise ValueError('Earlier forward position unresolved')
        # Rejected historical attempts are allowed only when that position has an approved attempt.
        approved = {r['position'] for r in state['runs'] if r.get('status') in ('approved_reviewed','approved_mechanical')}
        if any(r['position'] < item['position'] and r['position'] not in approved for r in state['runs']):
            raise ValueError('Earlier failed/rejected position still unresolved')


def changed_files(repo, sha):
    # Root commits and merges: union of paths changed against any parent.
    parents = legacy.git(repo, 'rev-list', '--parents', '-n', '1', sha).decode().split()[1:]
    files = set()
    if not parents:
        raw = legacy.git(repo, 'diff-tree', '--root', '--no-commit-id', '--name-only', '-r', '-z', sha)
        files.update(x.decode() for x in raw.split(b'\0') if x)
    for parent in parents:
        raw = legacy.git(repo, 'diff', '--name-only', '--no-renames', '-z', parent, sha)
        files.update(x.decode() for x in raw.split(b'\0') if x)
    return sorted(files)


def enable(path, verdict):
    verdict = Path(verdict).resolve()
    expected = ROOT/'reviews/verdicts/run-ahead-implementation-002.md'
    if verdict != expected or not verdict.is_file():
        raise ValueError('The completed implementation verdict is required')
    text = verdict.read_text()
    if not re.search(r'\bACCEPTED\b', text, re.I) or re.search(r'\b(REJECTED|HELD)\b', text, re.I):
        raise ValueError('Explicit implementation acceptance required')
    with legacy.locked(path), transaction(path) as state:
        updated = migrate(state)
        repo = ROOT/'.sources/exllamav3.git'
        for q in updated['review_queue']:
            manifest = json.loads((ROOT/q['packet']/'manifest.json').read_text())
            q['files'] = changed_files(repo, manifest['task_sha'])
            q.setdefault('ran_ahead_of', [])
        updated['run_ahead'] = dict(enabled=True, verdict=legacy.relative(verdict), sha256=digest(verdict))
        state.clear(); state.update(updated)


def worker(snapshot, auth):
    """Private legacy cycle: force administrative review, never mechanical approval."""
    original, tracking, original_author = legacy.assess, legacy.TRACKING, legacy.author
    state = json.loads(snapshot.read_text())
    reservation = next(q for q in state['review_queue'] if q['status'] == 'reserved')
    def bound_author(packet, output, *args, **kwargs):
        with provenance_binding(packet, output, reservation['approved_entries_snapshot'],
                                reservation['implementation_sha256']):
            return original_author(packet, output, *args, **kwargs)
    def full_review(*args, **kwargs):
        result = original(*args, **kwargs)
        if result['tier'] != 'full_review':
            result = dict(result, tier='full_review', run_ahead_mechanical_review=True)
        return result
    legacy.assess = full_review
    legacy.author = bound_author
    legacy.TRACKING = snapshot.with_suffix('.tracking.md')
    from .ancestor_selection import installed
    try:
        with installed():
            return legacy.cycle(snapshot, auth)
    finally:
        legacy.assess, legacy.TRACKING, legacy.author = original, tracking, original_author


def run(path, auth):
    # Same session lock as existing cycle/replacement supervisors. Queue operations
    # use another lock and therefore remain available during this subprocess.
    with legacy.locked(path):
        with transaction(path) as state:
            require_enabled(state)
            repo = ROOT/'.sources/exllamav3.git'
            order = legacy.git(repo,'rev-list','--reverse','--topo-order',state['history_tip']).decode().split()
            position = state['next_position']
            item = reserve(state, position=position, kind='forward', files=changed_files(repo,order[position-1]))
            live = next(q for q in state['review_queue'] if q.get('token') == item['token'])
            live['implementation_sha256'] = implementation_hashes()
            private = deepcopy(state)
            private.update(status='ready', handover=None, active_session=None)
        directory = ROOT/'.teacher/admin/run-ahead'
        directory.mkdir(parents=True, exist_ok=True)
        snapshot = directory/(item['token']+'.json')
        try:
            write_json(snapshot, private)
            log = snapshot.with_suffix('.log')
            with log.open('x') as output:
                result = subprocess.run([sys.executable, '-m', 'orchestration.run_ahead', 'worker',
                                         '--state', str(snapshot), '--auth-file', str(auth)],
                                        cwd=ROOT, stdout=output, stderr=subprocess.STDOUT)
            completed = json.loads(snapshot.read_text())
            rows = completed['runs'][len(private['runs']):]
            if result.returncode or len(rows) != 1 or rows[0]['status'] != 'awaiting_review_request':
                raise ValueError('Cycle stopped before one review draft; inspect '+str(log))
            with transaction(path) as state:
                packet = ROOT/rows[0]['packet']
                selected = verify_selection(packet,item['approved_entries_snapshot'])
                live = next(q for q in state['review_queue'] if q.get('token')==item['token'])
                live.update(selected_approved_entries=selected,packet_manifest_sha256=digest(packet/'manifest.json'))
                finish(state, item['token'], row=rows[0])
            return dict(status='awaiting_review_request', run=rows[0]['run'], snapshot=str(snapshot), log=str(log))
        except BaseException as exc:
            with transaction(path) as state:
                finish(state, item['token'], stop=dict(kind=type(exc).__name__, detail=str(exc), run=item.get('run'), position=item['position']))
            raise


def check_verdict(item, verdict, *, outcome='approved'):
    """Bind the exact request, all its artifacts, and all verdict fingerprints."""
    verdict = Path(verdict)
    run = ROOT/item['run']
    if verdict.resolve().parent != ROOT/'reviews/verdicts' or verdict.name != run.name+'.md':
        raise ValueError('Verdict filename must identify exact run')
    text = verdict.read_text()
    decision = re.search(r'(?ms)^## Decision\s*\n(.*?)(?=^## |\Z)', text)
    if not decision or item['run'] not in text:
        raise ValueError('Verdict must identify run and decision')
    if outcome == 'approved':
        if not re.search(r'APPROVED for ancestor retrieval only', decision[1], re.I) or re.search(r'\b(REJECTED|HELD|NOT approved)\b', decision[1], re.I):
            raise ValueError('Explicit approval required')
    elif not re.search(r'\b'+outcome+r'\b', decision[1], re.I):
        raise ValueError('Verdict does not state requested outcome')
    request = ROOT/item['request']
    if digest(request) != item['request_sha256']:
        raise ValueError('Request changed after publication')
    listed = re.findall(r'^- (.+): `([a-f0-9]{64})`$', request.read_text(), re.M)
    required = {legacy.relative(run/f) for f in ('draft.json','draft.md','raw-transcript.json','provenance.json')}
    required.add(item['packet']+'/manifest.json')
    if not required <= {p for p,h in listed}:
        raise ValueError('Missing required request fingerprints')
    for name, expected in listed:
        if digest(ROOT/name) != expected: raise ValueError('Request artifact changed: '+name)
    for name, expected in re.findall(r'^- `([^`]+)`: `([a-f0-9]{64})`$', text, re.M):
        artifact = run/name if '/' not in name else ROOT/name
        if digest(artifact) != expected: raise ValueError('Verdict artifact changed: '+name)
    explicit = re.search(r'^- request: `([a-f0-9]{64})`$', text, re.M)
    if explicit and digest(request) != explicit[1]: raise ValueError('Verdict request mismatch')
    return text


def approve(path, run, verdict):
    with transaction(path) as state:
        require_enabled(state)
        item = next(q for q in state['review_queue'] if q.get('run') == run)
        approval_guard(state, item)
        if item.get('implementation_sha256',implementation_hashes()) != implementation_hashes():
            raise ValueError('Queue implementation changed since authoring; recovery review required')
        check_verdict(item, verdict)
        if item['kind'] == 'replacement':
            old = item['supersedes_run']
            if old not in state['approved_entries']:
                raise ValueError('Superseded run is not active')
            row = next(r for r in state['replacement_reviews'] if r['candidate_run'] == run)
        else:
            row = next(r for r in state['runs'] if r['run'] == run)
        # Includes approval-model, immutable packet, transcript/annotation and assisted gates.
        note = f'Ancestor retrieval only. {legacy.relative(verdict)} sha256 {digest(verdict)}'
        from .ancestor_selection import installed
        with installed():
            legacy.validate_run(ROOT/run, ROOT/item['packet'], ROOT/'.sources/exllamav3.git', ROOT/'data/evidence/github', item['position'])
            legacy.approve_run(ROOT/run, ROOT/item['packet'], 'Fable', note)
        row.update(status='approved_reviewed', verdict=legacy.relative(verdict), verdict_sha256=digest(verdict))
        if item['kind'] == 'replacement':
            state['approved_entries'] = [run if r == old else r for r in state['approved_entries']]
            for previous in state['runs'] + state.get('replacement_reviews', []):
                if previous.get('run', previous.get('candidate_run')) == old:
                    previous.update(status='superseded', superseded_by=run)
        elif run not in state['approved_entries']:
            state['approved_entries'].append(run)
        item.update(status='approved_reviewed', verdict=legacy.relative(verdict), verdict_sha256=digest(verdict))
        # No change to active status, next_position, pending dependencies or a stop.
        return dict(status='approval_recorded', run=run, next_position=state['next_position'])


def recover(path, authorization, *, retry_position=None):
    """Explicit operator judgement; never inferred from queue capacity or an inbox.

    Release a stop only against a bound reviewer decision. A retry must complete
    before any new work. Failed reservations remain permanent audit history.
    """
    authorization = Path(authorization)
    with transaction(path) as state:
        require_enabled(state)
        stop = state.get('queue_stop')
        if not stop or state.get('active_session'): raise ValueError('No inactive stop to recover')
        text = authorization.read_text()
        if not text.strip() or not authorization.resolve().is_relative_to(ROOT/'reviews/verdicts'):
            raise ValueError('Recovery requires a reviewer/user decision file')
        if stop.get('run') and stop['run'] not in text:
            raise ValueError('Recovery decision must identify stopped run')
        if retry_position is None:
            if stop.get('outcome') in ('rejected','held','retry_awaiting_verdict'):
                item = next(q for q in state['review_queue'] if q.get('run') == stop['run'])
                if item['kind'] == 'forward' and not any(r['position'] == item['position'] and r['status'] in ('approved_reviewed','approved_mechanical') for r in state['runs']):
                    raise ValueError('Forward rejection still needs an approved retry')
        else:
            item = next(q for q in reversed(state['review_queue']) if (q.get('run') == stop.get('run') if stop.get('run') else q.get('position') == stop.get('position')) and q['status'] in ('failed','rejected','held'))
            if item['position'] != retry_position:
                raise ValueError('Retry must address the stopped position')
            state['retry_only'] = dict(position=retry_position, kind=item['kind'], stopped_token=item.get('token'))
        state.setdefault('recovery_log', []).append(dict(stop=stop, authorization=legacy.relative(authorization), sha256=digest(authorization), retry_position=retry_position))
        state['queue_stop'] = None
        state['status'] = 'ready'


def record_stop(path, run, verdict, outcome):
    if outcome not in ('rejected','held'):
        raise ValueError('Explicit rejection/hold required')
    verdict = Path(verdict)
    if not verdict.is_file(): raise ValueError('Missing verdict')
    with transaction(path) as state:
        require_enabled(state)
        item = next(q for q in state['review_queue'] if q.get('run') == run)
        if item['status'] != 'pending_full_review': raise ValueError('Not pending review')
        check_verdict(item, verdict, outcome=outcome)
        item.update(status=outcome, verdict=legacy.relative(verdict), verdict_sha256=digest(verdict))
        for row in state['runs'] + state.get('replacement_reviews', []):
            if row.get('run', row.get('candidate_run')) == run: row['status'] = outcome
        state['queue_stop'] = dict(outcome=outcome, run=run, verdict=legacy.relative(verdict))
        if not state.get('active_session'): state['status'] = 'stopped_recovery'


def implementation_hashes():
    return {str(p.relative_to(ROOT)):digest(p) for p in sorted((ROOT/'orchestration').glob('*.py'))}


@contextmanager
def provenance_binding(packet, output, candidates, expected_hashes):
    """Bind administrative execution metadata at every provenance write.

    This stays outside teacher input and preserves the ordinary author path.
    Selection is checked before a provider can start; failed runs retain it too.
    """
    if implementation_hashes() != expected_hashes:
        raise ValueError('Orchestration changed after reservation')
    packet, output = Path(packet), Path(output)
    selected = verify_selection(packet, candidates)
    manifest = json.loads((packet/'manifest.json').read_text())
    binding = dict(implementation_sha256=deepcopy(expected_hashes),
                   selected_approved_entries=selected,
                   ancestor_entries=deepcopy(manifest['ancestor_entries']),
                   packet_manifest_sha256=digest(packet/'manifest.json'),
                   visible_ancestor_count=len(selected),
                   strict_ancestor_count=len(manifest['history_order']),
                   sparse=len(selected) != len(manifest['history_order']))
    module = importlib.import_module('teacher.author')
    original = module.write_json
    target = (output/'provenance.json').resolve()
    def bound_write(path, value):
        if Path(path).resolve() == target:
            value = dict(value, orchestration=deepcopy(binding))
        return original(path, value)
    module.write_json = bound_write
    try:
        yield
    finally:
        module.write_json = original


def verify_selection(packet, candidates):
    """Check all exported prose against hash-bound approved artifacts, never pending."""
    from teacher.retrieval import prose, hashes, ASSEMBLY_ARTIFACTS
    from teacher.worker import load_blob
    from .ancestor_selection import selected_manifest
    manifest = json.loads((packet/'manifest.json').read_text())
    selected_manifest(manifest)
    approved = {}
    for run in candidates:
        directory = ROOT/run
        entry_file = 'entry.json' if (directory/'entry.json').exists() else 'draft.json'
        entry = json.loads((directory/entry_file).read_text())
        review = json.loads((directory/'review.json').read_text())
        names = ('entry.json','provenance.json','assembly.json') if entry_file == 'entry.json' else ('draft.json','raw-transcript.json','provenance.json')
        # Root assemblies have a distinct artifact set; use their bound names.
        if entry_file == 'entry.json': names = ASSEMBLY_ARTIFACTS
        if review.get('status') != 'approved' or not review.get('reviewer') or not review.get('reviewed_at') or review.get('sha') != entry['sha'] or review.get('approved_artifacts') != hashes(directory,names):
            raise ValueError('Unapproved or changed ancestor')
        if entry['sha'] not in manifest['commits']:
            # The approved snapshot can also contain non-ancestors; do not export them.
            continue
        source = manifest['commits'][entry['sha']]
        if entry.get('parent_shas') != source['parents'] or entry.get('cutoff_date') != source['date']:
            raise ValueError('Ancestor identity differs from source ancestry')
        if entry_file == 'entry.json' and review.get('ancestor_context_approved') is not True:
            raise ValueError('Root assembly is not approved for ancestor context')
        if entry_file == 'entry.json':
            chapters = {c['id']:prose(c['annotation']) for c in entry['chapters']}
            projected = {'sha':entry['sha'], 'chapters':chapters}
        else:
            projected = {'sha':entry['sha'], 'annotation':prose(entry['annotation'])}
            chapters = {c['id']:prose(c) for c in entry['annotation']['chapters']}
        def content_hash(value):
            return hashlib.sha256(json.dumps(value,ensure_ascii=False).encode()).hexdigest()
        ref = dict(sha=entry['sha'],prose_blob=content_hash(projected),chapters={k:content_hash(v) for k,v in chapters.items()})
        approved.setdefault(entry['sha'],[]).append((ref,run))
    selected = []
    for ref in manifest['ancestor_entries']:
        matches = [run for expected,run in approved.get(ref['sha'],[]) if expected == ref]
        if ref['sha'] not in manifest['commits'] or not matches:
            raise ValueError('Packet contains pending, altered or non-ancestor prose')
        for blob in [ref['prose_blob'], *ref['chapters'].values()]:
            load_blob(packet,blob)
        selected.append(matches[0])
    if len(selected) != len(set(selected)):
        raise ValueError('Duplicate approved prose')
    return selected


def prepared(path, auth, spec_path):
    """Execute one administratively prepared replacement/retry with the shared locks.

    Spec binds the existing recovery/plan authorization and preflight. It never
    enters a packet, prompt, transcript or teacher provenance.
    """
    from teacher.author import author
    from .ancestor_selection import installed
    spec_path = Path(spec_path)
    spec = json.loads(spec_path.read_text())
    packet, output = ROOT/spec['packet'], ROOT/spec['run']
    kind, position = spec['kind'], spec['position']
    with legacy.locked(path):
        with transaction(path) as state:
            require_enabled(state)
            if not re.fullmatch(r'commit-'+f'{position:06d}'+r'-[0-9]{3}',output.name):
                raise ValueError('Run name must identify exact position/attempt')
            if output.exists(): raise ValueError('Attempt already exists; no automatic retry')
            authorization = spec['authorization']
            decision = ROOT/authorization['path']
            if not decision.resolve().is_relative_to(ROOT/'reviews/verdicts') or digest(decision) != authorization['sha256']:
                raise ValueError('Missing or changed prepared-run authorization')
            manifest = json.loads((packet/'manifest.json').read_text())
            repo = ROOT/'.sources/exllamav3.git'
            order = legacy.git(repo,'rev-list','--reverse','--topo-order',state['history_tip']).decode().split()
            if manifest['task_sha'] != order[position-1]: raise ValueError('Wrong position/task SHA')
            if kind == 'replacement':
                old = spec['supersedes_run']
                if old not in state['approved_entries']: raise ValueError('Replacement target is not active')
                previous = json.loads((ROOT/spec['original_packet']/'manifest.json').read_text())
                if previous['task_sha'] != manifest['task_sha'] or manifest['guidance_version'] != 12 or {k:v for k,v in previous.items() if k!='guidance_version'} != {k:v for k,v in manifest.items() if k!='guidance_version'}:
                    raise ValueError('Replacement differs beyond adopted guidance')
                pf_path = ROOT/spec['preflight']['path']
                pf = json.loads(pf_path.read_text())
                if digest(pf_path) != spec['preflight']['sha256'] or pf.get('packet') != spec['packet'] or pf.get('status') != 'passed' or not pf.get('isolated_header_probe'):
                    raise ValueError('Accepted-plan header preflight required')
                attempts = [q for q in state['review_queue'] if q['kind']=='replacement' and q['position']==position]
                if attempts: raise ValueError('Replacement already attempted; new explicit plan required')
            elif kind == 'forward':
                if not state.get('retry_only') or state['retry_only']['position'] != position:
                    raise ValueError('Prepared forward work requires explicit recovery')
                previous = ROOT/spec['original_packet']/'manifest.json'
                if previous.read_bytes() != (packet/'manifest.json').read_bytes():
                    raise ValueError('Retry must preserve original packet manifest')
            else: raise ValueError('Unknown prepared work kind')
            # Original replacement packets can retain historical approved prose.
            candidates = list(state['approved_entries'])
            if kind == 'replacement':
                candidates += [r.get('run',r.get('candidate_run')) for r in state['runs']+state.get('replacement_reviews',[]) if r.get('status')=='superseded']
            selected = verify_selection(packet, candidates)
            item = reserve(state,position=position,kind=kind,files=changed_files(repo,manifest['task_sha']),run=spec['run'],packet=spec['packet'])
            live = next(q for q in state['review_queue'] if q.get('token') == item['token'])
            live.update(spec=legacy.relative(spec_path),spec_sha256=digest(spec_path),implementation_sha256=implementation_hashes(), selected_approved_entries=selected,packet_manifest_sha256=digest(packet/'manifest.json'))
            if kind == 'replacement': live['supersedes_run'] = spec['supersedes_run']
        try:
            with installed(), provenance_binding(packet,output,candidates,live['implementation_sha256']):
                legacy.validate_bundle(packet,ROOT/'data/evidence/github'/f'{position:06d}-eligible.json')
                author(packet,output,auth)
                validation = legacy.validate_run(output,packet,repo,ROOT/'data/evidence/github',position)
            report = ROOT/'reports'/f'{output.name}-queue-validation.json'
            write_json(report,validation)
            row = dict(position=position,run=spec['run'],packet=spec['packet'],status='awaiting_review_request',validation=legacy.relative(report),spec_sha256=digest(spec_path))
            with transaction(path) as state: finish(state,item['token'],row=row)
            return dict(status='awaiting_review_request',run=spec['run'],validation=legacy.relative(report))
        except BaseException as exc:
            with transaction(path) as state:
                finish(state,item['token'],stop=dict(kind=type(exc).__name__,detail=str(exc),run=spec['run'],position=position))
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('enable','cycle','worker','publish','approve','stop','recover','prepared'))
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--auth-file', type=Path, default=Path.home()/'.codex/auth.json')
    parser.add_argument('--run'); parser.add_argument('--request', type=Path)
    parser.add_argument('--verdict', type=Path); parser.add_argument('--outcome')
    parser.add_argument('--spec', type=Path)
    parser.add_argument('--retry-position', type=int)
    args = parser.parse_args()
    if args.action == 'enable': result = enable(args.state,args.verdict)
    elif args.action == 'worker': result = worker(args.state,args.auth_file)
    elif args.action == 'cycle': result = run(args.state,args.auth_file)
    elif args.action == 'prepared': result = prepared(args.state,args.auth_file,args.spec)
    elif args.action == 'recover': result = recover(args.state,args.verdict,retry_position=args.retry_position)
    elif args.action == 'publish':
        with transaction(args.state) as state: publish(state,args.run,args.request)
        result = dict(status='request_published')
    elif args.action == 'approve': result = approve(args.state,args.run,args.verdict)
    else: result = record_stop(args.state,args.run,args.verdict,args.outcome)
    print(json.dumps(result))


if __name__ == '__main__': main()
