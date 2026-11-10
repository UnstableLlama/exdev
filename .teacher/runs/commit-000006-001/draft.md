# 7163258443e84ddfee2517adb6d8d46794c507d1


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/7163258443e84ddfee2517adb6d8d46794c507d1) · [Evidence ledger](draft.json)

Removes an include for the absent exl3_gemv.cuh header, preserving existing native Python bindings.

- [Remove an unavailable binding header](#native-bindings)

## Problem

bindings.cpp included quant/exl3_gemv.cuh, but that header is absent from the parent revision's quant directory. [source; call_409426339cec41f29b4c76260c76546f, call_0455c0fce9ab48ff80fe8bc72c98b232]

## Reasoning

Removing the stale include eliminates a missing-header dependency without changing the Python binding registrations. [source; call_df65bf6cb9124be0bbb2fe93afe37037, call_409426339cec41f29b4c76260c76546f]

## Impact

The change should remove this compilation blocker when building against the checked-in headers; it does not establish that the entire extension builds successfully. [inference; call_df65bf6cb9124be0bbb2fe93afe37037, call_0455c0fce9ab48ff80fe8bc72c98b232]

<a id="native-bindings"></a>

## Remove an unavailable binding header

The sole edit deletes the exl3_gemv.cuh include. The existing exl3_gemm.cuh include remains, as do the exl3_gemm and exl3_gemm_num_kernel_variants Python registrations; no exl3_gemv registration appears in the inspected binding module. [source; call_df65bf6cb9124be0bbb2fe93afe37037, call_409426339cec41f29b4c76260c76546f]

This repairs the translation unit's include dependencies rather than supplying a new GEMV implementation or changing the exposed quantized multiplication API. [inference; call_df65bf6cb9124be0bbb2fe93afe37037, call_409426339cec41f29b4c76260c76546f, call_0455c0fce9ab48ff80fe8bc72c98b232]

## Uncertainty and limits

No native build or runtime test was executed. A scalar computation would not meaningfully verify this preprocessor dependency change.
