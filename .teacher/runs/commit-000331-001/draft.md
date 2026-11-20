# 69e728ef0b2aff6e45acfc0c48d390b1aef85a70


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/69e728ef0b2aff6e45acfc0c48d390b1aef85a70) · [Evidence ledger](draft.json)

Computes the EXL3 proxy error in Hessian column blocks of up to 1,024, preserving the formula and existing OoM fallback without changing quantization. The accuracy test still accepts the unavailable-metric sentinel.

- [Evaluate the EXL3 proxy error in Hessian column blocks](#quantizer)

## Problem

After LDLQ produces quantized weights and trellis indices, `quantize_exl3` computes a Hessian-weighted diagnostic. The parent evaluates two full-width contractions, one for the quantization residual and one for the reference weights. A `torch.OutOfMemoryError` at this stage leaves the diagnostic unavailable even if quantization itself has finished. [source; call_f5d9b07104f741f0a7e78868f1fe5b8b]

## Reasoning

The patch partitions the contracted input-channel index rather than taking only diagonal Hessian blocks. Every Hessian column is used exactly once, and each block still sees every Hessian row. This preserves cross-block contributions and the full metric in exact arithmetic. [source; call_18f1e39716ea46e8b1559d14a81813ef]

Reducing the size of contraction intermediates is a plausible reason to chunk the diagnostic: contracting the full weight operand with a Hessian column slice first would produce an intermediate with at most 1,024 columns along the sliced axis. The actual intermediate shapes depend on contraction order. The tradeoff is more contractions and scalar reads; on CUDA, each `.item()` needs its partial result before the Python loop can continue. [inference; call_18f1e39716ea46e8b1559d14a81813ef, call_f5d9b07104f741f0a7e78868f1fe5b8b]

## Impact

Only the post-quantization metric calculation changes. The LDLQ search, reconstruction, and packing are untouched. Conversion still displays a nonnegative score to six decimal places or `(OoM)` for the negative sentinel. The repository accuracy test still does not distinguish that sentinel from a score below its threshold. [source; call_18f1e39716ea46e8b1559d14a81813ef, call_f5d9b07104f741f0a7e78868f1fe5b8b, call_2a2ee06adc5e4f89bd9e8be310d08797, call_48397237040a4969948cbe900cdef310]

## Source Notes

The original quantizer chapter describes the transformed-weight space and why the normalized Hessian proxy should not be treated as the original activation loss. The earlier metric-OoM entry describes the `-1.0` fallback and records the test's upper-bound-only check. [ancestor; call_6623592759154fceaa08fe29bb0b742b, call_b0a9d91f9d9a4675a86d4dd725dbdd2d]

Issue #34, “torch._C._LinAlgError on last layer of quant,” opens with a Cholesky failure. Separately, memmaptensor reports GEMM errors from `einsum` at the end of quantization and says a chunked implementation seemed to work. The connection to this patch is inferred from that specific match: the parent has two full `einsum` calls at the end of quantization, and the patch replaces both with chunked contractions. The discussion does not establish that this is the same implementation, that the reported GEMM errors were `OutOfMemoryError`, or that the task author was responding to the comment. [inference; call_cf028d09ba1f45f2871ce20439586edc, call_22d57948fbec4a2785f13073bf2a6ff6, call_18f1e39716ea46e8b1559d14a81813ef]

Closed issue #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” traces an output-head reshape failure to `preapply_had_r`; the thread reports a padding fix. Closed issue #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” traces a NaN-associated failure to Cholesky. Closed issue #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT,” also traces Cholesky failure after NaN warnings, but the reporter later could not reproduce it. Their relevance is inferred from the named quantizer and traceback stages; none points to the metric contraction. [inference; call_52fea109f2d84f5ab1847a1d83da7577, call_b656c5c1271444e1b461d1f47d3c92fc, call_dea7452a199846b498a1b08c8a1ccbf6, call_bcddea03c47146168407a0e76c26fc1b, call_c6af8ca6403b45ef8e49039d85e5bffa, call_263834427f3543c4a3811519bee9aa6b, call_18f1e39716ea46e8b1559d14a81813ef]

Issue #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” report Cholesky failures at some bitrates. Issue #53, “Command A support,” begins as a request for an EXL3 quant and later includes a Cholesky traceback even after resuming. The inferred connection is the shared `Linear.convert_exl3` → `quantize_exl3` path; the tracebacks end in `finalize_capture_H`/`block_ldl`, before the metric runs. [inference; call_7f8faa4ec1e649ad82b6552778b2edc5, call_5baee9ca929c4015af765d4951b2dd4b, call_75a9705f13894f60af18d30411ff53ba, call_edb20896dd424869a7e80c9d9f0f1175, call_f5d9b07104f741f0a7e78868f1fe5b8b]

The remaining path matches concern other mechanisms: PR #26, “Superior 3INST parameters,” proposes decoder multiplier changes; #33, “Error converting model,” opens with a file-open failure in `compile_model`; and #7, “quantizing model: undefined symbol: __cxa_call_terminate,” fails during the native extension import from the conversion entry point. Their inferred relevance is the shared EXL3 quantizer or conversion workflow, not the changed metric. [inference; call_ae4549f6e2d2469eaf50b24231991217, call_b9b420dffa9645b4890852aef24483c9, call_3757bba9aa884f478783770fd8cc6f47, call_18f1e39716ea46e8b1559d14a81813ef]

<a id="quantizer"></a>

## Evaluate the EXL3 proxy error in Hessian column blocks

`Linear.capture_H` accumulates activation Gram matrices in FP32. `finalize_capture_H` normalizes, damps and transforms the matrix before factorization. After `ldlq`, the metric uses regularized working weights `W = weight_r`, their residual `E = weight_r - weight_q`, and the transformed Hessian `Hd`. For an input-by-output matrix A, `ik,ij,jk->` computes `tr(Aᵀ Hd A)`, summing over all output channels. The ratio remains `trace(E) / max(trace(W), 1e-8)`, where each trace is Hessian-weighted and `1e-8` floors the denominator to avoid division by zero or a very small value. [source; call_9ca67d88531748bb9419be027a569504, call_263834427f3543c4a3811519bee9aa6b, call_f5d9b07104f741f0a7e78868f1fe5b8b, call_18f1e39716ea46e8b1559d14a81813ef]

The new local `block_trace(A, B)` walks `B.shape[1]` in spans of at most 1,024 input channels. Each call pairs `B[:, start:end]` with `A[start:end, :]` on index `j`, leaving the first `A` unsliced. The last span is clipped to fit, so the helper does not require a multiple of 1,024. It adds each scalar `.item()` result to a Python float, changing the floating-point grouping even though the algebra is unchanged. [source; call_18f1e39716ea46e8b1559d14a81813ef]

A bounded scalar transcription with nonzero off-diagonal Hessian entries produced identical full and chunked numerator/denominator sums: 74/138 for spans of 3, 3 and 1, and 270866/18492 for spans of 1,024 and 1. The latter exercises the helper's default-width boundary in isolation, not a shape accepted by the whole quantizer. [execution; call_8d578b7785cb40e48d44a5616a831074, call_18f1e39716ea46e8b1559d14a81813ef, call_263834427f3543c4a3811519bee9aa6b]

This is not end-to-end streaming: the existing greater-than-500-million-element rule may move the LDLQ working weights to CPU, but the metric still moves the full Hessian and each full weight operand to the selected device. It processes `E` and then `W`, clearing the local reference to `E` before transferring `W`. Only the metric's `torch.OutOfMemoryError` handler supplies `-1.0`; Hessian preparation and LDLQ run before it, and reconstruction and packing run after it. In particular, the parent source's separate Cholesky CPU retry handles memory failures, not a non-positive-definite input, and this patch leaves that distinction intact. [source; call_18f1e39716ea46e8b1559d14a81813ef, call_f5d9b07104f741f0a7e78868f1fe5b8b, call_263834427f3543c4a3811519bee9aa6b]

The only direct caller found is `Linear.convert_exl3`, which builds `LinearEXL3` from the packed tensors and forwards `proxy_err` unchanged, either alone or alongside reconstructed weights. Its two located callers are conversion `main` and `test_quant_dequant`. The former handles the sentinel for display; the latter still applies only an upper bound. Inspection of the task diff and parent code shows the earlier test defect is carried over, not introduced by chunking. [source; call_b76917199baf426ebfa7202be71b9cda, call_6e4e1c2ebb9f48e9af7e4d6443f3d2f9, call_9ca67d88531748bb9419be027a569504, call_2a2ee06adc5e4f89bd9e8be310d08797, call_48397237040a4969948cbe900cdef310, call_18f1e39716ea46e8b1559d14a81813ef]

## Authoring-time findings — pending review

### proxy-oom-sentinel-passes-test-bound (suspected; defect)

The quantization test's proxy-error assertion accepts an unavailable metric as though it met the accuracy bound. This behavior is inherited.

Trigger: `test_quant_dequant` calls `Linear.convert_exl3` with `return_weight_q=True`; metric computation raises a caught `torch.OutOfMemoryError`, and reconstruction and packing succeed so the test receives `proxy_err=-1.0`.

Expected: Distinguish an unavailable metric from a measured error before applying the bitrate-specific bound.

Actual: The assertion `proxy_err < max_proxy_err_per_K[K]` accepts `-1.0` for all eight tested bitrates. The separate weight and reconstruction checks still run, so this does not imply that the full test passes. Conversion `main` is not affected by this test defect; it displays `(OoM)`.

Locations: 69e728ef0b2aff6e45acfc0c48d390b1aef85a70:tests/test_quant_fn.py — test_quant_dequant

Source evidence: call_18f1e39716ea46e8b1559d14a81813ef, call_f5d9b07104f741f0a7e78868f1fe5b8b, call_b76917199baf426ebfa7202be71b9cda, call_6e4e1c2ebb9f48e9af7e4d6443f3d2f9, call_9ca67d88531748bb9419be027a569504, call_48397237040a4969948cbe900cdef310, call_2a2ee06adc5e4f89bd9e8be310d08797

source_inspection: Compared the task hunk to the parent metric handler and traced the unchanged return value through the only direct caller found to its two repository consumers. [call_18f1e39716ea46e8b1559d14a81813ef, call_f5d9b07104f741f0a7e78868f1fe5b8b, call_9ca67d88531748bb9419be027a569504, call_48397237040a4969948cbe900cdef310, call_2a2ee06adc5e4f89bd9e8be310d08797]. Limits: Establishes the conditional assertion behavior at the inspected call sites, not whether the configured test can hit an actual memory failure.

scalar_transcription: Compared the sentinel with all eight transcribed thresholds; all eight comparisons passed. [call_8d578b7785cb40e48d44a5616a831074]. Limits: No repository test, reconstruction, or allocation failure was executed.

## Uncertainty and limits

No PyTorch, CUDA, model conversion, repository test, or real allocation failure was executed. The scalar check uses exact Python integer sums and binary64 division; it does not reproduce tensor precision, floating-point reduction order, or GPU synchronization.

The source does not establish the contraction plan, peak memory savings, wall-clock effect, or why 1,024 was chosen. It also does not establish that the patch prevents any particular reported GEMM failure.

Caller coverage is limited to literal whole-parent-tree searches and the inspected call sites; dynamic or external callers were not established.
