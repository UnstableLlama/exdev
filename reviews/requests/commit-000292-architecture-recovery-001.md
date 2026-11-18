# Architecture recovery request: commit 292

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

No teacher session or packet was created. No annotation approval is requested. The queue remains stopped at 292, active_session null; 291 approval is recorded. Please accept the reference discovery and proposed manual queue recovery before authoring.

Upstream `47d83f567ccc93633d70354f93f153dad6266812`: **Add Ernie 4.5 model (text only)** (title copied from git). Cutoff `2025-07-07T04:18:07+02:00`. The trigger derives `Ernie4_5_ForCausalLM` and `Ernie4_5_MoeForCausalLM` from `exllamav3/models/ernie4_5.py` and `exllamav3/models/ernie4_5_moe.py`; no unresolved architecture files or renames.

Discovery enumerated all 39 currently public repositories of the official HF publisher `baidu`, separately for each architecture, without a model-name filter. Each pass inspected 23 eligible pinned configs; 16 repositories have no eligible revision. Four dense and eleven MoE checkpoints match; eight vision-language configs do not match these architecture declarations. Unavailable lists are empty. The cutoff-eligible official README corroborates the Baidu HF publisher and PaddlePaddle/ERNIE source repository. A supplementary enumeration of the HF `PaddlePaddle` organization found no Ernie-named repositories; that is a publisher probe, not a claim that every config there was inspected. Deleted/private repositories cannot be enumerated. Administrative discovery/probe files stay out of teacher input.

Recovered official HF checkpoints (all revisions dated 2025-07-04; exact times in the report):

| Repository | Pin | Metadata files | Tensor headers |
| --- | --- | ---: | ---: |
| `baidu/ERNIE-4.5-0.3B-Base-PT` | `5a782fbfd6e0b7192323af875fbdaf0df73c2048` | 5 | 1 |
| `baidu/ERNIE-4.5-0.3B-Base-Paddle` | `e9e3f7e13c78cb2ccd3d5a3daea4588105c3130a` | 5 | 1 |
| `baidu/ERNIE-4.5-0.3B-PT` | `50f620af62e77797fc297d1512628e861537e1de` | 5 | 1 |
| `baidu/ERNIE-4.5-0.3B-Paddle` | `0fed0df1d2ae0c2fc75009b877bc2fcec44cc618` | 5 | 1 |
| `baidu/ERNIE-4.5-21B-A3B-Base-PT` | `c85eddf33fb5d11fbdf9c533fd7e17e378a6e646` | 5 | 11 |
| `baidu/ERNIE-4.5-21B-A3B-Base-Paddle` | `0a2f190323c56ad7022ce4f1731d2f7d62eec22f` | 4 | 9 |
| `baidu/ERNIE-4.5-21B-A3B-PT` | `3b57ea628d6a8b6fa100c9d204358982031d868c` | 5 | 11 |
| `baidu/ERNIE-4.5-21B-A3B-Paddle` | `09cbbd872d7fbb351a2055681e3863a57299328b` | 4 | 10 |
| `baidu/ERNIE-4.5-300B-A47B-2Bits-Paddle` | `509d573bf9a89848d005a40e68fe6b98dbbf63d5` | 5 | 24 |
| `baidu/ERNIE-4.5-300B-A47B-Base-PT` | `99adb973b44536504e784ba016bad0dfcb4fb3dc` | 5 | 122 |
| `baidu/ERNIE-4.5-300B-A47B-Base-Paddle` | `08d74b417f497ff2db75fd813445535c5304598b` | 5 | 122 |
| `baidu/ERNIE-4.5-300B-A47B-FP8-Paddle` | `b9e3a0cd5964c8afa45fb8ccb98dbff68ad3a0ef` | 5 | 61 |
| `baidu/ERNIE-4.5-300B-A47B-PT` | `a952c9a500ffaff4e0264accc13fadd7d1460b06` | 5 | 124 |
| `baidu/ERNIE-4.5-300B-A47B-Paddle` | `77b3a7f3c44d9ee9bd7f5edfed4900b3368586c5` | 5 | 124 |
| `baidu/ERNIE-4.5-300B-A47B-W4A8C8-TP4-Paddle` | `4c2e1ee47a23a47693f5f50ddfac8a45e9fc09b6` | 5 | 36 |

The accepted builder produced 73 metadata files and 658 tensor headers (731 objects), 27,090,550 bytes. All 15 selections are complete, with no failed or missing fetches. `load_bundle` passed again before this request. Header-only HTTP ranges, no weight payload; unchanged 16 MiB official-HF header bound. No mirror, curator attestation, unresolved bundle or new evidence status. PT, Paddle and quantized representations are all retained. An initial tree fetch failed with an SSL EOF; the subsequent administrative builder invocation succeeded. The first publisher-probe file also preserves a README 404 caused by using another repository's pin; the second records the successful README fetch at the correct repository pin. Neither failure is represented as a pinned non-match.

Proposed mechanics after acceptance: bind your recovery verdict through `orchestration.run_ahead recover --retry-position 292`; recover the GitHub inputs, enforce the salience-v3-paths truncation stop, index the parent and prepare `.teacher/retrieval/000292-001` using the current approved selection. Then use the existing `prepared` forward route for `.teacher/runs/commit-000292-001`, with explicit authorization bound by path/hash. Teacher: gpt-6.1-sol / medium, guidance 12. The ordinary cycle stops at this architecture trigger even with recovered evidence. No teacher or validator changes are proposed.

There is no original packet to preserve. Please explicitly authorize setting the forward spec's `original_packet` to this same newly prepared first packet: the byte-equality guard would be an identity check, not comparison against an earlier packet. This is the disclosed 271 first-packet mechanism, requiring authorization for 292. Nothing has been cleared or launched pending your answer. The eventual run will bind actual approved selection/orchestration hashes and report sparse/running-ahead status. The failed reservation ran ahead of 291; the eventual packet can now include approved 291. Catalog/path-only counts are unavailable until GitHub recovery runs.

291's canonical-use follow-ups remain administrative and owed with the eventual commit review request: formalize the special-token decoding consequence with precise base/extended-vocabulary reach, and establish the backend keyword default using cutoff-eligible library evidence. No reviewer material will reach the teacher.

No implementation change or new suite run for this recovery request; latest accepted host-enabled suite: 332 tests. Canonical/training remain false. No commit or push.

## SHA256

- `reports/run-ahead-detached-000292-df49a6a454a741c2b1f7cdea5c869595.json`: `61fae49c6023600118db379e4353eb7d10fbf282e5c0e0547ffc2334a77d3929`
- `reports/run-ahead-detached-000292-df49a6a454a741c2b1f7cdea5c869595.log`: `91303df783f63b198b3dfb418b294cd09a9376528afa2907673a60fd35d11fa6`
- `.teacher/admin/run-ahead/5fba6151493842f58aaa03939ac4b6be.log`: `3656127391859302de253af0349ee51f74a9c97309d4ddf033fe72f5c6afcc25`
- `reports/commit-000292-reference-discovery-001.json`: `f991ad61e625eddbcdc18edc39aadf46d3ea006e086799126b371fb405b639f6`
- `reports/commit-000292-reference-discovery-002.json`: `af45adde166c806dc58650360edff08ab0932e7af6eb072ef6f7fdc29aba5ad0`
- `reports/commit-000292-reference-selection-001.json`: `300f4b61eab3917592df23e527a994c7a269939e5df638f9192237118ccde44e`
- `reports/commit-000292-reference-selection-002.json`: `8687515842346e13236db60f6322f68df4219a8298ffb970c7ca7df5d3c263b9`
- `reports/commit-000292-reference-selection-003.json`: `8ed2a7384bd0c0930523d20660088131937a716de4c3dd56b08ee30e40e7012e`
- `reports/commit-000292-reference-publisher-probes-001.json`: `7f3a504d9a871378b9a59e68f62493ca93b27182f6517d9c9522b3bc1ff0b053`
- `reports/commit-000292-reference-publisher-probes-002.json`: `467337bb56b7620d975a999d3af56703af1bf5cd657253a16abb6398faa74535`
- `data/evidence/github/000292-references.json`: `38fd36b3611c07bb7885d4c34f72201720fd1edfd5e1a267ee88756d8d31e6aa`
- `teacher/architecture_evidence.py`: `2abf7fa45b3023bdef5c372ce7e1ee0553e8a315bf50e1aa579ebb5708eda2d6`
- `teacher/reference_discovery.py`: `a678bd7d3fa12201139c976e247d23a408c825583b06d6e6845c65fa9f30fa8c`
- `teacher/cycle.py`: `5c3768624cb16f134a5428a34687bea7eb70bc2626f909065d3676626a246e9e`
- `orchestration/run_ahead.py`: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
- `reviews/verdicts/commit-000291-001.md`: `be6ced934d2d07f81393fe2c3379f44610045d29378d94d65d7c9a8da1a3739e`
- `reports/commit-000292-architecture-recovery-001.json`: `8520292293d45baf5483127669757c8cad8d8c4a88fcabceb8b4fc65afaeb611`
