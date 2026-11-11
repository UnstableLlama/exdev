# b0919fca3223eb454c35fad96a04af73fef74eb5


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b0919fca3223eb454c35fad96a04af73fef74eb5) · [Evidence ledger](draft.json)

Reworks proxy-error evaluation into sequential scalar contractions to reduce memory overhead, but leaves a suspected undefined-name failure at the return.

- [Proxy-error contraction and tensor lifetimes](#quantizer)

## Problem

Proxy-error evaluation explicitly constructed E @ E.T and W @ W.T; the existing comments identified large intermediate tensors, especially for lm_head, as a memory concern. [source; call_f7f0f10331794e588cf96808a6106742]

## Reasoning

The patch replaces both Gram-matrix expressions with scalar einsum contractions and evaluates the numerator before transferring W to the working device. [source; call_f7f0f10331794e588cf96808a6106742]

## Impact

This offers lower temporary-memory overhead, but the diff also renames the computed result to proxy_err_2 without updating the return of proxy_err. [inference; call_f7f0f10331794e588cf96808a6106742, call_b74f589b368b4086aa96541bcf2b78e3, call_502b31bf1d75428e9044d4cd759c1a00]

<a id="quantizer"></a>

## Proxy-error contraction and tensor lifetimes

quantize_exl3 measures error after LDLQ in the transformed weight space: E = weight_r - weight_q, W = weight_r, and Hd = H.to(device). The unchanged CPU-buffer branch applies above 5e8 weight elements, making the ordering of device transfers relevant for large tensors. [source; call_b74f589b368b4086aa96541bcf2b78e3, call_f7f0f10331794e588cf96808a6106742]

For a matrix X with input-channel rows and output-channel columns, both formulations sum H[i,j] * X[i,k] * X[j,k] over i,j,k. The old expression explicitly forms an input-channel-square Gram matrix; einsum expresses the scalar directly, allowing a contraction plan that avoids that explicit intermediate. Algebraic equivalence does not require H to be symmetric. [inference; call_f7f0f10331794e588cf96808a6106742, call_b74f589b368b4086aa96541bcf2b78e3]

A standard-library scalar transcription on two 2-by-3 matrices produced identical old/new numerators of 54 and denominators of 87, yielding 0.6206896551724138. [execution; call_dc8524452f644aa5ac4c48b07df7d0f9]

The denominator floor remains 1e-8, preventing division by zero or a smaller denominator. The patch clears weight_r early, although W still aliases that tensor, then extracts num with item(), clears E, transfers W and computes den. Thus clearing weight_r alone does not release the weights; the useful lifetime change is releasing E before the denominator's device work. [source; call_f7f0f10331794e588cf96808a6106742]

The final progress update becomes unconditional. ProgressBar.__enter__ returns the object even without display text, and update internally checks that text, so this change preserves the no-display path. [source; call_f7f0f10331794e588cf96808a6106742, call_543f8dd7e68a4f2eaabb425a4462d8f7]

## Authoring-time findings — pending review

### proxy-error-return-name (suspected; defect)

The new metric assignment leaves the returned proxy-error name undefined.

Trigger: quantize_exl3 successfully completes quantization, metric evaluation and tensor packing and reaches its return statement.

Expected: Return weight_q, the computed normalized proxy error, and out_tensors.

Actual: The patch assigns proxy_err_2, while the unchanged return references proxy_err. Source inspection indicates a NameError instead of a successful return.

Locations: b0919fca3223eb454c35fad96a04af73fef74eb5:exllamav3/modules/quant/exl3_lib/quantize.py — quantize_exl3

Source evidence: call_f7f0f10331794e588cf96808a6106742, call_b74f589b368b4086aa96541bcf2b78e3, call_502b31bf1d75428e9044d4cd759c1a00

source_inspection: Compared the complete patch with the parent function and its proxy_err occurrences: the sole assignment is replaced, but the return is not. [call_f7f0f10331794e588cf96808a6106742, call_b74f589b368b4086aa96541bcf2b78e3, call_502b31bf1d75428e9044d4cd759c1a00]. Limits: The quantizer was not executed.

## Uncertainty and limits

No PyTorch or CUDA execution was performed; peak VRAM, contraction planning and floating-point differences remain unmeasured.

The scalar check uses exact small integer sums, not the repository implementation or GPU arithmetic.
