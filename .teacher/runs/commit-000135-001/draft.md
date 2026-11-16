# edafdd1f3d9a966a982f54334838f4f94ee51473


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/edafdd1f3d9a966a982f54334838f4f94ee51473) · [Evidence ledger](draft.json)

Parallelizes multi-GEMM across grid z-planes while retaining per-matrix slicing. Speedup is unmeasured; inspection identifies a zero-width division path and an enlarged broadcast scratch requirement.

- [Concurrent matrix groups in the cooperative GEMM grid](#quantized-inference)

## Problem

Multi-GEMM previously processed matrices sequentially using a grid capped by the work available for one matrix, leaving potential capacity unused. [source; call_b1f118b3e3394666a394fd19913a7294, call_fea1900736f0463c8a21e0e14df6e3aa]

## Reasoning

The change retains the per-matrix grid width and uses an additional grid dimension to process independent matrices concurrently, rather than dividing each matrix into smaller slices. [source; call_82d0b2ddc77c4d7180d7593d2dc4c124, call_18a5fa132362421498f124e072053e2d]

## Impact

This can increase concurrent work when kernel selection reduces the grid width and multiple outputs are available. It does not guarantee full utilization or a measured speedup. [inference; call_82d0b2ddc77c4d7180d7593d2dc4c124, call_fea1900736f0463c8a21e0e14df6e3aa]

## Source Notes

Whole-parent literal search found the Python extension binding but no Python call site for exl3_mgemm. The observations therefore concern the exposed native interface; reach into generation or conversion workflows is not established. [source; call_2e34b3a892fa4c1496cd89dd766d8aec, call_f146902dbea7449b85bb33cd418131b1]

<a id="quantized-inference"></a>

## Concurrent matrix groups in the cooperative GEMM grid

exl3_mgemm saves the device SM count before selection reduces num_sms, then launches (num_sms, 1, min(total_sms / num_sms, bszm_out)). The unchanged selector divides the K-by-N tile count by 12 to limit slices. Comments describe this divisor as experimental and leave evaluation of larger Ampere grids open. [source; call_82d0b2ddc77c4d7180d7593d2dc4c124, call_fea1900736f0463c8a21e0e14df6e3aa, call_0baac3772cb5415ebef38e680937f795]

Each z-plane handles j = i + blockIdx.z, advancing i by gridDim.z. It selects B and its scales through B_indices[j], broadcasts A only when bszm_in is one, and assigns separate transformed-input and output slices to j. Optional output weights likewise use j. [source; call_18a5fa132362421498f124e072053e2d]

Inactive tail planes skip transform and GEMM work but still participate in the grid-wide barriers. Active planes retain input Hadamard transformation, GEMM in 16-row steps, and output Hadamard transformation. The normalization remains 1/sqrt(128), optionally multiplied by the matrix weight on output. [source; call_18a5fa132362421498f124e072053e2d, call_b1f118b3e3394666a394fd19913a7294]

The inner kernel still partitions K-by-N tiles across gridDim.x, decodes packed weights and performs tensor-core multiplication with locked partial-output reduction. Separate z-planes receive lock offsets blockIdx.z * size_n / 128. This stride covers the output-column locks because supported N tiles are at least 128 columns. index_m now returns zero; both launch paths use a unit y dimension and advance row pointers explicitly. [source; call_54bd320653594b909b62803ba2dc5fac, call_ae67634a17934a3eb277a259d59b3091, call_db625d3448cf48a9b229e0f5dbf0caee, call_18a5fa132362421498f124e072053e2d, call_9f9d887e1b7541d39bb05c3bfba41d22]

A scalar scheduling check with 120 available SMs, width 32 and eight matrices produced three concurrent planes and 96 blocks, covering matrices in groups [0,1,2], [3,4,5], [6,7]. With only two matrices it produced 64 blocks; with width 120 it retained serial matrix processing. Thus integer packing and batch size can leave capacity unused. [execution; call_0adc900e5b3446168adcc5f1c4bf01a4]

The tradeoff is more independent work without changing the existing tile and slice policy, at the cost of distinct per-matrix transformed-input storage and continued whole-grid synchronization between phases. [inference; call_18a5fa132362421498f124e072053e2d, call_fea1900736f0463c8a21e0e14df6e3aa]

## Authoring-time findings — pending review

### zero-slice-division (suspected; defect)

The new concurrency calculation divides by a selector result that can be zero.

Trigger: Call exl3_mgemm with shape 2 forced, size_k=128 and size_n=128: the selector computes (128/32)*(128/128)/12 = 0.

Expected: Reject unsupported small workloads explicitly or retain a positive launch width.

Actual: The selector sets num_sms to zero and the new host expression evaluates total_sms / num_sms before launch. The prior zero-width launch problem is changed into an integer-division-by-zero path. Reach is the native interface exposed by the extension; no Python caller was found.

Locations: edafdd1f3d9a966a982f54334838f4f94ee51473:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm

Source evidence: call_82d0b2ddc77c4d7180d7593d2dc4c124, call_fea1900736f0463c8a21e0e14df6e3aa, call_ae67634a17934a3eb277a259d59b3091, call_2e34b3a892fa4c1496cd89dd766d8aec, call_f146902dbea7449b85bb33cd418131b1

scalar_transcription: Evaluated the selector's bounded tile-count arithmetic and obtained zero. [call_0adc900e5b3446168adcc5f1c4bf01a4]. Limits: Did not execute C++ division or launch CUDA; runtime failure manifestation is unmeasured.

### broadcast-scratch-capacity (suspected; new_requirement)

Broadcast-input multi-GEMM now requires scratch storage for every matrix rather than one input-sized scratch slice.

Trigger: bszm_in=1, bszm_out>1, with A_had allocated only as large as A, as the retained interface comment describes.

Expected: An input-sized scratch allocation should remain sufficient under the old contract, or the enlarged requirement should be documented and validated.

Actual: The kernel now writes and reads A_had + j*size_m*size_k, including for broadcast A. Later matrices therefore address beyond an input-sized allocation. The wrapper does not validate scratch capacity. No repository Python construction site was found; external extension callers are the established interface boundary.

Locations: edafdd1f3d9a966a982f54334838f4f94ee51473:exllamav3/exllamav3_ext/quant/exl3_gemm_kernel.cuh — exl3_mgemm_kernel

Source evidence: call_18a5fa132362421498f124e072053e2d, call_9f9d887e1b7541d39bb05c3bfba41d22, call_b1f118b3e3394666a394fd19913a7294, call_2e34b3a892fa4c1496cd89dd766d8aec, call_f146902dbea7449b85bb33cd418131b1

source_inspection: Compared the prior conditional scratch-pointer advance with the new unconditional matrix-indexed offsets and inspected wrapper validation. [call_18a5fa132362421498f124e072053e2d, call_9f9d887e1b7541d39bb05c3bfba41d22, call_b1f118b3e3394666a394fd19913a7294]. Limits: No external caller allocation or GPU memory violation was observed.

## Uncertainty and limits

No CUDA compilation, kernel execution, numerical comparison or performance measurement was performed.

Scalar checks model bounded integer scheduling and allocation arithmetic, not CUDA synchronization, memory safety or floating-point accumulation.

Dynamic or external callers are not excluded by the literal repository search.
