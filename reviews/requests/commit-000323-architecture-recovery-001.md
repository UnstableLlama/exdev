# Architecture recovery for commit 323

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

323 stopped at the architecture gate before packet preparation or authoring. 322/002 is recorded. Please review the reference discovery and authorize the manual first-packet recovery.

Upstream `544ba423bf9c58c940dca6cb36a1aa93f6cda41a` — **Add Exaone4 architecture**. Cutoff `2025-07-15T21:15:47+02:00`. The trigger resolves `Exaone4ForCausalLM` from `exllamav3/models/exaone4.py`. No class remains unresolved.

The pinned official model card corroborates the LG AI Research publisher `LGAI-EXAONE`. Across all 50 currently visible repositories, 24 pinned root configs were inspected, 12 had no cutoff-eligible revision, and nine pinned trees confirmed root config absence, including both EXAONE 4 GGUF releases. The five HTTP 401 histories remain unverified: EXAONE-3.0-7.8B-Instruct, EXAONE-Path-1.5, EXAONE-Path-2.0-rev-EGFR, EXAONE-Path-2.5 and EXAONEPath. Deleted and private repositories are outside this enumeration. The model card and discovery reports remain administrative.

| Official repository | Cutoff pin | Metadata | Headers |
| --- | --- | ---: | ---: |
| EXAONE-4.0-1.2B | `e1bc152ddee871e02a4b91826a700898686c2012` | 5 | 1 |
| EXAONE-4.0-1.2B-AWQ | `b3b1143a3c64a7a7cd6500e8f291c501fb7e81a6` | 5 | 1 |
| EXAONE-4.0-1.2B-FP8 | `fdbcbdb6610963c5496a613ef1e162c37361554c` | 5 | 1 |
| EXAONE-4.0-1.2B-GPTQ-Int8 | `6c9e2500123b93b0ccf0554974b6a38d4586a9b2` | 5 | 1 |
| EXAONE-4.0-32B | `90704823f5ab8d367ef2168e0f71b67c10575922` | 5 | 14 |
| EXAONE-4.0-32B-AWQ | `b8c397142e312456bf21a1a2f6c23c71a57e4914` | 5 | 4 |
| EXAONE-4.0-32B-FP8 | `7357333452152feb9236a492e2d43b65a266125c` | 5 | 7 |
| EXAONE-4.0-32B-GPTQ | `6ce4e899c7d0374dac9ca217fa4873bd04172cd7` | 5 | 5 |

The bundle passes `load_bundle` with 74 objects and 64,895,389 content bytes. All eight pins precede cutoff. All 34 safetensors headers came from bounded HTTP ranges. The largest normalized header is 115,547 bytes. No fetch failures within the recovered selections, weight payloads, mirrors or curator attestations.

Proposed after acceptance: use `orchestration.run_ahead recover --retry-position 323` bound to the recovery verdict, recover cutoff-pinned GitHub evidence, enforce the salience-v3-paths cap, index the parent, and build `.teacher/retrieval/000323-001` with approved ancestors including 322/002. Preflight the headers and run one unassisted contract 8 / guidance 12 / gpt-6.2-sol medium attempt via `orchestration.run_ahead.prepared`. Please authorize `original_packet` equal to that new packet since 323 has no earlier packet. A preparation or preflight failure returns to review. No implementation change or annotation approval requested.

322 ledger for review: four draft observations and one fix revision, all schema and evidence validated. The ledger distinguishes the KV sampler reader's introduction from the normless compatibility gap at 322, traces the prefill flag and shortcut to the initial commit, and records 322's sequential norm fallback under the existing missing-norm identity. Carry these bindings into the 323 annotation request if this handoff covers recovery only.

## Artifact bindings

- reports/run-ahead-detached-000323-fb7bf231057148409750c2701c24f565.json: `b5bae5f75f9ebe8ee045831919d3b829649e52d92fd1be13b670dba939610f24`
- reports/run-ahead-detached-000323-fb7bf231057148409750c2701c24f565.log: `ed4f6d18472fc70ba0a6320d3b3b04786ad12a68ed007475efef3f3321a46167`
- .teacher/admin/run-ahead/f781cc9c98464e3681bc57635ec8f653.json: `55a3f0aa17732463ff35701deab8dcd504f7d712736ef8b289d54bdf5217359c`
- .teacher/admin/run-ahead/f781cc9c98464e3681bc57635ec8f653.log: `3656127391859302de253af0349ee51f74a9c97309d4ddf033fe72f5c6afcc25`
- reports/commit-000323-reference-discovery-001.json: `6ab8450bc0faaef53125bc4a6f577d4b0113259f3b9e68bd4c2d94afac2326df`
- reports/commit-000323-discovery-proofs-001.json: `e8c3c81eb6c75d21d224afb86eb753a23c9ebfc025b203c91dfcb0e23e53bfa3`
- reports/commit-000323-reference-selection-001.json: `9907d6982567213c7a38c602987be16c91a18170d80ca0bd684c2fb9cb99fa5b`
- reports/commit-000323-official-model-card-001.md: `4f073d7ca4cc38bc2969b64906aa609a598130327948fee66a201ee6067be523`
- data/evidence/github/000323-references.json: `0dfced0c56c532870148a537857e2f49715b10e0c0afc8acc9b3c84097a27351`
- teacher/reference_discovery.py: `a678bd7d3fa12201139c976e247d23a408c825583b06d6e6845c65fa9f30fa8c`
- teacher/architecture_evidence.py: `2abf7fa45b3023bdef5c372ce7e1ee0553e8a315bf50e1aa579ebb5708eda2d6`
- orchestration/run_ahead.py: `f7c5f2d1d6f7eab53785a4f74e531458981caa9b208065dd910be29b78d6aca2`
- reviews/verdicts/teacher-model-implementation-003.md: `673ec2df9f139409fe4adda3484e13eede5ed282171e78f21d5628b32756f4de`
- reviews/verdicts/commit-000322-002.md: `d26bca2e76bf7960b287f30212cb5a57e7450d0cf4c85b3aa0c1b66d952bf93e`
- reports/commit-000322-ledger-001.json: `b9865bc778d077102bb649e110b3668b26b2f9d87760fd49c576225d677811d2`
- reports/defect-ledger/exllamav3-kv-sampler-requires-attention-norm--r001.json: `f41dd64ab2ef7b52b169838ad0ff98833c47f1a697651f8935543b307720652b`
- reports/defect-ledger/exllamav3-optional-components-forward--r002.json: `0f717ce937b112902ff32166b7954c2a1b1a2f913601e781a4eba88074c1b4c7`
- reports/defect-ledger/exllamav3-ungated-mlp-allocation-interface--r002.json: `dc70ced08b1c68146b9191cd298c94bbedc0566acd4225673cd5bd5c06c31c4c`
- reports/defect-ledger/exllamav3-prefill-flag-leaks-into-forward--r001.json: `da7f19eaab75218dcadc1a039fab9381238d758355fe4a4404eee3794ef95090`
- reports/defect-ledger/exllamav3-transformer-missing-norm-input--r002.json: `22f1c44456332747c7af7a229bfca1fdca49e27e9dc838fae2822ec1d117cf9a`
