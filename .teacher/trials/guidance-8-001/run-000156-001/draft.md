# cb7c70cde0ec5137c70d12afeffacd40d5db4770


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/cb7c70cde0ec5137c70d12afeffacd40d5db4770) · [Evidence ledger](draft.json)

Adds bracketed palette-color overrides to comparison plots and hides bracket suffixes from displayed labels; overrides also control connecting-line groups.

- [Label-driven plot colors](#usage-evaluation)

## Problem

Comparison plots previously selected colors only from backend-name substrings, preventing labels from explicitly overriding that choice. [source; call_c9ea918e053a403c821f7cc6362348b5, call_7b6e78499dcf404cab1c63cbdb90448a]

## Reasoning

Bracketed color tags provide presentation controls within existing model labels, without adding arguments or changing result dictionaries. [inference; call_7b6e78499dcf404cab1c63cbdb90448a, call_c9ea918e053a403c821f7cc6362348b5]

## Impact

Overrides affect point colors, annotation colors and dotted-line grouping. Selecting black excludes a point from connecting lines but not from the scatter plot. [source; call_7b6e78499dcf404cab1c63cbdb90448a, call_c9ea918e053a403c821f7cc6362348b5]

## Source Notes

The root usage-evaluation entry establishes the comparison runner and optional plotting workflow. The inspected memory-optimization entry concerns scoring temporaries, not plotting. [ancestor; call_685779dcd63b4e6b8638437c8739b44a, call_220d8ef7c36646a987e6b9e4569b1ee8]

Whole-tree literal search found main's guarded plot(results, args) call as the only direct call to this plotting function. [source; call_c8b7ba8e7481448795a348035c50e4ec, call_c9ea918e053a403c821f7cc6362348b5]

<a id="usage-evaluation"></a>

## Label-driven plot colors

get_color first searches for exact bracketed palette values: [green], [purple], [olive], [brown], [red], [blue] and [black]. Only afterward does it apply backend-name matching. Multiple recognized tags resolve by palette iteration order, not their position in the label. [source; call_7b6e78499dcf404cab1c63cbdb90448a, call_c9ea918e053a403c821f7cc6362348b5]

Adding the **** → black entry makes [black] available to the new palette scan. The literal **** remains a fallback substring rule after the existing backend rules; it is not a wildcard. [source; call_7b6e78499dcf404cab1c63cbdb90448a]

Displayed annotations now keep only text before the first opening bracket, trim whitespace and append perplexity rounded to three decimal places. Color selection still receives the complete original label. This hides every bracket suffix, including unsupported color tags or ordinary bracketed notes; printed result dictionaries retain the original label. [source; call_7b6e78499dcf404cab1c63cbdb90448a, call_c9ea918e053a403c821f7cc6362348b5]

The existing line builder groups all nonblack points by selected color and sorts their coordinates before drawing dotted lines. Consequently, explicit colors can separate or combine comparison groups independently of backend names; scoring and axis selection are unchanged. [source; call_c9ea918e053a403c821f7cc6362348b5, call_7b6e78499dcf404cab1c63cbdb90448a]

A standard-library transcription verified that EXL3 [red] selects red, EXL3 [black] disables line membership, EXL3 [orange] falls back to purple, and EXL3 [blue] [green] selects green. All four display EXL3 followed by the formatted score. [execution; call_19ed5c92b0784da1bcd3e46a5370afbd]

## Uncertainty and limits

No Matplotlib rendering or model evaluation was executed. The Python check transcribed string-selection logic only.
