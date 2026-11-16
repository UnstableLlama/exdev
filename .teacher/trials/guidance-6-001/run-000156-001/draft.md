# cb7c70cde0ec5137c70d12afeffacd40d5db4770


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/cb7c70cde0ec5137c70d12afeffacd40d5db4770) · [Evidence ledger](draft.json)

Adds bracketed color overrides to comparison labels and hides bracketed suffixes in plot annotations, also allowing explicit control of color-based connecting lines.

- [Label-controlled comparison plotting](#usage-evaluation)

## Problem

The comparison plot previously chose colors only from format-name substrings, preventing labels from explicitly overriding that choice. [source; call_9619689be329407b9ef0a687b065ce0b, call_845dca9656064c9587c602b2adb82dc3]

## Reasoning

Bracketed color tags provide presentation controls within existing labels, without introducing another result field or command-line option. [inference; call_9619689be329407b9ef0a687b065ce0b]

## Impact

The change affects plot colors, annotations and color-based connecting lines; it leaves perplexity calculation and printed result labels unchanged. [source; call_9619689be329407b9ef0a687b065ce0b, call_845dca9656064c9587c602b2adb82dc3]

## Source Notes

The root usage-evaluation entry describes the specification-driven comparison runner and optional plot. The later evaluator-memory entry describes scoring-buffer cleanup. Neither records a defect in the plotting code changed here. [ancestor; call_fef0ffac3d0243ea89a9ba7cfc36f9f0, call_1558768a6a684421bb9964748bf774e2]

<a id="usage-evaluation"></a>

## Label-controlled comparison plotting

plot.get_color now searches for exact bracketed color names before applying its existing format-substring fallback. Supported tags are [green], [purple], [olive], [brown], [red], [blue] and [black]. Multiple recognized tags resolve by palette order, not their position in the label. [source; call_9619689be329407b9ef0a687b065ce0b, call_845dca9656064c9587c602b2adb82dc3]

Adding the mapping from **** to black also makes [black] available to the new first pass. This enables an EXL3-labelled point to override purple and avoid connecting lines: the existing plot groups only nonblack points by color, sorts their coordinates and draws dotted lines. Explicit colors therefore control grouping as well as appearance. [source; call_9619689be329407b9ef0a687b065ce0b, call_845dca9656064c9587c602b2adb82dc3]

Annotations now keep only the text before the first opening bracket, strip surrounding whitespace, and append perplexity formatted to three decimal places. Color selection still receives the original label. This hides color metadata, but also hides any ordinary bracketed description and everything following it, even for an unsupported color. [source; call_9619689be329407b9ef0a687b065ce0b]

The parent-tree search found main as the sole direct caller of plot(results, args), gated by args.plot. main obtains results through test_ppl and prints them before plotting; the patch changes no stored result fields. [source; call_58d14e2b5086483989e994ee1a06ae13, call_845dca9656064c9587c602b2adb82dc3, call_9619689be329407b9ef0a687b065ce0b]

A scalar transcription verified that EXL3 [black] selects black, EXL3 [blue] [green] selects green, and EXL3 [cyan] falls back to purple while still losing its bracketed suffix. Formatting 4.12356 produced 4.124. These checks exercise string rules, not the repository plot implementation. [execution; call_1286be9a61cb446789a0c9ead4033c01]

## Uncertainty and limits

Only a standard-library transcription of color selection and label formatting was executed; Matplotlib rendering, annotation placement and model evaluation were not tested.
