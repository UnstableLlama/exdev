# 75c7366bb2e2a7671e38d079f9e5f54945b78006


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/75c7366bb2e2a7671e38d079f9e5f54945b78006) · [Evidence ledger](draft.json)

Adds DeciLM dispatch and per-block model construction for Nemotron, with explicit unsupported variants and a suspected empty-block conversion failure.

- [Construct DeciLM from heterogeneous block descriptions](#models)

## Problem

DeciLM checkpoints need per-block attention and FFN descriptions rather than Llama's uniform KV-head count and intermediate width. The change registers DeciLMForCausalLM and adds dedicated configuration and model classes. [source; call_27a64ff1db314344b4d52bd58b3f31df, call_658db52e7e464e96a481fe6114fa6d7b, call_5bcaffd8d1864a229bb451964edbbb77]

## Reasoning

Reusing Attention, GatedMLP and TransformerBlock keeps the existing execution machinery while allowing checkpoint layer numbering, active cache numbering and FFN widths to differ. [inference; call_658db52e7e464e96a481fe6114fa6d7b, call_11471df83aff4338b138ee66be5cab06, call_43e0ce5502024ab3bf00b1ae169e958c]

## Impact

Config.from_directory can now dispatch DeciLMForCausalLM to DeciLMConfig; Model.from_config subsequently instantiates DeciLMModel. Registration does not imply compatibility with every Nemotron configuration. [source; call_27a64ff1db314344b4d52bd58b3f31df, call_4b986ee963c04e4c827cb8f0f8bf272e, call_93913323ecf1489eaa94e1ab663b1780, call_658db52e7e464e96a481fe6114fa6d7b]

## Source Notes

The earlier optional-branch entry records missing-normalization and empty-allocation hazards in TransformerBlock. [ancestor; call_d48a48470ebc4aa286196a742309719f]

Those implementations are unchanged here. DeciLM supplies a norm whenever its corresponding branch exists, avoiding the missing-normalization trigger. It can construct entirely empty blocks; conversion skips their allocation, but its later bitrate calculation has a separate zero-denominator hazard. [source; call_658db52e7e464e96a481fe6114fa6d7b, call_0b73e7b306a44e08b08bdad3c5924a8b, call_e19d110e1a8e4190b538a614e7a52fca, call_62ccdaacccb248668cb1cc6a8e4b8604]

The inspected discussions report different problems: issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns native-extension loading; issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns chat invocation; PR #13, “Fix a tokenizer issue while converting models without a bos_token_id defined,” concerns null BOS handling. None supplies DeciLM execution evidence. [source; call_6d39b63bd0324ec482384424952244de, call_fdcf829edb4e446cb5d078b47e3d2846, call_63560424210a438fb177f3e1830c3b1a, call_432bf21bceec464b845d0f1494c9bcca]

<a id="models"></a>

## Construct DeciLM from heterogeneous block descriptions

DeciLMConfig requires block_configs to have num_hidden_layers entries. It reads global hidden size and query-head count, derives head_dim by integer division when absent or false, accepts SiLU or an omitted activation declaration, and uses the existing NEOX-style RoPE settings reader. Unlike LlamaConfig, it does not require a global intermediate_size or num_key_value_heads. [source; call_658db52e7e464e96a481fe6114fa6d7b, call_4b986ee963c04e4c827cb8f0f8bf272e, call_5bcaffd8d1864a229bb451964edbbb77]

Each block reads attention and ffn dictionaries. A truthy no_op removes that branch and its norm. Active attention maps n_heads_in_group directly to num_kv_heads and uses separate q_proj, k_proj, v_proj and o_proj tensors. Active FFNs use gate_proj, up_proj and down_proj through GatedMLP's default SiLU activation. [source; call_658db52e7e464e96a481fe6114fa6d7b, call_11471df83aff4338b138ee66be5cab06, call_43e0ce5502024ab3bf00b1ae169e958c]

FFN width is int(2 × ffn_mult × hidden_size / 3), then rounded upward to a multiple of 256 using (width + 255) // 256 × 256. Here 255 is the rounding offset, not a separate size limit. [source; call_658db52e7e464e96a481fe6114fa6d7b]

A standard-library transcription produced head_dim=128 for both 8192/64 and 16384/128. At hidden size 8192, multipliers 0.5, 1, 1.3125, 2.625, 3.28125 and 5.25 produce widths 2816, 5632, 7168, 14336, 17920 and 28672. At hidden size 16384, multiplier 0.4875 produces 5376 and multiplier 39 produces 425984. [execution; call_48aafba953b244df81e1a87475e6f559]

Tensor names retain the original block index, while cache_layer_idx advances only for active attention. This matches Attention.decode_flash_attn's lookup by layer_idx and Model.get_cache_layers' traversal of KV-capable modules. last_kv_module_idx records the last attention-bearing top-level block, allowing Model.prefill to stop there rather than execute trailing FFN-only blocks. [source; call_658db52e7e464e96a481fe6114fa6d7b, call_11471df83aff4338b138ee66be5cab06, call_93913323ecf1489eaa94e1ab663b1780]

The model retains token embedding, final RMSNorm and logits projection. Tied embeddings have an alternate-key path when the primary head is absent. prepare_inputs stores input_ids and delegates to prepare_for_attn, whose default is uncached Flash Attention; cached execution still requires its existing cache and position metadata. [source; call_658db52e7e464e96a481fe6114fa6d7b, call_11471df83aff4338b138ee66be5cab06]

Active branches explicitly reject linear replacement and sparsification. Active attention also rejects sink-token and related sink-attention options. These checks occur after the no_op test, so disabled branches need neither valid projection dimensions nor supported active-branch options. [source; call_658db52e7e464e96a481fe6114fa6d7b]

The pinned nvidia/Llama-3_3-Nemotron-Super-49B-v1 configuration uses 80 layers, hidden size 8192, 64 query heads and eight KV heads for active attention. Its disabled attention branches and varying FFN multipliers fit the new construction choices; all FFNs remain active and the explicitly rejected options are false or null. It declares SiLU, untied embeddings and Llama-3 RoPE scaling with factor 8, so those values are supplied rather than inferred from defaults. [source; call_f3e2de7843994aeea4a1e5f11b2eb115, call_658db52e7e464e96a481fe6114fa6d7b]

The pinned nvidia/Llama-3_1-Nemotron-51B-Instruct configuration also uses 80 layers, hidden size 8192, 64 query heads, SiLU, untied embeddings and RoPE factor 8. Its ordinary attention and FFN descriptions map to the new fields, but active replace_with_linear attention makes the model incompatible with the constructor's explicit assertion. [source; call_4ae5082d9a454c6186f17df475f1603b, call_658db52e7e464e96a481fe6114fa6d7b]

The pinned nvidia/Llama-3_1-Nemotron-Ultra-253B-CPT-v1 configuration uses 162 layers, hidden size 16384, 128 query heads and 16 KV heads for active attention, with SiLU, untied embeddings and RoPE factor 16. Its active-branch options fit the checks, but it contains fully disabled blocks that expose the conversion hazard recorded here. [source; call_02aab2b62eaa4009a3593fcf81031b44, call_6adc32af8d3d47258d5ded12f9424656, call_b4ac408fd9a34b6bb14e1db10f05d947, call_658db52e7e464e96a481fe6114fa6d7b, call_62ccdaacccb248668cb1cc6a8e4b8604]

The pinned nvidia/Llama-3_1-Nemotron-Ultra-253B-v1 configuration independently has the same listed global dimensions, active KV-head count, activation, untied embeddings and RoPE factor as the CPT variant. Its branch descriptions likewise include fully disabled blocks; registration and configuration parsing therefore do not establish successful conversion. [source; call_5a79634e0eba4ace92df2b8b73d6bc39, call_89a60826ca1a4f67844be4c251048979, call_c0b1583ac6ad42b68753481ba3e3ce78, call_658db52e7e464e96a481fe6114fa6d7b, call_62ccdaacccb248668cb1cc6a8e4b8604]

## Authoring-time findings — pending review

### nemotron-linear-replacement (suspected; external_compatibility)

Architecture registration covers less than the inspected Nemotron family: the 51B checkpoint requests an explicitly unsupported attention variant.

Trigger: Construct DeciLMModel from the pinned Llama-3_1-Nemotron-51B-Instruct configuration, reaching an active attention block with replace_with_linear=true.

Expected: Full compatibility with that checkpoint would require implementing its replacement attention branch.

Actual: DeciLMModel.__init__ asserts that replace_with_linear is false and rejects the configuration rather than constructing that branch.

Locations: 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/models/decilm.py — DeciLMModel.__init__

Source evidence: call_658db52e7e464e96a481fe6114fa6d7b, call_4ae5082d9a454c6186f17df475f1603b

source_inspection: Compared the checkpoint's active replacement flags with the constructor assertion. Parent-tree model_class search and Model.from_config inspection establish the factory call; get_base_model uses that factory for conversion. [call_7b529bebd64544a6a7ad3906eb16517d, call_93913323ecf1489eaa94e1ab663b1780, call_b6634cfc24314aa98b04c81dae2eedb2]. Limits: No construction was executed; the observation concerns the explicit compatibility boundary, not a demonstrated regression.

### empty-block-conversion (suspected; defect)

Fully disabled DeciLM blocks have zero weights, but conversion still calculates their bits per weight.

Trigger: Convert a configuration containing attention.no_op=true and ffn.no_op=true, as in both inspected Ultra variants, and reach the module's bitrate-reporting step.

Expected: Treat the empty block as a pass-through and skip or specially represent its undefined bits-per-weight statistic.

Actual: The constructor appends an empty TransformerBlock. Module.weights_numel returns zero; conversion skips allocation because there are no linears but subsequently evaluates num_bits / module.weights_numel(), giving a zero denominator.

Locations: 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/models/decilm.py — DeciLMModel.__init__, 29060addb5a3994cec3867e1f2f6b30ecda7b8a3:exllamav3/conversion/convert_model.py — main

Source evidence: call_658db52e7e464e96a481fe6114fa6d7b, call_e3f0e143d5794c6ba16e5c49e7855c18, call_62ccdaacccb248668cb1cc6a8e4b8604, call_02aab2b62eaa4009a3593fcf81031b44, call_5a79634e0eba4ace92df2b8b73d6bc39

source_inspection: Traced construction, child registration, weight aggregation and the conversion loop. Whole-parent search located convert.py importing main; its inspected call invokes main after prepare succeeds. The allocator's inherited empty-input division also remains, but the inspected conversion call guards allocation with if linears. [call_45208f30700c4091982ad735cb768531, call_f8dacaf3251a449abcfa8f8833d3c495, call_b6634cfc24314aa98b04c81dae2eedb2, call_22232b2b67ad4e4f958fb328c7294fa8, call_e19d110e1a8e4190b538a614e7a52fca]. Limits: Source reasoning only. Earlier loading and empty-dictionary serialization were not executed; this does not establish the first failure encountered in a complete conversion.

## Uncertainty and limits

No model loading, tensor inference, conversion or GPU test was executed. The Python check transcribed dimension arithmetic only.

Configuration comparisons do not establish agreement with checkpoint tensor shapes or numerical equivalence to NVIDIA's implementation.

The source specifies the FFN multiplier formula and 256-wide alignment, but does not explain their architectural or performance rationale.

Empty-tensor serialization was not executed; the conversion division observation is conditional on reaching the subsequent bitrate calculation.
