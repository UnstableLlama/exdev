# Recovery mechanics: fresh 295/002 with complete ancestor selection

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Upstream: `69f8f9a07b95142878997f79e0053b1c1e08422f` — "Clamp output of activation functions to float16 range".

295/001 is recorded as rejected under your verdict. Its 19 request bindings were rechecked. The authored run remains unchanged as rejected history. 296 was already running when the rejection arrived; it may finish, and its request must assess whether missing 295 mattered. The queue stop prevents further launches.

The new packet `.teacher/retrieval/000295-002` contains all 294 strict ancestor entries, including approved 294. All 293 previous ancestor references are identical. Every original non-manifest packet file is preserved byte for byte, including the two superseded ancestor catalog/search blobs retained through the read-only shared store. Only ancestor entries, approved selection and the derived ancestor catalog/search/graph coverage differ in the manifest. Task, source ancestry, cutoff, evidence, guidance 12 and every other manifest field are equal. Current hash-bound approval selection verification passes. The comparison report below records these checks. No teacher has started on this packet.

As for 281, the existing prepared-forward retry guard requires byte-identical manifests and cannot directly compare this changed manifest against 000295-001. Please authorize the same narrow mechanics: after 296 finishes, bind your recovery decision with `recover --retry-position 295`, then use the prepared-forward route for `.teacher/runs/commit-000295-002`, with `packet` and `original_packet` both set to new 000295-002. This is an identity check in the tool; the separately bound old/new comparison provides the substantive preservation check. Your decision must name the stopped run `.teacher/runs/commit-000295-001` and will be bound by path/hash in the prepared spec and recovery log. No guard change or silent bypass is proposed.

The teacher receives only the new packet: fresh unassisted Sol/medium, guidance 12, standing validation repair available. No previous attempt, failure hint, pointer, verdict, coverage request, tracking or ledger material is supplied. The prepared route records current approved selection and orchestration hashes. The retry stops for review. No code changes, commit or push; latest accepted host-enabled suite remains 332 tests. This is a mechanics request, not annotation approval. Awaiting authorization before launching.

## SHA256

- reviews/verdicts/commit-000295-001.md: `f075c2fe460c7900af684f6e0ce482908ef3975ec03916f09e55faa7d56eafd3`
- reports/commit-000295-retry-packet-002.json: `d3c3ae76da410700d870addfc6f50a77998cc19b29e78ad204b469b30e05ba27`
- .teacher/retrieval/000295-001/manifest.json: `5fc14eba295bbb20b47a4422b4f7966ca2beb38589a9bb514ec43f57913d87e8`
- .teacher/retrieval/000295-002/manifest.json: `802c5dad845caea1d30e5f846ae5875f829335f7e42dd5ba500852be920205db`
- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
