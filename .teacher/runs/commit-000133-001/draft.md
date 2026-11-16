# b73d0739044d14ebe12a73bdbd154c1f28b36f19


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b73d0739044d14ebe12a73bdbd154c1f28b36f19) · [Evidence ledger](draft.json)

Adds indexed, optionally weighted multi-GEMM through one cooperative CUDA launch, reusing existing kernels and dispatch. Performance is unmeasured; inspection identifies unchecked batch relationships and an inherited selector defect.

- [Indexed multi-GEMM in one cooperative launch](#quantized-inference)

## Problem

The existing outer kernel handles one quantized matrix per launch. This change adds an indexed sequence of matrix multiplications within one cooperative launch. [source; call_15364926baa24ee78fbc7ce7f3f3182d, call_a2f58fb919e64a109c16e7cabf824e12]

## Reasoning

Moving the sequence into the kernel can amortize host launch overhead while retaining the existing dequantization and tensor-core implementation. The matrices are processed sequentially, not concurrently; any performance benefit remains unmeasured. [inference; call_20a8c545d2794ea39eedf9dd97e36703, call_a2f58fb919e64a109c16e7cabf824e12, call_a059b5f0b7834bc69f22e6910c72c011]

## Impact

A new Python extension binding exposes exl3_mgemm. The change adds native dispatch and kernel implementations but no Python workflow calling the new operation. [source; call_3b8d230adeaa4fdab5954cde71171889, call_74d4c87185dc416c9358c9fc7ff54c5f, call_20a8c545d2794ea39eedf9dd97e36703]

## Source Notes

The earlier optimization entry records a Boolean-versus-dimension defect in select_gemm_shape. Fresh inspection finds that expression unchanged and now reused by multi-GEMM. [ancestor; call_f43978e213724ca18b01246a7009329b]

Issue #5, “Will exl3 quants need requanting later?”, asks about format stability and Ampere support. Turboderp replies that storage-format changes are not intended and distinguishes working support from desired performance. [source; call_ef04952bbb6a4ab4a5915fc29b9ab357]

That discussion is background rather than an established motivation for this commit: its concrete overlap is EXL3 GEMM and performance, not the new indexed multi-matrix interface. [inference; call_ef04952bbb6a4ab4a5915fc29b9ab357, call_20a8c545d2794ea39eedf9dd97e36703]

<a id="quantized-inference"></a>

## Indexed multi-GEMM in one cooperative launch

The actual interface differs from the copied single-matrix comment: A and C are rank-three tensors, while B, suh and svh are rank-one int64 tensors containing device addresses. A is FP16; C is FP16 or FP32. K supplies the shared weight bit width. Indices are required despite their optional C++ type; weights remain optional. [source; call_20a8c545d2794ea39eedf9dd97e36703, call_fd7fc42d6fde40cc83488b54865de4fd, call_43fd3ccd8bb94ba38a805ce7dbae1dcd]

For each i below max(A.size(0), C.size(0)), the kernel reads B_indices[i] and selects matching quantized-weight and scale pointers. It transforms A into A_had, synchronizes the grid, performs GEMM in 16-row chunks, and transforms C in place. Optional B_weights[i] multiplies the output-transform normalization. Grid synchronization separates successive matrix iterations. [source; call_a2f58fb919e64a109c16e7cabf824e12]

An input leading dimension of one reuses the same input across selected matrices; otherwise A and A_had advance by m*k elements. C advances by m*n elements only when its leading dimension exceeds one. Reusing C is not a cross-matrix sum: the inner GEMM initializes its accumulators and overwrites the destination for each multiplication. [source; call_a2f58fb919e64a109c16e7cabf824e12, call_a059b5f0b7834bc69f22e6910c72c011]

Unlike the single-GEMM wrapper's conditional transforms, multi-GEMM always performs both transforms and requires usable scratch and scale-pointer lists. The helpers process 128 elements per warp using a four-element transform followed by a 32-lane shuffle transform. The normalization constant is 1/sqrt(128); FP16 output is rounded before its half-precision post-scale multiplication. [source; call_15364926baa24ee78fbc7ce7f3f3182d, call_a2f58fb919e64a109c16e7cabf824e12, call_0ceccc9f7a944f1b87a24155db72d348]

A standard-library calculation gives 1/sqrt(128)=0.08838834764831843, matching the kernel's decimal constant to its stated precision. The indexing model also confirms input broadcasting for leading dimensions (1,2) and paired traversal for (2,2). [execution; call_a30c71f03a4143f39a1a13fed4dc3f3a]

The multi-GEMM tables instantiate all eight bit widths with both output types and the existing four shapes. Their (M,K,N,shared stages,fragment stages) tuples are (16,16,128,3,2), (16,32,128,4,3), (16,32,256,4,3) and (16,16,512,4,3). Thread counts remain 256,512,512,256. [source; call_bd76e4e29c2a4d09b82c8a3de5efe624, call_fd7fc42d6fde40cc83488b54865de4fd, call_5da18e32613949a29de1a4ae9cc56acc, call_27e3ae83f6b94a2e9e8245a1af2424ac, call_2f054d5ea9b342d3b2c82cb194811006, call_3c3187aeea814c1997291900b918172e, call_d293e76d830c4a26b08f8b2041cced93, call_27a03b2cfbf84db4afd2fb423f3e831f, call_0ee1106aed36494f98e79fd4ca48cb5f, call_4c08699744ed4257af64323075859918]

Dispatch reuses select_gemm_shape unless a positive forced index is supplied. It caps cooperative blocks by the number of K-by-N tiles divided by 12, following the existing experimentally chosen heuristic. The reused inner kernel requires tile divisibility, reserves 90 KiB of dynamic shared memory, stages packed weights asynchronously, dequantizes fragments and uses locked partial-output reduction. [source; call_cbcdb428574e402db736ad2085334ce1, call_cc98726f640145c6be6218c46e986932, call_a059b5f0b7834bc69f22e6910c72c011]

The existing single-GEMM path is retained. Its only kernel-body edits remove redundant braces and move each grid barrier after local pointer and row-count updates, still before the next multiplication or output transform. [source; call_a2f58fb919e64a109c16e7cabf824e12]

## Authoring-time findings — pending review

### multi-gemm-leading-dimension-validation (suspected; defect)

The wrapper accepts leading-dimension combinations that the kernel's maximum-length traversal cannot safely consume.

Trigger: For otherwise suitable contiguous tensors, use A leading dimension 2, C leading dimension 1 and indices shape (1,1); alternatively use leading dimensions 2 and 3 with indices shape (1,3).

Expected: Reject incompatible dimensions or ensure every iteration has valid input, scratch and index storage.

Actual: The first case passes the indices-width check but reads B_indices[1] beyond the one-element tensor. The second advances A to a nonexistent third input matrix. The wrapper does not validate the leading-dimension relationship. Reach established here is the newly exported exl3_mgemm binding; the whole-parent search found no existing literal callers.

Locations: b73d0739044d14ebe12a73bdbd154c1f28b36f19:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm, b73d0739044d14ebe12a73bdbd154c1f28b36f19:exllamav3/exllamav3_ext/quant/exl3_gemm_kernel.cuh — exl3_mgemm_kernel

Source evidence: call_20a8c545d2794ea39eedf9dd97e36703, call_a2f58fb919e64a109c16e7cabf824e12, call_150376bde74443279c853abfc747945f, call_74d4c87185dc416c9358c9fc7ff54c5f, call_3b8d230adeaa4fdab5954cde71171889

scalar_transcription: Modeled the wrapper's indices-width equality, maximum iteration count and input advancement for four leading-dimension combinations. [call_a30c71f03a4143f39a1a13fed4dc3f3a]. Limits: Checks address-index bounds symbolically, not CUDA execution or the resulting device failure.

### inherited-boolean-shape-threshold (suspected; defect)

The unchanged automatic shape selector carries its Boolean threshold defect into multi-GEMM.

Trigger: Automatic Hopper/Blackwell selection with bits<=6 and n<=4096, for example bits=3, k=16384 and n=4096.

Expected: A dimensional threshold should distinguish qualifying dimensions; the precise intended replacement condition is not established.

Actual: (size_k && bits >= 3) is Boolean and cannot exceed 8192, so this branch always returns shape 2. Parent-tree search identifies the existing select_exl3_gemm_kernel caller; the task adds select_exl3_mgemm_kernel as another direct caller. Positive forced shape indices bypass the expression.

Locations: b73d0739044d14ebe12a73bdbd154c1f28b36f19:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cu — select_gemm_shape

Source evidence: call_cc98726f640145c6be6218c46e986932, call_cbcdb428574e402db736ad2085334ce1, call_961767e4424d44ce960c87f2724d30cf

source_inspection: Compared the parent selector and its direct caller with the added multi-GEMM dispatcher; the defective expression is carried over unchanged. [call_cc98726f640145c6be6218c46e986932, call_cbcdb428574e402db736ad2085334ce1]. Limits: No performance consequence or intended alternative threshold established.

scalar_transcription: Evaluated the Boolean comparison for nine representative k/bit-width combinations; every comparison was false. [call_a30c71f03a4143f39a1a13fed4dc3f3a]. Limits: Python expression model, not execution of the repository selector.

## Uncertainty and limits

No CUDA compilation, GPU execution, numerical comparison or timing benchmark was performed.

Python checks model indexing and scalar arithmetic only; they do not test GPU memory access, synchronization, floating-point rounding or cooperative-launch viability.

External and dynamically constructed callers are not established by the parent-tree literal search.

The empirical rationale for device-specific shape thresholds is unestablished; the inherited divisor 12 is documented only as experimentally chosen.
