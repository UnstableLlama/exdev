# ea62df9eee39fd86654971a4001cb0f846b09020


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ea62df9eee39fd86654971a4001cb0f846b09020) · [Evidence ledger](draft.json)

EXL3 multi-GEMM can use fewer indices than allocated matrix slots without resizing its buffers. Existing attention and ordinary expert calls keep their behavior. The relaxed check bounds index traversal but admits some incompatible input/output sizes and an empty batch that still reaches launch.

- [Separate active MGEMM indices from allocated batch capacity](#quantized-inference)

## Problem

The indexed EXL3 multi-GEMM wrapper required the number of matrix indices to equal the number of output slots. That rejected a shorter index list even when the caller had enough output and scratch storage. The commit message describes allowing shorter lists; the implementation also accepts some lists larger than the output batch when they fit the input batch. [source; call_c3408b079191436db72ecf021afe3fb7, call_e1b125485e6c4bc4b277adc9ed1bb159, call_815c7d0fce2d43389265b272f9d39e71]

## Reasoning

The wrapper now reads N = indices.size(1), rejects N only if it exceeds both A.size(0) and C.size(0), and caps each local matrix count at N. It does not resize either tensor. The unchanged kernel iterates to the maximum of those capped counts, so an indexed invocation that reaches the kernel has N matrix iterations. The capped output count also bounds launch concurrency. The selector still uses the same per-matrix dimensions, bit width and output dtype; the change affects how many matrices run, not which GEMM specialization is selected. [source; call_e1b125485e6c4bc4b277adc9ed1bb159, call_0a220a3cb5be4c9d8a2bf8e04c42f174, call_aa337b3240ef41f4b245f90c6e288714, call_473e856e554b429dbbb4d2499d9ecec2]

The useful case is reusing a larger allocation for a smaller active set: with one broadcast input, eight output slots and four indices, only the first four slots participate. A stricter wrapper could preserve that use while separately requiring output capacity for every active matrix, either one broadcast input or sufficient input slots, and enough transformed-input scratch. Bounding index traversal alone does not enforce those conditions. [inference; call_e1b125485e6c4bc4b277adc9ed1bb159, call_aa337b3240ef41f4b245f90c6e288714, call_5455199f60de41649972091eca22784a]

## Impact

Whole-parent literal search found the extension binding and four direct Python calls. Attention.project_qkv passes no indices or weights, so its two-slot K/V projection bypasses the changed branch; it allocates two scratch slots and uses the fused path only when the helper exists and flattened token count is at most 32. BlockSparseMLP.forward has three indexed calls on its fused path: gate and up broadcast one token into fixed per-expert buffers; down consumes the per-expert activations and supplies routing weights. Ordinary top-k routing supplies exactly the configured slot count, so all three calls retain their existing effective sizes. [source; call_e243af5795bc4cdaace6952d1e485210, call_45872b19ca794b7a810d1e1bf5578078, call_ddd6252234f74c4baec0e7ef4ea099d5, call_fce86c4246c649fc830cff5f25804361, call_e1b125485e6c4bc4b277adc9ed1bb159]

An earlier leading-dimension defect is narrowed, not eliminated. Capping both local counts prevents the kernel's index-position counter from exceeding the supplied list length on accepted indexed calls. It still does not validate the matrix IDs in that list, or guarantee that indexed input, output, scratch and optional weight accesses are backed by storage. [source; call_3a02000a3b0242c0a55516e8427918d7, call_e1b125485e6c4bc4b277adc9ed1bb159, call_0a220a3cb5be4c9d8a2bf8e04c42f174, call_aa337b3240ef41f4b245f90c6e288714]

## Source Notes

The read ancestor entries establish the relevant history: “Add multi-GEMM kernel” describes the indexed cooperative launch and flags unequal leading dimensions; “MGEMM: Use full grid when possible” describes adding concurrent matrix groups and flags the scratch-capacity and zero-slice cases; the fused-attention entry explains why K/V supplies no indices; the routed-expert entry records the fixed-buffer mismatch when all experts are requested. [ancestor; call_5481cbec96b0455c863701843d940da0, call_d8fd91b19adf49a9a9780dbfa9abd653, call_8ccc6176b7fa436499f32072f307f8f3, call_87efbbd2248b4e079b2deecb1a8a72da]

The Boolean-versus-dimension selector defect recorded in the original MGEMM entry is already absent in this task's parent: the automatic Hopper/Blackwell branch for N divisible by 256 and at most 4096, after higher bit widths have been handled, tests size_k > 8192 and bits >= 3 separately. The task leaves that expression untouched. A scalar transcription at three bits and output width 4096 returned shape 2 for K=8192 and shape 3 for K=16384. [source; call_dba06acaad80412f8e56f78a5aed27f9, call_e1b125485e6c4bc4b277adc9ed1bb159, call_5455199f60de41649972091eca22784a]

The related discussions have different framing: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native extension import failure; #26, “Superior 3INST parameters,” proposes a codebook multiplier; #33, “Error converting model,” reports a safetensors file-open failure; #34, “torch._C._LinAlgError on last layer of quant,” reports a Cholesky failure; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” reports nonfinite state and failed Cholesky; #52, “Error converting moonshotai/Kimi-Dev-72B,” reports Cholesky failure at several bitrates; and #53, “Command A support,” requests support or an available EXL3 quant. [source; call_efcfebc23a094f219b458015a9a19b31, call_c21d55bc7312401caa54d62a5544cd1a, call_7b851f817b354d3cbf12f7630c86fe4b, call_2caa2e31bd204912a94bed019701d95e, call_bcc014ba01504407a2ca64da7eed0f6c, call_b9797d508f0d4e5292544f0513e1052e, call_96831baa8b904c55b6ad43b4d0172bb8]

These are contextual matches, not evidence of the reported reason for the fix: issue #7 names the extension that exposes the binding but fails before calling it; PR #26 discusses MCG multiplier selection, which the wrapper already supports and this diff does not edit; the conversion reports share convert_model.py with the inspected calibration code but their reported traces do not identify the MGEMM index check. The Command A request shares the broader EXL3 conversion context, not the changed matrix-count contract. [inference; call_e243af5795bc4cdaace6952d1e485210, call_0a220a3cb5be4c9d8a2bf8e04c42f174, call_0d0de0d974d8496d89b71e2d05d2503e, call_e1b125485e6c4bc4b277adc9ed1bb159, call_efcfebc23a094f219b458015a9a19b31, call_c21d55bc7312401caa54d62a5544cd1a, call_7b851f817b354d3cbf12f7630c86fe4b, call_2caa2e31bd204912a94bed019701d95e, call_bcc014ba01504407a2ca64da7eed0f6c, call_b9797d508f0d4e5292544f0513e1052e, call_96831baa8b904c55b6ad43b4d0172bb8]

<a id="quantized-inference"></a>

## Separate active MGEMM indices from allocated batch capacity

The leading axis of A and C counts matrix slots, not token rows. A and C still share the row count on axis 1; the separate rank-two indices tensor supplies its active count on axis 1. For active slot j, the kernel uses indices[j] to choose EXL3 weight and transform pointers, uses A slot zero only when the effective input count is one, and writes scratch and C by j. When weights are present, it scales each slot's output and sums the active outputs into slot zero. Inactive capacity at the end of a larger buffer is not cleared or reduced. [source; call_3a02000a3b0242c0a55516e8427918d7, call_e1b125485e6c4bc4b277adc9ed1bb159, call_aa337b3240ef41f4b245f90c6e288714]

The grid's z width is min(total device SMs / selected SMs per matrix, effective output slots). The selector limits SMs per matrix using the K-by-N tile count divided by 24 for tile-aligned dimensions; for shape 2 the tiles are 32 by 128. Reducing active output slots can reduce concurrent matrix groups without changing that tile choice. [source; call_0a220a3cb5be4c9d8a2bf8e04c42f174, call_473e856e554b429dbbb4d2499d9ecec2, call_d6c932fabbbd4c188e63bac9c854efcf, call_e1b125485e6c4bc4b277adc9ed1bb159]

A scalar transcription confirmed that (input slots, output slots, index count) of (1,8,4) and (8,8,4) both change from rejection to four iterations. For (8,1,1), the old check passed but the old iteration bound was eight; the new bound is one. The same check exposed input or output overruns for some newly accepted unequal batches. [execution; call_5455199f60de41649972091eca22784a]

## Authoring-time findings — pending review

### asymmetric-indexed-batch-capacity (suspected; defect)

The relaxed check allows the larger tensor to satisfy the predicate even when the other tensor cannot cover the kernel's traversal.

Trigger: Call the bound exl3_mgemm with otherwise suitable tensors, valid weight IDs and (input slots, output slots, index count) of (4,2,4) or (2,4,3), with positive launch width.

Expected: Reject the incompatible capacity or ensure every active matrix has a readable input and writable output.

Actual: Both cases used to fail the equality check. The first now visits output slots 2 and 3 beyond C; the second reads input slot 2 beyond A, since only an effective input size of one broadcasts. No inspected indexed Python caller constructs these particular shapes; the extension binding is the established reach.

Locations: ea62df9eee39fd86654971a4001cb0f846b09020:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm, e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/exllamav3_ext/quant/exl3_gemm_kernel.cuh — exl3_mgemm_kernel

Source evidence: call_e1b125485e6c4bc4b277adc9ed1bb159, call_aa337b3240ef41f4b245f90c6e288714, call_e243af5795bc4cdaace6952d1e485210, call_fce86c4246c649fc830cff5f25804361

scalar_transcription: Modeled acceptance, clamping and input/output slot offsets for both cases. [call_5455199f60de41649972091eca22784a]. Limits: Symbolic bounds, not observed device accesses.

### empty-indices-zero-grid (suspected; defect)

An empty index list now passes validation against a nonempty output allocation.

Trigger: Call the bound exl3_mgemm with rank-two indices of shape (1,0), positive allocated input and output batch sizes and otherwise compatible dimensions that yield a positive selected SM count.

Expected: Reject an empty active set explicitly or return without a launch.

Actual: Both effective counts become zero, grid z becomes zero, and the wrapper still attempts the cooperative launch. The inspected attention call has no indices and the three ordinary fused expert calls use the configured top-k count; no stock empty-list caller was identified.

Locations: ea62df9eee39fd86654971a4001cb0f846b09020:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm

Source evidence: call_e1b125485e6c4bc4b277adc9ed1bb159, call_0a220a3cb5be4c9d8a2bf8e04c42f174, call_e243af5795bc4cdaace6952d1e485210, call_45872b19ca794b7a810d1e1bf5578078, call_fce86c4246c649fc830cff5f25804361

scalar_transcription: Checked that (1,8,0) now passes and clamps to (0,0); inspected the subsequent grid construction and launch. [call_5455199f60de41649972091eca22784a, call_0a220a3cb5be4c9d8a2bf8e04c42f174]. Limits: No CUDA error or return value was measured.

### all-experts-still-exceed-fused-capacity (suspected; defect)

The relaxed bound still does not support all-expert routing with the fixed fused buffers.

Trigger: Call BlockSparseMLP.forward with one flattened token, fully EXL3 expert projections, activate_all_experts=True and more total experts than configured experts per token.

Expected: Evaluate all experts using adequate storage or route through the nonfused implementation.

Actual: Routing produces one index per expert, but the gate call has one input slot and only the configured top-k number of output slots. The new predicate rejects the gate call before up or down runs. This is a conditional module path: conversion supplies the flag during intended unquantized calibration, which is not evidence that ordinary conversion reaches the fully EXL3 branch.

Locations: e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward, ea62df9eee39fd86654971a4001cb0f846b09020:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm

Source evidence: call_ddd6252234f74c4baec0e7ef4ea099d5, call_fce86c4246c649fc830cff5f25804361, call_4ee53c1e09ec4211b761e05bf28ae846, call_d5698b1871bb42418c6c9bc7dd53bde9, call_0d0de0d974d8496d89b71e2d05d2503e, call_e1b125485e6c4bc4b277adc9ed1bb159

scalar_transcription: Checked the new predicate for one input slot, two output slots and eight expert indices. [call_5455199f60de41649972091eca22784a]. Limits: No router, model, conversion workflow or extension was executed.

### broadcast-scratch-capacity-unchecked (suspected; defect)

The earlier per-matrix scratch requirement remains unchecked.

Trigger: Supply one broadcast input, more than one active matrix and A_had with room for only the input's single matrix.

Expected: Reject insufficient scratch or manage scratch so every transform uses a valid slot.

Actual: The kernel broadcasts A but writes and reads scratch at j * size_m * size_k. The cap does not check scratch storage. The inspected K/V and routed-expert call sites allocate scratch per projection or configured expert slot; the undersized-scratch case is established at the extension interface, not those calls.

Locations: e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/exllamav3_ext/quant/exl3_gemm_kernel.cuh — exl3_mgemm_kernel

Source evidence: call_aa337b3240ef41f4b245f90c6e288714, call_3a02000a3b0242c0a55516e8427918d7, call_e1b125485e6c4bc4b277adc9ed1bb159, call_45872b19ca794b7a810d1e1bf5578078, call_ddd6252234f74c4baec0e7ef4ea099d5, call_fce86c4246c649fc830cff5f25804361

source_inspection: Compared A and scratch address calculations with the wrapper checks and direct callers' allocations. [call_aa337b3240ef41f4b245f90c6e288714, call_e243af5795bc4cdaace6952d1e485210, call_45872b19ca794b7a810d1e1bf5578078, call_ddd6252234f74c4baec0e7ef4ea099d5, call_fce86c4246c649fc830cff5f25804361]. Limits: No GPU memory violation was observed.

### zero-selected-sms-persists (suspected; defect)

The inherited division-by-zero path is still present; changing the active batch bound does not protect the per-matrix grid width.

Trigger: Call the binding with otherwise compatible tensors, valid bit width, nonempty active work, K and N both 128, and shape 2 forced.

Expected: Reject the unsupported grid explicitly or retain at least one SM block.

Actual: The selector's current divisor gives (128/32) * (128/128) / 24 = 0 in integer arithmetic, so the wrapper evaluates total_sms / num_sms with a zero denominator before launch. The four inspected Python calls use automatic shape selection; none supplies this forced-shape trigger.

Locations: e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cu — select_exl3_mgemm_kernel, ea62df9eee39fd86654971a4001cb0f846b09020:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm

Source evidence: call_d6c932fabbbd4c188e63bac9c854efcf, call_473e856e554b429dbbb4d2499d9ecec2, call_0a220a3cb5be4c9d8a2bf8e04c42f174, call_e1b125485e6c4bc4b277adc9ed1bb159, call_e243af5795bc4cdaace6952d1e485210, call_45872b19ca794b7a810d1e1bf5578078, call_fce86c4246c649fc830cff5f25804361

scalar_transcription: Computed the selector cap using the shape-2 tile sizes and current divisor. [call_5455199f60de41649972091eca22784a]. Limits: Did not execute the native division or observe its runtime manifestation.

## Uncertainty and limits

No CUDA compilation, GPU launch, numerical comparison or timing was performed. The Python check transcribes bounded integer arithmetic and symbolic slot indices, not native integer narrowing or overflow, GPU memory accesses, synchronization or launch error behavior.

The whole-parent literal search does not establish external or dynamically resolved callers. It does not establish that a stock model or conversion run supplies the newly accepted asymmetric or empty shapes.

The message establishes the requested capacity change, but not the specific caller or workload that motivated it. The source does not establish why the current MGEMM slice divisor is 24.
