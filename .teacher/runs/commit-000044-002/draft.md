# 3a7b4895e45b1eb2f291f8b09b0a5dac569e984c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3a7b4895e45b1eb2f291f8b09b0a5dac569e984c) · [Evidence ledger](draft.json)

Corrects DeciLM's per-layer KV-head count by dividing query heads by group size, changing K/V projection dimensions and runtime reshaping where the previous direct mapping differed.

- [Translate DeciLM group size into KV-head count](#models)

## Problem

DeciLM passed n_heads_in_group directly as the number of KV heads. The change instead divides the global query-head count by that per-layer value. [source; call_faa0516a55094f6faf0c009effa1028f]

## Reasoning

The revised mapping treats n_heads_in_group as query heads sharing one KV head, rather than as the count of KV heads themselves. [inference; call_faa0516a55094f6faf0c009effa1028f, call_7000822d1c0b45ecb6368225443df0d8]

## Impact

The corrected count determines K/V projection widths and the K/V head dimensions used by all three attention decode paths. Q and output projection dimensions are unchanged. [source; call_7000822d1c0b45ecb6368225443df0d8, call_faa0516a55094f6faf0c009effa1028f]

## Source Notes

Whole-parent searches found the exact key only in DeciLM's Attention construction; the broader n_heads search also located the global num_attention_heads readers. [source; call_72d1eb4021de437c87b69beaff29dc4a, call_31fd77ecded84f8b81799e1e420bf3c0]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and a reporter-supplied environment workaround, not a DeciLM head-count problem. [source; call_f0a4cd45f0e548ba889b75f2e92f2a87]

<a id="models"></a>

## Translate DeciLM group size into KV-head count

DeciLMConfig reads num_attention_heads into num_q_heads and defaults an absent or falsey head_dim to hidden_size // num_q_heads. DeciLMModel now computes num_kv_heads separately for each active attention block as num_q_heads // n_heads_in_group. Attention marked no_op bypasses this calculation; existing unsupported-attention assertions remain unchanged. [source; call_638a286c2c3c467bb7723aa559b55ba9, call_faa0516a55094f6faf0c009effa1028f]

Attention.__init__ multiplies the resulting KV-head count by head_dim for both K and V projection widths. Its decode methods reshape projected K/V using that same count, so the fix aligns construction and runtime interpretation without modifying the shared attention implementation. [source; call_7000822d1c0b45ecb6368225443df0d8]

For nvidia/Llama-3_1-Nemotron-51B-Instruct, the inspected configuration supplies 64 query heads, hidden size 8192 and ordinary attention group sizes 8, 16, 32 and 64. It also requests linear-replacement attention, which the unchanged constructor explicitly rejects; this patch does not add that capability. [source; call_2c969ce1a08b431684cc65e61ce6ec8b, call_638a286c2c3c467bb7723aa559b55ba9, call_faa0516a55094f6faf0c009effa1028f]

For nvidia/Llama-3_1-Nemotron-Ultra-253B-CPT-v1 and, separately, nvidia/Llama-3_1-Nemotron-Ultra-253B-v1, the inspected configurations supply 128 query heads, hidden size 16384 and group size 16 for active attention. Neither supplies head_dim, so both use the constructor's fallback. [source; call_a439415bb06b4167be24fe1374b28d15, call_8a7bedf311cf440fb36aaad3b81c350e, call_d5581aaa62034c5d9fdb1a7b8f2e02d6, call_8861ba2b2cfa4a5ab3d9f99e6d28e1f8, call_638a286c2c3c467bb7723aa559b55ba9]

For nvidia/Llama-3_3-Nemotron-Super-49B-v1, the inspected configuration supplies 64 query heads, hidden size 8192 and group size 8 for active attention, again without an explicit head_dim. [source; call_6473e1445f2b40f2aa49aa0e9e19bbb4]

A scalar calculation gives head_dim 128 for all four configurations. For 51B, group sizes 8/16/32/64 map to 8/4/2/1 KV heads and widths 1024/512/256/128. Each Ultra configuration changes from 16 to 8 KV heads, reducing the configured K/V width from 2048 to 1024. Super remains at 8 KV heads and width 1024 because 64 // 8 equals the previous value 8. [execution; call_26f69e8b9abd465eb31f54a6c69dfab5]

## Uncertainty and limits

The computation checks transcribed integer shape arithmetic only; no model loading, conversion, attention execution or GPU test was run.

Checkpoint tensor shapes and end-to-end compatibility were not verified. Correcting the head-count mapping alone does not establish complete support for any checkpoint.
