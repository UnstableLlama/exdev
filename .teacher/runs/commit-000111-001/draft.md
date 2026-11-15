# 7deeb0fff8c860f98021d3c7844d16e7ad9899c9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/7deeb0fff8c860f98021d3c7844d16e7ad9899c9) · [Evidence ledger](draft.json)

Makes ComboSampler use penalty-aware argmax at exactly zero temperature, bypassing filters and stochastic sampling while retaining the nonzero path.

- [Penalty-aware greedy sampling at zero temperature](#sampling)

## Problem

ComboSampler previously sent zero temperature through ordinary scaling and categorical sampling. SS_Temperature divides logits by temperature or computes its reciprocal for probabilities; neither implements an explicit greedy policy. [source; call_bf553db384274c70800795ca0c934b60, call_86e06ecd30da471f9265b3694792ee66]

## Reasoning

The patch branches after constructing the history-penalty stages: exactly zero temperature appends SS_Argmax; all other temperatures retain the existing filter-and-sample sequence. [source; call_e8210cba786e44aa91e2c0a990a08800]

## Impact

Zero-temperature selection remains penalty-aware but ignores min_p, top_k, top_p and temp_last. The chat example passes its temperature argument directly to ComboSampler. [source; call_e8210cba786e44aa91e2c0a990a08800, call_c2650ae1a3014816943c689260f9968b]

## Source Notes

The earlier ComboSampler entry records the incompatible min_p=0 default. This change bypasses that construction only at zero temperature. [ancestor; call_56fe8a0f30524538b97f044092a25a0a]

PR #22, “OpenAI compatible API example,” proposes an API endpoint and contains discussion code constructing ComboSampler. Its relevance is inferred from that shared constructor, not evidence that it motivated this fix. [inference; call_742db8c760404945b0779d7f3f5b0904, call_5b2679dfcec7495eb630f5fd131f63b0, call_e8210cba786e44aa91e2c0a990a08800]

<a id="sampling"></a>

## Penalty-aware greedy sampling at zero temperature

The zero-temperature path contains repetition penalties, presence/frequency penalties and argmax. Neutral penalties become no-ops; active penalties produce unsorted LOGITS. SS_Argmax handles both INIT and LOGITS by selecting along the vocabulary dimension and setting DONE, so this path does not require sorting, normalization or Gumbel noise. [source; call_e8210cba786e44aa91e2c0a990a08800, call_86e06ecd30da471f9265b3694792ee66]

CustomSampler.forward still applies vocabulary and allowed/blocked-token masks before the steps and reshapes the selected token to the input's non-vocabulary dimensions. Greedy therefore means the maximum of the eligible, penalty-adjusted logits, not necessarily the original model maximum. [source; call_86e06ecd30da471f9265b3694792ee66]

Zero is an exact dispatch sentinel, not an epsilon threshold. A scalar transcription selected argmax for both signed zeros, but retained filtering for 1e-9, 0.8 and 1.0. It also demonstrated that the existing probability-scaling expression 1.0/0.0 raises ZeroDivisionError. [execution; call_55d8fb4697a540b193e85b1126d015d6]

For nonzero temperature the order remains penalties, optional early temperature, min-p, top-k, top-p, optional late temperature and categorical sampling. Temperature 1.0 becomes a no-op. Existing CategoricalSampler and TopKSampler already use explicit zero-temperature argmax branches; reusing that policy avoids approximating greedy selection with a very small positive temperature. [source; call_bf553db384274c70800795ca0c934b60, call_e8210cba786e44aa91e2c0a990a08800, call_86e06ecd30da471f9265b3694792ee66]

## Authoring-time findings — pending review

### nonzero-default-min-p (suspected; defect)

The inherited default min-p construction failure persists for nonzero temperature; the new branch removes it only for zero temperature.

Trigger: Construct ComboSampler() or otherwise use nonzero temperature with min_p=0 while assertions are enabled.

Expected: Neutral min-p settings permit construction without filtering.

Actual: The nonzero branch constructs SS_MinP(0.0), whose constructor asserts 0.0 < min_p <= 1.0. The whole-parent-tree search found one direct construction site in examples/chat.py: it explicitly supplies min_p, defaults to 0.08, and exposes a zero value through its CLI. Default chat settings therefore avoid this trigger.

Locations: 7deeb0fff8c860f98021d3c7844d16e7ad9899c9:exllamav3/generator/sampler/presets.py — ComboSampler.__init__, 1db3dce033981fe2d1825165a9389b3fdcd21b67:exllamav3/generator/sampler/custom.py — SS_MinP.__init__

Source evidence: call_e8210cba786e44aa91e2c0a990a08800, call_bf553db384274c70800795ca0c934b60, call_86e06ecd30da471f9265b3694792ee66, call_e100c8eebb5d454c9dfc0e9e0faec6c3, call_c2650ae1a3014816943c689260f9968b, call_c27efd58b423492c9db5dc85250f292f

source_inspection: Compared the retained nonzero branch and default against the step assertion and inspected the direct chat caller. [call_e8210cba786e44aa91e2c0a990a08800, call_86e06ecd30da471f9265b3694792ee66, call_c27efd58b423492c9db5dc85250f292f]. Limits: No repository constructor was executed.

scalar_transcription: Evaluated the branch and min-p assertion predicates for signed zero and representative nonzero temperatures. [call_55d8fb4697a540b193e85b1126d015d6]. Limits: Standard-library scalar model only.

## Uncertainty and limits

No repository sampler, PyTorch operation or CUDA kernel was executed. The scalar check verifies branch predicates and Python reciprocal behavior, not generated tokens or tensor division-by-zero behavior.

Whole-tree literal search establishes the chat constructor and package export; dynamic or external callers are not exhaustively covered.
