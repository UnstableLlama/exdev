# cb7c70cde0ec5137c70d12afeffacd40d5db4770


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/cb7c70cde0ec5137c70d12afeffacd40d5db4770) · [Evidence ledger](draft.json)

Adds bracketed palette-color overrides and hides bracket suffixes in comparison-plot labels; chosen colors also control existing connecting-line groups.

- [Label-controlled plot colors](#usage-evaluation)

## Problem

Comparison plots previously selected colors only from format-name substrings, leaving unmatched labels black and displaying the entire label. [source; call_01be5aa0bcff4d28947bde55ef826815]

## Reasoning

The change separates display text from color selection: bracketed color names override format matching, while the visible label stops at the first opening bracket. [source; call_ee71cf42ca474c1891287a49c9bb209c]

## Impact

Color overrides also change connecting-line membership: existing plotting code groups points by color and excludes black points from lines. Evaluation scores and printed result labels are unchanged. [source; call_ee71cf42ca474c1891287a49c9bb209c, call_01be5aa0bcff4d28947bde55ef826815]

<a id="usage-evaluation"></a>

## Label-controlled plot colors

plot.get_color first searches for exact bracketed palette values: [green], [purple], [olive], [brown], [red], [blue], and [black]. It then falls back to format-name matching and finally black. This supports explicit overrides without adding a separate result field. [source; call_ee71cf42ca474c1891287a49c9bb209c, call_01be5aa0bcff4d28947bde55ef826815]

The new **** mapping supplies another black fallback marker, but does not outrank earlier format matches. Multiple bracketed colors are resolved in palette iteration order, not their textual order. [source; call_ee71cf42ca474c1891287a49c9bb209c, call_01be5aa0bcff4d28947bde55ef826815]

Displayed annotations strip surrounding whitespace from the portion before the first '[' and retain the newline plus perplexity formatted to three decimal places. Truncation applies even to unrecognized bracket content; color selection still receives the original full label. [source; call_ee71cf42ca474c1891287a49c9bb209c]

A scalar transcription selected red for 'EXL3 demo [red]', black for 'EXL3 demo [black]', purple for 'EXL3 ****', and green for 'custom [red] [green]'. It also confirmed that 'demo [unknown] suffix' displays only 'demo' before the score. [execution; call_494684b8c3384b8e819de8d6ebde203c]

## Uncertainty and limits

The check transcribed string-selection logic using standard-library Python; it did not execute the repository plotting function, Matplotlib rendering, or model evaluation.
