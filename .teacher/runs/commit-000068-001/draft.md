# 203db0c3bfeb1273fbe15f2e9622e9aec391d53e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/203db0c3bfeb1273fbe15f2e9622e9aec391d53e) · [Evidence ledger](draft.json)

Corrects RMSNorm.forward_torch’s return annotation from dict to torch.Tensor; computation and dispatch are unchanged.

- [Correct the Torch RMSNorm return annotation](#modules)

## Problem

RMSNorm.forward_torch declared a dict return type although its implementation returns the normalized tensor x. [source; call_8588c000197d479c8274664fac02d2a5]

## Reasoning

Changing the annotation to torch.Tensor aligns the declared interface with the existing return expression and with RMSNorm.forward, without rewriting normalization. [source; call_24dfce34b5a0468e87f6ac4b36379af1, call_8588c000197d479c8274664fac02d2a5]

## Impact

The change corrects type information; arguments, defaults, tensor operations and native dispatch remain unchanged. [source; call_24dfce34b5a0468e87f6ac4b36379af1]

<a id="modules"></a>

## Correct the Torch RMSNorm return annotation

forward_torch computes the last-axis mean square in float precision, adds rms_norm_eps, and multiplies by its reciprocal square root. It restores the input dtype before applying the weight, optionally offset by constant_bias, then applies the requested or configured output dtype and returns x. The corrected annotation describes this tensor result, not a dictionary of outputs. [source; call_8588c000197d479c8274664fac02d2a5, call_24dfce34b5a0468e87f6ac4b36379af1]

The separate forward method continues to allocate an output tensor, invoke ext.rms_norm and restore the original shape. This cleanup does not select the Torch implementation in place of the native implementation. [source; call_8588c000197d479c8274664fac02d2a5, call_24dfce34b5a0468e87f6ac4b36379af1]

## Uncertainty and limits

No PyTorch execution or static type-checker run was performed. A scalar numerical check would not meaningfully validate this annotation-only change.
