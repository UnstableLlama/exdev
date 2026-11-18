# d42d6238d88151eb837bdf709836d8726759fbd7


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d42d6238d88151eb837bdf709836d8726759fbd7) · [Evidence ledger](draft.json)

Registers SmolLM3 using shared Llama-style modules and selective per-layer RoPE. Reference tensor layouts match, but the inspected Base configuration lacks the required RoPE mask.

- [SmolLM3 dispatch, checkpoint mapping and selective RoPE](#models)

## Problem

SmolLM3ForCausalLM was absent from architecture dispatch. The parent tree already contained a SmolLM3 chat template, but not its model implementation. [source; call_54af2f3e3a6545ffbd65976df71180f0, call_555d1f4a9d7b40d6b1ec169ebb856a68, call_854643e6144347a1a004f9535cfe8163]

## Reasoning

The implementation closely follows Llama's shared-module construction while adding per-layer RoPE selection, full-attention validation and a default of tied embeddings. Registration and construction are coupled: the registry selects SmolLM3Config, which supplies SmolLM3Model as its text component. [source; call_cd60d9847d264006a1c5f28ff62cc28f, call_9d2f146ecdb04f65b7edfba488fe8e25, call_54af2f3e3a6545ffbd65976df71180f0, call_6b04a3fc891c4f578a4bf54851a61714, call_88df3e7ca56a4bffb05faf7ed4bb95d1]

## Impact

The new mapping matches the inspected SmolLM3-3B checkpoint's tensor names and dimensions. Compatibility is narrower than the architecture name suggests: the inspected SmolLM3-3B-Base configuration lacks the newly required no_rope_layers list. [source; call_9d2f146ecdb04f65b7edfba488fe8e25, call_6c86702924d24da2bc1c93994d6d6ac3, call_c80ac6eec258419c8304a67981a20ad5, call_f74e5291ed424bc18347b8dc54c52834, call_fd2d104fa94a478e90b175e33d41eeba]

## Source Notes

The root models entry was read for the Llama construction this implementation follows. It describes shared projection mappings, embedding-head fallback and attention preparation, and records sliding-window mapping gaps in other architectures. The parent chat entry was also read; it establishes that the earlier SmolLM3 edit supplied application-side prompting rather than architecture support. [ancestor; call_11efc444a5d94165b10dc7a7d13f06f8, call_405a3954b412428fa0fad62dfaacd54e]

The inherited sliding-window concern does not establish a SmolLM3 mismatch here: the inspected configurations disable sliding windows, and this constructor leaves Attention's window at its unrestricted default. [source; call_9d2f146ecdb04f65b7edfba488fe8e25, call_f6845af682664b7291b26c861c3d50d7, call_6c86702924d24da2bc1c93994d6d6ac3, call_c80ac6eec258419c8304a67981a20ad5, call_c7e7b694a6164e928676caaaf9253189]

Inspected discussions retain separate framing: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension/toolchain import failure; #33, “Error converting model,” reports a file-opening failure; #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports a vocabulary-width mismatch; and #55, “Possible GLM4 32B regression,” reports an int/None comparison in fused-weight loading. Their relationship to this task is only inferred shared infrastructure or source paths, not evidence that this architecture addition fixes them. [inference; call_b9f8cf9458e7407aa8e3da399a3795ff, call_ff070408b9164a7b83a6ef042348751f, call_e98ec16f73644854a2901e71536aa66c, call_fc407fe4c364492d965bbbff34286dbd, call_9d2f146ecdb04f65b7edfba488fe8e25]

Other inspected reports concern quantization failures: #34, “torch._C._LinAlgError on last layer of quant”; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values”; #52, “Error converting moonshotai/Kimi-Dev-72B”; #53, “Command A support,” whose discussion includes conversion failures; and #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT.” Any task connection is inferred from shared Linear/MLP paths. In particular, #52 recommends FP32 MLP outputs, which the new constructor requests, but this does not establish a SmolLM3-specific motivation or numerical result. [inference; call_502d8116d34f4fc29004292bdb549b2f, call_ee0c2143d5494228a9c089019a2e34fe, call_9a7a680f2df64a5a8e2dd4d517c8ce90, call_6e1d8b2fb7d942af9f47f116db8ae7ac, call_448a2e50c4024838b3d522b8b187ec19, call_1494b14b127843c98b89158145beb57a, call_9d2f146ecdb04f65b7edfba488fe8e25]

<a id="models"></a>

## SmolLM3 dispatch, checkpoint mapping and selective RoPE

Config.from_directory dispatches on the single architectures entry, not model_type. Adding SmolLM3Model to ARCHITECTURES makes SmolLM3ForCausalLM select SmolLM3Config; Model.from_config subsequently selects its text component. Existing architecture entries remain unchanged. [source; call_54af2f3e3a6545ffbd65976df71180f0, call_6b04a3fc891c4f578a4bf54851a61714, call_88df3e7ca56a4bffb05faf7ed4bb95d1]

SmolLM3Config derives absent head_dim from hidden_size divided by query-head count, defaults KV heads to query heads, accepts only SiLU when hidden_act is supplied, and requires intermediate width, RMS epsilon and layer count. Optional layer_types must contain only full_attention. Unlike LlamaConfig, tied embeddings default to true. Whole-parent searches found no existing no_rope or layer_types consumers; the new list is consumed directly by the new model constructor. [source; call_9d2f146ecdb04f65b7edfba488fe8e25, call_cd60d9847d264006a1c5f28ff62cc28f, call_7da1cc2299f04acdb47528ef81e5c2d9, call_146a5547218e495caedb6c19d8363c8e, call_5de72cabb4b841678112733a0eee5f62]

The model builds embedding → repeated pre-norm attention/residual and pre-norm gated-MLP/residual blocks → final RMSNorm → vocabulary projection. It preserves the usual q_proj/k_proj/v_proj/o_proj and gate_proj/up_proj/down_proj names and quantization-map groups. GatedMLP receives explicit FP16 gate/up intermediates and FP32 down outputs; the final norm emits FP16. These are runtime precision requests, distinct from checkpoint storage dtype. [source; call_9d2f146ecdb04f65b7edfba488fe8e25, call_f6845af682664b7291b26c861c3d50d7, call_c4927ef157154784ba58736eed147bf7, call_854643e6144347a1a004f9535cfe8163]

Despite its name, no_rope_layers enables RoPE where an element equals 1 and passes None elsewhere. Attention.load constructs RoPE only for nonempty settings, and all three inspected decode paths condition rotation on self.rope. Thus None removes rotation, not attention or KV caching. The supplied 3B and ONNX configurations use [1,1,1,0] repeated across 36 layers; the constructor uses this list rather than deriving it from no_rope_layer_interval=4. NEOX-style settings retain theta=5,000,000 and the configured 65,536-position limit. [source; call_9d2f146ecdb04f65b7edfba488fe8e25, call_f6845af682664b7291b26c861c3d50d7, call_6b04a3fc891c4f578a4bf54851a61714, call_6c86702924d24da2bc1c93994d6d6ac3, call_c7e7b694a6164e928676caaaf9253189]

Model by model: HuggingFaceTB/SmolLM3-3B supplies the required mask and full-attention list, with tied embeddings selected by default; HuggingFaceTB/SmolLM3-3B-ONNX has the same relevant dimensions and mask; HuggingFaceTB/SmolLM3-3B-Base has the same dimensions and explicitly tied embeddings but supplies only the interval, so it fails the required mask read. All three specify hidden width 2048, 16 query heads, four KV heads, intermediate width 11008, 36 layers, RMS epsilon 1e-6 and vocabulary size 128256. [source; call_6c86702924d24da2bc1c93994d6d6ac3, call_c7e7b694a6164e928676caaaf9253189, call_c80ac6eec258419c8304a67981a20ad5, call_9d2f146ecdb04f65b7edfba488fe8e25, call_20cbe54d352640f4bc9d094a2395675f]

Both complete two-shard headers were inspected for 3B and Base. Each contains embedding [128256,2048], Q/O [2048,2048], K/V [512,2048], gate/up [11008,2048], down [2048,11008], two [2048] norms per layer and final [2048] norm. All 326 stored tensors belong to the requested layout; no extra stored tensors remain unused. Neither checkpoint contains lm_head.weight, projection biases, weight_scale_inv or EXL3 tensor groups. Linear therefore uses ordinary weights, optional bias/scales remain absent, and the head can fall back to model.embed_tokens.weight. Base's matching header does not remove its earlier configuration failure. [source; call_f74e5291ed424bc18347b8dc54c52834, call_fd2d104fa94a478e90b175e33d41eeba, call_14602e5d264140578cb098b36a96013a, call_5a43def925924d3bb9b51edc31d0e2c5, call_cbc1ed777b164d1e87d1a2f422fc72a7, call_854643e6144347a1a004f9535cfe8163, call_9d2f146ecdb04f65b7edfba488fe8e25]

A bounded Python metadata calculation derives head width 128, four query heads per KV head, 27 rotated layers and nine unrotated layers at zero-based indices 3,7,11,15,19,23,27,31,35. It also reproduces the projection dimensions and 36×9+2=326 stored-tensor count; the relevant dimensions are all divisible by Linear's 128-element padding unit. This is scalar arithmetic, not tensor or kernel execution. [execution; call_7db7a203d59f49c5b6507b3b3fe08de0]

prepare_inputs preserves input_ids in params before calling prepare_for_attn, exactly like all 15 existing model call sites found and inspected. It adds no missing caller-side guard: cache exclusion and cached-attention preparation remain in the shared helper. default_chat_prompt separately emits an optional system turn, one user turn and an open ChatML assistant prefix; it supplies neither the chat example's reasoning-dependent defaults nor an explicit BOS string. [source; call_edc701885c9d47b584a739f293bdb817, call_88df3e7ca56a4bffb05faf7ed4bb95d1, call_f6845af682664b7291b26c861c3d50d7, call_9d2f146ecdb04f65b7edfba488fe8e25]

## Authoring-time findings — pending review

### base-config-missing-rope-mask (suspected; external_compatibility)

The registered SmolLM3 configuration cannot consume the inspected SmolLM3-3B-Base config unchanged.

Trigger: Select HuggingFaceTB/SmolLM3-3B-Base at the inspected revision through Config.from_directory, with its valid checkpoint files available.

Expected: Construct the architecture configuration using its interval-based RoPE description, or otherwise support this reference variant.

Actual: SmolLM3Config requires no_rope_layers with no_default. Base supplies no_rope_layer_interval=4 but no list, so read_dict raises ValueError before model construction. The factory passes the directory unchanged and provides no interval-to-list adaptation. The reach is configuration selection for this variant, not every existing factory caller or every SmolLM3 checkpoint.

Locations: d42d6238d88151eb837bdf709836d8726759fbd7:exllamav3/models/smollm3.py — SmolLM3Config.__init__

Source evidence: call_9d2f146ecdb04f65b7edfba488fe8e25, call_c80ac6eec258419c8304a67981a20ad5, call_6b04a3fc891c4f578a4bf54851a61714, call_20cbe54d352640f4bc9d094a2395675f, call_61938eb1b75046f395ba8da6e90daa12, call_555d1f4a9d7b40d6b1ec169ebb856a68

source_inspection: Compared all three reference configs with the task constructor and inspected the generic factory and typed-key reader. Whole-parent searches found no pre-existing SmolLM3 config builder or no_rope adaptation. [call_6c86702924d24da2bc1c93994d6d6ac3, call_c80ac6eec258419c8304a67981a20ad5, call_c7e7b694a6164e928676caaaf9253189, call_9d2f146ecdb04f65b7edfba488fe8e25, call_7da1cc2299f04acdb47528ef81e5c2d9, call_6b04a3fc891c4f578a4bf54851a61714, call_20cbe54d352640f4bc9d094a2395675f]. Limits: Full configuration initialization and checkpoint loading were not executed.

repository_execution: Executed the parent repository's extracted read_dict body in isolation with the missing-list condition and no_default sentinel; it raised ValueError naming no_rope_layers. [call_7db7a203d59f49c5b6507b3b3fe08de0]. Limits: Annotations were removed for isolated standard-library execution; this tests the helper, not the patched model.

## Uncertainty and limits

No complete patched model, GPU inference, conversion, output-equivalence test or performance benchmark was executed.

Tensor headers establish names, dimensions and stored BF16 dtype, not numerical equivalence or successful loading.

SmolLM3-3B-ONNX was checked only at the configuration boundary; ONNX artifact execution is not established.

The isolated read_dict check does not execute SmolLM3Config initialization, filesystem loading or attention kernels.
