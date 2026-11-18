# Architecture recovery: commit 302

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

302 stopped before any packet or teacher run.301 approval is recorded; the queue remains stopped, active_session null. Please accept the reference discovery and explicitly authorize the manual first-packet queue recovery below. No annotation approval requested.

Upstream `d42d6238d88151eb837bdf709836d8726759fbd7`: **Add SmolLM3 architecture** (git title). Cutoff `2025-07-09T03:25:28+02:00`. Trigger: `SmolLM3ForCausalLM`, derived from `exllamav3/models/smollm3.py`; no unresolved class files or renames.

Enumerated all84 currently visible HuggingFaceTB repositories, without a name filter:65 pinned root configs inspected,5 without an eligible revision,14 config404s resolved by pinned recursive trees proving root config absence. Three configs match. The cutoff-pinned official model card corroborates HuggingFaceTB; no other original official publisher identified. Deleted/private repositories remain unenumerable; absent root configs do not establish an architecture non-match. Discovery reports/model card stay administrative, outside teacher input.

Recovered all three matching repositories:

| HuggingFaceTB repository | Cutoff pin | Metadata | Headers |
| --- | --- | ---: | ---: |
| SmolLM3-3B | b49c77130b3407155d9b83b404d9b28b5d1845ae | 5 | 2 |
| SmolLM3-3B-Base | 01580eff9713fc66f8a70cb0c00d793f283efabb | 5 | 2 |
| SmolLM3-3B-ONNX | e706b13ab827d7f63a4710642cb05a57cb4df202 | 5 | 0 |

All pins are July8 before cutoff. Bundle19 objects, 46236168 content bytes; load_bundle passes. No failed fetches. ONNX has no published safetensors at its pinned tree: retained as complete_with_absences, not represented as tensor-covered. No ONNX weights downloaded. Four safetensors headers recovered by HTTP ranges only, unchanged16MiB bound; no mirror, curator attestation or unresolved bundle.

Proposed after acceptance: `orchestration.run_ahead recover --retry-position 302` bound to your verdict; recover GitHub inputs and enforce salience-v3-paths cap, index parent, prepare `.teacher/retrieval/000302-001` with current approved selection including301, preflight all four headers, then one unassisted Sol/medium guidance12 attempt at `.teacher/runs/commit-000302-001` via `prepared`. Explicitly authorize `original_packet` equal to that same new packet: no earlier302 packet exists, so the equality guard is an identity check (the accepted271/292 mechanism). Fetch/preparation/preflight failure stops for review. No stop cleared or teacher launched. Final request will report actual catalog counts, sparse/running-ahead status and teacher header reads; currently unavailable before GitHub/packet preparation.

No implementation changes;45 teacher/4 orchestration live hashes match accepted repair004 application. Latest accepted tests20 focused/337 full. Canonical/training false; no commit/push.

Artifact bindings:
- reports/run-ahead-detached-000302-5a94a6dfe7f1429892bfa79ff1db00f0.json: `ee49c822805785d58c0e73327dc4223b548da4bc5133519a885f564fff370b5d`
- reports/run-ahead-detached-000302-5a94a6dfe7f1429892bfa79ff1db00f0.log: `6607a9cc56806901e061d1877288043c7dc663864be53df13715d4343c2370fb`
- .teacher/admin/run-ahead/98915444a53b4bb9a4ee705b03860e41.log: `3656127391859302de253af0349ee51f74a9c97309d4ddf033fe72f5c6afcc25`
- reports/commit-000302-reference-discovery-001.json: `22c381780b3e1925b841da9012441243543b3442438dd0492c75f2de54d88377`
- reports/commit-000302-reference-discovery-002.json: `1ad5a63a8c8e9d152adf384545fe9452dff16ce1cf638c4f072ffe3396840591`
- reports/commit-000302-discovery-proofs-001.json: `4d89da2f863c5516810c51add6aace30ae5f392dce578ae4588dbb8de7e74616`
- reports/commit-000302-reference-selection-001.json: `1f05c287d788a5038613a4af12d3909311b5ea7defd28ac0abd0bd9c706faacd`
- reports/commit-000302-official-model-card-001.md: `61892da81f8f6a700847e43da9303d5fb457287a285c2389a57139031634da48`
- data/evidence/github/000302-references.json: `638e9ba7857b0d1dfc76754bddfb84282f2749d5c8b242dd1d9d10e5ef0e0214`
- reports/commit-000302-architecture-recovery-001.json: `2940a7d2d9f990f9c1c69933fb8b3a5377981653eb76bb86d2cfd2ca6958d3c6`
- reports/validation-repair-implementation-004-application.json: `764892c8af2835261e8a2d6d4c6e59fcb2f9ad993ee267d38301767829fedda2`
- reviews/verdicts/commit-000301-001.md: `b80716b9cbc494e24a30b2f447c452eb9157486f51327ead829200adf9875d6c`
- teacher/architecture_evidence.py: `2abf7fa45b3023bdef5c372ce7e1ee0553e8a315bf50e1aa579ebb5708eda2d6`
- teacher/reference_discovery.py: `a678bd7d3fa12201139c976e247d23a408c825583b06d6e6845c65fa9f30fa8c`
- teacher/cycle.py: `9e6f7eb484cc727cebfc40b1e1c6d926ae29423b90e0fe31abfeadac4e9344de`
- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
