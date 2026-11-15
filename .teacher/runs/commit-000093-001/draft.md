# 3b4c3d4ddec78a2b9855f27f83ff72c83d24437e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3b4c3d4ddec78a2b9855f27f83ff72c83d24437e) · [Evidence ledger](draft.json)

Removes a stale README to-do item for samplers already present in the code, without changing runtime behavior.

- [Remove the obsolete sampler roadmap item](#usage-evaluation)

## Problem

The README still listed samplers—especially repetition penalties and min-P—as missing, although their implementations already existed. [source; call_66ed14e81b3a41ccaedd0a86f3af9f15, call_0712a754d3b84332bbb85ca1f4ffa202]

## Reasoning

Removing the stale bullet aligns the roadmap with existing sampling support rather than adding that support in this commit. [inference; call_66ed14e81b3a41ccaedd0a86f3af9f15, call_1ed8023045b9453592b27986334e568f]

## Impact

Only README.md changes. Constrained sampling remains on the to-do list; runtime code and defaults are unchanged. [source; call_66ed14e81b3a41ccaedd0a86f3af9f15]

<a id="usage-evaluation"></a>

## Remove the obsolete sampler roadmap item

Existing SS_MinP normalizes probabilities as needed and masks candidates below the maximum probability multiplied by min_p. SS_RepP passes logits and past token IDs to the native repetition-penalty implementation. ComboSampler already composes these steps with other penalties, temperature, top-k, top-p and final sampling. [source; call_0712a754d3b84332bbb85ca1f4ffa202, call_1ed8023045b9453592b27986334e568f]

The edit withdraws the specific claim that these samplers are missing; it does not replace it with a claim of complete sampling support or remove the surrounding early-release warning. [source; call_66ed14e81b3a41ccaedd0a86f3af9f15]

## Uncertainty and limits

Source inspection establishes that the named sampling mechanisms exist, not that every sampler configuration works correctly.

No runtime tests were run; this one-line roadmap deletion offers no meaningful numerical computation to validate.
