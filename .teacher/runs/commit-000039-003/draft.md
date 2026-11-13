# 75c7366bb2e2a7671e38d079f9e5f54945b78006


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/75c7366bb2e2a7671e38d079f9e5f54945b78006) · [Evidence ledger](draft.json)

Adds DeciLM discovery and per-block model assembly using existing optional transformer branches; inspected Nemotron-51B metadata exposes unsupported linear replacements and a KV-head dimension mismatch.

- [DeciLM registration and heterogeneous decoder construction](#models)

## Problem

The architecture registry lacked DeciLMForCausalLM, so Config.from_directory could not select a DeciLM implementation. [source; call_efda0deeaec04ed8bce1386143c321a8, call_bf50c63e984d4e249a8b4b930a186a94]

## Reasoning

The implementation represents heterogeneous decoder blocks using existing attention, gated-MLP and optional-branch machinery rather than introducing another execution backend. [source; call_7abba61d0f374a1385e14ec6ba6b93e7, call_4f5d30c048f0474198e92ae08083dc2b]

## Impact

Architecture discovery now selects DeciLMConfig and DeciLMModel. This enables construction of the supported block forms, but does not establish compatibility with every Nemotron checkpoint. [source; call_efda0deeaec04ed8bce1386143c321a8, call_7abba61d0f374a1385e14ec6ba6b93e7]

## Source Notes

Whole-parent literal searches found no DeciLM or Nemotron occurrences; these searches do not exclude dynamically supplied architectures. [source; call_2ad507e8b20a4780b62791bb33cebc5c, call_b929d28b466b43aa9b00e8f2feafbeac]

The inspected discussions concern separate failures: “quantizing model: undefined symbol: __cxa_call_terminate,” “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” and “Fix a tokenizer issue while converting models without a bos_token_id defined.” They provide no explicit attribution of this DeciLM change to those reports. [source; call_aa20e039e0504de5820911480505d6f2, call_066b218ae8a74718b194c71cd0870aca, call_5b749fd6bc0548c3b165a66defe2eff1, call_d98ef688fe9945aa934fbd8add48b043]

<a id="models"></a>

## DeciLM registration and heterogeneous decoder construction

The new registry entry connects the architecture string to DeciLMConfig and DeciLMModel. Config.from_directory selects the configuration class, while Model.from_config invokes the model class stored by that configuration. [source; call_efda0deeaec04ed8bce1386143c321a8, call_bf50c63e984d4e249a8b4b930a186a94, call_006d9aaa71c14432b34cd48f176d5ea6]

DeciLMConfig reads global hidden width and query-head count, derives head dimension by integer division when absent or false-valued, and requires one block_configs entry per declared hidden layer. Each block supplies attention and ffn dictionaries rather than a single global intermediate width and KV-head count. [source; call_7abba61d0f374a1385e14ec6ba6b93e7, call_8c6fa0e6fd7c40ccbbea00c785bfa0ed, call_19f600c907c348c3825d15ff521e0177, call_21ff6934e1324cecb90189553afe3907]

A branch marked no_op creates neither its normalization nor its attention/MLP module. Present branches receive RMSNorm and are passed to TransformerBlock, whose forward method skips absent branches and applies residual additions for present ones. The new constructor always supplies a normalization for each present branch. [source; call_7abba61d0f374a1385e14ec6ba6b93e7, call_4f5d30c048f0474198e92ae08083dc2b]

The earlier optional-transformer entry describes matching allocation strategies for attention-only and MLP-only blocks. DeciLM's branch construction uses that existing interface. [ancestor; call_f874e9530c894bd4942257242a9bad74]

Checkpoint keys retain original block indices, but cache_layer_idx increments only for present attention modules. Attention.decode_flash_attn uses that dense index to retrieve KV storage. last_kv_module_idx tracks the final attention-bearing top-level module, allowing Model.prefill to stop there rather than process trailing MLP-only blocks or the output head. [source; call_7abba61d0f374a1385e14ec6ba6b93e7, call_fc652812faf94209865123fb314a1da1, call_006d9aaa71c14432b34cd48f176d5ea6]

For active FFNs, the constructor truncates 2 × ffn_mult × hidden_size / 3 to an integer and rounds that integer upward to a multiple of 256. Here 255 implements ceiling division; 256 is an alignment unit, not a dispatch threshold. [source; call_7abba61d0f374a1385e14ec6ba6b93e7]

Scalar transcription for the inspected 51B configuration produced intermediate widths 7168, 14336 and 28672 for multipliers 1.3125, 2.625 and 5.25. These equal the corresponding first-shard gate/up tensor dimensions. This checks arithmetic and metadata, not model execution. [execution; call_7f96e73bde8a462580742870120b414c, call_6857823172304b869eaaf21680d525ed, call_69378cd6036f4c6fb16be4de2719baaa]

Input preparation delegates to prepare_for_attn. Its existing alternatives remain uncached SDPA, uncached Flash Attention and cached Flash Attention; uncached preparation rejects a supplied cache, while rectangular cached preparation checks page alignment and requires exactly one of past_len or cache_seqlens. [source; call_7abba61d0f374a1385e14ec6ba6b93e7, call_fc652812faf94209865123fb314a1da1]

The implementation deliberately bounds its supported subset with assertions against active linear-replacement and sparsification branches and several sink-attention options. Reusing conventional modules keeps the integration small, but these checks are narrower than the commit message's unqualified Nemotron label. [inference; call_7abba61d0f374a1385e14ec6ba6b93e7]

## Authoring-time findings — pending review

### decilm-kv-head-mapping (suspected; defect)

Directly treating n_heads_in_group as the KV-head count disagrees with the inspected 51B checkpoint's second block.

Trigger: Construct attention for block 1 of the pinned nvidia/Llama-3_1-Nemotron-51B-Instruct configuration, where n_heads_in_group is 16, hidden_size is 8192 and num_attention_heads is 64.

Expected: Construct K/V projection dimensions matching the stored [512, 8192] tensors: four KV heads of dimension 128.

Actual: DeciLMModel passes 16 as num_kv_heads, so Attention declares K/V output width 2048 and later reshapes using 16 heads. The checkpoint header instead has width 512. The first block happens to match because both 8 and 64/8 are 8. The separate linear-replacement assertion prevents complete construction of this exact checkpoint before loading reaches the mismatch.

Locations: 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/models/decilm.py — DeciLMModel.__init__

Source evidence: call_7abba61d0f374a1385e14ec6ba6b93e7, call_fc652812faf94209865123fb314a1da1, call_6857823172304b869eaaf21680d525ed, call_69378cd6036f4c6fb16be4de2719baaa

source_inspection: Compared the constructor argument, Attention projection/reshape dimensions and pinned tensor shapes. Whole-parent searches found no pre-existing DeciLM callers; the inspected generic construction route is Model.from_config through config.model_class. [call_2ad507e8b20a4780b62791bb33cebc5c, call_ebf4fe2032fc48dcbe9ed47d3b906cd2, call_006d9aaa71c14432b34cd48f176d5ea6, call_23b81d3fb3cf4b2d9643b3898b1b1042]. Limits: Reach is established for generic model construction, not every external entry point. No tensor loading failure was executed.

scalar_transcription: Calculated head dimension 128, patch width 2048 and quotient-based width 512 for group size 16. [call_7f96e73bde8a462580742870120b414c]. Limits: Standard-library arithmetic only; no repository model or GPU kernel ran.

### nemotron-51b-linear-replacement (suspected; external_compatibility)

Registering DeciLM does not make the inspected Nemotron-51B checkpoint constructible.

Trigger: Instantiate the pinned 51B configuration through DeciLMModel with assertions enabled; block 11 has active attention with replace_with_linear=true.

Expected: For complete compatibility with this checkpoint, construct its configured linear-replacement attention branch.

Actual: The constructor raises the explicit assertion “DeciLM: replace_with_linear not supported.” This is an intentional unsupported form, not evidence that all Nemotron variants fail.

Locations: 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/models/decilm.py — DeciLMModel.__init__

Source evidence: call_7abba61d0f374a1385e14ec6ba6b93e7, call_6857823172304b869eaaf21680d525ed

source_inspection: Compared the checkpoint's active replacement branch with the constructor assertion and inspected Model.from_config's indirect constructor call. [call_7abba61d0f374a1385e14ec6ba6b93e7, call_6857823172304b869eaaf21680d525ed, call_ebf4fe2032fc48dcbe9ed47d3b906cd2, call_006d9aaa71c14432b34cd48f176d5ea6]. Limits: Constructor execution was not performed; compatibility assessment is limited to the inspected checkpoint and assertion-enabled execution.

## Uncertainty and limits

No model construction, tensor loading, conversion or GPU inference was executed. The Python check transcribed scalar dimension arithmetic only.

Reference inspection was limited to nvidia/Llama-3_1-Nemotron-51B-Instruct and its first tensor shard header. Configurations for Nemotron Ultra CPT, Ultra, Super, Qwen2.5-0.5B, TinyLlama, Phi-3, Mistral and Gemma were not read; no cross-model compatibility claim is made.

The numerical rationale for the MLP formula's factor 2/3 and the choice of 256-wide alignment is not established by the inspected sources.
