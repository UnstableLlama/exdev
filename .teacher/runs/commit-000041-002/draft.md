# 41717916cedc946ff93930c13aff9bf812fda90c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/41717916cedc946ff93930c13aff9bf812fda90c) · [Evidence ledger](draft.json)

Changes EXL3's default reconstruction threshold so exactly 32 flattened input rows use quantized GEMM; explicit overrides remain unchanged.

- [Keep exactly 32 rows on quantized GEMM](#quantized-inference)

## Problem

The default EXL3 forward dispatch selected full weight reconstruction at exactly 32 flattened input rows. The patch moves that boundary from >= 32 to > 32. [source; call_af3c23f86eab4124a5b8c577ac22e547]

## Reasoning

Keeping 32-row inputs on the quantized GEMM path is consistent with its existing dispatch tiers: several devices select a 32-row kernel, while Hopper and Blackwell distinguish rows above 32. Avoiding reconstruction at this boundary is a plausible rationale, not a demonstrated performance result. [inference; call_94ad1e2fe78d48a2824d6f5f901c8469, call_af3c23f86eab4124a5b8c577ac22e547]

## Impact

Only the default choice at 32 rows changes; explicit reconstruct=True or False continues to override the threshold. [source; call_b68bb3135591400db28d1750950ee7fa, call_af3c23f86eab4124a5b8c577ac22e547]

## Source Notes

The existing test compares explicitly forced quantized and reconstructed paths, including batch sizes 31, 32 and 33. It does not exercise default threshold selection. [source; call_a88180761a6b42269f1d404b1eb96d4f]

<a id="quantized-inference"></a>

## Keep exactly 32 rows on quantized GEMM

LinearEXL3.forward first reshapes input to (-1, in_features), so 32 counts flattened activation rows rather than necessarily the batch dimension. Both paths apply the input Hadamard transform and retain output reshaping, bias addition and dtype handling. [source; call_b68bb3135591400db28d1750950ee7fa]

The reconstructed path allocates an in_features × out_features FP16 weight tensor, decodes the trellis through ext.reconstruct, then uses ext.hgemm, a cuBLAS half-precision matrix multiply. The quantized alternative passes the trellis directly to ext.exl3_gemm, avoiding that full weight allocation. Output transforms are fused when packed output signs are supplied, or applied separately for unpacked output scales. [source; call_b68bb3135591400db28d1750950ee7fa, call_b1543f1d96a14fc3bae1d9f947a7251d, call_f73fe2d1280044aca35805cddccdcb57, call_94ad1e2fe78d48a2824d6f5f901c8469]

The selected native path still has its own preconditions: exl3_gemm checks half-precision activations/output and packed tensor shape relationships; launch requires dimensions divisible by the chosen kernel tiles and supports bitrates 1 through 8. The threshold change does not relax those constraints. [source; call_94ad1e2fe78d48a2824d6f5f901c8469, call_af3c23f86eab4124a5b8c577ac22e547]

A standard-library transcription checked row counts 1 through 4096: only 32 changed default branch, while explicit Boolean overrides remained unchanged. At 31, 32 and 33 rows the new reconstruction defaults were False, False and True. [execution; call_d510b1e277dd437eb2ab6b5d6d55a09d]

## Uncertainty and limits

No CUDA kernels or repository tests were executed; speed, numerical equivalence and device-specific success remain unmeasured.

The scalar check models Python dispatch only, not tensor reshaping, reconstruction or GPU arithmetic.
