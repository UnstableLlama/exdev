# 28b09f96df750c5943dd7aec83e7a1b8d1785b69


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/28b09f96df750c5943dd7aec83e7a1b8d1785b69) · [Evidence ledger](draft.json)

Defers restoring swapped weights until after Hessian LDL decomposition to reduce GPU allocation overlap; source inspection also exposes a possible CPU-bias carryover.

- [Delay weight restoration until after Hessian decomposition](#conversion)

## Problem

Conversion restored each FP16 layer to its original device before converting its weights to float32 and finalizing the Hessian. This kept the weight matrix resident during LDL decomposition. [source; call_7cf76af2b9ea4928a7030918c2f37e76, call_87b02b21899a44bf87edf92d5c231473, call_dcdcbbf606544384beb86e1b4cfa77b4]

## Reasoning

The change separates the intended quantization device from the weight's current storage device, allowing Hessian preparation to finish before restoring weights. [source; call_dea61c2ecef041ee9048ac3aac8355e3, call_98857ddab88b4995b813d169900ac388]

## Impact

Keeping the float32 weight on CPU during decomposition should reduce overlapping GPU allocations, at the cost of retaining that float32 representation in host memory. Peak VRAM and conversion speed were not measured. [inference; call_a7bb3f335f364492855ec7af184ffc8c, call_dea61c2ecef041ee9048ac3aac8355e3, call_98857ddab88b4995b813d169900ac388]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension-import failure and a reporter-described environment remedy, not a weight-residency failure. It does not establish motivation for this change. [source; call_5f6810a7cca14152a72c211d8a997f17]

<a id="conversion"></a>

## Delay weight restoration until after Hessian decomposition

The converter still swaps all target linears to CPU, but no longer unswaps each one before convert_exl3. That method captures swap_device before destroying the FP16 wrapper, converts the still-CPU weight to float32, and passes the saved destination to quantize_exl3. [source; call_7cf76af2b9ea4928a7030918c2f37e76, call_a7bb3f335f364492855ec7af184ffc8c, call_dea61c2ecef041ee9048ac3aac8355e3]

quantize_exl3 chooses the saved destination when supplied, calls finalize_capture_H, moves the stored L to CPU and the working L to that destination, and only then transfers the weight. finalize_capture_H restores captured H, regularizes and transforms it, computes block LDL with block size 16, and caches the result; already-finalized shared Hessians bypass recomputation. [source; call_98857ddab88b4995b813d169900ac388, call_dcdcbbf606544384beb86e1b4cfa77b4, call_3465a0d248704254862e2f3f6735c6da]

The new destination argument defaults to None, retaining weight.device for unswapped callers. LinearFP16 swap and unswap operations also become idempotent: repeated calls return instead of asserting, preserving the originally recorded destination. [source; call_98857ddab88b4995b813d169900ac388, call_7b487efadf4245a0811ad3fb243a0b1a, call_e5a954f835c4411aae0955207c4ff033]

For illustration, a 4096-by-4096 float32 weight occupies 67,108,864 bytes, or 64 MiB. This is the weight payload whose GPU residency can be deferred, not a measured reduction in peak allocated or reserved VRAM. [execution; call_3761a7a75fb6463d9052a00a01bfca69]

## Authoring-time findings — pending review

### cpu-bias-after-conversion (suspected; defect)

Delaying restoration transfers the weight but leaves a swapped bias on CPU in the newly constructed quantized layer.

Trigger: Convert a GPU-resident LinearFP16 with a non-None bias through the converter's swap_cpu path, then execute the converted layer on GPU.

Expected: The converted bias should be colocated with the GPU output before bias addition.

Actual: swap_cpu moves both weight and bias to CPU. After removal of unswap_cpu, convert_exl3 retains that CPU bias unchanged; quantize_exl3 transfers only the weight. LinearEXL3 stores the bias without a device transfer, then adds it to the output, suggesting a device mismatch.

Locations: 28b09f96df750c5943dd7aec83e7a1b8d1785b69:exllamav3/modules/linear.py — Linear.convert_exl3, 28b09f96df750c5943dd7aec83e7a1b8d1785b69:exllamav3/conversion/convert_model.py — main

Source evidence: call_e5a954f835c4411aae0955207c4ff033, call_87b02b21899a44bf87edf92d5c231473, call_a7bb3f335f364492855ec7af184ffc8c, call_98857ddab88b4995b813d169900ac388, call_440ce47cce3049f899e07bfe278edfe4

source_inspection: Whole-parent-tree caller search found the converter and tests/test_quant_fn.py. The converter swaps weights and subsequently performs module forward passes. The inspected test calls conversion without that swap sequence. The observation therefore concerns swapped, biased GPU layers, not every conversion caller. [call_f5768e56d1234fc8975acbe0e09493ae, call_7cf76af2b9ea4928a7030918c2f37e76, call_55d1f8413a404c489ecd73fc63b76549, call_440ce47cce3049f899e07bfe278edfe4]. Limits: Source inspection only; no biased-layer GPU execution.

## Uncertainty and limits

No CUDA conversion, memory profiling, or repository tests were executed. The numerical check measures only illustrative tensor-size arithmetic.

The suspected bias-device mismatch is based on source data flow; its runtime exception and affected model coverage were not tested.
