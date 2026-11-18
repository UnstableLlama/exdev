# Recovery mechanics: fresh 281/002 with complete ancestor selection

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

281/001 is recorded as rejected under your verdict. Its 14 request bindings were rechecked. The entry's CUDA action version is false; my request assessment also missed it. The authored run remains unchanged as rejected history. 282 was already running when the rejection arrived; it may finish, and its request must assess whether missing 281 mattered. The queue stop prevents further launches.

The new packet `.teacher/retrieval/000281-002` contains all 280 strict ancestor entries, including approved 280. All 279 previous ancestor references are identical. Every original non-manifest packet file is preserved byte for byte. Only ancestor entries, approved selection and the derived ancestor catalog/search/graph coverage differ in the manifest. Task, source ancestry, cutoff, evidence, guidance 12 and every other manifest field are equal. Current hash-bound approval selection verification passes. The comparison report below records these checks. No teacher has started on this packet.

As for 277, the existing prepared-forward retry guard requires byte-identical manifests and cannot directly compare this changed manifest against 000281-001. Please authorize the same narrow mechanics: after 282 finishes, bind your recovery decision with `recover --retry-position 281`, then use the prepared-forward route for `.teacher/runs/commit-000281-002`, with `packet` and `original_packet` both set to new 000281-002. This is an identity check in the tool; the separately bound old/new comparison provides the substantive preservation check. Your decision must name the stopped run `.teacher/runs/commit-000281-001` and will be bound by path/hash in the prepared spec and recovery log. No guard change or silent bypass is proposed.

The teacher receives only the new packet: fresh unassisted Sol/medium, guidance 12, standing validation repair available. No previous attempt, failure hint, pointer, verdict, coverage request, tracking or ledger material is supplied. The prepared route records current approved selection and orchestration hashes. The retry stops for review. No code changes, commit or push; latest accepted host-enabled suite remains 332 tests. This is a mechanics request, not annotation approval. Awaiting authorization before launching.

## SHA256

- reviews/verdicts/commit-000281-001.md: `96f23e2473c0a905fbd099b52cc812902e41e4eee4a36b4b0a93746891760aa0`
- reports/commit-000281-retry-packet-002.json: `540ff59562ce6542d5cb593c2c670404213e00ab507bf4fd68a2eb8dc8ded70a`
- .teacher/retrieval/000281-001/manifest.json: `5f46e74b720e54c231970a42fef08f281df9290ca72c867475da5f1013feff6e`
- .teacher/retrieval/000281-002/manifest.json: `99205770a2436a9dc86ac636ca00d12970c9a78a53d69247865059d7e17aeb2c`
- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
