# 1284d43c76349160992d42a241c81071fcc7b919


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1284d43c76349160992d42a241c81071fcc7b919) · [Evidence ledger](draft.json)

Re-enables a deeper-pipelined shape 1 and retunes single/multi-GEMM dispatch and block counts. Speedups are unmeasured; inspection identifies an expanded zero-block multi-GEMM hazard, a stale declaration and a carried-over selector defect.

- [Retuned GEMM shapes, pipelines and matrix concurrency](#gemm)

## Problem

The change retunes EXL3 GEMM for small reduction dimensions, re-enables shape 1, and separates single-matrix from multi-matrix scheduling. [source; call_03ba85c9aa374d168a3d1adc9af07679, call_fb9cf5a937bd4bbd8d50d3cb598da12c]

## Reasoning

The shape-1 registration, deeper pipeline and new five-fragment loop are interdependent: the newly selected specialization requires the added loop to perform multiplication. The macro extraction preserves the existing one-through-four-stage operation order. [source; call_3a4f64b15d904164b83a4aae002d95d6, call_fb9cf5a937bd4bbd8d50d3cb598da12c, call_50979acd58c446beaf778a074e14f6c6]

Smaller tiles and deeper staging plausibly trade more pipeline storage for better overlap on short-K workloads. Reducing blocks per matrix can also permit more concurrent matrices. These are interpretations of the implementation, not measured speedups. [inference; call_50979acd58c446beaf778a074e14f6c6, call_38080e6040f045e4b932629b85a71bef, call_03ba85c9aa374d168a3d1adc9af07679]

## Impact

Single GEMM can use more blocks, while multi-GEMM halves its tile-based block allowance. Shape 1 becomes available through both dispatch tables, although its new automatic selection rule applies only to single GEMM. [source; call_03ba85c9aa374d168a3d1adc9af07679, call_fb9cf5a937bd4bbd8d50d3cb598da12c]

## Source Notes

The earlier cooperative-GEMM entry was read. It establishes the extraction of the inner pipeline, cooperative Hadamard fusion, shape-based dispatch and an already-recorded Boolean threshold defect. [ancestor; call_e886e10983e443ddac232dceb5bb5e51]

Issue #5, “Will exl3 quants need requanting later?”, asks about format stability and subsequently Ampere support. The response distinguishes working Ampere support from desired performance. [source; call_c029dfb855504a6588f4ccdea0dc3d2f]

Issue #5 is related performance context because its response mentions Ampere and the EXL3 GEMM kernel, both present in this change. It does not establish a direct issue-to-commit relationship. [inference; call_c029dfb855504a6588f4ccdea0dc3d2f, call_03ba85c9aa374d168a3d1adc9af07679]

<a id="gemm"></a>

## Retuned GEMM shapes, pipelines and matrix concurrency

Shape 1 retains its (M,K,N) tile of (16,16,128), but changes from three shared-memory stages and two fragment slots to six and five. Its block size remains 256 threads. Shapes 2 and 3 use (16,32,128) and (16,32,256), respectively, with 512 threads. [source; call_472951bff18b494ba421144a9d74a3b7, call_fb9cf5a937bd4bbd8d50d3cb598da12c]

FSTAGE schedules global loading, waits for shared data, loads/dequantizes a fragment slot, multiplies another slot, reduces at a K-column or slice boundary, and advances. Five-stage execution cycles load/multiply pairs (1,0), (2,1), (3,2), (4,3), (0,4). The pre-loop load of slot 0 supplies the first multiplication; load_frags stops loading when its input slice is exhausted. [source; call_3a4f64b15d904164b83a4aae002d95d6, call_50979acd58c446beaf778a074e14f6c6]

A scalar schedule model consumed tiles in order for fragment counts 1–5 and slice lengths 1–39. Applying the inspected shared-memory formula to new shape 1 gives 10,240 bytes at two bits, 13,312 at four bits and 19,456 at eight bits, all below the source's 90-KiB ceiling. This does not change the host's fixed 90-KiB launch allocation. [execution; call_98aec4ae86c048d286bdc4893afae37c, call_50979acd58c446beaf778a074e14f6c6, call_38080e6040f045e4b932629b85a71bef]

For CC_OLD/Ampere at up to four bits, K <= 2048 now selects shape 2 regardless of N. Ada adds the same short-K preference at up to three bits only for single GEMM. Hopper/Blackwell select shape 1 for single GEMM at exactly two or four bits when K <= 2048. Other rules remain, including divisibility-based wider tiles; positive forced indices bypass automatic selection. [source; call_03ba85c9aa374d168a3d1adc9af07679, call_656022c52c8640af84b036a235c66ec2]

The selected kernels retain cooperative input/output transforms, 16-row iteration and the shared inner routine. Shape compatibility checks require K and N to be divisible by the selected tile dimensions. The host selector does not itself invoke that compatibility helper. [source; call_9bc9485739724c30be202b7f36763b1b, call_656022c52c8640af84b036a235c66ec2, call_38080e6040f045e4b932629b85a71bef]

For tile-aligned dimensions, let T=(K/tile_K)*(N/tile_N). Single GEMM changes its block cap from floor(T/12) to T and clamps the result to at least one. Multi-GEMM instead changes floor(T/12) to floor(T/24), without a lower clamp. Its host computes matrix concurrency as min(total_sms/num_sms, output-matrix count), so fewer blocks per matrix can increase grid-z concurrency. [source; call_03ba85c9aa374d168a3d1adc9af07679, call_38080e6040f045e4b932629b85a71bef]

Whole-tree search found two callers of select_gemm_shape, both updated with the new multi argument: false for single GEMM and true for multi-GEMM. The header declaration remains on the five-argument form; no remaining five-argument call was found. [source; call_d152207677b04eb7a27024f744d8726d, call_03ba85c9aa374d168a3d1adc9af07679, call_472951bff18b494ba421144a9d74a3b7, call_fb9cf5a937bd4bbd8d50d3cb598da12c]

The benchmark changes its bitrate variable K from eight to one, raises timed runs from 50 to 60, adds matrix dimensions (2048,4096), and includes shape 1 in forced comparisons. It checks compatibility, warms up ten calls and cycles buffers to reduce cache bias; it explicitly does not test correctness. Its one-bit default does not exercise the new automatic two/four-bit shape-1 rule. [source; call_b2ac2ee48aee4ab2baf1d6f38c8eb2e9, call_4561cab62bf44605be9a6701ab08e07a, call_03ba85c9aa374d168a3d1adc9af07679]

## Authoring-time findings — pending review

### zero-multi-grid (suspected; defect)

The tighter multi-GEMM cap expands the range that produces zero blocks and reaches integer division by zero.

Trigger: For example, automatic Ampere multi-GEMM with K=512, N=128 and bits=2 selects shape 2, giving 16 tiles and num_sms=0 under division by 24; the previous division by 12 gave one block.

Expected: A nonempty supported matrix should receive a positive block count or be rejected before concurrency arithmetic.

Actual: exl3_mgemm computes total_sms / num_sms without a zero guard. Direct Python callers occur in attention's fused K/V projection and the fused expert gate/up/down path; their inspected call sites do not enforce a minimum tile count. This does not establish that typical model dimensions trigger the condition.

Locations: 1284d43c76349160992d42a241c81071fcc7b919:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cu — select_exl3_mgemm_kernel, 1284d43c76349160992d42a241c81071fcc7b919:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm

Source evidence: call_03ba85c9aa374d168a3d1adc9af07679, call_38080e6040f045e4b932629b85a71bef, call_da84d59aa1074698ba78355a1f4d8508, call_c8f9812dd9c74a1dbccdeca94c5cbf29, call_9924fc1c08554d6e95479b80c4346795

scalar_transcription: For 16 tiles and 80 available SMs, Python calculated old cap 1 and new multi cap 0. [call_98aec4ae86c048d286bdc4893afae37c]. Limits: No repository or CUDA execution; downstream division was identified by inspection.

### inherited-boolean-threshold (suspected; defect)

The earlier recorded Boolean dimension comparison is carried over unchanged.

Trigger: Hopper/Blackwell automatic selection with bits=3, K=16384 and N=4096 reaches (size_k && bits >= 3) > 8192.

Expected: A meaningful dimension threshold should compare a dimension; the precise intended selection rule is unestablished.

Actual: The Boolean value cannot exceed 8192, so this ternary always chooses shape 2. Both single and multi selectors call this function; positive forced shapes bypass it.

Locations: 1284d43c76349160992d42a241c81071fcc7b919:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cu — select_gemm_shape

Source evidence: call_656022c52c8640af84b036a235c66ec2, call_03ba85c9aa374d168a3d1adc9af07679, call_d152207677b04eb7a27024f744d8726d

source_inspection: Compared the parent selector and its two callers with the complete task diff; the expression remains. [call_656022c52c8640af84b036a235c66ec2, call_03ba85c9aa374d168a3d1adc9af07679]. Limits: No performance consequence measured.

### stale-selector-declaration (suspected; external_compatibility)

The header still advertises a five-argument selector whose definition has become six-argument.

Trigger: A translation unit calls select_gemm_shape using the unchanged header declaration.

Expected: The declaration should match the available definition.

Actual: The declared five-argument overload has no matching definition in the inspected tree. Both discovered repository calls use the new definition locally, so this is not evidence of a current internal build failure.

Locations: 1284d43c76349160992d42a241c81071fcc7b919:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cuh — select_gemm_shape

Source evidence: call_d152207677b04eb7a27024f744d8726d, call_472951bff18b494ba421144a9d74a3b7, call_03ba85c9aa374d168a3d1adc9af07679, call_fb9cf5a937bd4bbd8d50d3cb598da12c

source_inspection: Searched the whole parent tree and compared every selector occurrence against the task diff. [call_d152207677b04eb7a27024f744d8726d, call_03ba85c9aa374d168a3d1adc9af07679, call_fb9cf5a937bd4bbd8d50d3cb598da12c]. Limits: No external consumer or linker test was run.

## Uncertainty and limits

No CUDA compilation, kernel execution, numerical comparison or timing benchmark was performed.

The Python checks model fragment ordering and integer arithmetic only; they do not model asynchronous copies, GPU synchronization, register allocation or floating-point reduction.

The inspected sources do not establish why 2048 or the new divisor 24 is optimal for the named device tiers.

Literal whole-tree searches do not establish compatibility for dynamic or external callers.
