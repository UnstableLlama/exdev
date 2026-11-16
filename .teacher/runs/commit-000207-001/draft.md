# 95c5097b3099de821058504a282d7f83cf3369b2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/95c5097b3099de821058504a282d7f83cf3369b2) · [Evidence ledger](draft.json)

Corrects None checks across all attention backends, restoring dispatch to fused RMSNorm/RoPE while leaving inherited native-kernel concerns unchanged.

- [Test fused normalization weights for absence](#attention)

## Problem

All three attention decode paths tested the truth value of q_norm_tensor instead of testing whether fused normalization weights were absent. [source; call_ea255cbac5eb456fb34b3133314da2b1, call_73aa0d50edbe490fa98b95d295335d23]

## Reasoning

Replacing `not self.q_norm_tensor` with `self.q_norm_tensor is None` makes dispatch depend on weight availability, not tensor contents. [source; call_ea255cbac5eb456fb34b3133314da2b1]

## Impact

The correction covers uncached SDPA, uncached Flash Attention and cached Flash Attention. It removes the tensor truth-value evaluation before fused RMSNorm/RoPE without changing normalization parameters or backend calls. [source; call_ea255cbac5eb456fb34b3133314da2b1, call_73aa0d50edbe490fa98b95d295335d23]

## Source Notes

Read the QK LayerNorm ancestor entry, which identifies the tensor-truth dispatch regression and inherited native normalization/bounds concerns. [ancestor; call_fd14c63cffbb43ab96e5e3aa46e968ae]

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns conversion and a tokenizer-truncation diagnosis; #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, concerns scaling policy. Their relationship here is inferred only from attention/rope path overlap, not evidence that this fix addresses those reports. [inference; call_c3095b297ac24e41a76664f27e88dcd9, call_865863ca52d043f29ad7785a17ad0daa, call_4cc6d424be90435ba861b6bb0be27290]

<a id="attention"></a>

## Test fused normalization weights for absence

Attention initializes normalization tensors to None and exposes loaded weights only for RMSNorm. LayerNorm therefore continues through separate Q/K normalization, while loaded RMSNorm with RoPE skips that fallback and passes its weights, epsilon and constant bias into RoPE.apply. [source; call_73aa0d50edbe490fa98b95d295335d23, call_ea255cbac5eb456fb34b3133314da2b1]

No-norm and no-RoPE short-circuit behavior is preserved. Standalone normalization still requests half output before rotation. RoPE.apply forwards optional weights to the native RMSNorm/rotation kernel, whose wrapper requires half Q/K and a one-dimensional Q normalization weight of head_dim elements. [source; call_73aa0d50edbe490fa98b95d295335d23, call_c74c2ba56f7444fa8b2aee768fd5d98e, call_bce13ed0f65042f9bc878bbdc33f65cf]

A bounded Python control-flow transcription showed that a present truth-rejecting weight raises under the old condition but selects the fused route under the new condition. Missing weights, absent RoPE and absent normalization retained their branch results. [execution; call_ffef3140733148fc98aff80da7eff51d]

The ancestor's dispatch defect is removed by all three substitutions. Its native reduction and padded-read concerns are carried over: the task changes no native code, and successful dispatch alone does not establish correct fused-kernel execution. [source; call_ea255cbac5eb456fb34b3133314da2b1, call_bce13ed0f65042f9bc878bbdc33f65cf, call_94522b0db4044e13ad19634f8b5d4b94]

## Authoring-time findings — pending review

### inherited-fused-rope-concerns (suspected; defect)

The newly reachable fused path retains conflicting shared reduction writes and unguarded padded input reads.

Trigger: Fused normalization with nonuniform lane values; or RoPE with a head width requiring padding, such as 80, or shorter partial-rotary frequencies.

Expected: Store one complete reduction per warp and restrict frequency and weight reads to their logical arrays.

Actual: Every lane writes its shuffle-down result to the same per-warp sums slot. inv_freq[t] and the normalization half2 weight read are unguarded. Attention's three decode methods reach RoPE.apply; the inspected science caller also invokes rotation but supplies no normalization weights.

Locations: 2cc8f718dacbd75c2cfc3cc229dc787090333bde:exllamav3/exllamav3_ext/rope.cu — rope_kernel

Source evidence: call_bce13ed0f65042f9bc878bbdc33f65cf, call_94522b0db4044e13ad19634f8b5d4b94, call_38de610fbc98478abc8399d2f0ca4648, call_b2fe0bc679ac4baeab2ed51679068e36, call_98df351476e948eeb4062701ec52d196

source_inspection: Compared native loads and reduction writes with the reduction helper, Python wrapper, attention callers and task diff. [call_bce13ed0f65042f9bc878bbdc33f65cf, call_94522b0db4044e13ad19634f8b5d4b94, call_c74c2ba56f7444fa8b2aee768fd5d98e, call_ea255cbac5eb456fb34b3133314da2b1]. Limits: No GPU race or memory-error reproduction.

scalar_transcription: Launch arithmetic for head width 80 gives 64 x lanes but only 40 full-width frequency entries. [call_ffef3140733148fc98aff80da7eff51d]. Limits: Python integer arithmetic only, not kernel execution.

## Uncertainty and limits

No PyTorch, CUDA kernel or model workflow was executed. The Python check models control flow with a truth-rejecting object; it does not reproduce PyTorch's exception.

Native numerical correctness and memory safety remain unverified by GPU execution. Literal caller searches do not establish dynamic or external reach.
