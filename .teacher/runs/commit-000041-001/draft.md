# 41717916cedc946ff93930c13aff9bf812fda90c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/41717916cedc946ff93930c13aff9bf812fda90c) · [Evidence ledger](draft.json)

Changes automatic EXL3 reconstruction from at least 32 flattened input rows to more than 32, preserving explicit overrides.

- [Keep 32-row EXL3 operations on the quantized path](#quantized-inference)

## Problem

The default EXL3 dispatch reconstructed weights at exactly 32 input rows. The patch moves that boundary so reconstruction begins above 32 rows. [source; call_2eb38ac3636b4babafc6bd00a6c163de]

## Reasoning

The threshold counts rows after flattening all leading input dimensions, not just the original batch dimension. Explicit params['reconstruct'] values still override the automatic choice. [source; call_3536b0ad59994cfdadf372888f9a2edc, call_2eb38ac3636b4babafc6bd00a6c163de]

## Impact

At exactly 32 flattened rows with no override, forward now uses ext.exl3_gemm instead of allocating and reconstructing a dense inner weight tensor for ext.hgemm. Other row counts retain their previous dispatch. [source; call_3536b0ad59994cfdadf372888f9a2edc, call_2eb38ac3636b4babafc6bd00a6c163de]

## Source Notes

The earlier bias-normalization entry describes FP32-to-FP16 constructor conversion; this threshold-only patch leaves that behavior unchanged. [ancestor; call_9b54db2d6d3c41a999c8ccb210313d28]

<a id="quantized-inference"></a>

## Keep 32-row EXL3 operations on the quantized path

Both branches first apply the input Hadamard transform. Reconstruction obtains a fresh half-precision matrix shaped (in_features, out_features), fills it through ext.reconstruct, and passes it to ext.hgemm. The alternative passes the packed trellis directly to ext.exl3_gemm. Output transforms, bias addition and output dtype handling are unchanged. [source; call_3536b0ad59994cfdadf372888f9a2edc, call_2eb38ac3636b4babafc6bd00a6c163de]

A standard-library transcription checked row counts 1–4096: only 32 changed its default branch. Explicit True and False overrides remained unchanged at sampled boundary-adjacent sizes. This checks dispatch arithmetic, not tensor execution. [execution; call_10d884464e1d47749db618671340db3c]

The existing test_qgemm includes sizes 31, 32 and 33 and compares explicitly forced quantized and reconstructed outputs. Because both calls supply reconstruct, that test does not exercise the changed automatic threshold. [source; call_39b8d9d093a744de985ae810b04c6a32]

## Uncertainty and limits

No CUDA kernel, model inference or repository test was executed; numerical equivalence and performance gains remain unmeasured.

The inspected evidence establishes the boundary change but not why 32 is the preferred crossover.
