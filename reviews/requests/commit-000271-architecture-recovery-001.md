# Architecture recovery request: commit 271

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

No teacher session or packet was created. No annotation approval is requested. The queue remains stopped at 271, active_session null; 270 approval is recorded. Please accept the reference discovery and proposed manual queue recovery before authoring.

Upstream `2d1ce8910339ce3f10b3c46ee0b92cff23df71da`: **Add Dots1ForCausalLM architecture**. Cutoff `2025-06-14T15:32:35+02:00`. The trigger derives `Dots1ForCausalLM` from `exllamav3/models/dots1.py`; no unresolved architecture files.

Discovery enumerated all currently public repositories of both the original publisher `rednote-hilab` (one repository) and official successor `dots-studio` (17). The original instruct API redirects to the successor; card metadata and the cutoff-eligible issue 51 link corroborate that relationship. The original base name is now a recreated repository with only post-cutoff history; it is not a pinned non-match. Fifteen other successor repositories have no eligible revision. Both matching configs were read. Deleted/private repositories cannot be enumerated. Full administrative discovery and redirect probes are bound below; they are not teacher input.

Recovered official HF checkpoints:

- `dots-studio/dots.llm1.base` at `37802f86127ccf904b5d7bf413fc029daf13b4a3` (2025-06-10).
- `dots-studio/dots.llm1.inst` at `9fd724b876dd2f42b4447f65c4070e9cb55c4c53` (2025-06-11).

The accepted builder selected the latest eligible revision for each, fetched four metadata files and 67 tensor headers per checkpoint (142 objects total), and `load_bundle` passed again. Bundle size 29,292,157 bytes. Header-only HTTP ranges; no weight payload. No mirror, curator attestation, unresolved bundle or new evidence status. Existing official-HF header bounds apply unchanged.

Proposed mechanics after acceptance: bind your recovery verdict through `orchestration.run_ahead recover --retry-position 271`; recover the GitHub inputs, enforce the salience-v3-paths truncation stop, index the parent and prepare `.teacher/retrieval/000271-001` using the current approved selection. Then use the existing `prepared` forward route for `.teacher/runs/commit-000271-001`, with explicit authorization bound by path/hash. The ordinary cycle always stops at this architecture trigger, even with recovered evidence. No teacher or validator changes are proposed.

Important mechanics disclosure: there is no original packet to preserve. I propose setting the forward spec's `original_packet` to this same newly prepared first packet, so its existing byte-equality guard is an identity check, not a comparison against an earlier packet. Please explicitly authorize this first-packet use or specify another recovery path. Nothing has been cleared or launched pending your answer. The run will record its actual approved selection/orchestration hashes and sparse/running-ahead status; the failed reservation ran ahead of 270, but the eventual packet can now include approved 270. Catalog/path-only counts are not yet available because GitHub input recovery has not run.

No implementation change; no new suite run for this recovery request. Latest accepted host-enabled suite: 332 tests. Canonical/training remain false. No commit or push.

270 ledger work remains owed with the eventual commit review request: three new routing identities, accumulator/fused-shared fix revisions at 270, and observations on the two carried identities. Reviewer future-fix knowledge remains administrative only.

## SHA256

- `reports/run-ahead-detached-000271-0d176c3806da4fd8bfc63dd3a7bc0063.json`: `285b7bf87c3f48f24e9d4131340d730033b7847337896925590a0745d744d17d`
- `reports/run-ahead-detached-000271-0d176c3806da4fd8bfc63dd3a7bc0063.log`: `40493f28fa3cf4f4154e555fce30ff89f908c866fba0b24eeb13f13d9d16de5d`
- `.teacher/admin/run-ahead/bf147d9d26c54f0cbbcc128604d8aa47.log`: `3656127391859302de253af0349ee51f74a9c97309d4ddf033fe72f5c6afcc25`
- `reports/commit-000271-reference-discovery-001.json`: `4dfde93b6eaffbe0d9097aaac3878dd0d43c9a395312662f863b5fac8e1b2f5e`
- `reports/commit-000271-reference-discovery-002.json`: `248d280c248bdd185d6511a1c21fdabe6c810c6f666fb4372d29cd2fabf0884e`
- `reports/commit-000271-reference-discovery-003.json`: `9738f44369b6773295bbe391255b89e19e883fd6b075d3abc99782c2cb83702d`
- `reports/commit-000271-reference-probes-001.json`: `5566f96d6c09f4f8b134661e4b32fabd42ba20c732a76f7203bad7afe5a8a867`
- `reports/commit-000271-reference-selection-002.json`: `a3c66abbe0161ad435957a47432727523b5ee1b3ffad24b51a18a06b38c9b3f5`
- `data/evidence/github/000271-references.json`: `46fa3493b3d5b63b1cae89648cb6f68787b53b0e40e1c18bdea5609505535f00`
- `teacher/architecture_evidence.py`: `2abf7fa45b3023bdef5c372ce7e1ee0553e8a315bf50e1aa579ebb5708eda2d6`
- `teacher/reference_discovery.py`: `a678bd7d3fa12201139c976e247d23a408c825583b06d6e6845c65fa9f30fa8c`
- `teacher/cycle.py`: `5c3768624cb16f134a5428a34687bea7eb70bc2626f909065d3676626a246e9e`
- `orchestration/run_ahead.py`: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
- `reviews/verdicts/commit-000270-001.md`: `46dadf482ef4d887d4fd49bdf9db35135f36a02b17b162d507df68c1200caf59`
- `reports/commit-000271-architecture-recovery-001.json`: `879081307b7663507f55aade7ec31e9a3b3561e9bee32470cdebc2060f6f760d`
