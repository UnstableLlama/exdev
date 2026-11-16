# d54648bfaba4ab016fc3345938cc9c0f1b02be48


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d54648bfaba4ab016fc3345938cc9c0f1b02be48) · [Evidence ledger](draft.json)

LinearFP16 uses an uninitialized output buffer instead of zero filling it and simplifies dtype fallback. Existing multiplication supplies the output values; performance remains unmeasured.

- [Allocate dense linear output without zero filling](#quantized-inference)

## Problem

LinearFP16.forward zero-filled an output buffer immediately before matrix multiplication wrote its result into it. [source; call_3a379c92d4e7403b95dcfc51645011e1]

## Reasoning

Replacing zeros with empty removes initialization work. The existing Torch branch supplies out=y; the native branch uses alpha=1 and beta=0, requesting a product without accumulating the previous output. [source; call_fafcddb6438a49188f568417ed208339, call_3a379c92d4e7403b95dcfc51645011e1, call_0137a72af76b45e6b12e49ebb9937bb1]

## Impact

Output dimensions, device, bias addition and final reshaping remain unchanged. Any latency improvement is unmeasured. [source; call_fafcddb6438a49188f568417ed208339, call_3a379c92d4e7403b95dcfc51645011e1]

## Source Notes

The root quantized-inference entry establishes the dense backend’s original role; the later dtype-dispatch entry explains the existing Torch/native split and native half-input restriction. Both entries were read. [ancestor; call_21696b8527c540fe958da282de4b74d6, call_82aa3b65a1ed49acb708edc6107f3a12]

Issue #39, “Gemma 3 architecture not in list?”, concerns architecture availability and subsequent frontend discussion, not evidence validating this output-allocation change. [source; call_ad87dcb25df143faa1848c85f31faeae]

<a id="quantized-inference"></a>

## Allocate dense linear output without zero filling

The buffer remains a flattened-row-count × out_features tensor. Matching input/output dtypes select torch.matmul; differing dtypes select ext.hgemm. Both precede the optional in-place bias addition, so successful multiplication supplies the initialization that bias addition needs. [source; call_fafcddb6438a49188f568417ed208339, call_3a379c92d4e7403b95dcfc51645011e1, call_0137a72af76b45e6b12e49ebb9937bb1]

The accompanying dtype edit replaces first_not_none with an or chain: call override, instance default, then torch.half. The old helper explicitly skipped only None; the new expression skips false-valued objects. The declared interface remains torch.dtype or None, and the now-unused helper import remains. [source; call_fafcddb6438a49188f568417ed208339, call_3719e6672f8943edb2e48638ebc0ff21, call_3a379c92d4e7403b95dcfc51645011e1]

The optimization trades a guaranteed zeroed allocation for reliance on the already-present overwrite operation; it does not introduce buffer reuse or fuse bias into multiplication. [inference; call_fafcddb6438a49188f568417ed208339, call_3a379c92d4e7403b95dcfc51645011e1]

## Uncertainty and limits

No GPU execution, numerical comparison or benchmark was performed. A scalar arithmetic model would not validate Torch/cuBLAS output-buffer behavior or allocation performance.

Successful output production still depends on the selected multiplication backend. Native hgemm checks half inputs and compatible rank-two shapes, but does not inspect cuBLAS return statuses; backend failure behavior with an uninitialized output was not tested.
