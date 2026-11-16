# d54648bfaba4ab016fc3345938cc9c0f1b02be48


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d54648bfaba4ab016fc3345938cc9c0f1b02be48) · [Evidence ledger](draft.json)

LinearFP16 replaces zero-filled output allocation with empty allocation and simplifies dtype selection. Existing multiplication paths supply overwrite semantics; speedup and numerical behavior were not measured.

- [Allocate dense linear output without zero initialization](#linear-fp16)

## Problem

LinearFP16.forward zero-filled its output before assigning the matrix product, doing initialization that successful multiplication does not need. [source; call_c1a1a6ca205e49929683b4e2b0e15816, call_69a96ef9e0924ad39ec98c84ca926a91]

## Reasoning

Replacing zeros with empty avoids the explicit zero-fill while preserving allocation shape, device and subsequent multiplication. This is a performance optimization, not a reduction in output storage. [inference; call_2b076d6d2fcd41bd94b06cc99f5d9704, call_c1a1a6ca205e49929683b4e2b0e15816]

## Impact

Bias addition and restoration of the input's leading dimensions remain unchanged; correctness now explicitly relies on multiplication writing the output before bias reads it. [source; call_2b076d6d2fcd41bd94b06cc99f5d9704, call_c1a1a6ca205e49929683b4e2b0e15816]

## Source Notes

The root quantized-inference entry was read. It establishes the original dense alternative and its cuBLAS alpha=1, beta=0 overwrite design. [ancestor; call_028b605b66f0406aa0ea4591c6432c6d]

Issue #39, “Gemma 3 architecture not in list?”, concerns architecture availability and later frontend/BOS discussion; it supplies no explicit connection to this allocation change. [source; call_80429a6b008a49d1b17bd46e9e5f20df]

<a id="linear-fp16"></a>

## Allocate dense linear output without zero initialization

forward flattens input leading dimensions and allocates a two-dimensional output. Matching input/output dtypes select torch.matmul with out=y; differing dtypes select ext.hgemm. Neither selection changes in this commit. [source; call_c1a1a6ca205e49929683b4e2b0e15816, call_2b076d6d2fcd41bd94b06cc99f5d9704]

The native alternative requires two-dimensional, shape-compatible half inputs and half or float output. Both cuBLAS branches pass alpha=1 and beta=0, selecting the product without accumulation of previous output contents. This existing overwrite contract supplies the precondition for removing zero initialization. [source; call_69a96ef9e0924ad39ec98c84ca926a91, call_2b076d6d2fcd41bd94b06cc99f5d9704]

Dtype selection changes from first_not_none(out_dtype, self.out_dtype, torch.half) to an or chain. The helper selected the first non-None value; the replacement selects the first truthy value, retaining the same priority for truthy dtype values and falling back to half. [source; call_2b076d6d2fcd41bd94b06cc99f5d9704, call_689269118bde4ef39c2f2d4a686e6f0e]

## Uncertainty and limits

No PyTorch or CUDA execution or performance measurement was performed. A scalar computation would not establish allocation cost or native output-write behavior.

The dtype expression now uses truthiness rather than an explicit None test. Actual torch.dtype truthiness was not tested; equivalence is conditional on supplied dtype objects being truthy.
