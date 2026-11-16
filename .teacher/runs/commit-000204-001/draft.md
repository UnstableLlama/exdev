# 1ad855ada6db1e3ad06b679acd08737f6edd101b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1ad855ada6db1e3ad06b679acd08737f6edd101b) · [Evidence ledger](draft.json)

Catches OoM during post-quantization proxy-error computation and reports an unavailable metric while allowing conversion to continue; the existing accuracy test does not recognize the new sentinel.

- [Make proxy-error computation optional under memory pressure](#conversion)

## Problem

After quantization completed, computing the diagnostic proxy error could still abort conversion on an out-of-memory exception. [source; call_ae3941d6373a40a49369e1085efe0990, call_d5a362ef0a5b455da87e1da197aff1bd]

## Reasoning

The change treats metric availability separately from quantized-weight availability: it preserves completed quantization and substitutes a negative sentinel when metric computation runs out of memory. [source; call_ae3941d6373a40a49369e1085efe0990]

## Impact

Conversion can proceed past a caught metric OoM, displaying '(OoM)' instead of a numeric error. This is not general OoM recovery: earlier quantization and subsequent reconstruction or packing remain outside the handler. [source; call_2aeb5cc376f24b9a8abd7b391fedd794, call_ae3941d6373a40a49369e1085efe0990, call_d5a362ef0a5b455da87e1da197aff1bd]

## Source Notes

The root quantizer entry describes the existing Hessian-guided quantization, working-space diagnostic and CPU-buffer memory tradeoff. The image-dump entry establishes the optional diagnostic path through Linear.convert_exl3 into quantize_exl3; neither entry supplies evidence of successful OoM recovery. [ancestor; call_4e8a0c02aec14a98abc6485bdcae0962, call_97453f707d474f2f92fb3a3a45135004]

Issue #34, 'torch._C._LinAlgError on last layer of quant', principally reports Cholesky failure. A later comment reports einsum GEMM errors and a chunked workaround. Its possible connection is inferred from the same einsum metric mechanism; neither that comment nor the traceback establishes the specific OutOfMemoryError caught here. [inference; call_04f7b6164e554c53b3aadc6963dd4e88, call_ae3941d6373a40a49369e1085efe0990]

Other conversion reports concern distinct stages: #8 reports an invalid reshape, #11 a bias datatype assertion, #16 an invalid CUDA configuration, #38 Nemotron tensor dimensions, #43 abliterated Qwen3 Cholesky failure, and PR #13 missing bos_token_id handling. Their connection here is only inferred from shared conversion files or call chains, not evidence that this patch fixes them. [inference; call_86552a81f4704e749328125893d26edc, call_b33eeddcd9ce45cb964eea852a2a17b1, call_12f3f8c90ff24f11bae48f427f4d80fb, call_672a9bb42a0b41039e280aeed79f090b, call_b09c2b796fab4cebba2013cc433f2163, call_8db14873c975422c9afe015d5079f9c3, call_ae3941d6373a40a49369e1085efe0990]

PR #26, 'Superior 3INST parameters', discusses codebook experiments; #33, 'Error converting model', begins with file-opening failure and later discusses GLM inference; #42 reports NaNs and Cholesky failure at 3.0 bpw. Shared quantizer or conversion paths provide only an inferred contextual connection, not a demonstrated motivation for this patch. [inference; call_c072966272aa469da06f8ad0cbcd9514, call_fcaa68c95eb647d6b6d271446a209514, call_6b7699d8d2de4f95bd4488e165f0739b, call_894ce137bf1f4ca497da6afe8576045d, call_0bb79e71638148a699b56fe6e4d9ae5f, call_ae3941d6373a40a49369e1085efe0990]

<a id="conversion"></a>

## Make proxy-error computation optional under memory pressure

quantize_exl3 computes the metric after ldlq returns reconstructed working weights and encoded indices. With E = weight_r − weight_q, each einsum sums A[i,k] H[i,j] A[j,k] over all indices: the numerator uses E and the denominator uses weight_r. The existing 1e-8 floor prevents division by a zero or very small denominator. [source; call_d5a362ef0a5b455da87e1da197aff1bd]

Even when working weights were moved to CPU by the existing greater-than-5e8-element threshold, the metric transfers H, E and W to the selected compute device. The patch encloses subtraction, transfers, contractions and normalization in one try block; it does not implement chunking or CPU retry. [source; call_d5a362ef0a5b455da87e1da197aff1bd, call_ae3941d6373a40a49369e1085efe0990]

On success the formula is unchanged. On torch.OutOfMemoryError, weight_r, E, W and Hd are set to None and proxy_err becomes -1.0. Assignments replace deletions on the normal path too, while the exception path can clear names even if failure occurred before their initialization. Quantized weights and encoded indices remain available for the unchanged downstream work. [source; call_ae3941d6373a40a49369e1085efe0990, call_d5a362ef0a5b455da87e1da197aff1bd]

Whole-parent-tree searches locate one direct quantize_exl3 caller, Linear.convert_exl3, which forwards the metric unchanged after constructing LinearEXL3. Its two callers are conversion main and test_quant_dequant. Main is updated to format nonnegative values with six decimals and otherwise show '(OoM)'; the test remains on its old upper-bound-only interpretation. [source; call_b71a145eba9049f5a54bfdc0acf15576, call_7970f2e8f90945318464428a02ae02e1, call_70a9370d8e854ddfa0935fe6c2b47d70, call_7dfbdc899f1840bd805a6f8b2bb6a562, call_1bc5fb77484d45b3befde59b61cb9cb8, call_2aeb5cc376f24b9a8abd7b391fedd794]

The paired edits implement a producer/consumer contract: -1.0 means unavailable rather than exceptionally good accuracy, and conversion's display translates that status. Skipping this diagnostic favors retaining completed quantization work over obtaining a metric, without changing the encoded output algorithm. [inference; call_ae3941d6373a40a49369e1085efe0990, call_2aeb5cc376f24b9a8abd7b391fedd794]

A bounded scalar transcription produced numerator 0.46 and denominator 46 for E = 0.1W, yielding approximately 0.01. It also confirmed that -1.0 passes every existing proxy-error test threshold for K=1 through 8. [execution; call_586cc18cefd64727938507ad32941ecb]

## Authoring-time findings — pending review

### proxy-sentinel-test (suspected; defect)

The unchanged quantization test accepts an unavailable metric as satisfying its accuracy bound.

Trigger: Metric computation raises a caught OutOfMemoryError, and subsequent reconstruction and packing succeed so test_quant_dequant receives proxy_err=-1.0.

Expected: The proxy-error check should distinguish an unavailable metric from a measured error below its threshold.

Actual: assert proxy_err < max_proxy_err_per_K[K] accepts -1.0 for every tested bitrate. Independent weight checks still run, so this does not establish that the entire test passes.

Locations: 1ad855ada6db1e3ad06b679acd08737f6edd101b:tests/test_quant_fn.py — test_quant_dequant

Source evidence: call_1bc5fb77484d45b3befde59b61cb9cb8, call_ae3941d6373a40a49369e1085efe0990, call_7dfbdc899f1840bd805a6f8b2bb6a562, call_7970f2e8f90945318464428a02ae02e1

source_inspection: Traced the new sentinel through the sole direct quantizer caller to both located consumers; conversion main handles it, but the test does not. [call_70a9370d8e854ddfa0935fe6c2b47d70, call_7970f2e8f90945318464428a02ae02e1, call_1bc5fb77484d45b3befde59b61cb9cb8]. Limits: Reach is the inspected repository call sites, not external callers.

scalar_transcription: Compared -1.0 with all eight transcribed test thresholds; all comparisons returned true. [call_586cc18cefd64727938507ad32941ecb]. Limits: No repository test or real OoM was executed.

## Uncertainty and limits

No PyTorch conversion, actual allocation failure, CUDA kernel or allocator recovery was executed. Clearing local references does not establish that subsequent allocations succeed.

The scalar check uses Python binary64 arithmetic and transcribed expressions, not PyTorch einsum or GPU reduction ordering.

The handler specifically catches torch.OutOfMemoryError; coverage of other allocator or GEMM failure representations is unestablished.
