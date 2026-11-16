# SPDX-License-Identifier: MIT
"""Administrative walk orchestration. Never imported by a teacher worker.

Blocks through one review handoff (including intervening mechanical commits).
Judgement stops precede authoring; requests remain skeletons until edited/filed.
"""
import argparse
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil

from .author import author, write_json
from .packet import git
from .walk_inputs import prepare, validate_bundle, references
from .graph_packet import attach_graphs
from .ancestor_context import attach_entries, approve_run
from .approval_policy import assess, approve_mechanical
from .runner import Runner
from .blob_store import store_root

ROOT = Path(__file__).resolve().parents[1]
MIN_FREE_BYTES = 2 * 1024**3
TRACKING = ROOT / 'reviews/ASTRA-TRACKING.md'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def relative(path):
    path = Path(path).resolve()
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


class Stop(Exception):
    def __init__(self, status, detail):
        self.status, self.detail = status, detail
        super().__init__(detail)


@contextmanager
def locked(state_path):
    with Path(str(state_path) + '.cycle.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Stop('busy', 'Another cycle/approval holds the state lock')
        yield


def tracking_status(state):
    """Keep a small current status above the append-only obligation register."""
    text = TRACKING.read_text() if TRACKING.exists() else '# Astra tracking — administrative only\n'
    block = '<!-- cycle-status -->\n' + '\n'.join([
        'Current journal status: `' + str(state.get('status')) + '`.',
        'Next position: `' + str(state.get('next_position')) + '`.',
        'Handover: `' + json.dumps(state.get('handover'), sort_keys=True) + '`.',
        'Advancement pause: `' + json.dumps(state.get('advancement_pause'), sort_keys=True) + '`.',
    ]) + '\n<!-- /cycle-status -->'
    if '<!-- cycle-status -->' in text:
        text = re.sub(r'(?s)<!-- cycle-status -->.*?<!-- /cycle-status -->', lambda _:block, text)
    else:
        first, separator, rest = text.partition('\n')
        text = first + '\n\n' + block + '\n' + rest
    TRACKING.write_text(text)


def guard_state(state):
    if state.get('advancement_pause'):
        raise Stop('advancement_paused', 'Explicit administrative advancement pause')
    if state.get('status') != 'ready':
        raise Stop('state_not_ready', str(state.get('status')))


def guard_disk(root):
    free = shutil.disk_usage(root).free
    if free < MIN_FREE_BYTES:
        raise Stop('low_disk', f'{free} bytes free; need {MIN_FREE_BYTES}')
    return free


def architecture_gate(repo, sha, evidence):
    from .architecture_evidence import trigger_details, load_bundle
    details = trigger_details(repo, sha)
    if details.get('unresolved_class_files'):
        raise Stop('unresolved_architecture', 'Unresolved architecture class files require review')
    # The caller supplies the exact position's reference bundle, not a directory.
    path = Path(evidence)
    if path.exists():
        try:
            bundle = load_bundle(repo, sha, path)
        except ValueError as error:
            raise Stop('invalid_reference_bundle', str(error))
        if bundle and bundle.get('unresolved_architecture_files'):
            raise Stop('unresolved_reference_bundle', 'Reference bundle has unresolved files')
        if bundle and bundle.get('administrative_outcome', {}).get('basis') == 'curator_attestation':
            raise Stop('curator_attestation', 'Curator attestation needs explicit full review')
    if details.get('registry_architectures') or details.get('derived_architectures') or details.get('class_files'):
        raise Stop('architecture_trigger', 'Architecture discovery/recovery needs author judgement; use the manual path')


def catalog_selection(repo, sha, cutoff, histories, excluded):
    from .closed_discussions import select, task_terms, message_terms, task_paths, CAP
    from .recover_github import parent_tree_paths
    paths = parent_tree_paths(repo, sha)
    args = (histories, cutoff, task_terms(repo, sha), paths, excluded)
    kw = dict(message=message_terms(repo, sha))
    cap = max(CAP, len(histories))
    legacy = select(*args, **kw, cap=cap)
    unlimited = select(*args, **kw, changed_paths=task_paths(repo, sha), cap=cap)
    selected = select(*args, **kw, changed_paths=task_paths(repo, sha))
    lexical = {r['url'] for r in legacy['items']}
    kept = {r['url'] for r in selected['items']}
    cut = [r for r in unlimited['items'] if r['url'] not in kept and r['matched_paths']]
    report = dict(rule=selected['rule'], qualified_count=selected['qualified_count'],
                  selected_count=len(selected['items']),
                  path_only_qualified_count=sum(r['url'] not in lexical for r in unlimited['items']),
                  path_only_selected_count=sum(r['url'] not in lexical for r in selected['items']),
                  cap=CAP, truncated=selected['truncated'],
                  path_qualified_cut=[{k:r[k] for k in ('kind','number','matched_paths')} for r in cut],
                  authoring_allowed=not cut)
    selected.update(task_sha=sha, cutoff=cutoff, complete=True)
    return selected, report


def guard_catalog(report):
    if report['path_qualified_cut'] or not report['authoring_allowed']:
        raise Stop('path_catalog_truncated', 'Propose an ordering before any teacher run')


def write_new(path, value):
    path = Path(path)
    if path.exists():
        raise Stop('existing_preparation', f'Refusing to overwrite {path}')
    write_json(path, value)


def recover_inputs(repo, sha, position, evidence, reports):
    """Same helpers/order as the former scripts; no discussion-history cache change."""
    from .recover_github import repository_discussions, recover, parent_tree_paths, repo_path_hints, bounded_discussions
    from .evidence import discussion_snapshot, eligible_content
    evidence, reports = Path(evidence), Path(reports)
    prefix = f'{position:06d}'
    if any((evidence / f'{prefix}-{suffix}.json').exists() for suffix in ('eligible','unreferenced','closed','recovered-none')):
        raise Stop('existing_preparation', 'Existing bundles require manual validation; never overwrite bound inputs')
    cutoff = git(repo, 'show', '-s', '--format=%cI', sha).decode().strip()
    message = git(repo, 'show', '-s', '--format=%B', sha).decode().rstrip('\n')
    wanted = set()
    for ref in references(message):
        match = re.fullmatch(r'#(\d+)', ref) or re.fullmatch(r'https?://github.com/turboderp-org/exllamav3/(?:issues|pull)/(\d+)', ref)
        if not match:
            raise Stop('reference_needs_judgement', f'Unrecognised explicit reference: {ref}')
        wanted.add(int(match[1]))
    histories = []
    for kind, number in repository_discussions('turboderp-org', 'exllamav3', cutoff):
        bundle = recover('turboderp-org', 'exllamav3', number)
        if bundle['kind'] != kind:
            raise ValueError('Discussion kind mismatch')
        histories.append(bundle)
        write_json(evidence / f'discussion-{kind}-{number}-history.json', bundle)
    matched = [b for b in histories if b['number'] in wanted]
    if {b['number'] for b in matched} != wanted:
        raise Stop('reference_needs_judgement', 'Referenced discussion absent at cutoff; recovered-none needs review')
    eligible = []
    for bundle in matched:
        for obj in bundle['objects']:
            item = eligible_content(obj, cutoff)
            if item is not None:
                item['retrieved_at'] = bundle['retrieved_at']
                eligible.append(item)
    if wanted and not eligible:
        raise Stop('reference_needs_judgement', 'No eligible referenced content; recovered-none needs review')
    paths = parent_tree_paths(repo, sha)
    items = []
    for bundle in histories:
        row = discussion_snapshot(bundle, cutoff)
        if row is not None:
            hints = repo_path_hints(row, paths)
            if hints is not None:
                row.update(hints)
            items.append(row)
    items, truncated = bounded_discussions(items)
    closed, report = catalog_selection(repo, sha, cutoff, histories, {b['url'] for b in matched})
    report_path = reports / f'commit-{prefix}-catalog-selection-001.json'
    write_new(report_path, report)
    guard_catalog(report)
    if eligible:
        write_new(evidence / f'{prefix}-eligible.json', dict(task_sha=sha, cutoff=cutoff, items=eligible))
    write_new(evidence / f'{prefix}-unreferenced.json', dict(task_sha=sha, cutoff=cutoff, complete=True, limit=100, truncated=truncated, items=items))
    write_new(evidence / f'{prefix}-closed.json', closed)
    return report_path


def index_parent(position, records, store):
    from graph.timeline import Timeline
    from graph.index_commit import build
    if position <= 1:
        return
    paths = list(Path(records).glob(f'{position-1:06d}_*.json'))
    if len(paths) != 1:
        raise ValueError('Missing or ambiguous preceding graph record')
    timeline = Timeline(Path(store) / 'timeline.sqlite')
    try:
        timeline.ingest(build(read(paths[0])))
    finally:
        timeline.close()


def prepare_packet(repo, sha, position, packet, evidence, store, sources, *, ancestor_packets=None):
    """Only existing builders; no orchestration metadata enters the packet."""
    manifest = prepare(repo, sha, position, packet, evidence, ancestor_packets=ancestor_packets)
    attach_graphs(packet, store)
    selected = []
    for source in map(Path, sources):
        file = source / ('entry.json' if (source / 'entry.json').exists() else 'draft.json')
        if read(file)['sha'] in manifest['commits']:
            selected.append(source)
    attach_entries(packet, selected)
    validate_bundle(packet, Path(evidence) / f'{position:06d}-eligible.json')
    return read(Path(packet) / 'manifest.json')


def validate_run(run, packet, repo, evidence, position):
    run, packet = Path(run), Path(packet)
    validate_bundle(packet, Path(evidence) / f'{position:06d}-eligible.json')
    decision = assess(run, packet, repo)
    provenance, manifest = read(run/'provenance.json'), read(packet/'manifest.json')
    if provenance['packet_manifest_sha256'] != digest(packet/'manifest.json'):
        raise ValueError('Manifest fingerprint mismatch')
    for file, expected in provenance['implementation_sha256'].items():
        if digest(ROOT/file) != expected:
            raise ValueError('Implementation hash mismatch: '+file)
    coverage = manifest.get('coverage_request')
    if bool(coverage) != bool(provenance.get('reviewer_assisted')):
        raise ValueError('Assistance provenance mismatch')
    if coverage and provenance.get('coverage_request') != {k:coverage[k] for k in ('path','sha256')}:
        raise ValueError('Coverage provenance mismatch')
    blobs = list((packet/'blobs').iterdir())
    for blob in blobs:
        if (digest(blob) != blob.name or blob.stat().st_mode & 0o222 or
                not os.path.samefile(blob, store_root(packet)/blob.name)):
            raise ValueError('Blob integrity/link failure: '+blob.name)
    transcript = read(run/'raw-transcript.json')
    calls = {c['id']:c for x in transcript if x.get('role')=='assistant' for c in x.get('calls',[])}
    counts, replayed = Counter(), 0
    runner = Runner(packet)
    for result in transcript:
        if result.get('role') != 'tool':
            continue
        call = calls[result['call_id']]
        if runner.invoke(call['tool'], call['arguments']) != json.loads(result['content']):
            raise ValueError('Tool replay mismatch: '+result['call_id'])
        counts[result['name']] += 1
        replayed += 1
    cov = read(run/'coverage.json')
    return dict(status='validated', assessment=decision, packet_implementation_blob_hashes_verified=True,
                reviewer_assisted=bool(coverage), tool_counts=dict(counts), identical_replayed_calls=replayed,
                shared_readonly_blob_links_verified=len(blobs), open_catalog_rows=len(manifest['unreferenced_discussion_catalog']),
                closed_catalog_rows=len(manifest['closed_discussion_catalog']['rows']),
                task_sections_total=cov['task_sections_total'], fully_read_task_sections=cov['fully_read_task_sections'],
                ancestor_prose_read_count=cov.get('retrieval_usage',{}).get('ancestor_prose_read_count'),
                runtime={k:provenance[k] for k in ('codex_version','python_version','machine_architecture','operating_system')})


def make_summary(run, packet, repo, position, report_path, catalog_path, evidence):
    run, packet = Path(run), Path(packet)
    validation = read(report_path)
    files = [run/name for name in ('draft.json','draft.md','raw-transcript.json','provenance.json','coverage.json')]
    files += [packet/'manifest.json', Path(report_path), Path(catalog_path)]
    for suffix in ('eligible','unreferenced','closed','references','recovered-none'):
        path = Path(evidence)/f'{position:06d}-{suffix}.json'
        if path.exists(): files.append(path)
    # Bind run arguments separately so the author can distinguish file reads from scalar checks.
    run_calls = [c for x in read(run/'raw-transcript.json') for c in x.get('calls',[]) if c['tool']=='run']
    return dict(status='awaiting_author_request', position=position, run=relative(run), packet=relative(packet),
                sha=read(packet/'manifest.json')['task_sha'],
                title=git(repo,'show','-s','--format=%s',read(packet/'manifest.json')['task_sha']).decode().strip(),
                validation=validation, catalog=read(catalog_path), run_calls=run_calls,
                hashes={relative(p):digest(p) for p in files})


def skeleton(summary, thread):
    v, c = summary['validation'], summary['catalog']
    text = f"# Review request: {Path(summary['run']).name}\n\nReply-to thread: {thread}\n\n"
    text += f"Run: `{summary['run']}`\nPacket: `{summary['packet']}`\nUpstream: `{summary['sha']}` — \"{summary['title']}\" (copied from Git).\n"
    text += 'Requested scope: ancestor retrieval only. Canonical and training remain false.\n\n'
    text += f"Reviewer-assisted: {v['reviewer_assisted']}. {v['identical_replayed_calls']} calls replay identically; {v['shared_readonly_blob_links_verified']} read-only shared-store blobs verified.\n"
    text += f"Task sections fully read: {len(v['fully_read_task_sections'])}/{v['task_sections_total']}; ancestor prose reads (report-only): {v['ancestor_prose_read_count']}.\n"
    text += f"Tool counts: {json.dumps(v['tool_counts'],sort_keys=True)}. Runtime: {json.dumps(v['runtime'],sort_keys=True)}.\n\n"
    text += f"Catalog: {v['open_catalog_rows']} open rows; {c['qualified_count']} closed qualify, {c['selected_count']} selected; {c['path_only_qualified_count']} by path alone, {c['path_only_selected_count']} selected by path alone. Cap {c['cap']}; truncated: {c['truncated']}; path rows cut: {len(c['path_qualified_cut'])}.\n\n"
    text += 'AUTHOR JUDGEMENT REQUIRED: explain the draft/findings, execution scope and run file reads, ledger candidates, implementation changes/tests, unusual evidence or coverage limits, and sampled mechanical handover. This skeleton is not a filed request.\n\n## SHA256\n\n'
    return text + ''.join(f'- {p}: `{h}`\n' for p,h in summary['hashes'].items())


def cycle(state_path, auth_file):
    state_path = Path(state_path)
    with locked(state_path):
        state = read(state_path)
        try:
            guard_state(state)
            repo, evidence, reports = ROOT/'.sources/exllamav3.git', ROOT/'data/evidence/github', ROOT/'reports'
            order = git(repo,'rev-list','--reverse','--topo-order',state['history_tip']).decode().split()
            while state['next_position'] <= len(order):
                position = state['next_position']; sha = order[position-1]
                if any(r.get('position') == position and r.get('status') in ('preparing','authoring','running') for r in state['runs']):
                    raise Stop('half_started_run', 'Existing incomplete run requires explicit recovery')
                guard_disk(ROOT)
                architecture_gate(repo,sha,evidence/f'{position:06d}-references.json')
                catalog_path = recover_inputs(repo,sha,position,evidence,reports)
                index_parent(position, ROOT/'data/exllamav3-v5/records', ROOT/'store')
                attempt = 1
                while (ROOT/f'.teacher/retrieval/{position:06d}-{attempt:03d}').exists() or (ROOT/f'.teacher/runs/commit-{position:06d}-{attempt:03d}').exists():
                    attempt += 1
                packet = ROOT/f'.teacher/retrieval/{position:06d}-{attempt:03d}'
                run = ROOT/f'.teacher/runs/commit-{position:06d}-{attempt:03d}'
                record = dict(position=position,sha=sha,run=relative(run),packet=relative(packet),status='preparing')
                state['runs'].append(record); state['status']='running'; write_json(state_path,state)
                prepare_packet(repo,sha,position,packet,evidence,ROOT/'store',[ROOT/p for p in state['approved_entries']])
                guard_disk(ROOT)
                record['status']='authoring'; write_json(state_path,state)
                author(packet,run,auth_file)
                result = validate_run(run,packet,repo,evidence,position)
                report_path = reports/f'commit-{position:06d}-validation-{attempt:03d}.json'
                write_new(report_path,result)
                summary = make_summary(run,packet,repo,position,report_path,catalog_path,evidence)
                summary_path = reports/f'commit-{position:06d}-cycle-{attempt:03d}.json'
                write_new(summary_path,summary)
                skeleton_path = ROOT/f'reviews/requests/commit-{position:06d}-{attempt:03d}.skeleton.md'
                with skeleton_path.open('x') as f:f.write(skeleton(summary,os.environ.get('CODEX_THREAD_ID','AUTHOR MUST FILL THREAD')))
                record.update(result['assessment'])
                if record['tier']=='full_review':
                    record['status']='awaiting_review_request';state['status']='awaiting_review_request'
                    samples=[r for r in state['runs'] if r.get('tier')=='mechanical' and r.get('sampled') and not r.get('sample_handed_over')]
                    state['handover']=dict(full_review=record['run'],sampled_mechanical=[r['run'] for r in samples])
                    for r in samples:r['sample_handed_over']=True
                    write_json(state_path,state);tracking_status(state)
                    return dict(status=state['status'],summary=relative(summary_path),skeleton=relative(skeleton_path),draft=relative(run/'draft.md'),validation=result,catalog=summary['catalog'],hashes=summary['hashes'])
                approve_mechanical(run,packet,repo)
                record['status']='approved_mechanical';state['approved_entries'].append(record['run'])
                state.update(status='ready',next_position=position+1);write_json(state_path,state)
            state['status']='complete';write_json(state_path,state);return dict(status='complete')
        except Stop as stop:
            # Preserve existing pauses/review gates verbatim; a new stop never authorises retry.
            if state['status'] in ('ready','running'):
                state['status']='stopped_cycle';state['cycle_stop']=dict(status=stop.status,detail=stop.detail)
                write_json(state_path,state)
            return dict(status=stop.status,detail=stop.detail)
        except BaseException as error:
            state.update(status='stopped_failure',error_type=type(error).__name__)
            write_json(state_path,state)
            raise


def approval(state_path, verdict):
    """Explicit operator invocation, not automatic interpretation of an inbox."""
    state_path, verdict = Path(state_path), Path(verdict)
    with locked(state_path):
        state=read(state_path);handover=state.get('handover') or {}
        if state['status']!='awaiting_full_review' or not handover.get('full_review'):
            raise Stop('approval_state_mismatch','No pending full-review handover')
        run=ROOT/handover['full_review'];record=next(r for r in state['runs'] if r['run']==handover['full_review'])
        if verdict.name != run.name+'.md':raise ValueError('Verdict filename does not identify pending run')
        text=verdict.read_text()
        decision=re.search(r'(?ms)^## Decision\s*\n(.*?)(?=^## |\Z)',text)
        if not decision or not re.search(r'APPROVED for ancestor retrieval only',decision[1]) or re.search(r'\b(REJECTED|HELD)\b',decision[1]):
            raise Stop('verdict_needs_judgement','Only an explicit approval can be recorded by this command')
        if handover['full_review'] not in text:raise ValueError('Verdict does not name pending run')
        request=ROOT/handover['request'];listed=re.findall(r'^- (.+): `([a-f0-9]{64})`$',request.read_text(),re.M)
        required={relative(run/f) for f in ('draft.json','draft.md','raw-transcript.json','provenance.json')}
        required.add(record['packet']+'/manifest.json')
        if not required <= {p for p,h in listed}:raise ValueError('Request missing required artifact hashes')
        for p,h in listed:
            if digest(ROOT/p)!=h:raise ValueError('Review request hash mismatch: '+p)
        for name, expected in re.findall(r'^- `([^`]+)`: `([a-f0-9]{64})`$', text, re.M):
            artifact = run/name if '/' not in name else ROOT/name
            if digest(artifact) != expected:raise ValueError('Verdict artifact hash mismatch: '+name)
        explicit_request = re.search(r'^- request: `([a-f0-9]{64})`$', text, re.M)
        if explicit_request and digest(request) != explicit_request[1]:raise ValueError('Verdict request hash mismatch')
        note=f'Ancestor retrieval only. {relative(verdict)} sha256 {digest(verdict)}'
        approve_run(run,ROOT/record['packet'],'Fable',note)
        record.update(status='approved_reviewed',verdict=relative(verdict),verdict_sha256=digest(verdict))
        state['approved_entries'].append(record['run']);state.update(status='ready',next_position=record['position']+1,handover=None)
        # A new block preserves every follow-up verbatim. Closing items is author judgement.
        sections=[]
        for title in ('Follow-ups','Must fix before canonical use'):
            found=re.search(r'(?ms)^## '+re.escape(title)+r'\s*\n(.*?)(?=^## |\Z)',text)
            if found:sections.append(f'### {title}\n\n'+found[1].strip())
        with TRACKING.open('a') as f:
            f.write(f'\n## Recorded {verdict.stem}\n\n{note}\n\n'+'\n\n'.join(sections)+'\n')
        write_json(state_path,state);tracking_status(state)
        return dict(status='approval_recorded',next_position=state['next_position'],advancement_pause=state.get('advancement_pause'),verdict_sha256=digest(verdict))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state',type=Path,required=True)
    parser.add_argument('--auth-file',type=Path,default=Path.home()/'.codex/auth.json')
    parser.add_argument('--approve',type=Path,help='Explicitly record this pending run approval and track follow-ups')
    args=parser.parse_args()
    try:result=approval(args.state,args.approve) if args.approve else cycle(args.state,args.auth_file)
    except Stop as stop:result=dict(status=stop.status,detail=stop.detail)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
