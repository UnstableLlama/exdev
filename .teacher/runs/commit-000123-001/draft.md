# 5d470a29780927c1c8c874609597823f210ae3b9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5d470a29780927c1c8c874609597823f210ae3b9) · [Evidence ledger](draft.json)

Fuses EXL3 input/output Hadamard transforms into cooperative GEMM, introduces four retuned shapes and bitrate-specific dispatch tables, and updates Python callers. Performance is unmeasured; a Boolean dimension-threshold expression is a suspected selector defect.

- [Cooperative GEMM with scale-and-Hadamard fusion](#quantized-inference)

## Problem

The direct EXL3 linear path launched separate input Hadamard, quantized GEMM and output Hadamard operations. The change combines these operations within a cooperative kernel. [source; call_cf9fb72ff5fa4825a8ddd7a78f448138, call_f219404ec95840b8b94011912682b37e]

## Reasoning

Grid-wide synchronization separates input transformation, GEMM row chunks and output transformation. This permits fusion across blocks while retaining the existing shared-memory/dequantization pipeline. [source; call_f219404ec95840b8b94011912682b37e, call_09083d0020774fd6b9cb612518c2a3b4]

Reducing launch overhead is a plausible benefit, but this is launch fusion rather than elimination of intermediate global-memory traffic: transformed inputs still occupy A_had and output transformation reads and writes C. [inference; call_f219404ec95840b8b94011912682b37e]

## Impact

LinearEXL3.forward supplies input/output scale vectors and scratch storage directly to GEMM. Its reconstruction alternative remains separate Hadamard → dense GEMM → Hadamard, with the existing default of reconstruction above 32 flattened input rows. [source; call_cf9fb72ff5fa4825a8ddd7a78f448138, call_62a2e2d31d8046199a7ae32455ce8d91]

The extension's GEMM signature changes, and kernel enumeration becomes shape enumeration with a separate compatibility query. Whole-parent literal search identifies LinearEXL3.forward and the benchmark as Python callers; both are updated by the diff. [source; call_c331115211bc4a0390af66dea74a9281, call_f464fd0646d6498fa38c29a20de1b523, call_e125ab4d9cb74a86bd3a8eddb63974bd, call_cf9fb72ff5fa4825a8ddd7a78f448138]

## Source Notes

The earlier output-precision entry describes the separate scale-fused Hadamard path and FP16-input restriction. The present change restores fusion using unpacked half-precision scales rather than the formerly disabled packed-sign argument. [ancestor; call_603c773d7ff842af965d781ab37d5ed4]

Issue #5, “Will exl3 quants need requanting later?”, asks about storage stability and subsequently Ampere support. The response distinguishes functioning Ampere support from desired performance and promises backward compatibility if storage changes. [source; call_f74574645e5e41d6b36d5398795321eb]

That discussion provides related performance context because it explicitly mentions the EXL3 GEMM kernel and Ampere; it does not establish that this commit implements a particular promise or resolves the issue. [inference; call_f74574645e5e41d6b36d5398795321eb, call_a46bf35565a64c97b4686ff4280cc9b9]

<a id="quantized-inference"></a>

## Cooperative GEMM with scale-and-Hadamard fusion

exl3_gemm now accepts optional suh, A_had and svh. Supplying suh requires shape-matched A_had; input remains FP16, packed weights remain int16, and output remains FP16 or FP32. The actual scale checks require k input scales and n output scales, despite the wrapper comment describing shorter vectors. [source; call_7fb8193f7d944fd58205863153f52e28, call_1a409f874f6b4dac9554ae3b87de03f9]

The outer kernel distributes 128-element input segments across warps, applies pre-scales and a normalized Hadamard into A_had, synchronizes the grid, then redirects A to that scratch buffer. It processes GEMM in 16-row increments with a grid barrier after each increment. Finally, output segments receive an in-place Hadamard followed by svh scaling. [source; call_f219404ec95840b8b94011912682b37e, call_4142b6a7cbd7412da0c5b085edd206b5]

The shared Hadamard helpers combine four values per lane with five XOR-shuffle butterfly stages across 32 lanes. The half path performs scale multiplication in half precision and rounds transformed values before post-scaling; the float path keeps transformed values in float. Standalone Hadamard kernels now call the same helpers. [source; call_4142b6a7cbd7412da0c5b085edd206b5, call_9ffd20b60fce4a149c0fe8bcb2c5dd78]

A standard-library calculation gives 1/sqrt(128) = 0.08838834764831843. The source decimal constant has 128 times its square approximately 0.9999999999927947, consistent with normalization before CUDA float rounding. [execution; call_d3cab3b4c1d14ad5ba6f59fab37b8a01]

The extracted GEMM inner routine retains asynchronous global-to-shared staging, register fragments, bitrate-specialized dequantization, tensor-core multiplication and lock-ordered partial-output reduction. Cooperative barriers supplement rather than replace those per-output reduction locks. [source; call_09083d0020774fd6b9cb612518c2a3b4, call_f219404ec95840b8b94011912682b37e]

Four shape tuples replace six prior variants. All use M=16; their (K,N) tiles are (16,128), (32,128), (32,256) and (16,512). Shape 1 has three shared stages and one fragment stage; the others have four and two. The block size is 256 times K/16, giving 256 or 512 threads. [source; call_f81e31b067ab4382890777ef976b57dc, call_7fb8193f7d944fd58205863153f52e28]

Selection now depends on device tier, bitrate and k/n dimensions rather than m. Width divisibility by 256 or 512 influences wider tiles. The block count is capped by floor((k/tile_k)*(n/tile_n)/12); the source labels 12 experimental. Exact performance reasons for the device-specific dimension thresholds are not documented by the inspected selector. [source; call_a46bf35565a64c97b4686ff4280cc9b9]

The host launches a one-dimensional cooperative grid with 90 KiB dynamic shared memory per block. Device SM counts, architecture tiers and lock allocation move into DevCtx. Dispatch references bitrate-specific FP16/FP32 function tables; the inspected one-bit compilation unit instantiates all four shapes for both output types. [source; call_7fb8193f7d944fd58205863153f52e28, call_15e80f33533c4b1ca0bdd3f9a10f8322, call_a46bf35565a64c97b4686ff4280cc9b9, call_710ddf5468a94ecc91995ef5e6161144]

The benchmark now supplies scales and aliases A_had to A, queries shape compatibility without launching, and times fused calls. Its defaults change from eight-bit to one-bit weights and from 200 to 50 runs; these edits are not performance results. [source; call_e125ab4d9cb74a86bd3a8eddb63974bd]

## Authoring-time findings — pending review

### boolean-dimension-threshold (suspected; defect)

A new Hopper/Blackwell selector condition compares a Boolean expression with 8192, making its shape-3 arm unreachable.

Trigger: Automatic selection reaches the non-eight-bit size_n <= 4096 branch after bypassing the earlier shape-1 condition; for example bits=3, size_k=16384, size_n=4096.

Expected: If this ternary is intended to distinguish a dimension threshold, its condition should compare a dimension rather than a Boolean. The precise intended rule is unestablished.

Actual: (size_k && bits >= 3) is zero or one, so comparison with 8192 is always false and the branch returns shape 2. This reaches automatic direct-GEMM calls from LinearEXL3.forward and the benchmark's preferred-shape query; forced positive shape indices bypass it.

Locations: 5d470a29780927c1c8c874609597823f210ae3b9:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cu — select_gemm_shape

Source evidence: call_a46bf35565a64c97b4686ff4280cc9b9, call_349c6d091db34c72befe32bd4bc42376, call_c331115211bc4a0390af66dea74a9281, call_cf9fb72ff5fa4825a8ddd7a78f448138, call_e125ab4d9cb74a86bd3a8eddb63974bd

source_inspection: Inspected the new selector, host dispatch and updated callers. Whole-parent search finds no previous select_gemm_shape symbol and identifies direct GEMM Python call sites. [call_a46bf35565a64c97b4686ff4280cc9b9, call_7fb8193f7d944fd58205863153f52e28, call_c331115211bc4a0390af66dea74a9281, call_349c6d091db34c72befe32bd4bc42376]. Limits: No runtime performance consequence established; external callers were not enumerated.

scalar_transcription: Python modeled the Boolean comparison for k=4096, 16384 and 32768 with representative bitrates; every result was false. [call_d3cab3b4c1d14ad5ba6f59fab37b8a01]. Limits: Expression check only, not repository or GPU execution.

## Uncertainty and limits

No CUDA compilation, kernel execution, numerical comparison or timing benchmark was performed. Cooperative-launch availability and residency were not experimentally established.

Scalar checks use Python arithmetic, not CUDA floating-point rounding, tensor-core execution or concurrent memory operations.

Compilation-unit inspection covered the one-bit implementation and dispatch declarations, not every bitrate-specific translation unit.

Literal caller searches do not establish compatibility for dynamic or external extension users.
