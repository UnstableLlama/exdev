# d908052e96929a4f92e90256838f9cad9b72226d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d908052e96929a4f92e90256838f9cad9b72226d) · [Evidence ledger](draft.json)

Add an OOM-triggered CPU Cholesky fallback and reuse Hessian device storage for the LDL factor while preserving the Hessian on CPU for proxy-error evaluation.

- [CPU Cholesky fallback with device-storage reuse](#quantizer)

## Problem

block_ldl previously allocated a Cholesky factor alongside the Hessian, with no recovery from device out-of-memory errors. [source; call_63db9ac495cb4aa4a30a76548d6aeb56]

## Reasoning

The change preserves the Hessian on CPU and reuses its original device storage for the factor. Recognized out-of-memory exceptions instead trigger CPU Cholesky before copying the factor into that same device storage. [source; call_6edf965bcbbb4f55a291d5022ea588f2]

## Impact

This can allow factorization to proceed when device Cholesky cannot allocate its working storage, trading host memory and transfers for lower device-memory demand. Subsequent block inversion and normalization still run on the original device. [inference; call_6edf965bcbbb4f55a291d5022ea588f2, call_63db9ac495cb4aa4a30a76548d6aeb56]

## Source Notes

The preceding entry describes deleting the working LDL factor after quantization; this change addresses its construction instead. [ancestor; call_6c3c808652bf4516b221d95e523500a7]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension-import failure and an environment workaround, not a Cholesky allocation failure. [source; call_bdeddcd057794b0da73c7df0459cdfb3]

<a id="quantizer"></a>

## CPU Cholesky fallback with device-storage reuse

finalize_capture_H regularizes and transforms the Hessian before calling block_ldl(H, 16). The unchanged 16 is the diagonal block width: block_ldl requires divisibility by that width, extracts and inverts diagonal Cholesky blocks, and normalizes block columns to produce a block-unit-lower factor. [source; call_63db9ac495cb4aa4a30a76548d6aeb56]

On the successful device path, block_ldl first copies H to CPU, overwrites the original H storage with the Cholesky result, and rebinds L to that storage. Keeping the CPU copy preserves the transformed Hessian while allowing the caller-held device allocation to become useful factor storage. [source; call_6edf965bcbbb4f55a291d5022ea588f2]

The try block includes Cholesky and the following copies. Exceptions qualify for retry when their class name is OutOfMemoryError or their text contains CUDA out of memory or HIP out of memory; other exceptions are re-raised. The retry prints the device, calls free_mem, factors a CPU copy, and copies that result into H. free_mem performs garbage collection and CUDA cache clearing. [source; call_6edf965bcbbb4f55a291d5022ea588f2, call_22971dbc768c44b28119687a2cc026d2]

The second return value changes from D to the preserved CPU Hessian, and the unused computation D[i] = DL[i] @ DL[i].T is removed. Whole-parent-tree literal search finds only finalize_capture_H calling block_ldl; its unpacking changes from L, _ to L, H. [source; call_3872383cf9e3466a99358ff4ff7fd752, call_6edf965bcbbb4f55a291d5022ea588f2]

The caller zeros L's diagonal and stores L separately from H_data['H']. Preserving H matters because quantize_exl3 later transfers it back to the computation device for residual and reference Hessian contractions used in proxy error. [source; call_6edf965bcbbb4f55a291d5022ea588f2, call_63db9ac495cb4aa4a30a76548d6aeb56]

A standard-library list model of both copy-and-rebind paths preserved the original Hessian values while reusing the modeled device-buffer identity for the factor. This checked the ownership sequence, not repository Cholesky or GPU execution. [execution; call_5c5c032af6b44ad7b76a84d95da6db1b]

## Uncertainty and limits

No repository PyTorch execution, CPU/GPU numerical comparison, forced-OOM test or VRAM measurement was performed. The list-based ownership model does not establish tensor aliasing, allocator behavior or transfer costs.

The fallback does not cover failures in subsequent block inversion, normalization or quantization, and CPU factorization can itself fail.
