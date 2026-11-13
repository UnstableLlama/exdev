# 75c7366bb2e2a7671e38d079f9e5f54945b78006


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/75c7366bb2e2a7671e38d079f9e5f54945b78006) · [Evidence ledger](draft.json)

Adds DeciLM dispatch and per-block construction for Nemotron-style models, including optional branches, variable FFN widths and contiguous attention-cache indices. Initial checkpoint dimensions match; end-to-end compatibility is untested.

- [Construct heterogeneous DeciLM blocks using shared modules](#models)

## Problem

DeciLM needs per-block attention and feed-forward configuration rather than Llama's uniform KV-head count and intermediate width. The pinned Nemotron-Super configuration declares DeciLMForCausalLM, includes attention-free blocks, and leaves the global intermediate_size and num_key_value_heads null. [source; call_ca5233e4b6a44243b6cd26fe157dc4e2, call_89aca1ba76b34e249371275b610b5fff]

## Reasoning

The change adds an architecture adapter using existing transformer components instead of introducing a separate execution engine. Its distinguishing work is constructing heterogeneous blocks and separating checkpoint layer numbers from contiguous cache indices. [source; call_5f5910b2075444a0a1c568e603d6f921, call_d952ce0f9ad647d5961aa136a77b6710]

## Impact

Config.from_directory can now dispatch DeciLMForCausalLM to DeciLMConfig, whose model_class selects DeciLMModel through Model.from_config. [source; call_5f5910b2075444a0a1c568e603d6f921, call_d952ce0f9ad647d5961aa136a77b6710, call_7c80f70cb0cf43b5889981c9a6d81e68, call_9bfb15c6aaba46bbb31b4638f414eb62]

## Source Notes

The earlier architecture entry describes the shared checkpoint-to-module adapter design. This change extends that design with a dedicated heterogeneous-block constructor. [ancestor; call_68e9b529aafe4b7ebfb8e0cf485aca2b]

The inspected discussions concern separate matters: issue 7 reports an undefined __cxa_call_terminate symbol; issue 12 reports Qwen stop-condition failure; PR 13 reports conversion with missing BOS metadata; PR 4 proposes a spelling correction. None supplies DeciLM execution evidence. [source; call_e6dfb0dbf2bb4aca86a52df4914c6913, call_3aa2c13a875b44b0b3e3d83ab9f17656, call_d25dd006307540cbae6ffea3176bd456, call_b6f9958acb264f779bd369ebad8ebad1, call_c71fc01cfdad46df8caa9f8e8c19ee48]

<a id="models"></a>

## Construct heterogeneous DeciLM blocks using shared modules

DeciLMConfig reads global hidden width, query-head count, optional head dimension, normalization epsilon and layer count, reuses NEOX-style RoPE settings, and requires block_configs to contain exactly one entry per declared layer. Unlike LlamaConfig, it does not require a global intermediate width or KV-head count. [source; call_d952ce0f9ad647d5961aa136a77b6710, call_ca5233e4b6a44243b6cd26fe157dc4e2]

Each block's attention and ffn dictionaries independently control branch construction through no_op. An omitted branch has neither its normalization nor its computation module. Existing TransformerBlock.forward skips absent branches and adds each present branch's output residually; the DeciLM constructor supplies a normalization whenever it supplies a branch. [source; call_d952ce0f9ad647d5961aa136a77b6710, call_d35a3c18ec7f4a97a85d632182883693]

Active attention uses n_heads_in_group directly as num_kv_heads and retains checkpoint names model.layers.<original index>.self_attn.{q,k,v,o}_proj. Its separate cache_layer_idx advances only for active attention. This matches Cache's ordered list of actual cache-capable modules and Attention.decode_flash_attn's lookup by layer_idx, avoiding cache gaps where attention is omitted. [source; call_d952ce0f9ad647d5961aa136a77b6710, call_9b96cc03bd4149649d2e136e3394ae81, call_b30a06bb59bf4475a8e73712d1bb6fae, call_9bfb15c6aaba46bbb31b4638f414eb62]

last_kv_module_idx records the top-level block containing the final active attention. Model.prefill stops there, and TransformerBlock's prefill early return skips that block's remaining residual/MLP work. Full forward still traverses all blocks, including any trailing attention-free blocks. [source; call_d952ce0f9ad647d5961aa136a77b6710, call_9bfb15c6aaba46bbb31b4638f414eb62, call_d35a3c18ec7f4a97a85d632182883693]

Active feed-forward branches calculate int(2 * ffn_mult * hidden_size / 3), then round that integer upward to a multiple of 256 using (value + 255) // 256 * 256. GatedMLP maps separate gate/up projections into that width and a down projection back to hidden width, using its default SiLU multiplication path. [source; call_d952ce0f9ad647d5961aa136a77b6710, call_6f91defcd402431faa667ab24cfed81c]

A standard-library scalar transcription with Nemotron-Super's hidden width 8192 produced intermediate widths 2816, 5632, 7168, 14336, 17920 and 28672 for multipliers 0.5, 1, 1.3125, 2.625, 3.28125 and 5.25. It also calculated head dimension 128 and KV projection width 1024. [execution; call_de877a3508ee4e56828cb35125b53ee2]

The first checkpoint shard corroborates the initial mappings: layers 0 and 1 have gate/up widths 14336 and 28672 respectively, Q/O matrices are [8192,8192], and K/V matrices are [1024,8192]. These are metadata matches, not output-equivalence results. [source; call_89aca1ba76b34e249371275b610b5fff, call_2accad3d8633411d84d26b692a6b5f50, call_d952ce0f9ad647d5961aa136a77b6710]

Support is explicitly bounded: active attention rejects truthy sink-token, linear-replacement, sparsification, unshifted-sink and prefill-window-in-sink settings; active FFNs reject linear replacement and sparsification. These checks occur after no_op selection, so skipped branches do not require those implementations. [source; call_d952ce0f9ad647d5961aa136a77b6710]

The adapter preserves the embedding → blocks → final RMSNorm → lm_head sequence, the tied-embedding fallback, and existing attention input preparation. Reusing those interfaces limits architecture-specific code to configuration and construction; successful end-to-end operation remains unmeasured. [inference; call_d952ce0f9ad647d5961aa136a77b6710, call_ca5233e4b6a44243b6cd26fe157dc4e2, call_9b96cc03bd4149649d2e136e3394ae81]

## Uncertainty and limits

No model loading, conversion, GPU inference, numerical-equivalence test or performance measurement was run.

External validation covers Nemotron-Super's configuration and first tensor shard only, not every shard or the other catalogued Nemotron variants.

The scalar check validates transcribed dimension arithmetic, not repository execution or BF16/FP16 behavior. The source establishes the two-thirds multiplier and 256-wide rounding, but not their original design rationale.
