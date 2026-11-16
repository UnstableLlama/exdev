# 538dcae365891784729d198539f72ceece5631eb


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/538dcae365891784729d198539f72ceece5631eb) · [Evidence ledger](draft.json)

Honors transpose requests for in-memory Safetensors overrides, restoring unquantized linear weights to their internal layout during conversion reload.

- [Preserve linear weight orientation during in-memory reload](#loading)

## Problem

In-memory replacement tensors bypassed the requested transpose, unlike file-backed loads. This broke the weight-layout round trip for unquantized linear layers. [source; call_7440558c49e242679bf2fc26d77402cf, call_7a0b624e864644f997cdf4824e2f86fc, call_d6c850a7414f418aa83a9d11628e33a8]

## Reasoning

The fix transfers the replacement tensor to the requested device, then applies .T.contiguous() when transpose=True before returning it. [source; call_27926c69da9043a9876410a9e41b1710]

## Impact

This restores the layout expected by LinearFP16 when conversion reloads collected tensors from memory; it does not change the file-backed loading paths. [source; call_597d131f6c24412c858ea7bfb64a13ea, call_d6c850a7414f418aa83a9d11628e33a8, call_27926c69da9043a9876410a9e41b1710]

## Source Notes

Issue #34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure and discusses overflow. Its connection here is only inferred from shared conversion and linear-module paths, not evidence that this transpose fix addresses that report. [inference; call_b74db269bde9488583dcda4d5ea8470e, call_27926c69da9043a9876410a9e41b1710]

<a id="loading"></a>

## Preserve linear weight orientation during in-memory reload

LinearFP16 stores weights in input-by-output layout and exports their contiguous transpose. Linear.load_fp16 requests transpose=True to recover that internal layout. Conversion collects module tensors, installs them through set_new_tensors, reloads the module, then clears the override before advancing calibration states. [source; call_7a0b624e864644f997cdf4824e2f86fc, call_d6c850a7414f418aa83a9d11628e33a8, call_597d131f6c24412c858ea7bfb64a13ea]

Previously, the override returned immediately after device transfer. The new conditional transpose restores this round trip at the shared loader boundary rather than adding conversion-specific handling to Linear. Requests without transposition retain their previous behavior. [source; call_27926c69da9043a9876410a9e41b1710, call_7440558c49e242679bf2fc26d77402cf]

A standard-library matrix transcription verified that exporting a 2-by-3 internal weight as 3-by-2 and transposing it again restores both its shape and values. For a nonsymmetric square example, omitting the transpose changed the modeled output from [31, 46] to [23, 53], showing why matching dimensions alone cannot validate orientation. [execution; call_31795b9a7559449fbed57014a69c1bc5]

## Uncertainty and limits

No model conversion, PyTorch operation or native kernel was executed. The scalar check validates layout arithmetic only, not device transfer or contiguity.

The replacement-tensor branch still bypasses file-backed dtype conversion and padding logic; the change establishes transpose handling, not complete equivalence between loading sources.
