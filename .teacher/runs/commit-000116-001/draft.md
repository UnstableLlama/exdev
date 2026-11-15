# d99acb4dce128b60802c9f02b2b3c26e5a078e8e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d99acb4dce128b60802c9f02b2b3c26e5a078e8e) · [Evidence ledger](draft.json)

Adds CUDA-backed infinity and NaN counting during calibration and per-qmap warnings before quantization, without sanitizing inputs or stopping conversion.

- [Counting nonfinite calibration activations](#calibration)

## Problem

Calibration accumulated input Gram matrices without reporting how many incoming activation values were infinite or NaN. [source; call_9740bea99cc34ba2a7e0e5e0e0a1dafe, call_fae9b1317daa4ecca1738be54959317c]

## Reasoning

The change adds diagnostics rather than numerical remediation: inputs are counted before Gram-matrix accumulation, and conversion prints warnings without aborting or replacing invalid values. [source; call_fae9b1317daa4ecca1738be54959317c, call_533ba900d061495a840e3ce0986bdf6e, call_1ce98754924946e380bcd55f69a20b16]

## Impact

Conversion reports per-qmap infinity and NaN totals after capturing a module or slice, before moving its captured matrix to CPU and proceeding with quantization. [source; call_533ba900d061495a840e3ce0986bdf6e, call_1ce98754924946e380bcd55f69a20b16]

<a id="calibration"></a>

## Counting nonfinite calibration activations

Linear.capture_H initializes a two-element torch.long counter on the layer device and a Python num_total counter for each qmap. Every capture invocation adds x.numel() and calls the new native counter before the existing first_key guard. Consequently, shared-qmap layers contribute repeated activation observations to these diagnostics even though only the first layer contributes to H; the numerator and denominator both follow this broader counting scope. [source; call_fae9b1317daa4ecca1738be54959317c, call_9740bea99cc34ba2a7e0e5e0e0a1dafe]

The existing forward path invokes capture_H only when capture parameters are present and the layer has a qmap. The whole-tree search located capture dictionaries in conversion and test_quant_fn.py; both start empty and let Linear construct the records, so these inspected callers receive the added fields automatically. [source; call_339c66a08f2f46febd48c3c0f96e15d8, call_9740bea99cc34ba2a7e0e5e0e0a1dafe, call_1ce98754924946e380bcd55f69a20b16, call_1752d09fd38d4efb9bb4300144441ed4]

The binding exports count_inf_nan(x, y). Its wrapper selects the input device and current CUDA stream, dispatches half or float inputs, and rejects other input dtypes. Half values are converted to float for classification. The kernel atomically adds infinity counts to y[0] and NaN counts to y[1], preserving totals across capture calls rather than resetting them. [source; call_054bddf5409e48c6a0292e3c0f5615a1, call_60d6b3ec13be4996a76cb6fa55d2bcfe, call_964a7d745102466c9c3701625ced4cb3]

Each block covers up to 32,768 elements using 1,024 threads: a full block assigns 32 strided elements per thread. Counts are reduced within 32-lane warps, then through 32 shared-memory warp totals, leaving thread zero to perform two global atomic additions. This aggregates updates instead of issuing an atomic operation for every nonfinite element. [source; call_964a7d745102466c9c3701625ced4cb3]

A standard-library scalar transcription visited every element exactly once for seven sizes around thread and block boundaries, including 32,768 and 32,769 elements. [execution; call_24cad25fa1c047a98ae27f3a0158febc]

The added scan and host extraction of counters trade extra calibration work for localized warnings that identify the qmap and report both nonfinite counts against the total observations. The patch provides no measured overhead or evidence that the warnings prevent quantization failures. [inference; call_fae9b1317daa4ecca1738be54959317c, call_533ba900d061495a840e3ce0986bdf6e, call_964a7d745102466c9c3701625ced4cb3]

## Uncertainty and limits

No CUDA compilation, kernel execution, or model conversion was performed. The scalar check validates only bounded indexing arithmetic, not reductions, atomics, device placement, or GPU integer-overflow behavior.

The diagnostic scans incoming activations, not the accumulated Gram matrix; it does not establish that accumulation remains finite.

The native wrapper checks the output dtype and supports half/float inputs, but does not explicitly validate tensor contiguity, output shape, or matching CUDA devices.
