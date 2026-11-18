# 2d1ce8910339ce3f10b3c46ee0b92cff23df71da


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2d1ce8910339ce3f10b3c46ee0b92cff23df71da) · [Evidence ledger](draft.json)

Registers Dots1 with normalized attention and dense/routed/shared experts. Reference configurations match; prompt formatting and conditional all-expert fusion retain suspected problems.

- [Dots1 assembly and runtime contracts](#dots1)

## Problem

The parent registry lacks Dots1ForCausalLM. This change registers it and adds configuration and model assembly. [source; call_8323ffbeec8e4e2ab27cbe6ee14c2780, call_4c535927b72f4ea4a2b1ff52c8a9e7f4, call_e2114d9afaa94e66835167b308aa38fe]

## Reasoning

The builder combines existing normalized attention with initial dense layers, then routed and shared experts. Explicit single-group settings select the existing Dots router. [source; call_e2114d9afaa94e66835167b308aa38fe, call_52db8331983c45d18ee119810b923a34]

## Impact

Both reference configurations agree with the assembly's dimensional mapping. This establishes source compatibility, not successful loading or generation. [source; call_17e4a2ef49fe447cb1bd0dddb963948f, call_6641bee795a04cba95a463ad14925aaa, call_e2114d9afaa94e66835167b308aa38fe]

## Source Notes

Read the Qwen3-MoE entry for the closely followed assembly, the parent routing entry for prerequisites and conditional defects, and the Dots chat-template entry for the separate example formatter. [ancestor; call_3b670004769d47d4a49d624e56483a75, call_4012480d25e547a68fedc8293a7a74b7, call_c83bb167290a4ca09d3a5ccbb755e5cb, call_85db127fc8424890a358a9149a51d5b7]

Issue #51, “dots.llm1 support,” is louiehelm's request proposing Qwen3 attention with Deepseek-style MoE. Its relationship to turboderp's change is inferred from the architecture name and composition, not an explicit commit reference. [inference; call_fa4b4c1b0390478aa83c7c88f3360010, call_e2114d9afaa94e66835167b308aa38fe]

Other inspected discussions are background: PR #4, “chore: update config.py,” corrects spelling; PR #26, “Superior 3INST parameters,” discusses decoder choices; #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, requests scaling automation. Their inferred connections are shared configuration, conversion and Qwen3-derived code, not established motivation. [inference; call_46bd34d7e09b409084424a56866996eb, call_a8f0d0c7a9dd474d87927db93ce6d806, call_cb9473d11e124959ad5705b059278afe, call_2be97c6878f3426fb1384d9fe7cae82e]

Issue #33, “Error converting model,” reports file-opening failure and later GLM4 sampling problems. #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” report conversion failures. #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” concerns vocabulary dimensions. Connections inferred through inspected shared files do not establish Dots defects or fixes. [inference; call_4638dc900d8b442699a0faf13546eacc, call_3abc56181a734ec2a9edfa5d31c5ab91, call_c94f113be17a4b9ba9a922b6050a4388, call_6f24ea4214bf4181b92e0669ecead663, call_76efa4a52b054bc19e8893ee189f4e50]

<a id="dots1"></a>

## Dots1 assembly and runtime contracts

Registration makes Config.from_directory select Dots1Config. It accepts explicit head_dim or derives hidden_size // num_attention_heads, defaults KV heads to query heads, and requires supplied activation/scoring settings to be silu, noaux_tc and normalized top-k probabilities. Dense and expert widths are required. Defaults are one shared expert, 128 routed experts, eight selected experts, three initial dense layers and routed scale 2.5. [source; call_4c535927b72f4ea4a2b1ff52c8a9e7f4, call_e2114d9afaa94e66835167b308aa38fe, call_d86790bf973d49678cfbd03d76bffd19]

dots-studio/dots.llm1.base specifies hidden size 4096, 32 query/KV heads, 62 layers, dense width 10944, expert width 1408, 128 routed experts, six selected experts, two shared experts and one initial dense layer. dots-studio/dots.llm1.inst independently specifies the same values. Both omit head_dim, use RMS epsilon 1e-5, untied embeddings, vocabulary 152064, rope_theta 10000000 and position limit 32768. Their counts override the differing builder defaults. Base EOS is 151643; instruction EOS is 151645. [source; call_17e4a2ef49fe447cb1bd0dddb963948f, call_6641bee795a04cba95a463ad14925aaa, call_e2114d9afaa94e66835167b308aa38fe]

Integer calculations give head dimension 128, attention width 4096, shared width 2816, one dense block and 61 sparse blocks. Rounding dense width to a 128-element multiple gives 11008. These are transcribed shape calculations, not tensor tests. [execution; call_449c0ff815694de282c6c2388b45453f]

The pipeline is embedding → sequential pre-normalized TransformerBlocks → final RMSNorm → vocabulary Linear. Each block adds attention, then normalizes the updated residual before its MLP. Q/K normalization operates per head before RoPE; V is not normalized. The builder selects NEOX RoPE, unspecified attention scale and no sliding window. Attention/MLP outputs request FP32; gated intermediates and final normalization request FP16. [source; call_e2114d9afaa94e66835167b308aa38fe, call_247054539f9d4ff1b4e7edc49af417c7, call_812388b25d714a3484046a696a90e091, call_d86790bf973d49678cfbd03d76bffd19]

idx < first_k_dense_replace selects GatedMLP; later blocks combine BlockSparseMLP with a shared GatedMLP of width moe_intermediate_size × n_shared_experts. Each expert computes down(silu(gate(x)) × up(x)). Routed outputs are weighted and accumulated, then shared output is added without routing weights. GatedMLP supplies the projection lists required by shared-expert allocation, avoiding the inherited plain-MLP interface mismatch. [source; call_e2114d9afaa94e66835167b308aa38fe, call_52db8331983c45d18ee119810b923a34, call_10e518f8915d4aeeae77b6698963521b, call_247054539f9d4ff1b4e7edc49af417c7]

deepseekv3_routing=True and n_group=topk_group=1 select routing_dots. It adds correction bias to logits, selects top-k, applies sigmoid, normalizes with a 1e-20 stabilizer and scales by routed_scaling_factor. Thus 2.5 scales the mixture; the two ones satisfy dispatch prerequisites. Unlike routing_ds3, bias affects weights as well as selection. The builder supplies scaling, and the sampled checkpoint supplies gate.e_score_correction_bias. [source; call_e2114d9afaa94e66835167b308aa38fe, call_52db8331983c45d18ee119810b923a34, call_8a62af66837e4675b221b577569502c0]

Multiple flattened tokens or non-EXL3 experts use ordinary grouping. One token with fully EXL3 experts uses indexed multi-GEMM. MultiLinear requires matching dimensions, bit widths and decoder multipliers, absent biases/softcaps and unit post-scale. Dots avoids the ancestor's default native-call mismatch and unassigned grouped-route case, but leaves the conditional all-expert buffer mismatch unchanged. [source; call_e2114d9afaa94e66835167b308aa38fe, call_52db8331983c45d18ee119810b923a34, call_66bb31ddabdf4825b01e7b5a0a92d9d9, call_a42c248d9f474413bd5d4564ed311829]

Base checkpoint samples contain embedding/head [152064,4096], attention matrices [4096,4096], Q/K norms [128], residual norms [4096], dense gate/up [10944,4096] and down [4096,10944]. Sparse samples contain expert gate/up [1408,4096], down [4096,1408], router [128,4096], correction bias [128], shared gate/up [2816,4096] and down [4096,2816]. model.norm.weight is [4096]. All sampled tensors are BF16. [source; call_327b3cbb738c4f2090a1c2f5e8deca33, call_8a62af66837e4675b221b577569502c0, call_81c7b1ec0f894c8bb04cafac055db107]

Linear checks EXL3 groups before requesting ordinary .weight with float2half=True and transposition. It also requests optional .bias and .weight_scale_inv; EXL3 loading requests trellis and optional scale, rotation and multiplier tensors. The builder configures no fused-QKV alternative. Samples support ordinary naming and orientation, not completeness of every optional or alternate path. [source; call_b4bc9423264b4900b9656399ddc15d40, call_e2114d9afaa94e66835167b308aa38fe, call_327b3cbb738c4f2090a1c2f5e8deca33, call_8a62af66837e4675b221b577569502c0]

The builder clears the first attention o_proj's qmap, with a comment reporting irregularity that breaks quantization. It also enables calibration_all_experts: conversion passes that flag during capture and recomputes reference states using ordinary selected-expert routing. These settings affect calibration rather than changing ordinary inference routing. [source; call_e2114d9afaa94e66835167b308aa38fe, call_e2040489302f4337909cd117b4dbde4a]

prepare_inputs stores input_ids and calls prepare_for_attn, matching all twelve located callers without dropping their caller-side guards. The helper defaults to uncached FlashAttention and retains cached-mode requirements. Both references disable embedding tying, so the optional head fallback is inactive. [source; call_e2114d9afaa94e66835167b308aa38fe, call_b73ccd7416c948d99c6b516cdc6a4fa9, call_e2040489302f4337909cd117b4dbde4a, call_812388b25d714a3484046a696a90e091, call_17e4a2ef49fe447cb1bd0dddb963948f, call_6641bee795a04cba95a463ad14925aaa]

## Authoring-time findings — pending review

### dots-default-prompt-format (suspected; external_compatibility)

The convenience formatter emits ChatML instead of the reference instruction checkpoint's Dots format.

Trigger: Call Dots1Model.default_chat_prompt for dots.llm1.inst.

Expected: Use system/userprompt/response delimiters and the checkpoint's default system message.

Actual: Emits im_start/im_end blocks and no default system message. Whole-parent search found one direct caller in the vision example imgsearch.py, not proof that ordinary Dots chat reaches it. The separate Dots example formatter is unaffected.

Locations: 2d1ce8910339ce3f10b3c46ee0b92cff23df71da:exllamav3/models/dots1.py — Dots1Model.default_chat_prompt

Source evidence: call_e2114d9afaa94e66835167b308aa38fe, call_fc2b0aec99774e46860d241fa6d0a782, call_d376508b64204f1bbedc340e93ce9ff2, call_449c0ff815694de282c6c2388b45453f

source_inspection: Compared the method, pinned tokenizer template, existing Dots formatter and located caller. [call_e2114d9afaa94e66835167b308aa38fe, call_fc2b0aec99774e46860d241fa6d0a782, call_449c0ff815694de282c6c2388b45453f]. Limits: No generation test or quantified output degradation.

### inherited-dots-all-expert-fusion (suspected; defect)

All-expert routing retains selected-expert-sized fused buffers.

Trigger: Forward one flattened token through fully EXL3 Dots experts with activate_all_experts=True.

Expected: Evaluate all 128 experts with compatible buffers or select the ordinary path.

Actual: Routing returns 128 indices, while buffers have six slots for both references. Dispatch does not exclude all-expert activation; exl3_mgemm checks indices dimension 1 against output dimension 0. TransformerBlock forwards params unchanged. Initial BF16 calibration avoids fusion, so normal initial conversion failure is not established.

Locations: 2d1ce8910339ce3f10b3c46ee0b92cff23df71da:exllamav3/models/dots1.py — Dots1Model.__init__, b8c830c17f53cf0d4caf7b774fe458b2f31cb85c:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_e2114d9afaa94e66835167b308aa38fe, call_52db8331983c45d18ee119810b923a34, call_247054539f9d4ff1b4e7edc49af417c7, call_e2040489302f4337909cd117b4dbde4a, call_a42c248d9f474413bd5d4564ed311829

source_inspection: Compared routing cardinality, allocation, dispatch, caller flags and native shape validation. [call_52db8331983c45d18ee119810b923a34, call_a42c248d9f474413bd5d4564ed311829, call_e2040489302f4337909cd117b4dbde4a]. Limits: Conditional API path; no extension invocation.

scalar_transcription: Calculated 128 all-expert indices versus six fused slots. [call_449c0ff815694de282c6c2388b45453f]. Limits: Integer calculation, not repository execution.

## Uncertainty and limits

No model loading, conversion, generation or CUDA execution was performed.

Headers sampled ordinary tensor forms, not every layer, expert or optional suffix. Instruction-checkpoint tensor equivalence is not established by matching configurations.

The approved model.safetensors.index.json read failed; a complete checkpoint inventory remains unavailable.

The first output projection's reported irregularity and the quantization workaround's effectiveness remain unmeasured.

Dimension calculations do not establish floating-point routing behavior, including FP16 underflow or the effective 1e-20 stabilizer.
