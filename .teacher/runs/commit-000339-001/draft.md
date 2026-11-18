# e14fa3cf22ff9c4203736690522c7baaf17dd57b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/e14fa3cf22ff9c4203736690522c7baaf17dd57b) · [Evidence ledger](draft.json)

Guards automatic EXL3 GEMM shape selection against incompatible output widths, repairs a Hopper/Blackwell K threshold, and synchronizes the selector declaration. Scalar checks demonstrate the dispatch arithmetic, not GPU correctness or speed; separate multi-GEMM launch and input-validation issues remain.

- [Choose EXL3 GEMM tiles that cover the output width](#gemm)

## Problem

The commit describes a GEMM mapping fix for “some odd tensor shapes.” Here, “odd” includes output widths N that are multiples of 128 but not 256. Several automatic dispatch branches could select shape 3, whose 256-column tiles do not cover those widths. The kernel rounds the N tile count down; it does not run a partial output tile. [source; call_8ea91d7bf10f4e44814d63c705065697, call_0ac71f39100d4148895fe03424ec3c17, call_3393a7ae877d4e478e1107ca61ddc70b, call_6ee8c689f6b64f2d9479e75c6cf67a79]

A separate Hopper/Blackwell branch compared `(size_k && bits >= 3)` with 8192. The left side is Boolean, so the branch could never select shape 3. The header also still declared a five-argument selector even though the definition and both internal callers already used six arguments. [source; call_0ac71f39100d4148895fe03424ec3c17, call_4d211a8a76e743aea6b286e3bedfb769]

## Reasoning

The added `N % 256 == 0` tests make tile compatibility a prerequisite for the affected shape-3 preferences. Those tests also make the corrected Hopper/Blackwell K threshold safe with respect to N: repairing the comparison alone would let that branch choose shape 3 for a sufficiently large K even when N could not fill 256-column tiles. [source; call_40831d8b34cf4edeb9683ccbde66ab82, call_3393a7ae877d4e478e1107ca61ddc70b]

The likely design goal is to keep the existing wider-tile preferences where they fit rather than route all matrices through the conservative 128-column shape. The tile widths explain the divisibility tests; they do not explain why the existing architecture-, bitrate-, and dimension-specific performance cutoffs were chosen. [inference; call_40831d8b34cf4edeb9683ccbde66ab82, call_0ac71f39100d4148895fe03424ec3c17, call_3393a7ae877d4e478e1107ca61ddc70b, call_6ee8c689f6b64f2d9479e75c6cf67a79]

## Impact

Both automatic dispatchers use the repaired selector: single GEMM passes `multi=false`, multi-GEMM passes `multi=true`, and both bypass it for positive forced indices. Inspected Python entry points are `LinearEXL3.forward` on its direct quantized path, the benchmark's automatic preference call, `Attention.project_qkv` on its fused K/V path, and the three fused expert projections in `BlockSparseMLP.forward`. The reconstruction path and benchmark's compatibility-checked forced runs do not use automatic selection. [source; call_0ac71f39100d4148895fe03424ec3c17, call_40831d8b34cf4edeb9683ccbde66ab82, call_faa7ac370560461a8d685563f83de158, call_17f45a12e78f43b680df81112c6a2afb, call_9e9744b9950246669bef00096871f450, call_58010382ede04a63b865755a78f01213, call_ce263e730a3a44569c775291fc3214aa, call_63a77705cf13459e8b985f9cbedd194e, call_abcc2402838746caada742ae00bbb541, call_8f501b8b06a740cf8265833eff42a72e]

The header now declares the existing six-argument `select_gemm_shape` definition, without a default for `multi`. The whole-parent literal search found just the declaration, definition, and the two already-six-argument calls; neither caller needed changing. This fixes a declaration mismatch, not a demonstrated internal build failure. [source; call_4d211a8a76e743aea6b286e3bedfb769, call_c1bd807a99fd4162bf05037908b4caa4, call_0ac71f39100d4148895fe03424ec3c17]

## Source Notes

The cooperative-GEMM entry (5d470a29) describes the introduction of the four shapes and records the Boolean threshold defect. The later tuning and multi-GEMM entries (c4867edd, b73d0739, a905cffb, 1284d43c) track the same expression through reuse by both dispatchers. The 1284d43c entry also records the stale declaration and zero-block cap. The concurrent-grid entry (edafdd1f) explains why a zero cap reaches the host's concurrency division and why broadcast input needs per-matrix scratch. The experimental codebook entry (d359bcc0) explains the independent codebook dimension of the dispatch tables. [ancestor; call_3164a4097584482c989dcd1408e74290, call_2177a51739384df692a8966b6a2dfa38, call_83e0f3639f264859a814183ab398c10b, call_293e816a782d416cb5ee99f5917988ff, call_6dad1cae2e184ad18ae71874ad97ad67, call_1b847d03b73c48c7854aa17c480556b9, call_4cb58e3671fa410e95635579dee00c09, call_3e0dc35d4c2f483885b5a9aad4966374]

The task removes the inherited Boolean comparison and fixes the declaration. It leaves the multi-GEMM block cap and concurrency division in place. It also leaves the wrapper's leading-dimension and scratch handling unchanged, including the pre-dispatch index-count check that can reject the all-expert fused case. The kernel mapping fix is not a general multi-GEMM input-validation fix. [source; call_40831d8b34cf4edeb9683ccbde66ab82, call_c1bd807a99fd4162bf05037908b4caa4, call_0ac71f39100d4148895fe03424ec3c17, call_17f45a12e78f43b680df81112c6a2afb, call_8e5e7f134dba4f0fb8059a9f3615bcc4, call_b44911ec78194e368b0981d367594490, call_8f501b8b06a740cf8265833eff42a72e]

Issue #5, “Will exl3 quants need requanting later?”, asks about storage stability and whether quantizing on Ampere is practical. Turboderp distinguishes working Ampere support from desired performance. Issue #61, “Run ERNIE-4.5-300B-A47B-PT 2.25bpw with 5x20G 3080 got 'Insufficient VRAM'”, reports a model-loading failure; the reporter says switching the allocator backend worked. [source; call_bbc0976aa1e94a09a897b8b5d5acb45c, call_3d7d740dd86a4e5c84896e6d285a0082]

Issue #5 is relevant background because the reply names both Ampere and the EXL3 GEMM kernel, but it reports no bad shape choice. Issue #61 shares tensor-shape and Ampere terminology, but its traceback ends in model autosplit before GEMM dispatch. Neither discussion establishes a link to this fix or validates it. [inference; call_bbc0976aa1e94a09a897b8b5d5acb45c, call_3d7d740dd86a4e5c84896e6d285a0082, call_40831d8b34cf4edeb9683ccbde66ab82]

<a id="gemm"></a>

## Choose EXL3 GEMM tiles that cover the output width

For A[M,K] × B[K,N], M is the row count, K the reduction dimension, and N the output width. Shapes 1–4 all use 16-row tiles; their (K,N) tiles are (16,128), (32,128), (32,256), and (16,512), with 256, 512, 512, and 256 threads respectively. Both kernel families feed the same inner tiled routine. It handles partial M tiles but counts only full K and N tiles. The separate `exl3_gemm_shape_compat` helper checks both divisibilities; the native dispatchers do not call it. [source; call_3393a7ae877d4e478e1107ca61ddc70b, call_0ac71f39100d4148895fe03424ec3c17, call_8e5e7f134dba4f0fb8059a9f3615bcc4, call_6ee8c689f6b64f2d9479e75c6cf67a79]

OLD/Ampere now require N divisible by 256 before entering either the at-most-four-bit branch or the N<4096 branch that can choose shape 3 at K>8192. Ada adds the same gate to its at-most-three-bit branch. An N divisible by 128 but not 256 also fails the 512-column test, so it falls through to shape 2 on those tiers. [source; call_40831d8b34cf4edeb9683ccbde66ab82, call_0ac71f39100d4148895fe03424ec3c17, call_3393a7ae877d4e478e1107ca61ddc70b]

Hopper/Blackwell add the same gate to the seven-or-more-bit branch for N≤8192, where shape 3 requires K>32768. For lower bitrates and N≤4096, the repaired, gated rule picks shape 3 only when K>8192 and bits≥3. The earlier single-GEMM exception still takes priority: two- or four-bit weights with K≤2048 use shape 1, which also has a 128-column tile. Shape 4's existing 512-column gates are unchanged; the OLD/Ampere test also requires K×N>4096² (16,777,216 weight positions) and at most six bits. [source; call_40831d8b34cf4edeb9683ccbde66ab82, call_0ac71f39100d4148895fe03424ec3c17, call_3393a7ae877d4e478e1107ca61ddc70b]

The scalar transcription checked 196,608 combinations of three tier groups, eight K values, widths in steps of 128, all eight bitrates, and both `multi` settings. N was incompatible with the selected tile in 20,208 parent cases and none of the patched cases in this sample. At Ampere, K=4096, N=2176, and four bits, the model changes from shape 3 covering 2,048 columns to shape 2 covering all 2,176. At Hopper/Blackwell, K=16384, N=4096, and three bits, it changes from shape 2 to shape 3; both cover all columns. [execution; call_2d7e3e5b3dc440928ef05d2ecf8c7573]

After selection, the existing dispatch uses the shape index for block size and tile-based launch limits, then combines it with the codebook slot to select a function pointer from the bitrate- and output-precision-specific table. The patch changes which specialization is chosen, not the packed-weight format, kernel implementation, or precision. The added `DBGI3` line is commented out. [source; call_40831d8b34cf4edeb9683ccbde66ab82, call_0ac71f39100d4148895fe03424ec3c17, call_3393a7ae877d4e478e1107ca61ddc70b]

## Authoring-time findings — pending review

### retained-zero-multi-gemm-block-cap (suspected; defect)

A compatible automatic tile choice can still leave multi-GEMM with zero blocks.

Trigger: An otherwise valid Ampere multi-GEMM call uses automatic selection with K=512, N=128, and two-bit weights.

Expected: Use at least one block for a nonempty supported workload, or reject it before computing launch concurrency.

Actual: Shape 2 has 16 K-by-N tiles here. The unchanged cap divides by 24 without a lower clamp, setting `num_sms` to zero. `exl3_mgemm` then evaluates `total_sms / num_sms`. Fused attention and expert callers use automatic dispatch without a minimum-tile check at the call site, but no ordinary model invocation of this exact case was established.

Locations: e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cu — select_exl3_mgemm_kernel, e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm

Source evidence: call_40831d8b34cf4edeb9683ccbde66ab82, call_0ac71f39100d4148895fe03424ec3c17, call_17f45a12e78f43b680df81112c6a2afb, call_58010382ede04a63b865755a78f01213, call_abcc2402838746caada742ae00bbb541, call_8f501b8b06a740cf8265833eff42a72e

scalar_transcription: Modeled patched selection and the integer cap; the result was shape 2, 16 tiles, and zero blocks. The subsequent division was established by source inspection. [call_2d7e3e5b3dc440928ef05d2ecf8c7573, call_17f45a12e78f43b680df81112c6a2afb]. Limits: Did not execute the C++ division or measure its failure mode.

### retained-k-tile-validation-gap (suspected; defect)

The new rules enforce N alignment in the affected branches, but automatic dispatch still does not validate K against the selected tile.

Trigger: An otherwise valid direct single-GEMM call on Ampere uses automatic selection, two-bit packed weights, no optional transforms, K=144, and N=128. K meets the wrapper comment's multiple-of-16 condition.

Expected: Use a shape that covers all of K, or reject the unsupported alignment before launch.

Actual: The fallback chooses shape 2, whose K tile is 32. The inner loop counts four full K tiles, leaving 16 reduction elements out. The native binding and wrapper expose the case; the inspected direct linear caller does not establish that a checkpoint presents it. The benchmark checks compatibility for forced runs, not for its automatic query.

Locations: e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cu — select_exl3_gemm_kernel, e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/exllamav3_ext/quant/exl3_gemm_inner.cuh — exl3_gemm_kernel_inner

Source evidence: call_40831d8b34cf4edeb9683ccbde66ab82, call_0ac71f39100d4148895fe03424ec3c17, call_3393a7ae877d4e478e1107ca61ddc70b, call_6ee8c689f6b64f2d9479e75c6cf67a79, call_17f45a12e78f43b680df81112c6a2afb, call_9e9744b9950246669bef00096871f450, call_ce263e730a3a44569c775291fc3214aa, call_63a77705cf13459e8b985f9cbedd194e

scalar_transcription: Checked the full-tile arithmetic for the source-selected K tile: 128 elements covered and 16 left over. [call_bed4f69929e74be4a73056d2f06378b7]. Limits: No tensor values or GPU output were evaluated.

### retained-multi-gemm-leading-dimension-gap (suspected; defect)

The unchanged multi-GEMM wrapper does not ensure that the input and output matrix groups agree with the kernel's traversal.

Trigger: An otherwise valid multi-GEMM binding call has two input matrices, one output matrix, and an indices tensor of shape (1,1).

Expected: Reject incompatible group sizes before dispatch.

Actual: The indices-width check agrees with the single output matrix, but the kernel iterates over the maximum of the input and output group sizes and attempts to use a second index. The inspected fused K/V and expert callers use broadcast or paired group sizes, so this example concerns the binding rather than those normal call shapes.

Locations: e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm, e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/exllamav3_ext/quant/exl3_gemm_kernel.cuh — exl3_mgemm_kernel

Source evidence: call_40831d8b34cf4edeb9683ccbde66ab82, call_17f45a12e78f43b680df81112c6a2afb, call_8e5e7f134dba4f0fb8059a9f3615bcc4, call_58010382ede04a63b865755a78f01213, call_abcc2402838746caada742ae00bbb541, call_8f501b8b06a740cf8265833eff42a72e

source_inspection: Compared the wrapper's index check, the kernel's matrix loop, and the located Python constructions against the task diff. [call_17f45a12e78f43b680df81112c6a2afb, call_8e5e7f134dba4f0fb8059a9f3615bcc4, call_40831d8b34cf4edeb9683ccbde66ab82]. Limits: No device memory access or failure was observed.

### retained-multi-gemm-broadcast-scratch-contract (suspected; new_requirement)

Broadcasting one input matrix does not broadcast its transformed-input scratch slice.

Trigger: A multi-GEMM binding caller supplies one input, multiple active outputs, and scratch sized only like the input, as the wrapper comment suggests.

Expected: Document and validate one scratch slice per active matrix, or make input-sized scratch sufficient.

Actual: The kernel advances the scratch pointer by M×K elements per matrix even when it reuses A. The wrapper does not check that capacity. Fused K/V and expert gate/up allocate per-matrix scratch; fused down uses paired matrices with matching scratch.

Locations: e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/exllamav3_ext/quant/exl3_gemm_kernel.cuh — exl3_mgemm_kernel

Source evidence: call_40831d8b34cf4edeb9683ccbde66ab82, call_17f45a12e78f43b680df81112c6a2afb, call_8e5e7f134dba4f0fb8059a9f3615bcc4, call_58010382ede04a63b865755a78f01213, call_abcc2402838746caada742ae00bbb541, call_8f501b8b06a740cf8265833eff42a72e

source_inspection: Compared broadcast input addressing with scratch addressing, wrapper checks, and existing allocations. [call_8e5e7f134dba4f0fb8059a9f3615bcc4, call_17f45a12e78f43b680df81112c6a2afb, call_abcc2402838746caada742ae00bbb541, call_8f501b8b06a740cf8265833eff42a72e]. Limits: No external caller allocation or device memory violation was observed.

### retained-fused-all-expert-index-count (suspected; defect)

The mapping fix cannot resolve the inherited mismatch between all-expert routing and the fused expert buffers.

Trigger: A single token takes the fused EXL3 expert path with `activate_all_experts` enabled and more total experts than experts per token.

Expected: Allocate space for all selected experts or use the expert-grouped path.

Actual: Routing produces one index per expert, but the fused gate output has one slice per configured expert-per-token slot. The direct call from `BlockSparseMLP.forward` is rejected by the wrapper's index-width check before kernel selection. Ordinary conversion was not shown to meet the fully quantized trigger.

Locations: e14fa3cf22ff9c4203736690522c7baaf17dd57b:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_40831d8b34cf4edeb9683ccbde66ab82, call_591f06344fbb4b10a0e0ee94bc8872ca, call_b44911ec78194e368b0981d367594490, call_8f501b8b06a740cf8265833eff42a72e, call_17f45a12e78f43b680df81112c6a2afb

source_inspection: Traced the routing count and fused gate buffer to the native width check; neither is changed by the mapper diff. [call_b44911ec78194e368b0981d367594490, call_8f501b8b06a740cf8265833eff42a72e, call_17f45a12e78f43b680df81112c6a2afb, call_40831d8b34cf4edeb9683ccbde66ab82]. Limits: Conditional reach established from source; no routing or conversion run was performed.

## Uncertainty and limits

No CUDA build, kernel launch, numerical comparison, model run, or timing benchmark was performed. The Python checks transcribe bounded selector and tile arithmetic; they do not emulate fixed-width integer overflow, CUDA memory accesses, or floating-point execution.

The exact model or tensor that prompted the change is unestablished. The inspected branches and callees explain tile compatibility, not the empirical rationale for the performance thresholds.

Caller reach is based on whole-parent literal searches and inspected call sites. It does not establish which deployed models encounter the affected dimensions or enumerate dynamic and external callers.
