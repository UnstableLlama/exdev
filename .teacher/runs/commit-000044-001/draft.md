# 3a7b4895e45b1eb2f291f8b09b0a5dac569e984c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3a7b4895e45b1eb2f291f8b09b0a5dac569e984c) · [Evidence ledger](draft.json)

Corrects DeciLM attention construction by deriving KV-head count from query-head count divided by per-block group size, affecting K/V dimensions without changing shared attention kernels.

- [Derive DeciLM KV-head counts from attention group sizes](#models)

## Problem

DeciLMModel passed n_heads_in_group directly as the KV-head count. The patch instead derives that count by dividing the global query-head count by the per-block group size. [source; call_e6aacf01cdd1462a8936ec12faad45d3]

## Reasoning

The revised expression interprets n_heads_in_group as query heads sharing one KV head, rather than the number of KV heads. This keeps the architecture-specific translation in DeciLMModel while retaining the shared Attention interface. [inference; call_e6aacf01cdd1462a8936ec12faad45d3, call_fb4dcac8f41446a08860928ba6f7714d]

## Impact

The derived count controls K/V projection widths, K/V tensor reshaping and Attention's grouped-query flag. Query and output projection widths remain unchanged. [source; call_fb4dcac8f41446a08860928ba6f7714d, call_e6aacf01cdd1462a8936ec12faad45d3]

## Source Notes

The earlier DeciLM entry describes the original direct mapping and reports matching initial checkpoint dimensions; that historical check did not establish correctness for other group sizes. [ancestor; call_381393499b5447739d2ef0f7cecb7f25]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and a reporter-described environment workaround, not a DeciLM head-configuration failure. [source; call_0f0655f621034632a000c3e96ee1ee49]

<a id="models"></a>

## Derive DeciLM KV-head counts from attention group sizes

DeciLMConfig obtains num_q_heads from num_attention_heads. For each active attention block, DeciLMModel now supplies num_q_heads // n_heads_in_group to Attention. Attention-free blocks bypass this construction; checkpoint projection names and contiguous cache-layer indexing are unchanged. [source; call_5a3c061650bf4b82a085dc1e71295d94, call_e6aacf01cdd1462a8936ec12faad45d3]

Attention constructs each K/V projection with num_kv_heads * head_dim output features and uses the same head count when reshaping projected tensors in all three decode paths. Its SDPA path enables grouped-query attention when query and KV counts differ. [source; call_fb4dcac8f41446a08860928ba6f7714d]

A scalar transcription with 32 query heads, group size 8 and head dimension 128 changes the KV count from 8 to 4 and each KV width from 1024 to 512. With 64 query heads and group size 8, both formulas give 8 KV heads, illustrating how one dimension check can miss the distinction. [execution; call_a8601004c9ed4111bdb3dce671d7726b]

For 32 query heads, the scalar check maps group size 1 to 32 KV heads and group size 32 to one KV head—the unshared and fully shared endpoints of the revised interpretation. [execution; call_a8601004c9ed4111bdb3dce671d7726b]

## Uncertainty and limits

No model loading, conversion or GPU inference was executed; the scalar check models only integer head-count and width arithmetic.

No external DeciLM configuration specification or checkpoint was inspected in this session. Valid positive, evenly dividing group sizes are assumed when interpreting the quotient as a head count; the changed expression adds no validation.
