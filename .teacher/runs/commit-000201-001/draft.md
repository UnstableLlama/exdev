# 91c7cc41881c50abf6608a07c53b9d888c9cf2a6


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/91c7cc41881c50abf6608a07c53b9d888c9cf2a6) · [Evidence ledger](draft.json)

Wires optional Cohere Q/K LayerNorm into the existing attention path and unconditionally requests float32 MLP output; inspected Command R Plus configurations enable the new norms.

- [Optional Cohere Q/K LayerNorm and MLP output precision](#models)

## Problem

CohereModel previously supplied no Q/K normalization, even for configurations requesting it. The change connects the optional configuration flag to paired LayerNorm modules. [source; call_f25b3efcfe3e46f8b69f15431040a8ed, call_563f5d58d34440f18d3a16fa9acb3a4b]

## Reasoning

The implementation reuses the parent's standalone LayerNorm attention path rather than adding a normalization kernel. That path normalizes Q and K before RoPE and leaves V unchanged. [source; call_563f5d58d34440f18d3a16fa9acb3a4b, call_5c5c7185650f462caac0ead8cc6dec9f]

## Impact

Absent or false use_qk_norm preserves attention without head norms. Independently of that flag, every Cohere GatedMLP now requests float32 output. [source; call_563f5d58d34440f18d3a16fa9acb3a4b]

## Source Notes

Read the Cohere introduction and QK LayerNorm ancestor entries. The former records the missing Command R Plus normalization; the latter establishes the reusable standalone path and records concerns in RMSNorm dispatch and the alternative LayerNorm method. [ancestor; call_9ea688859c1840de8a7b5bfc1180473c, call_460b100999d44480b5ae09b3421aa9a4]

The missing Cohere wiring is removed by this diff. The parent's tensor-truth condition and forward_torch implementation remain unchanged, but the new path uses LayerNorm.forward with q_norm_tensor=None, not loaded RMSNorm tensors or forward_torch. [source; call_563f5d58d34440f18d3a16fa9acb3a4b, call_5c5c7185650f462caac0ead8cc6dec9f, call_bb4dc7c222bf42cc919a4ae0f07a37e3]

Inspected discussion #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; PR #4, “chore: update config.py,” proposes a spelling correction. Their connection to this inspection is inferred from config.py overlap, not evidence that either motivated this change. [inference; call_57e7773aa6ce4e959d20d60e1a075093, call_9355d0318dda4945bdd67b88f1986967, call_e384057943fd43608e7456302493d782]

<a id="models"></a>

## Optional Cohere Q/K LayerNorm and MLP output precision

CohereConfig reads use_qk_norm with expected type int and default False. Whole-parent-tree searches found neither use_qk_norm nor qk_norm. Config.read_cfg delegates to read_dict, whose isinstance-based validation accepts boolean values without converting them. [source; call_563f5d58d34440f18d3a16fa9acb3a4b, call_fd0e3e868ca64ab89f3b7e1df7513a3e, call_247bcc6da3e146cdaa75e0932304e12d, call_e384057943fd43608e7456302493d782, call_970737e06a13417e9a461472f0bda2d0]

Executing the repository read_dict through runpy returned False for an absent key and preserved False, True and integer 1 for supplied values. Thus the int annotation does not reject the inspected JSON boolean flags. [execution; call_cbbd7a2018e74f66907eca42d5fb52f9]

When enabled, each layer constructs norms at model.layers.<idx>.self_attn.q_norm and k_norm using the existing layer_norm_eps mapping, whose default is 1e-5. LayerNorm.load requires the corresponding .weight and treats .bias as optional. Both objects are supplied together, satisfying Attention's paired-norm assertion. [source; call_563f5d58d34440f18d3a16fa9acb3a4b, call_f25b3efcfe3e46f8b69f15431040a8ed, call_bb4dc7c222bf42cc919a4ae0f07a37e3, call_5c5c7185650f462caac0ead8cc6dec9f]

All three attention decode routes reshape Q/K into batch × sequence × heads × head_dim, call the standalone norms with half output, and then apply RoPE. LayerNorm weights are not exposed as fused RMSNorm weights. For multidimensional affine weights, LayerNorm.forward normalizes only the final axis without affine parameters, then broadcasts the weight multiplication and optional bias addition. [source; call_5c5c7185650f462caac0ead8cc6dec9f, call_bb4dc7c222bf42cc919a4ae0f07a37e3]

Existing LayerNorm constructors in Cohere and Cohere2 serve block-input and final normalization, using the same epsilon argument and no quantization map; final norms request half output explicitly. The new constructors retain these conditions but operate on head-shaped attention tensors. Cohere2 is not modified. [source; call_ddda803b67c349d4944fe968d3abb888, call_f25b3efcfe3e46f8b69f15431040a8ed, call_2619a62fb97c448bb211c87454d8b9a7, call_563f5d58d34440f18d3a16fa9acb3a4b]

The float32 setting reaches GatedMLP's down-projection constructors and final dtype selection; it does not change the gate/up intermediate dtype setting. Multiple MLP slices accumulate their down-projection outputs before returning. ParallelDecoderBlock consumes this result through x += y2, after adding attention output; its prefill early return skips the MLP. Q/K LayerNorm explicitly returns half tensors and does not require the MLP output setting as a precondition. [source; call_563f5d58d34440f18d3a16fa9acb3a4b, call_72ceb5594d3343fab887e0f5be4fba47, call_cdf44bf251bf4bcebf5f7ddbc57742fc, call_5c5c7185650f462caac0ead8cc6dec9f]

Among the inspected CohereLabs configurations, aya-23-35B, aya-23-8B, aya-expanse-32b, aya-expanse-8b and c4ai-command-r-08-2024 each explicitly disable use_qk_norm. Each therefore retains no head norms under this mapping. All specify layer_norm_eps=1e-5. [source; call_0b3a1505f4314dcba631a12983d5d405, call_5d8515a456ea491cb8e910e044fe912f, call_0a97bf7e3aac446cb1fdd91fbf1664ab, call_62da08f9e96c424d96a48d34887567f4, call_9176ba32ee67467c9375e8b6ca6bfc2e, call_563f5d58d34440f18d3a16fa9acb3a4b]

c4ai-command-r-v01 and c4ai-command-r-v01-4bit each omit use_qk_norm and take False. c4ai-command-r-plus, c4ai-command-r-plus-08-2024 and c4ai-command-r-plus-4bit each set it true and therefore select the new paired norms. All five specify layer_norm_eps=1e-5; the three Plus configurations each have hidden width 12288, 96 query heads and 8 KV heads. [source; call_52220672affe42c080d205f2e6116753, call_5399a84d87274ba7b52499de346fb3ba, call_5bf3ce3dac124e558818e16648044d05, call_1361b8e3582546b694a7addd29bdb5e4, call_58d7f0b69b5f4496b634cf9f093d7861, call_563f5d58d34440f18d3a16fa9acb3a4b]

A bounded integer calculation gave head_dim=128 for all three hidden-width/query-head pairs represented by these configurations: 4096/32, 8192/64 and 12288/96. This checks the existing fallback division, not actual tensor loading or broadcasting. [execution; call_cbbd7a2018e74f66907eca42d5fb52f9]

## Uncertainty and limits

No model loading, generation, PyTorch operation or GPU kernel was executed. The successful run exercised only the repository's standard-library configuration reader and integer shape arithmetic.

Configuration agreement does not establish checkpoint tensor compatibility or numerical equivalence. In particular, the two 4bit configurations describe bitsandbytes storage; this patch does not establish support for that format.

The inspected model files are hash-verified mirror copies; their supplied revisions identify verified file sets rather than official Git commits.

The reason for the unconditional float32 MLP output change and its numerical or performance benefit are not established by measurements.
