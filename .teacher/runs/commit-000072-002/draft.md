# c44e56c73b2c67eee087c7195c9093520494d3bf


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c44e56c73b2c67eee087c7195c9093520494d3bf) · [Evidence ledger](draft.json)

Adds GLM4 dispatch and a four-norm decoder using existing attention and MLP primitives, partial GPTJ RoPE and selected FP32 outputs. Six model configurations were checked; native partial-RoPE bounds remain a suspected inherited concern.

- [GLM4 construction, precision and rotary integration](#models)

## Problem

Glm4ForCausalLM lacked architecture dispatch. The change registers Glm4Config and Glm4Model and supplies the model constructor. [source; call_681cb7cb0a4543188dff5bf4483cd8c9, call_1c9251074c7444a4ad28297bfad13f5b]

## Reasoning

The implementation composes existing attention, normalization and gated-MLP primitives rather than adding GLM-specific kernels. Its distinguishing choices are four norms per block, GPTJ rotary pairing and selected FP32 branch outputs. [source; call_1c9251074c7444a4ad28297bfad13f5b, call_05df257ecec64e2c9b1b5cc49ec98da4]

## Impact

Config.from_directory can now select GLM4 instead of rejecting its architecture string. Registration alone does not establish successful checkpoint loading or inference. [source; call_f326325ed085407f8eb9615e83498b1b, call_681cb7cb0a4543188dff5bf4483cd8c9]

## Source Notes

Issue 7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension-import failure and a reporter-supplied environment workaround. Issue 15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns Qwen quantization. Neither discussion establishes GLM4 compatibility or motivation for this change. [source; call_710ccfbfb5f143e09d55a3f36f11219d, call_13b13d0b873f4c5abf756bcfcdcfb711]

<a id="models"></a>

## GLM4 construction, precision and rotary integration

Glm4Config requires hidden size, query-head count, intermediate width, normalization epsilon and layer count. Missing KV-head count defaults to query-head count; missing or false-valued head_dim falls back to hidden_size // num_attention_heads. hidden_act may be absent, but if present must be silu. Tied embeddings default to false. [source; call_1c9251074c7444a4ad28297bfad13f5b, call_f326325ed085407f8eb9615e83498b1b]

The module sequence is model.embed_tokens, indexed transformer blocks, model.norm and lm_head. Each block maps separate q_proj/k_proj/v_proj/o_proj attention weights and up_proj/gate_proj/down_proj MLP weights, with gate_up_proj as a fused-weight fallback. A tied head can fall back to model.embed_tokens when the constructor's lm_head presence check fails. [source; call_1c9251074c7444a4ad28297bfad13f5b, call_29acc0f0da8749939ee5db438279406e, call_62c5ccb2fcea41a9b4f1d3f795a624fc]

TransformerBlock applies input_layernorm before attention and post_self_attn_layernorm before its residual addition; post_attention_layernorm precedes the MLP and post_mlp_layernorm precedes its residual addition. GLM4 requests FP32 post-norm outputs and MLP output, while retaining FP16 gate/up intermediates and final model.norm output. Residual additions remain in-place on x; the constructor does not itself request an FP32 residual stream. [source; call_1c9251074c7444a4ad28297bfad13f5b, call_05df257ecec64e2c9b1b5cc49ec98da4, call_29acc0f0da8749939ee5db438279406e]

The fused MLP fallback interprets rows [0, intermediate_size) as gate weights and the following equally sized range as up weights. GatedMLP forbids combining that fallback with intermediate slicing. Both inspected GLM4 widths, 23040 and 13696, are below the existing 55296 slicing limit, whose source comment identifies single-GPU quantization capacity as its purpose. [source; call_29acc0f0da8749939ee5db438279406e, call_7bc351c0ac8c444c9cba9fc39c88d8fb, call_100b148f9e374c82958469624aebeafa, call_cb3e9c8a8f224a089d5fccb52896a7e1]

GLM4 selects GPTJ RoPE. The native implementation rotates adjacent channel pairs, whereas the NEOX alternative pairs channels across halves of the rotary region. The shared configuration reader supplies rope_theta, optional scaling and partial_rotary_factor; the default frequency builder uses int(head_dim * partial_rotary_factor) rotary dimensions. [source; call_1c9251074c7444a4ad28297bfad13f5b, call_f326325ed085407f8eb9615e83498b1b, call_28b4205dec974a7c8078b9516b2ba157, call_10e0289e524f4faebbc1413c94c2d931]

prepare_inputs saves input_ids in params and delegates to prepare_for_attn. Its default is uncached Flash Attention; uncached SDPA is another existing option, while cached Flash Attention requires cache metadata. All three attention implementations call native RoPE.apply, not the Torch rotary alternative. [source; call_1c9251074c7444a4ad28297bfad13f5b, call_6e81a1b44d8245dd9c88cdd145f6871b]

zai-org/GLM-4-32B-0414, zai-org/GLM-4-32B-Base-0414 and zai-org/GLM-Z1-32B-0414 each declare Glm4ForCausalLM, hidden size 6144, 61 layers, intermediate width 23040, 48 query heads and 2 KV heads. Each supplies head_dim=128, SiLU and untied embeddings, so the corresponding constructor fallbacks are unused. [source; call_100b148f9e374c82958469624aebeafa, call_e7004ab8c73b41f08797ac8c8c4009e5, call_dddbd67ce0794465b67d2a503052149f]

zai-org/GLM-4-9B-0414 and zai-org/GLM-Z1-9B-0414 each declare the same architecture with hidden size 4096, 40 layers, intermediate width 13696, 32 query heads and 2 KV heads. Both explicitly supply head_dim=128, SiLU and untied embeddings. Their attention_bias=true differs from the inspected 32B variants; Linear loads optional bias tensors by their presence rather than consulting that configuration flag. [source; call_cb3e9c8a8f224a089d5fccb52896a7e1, call_8f8f1a9ce81440cbaf6fc13236c0e489, call_62c5ccb2fcea41a9b4f1d3f795a624fc]

zai-org/GLM-Z1-Rumination-32B-0414 also uses the new architecture mapping, hidden size 6144, 61 layers and intermediate width 23040, but specifies 8 KV heads and max_position_embeddings=131072 rather than 2 and 32768. It explicitly supplies head_dim=128, SiLU and untied embeddings. All six configurations specify partial_rotary_factor=0.5, rope_theta=10000, rms_norm_eps=1e-5 and vocabulary size 151552. [source; call_3d7f06896f82458e9e8fa8f4baaf2fbb, call_100b148f9e374c82958469624aebeafa, call_e7004ab8c73b41f08797ac8c8c4009e5, call_dddbd67ce0794465b67d2a503052149f, call_cb3e9c8a8f224a089d5fccb52896a7e1, call_8f8f1a9ce81440cbaf6fc13236c0e489]

A standard-library scalar transcription gives Q/KV output widths of 6144/256 for the ordinary 32B configurations, 4096/256 for 9B and 6144/1024 for Rumination. Their query-to-KV head ratios are respectively 24, 16 and 6. The shared rotary settings produce 64 rotated channels and 32 frequencies; the native launch has 64 x-threads. [execution; call_8561102475d14ee4ac2151e783486b0a]

## Authoring-time findings — pending review

### partial-rope-frequency-load (suspected; defect)

The newly selected partial GPTJ path encounters an inherited source-level frequency bounds concern.

Trigger: Native RoPE runs with the inspected GLM4 settings head_dim=128 and partial_rotary_factor=0.5.

Expected: Only threads rotating the first 64 channels should read the 32-element inverse-frequency tensor; remaining threads should copy channels without reading it.

Actual: rope_kernel unconditionally evaluates inv_freq[threadIdx.x] before testing the partial rotary boundary. The launch spans indices 0–63 although the tensor has 32 elements. This code is unchanged by the task. Whole-parent searches locate RoPE.apply as the Python native caller and all three Attention decode methods as its callers, so the concern reaches GLM4's default and alternative attention modes if execution reaches RoPE. A runtime fault is not established.

Locations: e9a3b6a9256fc59f888b80a7d4a58883954b39de:exllamav3/exllamav3_ext/rope.cu — rope_kernel, c44e56c73b2c67eee087c7195c9093520494d3bf:exllamav3/models/glm4.py — Glm4Config.__init__

Source evidence: call_10e0289e524f4faebbc1413c94c2d931, call_28b4205dec974a7c8078b9516b2ba157, call_1c9251074c7444a4ad28297bfad13f5b, call_14862b5a245c4337b78d6b7f50a13b7f, call_5f66387bb5fa4460b04492ae2150b992, call_6e81a1b44d8245dd9c88cdd145f6871b

scalar_transcription: Modeled the inspected frequency count and launch width: 32 of 64 x-thread indices exceed the frequency tensor's logical bounds, covering indices 32–63. [call_8561102475d14ee4ac2151e783486b0a]. Limits: Integer indexing model only; no CUDA execution or compiler-output inspection. Copy-only threads do not use the computed trigonometric values.

## Uncertainty and limits

No checkpoint loading, conversion, model inference or GPU kernel execution was performed. Scalar checks covered dimensions and source-level indexing only.

All six indexed GLM4 configurations were inspected, but tensor headers were not; checkpoint key and tensor-shape compatibility remains unverified.

The numerical benefit of the FP32 branch outputs was not measured. CUDA compilation may affect whether the suspected unused out-of-range frequency loads execute.
