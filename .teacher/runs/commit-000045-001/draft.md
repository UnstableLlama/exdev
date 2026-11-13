# 3d51a39d1338d7538853ac03ec641b435b2c66ab


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3d51a39d1338d7538853ac03ec641b435b2c66ab) · [Evidence ledger](draft.json)

Guards conversion’s bits-per-weight calculation for zero-weight modules and prints no_weights instead of a numeric bitrate.

- [Report weightless modules without dividing by zero](#conversion)

## Problem

Conversion calculated bits per weight unconditionally, so a module reporting zero weights caused division by zero after its tensors were saved and before calibration state advanced. [source; call_90d0596cd75347ff9490274358e49bc4]

## Reasoning

The change represents an undefined bitrate as None rather than inventing a numeric value, and adjusts progress formatting to print no_weights instead. [source; call_e73491cf9afc4675bababc81bfbdb889]

## Impact

The zero-weight case no longer fails at this division or attempts numeric formatting of None. Quantization, tensor saving, forward passes and checkpoint logic are otherwise unchanged. [source; call_e73491cf9afc4675bababc81bfbdb889, call_90d0596cd75347ff9490274358e49bc4]

## Source Notes

The earlier conversion entry describes changes to time estimation and checkpoint frequency, separate from this bitrate-reporting correction. [ancestor; call_5df8c87b8283446d95948c4b3b81b365]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure. Its inferred overlap is only the conversion entry path named in its traceback; it does not establish motivation for this arithmetic fix. [inference; call_31b67b7e117149179519326ece828503, call_e73491cf9afc4675bababc81bfbdb889]

<a id="conversion"></a>

## Report weightless modules without dividing by zero

Module.weights_numel sums child counts, yielding zero for an empty module. TransformerBlock permits absent attention, MLP and normalization submodules; absent children are not registered. Such an empty block therefore supplies a concrete zero-weight case. [source; call_97baaee1bc7c48e390912e4237a07b2b, call_c6f476008cf74cf88ffd8a736b97e562]

main already skips calibration capture when there are no quantization maps and skips allocation when there are no linear targets. It still collects and saves module tensors, then computes their size. dsize sums tensor element counts multiplied by element sizes; multiplying by 8 converts bytes to bits. [source; call_90d0596cd75347ff9490274358e49bc4, call_d2ea65def540466da3dea1ca0f71a317]

The new conditional evaluates the division only for a nonzero weight count. Feedback uses final_bpw truthiness, so no_weights also covers a numeric zero bitrate, not exclusively None. Positive bitrates retain two-decimal formatting. [source; call_e73491cf9afc4675bababc81bfbdb889]

A standard-library scalar transcription produced ZeroDivisionError under the old expression for both zero and 16 bytes with zero weights; the new expression produced None and no_weights. With 16 bytes and 32 weights, both expressions returned 4 bits per weight. [execution; call_77975e411ecf426cbfd8e40d6ce5f321]

## Uncertainty and limits

No model conversion or GPU execution was performed. The scalar check does not establish empty-dictionary serialization behavior or end-to-end conversion success.
