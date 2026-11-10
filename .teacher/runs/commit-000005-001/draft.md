# 90db82667efc676ae3e95fe22e1dee2db5696920


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/90db82667efc676ae3e95fe22e1dee2db5696920) · [Evidence ledger](draft.json)

Corrects “for a smaller models” to “for smaller models” in the README.

- [Conversion-time wording](#documentation-wording)

## Problem

The README conversion-time description used the ungrammatical phrase “for a smaller models.” [source; call_70b514af321b4d79882895c191f2e21e]

## Reasoning

Removing “a” makes the phrase agree with the plural “models,” without changing the surrounding conversion claims. [source; call_70b514af321b4d79882895c191f2e21e]

## Impact

The change corrects README prose only; it does not alter executable code or the stated performance estimates. [source; call_70b514af321b4d79882895c191f2e21e]

<a id="documentation-wording"></a>

## Conversion-time wording

README.md now says conversion takes “a couple of minutes for smaller models,” preserving the existing contrast with larger models. [source; call_70b514af321b4d79882895c191f2e21e]

## Uncertainty and limits

The surrounding performance estimates were not verified. No computation or runtime test is useful for this grammatical correction.
