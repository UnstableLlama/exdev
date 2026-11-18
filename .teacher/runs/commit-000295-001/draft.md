# 69f8f9a07b95142878997f79e0053b1c1e08422f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/69f8f9a07b95142878997f79e0053b1c1e08422f) · [Evidence ledger](draft.json)

Bounds FP32-input SiLU/GELU gated products at the FP16 store using ±65504; half-input arithmetic and inherited caller/tail limitations remain unchanged.

- [Saturate FP32 gated-activation outputs at the FP16 store](#runtime)

## Problem

The FP32-input gated-activation kernel converted activation(x)*y directly to FP16, allowing large products to overflow the output representation. [source; call_71664dc1b6f248a08ebaafbbcc831ea5, call_2c29573b73d445499fb48bfc7967e932]

## Reasoning

Clamp the converted half2 pair before storing it. This preserves FP32 activation and multiplication while bounding the FP16 result; it does not clamp inputs or intermediate arithmetic. [source; call_2c29573b73d445499fb48bfc7967e932, call_71664dc1b6f248a08ebaafbbcc831ea5]

## Impact

The change covers both SiLU and GELU specializations with FP32 inputs. The FP16-input kernel and PyTorch-based non-gated MLP activations remain unchanged, so the commit message is broader than the implementation. [source; call_2c29573b73d445499fb48bfc7967e932, call_71664dc1b6f248a08ebaafbbcc831ea5, call_943a2748badd426489f658292ab6560c]

## Source Notes

The FP32-activation ancestor entry records the mixed-precision output contract, incompatible in-place FP32 callers and an omitted odd-element tail. [ancestor; call_c3b68455aa53434e9072b29eb1b7a5c7]

Current source retains the GatedMLP destination mismatch and odd-element tail. Unlike the earlier entry's account, the parent BlockSparseMLP ordinary path now supplies a separate half destination when needed; its fused path also supplies a half destination. [source; call_943a2748badd426489f658292ab6560c, call_159670c1fcb0427593ff8a12c5b5ec12, call_71664dc1b6f248a08ebaafbbcc831ea5, call_2c29573b73d445499fb48bfc7967e932]

The inspected discussions concern different failures: “TypeError with presence penalty” reports argument incompatibility, while “humaneval.py: fix top_k type, remove rep_p, add qwen3” discusses evaluation, penalty-kernel NaNs and prompting. Neither establishes the motivation for this activation clamp. [source; call_39cb293a37cf4ffda04c25f932b79b5c, call_29b0383aa75b4730bc505861e3763f1c]

<a id="runtime"></a>

## Saturate FP32 gated-activation outputs at the FP16 store

act_mul_kernel_f loads float2 pairs, applies SiLU or the tanh-based GELU approximation per lane, multiplies by the corresponding y lanes, then rounds to half2. The new helper applies an upper bound followed by a lower bound to that converted pair before the store. [source; call_71664dc1b6f248a08ebaafbbcc831ea5, call_2c29573b73d445499fb48bfc7967e932]

The bounds ±65504 are binary16's finite extrema: (2−2^-10)×2^15 = 65504. A standard-library scalar model retained ordinary rounded values and saturated modeled overflow: 65000 became 64992, while ±70000 became ±65504 after conversion and clamping. [execution; call_579ecb8b6b6e41c0854fe62d807350c1]

Placing the clamp after conversion allows the existing half2 min/max operations to bound overflowed output lanes without widening the destination. This trades extreme-value magnitude for a bounded representation; it does not recover precision lost during conversion or establish that earlier arithmetic was finite. [inference; call_2c29573b73d445499fb48bfc7967e932, call_71664dc1b6f248a08ebaafbbcc831ea5]

silu_mul and gelu_mul dispatch on x.dtype(), require matching input dtypes and always require a half destination. Their FP32 branches share the changed kernel; the half-input branches still store __hmul2 directly without this clamp. [source; call_71664dc1b6f248a08ebaafbbcc831ea5, call_2c29573b73d445499fb48bfc7967e932]

Whole-tree searches locate the exported operations in GatedMLP and BlockSparseMLP. BlockSparseMLP's ordinary expert path allocates half a when interm_dtype is not half, and its fused path uses half interm_a. These paths can reach the clamp with FP32 gate/up results. GatedMLP instead passes u as both input and destination, so FP32 u fails validation before reaching it. [source; call_7d5b049484c24d2f996272265d7dd4ff, call_552e0615c42b41d68dc5dd84896d66b7, call_5bdffbfb5c3749cfbde15f1ba19e63b2, call_943a2748badd426489f658292ab6560c, call_159670c1fcb0427593ff8a12c5b5ec12, call_71664dc1b6f248a08ebaafbbcc831ea5]

## Authoring-time findings — pending review

### inherited-fp32-gated-destination (suspected; defect)

GatedMLP retains an in-place destination incompatible with the FP32-input activation contract.

Trigger: GatedMLP.forward receives FP32 gate/up projection results.

Expected: Supply a half activation destination so the supported FP32-input kernel can run.

Actual: activation_fn_call(g, u, u) supplies FP32 z; the wrapper rejects z before launching the newly clamped kernel. Both BlockSparseMLP activation paths prepare half destinations instead.

Locations: 6f9928b3acee3b52f5064a1ce8ef436b2442ea52:exllamav3/modules/mlp.py — GatedMLP.forward, 69f8f9a07b95142878997f79e0053b1c1e08422f:exllamav3/exllamav3_ext/activation.cu — silu_mul / gelu_mul

Source evidence: call_943a2748badd426489f658292ab6560c, call_71664dc1b6f248a08ebaafbbcc831ea5, call_2c29573b73d445499fb48bfc7967e932

source_inspection: Compared whole-tree activation caller matches, destination preparation and unchanged wrapper checks. [call_5bdffbfb5c3749cfbde15f1ba19e63b2, call_159670c1fcb0427593ff8a12c5b5ec12, call_943a2748badd426489f658292ab6560c, call_71664dc1b6f248a08ebaafbbcc831ea5]. Limits: Conditional on FP32 projection results; no model execution.

### inherited-odd-activation-tail (suspected; defect)

The clamp does not repair the inherited omission of an odd final element.

Trigger: Call either exported activation with otherwise suitable buffers and an odd element count.

Expected: Write activation(x)*y for every output element.

Actual: Both kernels process only numel/2 complete pairs. The final destination element remains untouched; wrappers have neither an evenness check nor a scalar tail.

Locations: 69f8f9a07b95142878997f79e0053b1c1e08422f:exllamav3/exllamav3_ext/activation.cu — act_mul_kernel_f / act_mul_kernel_h

Source evidence: call_71664dc1b6f248a08ebaafbbcc831ea5, call_2c29573b73d445499fb48bfc7967e932, call_7d5b049484c24d2f996272265d7dd4ff, call_552e0615c42b41d68dc5dd84896d66b7

scalar_transcription: Enumerated the inspected launch and pair-index arithmetic. Lengths 1, 3, 129 and 513 each omitted their final index; 128 and 512 were fully covered. [call_579ecb8b6b6e41c0854fe62d807350c1, call_71664dc1b6f248a08ebaafbbcc831ea5]. Limits: Index model only, not kernel execution. Exported calls expose the case; this does not establish that normal padded model workloads produce odd lengths.

## Uncertainty and limits

No CUDA build, kernel execution, model evaluation or performance measurement was performed.

The scalar check models binary16 rounding and saturation, not CUDA intrinsic execution or NaN handling.

Whole-tree literal caller searches do not establish the behavior of dynamic or external callers.
