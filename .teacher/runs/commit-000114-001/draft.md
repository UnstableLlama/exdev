# 86ee10b642019ab2b8be6bdaf8a9b7502f977e6e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/86ee10b642019ab2b8be6bdaf8a9b7502f977e6e) · [Evidence ledger](draft.json)

Allows min_p=1, enabling maximum-probability-only filtering while preserving ties and zero's existing no-op behavior.

- [Inclusive min-p upper endpoint](#sampling)

## Problem

SS_MinP rejected min_p=1 even though its filtering rule supports retaining maximum-probability candidates. [source; call_37f9f95072cd47b29474d13094015272, call_800c6d1d44a247bc8f7831266b55bf74]

## Reasoning

The only change makes the constructor's upper bound inclusive, accepting [0, 1] rather than [0, 1). Filtering and zero's no-op substitution remain unchanged. [source; call_37f9f95072cd47b29474d13094015272, call_800c6d1d44a247bc8f7831266b55bf74]

## Impact

ComboSampler can now construct its nonzero-temperature path with min_p=1. Its zero-temperature branch bypasses min-p; DefaultSampler's fixed 0.08 and ComboSampler's default zero are unaffected. [source; call_2291dafe4daf4d2fb6fe79dde31527b6, call_37f9f95072cd47b29474d13094015272]

## Source Notes

The parent entry describes accepting zero while excluding one. This patch restores the upper endpoint without undoing zero support. [ancestor; call_9067404078fe4d01be52675826a8bb87]

PR #30, “fix: don't add min_p and top_p samplers to stack if falsy,” reports zero-value assertions and uncertainty about whether one disables filtering. Its relationship here is inferred from the matching min_p validation topic, not an explicit upstream link. The report is by randoentity, distinct from the supplied task author turboderp; this patch accepts one rather than omitting falsy steps. [inference; call_16ac5dbdbe1d44f4acccfdf90e7b7e47, call_37f9f95072cd47b29474d13094015272]

<a id="sampling"></a>

## Inclusive min-p upper endpoint

Min-p's threshold is the largest probability multiplied by min_p. Normalized unsorted input uses a row maximum; normalized sorted input uses the first column. The inclusive comparison retains ties. At one, only maxima survive: this is maximal filtering, not an off setting. [source; call_800c6d1d44a247bc8f7831266b55bf74, call_37f9f95072cd47b29474d13094015272]

CustomSampler substitutes SS_NoOp for zero before preparing steps. One instead follows the existing normalization and masking path, which marks probabilities unnormalized while preserving sortedness. The patch does not replace this path with argmax, so tied maxima remain available to subsequent sampling. [source; call_800c6d1d44a247bc8f7831266b55bf74, call_37f9f95072cd47b29474d13094015272]

A scalar transcription confirmed that only one changes acceptance among the tested values −0.1, 0, 0.5, 1 and 1.1. At min_p=1, masking [0.6, 0.3, 0.1] gives [0.6, 0, 0], while [0.4, 0.4, 0.2] gives [0.4, 0.4, 0], preserving both tied maxima. [execution; call_784852ccace040229a4ae7ac047880d6]

## Uncertainty and limits

No repository sampler, PyTorch operation or GPU kernel was executed. The scalar transcription checks ordinary finite Python probabilities, not tensor rounding, nonfinite inputs or stochastic sampling.
