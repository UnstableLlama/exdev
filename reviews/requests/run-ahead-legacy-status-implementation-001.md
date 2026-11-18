# Run-ahead legacy status compatibility and 256 approval recovery

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

256 is approved by your verdict, but the accepted queue approval command refuses it with `Earlier forward position unresolved`. No approval or journal mutation occurred in that invocation; no 257 teacher session started. The diagnosis lists five historical rows at positions17,32,39,41 whose superseded labels predate migration. Each position has an approved successor recorded in replacement_reviews; the guard also previously looked only in runs. Existing history and authored artifacts remain unchanged.

The narrow patch recognizes exactly `superseded_missing_inputs` and `superseded_for_future_retrieval` alongside `superseded`. The approved-position set now includes approved rows in replacement_reviews as well as runs, consistently in both queue-order and unresolved-position checks. The subsequent guard still requires an approved attempt at every earlier position. Regressions exercise both labels with and without an approved successor, and a position whose only approval is in replacement_reviews (rejection remains blocked). The corrected guard passes against the live journal in a read-only check. No teacher, packet, validation, approval-scope, selection or migration behavior is changed.

Please review this implementation and authorize recovery of the queued256 approval: after acceptance, update its queue item's orchestration implementation-hash binding from the accepted original to this reviewed implementation, and rebind its request to the recovery supplement bound below, retaining both original bindings in the recovery report; rerun ordinary queue approval against your unchanged256 verdict; clear the accepted dependency-gap advancement pause citing that verdict; then launch257. Run provenance, packet, reservation snapshot and authored artifacts stay immutable. The recovery supplement preserves the original request byte for byte except its bound orchestration source hash, plus a disclosure and binding to the original request; the original request is not edited. This explicit recovery is needed because both the queue implementation pin and original request source fingerprint intentionally refuse code changes since authoring. No automatic pin bypass or legacy approval command was used.

For the two asks owed with257: 255's prior manual recording updated review.json and the journal run row but omitted approved_entries. I have not established that the unusual verdict filename caused it; attributing that would be speculation. The queue's successful approve path appends the run to approved_entries and marks the row and queue approved within one journal transaction, so that particular manual journal omission is prevented. Its run-level approval write precedes journal commit, so failures after that write can still require explicit reconciliation; this is not a claim of cross-file atomicity. This attempt failed in the initial guard, before that write.

234 overflow r005 is accepted. The256 serialization-fix ledger revision remains owed with257's request. No commit/push. No teacher session on this unaccepted implementation.

Validation results and bindings follow.

24 focused tests passed. Full host-enabled suite: `EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests`: 332 tests passed in 108.364 seconds. The read-only compatibility check passes on the current journal.

SHA-256 bindings (journal is the unchanged pre-recovery state):

- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
- tests/test_run_ahead.py: `55dae815e60709c2ecdb5303aff42581cc9cb7fefb9e988037cd4f84eed41bda`
- reports/run-ahead-legacy-status-001/implementation.patch: `0a01462ca53cd5db807c2aca43c5c30d1d8150947467a736b2f39b5e989d4d78`
- reports/run-ahead-legacy-status-001/diagnosis.json: `b8fda8b3765bd78b75d5349d3f4b441223f92c2601bb6018e3f9d1102f12ae04`
- reports/run-ahead-legacy-status-001/focused.log: `9983a40197e463a3c34a39d19173c86248aa869d148b36aaa2941ef85ffae0fe`
- reports/run-ahead-legacy-status-001/suite.log: `59fdaaa8027d5fb9f12a86d5afb45fc137d5ecab6e499fd0583a3b24c699b486`
- reports/run-ahead-legacy-status-001/run_ahead.before.py: `c3585aab08de60d289caf0fc5290da06307848966569e427dd1c431431a1a67d`
- reports/run-ahead-legacy-status-001/test_run_ahead.before.py: `03be97fedf54a9c29b2161c1cf47b443b26e363cad571a11e42918e3cf4ef866`
- reports/run-ahead-legacy-status-001/commit-000256-001.recovery-request.md: `1049c0ebe2760ed08b85734fce5ed10d06db10854c1b393b46bc226ac7769c88`
- reviews/requests/commit-000256-001.md: `3f17c03fb762790785472ce399d3b03d6a84e4f07a61c3a4b9ccf059f40a0248`
- reviews/verdicts/commit-000256-001.md: `53aa4adca50b5cbb0917574c9da515fda8d9bf4bac4dc6888224fe5fe240c1db`
- reports/teacher-walk-001.json: `0ee678aa3c46e9dbb42c3d1cbf4c1498e3c194694d907e1d76a563e99160a3b4`
