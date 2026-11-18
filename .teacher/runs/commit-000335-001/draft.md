# 3be1ea105bdc1c214904d47ebc611ec001c5ed39


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3be1ea105bdc1c214904d47ebc611ec001c5ed39) · [Evidence ledger](draft.json)

Merges dev’s blockwise EXL3 proxy-error calculation into dev_tp. It preserves the Hessian-weighted formula in exact arithmetic and leaves quantization and packing unchanged. The existing out-of-memory sentinel still bypasses the test’s proxy-error bound.

- [Bring blockwise EXL3 proxy-error computation into dev_tp](#quantizer)

## Problem

Before the merge, dev_tp computed the EXL3 proxy error with two full-width Hessian contractions after LDLQ. A caught OutOfMemoryError in that diagnostic made the score unavailable even if the quantization search had completed. [source; call_85e9764b1d794cf5b7ac087f2223a870, call_b5a79e620a4e4e189e847d45e7361f40]

## Reasoning

The merge brings in dev's existing blockwise contraction, rather than introducing a separate implementation on dev_tp. The first-parent diff is a single quantize.py hunk, identical to the change in second parent 69e728ef. Both diffs produce the same quantize.py blob. The supplied tree comparisons distinguish file identity from tree identity: the merge tree differs from both parent trees. [source; call_85e9764b1d794cf5b7ac087f2223a870, call_80b25f606aef4985a4001204eaf464a5, call_dd84e2df593a46f1bd84741d95b03252]

Bounding one dimension of a contraction intermediate is a plausible reason to chunk the diagnostic. If einsum first contracts the full weight operand with the Hessian slice over input index i, the result spans at most 1,024 positions on j instead of the full input width. This trades a smaller possible intermediate for more contractions and scalar reads. A CUDA partial must be available before its .item() can be accumulated by Python; the patch does not specify the actual contraction plan. [inference; call_80b25f606aef4985a4001204eaf464a5, call_b5a79e620a4e4e189e847d45e7361f40]

## Impact

The first-parent change is confined to the post-LDLQ diagnostic. It does not alter tensor-parallel dispatch, the trellis search, reconstruction, or packing. Conversion still prints a nonnegative score to six decimal places or `(OoM)` for the negative sentinel. The accuracy test still treats that sentinel as below its error bound. [source; call_80b25f606aef4985a4001204eaf464a5, call_b5a79e620a4e4e189e847d45e7361f40, call_38b8253444294c37b59173e9908b74b8, call_bf7fa651ce4440b19ee28bf546795f8a]

## Source Notes

The original EXL3 quantizer chapter explains the transformed-weight space, LDLQ feedback, and the distinction between the proxy and original activation loss. The metric-OoM entry describes the separation of score availability from successful quantization and records the sentinel/test mismatch. The second-parent blockwise entry describes the same partition brought in by this merge and records that the mismatch persists there too. [ancestor; call_09e841c984274900a088bb01d5383036, call_a64e1ea0193b456bb86a1c08e10eccf0, call_6edde638e3e841f1aef155943412825d]

Issue #34, “torch._C._LinAlgError on last layer of quant,” opens with a Cholesky failure. Separately, memmaptensor reports late-quantization einsum GEMM errors and says chunking seemed to help. That comment is an inferred match to the two terminal metric einsums replaced here, not evidence that the merge responds to the comment, uses the same implementation, or catches the reported GEMM error. [inference; call_45ba781d76094a87aed35205acee772a, call_80b25f606aef4985a4001204eaf464a5, call_b5a79e620a4e4e189e847d45e7361f40]

The closed reports overlap the quantizer but point to different operations. #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” traces an output-head reshape in preapply_had_r and reports success after padding. #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” and #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT,” show non-positive-definite Cholesky failures and NaN warnings; the #58 reporter later could not reproduce the failure. The inferred connection is the shared quantizer path, not the post-LDLQ contraction. [inference; call_afbb4a5e56d545549c5987fb27bdd682, call_7308fcf0295e4b6b8b55465e4be167ef, call_f132ee0bdad74b9eb9ac70531c14f598, call_86397c6c0ef949f5a5503456bc21da32, call_8d1d2991b43642518297015c8f68e4b2, call_b5a79e620a4e4e189e847d45e7361f40]

Issue #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” report Cholesky failures at particular bitrates. #53, “Command A support,” starts as a request for an EXL3 quant and later reports a Cholesky failure that recurs on resume. Their tracebacks match the inspected Linear.convert_exl3 → quantize_exl3 → finalize_capture_H → block_ldl chain. That places the reported failures before the changed metric, not in it. [inference; call_7bbb5954d4c84d9fa1be5304f50a58f7, call_cc66ecd004724f8baebb6b2f1a7f39ce, call_0857e1c5bcc74bc08eca0c95ef38c4c4, call_870adb2c38334baea75ab03e8f97b85b, call_8d1d2991b43642518297015c8f68e4b2, call_b5a79e620a4e4e189e847d45e7361f40]

Other inferred workflow overlaps do not describe this metric: PR #26, “Superior 3INST parameters,” proposes a decoder multiplier; #33, “Error converting model,” opens with a file-open error in compile_model; and #7, “quantizing model: undefined symbol: __cxa_call_terminate,” fails importing the extension from the conversion entry point. The shared mechanisms are respectively the EXL3 quantizer and the conversion workflow, not the changed contraction. [inference; call_80b1719a81274dc288b299e3fc2e84ae, call_cb25dac22d59453abdb1272e3a42731a, call_77812b5ab3734b28ae7f477f282c0f8d, call_80b25f606aef4985a4001204eaf464a5]

<a id="quantizer"></a>

## Bring blockwise EXL3 proxy-error computation into dev_tp

Linear.capture_H accumulates FP32 activation Gram matrices; finalize_capture_H normalizes by the sample count, damps the diagonal, and applies sign flips and input Hadamards. After LDLQ, the metric uses the resulting transformed Hessian Hd, regularized working weights W = weight_r, and residual E = weight_r − weight_q. For input-by-output A, `ik,ij,jk->` sums A[i,k]·Hd[i,j]·A[j,k], i.e. tr(AᵀHdA). The numerator uses E and the denominator W. The unchanged 1e-8 denominator floor prevents division by zero or a very small denominator. [source; call_642a4afca54d46248074bc7730e670e3, call_8d1d2991b43642518297015c8f68e4b2, call_b5a79e620a4e4e189e847d45e7361f40, call_80b25f606aef4985a4001204eaf464a5]

The local block_trace slices Hessian columns and matching rows of the right weight operand on j. It leaves all Hessian rows and the left operand intact, so off-diagonal interactions across tile boundaries still contribute; this is not a block-diagonal approximation. The last span is clipped to the remaining input channels. The formula is preserved in exact arithmetic, but adding each .item() to a Python float changes the reduction grouping. [source; call_80b25f606aef4985a4001204eaf464a5]

A scalar transcription with nonzero off-diagonal Hessian entries gave the same full and blocked numerator/denominator pairs: 71/147 for spans of 3, 3, and 1, and 1,025,980/18,528 for spans of 1,024 and 1. The latter exercises the helper's default-width boundary in isolation. [execution; call_fdeafaab97f147f79d6fbcdd75663233]

The change is not an end-to-end streaming calculation. The existing rule moves working weights to CPU above 500 million elements for LDLQ, but the metric still transfers the full Hessian and full residual and reference operands to the chosen device, clearing the local E reference before transferring W. A metric OutOfMemoryError still produces -1.0. The earlier Cholesky CPU retry handles memory failures, not non-positive-definite input; later reconstruction and packing are also outside the metric handler. [source; call_b5a79e620a4e4e189e847d45e7361f40, call_8d1d2991b43642518297015c8f68e4b2, call_80b25f606aef4985a4001204eaf464a5]

The only direct quantize_exl3 caller found is Linear.convert_exl3, which installs LinearEXL3 from the packed output and passes through the metric unchanged, alone or alongside the reconstructed weight. The two located wrapper callers are conversion main and test_quant_dequant. The former interprets the sentinel; the latter does not. The current source also shows that the original chapter's repeated-column sampling observation no longer describes the active scale search: g_scale_gss uses `(i + w) % tiles_n`. In contrast, the original chapter's stale trellis-cost read remains before the metric and is not corrected by the merge. [source; call_4b3703c6e03347d1888aaa87447c8552, call_262a078c18f54b46b01bd1247a700d65, call_642a4afca54d46248074bc7730e670e3, call_38b8253444294c37b59173e9908b74b8, call_bf7fa651ce4440b19ee28bf546795f8a, call_8d1d2991b43642518297015c8f68e4b2, call_c96ab23eae8544fbaf8994badcc950aa, call_b7c34f44e5c3400a838e1a060fcf3f0d, call_0ff27caf4cc64d8f8b4d857d6c88ede4, call_80b25f606aef4985a4001204eaf464a5]

## Authoring-time findings — pending review

### proxy-oom-sentinel-passes-test-bound (suspected; defect)

The merge carries over the accuracy test's treatment of an unavailable proxy score as a successful error check.

Trigger: During test_quant_dequant, the metric raises a caught torch.OutOfMemoryError and the subsequent reconstruction and packing succeed, allowing Linear.convert_exl3 to return -1.0 and the reconstructed weights.

Expected: Distinguish an unavailable score from a measured error below the bitrate-specific threshold.

Actual: The test's strict upper-bound assertion accepts -1.0 for every tested K from 1 through 8. Independent weight checks still run. Conversion main instead prints `(OoM)`.

Locations: 3be1ea105bdc1c214904d47ebc611ec001c5ed39:tests/test_quant_fn.py — test_quant_dequant

Source evidence: call_80b25f606aef4985a4001204eaf464a5, call_b5a79e620a4e4e189e847d45e7361f40, call_4b3703c6e03347d1888aaa87447c8552, call_262a078c18f54b46b01bd1247a700d65, call_642a4afca54d46248074bc7730e670e3, call_bf7fa651ce4440b19ee28bf546795f8a, call_38b8253444294c37b59173e9908b74b8

source_inspection: Compared the complete first-parent hunk with the unchanged handler and traced the score through the only located direct caller to conversion main and the test. [call_80b25f606aef4985a4001204eaf464a5, call_b5a79e620a4e4e189e847d45e7361f40, call_642a4afca54d46248074bc7730e670e3, call_bf7fa651ce4440b19ee28bf546795f8a, call_38b8253444294c37b59173e9908b74b8]. Limits: Establishes the conditional behavior, not that the configured test can exhaust device memory or pass as a whole.

scalar_transcription: Compared -1.0 against the eight transcribed bounds; all eight comparisons were true. [call_fdeafaab97f147f79d6fbcdd75663233]. Limits: No allocation failure, repository test, or weight check was executed.

### trellis-first-pass-reads-stale-costs (suspected; defect)

The inherited first-pass trellis argmin reads the incoming cost buffer rather than the final cost buffer.

Trigger: A tile reaches quantize_tiles_kernel and completes the 256-step rotated forward pass. The native quantize_tiles dispatcher launches the kernel for the Python tile wrappers, which are used by LDLQ, scale sampling, and the direct tile tests.

Expected: Choose the first-pass terminal overlap by minimizing costs that include the final step, then use it to start backtracking.

Actual: argmin_cost reads temp_costs_inc, which holds costs from step 254 (zero-based), while temp_costs holds step 255. If their minimizing overlaps differ, backtracking starts from the wrong first-pass endpoint; the metric hunk does not change that selection.

Locations: 3be1ea105bdc1c214904d47ebc611ec001c5ed39:exllamav3/exllamav3_ext/quant/quantize.cu — quantize_tiles_kernel

Source evidence: call_b7c34f44e5c3400a838e1a060fcf3f0d, call_0ff27caf4cc64d8f8b4d857d6c88ede4, call_342a2130ed8c49dbafb67226a030ace6, call_649ed4d11c6e46ac83fe38b48895b0d3, call_2253e57399da4e9f9fbf289b5d3e3635, call_0206299cd0b9487f932604c1c4a01b51, call_8d1d2991b43642518297015c8f68e4b2, call_5687443fa0564aeebc03134bc6584acd, call_80b25f606aef4985a4001204eaf464a5

source_inspection: Checked which buffer the forward loop writes and which one the argmin consumes; traced the native launch and wrapper call sites in the parent. The merge changes only the later metric. [call_b7c34f44e5c3400a838e1a060fcf3f0d, call_0ff27caf4cc64d8f8b4d857d6c88ede4, call_342a2130ed8c49dbafb67226a030ace6, call_0206299cd0b9487f932604c1c4a01b51, call_80b25f606aef4985a4001204eaf464a5]. Limits: Establishes the read/write discrepancy, not whether a given tile's selected overlap or quantization error changes.

scalar_transcription: Swapped two mock buffer references before each write and stamped each write with its step index. At argmin, the output and incoming buffers carried 255 and 254 respectively. [call_4a1c8d26ba084ed1aead7e3437fce41e]. Limits: This models buffer ownership only; it does not run the kernel or model costs, thread synchronization, or quality.

## Uncertainty and limits

No PyTorch or CUDA quantization, allocation failure, repository accuracy test, or performance benchmark was executed. Contraction order, peak memory, wall-clock cost, and the reason for choosing 1,024 are unestablished.

The contraction transcription uses exact Python integer products and sums followed by binary64 scalar accumulation. It checks column coverage and arithmetic identity on the chosen inputs, not tensor rounding, strides, GPU synchronization, or whole-quantizer shape support.

Caller coverage is limited to literal parent-tree searches and inspected call sites; dynamic and external callers were not established.
