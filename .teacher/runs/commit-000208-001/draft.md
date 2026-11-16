# 7aa775b6b3e8200ddab4925f41b6323363ad0a16


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/7aa775b6b3e8200ddab4925f41b6323363ad0a16) · [Evidence ledger](draft.json)

Integrates PR #45’s explicit None checks across attention backends, avoiding normalization-tensor truth testing while retaining inherited native-kernel concerns.

- [Select fused normalization by weight availability](#attention)

## Problem

PR #45 reports that loading DeepSeek-R1-0528-Qwen3-8B reached a boolean check on a multi-element normalization tensor when RoPE was enabled. [source; call_0c9d5447db3d4be480e5a0c4b2d40f7c]

## Reasoning

The first-parent diff replaces tensor truth testing with an explicit None test in all three attention decode paths. Dispatch consequently depends on whether fused normalization weights exist, not their contents. [source; call_0a476f398d8748cd935631168ae0dab1]

## Impact

The change covers uncached SDPA, uncached Flash Attention and cached Flash Attention without changing their backend calls or normalization arguments. [source; call_0a476f398d8748cd935631168ae0dab1, call_c952d5a3c9a54a478681405977cd75af]

## Source Notes

Read the second-parent explanation, which records the same dispatch correction and inherited fused-kernel reduction and bounds concerns. [ancestor; call_91f79bb06e4946bbbe2658221f5647f6]

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns conversion and a tokenizer-truncation diagnosis. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading. Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, concerns scaling policy. Their connection here is inferred only from shared attention or RoPE source paths; they do not establish additional failures fixed by this patch. [inference; call_6cebeced3ce441c680c9d0fdeb76853f, call_96d30c013fad4611b1bfec6db78ab891, call_7935dd6385674291ad68ad8fa5c0d64e, call_0a476f398d8748cd935631168ae0dab1]

<a id="attention"></a>

## Select fused normalization by weight availability

Attention initializes Q/K normalization tensors to None and populates them during loading only for RMSNorm. With RoPE and loaded RMSNorm weights, the corrected condition skips standalone normalization and passes weights, epsilon and constant bias into RoPE.apply. LayerNorm retains separate Q/K normalization with half output because its fused weights remain absent. [source; call_c952d5a3c9a54a478681405977cd75af, call_0a476f398d8748cd935631168ae0dab1]

RoPE.apply makes inputs contiguous and forwards optional weights to the native kernel. The native wrapper requires half Q/K and validates a supplied Q normalization weight as one-dimensional with head_dim elements. The kernel applies RMS normalization before rotation; this patch does not add fused LayerNorm. [source; call_fc8b39e30a18407caff3dc447bf78a8f, call_544f165f7e1849f3a7974fae9828b7a5]

A bounded Python transcription showed the old expression raising for a present truth-rejecting weight while the new expression selected the fused route. Missing weights, absent RoPE and absent normalization preserved their branch outcomes. [execution; call_c70798fcecd34d9e9929785dd6b584b7]

The inherited dispatch defect is removed, but the native reduction and padded-load concerns remain: the complete task diff changes only the three Python conditions. Successful dispatch therefore does not establish successful fused-kernel execution. [source; call_0a476f398d8748cd935631168ae0dab1, call_544f165f7e1849f3a7974fae9828b7a5, call_6d965aa333c549109a2127a6953484ce]

## Authoring-time findings — pending review

### inherited-native-rope-concerns (suspected; defect)

The fused route retains conflicting reduction writes and unguarded frequency and normalization-weight reads.

Trigger: Fused RMS normalization with differing lane reduction results, or a head dimension requiring launch padding, such as 80; partial rotary dimensions can also shorten the frequency array.

Expected: Publish one complete sum per warp and restrict reads to logical frequency and weight bounds.

Actual: Every lane stores its shuffle-down reduction into the same per-warp sums slot. inv_freq[t] and the half2 normalization weight are read without logical bounds checks. All three attention decode paths call RoPE.apply. The direct test caller includes width 80 with normalization; the science caller supplies no normalization weights.

Locations: 2cc8f718dacbd75c2cfc3cc229dc787090333bde:exllamav3/exllamav3_ext/rope.cu — rope_kernel

Source evidence: call_544f165f7e1849f3a7974fae9828b7a5, call_6d965aa333c549109a2127a6953484ce, call_ded4c658fb784affafd363770aa77535, call_1a8a9249b162478c9aa63dd0f596713d, call_fb08c9ae031742d9aa9b9bec1ecb3b8d, call_182d8eb4c4be4d6e92a64d7c98bf39fe

source_inspection: Compared the kernel, reduction helper, Python wrapper, direct callers and complete task diff; these native concerns are carried over unchanged. [call_544f165f7e1849f3a7974fae9828b7a5, call_6d965aa333c549109a2127a6953484ce, call_0a476f398d8748cd935631168ae0dab1]. Limits: No GPU race or memory-error reproduction.

scalar_transcription: Computed the launch's rounding to 32-lane warps: width 80 produces 64 x lanes but only 40 full-width frequency entries. [call_c70798fcecd34d9e9929785dd6b584b7, call_544f165f7e1849f3a7974fae9828b7a5, call_fc8b39e30a18407caff3dc447bf78a8f]. Limits: Integer shape arithmetic only, not execution of CUDA loads.

## Uncertainty and limits

No PyTorch model workflow or CUDA kernel was executed. The Python check models dispatch with a truth-rejecting object, not an actual tensor.

Native numerical correctness and memory safety remain unverified by GPU execution; literal caller searches do not establish dynamic or external reach.
