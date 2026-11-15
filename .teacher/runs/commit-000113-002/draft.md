# 1d4920f25a27b077bf69f1dee3b5a55fcaf7e0f0


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1d4920f25a27b077bf69f1dee3b5a55fcaf7e0f0) · [Evidence ledger](draft.json)

Accepts zero min-p as a no-op, fixing default ComboSampler construction, and excludes the previously accepted endpoint of one.

- [Zero min-p as a neutral sampling step](#sampling)

## Problem

ComboSampler defaults min_p to zero, but its nonzero-temperature branch constructed SS_MinP(0), which rejected zero with an assertion. [source; call_cf1ba41ca71f45058be99520b8672073, call_4c3e12f4da2e4063ae6dc6cefc93f940]

## Reasoning

The patch changes the accepted interval from (0, 1] to [0, 1) and makes zero select SS_NoOp through the existing alternative-step mechanism. [source; call_d7f2b6a39c7148c2bbc48d37146464e4]

## Impact

This removes the default ComboSampler min-p construction failure. Positive values below one retain their existing filtering behavior; exactly one now fails validation when assertions are enabled. [source; call_d7f2b6a39c7148c2bbc48d37146464e4, call_cf1ba41ca71f45058be99520b8672073]

## Source Notes

The earlier zero-temperature entry recorded the default min-p failure as persisting on the nonzero-temperature path. [ancestor; call_d82e369ce1b8445ca74651a3495995d4]

PR #30, “fix: don't add min_p and top_p samplers to stack if falsy,” reports assertions for zero-valued min_p and top_p. Its relationship to this change is inferred from the matching min_p assertion, not an explicit upstream link. The task changes min-p only, using step substitution rather than the omission proposed by the PR title. [inference; call_bce2656f4ac44748a33c926534042f01, call_d7f2b6a39c7148c2bbc48d37146464e4]

<a id="sampling"></a>

## Zero min-p as a neutral sampling step

CustomSampler calls alt() before prep(). Replacing zero-valued min-p with SS_NoOp therefore avoids both min-p's normalization prerequisite and its masking operation. The no-op leaves sampling state unchanged; it remains in the step list rather than being deleted. [source; call_4c3e12f4da2e4063ae6dc6cefc93f940, call_d7f2b6a39c7148c2bbc48d37146464e4]

Active min-p retains probabilities greater than or equal to min_p times the largest probability. Unsorted normalized input uses a row maximum; sorted normalized input uses its first column. Masking marks the result unnormalized while preserving whether it is sorted. [source; call_4c3e12f4da2e4063ae6dc6cefc93f940]

Zero represents no relative probability cutoff. One would retain only maximum-probability candidates, including ties, but is now excluded by the constructor. The patch supplies no explanation for excluding this endpoint. [source; call_4c3e12f4da2e4063ae6dc6cefc93f940, call_d7f2b6a39c7148c2bbc48d37146464e4]

A scalar transcription verified the changed endpoint predicates. For probabilities [0.6, 0.3, 0.1], a min-p fraction of 0.5 produces threshold 0.3 and retains the first two values, demonstrating inclusive threshold comparison. [execution; call_f3741f62fba4414291c2e1580b2ffb97]

ComboSampler's zero-temperature branch already bypasses min-p entirely. DefaultSampler continues using 0.08, so its construction and filtering are unchanged. [source; call_cf1ba41ca71f45058be99520b8672073]

## Uncertainty and limits

No repository sampler, PyTorch operation or GPU kernel was executed. The scalar check models predicates and filtering with Python numbers, not tensor precision or sampled-token equivalence.
