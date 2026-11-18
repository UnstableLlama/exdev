# Run-ahead migration 001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Please review the journal migration required by run-ahead-implementation-002, condition 2. No teacher session has started; 256 waits for your answer. Nothing committed or pushed.

234/002 is recorded as approved for ancestor retrieval only and replaces234/001 in the active approved-entry selection. The old artifacts remain history. The refreshed dependent inventory still lists235,241,248; none was re-authored. All three255 ledger records are accepted. Canonical/training approval remains false.

Migration ran only after the journal was ready at256, with no handover, pending replacement review or active session. The byte backup and post-migration snapshot are bound below. The diff adds only `review_queue: []`, `active_session: null`, and the enabled `run_ahead` object bound to your implementation verdict. Every existing field, including all approvals, history and next_position256, is unchanged. The live journal matches the after snapshot.

Before migration I completed condition 3 in `orchestration/run_ahead.py`: both ordinary queued authoring and prepared runs now bind orchestration Python-file hashes, selected approved run paths, bound ancestor entries, packet manifest hash, visible/strict ancestor counts and sparse status into the run's `provenance.json` under `orchestration`. Selection and code hashes are checked before authoring; repeated and failure provenance writes retain the binding. The temporary writer wrapper restores on exit. Teacher files, prompts and packet contents were unchanged by this addition.

Two added tests cover repeated/failure writes, restoration, unrelated writes, changed-code refusal and unapproved-selection refusal; the existing private-worker test was adapted for its reservation lookup. Full host-enabled suite: **330 tests, OK**,115.463 seconds (`EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests`). An initial sandboxed focused run hit the host namespace restriction and exposed the fixture adjustment; the complete host-enabled run passed afterward. Existing packet/prompt/command identity coverage remains passing.

After acceptance, use the queue driver with one teacher session at a time, at most three unresolved requests, finished requests filed before another launch, and approvals recorded in ascending forward order. Each run-ahead request will name the positions it ran ahead of, state sparse versus complete, and report visible versus strict ancestor counts. No first live queue/provider run has occurred.

234 follow-ups remain administrative: add its table consequence as an observation of the existing231 resize-overflow identity with the next commit request; retain the missing-lm_head-suffix reviewer observation until its ledger origin is supported. No reviewer material enters teacher input. Revision-mode implementation002/token retention remains separately owed.

## SHA-256 bindings

| File | SHA-256 |
| --- | --- |
| `reports/run-ahead-migration-001.before.json` | `6c08987cddaa9b0d8444f41da11e7a46c34570d333e78e307373b783d53f7855` |
| `reports/run-ahead-migration-001.after.json` | `573ec55cd28d19ad3285a25eba7c303e0d7ead7db58dcd49558a2b83e3a72ce1` |
| `reports/run-ahead-migration-001.diff` | `ab48ebc34cd991efc762106ea6a2804b618a4e0f904157247adf38cb234e2870` |
| `reports/run-ahead-migration-001.json` | `db84e1cc69fc1da9b2d79991be02473df22c3d442ad21b2cbeab6788cbb6b7fb` |
| `reports/run-ahead-migration-001-full-tests.log` | `dee1ed9abf8c8e5ff1920c98aa7f48670666150514e17cd091cc41a94ebfc326` |
| `reviews/verdicts/run-ahead-implementation-002.md` | `3d7d471280fe388ce19a7da7e81f8316cee92a7aefa96c700992525169a99e14` |
| `reviews/verdicts/run-ahead-001.decision.md` | `0fbb5b4728164d65bd51a5e883831e2bac825d7fcf64ddb4f0095ce0fbeeedb0` |
| `reviews/verdicts/commit-000234-002.md` | `9b3a75cb0f93768fc25ce94620cf9ecf475aa6a6239b1bf44e92dd8babd550c5` |
| `reviews/requests/commit-000234-002.md` | `443c6d1019ae723fbc7bc569538a3fb961428f173c4f9658555d6875d8a94e46` |
| `reports/commit-000234-replacement-dependents-approval-002.json` | `9b27d22abe3afde301ebb48fad4dd8ebf7df873b29d34524c98336ac839428d8` |
| `tests/test_run_ahead.py` | `03be97fedf54a9c29b2161c1cf47b443b26e363cad571a11e42918e3cf4ef866` |
| `orchestration/__init__.py` | `68915857024c488a95f5e3551c720604a70120c5551b9ece25b8ddb79e88954a` |
| `orchestration/ancestor_selection.py` | `d28216a56e79cd9ab0de457967cc5218622a8a3c198f798f1490826c06302d2c` |
| `orchestration/notify.py` | `db348ead800ebaba14c6e1a061831ee869a733113be2765ef07ac5590948e821` |
| `orchestration/run_ahead.py` | `c3585aab08de60d289caf0fc5290da06307848966569e427dd1c431431a1a67d` |
