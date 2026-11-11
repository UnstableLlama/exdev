# f4da1467ba031d3c2b3ee4ee2a57c9ae01eb40ae


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f4da1467ba031d3c2b3ee4ee2a57c9ae01eb40ae) · [Evidence ledger](draft.json)

Enables a 1024-thread launch bound on the tile quantization kernel without changing launch geometry or arithmetic; the suggested Blackwell fix remains unverified.

- [Explicit launch bound for tile quantization](#quantizer)

## Problem

The change enables a previously commented-out launch-bound annotation on the tile quantization kernel. The diff alone does not establish a Blackwell failure or its resolution. [source; call_d69124cda5b749fe99696b88c4e270e1]

## Reasoning

The annotation's 1024 matches NUM_THREADS and the maximum block size selected by the existing launcher; this changes the kernel declaration rather than reducing launch sizes or changing quantization arithmetic. [source; call_d69124cda5b749fe99696b88c4e270e1, call_028a47643b3e4ea7b97df3ca8c75a810]

## Impact

The annotation applies to all eight dispatched quantize_tiles_kernel specializations. The separate decode_kernel declaration remains unchanged. [source; call_d69124cda5b749fe99696b88c4e270e1, call_028a47643b3e4ea7b97df3ca8c75a810]

## Source Notes

An earlier entry describes centralizing launch sizing and iteration strides through NUM_THREADS; this change retains that arrangement. [ancestor; call_3fdfc8900a4c4047aaa10aa1687cb19a]

<a id="quantizer"></a>

## Explicit launch bound for tile quantization

The sole edit activates __launch_bounds__(1024) on quantize_tiles_kernel<K>. The host launcher still computes edges = 65536 >> K and threads = min(1024, edges), then launches one block per tile in each scratch-space-sized batch. [source; call_d69124cda5b749fe99696b88c4e270e1, call_028a47643b3e4ea7b97df3ca8c75a810]

Each block processes 256 input values using two cost buffers and predecessor storage. The first forward/backward pass derives a starting state; the second applies the tail-biting constraint and writes reconstructed values and unpacked indices. These data paths and calculations are untouched. [source; call_028a47643b3e4ea7b97df3ca8c75a810, call_d69124cda5b749fe99696b88c4e270e1]

A scalar enumeration of the inspected launch formulas produced 1024 threads for K=1–6, 512 for K=7 and 256 for K=8. Every launch fits the declared bound, and the existing 1024-stride loops cover every edge exactly once. [execution; call_028a47643b3e4ea7b97df3ca8c75a810, call_b52746162bb947b9933a71ff20bdf335]

Unlike changing block geometry, this patch preserves the work partition and supplies an explicit kernel declaration constraint. Whether that changes generated resource usage enough to address the reported architecture concern is not established. [inference; call_d69124cda5b749fe99696b88c4e270e1, call_028a47643b3e4ea7b97df3ca8c75a810]

## Uncertainty and limits

No CUDA compilation, GPU execution, register-allocation inspection or performance measurement was performed; Blackwell compatibility remains unverified.

No eligible CUDA documentation was supplied to establish compiler-version-specific launch-bound behavior.

The Python check models integer launch geometry and indexing only, not kernel synchronization or numerical correctness.
