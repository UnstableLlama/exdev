# 8e0634b6a595bc4aa6f5fbc24a1e59ffd7eaf7f6


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/8e0634b6a595bc4aa6f5fbc24a1e59ffd7eaf7f6) · [Evidence ledger](draft.json)

Adds guarded CPU offload and restoration methods for LinearEXL3 tensors, without wiring them into the conversion loop.

- [Explicit CPU offload for quantized linear tensors](#quantized-inference)

## Problem

LinearEXL3 lacked CPU swap methods for temporarily offloading its quantized tensors during quantization. [source; call_01bc104e87f145ad95e378382dbd0607, call_5f5197db3f75484db97f19efaa6d3354]

## Reasoning

The change adds explicit offload and restore operations rather than changing inference or automatically scheduling transfers. This provides a memory-management capability whose benefit depends on callers using it. [source; call_5f5197db3f75484db97f19efaa6d3354, call_07de5bce5cf9473e85a367871e4a8c33]

## Impact

The existing converter swaps only LinearFP16 instances before conversion; this patch does not add a call to swap newly quantized EXL3 layers. Immediate converter VRAM savings are therefore not established. [source; call_c1a2740bce0746dc8640ba77f821e0d8, call_07de5bce5cf9473e85a367871e4a8c33, call_5f5197db3f75484db97f19efaa6d3354]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure and a reporter-provided environment workaround, not CPU tensor swapping. [source; call_232e7da8903b4de0b731d0d58336a7b5]

<a id="quantized-inference"></a>

## Explicit CPU offload for quantized linear tensors

Construction initializes swap_device to None. swap_cpu records the trellis device, then replaces each present su, sv, suh, svh, trellis and bias tensor with its CPU counterpart. The constructor already requires a non-null trellis. [source; call_5f5197db3f75484db97f19efaa6d3354, call_01bc104e87f145ad95e378382dbd0607]

unswap_cpu moves the same six optional tensor attributes to the saved device and clears the marker. Repeated swaps while marked, and restores while unmarked, return immediately. Restoration uses one shared destination, not a separate original device per tensor. [source; call_5f5197db3f75484db97f19efaa6d3354]

The methods preserve the stored quantized representation: they transfer packed and unpacked sign/scale tensors and the trellis without reconstructing a dense weight. Forward and weight reconstruction remain unchanged and do not automatically restore swapped tensors. [source; call_5f5197db3f75484db97f19efaa6d3354, call_01bc104e87f145ad95e378382dbd0607]

Explicit offload can reduce device-resident tensor storage while another layer is quantized, at the cost of CPU storage and transfer work. Callers must arrange restoration before device-side use; the patch supplies the mechanism rather than that scheduling policy. [inference; call_5f5197db3f75484db97f19efaa6d3354, call_01bc104e87f145ad95e378382dbd0607, call_07de5bce5cf9473e85a367871e4a8c33]

## Uncertainty and limits

No repository or CUDA execution was performed; transfer costs, allocator behavior and peak VRAM savings remain unmeasured.

A scalar calculation would not meaningfully validate this device-transfer change; tensor placement and restoration require runtime testing.
