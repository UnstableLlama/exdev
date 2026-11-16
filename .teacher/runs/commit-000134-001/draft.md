# 74abd5e135f574f958faa6507f40c12c3f0cadba


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/74abd5e135f574f958faa6507f40c12c3f0cadba) · [Evidence ledger](draft.json)

Routes LinearFP16 multiplication through Torch when input and output dtypes match, retaining native GEMM for mixed output precision. The claimed Blackwell performance improvement is unmeasured.

- [Dtype-based dispatch for unquantized linear multiplication](#quantized-inference)

## Problem

LinearFP16.forward previously sent every multiplication through ext.hgemm, including half-precision output, whose native implementation calls cublasHgemm. [source; call_1d039b76157e45c3977d7bf7d049b238, call_fb1c3408cba04864be7c1d68d95a472a]

## Reasoning

The change selects Torch when the resolved output dtype equals the input dtype, retaining the native route when they differ. This preserves the native half-input, float-output alternative rather than replacing all GEMM calls. [source; call_f889249c48024258b645236cc0c2574c, call_fb1c3408cba04864be7c1d68d95a472a]

## Impact

Dispatch is dtype-based, not Blackwell-specific: matching input/output dtypes select Torch on every device reaching this method. The condition does not explicitly test the weight dtype. [source; call_f889249c48024258b645236cc0c2574c]

## Source Notes

The parent tree also mentions Blackwell in a PTX comment about predicated global-to-shared loads producing incorrect compiled code. That occurrence does not establish a connection to this matmul dispatch change. [source; call_32d6f9c1c0ae48c6aba3e9178825a52f]

Issue #31, “TypeError with presence penalty,” reports incompatible apply_pres_freq_pens arguments in TabbyAPI and subsequent recovery after TabbyAPI updates; it supplies no matmul performance evidence. [source; call_ff684695bc254e198321516fe2acde4f]

<a id="quantized-inference"></a>

## Dtype-based dispatch for unquantized linear multiplication

Output dtype precedence remains the call's out_dtype, then the instance's out_dtype, then torch.half. The resolved value is now stored once and reused for allocation and dispatch. [source; call_f889249c48024258b645236cc0c2574c, call_c6d0443b3775451799adf44b69f33c9a]

The method still flattens leading input dimensions, allocates a zero-filled output on the input device, multiplies by the stored weight, adds bias separately, and restores the leading dimensions. Torch writes directly into that output using out=y; allocation and bias fusion are not optimized by this patch. [source; call_f889249c48024258b645236cc0c2574c, call_1d039b76157e45c3977d7bf7d049b238]

The retained native callee requires rank-two half inputs and half or float output, with compatible matrix dimensions. Half output uses cublasHgemm; float output uses cublasGemmEx with CUBLAS_COMPUTE_32F. Both use alpha=1 and beta=0, requesting the product without accumulation of the previous output. [source; call_fb1c3408cba04864be7c1d68d95a472a]

This is a narrow alternative to replacing the native helper globally: LinearFP16_torch remains unchanged, and the separate ext.hgemm call in exl3.py is outside the patch. [source; call_1d039b76157e45c3977d7bf7d049b238, call_77e631d700624d4ab6303a00424f0e05, call_f889249c48024258b645236cc0c2574c]

## Uncertainty and limits

The reported Blackwell speed advantage is not established by benchmarks here; Torch's internal selected kernel was not available for inspection.

No GPU execution or numerical comparison was performed. A scalar arithmetic check would not validate this library-dispatch performance change.

Numerical equivalence between Torch matmul and the native cuBLAS paths remains unmeasured.
