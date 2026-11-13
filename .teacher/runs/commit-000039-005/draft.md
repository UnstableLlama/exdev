# 75c7366bb2e2a7671e38d079f9e5f54945b78006


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/75c7366bb2e2a7671e38d079f9e5f54945b78006) · [Evidence ledger](draft.json)

Adds configurable DeciLM blocks and architecture dispatch, but inspected Nemotron checkpoints reveal incomplete compatibility: 51B rejects linear-replacement attention, Ultra KV dimensions disagree with headers, and fully disabled blocks encounter an unchanged conversion hazard.

- [DeciLM construction and checkpoint compatibility](#models)

## Problem

The change registers DeciLMForCausalLM and adds a constructor driven by per-block attention and feed-forward configurations rather than a uniform decoder layout. [source; call_63b54f15c0d8489a9c45badc35ce142e, call_c5d0364ee0a64baaba7114827c87aef3]

## Reasoning

Reusing Attention, GatedMLP and TransformerBlock limits the implementation to existing execution primitives. Unsupported linear replacements, sparsification and sink-attention features are explicitly rejected rather than approximated. [source; call_c5d0364ee0a64baaba7114827c87aef3, call_fd0f1ddc49674a0895a5099a01e16b90, call_ae3b56f347d0457eb0e4d5eb17c12e0b]

## Impact

Architecture registration is not equivalent to compatibility with every Nemotron checkpoint: the inspected models expose an explicit rejection, attention-shape mismatches and an empty-block conversion hazard. [inference; call_c5d0364ee0a64baaba7114827c87aef3, call_83ce6c54f13141e6b5729af06dc5dec6, call_13b10fedd3c84467862141aa2f805975, call_7edad7394eda4c4c93a88938bf9ab62d, call_dff116790edc47c99208460af0fd7e8f]

## Source Notes

The discussions inspected concern other failures: issue 7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure; issue 12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports a chat-mode problem after conversion; PR 13, “Fix a tokenizer issue while converting models without a bos_token_id defined,” reports missing-BOS handling. None supplies evidence of successful DeciLM execution. [source; call_e47cc2dce31f4429aea08c8214614aa5, call_6fe98d36427a4214aacca15e74e410c7, call_202ddf8ecc4d43089a38d05b9f96358f, call_66310e9c191241ceba655d3f24327d22]

<a id="models"></a>

## DeciLM construction and checkpoint compatibility

DeciLMConfig reads hidden size, query-head count, normalization epsilon and block_configs, checks the block-list length against num_hidden_layers, requires SiLU and defaults missing head_dim to hidden_size // num_attention_heads. The model constructs embedding, indexed transformer blocks, final RMSNorm and an output projection, with an embedding fallback for a tied output head. [source; call_c5d0364ee0a64baaba7114827c87aef3]

Each no_op branch becomes None together with its normalization. Present branches receive RMSNorm, so this constructor does not exercise TransformerBlock's uninitialized-y path for a present branch without an input norm. Both-disabled blocks remain in the module list and their forward method returns the input through dtype conversion. [source; call_c5d0364ee0a64baaba7114827c87aef3, call_fd0f1ddc49674a0895a5099a01e16b90]

Checkpoint keys retain the original block index, while cache_layer_idx increments only for active attention. last_kv_module_idx records the final attention-bearing module, matching Model.prefill's stopping condition. prepare_inputs delegates attention-mode preparation to prepare_for_attn. [source; call_c5d0364ee0a64baaba7114827c87aef3, call_d6b8a76c67874e9a961d4f19ff47a08c, call_2ef6e78ff43543d6bdf05902018fa316]

For an active MLP, the constructor truncates 2 * ffn_mult * hidden_size / 3 to an integer, then rounds upward to a multiple of 256 using an added 255. GatedMLP declares up/gate weights of shape [intermediate, hidden] and down weights of shape [hidden, intermediate]. Attention declares K/V output widths as num_kv_heads * head_dim, with n_heads_in_group passed directly as num_kv_heads. [source; call_c5d0364ee0a64baaba7114827c87aef3, call_ae3b56f347d0457eb0e4d5eb17c12e0b, call_2ef6e78ff43543d6bdf05902018fa316]

nvidia/Llama-3_1-Nemotron-51B-Instruct config declares hidden_size 8192, 64 query heads and 80 blocks. Block 0 has n_heads_in_group=8 and ffn_mult=1.3125: declared Q/O [8192,8192], K/V [1024,8192], up/gate [7168,8192] and down [8192,7168] match its first-shard header. Block 1 instead stores K/V [512,8192], whereas its n_heads_in_group=16 declares [2048,8192]. The explicit feature assertions first reject block 11 for attention replace_with_linear=true. No block disables both branches. [source; call_bcbc00a8bc1a4e7caff8ecd8a73f01ea, call_83ce6c54f13141e6b5729af06dc5dec6, call_c5d0364ee0a64baaba7114827c87aef3, call_2ef6e78ff43543d6bdf05902018fa316]

nvidia/Llama-3_1-Nemotron-Ultra-253B-CPT-v1 declares hidden_size 16384, 128 query heads and 162 blocks. Its configuration passes the added feature assertions; there is no first rejected block. For block 0, n_heads_in_group=16 and ffn_mult=0.4875 declare Q/O [16384,16384], K/V [2048,16384], up/gate [5376,16384] and down [16384,5376]. The first-shard header agrees except that K/V are [1024,16384]. Both branches are disabled beginning at block 9. [source; call_1ee5cab1691449698564cf2078aaaf60, call_bee34d3db0c44730852a9380ef69163e, call_13b10fedd3c84467862141aa2f805975, call_c5d0364ee0a64baaba7114827c87aef3, call_2ef6e78ff43543d6bdf05902018fa316]

nvidia/Llama-3_1-Nemotron-Ultra-253B-v1 separately declares hidden_size 16384, 128 query heads and 162 blocks, and passes the added feature assertions without a rejected block. Block 0 has the same constructor dimensions as CPT. Headers from shards 1 and 2 agree with Q/O [16384,16384], up/gate [5376,16384] and down [16384,5376], but store K/V [1024,16384] rather than declared [2048,16384]. It also contains fully disabled blocks beginning at block 9. [source; call_94f2544e765c49d6b97a743487f8199b, call_d28c84a3954d4ef792a4ebd0a13d008f, call_a2675b2ec5db4464830934bc78faac67, call_7edad7394eda4c4c93a88938bf9ab62d, call_c5d0364ee0a64baaba7114827c87aef3]

nvidia/Llama-3_3-Nemotron-Super-49B-v1 declares hidden_size 8192, 64 query heads and 80 blocks. It passes the added feature assertions without a rejected block and has no fully disabled block. Block 0 has n_heads_in_group=8 and ffn_mult=2.625; declared Q/O [8192,8192], K/V [1024,8192], up/gate [14336,8192] and down [8192,14336] match its first-shard header. [source; call_7282c37ed5374e6f888036173aa33b00, call_3c50db0f3fcb4a58b4290ca6b0eeefec, call_c5d0364ee0a64baaba7114827c87aef3]

All four inspected configurations omit head_dim, yielding 128 under the fallback, specify SiLU and disable tied embeddings. A scalar transcription reproduced the selected MLP widths and K/V mismatches; notably Ultra block 0 truncates to 5324 and rounds to 5376. [execution; call_2be6e26fa2ff413da3f458067ce3492a]

For either Ultra model's fully disabled blocks, the parent converter skips calibration capture and allocation because there are no qmaps or Linear targets, but does not skip the module itself. It gathers an empty tensor dictionary, attempts to save it and then divides its byte count by weights_numel(), which is zero. This path does not arise from fully disabled blocks in the inspected 51B or Super configurations. [source; call_dff116790edc47c99208460af0fd7e8f, call_a593c9a6e07b45128b75c510d2ac351a, call_fd0f1ddc49674a0895a5099a01e16b90, call_1ee5cab1691449698564cf2078aaaf60, call_94f2544e765c49d6b97a743487f8199b, call_bcbc00a8bc1a4e7caff8ecd8a73f01ea, call_7282c37ed5374e6f888036173aa33b00]

## Authoring-time findings — pending review

### kv-head-mapping (suspected; defect)

Directly treating n_heads_in_group as the KV-head count produces projection declarations inconsistent with inspected checkpoint headers.

Trigger: Construct either inspected Ultra model, or block 1 of the inspected 51B model.

Expected: Declared K/V projection widths should match the checkpoint: 1024 for Ultra block 0 and 512 for 51B block 1.

Actual: The constructor declares width 2048 in all three cases. Model.from_config dispatches to the new constructor; conversion reaches it through get_base_model. No checkpoint execution was performed.

Locations: 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/models/decilm.py — DeciLMModel.__init__

Source evidence: call_c5d0364ee0a64baaba7114827c87aef3, call_2ef6e78ff43543d6bdf05902018fa316, call_83ce6c54f13141e6b5729af06dc5dec6, call_13b10fedd3c84467862141aa2f805975, call_7edad7394eda4c4c93a88938bf9ab62d, call_b9160930c60542b5aafef2bb680a6459, call_d6b8a76c67874e9a961d4f19ff47a08c, call_dff116790edc47c99208460af0fd7e8f

scalar_transcription: Computed head dimensions and declared K/V widths from transcribed configuration values and constructor expressions. [call_2be6e26fa2ff413da3f458067ce3492a]. Limits: Checks integer dimensions only, not model loading or attention execution.

### empty-block-conversion (suspected; defect)

Fully disabled blocks expose an unguarded zero-weight denominator in the unchanged converter.

Trigger: Conversion reaches a fully disabled Ultra block, first present at block 9, and saving its empty tensor dictionary returns normally.

Expected: Skip weight-based bitrate reporting or handle a zero-weight identity module without division.

Actual: main evaluates num_bits / module.weights_numel() with denominator zero before advancing calibration state. The inspected direct CLI caller is convert.py; earlier loading problems may prevent reaching this point.

Locations: 29060addb5a3994cec3867e1f2f6b30ecda7b8a3:exllamav3/conversion/convert_model.py — main, 75c7366bb2e2a7671e38d079f9e5f54945b78006:exllamav3/models/decilm.py — DeciLMModel.__init__

Source evidence: call_dff116790edc47c99208460af0fd7e8f, call_a593c9a6e07b45128b75c510d2ac351a, call_c5d0364ee0a64baaba7114827c87aef3, call_4794508a2f124cf28de9ddc25567e9d3, call_655deb56aa8d450e95440f204cd5f87f

scalar_transcription: Evaluated the modeled empty-module bitrate expression 0 / sum([]), which raised ZeroDivisionError. [call_2be6e26fa2ff413da3f458067ce3492a]. Limits: Did not execute the converter, tensor serialization or GPU operations.

## Uncertainty and limits

No checkpoint loading, conversion, inference or GPU execution was performed. The Python check transcribed dimension arithmetic and an empty-denominator expression only.

Tensor comparisons cover selected active blocks, not every tensor in each checkpoint.

Empty-block serialization through safetensors was not executed; the division-by-zero observation applies if serialization returns normally.

The factor 2/3 and 256-wide MLP alignment are explicit constructor rules; their architectural or hardware rationale is not established by the inspected evidence.
