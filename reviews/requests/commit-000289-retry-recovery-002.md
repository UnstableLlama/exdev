# Recovery mechanics: fresh assisted 289/002 with 288 visible

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

289/001 is recorded as rejected under your verdict; all 13 original request bindings were rechecked. The authored run remains unchanged as rejected history. 290 was already running when the rejection arrived and may finish; its request must assess whether missing 289 mattered. The queue stop prevents further launches.

The new packet `.teacher/retrieval/000289-002` contains all 288 approved strict ancestor entries, including 288. All 287 previous ancestor references are identical, and every original non-manifest packet file is preserved byte for byte. Current hash-bound approved selection verification passes. The comparison report below records these checks. No teacher has started on this packet.

The five changed ancestor-selection manifest keys are `ancestor_catalog_blob`, `ancestor_entries`, `ancestor_search_blob`, `ancestor_search_graph_commits` and `approved_ancestor_selection`. The other changed top-level keys are `coverage_request` and `walk_input_contract`; within the latter only `coverage_request_path` and `coverage_request_sha256` change. Task, source ancestry, cutoff, evidence, guidance 12 and every other manifest field are equal.

The exact coverage attachment is `reviews/verdicts/commit-000289-002.coverage.md`, bound below. I inspected it for conclusions, hindsight answers and length quotas: it contains pointer-only questions. Nothing from 289/001 or its verdict will be supplied to the teacher. This is a fresh reviewer-assisted attempt, not revision mode.

The existing prepared-forward retry guard requires byte-identical manifests and cannot directly compare the new manifest against 000289-001. Please authorize the same narrow mechanics used for 281: after 290 finishes, bind your recovery decision with `recover --retry-position 289`, then use the prepared-forward route for `.teacher/runs/commit-000289-002`, with `packet` and `original_packet` both set to new 000289-002. This is an identity check in the tool; the separately bound old/new comparison provides the substantive preservation check. Your decision must name the stopped run `.teacher/runs/commit-000289-001` and will be bound by path/hash in the prepared spec and recovery log. No guard change is proposed.

Teacher: gpt-6.1-sol / medium, guidance 12, standing validation repair available. The teacher receives the new packet and its coverage attachment only. The prepared route records current approved selection and orchestration hashes. The retry stops for review, requested scope ancestor retrieval only; canonical/training remain false. No 291 launch while stopped. No implementation changes, commit or push; latest accepted host-enabled suite remains 332 tests. This is a mechanics request, not annotation approval. Awaiting authorization before launching.

## SHA256

- reviews/verdicts/commit-000289-001.md: `bf98c7530080e4bdf7c471c4b0c7b3cff27432bb3f7cd653d04fb436f1fa82c7`
- reviews/verdicts/commit-000289-002.coverage.md: `3eb732296acfbcf2204045f4076a546c9121ab70be1b4d30e5d83402460c4dc2`
- reports/commit-000289-retry-packet-002.json: `84dc444b1a9896ccc6fe244e2aecf01855fd5c3cd47d958320d5bb5d129c7f7c`
- .teacher/retrieval/000289-001/manifest.json: `b6eb4005bc56d533007951eb4ff393c65cadca03ab4b1716b3339b4747328bb2`
- .teacher/retrieval/000289-002/manifest.json: `cc07fc002203a4c9a0306753003a362f6395715493b6c4e3d3718e2f31918c74`
- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
