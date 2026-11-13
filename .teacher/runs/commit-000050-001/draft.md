# 2322004f58a8e2156bd9ed5ca77e2d7abdbf40a9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2322004f58a8e2156bd9ed5ca77e2d7abdbf40a9) · [Evidence ledger](draft.json)

Release the working LDL factor immediately after quantization, before proxy-error evaluation; other edits replace existing None assignments with explicit deletions.

- [Release the working LDL factor before error evaluation](#quantizer)

## Problem

quantize_exl3 retained its working LDL factor L after its last use in ldlq, overlapping its lifetime with proxy-error evaluation and output packing. [source; call_d848526986d3471885c653454e77c519]

## Reasoning

The substantive lifetime change is del L immediately after ldlq returns. Replacing existing assignments to None with del removes local bindings but already-released tensor references were not an additional source of savings. [source; call_be6448c192d748d7b89faa2923eb46af, call_d848526986d3471885c653454e77c519]

## Impact

Dropping the working factor earlier can reduce live GPU storage during subsequent metrics and packing, without changing the quantization arithmetic. Actual peak-VRAM savings are unmeasured. [inference; call_be6448c192d748d7b89faa2923eb46af, call_d848526986d3471885c653454e77c519]

## Source Notes

The parent entry describes an earlier, separate optimization: blockwise in-place Hessian Hadamard transforms. [ancestor; call_bd16a6253d6642f28562e6fcbd884133]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension-import failure and a reporter-supplied environment workaround, not tensor-lifetime pressure. [source; call_4a55a9a41e7b4b9db71ff36b19202b76]

<a id="quantizer"></a>

## Release the working LDL factor before error evaluation

finalize_capture_H supplies H, L and input signs. quantize_exl3 moves the cached H_data['L'] to CPU and its working L to the computation device. The new deletion preserves that reusable CPU cache while ending the local working factor's lifetime after ldlq. [source; call_d848526986d3471885c653454e77c519, call_be6448c192d748d7b89faa2923eb46af]

ldlq uses slices of L for error compensation and synchronizes the configured devices before returning only quantized weights and encoded indices. No subsequent statement in quantize_exl3 needs L. [source; call_d848526986d3471885c653454e77c519]

The metric still forms E = weight_r - weight_q and aliases W = weight_r, transfers H to the device, then evaluates residual and reference Hessian contractions sequentially. Deleting weight_r does not remove W's reference. The unchanged denominator floor of 1e-8 prevents division by zero or a smaller denominator. [source; call_d848526986d3471885c653454e77c519, call_be6448c192d748d7b89faa2923eb46af]

A standard-library weak-reference model verified that assigning None and deleting a binding both preserve an independently held alias, and that deleting a separate working object leaves a cached object intact. This modeled ownership, not repository tensor execution. [execution; call_263d6ad7fe5f4bdea23e9d654603c725]

The patch shortens ownership rather than adding forced garbage collection or CUDA cache clearing. Its benefit therefore depends on whether other references retain the working storage and how the allocator reuses released memory. [inference; call_be6448c192d748d7b89faa2923eb46af, call_d848526986d3471885c653454e77c519]

## Uncertainty and limits

No PyTorch/CUDA execution, allocator measurements or end-to-end quantization tests were performed. Python object-lifetime checks do not establish GPU storage release or allocator-reserved memory reductions.
