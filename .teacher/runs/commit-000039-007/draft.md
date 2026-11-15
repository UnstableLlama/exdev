# 75c7366bb2e2a7671e38d079f9e5f54945b78006


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/75c7366bb2e2a7671e38d079f9e5f54945b78006) · [Evidence ledger](draft.json)

Registers DeciLM and builds heterogeneous Nemotron-style blocks using existing inference modules; older Deci schemas and linear-replacement variants remain outside the implemented subset, and empty blocks expose a conversion hazard.

- [Compose DeciLM blocks from checkpoint configuration](#models)

## Problem

The architecture registry lacked DeciLMForCausalLM. The existing Llama builder used uniform attention and MLP dimensions, whereas the new builder consumes per-block attention and feed-forward descriptions. [source; call_24a52f35f1ca4dec876e2c5e69de9c41, call_4982f18891ac4b7bbe4c4303af535a5b, call_5b104c86da754311bb5235e4950819dc]

## Reasoning

Reusing Attention, GatedMLP and TransformerBlock makes this an architecture-composition change rather than a new inference kernel. Per-block construction permits omitted branches and varying widths while retaining existing tensor names and quantization interfaces. [inference; call_4982f18891ac4b7bbe4c4303af535a5b, call_836ff0213685478c8f2b5097446530b8, call_aa57b6ead72f49fbb686e925915ab60f]

## Impact

Config.from_directory can now select DeciLMConfig, and Model.from_config instantiates its DeciLMModel. Registration does not imply compatibility with every checkpoint advertising that architecture: block_configs is required, and linear-replacement, sparsity and sink-attention options are explicitly rejected for active branches. [source; call_24a52f35f1ca4dec876e2c5e69de9c41, call_7515d5176ffd4cc9a6e3ce71d1853a5c, call_01f09d7d21f0430ea026b1f8cc1e187d, call_4982f18891ac4b7bbe4c4303af535a5b]

## Source Notes

The earlier optional-transformer entry records missing-normalization input handling and empty-block allocation observations. [ancestor; call_eedf8e1f1320496f89ed3e06180f3c34]

The missing-normalization implementation is unchanged, but DeciLM supplies a norm for every active branch, avoiding that trigger. Empty-block allocation still divides by zero when called directly; conversion guards allocate_q with if linears, although its later bitrate calculation has a separate empty-block problem. [source; call_836ff0213685478c8f2b5097446530b8, call_cf2ee5ff3e564600bffda170f26626f0, call_ce7587ef5ac442e7977ecf07afe44277, call_4982f18891ac4b7bbe4c4303af535a5b]

Inspected discussions concern separate issues: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension/toolchain problem; #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns chat mode; #13 reports conversion without a bos_token_id; #4, “chore: update config.py,” corrects a spelling error. None supplies evidence of DeciLM validation. [source; call_22e03949acd240579a1f24693faa426c, call_5507d772a70b4a00965c79a6d5587616, call_9b8e5dae3daa4d3196676d3412990e74, call_2d67f50df68f47af8387d98706b5cc21, call_507571702b4b4d5283fef62d20e13524]

<a id="models"></a>

## Compose DeciLM blocks from checkpoint configuration

DeciLMConfig reads global hidden width, query-head count and normalization epsilon; absent or false-valued head_dim falls back to hidden_size // num_attention_heads. It accepts SiLU or an omitted activation setting, defaults untied embeddings, selects NEOX RoPE layout, and requires one block_configs entry per hidden layer. [source; call_4982f18891ac4b7bbe4c4303af535a5b, call_7515d5176ffd4cc9a6e3ce71d1853a5c]

Each block reads attention and ffn independently. no_op removes that branch and its norm. Active attention maps n_heads_in_group directly to num_kv_heads; Attention uses that value for K/V projection widths and reshaping. Active MLP width is int(2 * ffn_mult * hidden_size / 3), rounded upward to a multiple of 256 using +255 before integer division. [source; call_4982f18891ac4b7bbe4c4303af535a5b, call_aa57b6ead72f49fbb686e925915ab60f]

Checkpoint layer indices remain in tensor keys even when attention is absent. A separate cache_layer_idx advances only for active attention; last_kv_module_idx records the last containing module. This matches Attention's cache.get_layer(layer_idx) access and Model.prefill's stop-at-last-KV behavior. [source; call_4982f18891ac4b7bbe4c4303af535a5b, call_aa57b6ead72f49fbb686e925915ab60f, call_01f09d7d21f0430ea026b1f8cc1e187d]

The model retains embedding → transformer blocks → final RMSNorm → logits Linear ordering. prepare_inputs stores input_ids and delegates attention preparation. The existing helper defaults to uncached Flash Attention, rejects caches for uncached modes, and prepares page tables and sequence lengths for cached Flash Attention. [source; call_4982f18891ac4b7bbe4c4303af535a5b, call_aa57b6ead72f49fbb686e925915ab60f]

The pinned configurations for Deci/DeciCoder-6B, Deci/DeciLM-6b, Deci/DeciLM-6b-instruct, Deci/DeciLM-7B and Deci/DeciLM-7B-instruct use num_key_value_heads_per_layer rather than block_configs. Deci/DeciLM-7B-instruct-GGUF instead declares a global KV-head count and also lacks block_configs. All six share the registered architecture string but do not supply the required new block schema. [source; call_7ace340683e94a2d90915281d9de9c4e, call_5dc21567543d4fe48389a75203f0f274, call_9b451de06fed4950819ab31c952ddfda, call_08149e626dbf4b74b07d0f710430569d, call_3bb25a14eb8f47609862e34d4c4285f5, call_017d5dddfb234053b48ba59ca8768604, call_4982f18891ac4b7bbe4c4303af535a5b]

nvidia/Llama-3_1-Nemotron-51B-Instruct supplies block_configs, hidden_size 8192 and 64 query heads, but includes active attention with replace_with_linear=true, which the new constructor rejects. Its configuration therefore falls outside the implemented subset. [source; call_81ecfa9c801f46c2b68ea154cfbeb659, call_4982f18891ac4b7bbe4c4303af535a5b]

nvidia/Llama-3_3-Nemotron-Super-49B-v1 supplies the expected block schema, 8192 hidden width, 64 query heads, eight KV heads on active attention, and attention-only omissions. nvidia/Llama-3_1-Nemotron-Ultra-253B-CPT-v1 and nvidia/Llama-3_1-Nemotron-Ultra-253B-v1 each supply 16384 hidden width, 128 query heads, sixteen KV heads on active attention, and fully omitted blocks as well as attention-only omissions. Each explicitly uses SiLU and untied embeddings; these configuration values fit the builder's corresponding mappings, subject to the empty-block conversion observation. [source; call_60cd332ceddf4de0aeda9b9e6371c468, call_84ab557e901849ac916093bbb60a2210, call_efaf593c692347e58ea3a4fa3ed91195, call_92e12e56cf0c449e985d3687bc303361, call_f8a56c4e21ad43bfb5b61c7f7140bac2, call_4982f18891ac4b7bbe4c4303af535a5b]

A standard-library scalar check yields head_dim=128 for the inspected 4096/32, 8192/64 and 16384/128 configurations. At hidden width 8192, ffn_mult values 0.5, 1 and 5.25 produce widths 2816, 5632 and 28672; at 16384, values 0.4875 and 39 produce 5376 and 425984. These are arithmetic results, not checkpoint or kernel tests. [execution; call_53414cc7d7e64d01abab1de1f228189e]

## Authoring-time findings — pending review

### empty-block-conversion-bitrate (suspected; defect)

The new builder retains fully empty transformer blocks, exposing an unguarded conversion bitrate division.

Trigger: Convert a block with both attention.no_op and ffn.no_op true, as present in both inspected Nemotron Ultra configurations, and reach the post-save bitrate calculation.

Expected: A parameterless identity block should be skipped or reported without dividing by its weight count.

Actual: No submodules are registered, so weights_numel() returns zero. Conversion skips allocate_q but subsequently evaluates num_bits / module.weights_numel(), which divides by zero if the preceding save completes.

Locations: 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/models/decilm.py — DeciLMModel.__init__, 29060addb5a3994cec3867e1f2f6b30ecda7b8a3:exllamav3/conversion/convert_model.py — main

Source evidence: call_4982f18891ac4b7bbe4c4303af535a5b, call_f11f02ec43a0433d9ddb9c5fe019f082, call_ce7587ef5ac442e7977ecf07afe44277, call_84ab557e901849ac916093bbb60a2210, call_92e12e56cf0c449e985d3687bc303361

source_inspection: Traced empty-block construction, None-filtering registration and weight summation into conversion. Whole-parent import search located convert.py as the direct CLI entry calling main; this observation concerns conversion, not every inference workflow. [call_836ff0213685478c8f2b5097446530b8, call_f11f02ec43a0433d9ddb9c5fe019f082, call_999fa0b2eb5d414cbcbf4978a24d90ee, call_c1092a059fee42fcbbe65ba2697dc4f3, call_ce7587ef5ac442e7977ecf07afe44277]. Limits: No end-to-end conversion or empty-tensor serialization was executed; an earlier failure is not excluded.

scalar_transcription: Evaluated the zero-weight division with standard-library Python and observed ZeroDivisionError. [call_53414cc7d7e64d01abab1de1f228189e]. Limits: This models the arithmetic only and does not execute the converter.

## Uncertainty and limits

No model loading, conversion, tensor inference or GPU execution was performed. Scalar checks reproduce Python dimension arithmetic only.

Configuration compatibility is not tensor-shape or numerical-equivalence validation; checkpoint tensor headers were not inspected.

The code establishes the two-thirds MLP-width transformation and 256-element rounding, but the architectural rationale for those choices is not established by the inspected evidence.
