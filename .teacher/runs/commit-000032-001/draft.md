# 1d77c0525ab2b1e716de6147023a48041496110c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1d77c0525ab2b1e716de6147023a48041496110c) · [Evidence ledger](draft.json)

Pads Linear output widths and loaded FP16 tensors to multiples of 128, accommodating nonaligned vocabulary projections before EXL3 conversion.

- [Align linear output dimensions through zero padding](#modules)

## Problem

Linear previously retained the exact output width, while EXL3 quantization requires its transposed weight's output dimension to be divisible by 128. Nonaligned vocabulary projections could violate that requirement. [source; call_c7e5c69d9e0646549110b604e5d7e93c, call_149990c644184411bb771111ed351bf7, call_c4bce6f26d4746a585267aa4b95af671, call_525c45ad2b8d47b397d97ead5bc86301]

## Reasoning

The patch rounds output widths upward and zero-pads loaded weights and optional biases before constructing LinearFP16, so conversion receives physically padded tensors rather than only enlarged dimension metadata. [source; call_4e3764fc6d944d5ba1aa2adee5053803, call_c7e5c69d9e0646549110b604e5d7e93c]

## Impact

Padding applies to every Linear by default, not only vocabulary heads. Already aligned dimensions are unchanged; unaligned dimensions consume additional storage and produce wider outputs because Linear.forward does not trim them. [source; call_4e3764fc6d944d5ba1aa2adee5053803, call_c7e5c69d9e0646549110b604e5d7e93c, call_149990c644184411bb771111ed351bf7]

## Source Notes

An earlier annotation reported a lowercase/uppercase EXL3 metadata discriminator mismatch. [ancestor; call_c1b07069924d457bafe093a3268eabf4]

That mismatch is already removed in the inspected parent: both Linear.quant_format_id and its metadata consumer use lowercase 'exl3'. This patch leaves those paths unchanged. [source; call_c7e5c69d9e0646549110b604e5d7e93c, call_4e99eae3dcd247a8b8684ae52bf23843, call_4e3764fc6d944d5ba1aa2adee5053803]

<a id="modules"></a>

## Align linear output dimensions through zero padding

Linear.__init__ adds optional pad_to=128, preserves the requested width as out_features_unpadded, and computes ceil(out_features / pad_to) × pad_to. Here 'odd' means nonaligned, not merely an odd integer. The default matches the quantizer's size_n % 128 assertion. [source; call_4e3764fc6d944d5ba1aa2adee5053803, call_c4bce6f26d4746a585267aa4b95af671]

pad_out returns None or already-aligned tensors unchanged. Otherwise it allocates zeros with the original dtype and device, copies weight rows or bias entries into the prefix, and returns contiguous storage. For fused weights, load_fp16 selects the requested row range before padding the weight. [source; call_4e3764fc6d944d5ba1aa2adee5053803]

LinearFP16 transposes the padded weight into input-by-output layout. convert_exl3 retrieves that tensor for quantization, and weights_numel now counts the padded width. This aligns storage, quantization input and reported dimensions, at the cost of retaining extra output channels rather than trimming them at the Linear boundary. [source; call_149990c644184411bb771111ed351bf7, call_c7e5c69d9e0646549110b604e5d7e93c, call_4e3764fc6d944d5ba1aa2adee5053803]

A standard-library transcription verified rounding invariants for widths 1–9999: the result is divisible by 128 and adds between 0 and 127 channels. Example widths 129 and 151665 round to 256 and 151680 respectively. [execution; call_93c261f122ea48bd9ce7e2db6dd40875]

## Uncertainty and limits

The arithmetic check executes a scalar transcription, not repository tensor operations, conversion, or GPU kernels.

End-to-end compatibility of padded outputs with generation and non-vocabulary projections was not established.

The fused-weight branch pads bias before slicing it; compatibility across fused bias layouts was not executed or established.
