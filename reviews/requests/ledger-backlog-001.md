# Ledger backlog 001 — review request

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Administrative ledger review only; no canonical/training approval requested.

208 is recorded APPROVED for ancestor retrieval only via `--approve`. No 209 packet/run exists; advancement pause stays until this batch is accepted.

Binding decision: `reviews/verdicts/ledger-backlog.decision.md`, SHA-256 `4073325bf693ff76e2ce0c96c90973efe20238bf3f6047e8077390bfb4764235`. 208 verdict SHA-256: `6fdb488a94ea99274ce9155e04fed2f73075c62a206b74dc36e54c06bf4df015`.

## Batch and validation

100 appended records: 63 new identities and 37 revisions. The 199 obligation rows below include three explicit holds; 72 existing-identity rows retain earlier discharges and provenance. Repeated affected/fix observations share identities. Only history through approved 208 is used. Partial fixes remain partial, uncertain introductions remain unknown, source/stand-in checks do not imply GPU execution, and reviewer-only observations remain labelled in records and observations. No teacher receives this material.

All 114 preexisting records match HEAD bytes. All 214 records pass evidence hash/path and revision-chain checks. Schema validation passes 93/100 new records and 180/214 total; seven new and 27 existing reviewer-origin records fail `Unknown origin`. Labels are preserved; no validator changes or eligibility workaround were made. Supplemental field, status, classification and dependency checks pass for those 34 records. This disclosed limitation is not full schema validation success. No code changed, so no full suite was run.

No authored run or packet changed by this batch. The manifest also hashes the recorded 208 approval and journal pause. Reviewer-owned `reviews/fable/STATE.md` is outside this author batch. Canonical prose conditions, GPU/model checks, discussion-history caching and guidance cost comparisons are not discharged by ledger filing.

| Artifact | SHA-256 |
|---|---|
| `reports/ledger-backlog-001.files.json` | `a02811ebba306a299c30a5e44b8e48edc92d9fceb20c2927c2f96601556582b8` |
| `reports/ledger-backlog-001.json` | `e6f23b9edf631e0bdc9d403e9b1466d75cd81b4f710adae57d73a238c7bfddc5` |
| `reports/ledger-backlog-001.validation.txt` | `5b27d59f8350260985257634d04c644c203301c7c29184e67c60d1e2f59529f1` |

The manifest gives exact hashes for every batch record, evidence snapshot, report, validation output and changed author tracking file. Self-hashes are excluded; the manifest hash is above. Evidence snapshots bind verdict text and approved drafts; original run/tool citations remain contextual references, not newly executed tests.

## Obligation-to-record table

Record paths are under `reports/defect-ledger/`; verdict names under `reviews/verdicts/`. Rows are filings for review, not declarations of acceptance.

| Owed item | Owing verdict | Record / revision or hold |
|---|---|---|
| 39: kv-head-mapping | commit-000039-005.md | `exllamav3-decilm-kv-head-count--r003.json` (r003) |
| 39: empty-block-conversion | commit-000039-005.md | `exllamav3-empty-block-conversion--r001.json` (r001) |
| 40: markdown-multiline-input | commit-000040-001.md | `exllamav3-markdown-multiline-input--r001.json` (r001) |
| 44: remaining-51b-linear-attention-rejection | commit-000044-003.md | `exllamav3-decilm-linear-attention-limitation--r001.json` (r001) |
| 44: carried-over-empty-block-bitrate | commit-000044-003.md | `exllamav3-empty-block-conversion--r001.json` (r001) |
| 47: cpu-bias-after-conversion | commit-000047-001.md | `exllamav3-cpu-bias-after-conversion--r001.json` (r001) |
| 52: split-source-group | commit-000052-001.md | `exllamav3-split-source-group--r001.json` (r001) |
| 52: inherited-native-read-wait | commit-000052-001.md | `exllamav3-native-read-wait--r001.json` (r001) |
| 53: default-cpu-staging | commit-000053-001.md | `exllamav3-default-cpu-staging--r001.json` (r001) |
| 53: padding-before-slicing | commit-000053-001.md | `exllamav3-padding-before-slicing--r001.json` (r001) |
| 53: inherited-native-read-wait | commit-000053-001.md | `exllamav3-native-read-wait--r001.json` (r001) |
| 55: unaligned-tail-padding | commit-000055-002.md | `exllamav3-padding-before-slicing--r001.json` (r001) |
| 55: ungated-mlp-allocation-interface | commit-000055-002.md | `exllamav3-ungated-mlp-allocation-interface--r001.json` (r001) |
| 55: ungated-list-allocation-key | commit-000055-002.md | `exllamav3-ungated-list-allocation-key--r001.json` (r001) |
| 55: inherited-split-source-group | commit-000055-002.md | `exllamav3-split-source-group--r001.json` (r001) |
| 55: inherited-native-read-wait | commit-000055-002.md | `exllamav3-native-read-wait--r001.json` (r001) |
| 58: reasoning-boundary-answer-loss | commit-000058-001.md | `exllamav3-reasoning-boundary-answer-loss--r001.json` (r001) |
| 59: reasoning-boundary-answer-loss | commit-000059-001.md | `exllamav3-reasoning-boundary-answer-loss--r001.json` (r001) |
| 60: inherited-reasoning-boundary-answer-loss | commit-000060-001.md | `exllamav3-reasoning-boundary-answer-loss--r001.json` (r001) |
| 62: unchecked-output-capacity | commit-000062-001.md | `exllamav3-unchecked-output-capacity--r001.json` (r001) |
| 63: unreachable-final-synchronization | commit-000063-001.md | `exllamav3-unreachable-final-synchronization--r001.json` (r001) |
| 63: inherited-premature-progress | commit-000063-001.md | `exllamav3-scale-progress-premature-completion--r002.json` (r002) |
| 65: partial-frequency-read | commit-000065-001.md | `exllamav3-partial-frequency-read--r001.json` (r001) |
| 65: torch-gptj-reference | commit-000065-001.md | `exllamav3-torch-gptj-reference--r001.json` (r001) |
| 66: required-scale-policy-test-caller | commit-000066-001.md | `exllamav3-required-scale-policy-test-caller--r001.json` (r001) |
| 66: inherited-premature-search-progress | commit-000066-001.md | `exllamav3-scale-progress-premature-completion--r002.json` (r002) |
| 71: fp32-mlp-intermediate-contract | commit-000071-002.md | `exllamav3-fp32-mlp-intermediate-contract--r001.json` (r001) |
| 72: partial-rope-frequency-load | commit-000072-002.md | `exllamav3-partial-frequency-read--r001.json` (r001) |
| 73: inherited-reasoning-boundary-answer-loss | commit-000073-001.md | `exllamav3-reasoning-boundary-answer-loss--r001.json` (r001) |
| 74: zero-block-scale | commit-000074-001.md | `exllamav3-zero-block-scale--r001.json` (r001) |
| 74: inherited-detach-diagnostic | commit-000074-001.md | `exllamav3-cache-detach-count-diagnostic--r003.json` (r003) |
| 76: single-device-progress | commit-000076-001.md | `exllamav3-single-device-progress--r001.json` (r001) |
| 77: inherited-detach-diagnostic | commit-000077-001.md | `exllamav3-cache-detach-count-diagnostic--r003.json` (r003) |
| 78: inherited-reasoning-boundary-answer-loss | commit-000078-001.md | `exllamav3-reasoning-boundary-answer-loss--r001.json` (r001) |
| 79: unchecked-pack-bitrate | commit-000079-001.md | `exllamav3-unchecked-pack-bitrate--r001.json` (r001) |
| 80: inherited-sorted-argmax | commit-000080-001.md | `exllamav3-sorted-argmax--r002.json` (r002) |
| 81: top-p-description-mismatch | commit-000081-001.md | `exllamav3-top-p-description-mismatch--r001.json` (r001) |
| 81: inherited-sorted-argmax | commit-000081-001.md | `exllamav3-sorted-argmax--r002.json` (r002) |
| 82: multinomial-sorted-token-mapping | commit-000082-001.md | `exllamav3-multinomial-sorted-token-mapping--r001.json` (r001) |
| 84: simultaneous-axis-padding | commit-000084-001.md | `exllamav3-simultaneous-axis-padding--r001.json` (r001) |
| 84: inherited-padding-before-slicing | commit-000084-001.md | `exllamav3-padding-before-slicing--r001.json` (r001) |
| 86: simultaneous-padding-restriction | commit-000086-001.md | `exllamav3-simultaneous-axis-padding--r001.json` (r001) |
| 86: padding-before-slicing | commit-000086-001.md | `exllamav3-padding-before-slicing--r001.json` (r001) |
| 88: retained-two-axis-padding | commit-000088-001.md | `exllamav3-simultaneous-axis-padding--r001.json` (r001) |
| 88: retained-padding-before-slicing | commit-000088-001.md | `exllamav3-padding-before-slicing--r001.json` (r001) |
| 89: unconditional-tk-import | commit-000089-001.md | `exllamav3-unconditional-tk-import--r001.json` (r001) |
| 90: missing-combo-sampler | commit-000090-001.md | `exllamav3-missing-combo-sampler--r003.json` (r003) |
| 91: combo-default-min-p | commit-000091-001.md | `exllamav3-min-p-zero-assertion--r001.json` (r001) |
| 92: chat-top-k-float | commit-000092-001.md | `exllamav3-chat-top-k-float--r001.json` (r001) |
| 92: chat-min-p-disable | commit-000092-001.md | `exllamav3-min-p-zero-assertion--r001.json` (r001) |
| 96: optional-components-forward | commit-000096-001.md | `exllamav3-optional-components-forward--r001.json` (r001) |
| 96: plain-mlp-allocation | commit-000096-001.md | `exllamav3-ungated-mlp-allocation-interface--r001.json` (r001) |
| 98: cohere-qk-normalization | commit-000098-001.md | `exllamav3-cohere-qk-normalization--r002.json` (r002) |
| 99: inherited-single-device-progress | commit-000099-001.md | `exllamav3-single-device-progress--r001.json` (r001) |
| 102: architecture-mismatch-diagnostic | commit-000102-001.md | `exllamav3-architecture-mismatch-diagnostic--r001.json` (r001) |
| 104: documentation-dump-scope | commit-000104-001.md | `exllamav3-documentation-dump-scope--r001.json` (r001) |
| 105: stream-argument-mismatch | commit-000105-001.md | `exllamav3-chat-stream-argument-mismatch--r003.json` (r003) |
| 108: asymmetric-norm-validation | commit-000108-001.md | `exllamav3-asymmetric-norm-validation--r001.json` (r001) |
| 111: nonzero-default-min-p | commit-000111-001.md | `exllamav3-min-p-zero-assertion--r001.json` (r001) |
| 119: deferred-bf16-odd-tail | commit-000119-001.md | `exllamav3-deferred-bf16-odd-tail--r002.json` (r002) |
| 120: metrics-wrapper-compatibility | commit-000120-001.md | `exllamav3-variant-collection-loader-api--r003.json` (r003) |
| 120: inherited-bf16-odd-tail | commit-000120-001.md | `exllamav3-deferred-bf16-odd-tail--r002.json` (r002) |
| 122: masked-full-penalty-endpoint | commit-000122-001.md | `exllamav3-repetition-penalty-masked-nan--r003.json` (r003) |
| 123: boolean-dimension-threshold | commit-000123-001.md | `exllamav3-boolean-dimension-threshold--r003.json` (r003) |
| 124: humaneval-top-k-float | commit-000124-001.md | `exllamav3-chat-top-k-float--r001.json` (r001) |
| 125: humaneval-top-k-float | commit-000125-001.md | `exllamav3-chat-top-k-float--r001.json` (r001) |
| 126: deferred-cuda-error-number | commit-000126-001.md | `exllamav3-deferred-read-errno-reporting--r002.json` (r002) |
| 127: ppl-vocabulary-bound | commit-000127-001.md | `exllamav3-ppl-axis-bound--r002.json` (r002) |
| 129: scalar-codebook-double-transform | commit-000129-001.md | `exllamav3-scalar-codebook-double-transform--r003.json` (r003) |
| 129: missing-gemv-header | commit-000129-001.md | `exllamav3-missing-gemv-kernel-header--r003.json` (r003) |
| 129: inherited-boolean-threshold | commit-000129-001.md | `exllamav3-boolean-dimension-threshold--r003.json` (r003) |
| 130: unicode-flush-bypasses-string-checks | commit-000130-001.md | `exllamav3-unicode-flush-string-bypass--r002.json` (r002) |
| 130: retained-checkpoint-token-attribute | commit-000130-001.md | `exllamav3-checkpoint-token-attribute--r002.json` (r002) |
| 130: retained-terminal-string-bypass | commit-000130-001.md | `exllamav3-terminal-string-bypass--r002.json` (r002) |
| 133: multi-gemm-leading-dimension-validation | commit-000133-001.md | `exllamav3-multi-gemm-leading-dimension-validation--r003.json` (r003) |
| 133: inherited-boolean-shape-threshold | commit-000133-001.md | `exllamav3-boolean-dimension-threshold--r003.json` (r003) |
| 135: zero-slice-division | commit-000135-001.md | `exllamav3-gemm-zero-grid-cap--r002.json` (r002) |
| 135: broadcast-scratch-capacity | commit-000135-001.md | `exllamav3-mgemm-broadcast-scratch-capacity--r002.json` (r002) |
| 137: empty-codeblock-feedback | commit-000137-001.md | `exllamav3-empty-codeblock-feedback--r003.json` (r003) |
| 139: all-expert-fused-shape | commit-000139-001.md | `exllamav3-all-expert-fused-shape--r003.json` (r003) |
| 140: inherited-deferred-bf16-tail | commit-000140-001.md | `exllamav3-deferred-bf16-odd-tail--r002.json` (r002) |
| 141: inherited-all-expert-fused-shape | commit-000141-001.md | `exllamav3-all-expert-fused-shape--r003.json` (r003) |
| 145: empty-utf32-return-annotation | commit-000145-001.md | `exllamav3-empty-utf32-return-annotation--r002.json` (r002) |
| 146: empty-utf32-annotation | commit-000146-001.md | `exllamav3-empty-utf32-return-annotation--r002.json` (r002) |
| 153: retained-all-expert-fused-shape | commit-000153-002.md | `exllamav3-all-expert-fused-shape--r003.json` (r003) |
| 153: retained-mgemm-leading-dimensions | commit-000153-002.md | `exllamav3-multi-gemm-leading-dimension-validation--r003.json` (r003) |
| 153: retained-boolean-selector | commit-000153-002.md | `exllamav3-boolean-dimension-threshold--r003.json` (r003) |
| 153: retained-zero-slice-division | commit-000153-002.md | `exllamav3-gemm-zero-grid-cap--r002.json` (r002) |
| 153: retained-broadcast-scratch-contract | commit-000153-002.md | `exllamav3-mgemm-broadcast-scratch-capacity--r002.json` (r002) |
| 153: retained-deferred-bf16-tail | commit-000153-002.md | `exllamav3-deferred-bf16-odd-tail--r002.json` (r002) |
| 153: retained-empty-clipboard-feedback | commit-000153-002.md | `exllamav3-empty-codeblock-feedback--r003.json` (r003) |
| 153: retained-empty-utf32-annotation | commit-000153-002.md | `exllamav3-empty-utf32-return-annotation--r002.json` (r002) |
| 154: inherited-ppl-axis-bound | commit-000154-001.md | `exllamav3-ppl-axis-bound--r002.json` (r002) |
| 155: inherited-all-expert-fused-shape | commit-000155-001.md | `exllamav3-all-expert-fused-shape--r003.json` (r003) |
| 163: qwen3-moe-component-migration | commit-000163-002.md | `exllamav3-qwen3-moe-component-migration--r003.json` (r003) |
| 165: no-reference-finalization | commit-000165-001.md | `exllamav3-compare-q-no-reference-finalization--r006.json` (r006) |
| 165: cache-clear-argument-mismatch | commit-000165-001.md | `exllamav3-compare-q-cache-clear-argument-mismatch--r005.json` (r005) |
| 167: nonpositive-codeblock-index | commit-000167-001.md | `exllamav3-nonpositive-codeblock-index--r002.json` (r002) |
| 169: unsupported-cache-default-argument | commit-000169-001.md | `exllamav3-unsupported-cache-default-argument--r003.json` (r003) |
| 171: inherited-no-reference-finalization | commit-000171-001.md | `exllamav3-compare-q-no-reference-finalization--r006.json` (r006) |
| 171: inherited-cache-invalidation-mismatch | commit-000171-001.md | `exllamav3-compare-q-cache-clear-argument-mismatch--r005.json` (r005) |
| 172: embedding-order | commit-000172-001.md | `exllamav3-llamacpp-embedding-order--r002.json` (r002) |
| 172: cached-accounting | commit-000172-001.md | `exllamav3-llamacpp-cached-accounting--r002.json` (r002) |
| 173: filtered-reference-dependency | commit-000173-001.md | `exllamav3-compare-q-filtered-reference-dependency--r003.json` (r003) |
| 173: inherited-no-reference-finalization | commit-000173-001.md | `exllamav3-compare-q-no-reference-finalization--r006.json` (r006) |
| 174: fp8-dtype-not-loadable | commit-000174-001.md | `exllamav3-fp8-dtype-not-loadable--r001.json` (r001) |
| 174: scaling-before-deferred-read | commit-000174-001.md | `exllamav3-scaling-before-deferred-read--r001.json` (r001) |
| 174: scale-orientation-contract | commit-000174-001.md | `exllamav3-scale-orientation-contract--r001.json` (r001) |
| 175: inherited-filtered-reference-dependency | commit-000175-001.md | `exllamav3-compare-q-filtered-reference-dependency--r003.json` (r003) |
| 176: inherited-first-pass-cost-buffer | commit-000176-001.md | `exllamav3-first-pass-cost-buffer--r002.json` (r002) |
| 177: inherited-sorted-argmax | commit-000177-001.md | `exllamav3-sorted-argmax--r002.json` (r002) |
| 178: optional-output-return | commit-000178-001.md | `exllamav3-optional-output-return--r001.json` (r001) |
| 179: inherited-all-expert-fused-shape | commit-000179-001.md | `exllamav3-all-expert-fused-shape--r003.json` (r003) |
| 181: remaining-unequal-kv | commit-000181-001.md | `exllamav3-remaining-unequal-kv--r001.json` (r001) |
| inherited-exact-budget-boundary | commit-000182-001.md | **HELD**: 181 qualification and 182 explicit hold: allocation budget already includes +1; no unqualified exact-match exclusion record. |
| 183: optional-k-conversion | commit-000183-001.md | `exllamav3-optional-k-conversion--r001.json` (r001) |
| 183: reference-test-discarded-results | commit-000183-001.md | `exllamav3-reference-test-discarded-results--r001.json` (r001) |
| 183: partial-reference-width | commit-000183-001.md | `exllamav3-partial-reference-width--r001.json` (r001) |
| 184: inherited-all-expert-buffer-count | commit-000184-001.md | `exllamav3-all-expert-fused-shape--r003.json` (r003) |
| 184: fused-output-dtype-override | commit-000184-001.md | `exllamav3-fused-output-dtype-override--r001.json` (r001) |
| 184: persistent-output-alias | commit-000184-001.md | `exllamav3-persistent-output-alias--r001.json` (r001) |
| 185: normalization-settings-overwritten | commit-000185-001.md | `exllamav3-normalization-settings-overwritten--r001.json` (r001) |
| 185: warp-sum-store-race | commit-000185-001.md | `exllamav3-warp-sum-store-race--r001.json` (r001) |
| 185: padded-thread-read-bounds | commit-000185-001.md | `exllamav3-padded-thread-read-bounds--r001.json` (r001) |
| 185: inherited-reference-input-limits | commit-000185-001.md | `exllamav3-optional-k-conversion--r001.json` (r001) |
| 185: inherited-reference-input-limits | commit-000185-001.md | `exllamav3-partial-reference-width--r001.json` (r001) |
| 185: inherited-all-expert-workspace-mismatch | commit-000185-001.md | `exllamav3-all-expert-fused-shape--r003.json` (r003) |
| 185: inherited-persistent-output-contract | commit-000185-001.md | `exllamav3-fused-output-dtype-override--r001.json` (r001) |
| 185: inherited-persistent-output-contract | commit-000185-001.md | `exllamav3-persistent-output-alias--r001.json` (r001) |
| 186: zero-multi-grid | commit-000186-001.md | `exllamav3-gemm-zero-grid-cap--r002.json` (r002) |
| 186: inherited-boolean-threshold | commit-000186-001.md | `exllamav3-boolean-dimension-threshold--r003.json` (r003) |
| 186: stale-selector-declaration | commit-000186-001.md | `exllamav3-stale-selector-declaration--r001.json` (r001) |
| 187: inherited-all-expert-buffer-mismatch | commit-000187-001.md | `exllamav3-all-expert-fused-shape--r003.json` (r003) |
| 190: inherited-dtype-dispatch | commit-000190-001.md | `exllamav3-inherited-dtype-dispatch--r001.json` (r001) |
| 190: inherited-test-argument-mismatch | commit-000190-001.md | `exllamav3-inherited-test-argument-mismatch--r001.json` (r001) |
| 191: prefill-counted-as-output | commit-000191-001.md | `exllamav3-prefill-counted-as-output--r001.json` (r001) |
| 191: empty-filtered-dataset | commit-000191-001.md | `exllamav3-empty-filtered-dataset--r001.json` (r001) |
| 192: disabled-options-unbound | commit-000192-001.md | `exllamav3-disabled-options-unbound--r001.json` (r001) |
| 192: reported-probabilities-not-final | commit-000192-001.md | `exllamav3-reported-probabilities-not-final--r001.json` (r001) |
| 193: inherited-probability-contract | commit-000193-001.md | `exllamav3-reported-probabilities-not-final--r001.json` (r001) |
| 194: inherited-warp-sum-store | commit-000194-001.md | `exllamav3-warp-sum-store-race--r001.json` (r001) |
| 194: inherited-padded-input-reads | commit-000194-001.md | `exllamav3-padded-thread-read-bounds--r001.json` (r001) |
| 195: unchecked-vector-partition | commit-000195-001.md | `exllamav3-unchecked-vector-partition--r001.json` (r001) |
| 195: unused-test-dtype | commit-000195-001.md | `exllamav3-unused-test-dtype--r001.json` (r001) |
| 196: inherited-normalization-reduction | commit-000196-002.md | `exllamav3-warp-sum-store-race--r001.json` (r001) |
| 196: inherited-padded-input-reads | commit-000196-002.md | `exllamav3-padded-thread-read-bounds--r001.json` (r001) |
| 197: draft-cache-not-relocated | commit-000197-001.md | `exllamav3-draft-cache-not-relocated--r001.json` (r001) |
| 197: inherited-vector-boundary | commit-000197-001.md | `exllamav3-unchecked-vector-partition--r001.json` (r001) |
| 197: inherited-unused-test-dtype | commit-000197-001.md | `exllamav3-unused-test-dtype--r001.json` (r001) |
| 198: histogram-zero-bins | commit-000198-001.md | `exllamav3-histogram-zero-bins--r001.json` (r001) |
| 200: tensor-truth-dispatch | commit-000200-001.md | `exllamav3-tensor-truth-dispatch--r001.json` (r001) |
| 200: layernorm-reference-shape | commit-000200-001.md | `exllamav3-layernorm-reference-shape--r001.json` (r001) |
| 200: inherited-native-normalization-and-bounds | commit-000200-001.md | `exllamav3-warp-sum-store-race--r001.json` (r001) |
| 200: inherited-native-normalization-and-bounds | commit-000200-001.md | `exllamav3-padded-thread-read-bounds--r001.json` (r001) |
| 203: inherited-perplexity-axis-bound | commit-000203-001.md | `exllamav3-ppl-axis-bound--r002.json` (r002) |
| 204: proxy-sentinel-test | commit-000204-001.md | `exllamav3-proxy-sentinel-test--r001.json` (r001) |
| 205: verbose-skipped-scale | commit-000205-001.md | `exllamav3-verbose-skipped-scale--r001.json` (r001) |
| 205: skipped-state-strides | commit-000205-001.md | `exllamav3-skipped-state-strides--r001.json` (r001) |
| 207: inherited-fused-rope-concerns | commit-000207-001.md | `exllamav3-warp-sum-store-race--r001.json` (r001) |
| 207: inherited-fused-rope-concerns | commit-000207-001.md | `exllamav3-padded-thread-read-bounds--r001.json` (r001) |
| 208: inherited-native-rope-concerns | commit-000208-001.md | `exllamav3-warp-sum-store-race--r001.json` (r001) |
| 208: inherited-native-rope-concerns | commit-000208-001.md | `exllamav3-padded-thread-read-bounds--r001.json` (r001) |
| empty-block-conversion fix / full | commit-000045-002.md | `exllamav3-empty-block-conversion--r001.json` (r001) |
| min-p-zero-assertion fix / full | commit-000113-002.md | `exllamav3-min-p-zero-assertion--r001.json` (r001) |
| top-p-zero-assertion fix / full | commit-000115-001.md | `exllamav3-top-p-zero-assertion--r002.json` (r002) |
| architecture-mismatch-diagnostic fix / full | commit-000117-001.md | `exllamav3-architecture-mismatch-diagnostic--r001.json` (r001) |
| unconditional-tk-import fix / full | commit-000118-001.md | `exllamav3-unconditional-tk-import--r001.json` (r001) |
| torch-gptj-reference fix / full | commit-000183-001.md | `exllamav3-torch-gptj-reference--r001.json` (r001) |
| reference-test-discarded-results fix / full | commit-000185-001.md | `exllamav3-reference-test-discarded-results--r001.json` (r001) |
| disabled-options-unbound fix / full | commit-000193-001.md | `exllamav3-disabled-options-unbound--r001.json` (r001) |
| normalization-settings-overwritten fix / full | commit-000196-002.md | `exllamav3-normalization-settings-overwritten--r001.json` (r001) |
| unchecked-output-capacity fix / full | commit-000198-001.md | `exllamav3-unchecked-output-capacity--r001.json` (r001) |
| cohere-qk-normalization fix / full | commit-000201-001.md | `exllamav3-cohere-qk-normalization--r002.json` (r002) |
| kernel-attribute-cache-device fix / full | commit-000202-001.md | `exllamav3-kernel-attribute-cache-device--r002.json` (r002) |
| tensor-truth-dispatch fix / full | commit-000207-001.md | `exllamav3-tensor-truth-dispatch--r001.json` (r001) |
| chat-top-k-float fix / HumanEval caller | commit-000147-001.md | `exllamav3-chat-top-k-float--r001.json` (r001) |
| gemm-zero-grid-cap fix / single path only | commit-000186-001.md | `exllamav3-gemm-zero-grid-cap--r002.json` (r002) |
| optional-output-return fix / enabled branches only | commit-000192-001.md | `exllamav3-optional-output-return--r001.json` (r001) |
| 29: Omitted resume arguments overwrite saved checkpoint interval, devices and ratios with parser defaults. | commit-000029-001.md | `exllamav3-resume-argument-resets--r001.json` (r001) |
| 69: Configured tokenizer truncation can leave requested calibration slices empty. | commit-000069-003.md | `exllamav3-tokenizer-truncation-calibration--r001.json` (r001) |
| 69: fix tokenizer-truncation-calibration (full) | commit-000069-003.md | `exllamav3-tokenizer-truncation-calibration--r001.json` (r001) |
| 113: The min_p=1.0 endpoint is rejected for one commit. | commit-000113-002.md | `exllamav3-min-p-one-endpoint--r001.json` (r001) |
| 114: 114 restores the inclusive upper bound; one-commit regression, not a standing behavior change. | commit-000114-001.md | `exllamav3-min-p-one-endpoint--r001.json` (r001) |
| 114: fix min-p-one-endpoint (full) | commit-000114-001.md | `exllamav3-min-p-one-endpoint--r001.json` (r001) |
| 121: Same-directory stloader.cpp and stloader.cu share an object stem. | commit-000121-001.md | `exllamav3-same-stem-object-conflict--r001.json` (r001) |
| 119: Pair introduced at 119; introduction established by reviewer in 121. | commit-000119-001.md | `exllamav3-same-stem-object-conflict--r001.json` (r001) |
| 120: Pair persists at 120; reviewer attribution in 121. | commit-000120-001.md | `exllamav3-same-stem-object-conflict--r001.json` (r001) |
| 121: fix same-stem-object-conflict (full) | commit-000121-001.md | `exllamav3-same-stem-object-conflict--r001.json` (r001) |
| 114: SS_TopP zero assertion persists at 114. | commit-000114-001.md | `exllamav3-top-p-zero-assertion--r002.json` (r002) |
| 120: 120 remains affected by the reviewer finding introduced at 119. | commit-000120-001.md | `exllamav3-sliced-fp16-padding-target--r004.json` (r004) |
| 120: 120 remains affected by the reviewer finding introduced at 119. | commit-000120-001.md | `exllamav3-fused-fp32-weight-conversion--r002.json` (r002) |
| 136: fix chat-top-k-float (chat caller and sampler conversion) | commit-000136-001.md | `exllamav3-chat-top-k-float--r001.json` (r001) |
| 205: New script caller: histogram_bins < 4 makes tail-bin count zero; < 2 makes weight-bin count zero. | commit-000205-001.md | `exllamav3-histogram-zero-bins--r001.json` (r001) |
| 195: Reviewer-only second trigger: empty order is accepted, order[0] reads empty storage and unsigned rotate_len-1 wraps. | commit-000195-001.md | `exllamav3-unchecked-vector-partition--r001.json` (r001) |
| 205: Reviewer-only wider reach: count_inf_nan also uses dense indexing; no tensor execution. | commit-000205-001.md | `exllamav3-skipped-state-strides--r001.json` (r001) |
| 208: PR 45 records an occurrence of tensor truth-value failure; report is evidence, not local reproduction. Fix remains 95c5097b. | commit-000208-001.md | `exllamav3-tensor-truth-dispatch--r001.json` (r001) |
| 79: Reviewer identifies four K - 1 sites in one identity; the teacher identified two. No unchecked input execution. | commit-000079-001.md | `exllamav3-unchecked-pack-bitrate--r001.json` (r001) |
| 71 packed-scale parent forward/sign-flip candidate | commit-000071-002.md | **HELD**: Candidate conditional on establishing whether packed-scale models were published. Not established; no record or fix asserted. |
| reviewer_observation validator support | commit-000114-001.md | **HELD**: Separate nonurgent implementation request required; unchanged validator rejects this origin. Preserve reviewer labels and exclusions. |

## Existing-identity reconciliation

Previously filed obligations, including revisions in this batch. Preserved does not independently assert acceptance; original administrative status remains authoritative.

| Identity | Verdict/source | Current file / revision | Disposition |
|---|---|---|---|
| exllamav3-absolute-setup-source-paths | Legacy user-supplied Fable review in r002 administrative_review_status; no numbered verdict file found. r002 maintainer observation was awaiting review, not asserted accepted. | `exllamav3-absolute-setup-source-paths--r002.json` (r002) | previously filed; preserved unchanged |
| exllamav3-all-expert-fused-shape | commit-000139-001.md, commit-000140-001.md, commit-000141-001.md, commit-000142-001.md, commit-000155-001.md | `exllamav3-all-expert-fused-shape--r003.json` (r003) | revised in this batch |
| exllamav3-block-sparse-fused-intermediate-dtype | commit-000140-001.md | `exllamav3-block-sparse-fused-intermediate-dtype--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-boolean-dimension-threshold | commit-000123-001.md, commit-000131-001.md, commit-000133-001.md, commit-000134-001.md, commit-000186-001.md | `exllamav3-boolean-dimension-threshold--r003.json` (r003) | revised in this batch |
| exllamav3-cache-detach-count-diagnostic | commit-000036-001.md, commit-000077-001.md | `exllamav3-cache-detach-count-diagnostic--r003.json` (r003) | revised in this batch |
| exllamav3-cache-docstring-contract | commit-000027-001.md, commit-000028-001.md | `exllamav3-cache-docstring-contract--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-chat-stream-argument-mismatch | commit-000106-001.md, commit-000107-001.md | `exllamav3-chat-stream-argument-mismatch--r003.json` (r003) | revised in this batch |
| exllamav3-checkpoint-rotation-gap | commit-000015-001.md, commit-000016-001.md | `exllamav3-checkpoint-rotation-gap--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-checkpoint-token-attribute | commit-000130-001.md, commit-000131-001.md | `exllamav3-checkpoint-token-attribute--r002.json` (r002) | revised in this batch |
| exllamav3-cohere-qk-normalization | commit-000098-001.md, commit-000099-001.md, commit-000108-001.md, commit-000201-001.md | `exllamav3-cohere-qk-normalization--r002.json` (r002) | revised in this batch |
| exllamav3-compare-q-cache-clear-argument-mismatch | commit-000166-001.md, commit-000172-001.md, commit-000173-001.md, commit-000174-001.md | `exllamav3-compare-q-cache-clear-argument-mismatch--r005.json` (r005) | revised in this batch |
| exllamav3-compare-q-filtered-reference-dependency | commit-000174-001.md, commit-000176-001.md | `exllamav3-compare-q-filtered-reference-dependency--r003.json` (r003) | revised in this batch |
| exllamav3-compare-q-inference-mask-context | commit-000163-001.md | `exllamav3-compare-q-inference-mask-context--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-compare-q-no-reference-finalization | commit-000166-001.md, commit-000172-001.md, commit-000173-001.md, commit-000174-001.md, commit-000175-001.md, commit-000176-001.md | `exllamav3-compare-q-no-reference-finalization--r006.json` (r006) | revised in this batch |
| exllamav3-conversion-handle-accumulation | commit-000135-001.md | `exllamav3-conversion-handle-accumulation--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-decilm-kv-head-count | commit-000039-005.md, commit-000044-001.md, commit-000044-003.md, commit-000045-001.md | `exllamav3-decilm-kv-head-count--r003.json` (r003) | revised in this batch |
| exllamav3-deferred-bf16-odd-tail | commit-000119-001.md, commit-000120-001.md, commit-000140-001.md | `exllamav3-deferred-bf16-odd-tail--r002.json` (r002) | revised in this batch |
| exllamav3-deferred-read-errno-reporting | commit-000135-001.md | `exllamav3-deferred-read-errno-reporting--r002.json` (r002) | revised in this batch |
| exllamav3-double-prefixed-qtensor-path | commit-000016-001.md | `exllamav3-double-prefixed-qtensor-path--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-empty-codeblock-feedback | commit-000137-001.md, commit-000138-001.md, commit-000167-001.md, commit-000168-001.md | `exllamav3-empty-codeblock-feedback--r003.json` (r003) | revised in this batch |
| exllamav3-empty-utf32-return-annotation | commit-000145-001.md, commit-000146-001.md | `exllamav3-empty-utf32-return-annotation--r002.json` (r002) | revised in this batch |
| exllamav3-extra-tensor-warning-name | commit-000163-001.md, commit-000164-001.md | `exllamav3-extra-tensor-warning-name--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-first-pass-cost-buffer | commit-000179-001.md | `exllamav3-first-pass-cost-buffer--r002.json` (r002) | revised in this batch |
| exllamav3-format-identifier-consumer-mismatch | commit-000019-001.md, commit-000020-001.md, commit-000021-001.md | `exllamav3-format-identifier-consumer-mismatch--r002.json` (r002) | previously filed; preserved unchanged |
| exllamav3-fused-fp32-weight-conversion | commit-000120-001.md | `exllamav3-fused-fp32-weight-conversion--r002.json` (r002) | revised in this batch |
| exllamav3-fused-linear-bias-pad-slice-order | commit-000033-001.md | `exllamav3-fused-linear-bias-pad-slice-order--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-gemm-selector-divisibility | commit-000124-001.md, commit-000129-001.md, commit-000130-001.md, commit-000133-001.md, commit-000134-001.md | `exllamav3-gemm-selector-divisibility--r003.json` (r003) | previously filed; preserved unchanged |
| exllamav3-gemm-zero-grid-cap | commit-000136-001.md, commit-000186-001.md | `exllamav3-gemm-zero-grid-cap--r002.json` (r002) | revised in this batch |
| exllamav3-humaneval-unconditional-bos | commit-000151-001.md | `exllamav3-humaneval-unconditional-bos--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-in-memory-weight-transpose | commit-000139-001.md | `exllamav3-in-memory-weight-transpose--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-kernel-attribute-cache-device | commit-000189-001.md, commit-000202-001.md | `exllamav3-kernel-attribute-cache-device--r002.json` (r002) | revised in this batch |
| exllamav3-legacy-decilm-config | commit-000039-006.md, commit-000039-007.md, commit-000075-001.md | `exllamav3-legacy-decilm-config--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-llamacpp-cached-accounting | commit-000173-001.md | `exllamav3-llamacpp-cached-accounting--r002.json` (r002) | revised in this batch |
| exllamav3-llamacpp-embedding-order | commit-000173-001.md | `exllamav3-llamacpp-embedding-order--r002.json` (r002) | revised in this batch |
| exllamav3-logits-padding-width-mismatch | commit-000033-001.md, commit-000164-001.md, commit-000165-001.md | `exllamav3-logits-padding-width-mismatch--r002.json` (r002) | previously filed; preserved unchanged |
| exllamav3-mgemm-broadcast-scratch-capacity | commit-000136-001.md | `exllamav3-mgemm-broadcast-scratch-capacity--r002.json` (r002) | revised in this batch |
| exllamav3-missing-combo-sampler | commit-000090-001.md, commit-000091-001.md, commit-000092-001.md | `exllamav3-missing-combo-sampler--r003.json` (r003) | revised in this batch |
| exllamav3-missing-exl3-gemv-header | commit-000129-001.md, commit-000131-001.md, commit-000132-001.md | `exllamav3-missing-exl3-gemv-header--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-missing-gemv-kernel-header | commit-000131-001.md, commit-000132-001.md | `exllamav3-missing-gemv-kernel-header--r003.json` (r003) | revised in this batch |
| exllamav3-model-diff-unconditional-deferral | commit-000155-001.md, commit-000156-001.md, commit-000161-001.md | `exllamav3-model-diff-unconditional-deferral--r003.json` (r003) | previously filed; preserved unchanged |
| exllamav3-multi-gemm-leading-dimension-validation | commit-000133-001.md, commit-000134-001.md, commit-000135-001.md, commit-000136-001.md | `exllamav3-multi-gemm-leading-dimension-validation--r003.json` (r003) | revised in this batch |
| exllamav3-negative-final-device-share | commit-000029-001.md | `exllamav3-negative-final-device-share--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-negative-remaining-minutes | commit-000022-001.md, commit-000023-001.md, commit-000025-001.md | `exllamav3-negative-remaining-minutes--r002.json` (r002) | previously filed; preserved unchanged |
| exllamav3-nonpositive-codeblock-index | commit-000167-001.md, commit-000168-001.md | `exllamav3-nonpositive-codeblock-index--r002.json` (r002) | revised in this batch |
| exllamav3-ppl-axis-bound | commit-000154-001.md, commit-000155-001.md, commit-000203-001.md | `exllamav3-ppl-axis-bound--r002.json` (r002) | revised in this batch |
| exllamav3-presfreq-zero-decay-boundary | commit-000091-001.md, commit-000092-001.md | `exllamav3-presfreq-zero-decay-boundary--r002.json` (r002) | previously filed; preserved unchanged |
| exllamav3-proxy-error-return-name | commit-000012-001.md, commit-000013-001.md, commit-000014-001.md, commit-000015-001.md | `exllamav3-proxy-error-return-name--r003.json` (r003) | previously filed; preserved unchanged |
| exllamav3-python311-typing-override-import | commit-000017-001.md | `exllamav3-python311-typing-override-import--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-qwen3-moe-component-migration | commit-000163-002.md, commit-000166-001.md, commit-000167-001.md | `exllamav3-qwen3-moe-component-migration--r003.json` (r003) | revised in this batch |
| exllamav3-repetition-penalty-masked-nan | commit-000143-001.md, commit-000147-001.md, commit-000148-001.md, commit-000149-001.md | `exllamav3-repetition-penalty-masked-nan--r003.json` (r003) | revised in this batch |
| exllamav3-required-devices-key-test-caller | commit-000025-001.md, commit-000029-001.md | `exllamav3-required-devices-key-test-caller--r002.json` (r002) | previously filed; preserved unchanged |
| exllamav3-scalar-codebook-double-transform | commit-000129-001.md, commit-000131-001.md | `exllamav3-scalar-codebook-double-transform--r003.json` (r003) | revised in this batch |
| exllamav3-scale-progress-premature-completion | commit-000024-001.md, commit-000025-001.md | `exllamav3-scale-progress-premature-completion--r002.json` (r002) | revised in this batch |
| exllamav3-scale-tile-sampling-unused-width | commit-000014-001.md | `exllamav3-scale-tile-sampling-unused-width--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-shard-size-documentation | commit-000029-001.md, commit-000030-001.md, commit-000031-001.md | `exllamav3-shard-size-documentation--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-single-load-missing-deferred-abort | commit-000140-001.md | `exllamav3-single-load-missing-deferred-abort--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-sliced-fp16-padding-target | commit-000120-001.md, commit-000155-001.md, commit-000156-001.md, commit-000161-001.md | `exllamav3-sliced-fp16-padding-target--r004.json` (r004) | revised in this batch |
| exllamav3-sorted-argmax | commit-000080-001.md, commit-000081-001.md, commit-000136-001.md, commit-000177-001.md, commit-000178-001.md, commit-000179-001.md | `exllamav3-sorted-argmax--r002.json` (r002) | revised in this batch |
| exllamav3-terminal-string-bypass | commit-000130-001.md, commit-000131-001.md | `exllamav3-terminal-string-bypass--r002.json` (r002) | revised in this batch |
| exllamav3-tied-word-embeddings-key | commit-000019-001.md, commit-000020-001.md | `exllamav3-tied-word-embeddings-key--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-tokenizer-decode-filtering | commit-000032-001.md | `exllamav3-tokenizer-decode-filtering--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-tokenizer-decode-return-contract | commit-000032-001.md | `exllamav3-tokenizer-decode-return-contract--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-top-k-int-is-integer-compatibility | commit-000137-001.md, commit-000143-001.md, commit-000144-001.md, commit-000149-001.md, commit-000150-001.md, commit-000151-001.md, commit-000152-001.md | `exllamav3-top-k-int-is-integer-compatibility--r004.json` (r004) | previously filed; preserved unchanged |
| exllamav3-top-p-zero-assertion | commit-000114-001.md, commit-000115-001.md | `exllamav3-top-p-zero-assertion--r002.json` (r002) | revised in this batch |
| exllamav3-transformer-empty-block-allocation | commit-000036-001.md | `exllamav3-transformer-empty-block-allocation--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-transformer-missing-norm-input | commit-000036-001.md | `exllamav3-transformer-missing-norm-input--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-two-multiplier-resume-inconsistency | commit-000177-001.md | `exllamav3-two-multiplier-resume-inconsistency--r001.json` (r001) | previously filed; preserved unchanged |
| exllamav3-undeclared-tabulate | commit-000012-001.md, commit-000013-001.md, commit-000027-001.md, commit-000048-001.md | `exllamav3-undeclared-tabulate--r003.json` (r003) | previously filed; preserved unchanged |
| exllamav3-unicode-flush-string-bypass | commit-000131-001.md | `exllamav3-unicode-flush-string-bypass--r002.json` (r002) | revised in this batch |
| exllamav3-unset-max-total-tokens | commit-000146-001.md, commit-000147-001.md | `exllamav3-unset-max-total-tokens--r002.json` (r002) | previously filed; preserved unchanged |
| exllamav3-unsupported-cache-default-argument | commit-000169-001.md, commit-000170-001.md, commit-000171-001.md | `exllamav3-unsupported-cache-default-argument--r003.json` (r003) | revised in this batch |
| exllamav3-variant-collection-loader-api | commit-000120-001.md, commit-000140-001.md | `exllamav3-variant-collection-loader-api--r003.json` (r003) | revised in this batch |

## Requested disposition

Please review identity, attribution, reach, fixes and obligation reconciliation, including explicit holds and unchanged origin-validator limitation. Acceptance is required before 209. Subsequent ledger items will be filed with the next commit request.
