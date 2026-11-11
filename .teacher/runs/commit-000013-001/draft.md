# 08166e3f42463b13c51802ea892fb8ac66d90a45


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/08166e3f42463b13c51802ea892fb8ac66d90a45) · [Evidence ledger](draft.json)

Replaces two-stage scale grid search with golden-section search, reducing objective evaluations while assuming unimodal sampled quantization error.

- [Golden-section global-scale selection](#quantizer)

## Problem

Global-scale selection previously evaluated sampled quantization error on a coarse grid followed by a finer grid, repeatedly invoking quantize_tiles. [source; call_9cdb6553ae474b7b8f39a63c97fe0dd8]

## Reasoning

Golden-section search reuses one evaluated interior point after each interval reduction, trading grid coverage for an explicit assumption that error is unimodal in scale. [source; call_9cdb6553ae474b7b8f39a63c97fe0dd8]

## Impact

The scalar search model required 13 objective evaluations rather than the old loops' 28, a 53.6% reduction in evaluation count, not a measured quantization speedup. [execution; call_147f128e63d4445d8f3abec7aadf076d]

<a id="quantizer"></a>

## Golden-section global-scale selection

g_scale_gss replaces g_scale_mse_gridsearch while retaining its tile sampling and objective. Sampled 16-by-16 tiles are flattened to 256 elements and permuted into tensor-core order. Each objective evaluation quantizes tiles multiplied by scale, divides reconstructed values by that scale, and averages squared reconstruction error. This is direct sampled error, not the later Hessian-weighted proxy error. [source; call_0bf01a95088340dabc547570db4549bd, call_9cdb6553ae474b7b8f39a63c97fe0dd8]

The new interval is [0.1, 1.9], replacing the coarse [0.25, 1.075] grid and its local refinement. With phi=(1+sqrt(5))/2 and resphi=2-phi, the two interior points permit reuse of one objective value per iteration. The 0.01 tolerance bounds interval width in scale units; it is not an error threshold. [source; call_9cdb6553ae474b7b8f39a63c97fe0dd8]

A standard-library transcription on (scale-0.8)^2 performed 11 interval reductions and 13 evaluations, ending with width 0.0090449977 and midpoint 0.8011063168. The previous inclusive loops perform 12+16=28 evaluations. [execution; call_147f128e63d4445d8f3abec7aadf076d]

The return value is the final interval midpoint rather than the best evaluated point. Verbose output now shows interval bounds and reports the average of the two cached objective values, not an evaluation at the returned midpoint. A non-unimodal objective can invalidate interval elimination, so fewer evaluations do not establish a better minimum. [inference; call_9cdb6553ae474b7b8f39a63c97fe0dd8]

quantize_exl3 calls the new search after channel normalization and Hadamard transforms. It then multiplies weight_r by g_scale and divides su by g_scale before LDLQ, preserving the inverse scaling used when reconstructing weights and storing input-channel scales. [source; call_0bf01a95088340dabc547570db4549bd, call_9cdb6553ae474b7b8f39a63c97fe0dd8]

The patch removes the unused outlier-ratio search alternative. It also replaces the scaling progress total with 100 and removes search-loop progress updates, although the progress-bar argument remains accepted. [source; call_9cdb6553ae474b7b8f39a63c97fe0dd8]

## Uncertainty and limits

No repository quantizer or CUDA kernel was executed; runtime and quantization-quality effects remain unmeasured.

The scalar check used Python double precision and a synthetic quadratic objective, not tensor quantization error. The inspected sources do not establish unimodality or justify the chosen search bounds and tolerance.
