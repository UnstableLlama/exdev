# 7f3096ffd723fd908e1a2b2aa25243b2cc3f727a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/7f3096ffd723fd908e1a2b2aa25243b2cc3f727a) · [Evidence ledger](draft.json)

Counts ordinary dense weights in the EXL2 comparison adapter while preserving quantized accounting and the existing evaluation interface.

- [Count unquantized EXL2 linear weights](#usage-evaluation)

## Problem

The EXL2 comparison adapter counted every non-head linear module through q_tensors, without a separate path for ordinary, unquantized weights. [source; call_d5a8356484f5433eae02328240074315]

## Reasoning

The patch selects module.linear.weight when module.linear is truthy, wrapping it in a one-entry dictionary for the existing tensor-size helper. Otherwise it retains quantized-tensor accounting. Both branches retain module.numel() as the logical weight denominator. [source; call_cac8eec522914463abd156188acd3814, call_d5a8356484f5433eae02328240074315]

## Impact

The corrected totals flow through load_exllamav2 into comparison results and the layer-BPW or storage-size plot axis. Forward execution and perplexity calculations are unchanged; the reported VRAM value is calculated weight storage, not measured peak GPU allocation. [source; call_d5a8356484f5433eae02328240074315, call_8b67a9aeb3c34721a53b08356053f62e, call_cac8eec522914463abd156188acd3814]

## Source Notes

The earlier adapter entry distinguishes calculated weight storage from measured allocation and documents the existing autosplit reserve request. [ancestor; call_e7d4c5803d9346ea9daef79cfbcc1109]

Issue #19, “Any chance of a single model file?”, requests single-file packaging and discusses retaining the HF format. It does not report this EXL2 accounting problem. [source; call_6feaa0f4bf604eef9e08e638c1a9ea6b]

<a id="usage-evaluation"></a>

## Count unquantized EXL2 linear weights

The new selection applies to non-head ExLlamaV2Linear instances, not specifically to a block-sparse class. It counts the dense weight alone when present, avoiding simultaneous counting of both representations; quantized modules retain their full q_tensors accounting. [source; call_cac8eec522914463abd156188acd3814, call_d5a8356484f5433eae02328240074315]

get_tensor_size multiplies element size by element count and by eight to convert bytes to bits. Layer BPW divides accumulated storage bits by accumulated logical weights, while total storage adds the separately counted head. Thus dense weights contribute their actual dtype width rather than an assumed quantization rate. [source; call_d5a8356484f5433eae02328240074315, call_cac8eec522914463abd156188acd3814]

An isolated execution of the repository helper counted 4,096 synthetic two-byte elements as 65,536 bits, or 16 BPW. Combining that count arithmetically with 8,192 weights at four bits yielded eight BPW, illustrating the weighted aggregate rather than an average of module rates. [execution; call_4f089935967446b5b7709e04135c9b28]

## Uncertainty and limits

External ExLlamaV2 implementation and real block-sparse model layouts were not inspected; the relationship between module.linear, q_tensors and module.numel() remains an external compatibility assumption.

No model loading, GPU execution or perplexity evaluation was performed. The arithmetic check executed only the isolated existing helper with synthetic tensor-like objects.

The unchanged lm_head branch still uses q_tensors; this patch establishes no support for an unquantized head.
