# dc69b16752a9ee25e6dca731b9db5d7b5da26878


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/dc69b16752a9ee25e6dca731b9db5d7b5da26878) · [Evidence ledger](draft.json)

Makes GEMM kernel-attribute caching device-specific in both launchers, preserving lazy setup and existing kernel computation.

- [Device-local kernel attribute initialization](#gemm)

## Problem

Both GEMM launchers shared a process-wide set of configured kernel pointers. After one device inserted a kernel, another device using that same pointer skipped the attribute-setting call. [source; call_537379f1f021497d992002dfe8294f0a]

## Reasoning

The patch makes configuration bookkeeping device-specific while retaining lazy initialization: each device records its own configured kernels. [source; call_e129b54620134a1da6f1e079efcedf13]

## Impact

Both exl3_gemm and exl3_mgemm now attempt attribute setup independently on each device. Kernel selection, arguments, cooperative launch geometry and requested shared-memory size remain unchanged. [source; call_e129b54620134a1da6f1e079efcedf13, call_537379f1f021497d992002dfe8294f0a]

## Source Notes

The earlier output-precision and cooperative-fusion entries were read. They describe the FP16-input/FP32-output interface and the introduction of cooperative GEMM launches with device context management, respectively. [ancestor; call_7f4cea34868640d1af5a8092956103ba, call_236d0249741e4c1d98476ca41e7b03db]

Issue #5, “Will exl3 quants need requanting later?”, concerns format stability and Ampere performance. PR #36, “added max_total_tokens variable to class Generator, fixed type assert…”, reports a missing Generator attribute in TabbyAPI. Neither body identifies this GEMM attribute-cache change as its remedy. [source; call_3103532a01514599a1af3c91e6e2eb63, call_6015bb2c232749eba48c71e8d176eba9]

<a id="gemm"></a>

## Device-local kernel attribute initialization

Each launcher first guards A.device(), obtains the current CUDA device, and uses that device for context lookup. The patch reuses this device index for the attribute cache, aligning the cache lookup and insertion with the guarded launch device. [source; call_537379f1f021497d992002dfe8294f0a, call_e129b54620134a1da6f1e079efcedf13]

The single set becomes an array of MAX_DEVICES sets. MAX_DEVICES is 32, also used by DevCtx's device-property and lock arrays. Whole-parent-tree search found only the declaration and the two launchers consuming kernel_attr_set; the diff updates both consumers. [source; call_4404226f2c16453482ebf5c01c78d94f, call_2454278d06a741fd9453587015852cac, call_e129b54620134a1da6f1e079efcedf13]

On a cache miss, the launcher requests cudaFuncAttributeMaxDynamicSharedMemorySize = SMEM_MAX and inserts the kernel pointer. SMEM_MAX is 90 × 1024 bytes, described in source as the compute-capability-8.6 shared-memory maximum; the cooperative launch requests the same amount. [source; call_da45757d77924465a4ff08ebd3b32501, call_537379f1f021497d992002dfe8294f0a]

A Python model using two kernel identities on two devices produced two setup events for the old global cache and four for the new per-device cache; repeated calls on the same device stayed cached. It also calculated the shared-memory request as 92,160 bytes. [execution; call_301eb5db99494364b351f235dcd39b4a]

The apparent design goal is to avoid treating setup on one GPU as setup on every GPU, without paying the attribute-setting cost on every launch. This trades a single cache for bounded device-local caches rather than changing the numerical kernel. [inference; call_e129b54620134a1da6f1e079efcedf13, call_537379f1f021497d992002dfe8294f0a]

## Uncertainty and limits

No CUDA compilation, multi-GPU execution or performance measurement was performed. The scalar model demonstrates bookkeeping only, not CUDA attribute semantics or successful launches.

The existing unchecked cudaFuncSetAttribute return value and device-index assumptions are unchanged; their runtime consequences were not established.
