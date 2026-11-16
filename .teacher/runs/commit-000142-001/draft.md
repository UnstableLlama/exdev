# 43383ebdbcc2bc79113e6e9d4da2541f7860f92a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/43383ebdbcc2bc79113e6e9d4da2541f7860f92a) · [Evidence ledger](draft.json)

Protects the complementary repetition-penalty weight from zero, addressing the remaining infinite-logit NaN endpoint. Scalar FP32 checks support the mechanism; CUDA behavior was not tested.

- [Protecting the full-weight repetition endpoint](#sampling)

## Problem

At full repetition weight, an infinite logit could become NaN because interpolation multiplied the original logit by zero. [source; call_bbdf4426a67d4581af211e1e4842e5b4]

## Reasoning

The patch adds 1e-30 to the complementary interpolation weight, extending the existing positive offset on the penalty weight to both endpoints without adding a branch. [source; call_33f7e1f1e00a47df81c2e7788e30a26d]

## Impact

A scalar FP32 transcription changed full-weight negative-infinity output from NaN to negative infinity; positive infinity was likewise preserved. Tested finite logits and factors zero and one-half retained their previous results. [execution; call_679847a0aa2a48c78a912e7d1ea5b6a7]

## Source Notes

The earlier offset entry explicitly identified the remaining full-weight NaN endpoint. [ancestor; call_0a4cd4f7abeb4a3597f10f242eef7939]

The task removes that endpoint's zero multiplier in source; this addresses the inherited observation rather than leaving it carried over. [source; call_33f7e1f1e00a47df81c2e7788e30a26d, call_bbdf4426a67d4581af211e1e4842e5b4]

Whole-parent-tree NaN matches also include conversion diagnostics, calibration text and a quantization utility comment; these do not establish the same sampling failure. [inference; call_d5cc687c7a6142268b1c40816016ae48]

<a id="sampling"></a>

## Protecting the full-weight repetition endpoint

The kernel initializes token factors to zero, sets them to one for occurrences within the sustain window, and otherwise accumulates the maximum linearly decaying contribution. It computes w=v/rep_p for positive logits and w=v*rep_p otherwise. History scanning and this sign-dependent transformation are unchanged. [source; call_bbdf4426a67d4581af211e1e4842e5b4, call_33f7e1f1e00a47df81c2e7788e30a26d]

Previously, f=factors[i]+1e-30 protected w*f at factor zero, but f still rounded to one at full weight. The new f1=(1-f)+1e-30 protects v*f1 there. The constant is a positive numerical offset, not a recency threshold. [source; call_33f7e1f1e00a47df81c2e7788e30a26d, call_bbdf4426a67d4581af211e1e4842e5b4]

The scalar check represented the offset as approximately 1.000000003e-30, above FP32's smallest normal value, while adding it to one still rounded to one. Thus the correction must offset the complementary weight separately. [execution; call_679847a0aa2a48c78a912e7d1ea5b6a7]

Both half-input and float-input kernel specializations receive the correction and write FP32 output. SS_RepP.run directly calls the wrapper with either initial logits and newly allocated output or existing logits in place. Its alternative disables the step for rep_p=1 or a nonpositive combined history window; the native wrapper restricts batch size to one. [source; call_38af2e256cfd4aaf848cc352a0638922, call_87e0f783198941ee855e17a2866eebe1, call_bbdf4426a67d4581af211e1e4842e5b4]

This is a branch-free endpoint safeguard rather than explicit nonfinite classification. Selecting endpoint values directly would be an alternative, but the patch retains the interpolation structure. [inference; call_33f7e1f1e00a47df81c2e7788e30a26d]

## Uncertainty and limits

No CUDA kernel or repository test was executed. The scalar transcription rounds intermediate arithmetic to FP32 but does not reproduce CUDA compiler contraction or optimization.

The checked nonfinite cases use a positive finite penalty. This is not evidence of general NaN handling or validity for arbitrary penalty values.

Caller inspection establishes reach through SS_RepP, not that every generation workflow enables it or supplies infinite logits.
