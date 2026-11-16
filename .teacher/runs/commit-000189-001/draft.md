# d54648bfaba4ab016fc3345938cc9c0f1b02be48


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d54648bfaba4ab016fc3345938cc9c0f1b02be48) · [Evidence ledger](draft.json)

LinearFP16 stops zero-initializing its matrix-product output and simplifies dtype fallback. Existing overwrite-oriented multiplication supports the change; performance and numerical behavior remain unmeasured.

- [Allocate dense linear output without initialization](#quantized-inference)

## Problem

LinearFP16.forward zero-initialized an output buffer immediately before matrix multiplication wrote into it. [source; call_cc2ff63e62a04f2e8318553daa4cd493]

## Reasoning

Replacing zeros with empty avoids requesting initialization. This relies on multiplication producing the output before the subsequent in-place bias addition. [inference; call_88c8916292284ba3ac450d585d49ab2d, call_cc2ff63e62a04f2e8318553daa4cd493]

## Impact

Output dimensions, device, multiplication dispatch, bias addition and final reshaping remain unchanged; no speedup is measured. [source; call_88c8916292284ba3ac450d585d49ab2d, call_cc2ff63e62a04f2e8318553daa4cd493]

## Source Notes

The root quantized-inference entry establishes the dense backend's provenance. The later dtype-dispatch entry explains the existing Torch/native split and records native alpha=1, beta=0 operation. [ancestor; call_0503fe4345c1466daa918efa6b9920c4, call_b2f0ee6400c3433aa26c8c79298643f6]

<a id="quantized-inference"></a>

## Allocate dense linear output without initialization

forward flattens the input's leading dimensions and now allocates an empty (flattened rows, out_features) tensor on the input device. Matching input/output dtypes use torch.matmul with out=y; differing dtypes use ext.hgemm. Bias is added only after multiplication, and the original leading dimensions are restored. [source; call_88c8916292284ba3ac450d585d49ab2d, call_cc2ff63e62a04f2e8318553daa4cd493]

The retained native helper requires two-dimensional half inputs, compatible matrix dimensions and half or float output. Its half-output cublasHgemm and float-output cublasGemmEx calls both set alpha=1 and beta=0, requesting the matrix product without accumulation of the previous output. This existing overwrite policy supplies the precondition for removing initialization; dispatch itself is not changed. [source; call_4c2352ee71a44146abdce2888f4881d3, call_88c8916292284ba3ac450d585d49ab2d]

The accompanying dtype edit replaces first_not_none(out_dtype, self.out_dtype, torch.half) with an or chain. The former selects the first value that is not None; the latter selects the first truthy value. Both retain call-level, instance-level, then half ordering for truthy dtype values. This expression simplification does not supply the overwrite precondition needed by empty allocation. [source; call_0773b117e0264b8c9d02a5e9005c9bba, call_88c8916292284ba3ac450d585d49ab2d]

## Uncertainty and limits

No Torch, CUDA or cuBLAS execution, numerical comparison or allocation benchmark was performed. A standard-library scalar calculation would not validate library output-buffer handling or initialization cost.

Equivalence of the dtype expressions depends on supplied dtype values being truthy; actual torch.dtype truth behavior was not executed.
