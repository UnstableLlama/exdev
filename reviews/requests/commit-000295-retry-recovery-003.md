# Recovery mechanics: fresh assisted 295/003 on the same ancestor selection

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

295/002 is recorded as rejected under your verdict after all 22 original request bindings were rechecked. Its authored files remain unchanged as rejected history. 296 is approved but unrecorded until 295 is approved; no 297 is started.

The new packet `.teacher/retrieval/000295-003` is 000295-002 plus the exact coverage attachment. All 294 ancestor entries, ancestor selection and 4284 original non-manifest files are unchanged. The blobs remain read-only shared-store links. Hash-bound approved selection verification passes. Only top-level `coverage_request` and `walk_input_contract` differ; within the latter only `coverage_request_path` and `coverage_request_sha256` differ. Task, source ancestry, cutoff, evidence, guidance 12 and every other manifest field are equal. The bound comparison report records these checks. No teacher has started on this packet.

I inspected `reviews/verdicts/commit-000295-003.coverage.md`: it contains pointer-only coverage questions, with no conclusions, hindsight answers or length quotas. Its exact text and hash are attached. Nothing from attempts 001 or 002, their annotations, transcripts or verdicts will be supplied. This is a fresh reviewer-assisted attempt, not revision mode.

Please authorize the same narrow prepared-forward mechanics used for 295/002: bind your recovery decision with `recover --retry-position 295`, then launch `.teacher/runs/commit-000295-003` with `packet` and `original_packet` both set to new `.teacher/retrieval/000295-003`. The tool performs an identity comparison; the separately bound old/new comparison proves preservation and the sole coverage addition. Your decision must name the stopped run `.teacher/runs/commit-000295-002` and the new run `.teacher/runs/commit-000295-003`; its path and hash will be bound in the prepared spec and recovery log. No guard change is proposed.

Teacher: gpt-6.1-sol / medium, guidance 12, standing validation repair available. Only the new packet and its coverage attachment reach the teacher. The prepared route records current approved selection and orchestration hashes. The retry stops for review, requested scope ancestor retrieval only; canonical/training remain false. No new ledger item is owed from rejected 295. 296's ledger identity remains deferred until its approval is recorded. No implementation changes, commit or push; latest accepted host-enabled suite remains 332 tests. This is a mechanics request, not annotation approval. Awaiting authorization before launching.

## SHA256

- reviews/verdicts/commit-000295-002.md: `3a2174c89fcfc3eccc8e31706442209d834e505a757da13e25277849199b6820`
- reviews/verdicts/commit-000295-003.coverage.md: `429dea59ad067a7ad14da030300c9ac72f87edd384d6e7cbaab31f831098554c`
- reports/commit-000295-retry-packet-003.json: `da6cbc69d3dcd7044a8fbbaa8213127b8adf32e1e5ad9e853d037c564404dca9`
- .teacher/retrieval/000295-002/manifest.json: `802c5dad845caea1d30e5f846ae5875f829335f7e42dd5ba500852be920205db`
- .teacher/retrieval/000295-003/manifest.json: `b75e545c21f61d634e7a274fb61bf0c09d1c1e6773f29ca50d668d99b3796b01`
- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
