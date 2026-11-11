# 897e20a2ad1e10a7d3b09c63826d058c0f3bc651


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/897e20a2ad1e10a7d3b09c63826d058c0f3bc651) · [Evidence ledger](draft.json)

Accept FP32 biases in dense and EXL3 constructors by converting them to FP16, removing the EXL3 bias assertion that could interrupt conversion.

- [Normalize FP32 biases for dense and EXL3 layers](#quantized-inference)

## Problem

LinearEXL3 rejected FP32 bias tensors, including biases preserved from LinearFP16 during conversion. [source; call_b3507c645f0049afb182f3aa701daeda, call_41033f96b7da4be4b8f8939105faa310, call_119a504d7463413daf4bf5466213a851]

## Reasoning

Normalize FP32 biases at construction rather than requiring callers to cast them: both implementations now convert non-None torch.float biases to torch.half before storing them. [source; call_b49f156460cb46e99400c0636b6b7401, call_1f4d8fce89a344de9760989d88af9c8b]

## Impact

The change covers dense loading, direct EXL3 loading and dense-to-EXL3 conversion. Bias accessors and tensor export subsequently expose the converted bias. [source; call_119a504d7463413daf4bf5466213a851, call_b3507c645f0049afb182f3aa701daeda, call_41033f96b7da4be4b8f8939105faa310, call_b49f156460cb46e99400c0636b6b7401, call_1f4d8fce89a344de9760989d88af9c8b]

## Source Notes

Issue #11, “AssertionError: bias is wrong datatype,” was reported by async0x42 during DeepCoder-14B-Preview quantization. Its connection to this change is inferred from the traceback matching the removed LinearEXL3 assertion; the supplied discussion does not explicitly link the commit. [inference; call_978420725a2b4eff821a15445bc2861e, call_b49f156460cb46e99400c0636b6b7401]

The earlier quantized-inference entry describes FP16 bias as part of the EXL3 constructor contract and notes that dense weights already receive FP32-to-FP16 conversion. [ancestor; call_91cda48299104bc9b261db66522a878a]

<a id="quantized-inference"></a>

## Normalize FP32 biases for dense and EXL3 layers

Linear.load_fp16 passes loaded biases into LinearFP16; convert_exl3 later obtains that stored bias through get_bias_tensor and forwards it to LinearEXL3. Casting in LinearFP16 normalizes this upstream path, while casting independently in LinearEXL3 also handles biases loaded directly from quantized storage. [source; call_119a504d7463413daf4bf5466213a851, call_1f4d8fce89a344de9760989d88af9c8b, call_b49f156460cb46e99400c0636b6b7401]

This is FP32 input acceptance through downcasting, not FP32 bias preservation. Dense forward adds the stored bias to its half-precision output; EXL3 forward casts its result to the stored bias dtype before addition. None and existing half biases bypass the new conversion. [source; call_41033f96b7da4be4b8f8939105faa310, call_b3507c645f0049afb182f3aa701daeda, call_b49f156460cb46e99400c0636b6b7401, call_1f4d8fce89a344de9760989d88af9c8b]

A standard-library scalar illustration rounded FP32 0.10000000149011612 to binary16 0.0999755859375, showing the precision tradeoff of normalization. This did not execute repository code. [execution; call_83f00cf39cb34386bcb003cc55fc69f9]

EXL3 also loses its general bias-dtype assertion: non-FP32, non-half biases now pass this constructor check unchanged. The patch does not establish their downstream compatibility. LinearFP16_torch is unchanged. [source; call_b49f156460cb46e99400c0636b6b7401, call_41033f96b7da4be4b8f8939105faa310]

## Uncertainty and limits

No PyTorch constructor, CUDA inference or model conversion was executed. The scalar check illustrates rounding only, not framework casting behavior or model accuracy.

The reported issue does not establish the offending tensor's dtype; successful conversion of that model remains unverified.
