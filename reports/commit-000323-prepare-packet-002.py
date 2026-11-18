"""Build the authorised 323 retry input and audit differences from 001."""
import re
from pathlib import Path

from orchestration.ancestor_selection import installed
from orchestration.run_ahead import implementation_hashes, verify_selection
from teacher import cycle
from teacher.blob_store import store_root, verify

state = cycle.read('reports/teacher-walk-001.json')
prior_run = '.teacher/runs/commit-000323-001'
prior = next(row for row in state['review_queue'] if row.get('run') == prior_run)
assert prior['status'] == 'rejected' and state['queue_stop']['run'] == prior_run
assert state['next_position'] == 324 and not any(
    state.get(field) for field in ('active_session', 'advancement_pause', 'retry_only')
)
assert state['approved_entries'] == prior['approved_entries_snapshot']
assert implementation_hashes() == prior['implementation_sha256']
provenance = cycle.read(Path(prior_run) / 'provenance.json')
assert (provenance['model'], provenance['reasoning_effort']) == ('gpt-6.2-sol', 'medium')
for path, expected in provenance['implementation_sha256'].items():
    assert cycle.digest(path) == expected, path

request = Path(prior['request'])
assert cycle.digest(request) == prior['request_sha256']
bindings = dict(re.findall(r'^- ([^:\n]+): `([0-9a-f]{64})`$', request.read_text(), re.M))
assert len(bindings) == 16
for path, expected in bindings.items():
    assert cycle.digest(path) == expected, path

existing = Path(prior['packet'])
packet = Path('.teacher/retrieval/000323-002')
assert not packet.exists()
coverage = Path('reviews/verdicts/commit-000323-002.coverage.md')
coverage_hash = 'e53791ad0169bb4395b7373bc429d7c9a109e3e67c4f67cccf9fff44091b0486'
sha = '544ba423bf9c58c940dca6cb36a1aa93f6cda41a'
evidence = Path('data/evidence/github')
old = cycle.read(existing / 'manifest.json')
with installed():
    cycle.prepare(Path('.sources/exllamav3.git').resolve(), sha, 323, packet, evidence,
                  coverage_request=coverage, coverage_sha256=coverage_hash)
    cycle.attach_graphs(packet, Path('store'))
    cycle.attach_entries(packet, list(map(Path, state['approved_entries'])))
cycle.validate_bundle(packet, evidence / '000323-eligible.json')
new = cycle.read(packet / 'manifest.json')
assert new.pop('coverage_request') == dict(path=str(coverage), sha256=coverage_hash,
                                          text=coverage.read_text())
contract = new['walk_input_contract']
assert contract.pop('coverage_request_path') == str(coverage)
assert contract.pop('coverage_request_sha256') == coverage_hash
assert old.keys() == new.keys()
assert all(old[key] == new[key] for key in old), [key for key in old if old[key] != new[key]]
selected = verify_selection(packet, state['approved_entries'])
assert selected == prior['selected_approved_entries'] and len(selected) == 322

blobs = sorted((packet / 'blobs').iterdir())
assert [blob.name for blob in blobs] == sorted(p.name for p in (existing / 'blobs').iterdir())
assert len(blobs) == 4570
for blob in blobs:
    verify(blob, blob.name)
    assert blob.samefile(existing / 'blobs' / blob.name)
    assert blob.samefile(store_root(packet) / blob.name)
    assert not blob.stat().st_mode & 0o222
for path, expected in bindings.items():
    assert cycle.digest(path) == expected, path

report = dict(
    original_packet=str(existing), packet=str(packet),
    original_manifest_sha256=cycle.digest(existing / 'manifest.json'),
    manifest_sha256=cycle.digest(packet / 'manifest.json'),
    changed_manifest_keys=['coverage_request', 'walk_input_contract'],
    changed_contract_keys=['coverage_request_path', 'coverage_request_sha256'],
    old_ancestor_count=len(selected), new_ancestor_count=len(selected),
    added_ancestors=[], existing_ancestor_entries_equal=True, original_files_preserved=True,
    approved_selection_verified=True, shared_readonly_blob_links_verified=len(blobs),
    coverage_request=dict(path=str(coverage), sha256=coverage_hash),
    reference_bundle_sha256=contract['reference_bundle_sha256'],
    published_request_sha256=prior['request_sha256'], original_request_bindings_verified=len(bindings),
    teacher_started=False,
)
comparison = Path('reports/commit-000323-retry-packet-002.json')
assert not comparison.exists()
cycle.write_json(comparison, report)
print(comparison, cycle.digest(comparison), flush=True)
