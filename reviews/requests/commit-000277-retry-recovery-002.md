# Recovery mechanics: fresh 277/002 with complete ancestor selection

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

277/001 is recorded as rejected under your verdict; its 18 request bindings were rechecked. Both 276 ledger records are accepted. No prose or authored run was changed. 278 was already running when the rejection arrived; the queue stop prevents further launches, and its request will assess the missing 277 entry.

The requested new packet `.teacher/retrieval/000277-002` is prepared, with all 276 strict ancestor entries, including approved 276. The first 275 prose references are identical to 001. Every original non-manifest packet file is preserved byte for byte; only the ancestor entries, approved selection, and derived ancestor catalog/search/graph coverage change in the manifest. Current approval/hash selection verification passes. Task, source ancestry, cutoff, evidence, guidance 12 and all other manifest fields are equal. The report below records the comparison. No teacher has started on it.

The existing prepared-forward retry guard requires byte-identical manifests (`orchestration/run_ahead.py`, forward branch). It therefore cannot compare this packet against 000277-001 as written. Please explicitly authorize the following narrow mechanics, or specify another route: after 278 finishes, bind your recovery decision with `recover --retry-position 277`, then use the existing prepared-forward route for `.teacher/runs/commit-000277-002`, with `packet` and `original_packet` both set to the new 000277-002. This makes the tool's equality guard an identity check; the separate old/new comparison report is the substantive preservation check. This is disclosed rather than silently bypassing the guard. Your decision path/hash will be bound in the prepared spec and recovery log.

The teacher receives only the new packet: fresh unassisted Sol/medium, guidance 12, standing validation repair available, no previous attempt, verdict, coverage request, tracking or ledger material. Current approved-selection and orchestration hashes remain recorded by the prepared route. 001 remains rejected history. Retry completes and stops for review before further advancement. No code changes, commit or push; latest accepted host-enabled suite remains 332 tests. This request seeks mechanics authorization, not annotation approval.

## SHA256

- reviews/verdicts/commit-000277-001.md: `d3a7c416559482297c3d9462be8179845b3dfd5d8052a887e5fa43f2e4712f61`
- reports/commit-000277-retry-packet-002.json: `6245360e485dd13ecb4e517faf806ed1c0de06583f5b64cefef1d76ef90f8faf`
- .teacher/retrieval/000277-001/manifest.json: `804c2d8f5547c0747932831fdd65e96bd08a2b86fd4351abba51d4504bed735d`
- .teacher/retrieval/000277-002/manifest.json: `91d32b7c104349a4afe7176190b0b1f35eae4b5df90f6147dd2e72a6373dacd6`
- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
