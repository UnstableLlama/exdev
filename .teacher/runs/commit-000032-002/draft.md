# 1d77c0525ab2b1e716de6147023a48041496110c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1d77c0525ab2b1e716de6147023a48041496110c) · [Evidence ledger](draft.json)

Pads Linear output weights and biases to 128-wide alignment for unaligned vocabulary conversion; fused bias slicing can undo the padding.

- [Align linear outputs before quantization](#modules)

## Problem

Output widths not divisible by 128 cannot satisfy the quantizer's right-Hadamard reshape. Here “odd” means unaligned, not necessarily odd-valued. [source; call_1b82ada99e1a4f9f8a7bcab4c6b1309f, call_42ef8cb2aa5e4983bf3da29de834ddc8]

## Reasoning

Padding before LinearFP16 transposes the weights makes the quantizer receive an aligned output dimension, rather than changing the Hadamard algorithm. [source; call_a7662f4f940841bcbcbb6308bfd7f47c, call_a7f66232ccff4837857bba663ad4e890, call_56036f33cec94ae0be2eb366f1241dc9]

## Impact

The default applies to every Linear, not only vocabulary heads. It increases stored and computed output width while leaving input width unchanged; Linear.forward does not trim the result. [source; call_a7662f4f940841bcbcbb6308bfd7f47c, call_56036f33cec94ae0be2eb366f1241dc9, call_a7f66232ccff4837857bba663ad4e890]

## Source Notes

Issue #8, titled “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800”, reports lm_head conversion failures. A turboderp comment attributes them to missing padding. Its connection to this change is inferred from the matching Linear.convert_exl3 → preapply_had_r path and padding mechanism, not an explicit commit reference. [inference; call_e628dfb3bda7440daab676019e129a1a, call_a7662f4f940841bcbcbb6308bfd7f47c, call_42ef8cb2aa5e4983bf3da29de834ddc8]

The other inspected reports concern “quantizing model: undefined symbol: __cxa_call_terminate”, “AssertionError: bias is wrong datatype”, and “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions”. They are not evidence of successful padding validation; the new helper explicitly preserves dtype. [source; call_dd2167044579465795903fb7014ca2a8, call_086ea055af0a49cf8482416e54d6356e, call_b628b6a01855445fb7fcf5ce4c38a2e9, call_09c1e00445d24eb6aa7c3dbc4ec6b897, call_a7662f4f940841bcbcbb6308bfd7f47c]

<a id="modules"></a>

## Align linear outputs before quantization

Linear.__init__ retains the requested width as out_features_unpadded and rounds out_features upward to a multiple of optional pad_to, default 128. That default matches the quantizer's had_n=128 output transform. [source; call_a7662f4f940841bcbcbb6308bfd7f47c, call_1b82ada99e1a4f9f8a7bcab4c6b1309f]

pad_out passes through None and already-aligned tensors. Otherwise it allocates zero-filled weights or bias on the original device with the original dtype, copies the existing rows or entries, and returns contiguous storage. Ordinary FP16 loading pads both tensors; fused loading slices weights before padding. [source; call_a7662f4f940841bcbcbb6308bfd7f47c]

LinearFP16 stores the transpose, so padded weight rows become output columns in the matrix passed by convert_exl3 to quantize_exl3. Existing EXL3 loading is not given a corresponding tensor-padding operation. [source; call_a7f66232ccff4837857bba663ad4e890, call_56036f33cec94ae0be2eb366f1241dc9, call_a7662f4f940841bcbcbb6308bfd7f47c]

A standard-library calculation using the two issue #8 traces gives widths 151665 and 32064. Rounding produces 151680 and 32128, adding 15 and 64 outputs respectively, or 76800 and 196608 weight elements. Both padded widths divide exactly into 128-wide blocks. [execution; call_2d686dff6ce74433937a7d42278ab6c9]

Padding trades additional storage and computation for fixed-size transform compatibility. Extra logits are not removed by Linear itself; CustomSampler.forward masks positions at and beyond actual_vocab_size when a tokenizer is supplied. [source; call_a7662f4f940841bcbcbb6308bfd7f47c, call_56036f33cec94ae0be2eb366f1241dc9, call_849bedb4f13e43d78aea435a774aa99b]

## Authoring-time findings — pending review

### fused-bias-padding-order (suspected; defect)

The fused-weight branch pads bias before slicing it, unlike weights, so slicing can discard the newly added padding.

Trigger: Linear.load selects the fused FP16 fallback for an unaligned output width with a non-None bias; for example out_features=65 and frange=(0,65).

Expected: Slice the logical bias first, then pad it to the same 128-entry width as the weight output.

Actual: The helper creates 128 bias entries, but the following slice reduces them to 65. LinearFP16.forward subsequently adds that bias to a 128-wide output, yielding incompatible dimensions.

Locations: 1d77c0525ab2b1e716de6147023a48041496110c:exllamav3/modules/linear.py — Linear.load_fp16

Source evidence: call_a7662f4f940841bcbcbb6308bfd7f47c, call_a7f66232ccff4837857bba663ad4e890, call_3a10e20da4d64614938fef1e2cf32a30, call_161a91f4643b443abb6eda13aa11b2ad

source_inspection: Whole-parent search found Linear.load as the direct load_fp16 caller. Its fallback is reachable after EXL3 lookup fails. Attention constructs fused projection ranges, including a zero-based Q range; the task diff inserts bias padding before the existing slice. [call_3a10e20da4d64614938fef1e2cf32a30, call_56036f33cec94ae0be2eb366f1241dc9, call_161a91f4643b443abb6eda13aa11b2ad, call_a7662f4f940841bcbcbb6308bfd7f47c]. Limits: Conditional reach only: aligned or bias-free fused projections do not trigger this padding-order case.

scalar_transcription: Modeled zero-padding and slicing with a Python list: 65 logical bias entries become 128, then return to 65 after slicing. [call_2d686dff6ce74433937a7d42278ab6c9]. Limits: No PyTorch broadcasting or repository implementation was executed.

## Uncertainty and limits

No tensor loading, model conversion, generation or GPU kernel was executed. The standard-library check establishes shape arithmetic only.

End-to-end compatibility of padded intermediate projections and every logits consumer was not established.

The fused-bias observation uses a synthetic unaligned projection; no supplied model checkpoint establishes that exact trigger.
