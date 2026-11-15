# a7a6681e11d9bb99f5d1b9e8d223cb402ff80969


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a7a6681e11d9bb99f5d1b9e8d223cb402ff80969) · [Evidence ledger](draft.json)

Accepts top_p=0 and applies maximum truncation instead of treating zero as a no-op; top_p=1 remains neutral.

- [Zero top-p as maximum truncation](#sampling)

## Problem

SS_TopP rejected zero at construction, despite having a zero-valued no-op alternative that ordinary construction could not reach. [source; call_44e47f1a7da84571befaa6b518fd38e1, call_59cbb1cad27c4ea58aeb0ef8c92cc7a8]

## Reasoning

The patch accepts the closed interval [0, 1] and removes zero from no-op substitution. Zero now means maximum truncation; one remains the setting that disables this filtering step. [source; call_44e47f1a7da84571befaa6b518fd38e1, call_59cbb1cad27c4ea58aeb0ef8c92cc7a8]

## Impact

ComboSampler's nonzero-temperature branch can now construct SS_TopP(0). Its default top_p=1 is unchanged. TopPSampler already routes zero directly to argmax, and ComboSampler's zero-temperature branch bypasses top-p. [source; call_0eafca690a7347c4a83d254da6e17e4a, call_44e47f1a7da84571befaa6b518fd38e1]

## Source Notes

The preceding entry describes making min-p's upper endpoint inclusive while retaining zero as its no-op setting. [ancestor; call_6218e4144e6c4365aa4fb968ca1a44f8]

PR #30, “fix: don't add min_p and top_p samplers to stack if falsy,” reports zero-value assertions and uncertainty about disabling filters. Its relationship to this patch is inferred from the matching top_p assertion and endpoint semantics, not an explicit upstream link. Reporter randoentity differs from supplied fix author turboderp; the patch activates zero-valued top-p rather than omitting it. [inference; call_044a48f0fda242b8bb1b8a3f863e86cc, call_44e47f1a7da84571befaa6b518fd38e1]

<a id="sampling"></a>

## Zero top-p as maximum truncation

CustomSampler resolves alternatives before preparing steps. Since zero no longer becomes SS_NoOp, it follows SS_TopP's existing normalization and descending-sort prerequisites rather than an argmax shortcut. [source; call_59cbb1cad27c4ea58aeb0ef8c92cc7a8, call_44e47f1a7da84571befaa6b518fd38e1]

SS_TopP.run compares cumulative normalized probability with top_p, masks positions after the first, and marks the result PROBS_S. With a valid positive-mass distribution and top_p=0, only the first sorted candidate survives—even when maxima tie. The unchanged SS_Sample path maps the selected sorted position back through state.indices. [source; call_59cbb1cad27c4ea58aeb0ef8c92cc7a8]

A scalar transcription confirmed that zero alone changes acceptance among −0.1, 0, 0.5, 1 and 1.1. At zero, [0.6, 0.3, 0.1] becomes [0.6, 0, 0], and tied input [0.4, 0.4, 0.2] becomes [0.4, 0, 0]. At one, no-op substitution preserves both input rows. [execution; call_c85df2431b9e4d308622bd9e889c17c3]

## Uncertainty and limits

No repository sampler, PyTorch operation or GPU kernel was executed. The scalar transcription covers finite Python probabilities, not tensor rounding, nonfinite inputs or stochastic sampling.
