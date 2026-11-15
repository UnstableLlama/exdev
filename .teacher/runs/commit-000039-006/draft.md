# 75c7366bb2e2a7671e38d079f9e5f54945b78006


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/75c7366bb2e2a7671e38d079f9e5f54945b78006) · [Evidence ledger](draft.json)

Adds block-configured DeciLM/Nemotron construction using existing inference modules, with explicit feature restrictions, older-config incompatibility and an empty-block conversion concern.

- [Build DeciLM from heterogeneous block configurations](#models)

## Problem

The architecture registry lacked DeciLMForCausalLM. The change adds a configuration reader and model builder for its per-block attention and FFN descriptions. [source; call_d63f63edb9594598a23421b219e4dadc, call_82b608bd302d43ceabfa019039f70570]

## Reasoning

The implementation reuses existing attention, gated MLP and optional transformer branches instead of introducing separate inference kernels. Checkpoint layer indices remain unchanged while cache indices advance only for active attention branches. [source; call_82b608bd302d43ceabfa019039f70570, call_46edc9733bda43638ce5ed943220eac7, call_ccd753b597d649d78a31f998860bc338]

## Impact

Registration makes DeciLM selectable through Config.from_directory and Model.from_config, including the converter's get_base_model path. Registration does not establish compatibility with every checkpoint advertising that architecture. [source; call_d63f63edb9594598a23421b219e4dadc, call_ff1bbf90bdb244eda29f628b8b58ceb7, call_1161d92cc681419b8d5972ee8d72368c, call_23f42d72dfb64135bbaec1109461147e]

## Source Notes

The inspected discussions concern other changes: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension/toolchain problem; #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns chat mode; #13 concerns tokenizers without bos_token_id; #4, “chore: update config.py,” proposes a spelling correction. None supplies evidence of DeciLM validation. [source; call_4398ee454cb8498a805ef0e6289061d8, call_364a45b1b7b44f3189af521c75091efa, call_aafbc46838d44c08846c645b8906f32d, call_7ac0de69996140ddae5a1ff3c7d68428, call_c6702aa61e74463f95eb286e938090f2]

<a id="models"></a>

## Build DeciLM from heterogeneous block configurations

DeciLMConfig requires block_configs and checks its length against num_hidden_layers. It reads global hidden size and query-head count, defaults head_dim to hidden_size // num_attention_heads, accepts only SiLU when hidden_act is supplied, defaults tied embeddings to false, and delegates RoPE settings with NEOX layout. The parent tree has no block_config, n_heads_in_group or ffn_mult matches. [source; call_82b608bd302d43ceabfa019039f70570, call_ff1bbf90bdb244eda29f628b8b58ceb7, call_3a59d7fc7b014b29b68517df3cc5f1d3, call_e1b375e67be7487d95ef5f1be1a47657, call_de4ae7dc3ad644908690509163d20667]

Each block requires attention and ffn dictionaries. A truthy no_op omits that branch and its norm. Otherwise attention maps n_heads_in_group directly to num_kv_heads and uses separate q_proj/k_proj/v_proj/o_proj tensors; the FFN uses gate_proj/up_proj/down_proj. Active branches reject linear replacement and sparsification, while attention additionally rejects the listed sink-attention modes. These are explicit support boundaries, not alternate implementations. [source; call_82b608bd302d43ceabfa019039f70570, call_ccd753b597d649d78a31f998860bc338, call_25c6f3a140144e778926a62af49a2795]

The FFN width is int(2 * ffn_mult * hidden_size / 3), rounded upward to a multiple of 256 using +255 before integer division. Existing GatedMLP creates two hidden-to-intermediate projections and one intermediate-to-hidden projection, selecting its SiLU multiplication implementation by default. Quantization-map labels preserve shared input grouping for gate/up and Q/K/V. [source; call_82b608bd302d43ceabfa019039f70570, call_25c6f3a140144e778926a62af49a2795, call_ccd753b597d649d78a31f998860bc338]

The builder surrounds the blocks with model.embed_tokens, model.norm and lm_head. It records the last active attention block for prefill, allowing Model.prefill to stop after that block's cache update. prepare_inputs records input_ids and delegates attention preparation; the existing default is uncached Flash Attention, with separate cached and SDPA preparation paths. [source; call_82b608bd302d43ceabfa019039f70570, call_1161d92cc681419b8d5972ee8d72368c, call_ccd753b597d649d78a31f998860bc338]

The earlier optional-branch entry records missing-norm input handling and direct empty-block allocation defects. [ancestor; call_716c57db2f7d4b0980948e4d79ccd58e]

Those implementations are unchanged here. DeciLM supplies a norm for every active branch, avoiding the missing-norm trigger. It can construct wholly empty blocks; their ordinary forward path skips both branches. Direct allocation still divides by zero, although the inspected converter guards allocate_q with a nonempty linear list. [source; call_82b608bd302d43ceabfa019039f70570, call_46edc9733bda43638ce5ed943220eac7, call_4db4fc16aca243ef9c71654712b7bce7, call_2d1fe60092fb416e93ecba27461686f5]

Pinned nvidia/Llama-3_3-Nemotron-Super-49B-v1 uses the expected block schema: hidden size 8192, 64 query heads, active attention entries with n_heads_in_group=8, variable FFN multipliers and attention-only no-ops. Its first shard corroborates separate projection names, K/V shape [1024,8192], and first-layer gate/up shape [14336,8192]. It supplies SiLU, untied embeddings and llama3 RoPE scaling rather than relying on defaults. [source; call_01fce43cee8f4947acd6ceccce7131a0, call_c74abd2a375c44feaeafda4eae08c0c3, call_82b608bd302d43ceabfa019039f70570]

Pinned nvidia/Llama-3_1-Nemotron-Ultra-253B-CPT-v1 and nvidia/Llama-3_1-Nemotron-Ultra-253B-v1 each use hidden size 16384, 128 query heads, active n_heads_in_group=16 entries and 162 block descriptions, including wholly empty blocks. Both supply SiLU, untied embeddings and llama3 RoPE scaling. Their configuration structure fits the new reader, but this does not establish successful conversion of their empty blocks. [source; call_cfb4ac7792c84a42a06fb0d2a03f5516, call_9537373396d7444bbcb611c787986a71, call_ee4f3d010e0549278cbcc6d9fc4a2504, call_727ba4bab7534c67afe19b0d8503a133, call_82b608bd302d43ceabfa019039f70570, call_2d1fe60092fb416e93ecba27461686f5]

Pinned nvidia/Llama-3_1-Nemotron-51B-Instruct supplies the block schema and 8192/64 global dimensions, but includes active attention branches with replace_with_linear=true. The new constructor explicitly rejects those branches, so the commit's Nemotron wording is broader than this checkpoint's supported feature set. [source; call_55d748a2ab324cbea4a4df368fccba9e, call_82b608bd302d43ceabfa019039f70570]

The six pinned older configurations—Deci/DeciCoder-6B, Deci/DeciLM-6b, Deci/DeciLM-6b-instruct, Deci/DeciLM-7B, Deci/DeciLM-7B-instruct and Deci/DeciLM-7B-instruct-GGUF—all advertise DeciLMForCausalLM but omit block_configs. Each has hidden size 4096 and 32 attention heads, SiLU and untied embeddings. The first five express per-layer KV counts separately; the GGUF configuration instead supplies a global KV count. None provides the required per-block FFN mapping. [source; call_53a32c6937e9449ba21e936188e03d41, call_8c8cd2d5731743baab87854cd6978c3e, call_907a0800b8cb4acab1ededd73fbe79be, call_2e17b0a704954a409d02ecd121354f69, call_0c5bb688a8f6466b8be3ae9d7329f8cc, call_5cb57a6ba4944253ab0b5a328144d862, call_82b608bd302d43ceabfa019039f70570]

A standard-library transcription produced head_dim=128 for all three inspected global dimension pairs. For Super-49B, multipliers 0.5, 1, 1.3125, 2.625, 3.28125 and 5.25 produce widths 2816, 5632, 7168, 14336, 17920 and 28672. Its first-layer calculated projection shapes match the inspected header. This checks arithmetic, not model execution. [execution; call_29a2c290b8184d4785c5d2fa90a08fcc]

## Authoring-time findings — pending review

### legacy-decilm-config (suspected; external_compatibility)

The newly registered architecture name also identifies older configurations that the new reader cannot consume.

Trigger: Load any of the six inspected older Deci configurations through the new DeciLMConfig, after base initialization succeeds.

Expected: Architecture-wide compatibility would require translating the older per-layer KV and global FFN schema, or explicitly narrowing the supported checkpoint family.

Actual: The required block_configs read has no fallback; read_dict raises ValueError when that key is absent.

Locations: 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/models/decilm.py — DeciLMConfig.__init__

Source evidence: call_82b608bd302d43ceabfa019039f70570, call_a75e97eceda44a8db4501ce0bf785410, call_53a32c6937e9449ba21e936188e03d41, call_8c8cd2d5731743baab87854cd6978c3e, call_907a0800b8cb4acab1ededd73fbe79be, call_2e17b0a704954a409d02ecd121354f69, call_0c5bb688a8f6466b8be3ae9d7329f8cc, call_5cb57a6ba4944253ab0b5a328144d862

source_inspection: Compared all six pinned configs with the new required read and read_dict. Whole-parent caller search found Config.from_directory consumers; the inspected converter calls it directly, and the factory selects config_class from the registry. [call_e883e07ae5b8457695f54f8bc9972750, call_ff1bbf90bdb244eda29f628b8b58ceb7, call_23f42d72dfb64135bbaec1109461147e, call_d63f63edb9594598a23421b219e4dadc]. Limits: No checkpoint was loaded. Other factory consumers were located but not individually executed; GGUF weight-format support is not established.

### empty-block-allocation-carried (suspected; defect)

The inherited direct-allocation failure remains applicable to wholly empty DeciLM blocks.

Trigger: Call TransformerBlock.allocate_q on a block whose attention and FFN both have no_op=true.

Expected: Return an empty strategy or reject the empty allocation before dividing by its weight count.

Actual: All projections are absent, so allocate_transformer computes budget / numel with numel=0.

Locations: 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/conversion/allocation.py — allocate_transformer

Source evidence: call_82b608bd302d43ceabfa019039f70570, call_46edc9733bda43638ce5ed943220eac7, call_4db4fc16aca243ef9c71654712b7bce7

source_inspection: Checked the unchanged allocator and its TransformerBlock wrapper. Whole-parent allocate_q search located the converter consumer, which guards allocation with if linears and therefore avoids this particular failure. [call_53c0e4a58d95427d80ab4a5b51fb8059, call_2d1fe60092fb416e93ecba27461686f5]. Limits: Direct-call failure inferred from source; not an observed converter failure at allocate_q.

### empty-block-conversion-bitrate (suspected; defect)

Newly constructible empty blocks expose an unguarded converter bitrate denominator.

Trigger: Convert a wholly empty DeciLM block, such as those in the inspected Ultra configurations, and reach the final bitrate calculation.

Expected: Treat the block as a parameter-free identity and skip or specially represent its bitrate.

Actual: The converter skips quantization allocation but subsequently divides num_bits by module.weights_numel(); an empty TransformerBlock has no registered submodules and therefore a zero weight count.

Locations: 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/conversion/convert_model.py — main, 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/models/decilm.py — DeciLMModel.__init__

Source evidence: call_82b608bd302d43ceabfa019039f70570, call_36aecc2578e94b679d981d50d913a3a8, call_2d1fe60092fb416e93ecba27461686f5, call_cfb4ac7792c84a42a06fb0d2a03f5516, call_ee4f3d010e0549278cbcc6d9fc4a2504

source_inspection: Traced empty branch construction, None-filtering registration, recursive weight counting and the converter loop. Parent search located convert.py importing this main function; its successful prepare path calls main directly. [call_46edc9733bda43638ce5ed943220eac7, call_36aecc2578e94b679d981d50d913a3a8, call_23f42d72dfb64135bbaec1109461147e, call_6b2dcc11e4ce4b1ca9802aeed76c2a7f, call_06ca1e15c41d40a1bd2f17fdb26486b2]. Limits: No conversion was run. Empty-tensor serialization precedes this calculation and could fail earlier.

## Uncertainty and limits

No model loading, generation, conversion or GPU execution was performed. The Python check transcribed dimension arithmetic only.

Tensor-shape corroboration is limited to the first Super-49B shard; configuration agreement alone does not establish checkpoint-wide compatibility.

The source establishes the 2/3 FFN scaling and 256-wide alignment, but not the author's rationale for choosing them.

For empty blocks, behavior of saving an empty tensor dictionary was not executed; the subsequent zero-denominator bitrate calculation is established by source inspection.
