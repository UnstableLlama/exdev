# 9665ba99989955593d2fb148323c9a96c77d1bea


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/9665ba99989955593d2fb148323c9a96c77d1bea) · [Evidence ledger](draft.json)

Adds Mixtral registration and configuration-to-module mappings, reusing existing grouped-query attention and sparse-expert execution. Four pinned model configurations match the adapter's principal dimensions and defaults; runtime compatibility remains untested.

- [Mixtral configuration and sparse-expert assembly](#models)

## Problem

MixtralForCausalLM needs an architecture-specific configuration and checkpoint mapping before Config.from_directory can select it. [source; call_464704546b31427f82bab6b7144bc4fb, call_a757d578dbe3443d8ca636abaa148ce4]

## Reasoning

The change reuses existing attention, transformer-block and sparse-expert implementations rather than introducing Mixtral-specific kernels. [source; call_2d5bedc8781a4a6e8f879289e2ab7a60, call_5e4eb30a7797469492fa3c2cf6db384a]

## Impact

Registers MixtralModel and supplies MixtralConfig, making the architecture selectable through the existing configuration factory. [source; call_464704546b31427f82bab6b7144bc4fb, call_a757d578dbe3443d8ca636abaa148ce4, call_2d5bedc8781a4a6e8f879289e2ab7a60]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and the reporter's environment workaround. Its connection here is only inferred from the traceback's config.py import line; it is not evidence of a Mixtral defect or motivation for this change. [inference; call_eef447a2a45d4b3ab59964fdda7cad9d, call_a757d578dbe3443d8ca636abaa148ce4]

PR #4, “chore: update config.py,” proposes “containg → containing.” Its inferred connection is the matching typo in the shared configuration source, not architecture support. [inference; call_d39ef38926ec4b409b580c7cde1cd834, call_a757d578dbe3443d8ca636abaa148ce4]

<a id="models"></a>

## Mixtral configuration and sparse-expert assembly

MixtralConfig reads intermediate_size into moe_intermediate_size and num_local_experts into num_experts. These are deliberate checkpoint-key mappings: the existing Qwen3 MoE configuration instead reads moe_intermediate_size and num_experts. num_experts_per_tok controls how many experts are selected. [source; call_2d5bedc8781a4a6e8f879289e2ab7a60, call_85a6aed28c704fbc88bc39d964a5fcae, call_688dd32abb7c46359cfc4a171a743b2a, call_5e4eb30a7797469492fa3c2cf6db384a]

Missing or false-valued head_dim is derived as hidden_size // num_attention_heads; absent KV-head count defaults to the query-head count. hidden_act may be absent but must equal silu when supplied. The model uses NEOX-style RoPE settings and defaults tied embeddings to false. [source; call_2d5bedc8781a4a6e8f879289e2ab7a60, call_a757d578dbe3443d8ca636abaa148ce4]

Assembly is embedding → repeated pre-normalized attention and MoE residual blocks → final RMSNorm → vocabulary projection. Attention maps q_proj/k_proj/v_proj/o_proj. Each block_sparse_moe maps expert w1 to the activation gate, w3 to the up projection and w2 to the down projection; gate is the separate router. Expert intermediates and outputs are explicitly half precision. [source; call_2d5bedc8781a4a6e8f879289e2ab7a60, call_8f622b80a2934449b891476e0c56881f, call_5e4eb30a7797469492fa3c2cf6db384a]

The reused router produces unpadded expert scores, applies softmax, selects top-k experts and renormalizes their weights. Multiple flattened tokens or non-fully-EXL3 experts use the per-expert Torch path; a single token with fully EXL3 experts uses indexed fused projections. MultiLinear additionally requires compatible dimensions and K, no bias or softcap, and unit post-scale. [source; call_5e4eb30a7797469492fa3c2cf6db384a]

prepare_inputs preserves input_ids in params and delegates attention preparation. The shared default is uncached Flash Attention; SDPA and cached Flash Attention remain explicit alternatives with their existing cache and shape requirements. Mixtral supplies no sliding-window override. [source; call_2d5bedc8781a4a6e8f879289e2ab7a60, call_146eff0a48954d639c9feb0410880a57]

The pinned mistralai/Mixtral-8x7B-v0.1 and Mixtral-8x7B-Instruct-v0.1 configurations each match the new configuration mapping: hidden size 4096, intermediate size 14336, 32 layers, 32 query heads, eight KV heads and vocabulary 32000. Both specify eight experts with two selected per token. [source; call_7495decd53d3472996262fbdc094eb3e, call_03d40aa9e21348cca7f03cc58bd5ef4b, call_2d5bedc8781a4a6e8f879289e2ab7a60]

The pinned mistralai/Mixtral-8x22B-v0.1 matches with hidden size 6144, intermediate size 16384, 56 layers, 48 query heads, eight KV heads and vocabulary 32000. Mixtral-8x22B-Instruct-v0.1 has the same dimensions except vocabulary 32768. Both likewise specify eight experts and top-two routing. [source; call_9f301461ccf94971b530aa33aeb00e1e, call_28cb207946bf4b26baafdf0a1f8b7425, call_2d5bedc8781a4a6e8f879289e2ab7a60]

All four configurations omit head_dim, specify silu, untied embeddings, RMS epsilon 1e-5 and null sliding_window. They supply rope_theta 1000000 rather than using the shared 10000 fallback. Their declared bfloat16 dtype does not change this adapter's explicit half-precision MoE intermediates. [source; call_7495decd53d3472996262fbdc094eb3e, call_03d40aa9e21348cca7f03cc58bd5ef4b, call_9f301461ccf94971b530aa33aeb00e1e, call_28cb207946bf4b26baafdf0a1f8b7425, call_a757d578dbe3443d8ca636abaa148ce4, call_2d5bedc8781a4a6e8f879289e2ab7a60]

A standard-library calculation of the inspected dimension formulas gives head dimension 128 and KV projection width 1024 for all four models. Query-head grouping is four per KV head for 8x7B and six for 8x22B; assembled top-level module counts are respectively 35 and 59. [execution; call_4264f4062857485eab50bb5710ad5fd0]

## Uncertainty and limits

No model loading, conversion, generation or GPU execution was performed. The Python calculation checks transcribed shape arithmetic only.

Checkpoint tensor headers were not inspected; configuration compatibility does not establish that every weight is loadable or numerical outputs match a reference implementation.
