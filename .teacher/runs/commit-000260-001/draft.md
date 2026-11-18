# 463ebe1841ebe115ac46ccf91e1a40f68199c16a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/463ebe1841ebe115ac46ccf91e1a40f68199c16a) · [Evidence ledger](draft.json)

Adds an opt-in dark theme to compare_q plots, coordinating series, baseline, arrow and grid colors without changing evaluation.

- [Dark comparison plots](#usage-evaluation)

## Problem

The comparison plot previously used a fixed light-oriented palette; this change adds an opt-in dark presentation. [source; call_09edff22b1594ff6a2d1eb9475f285dd]

## Reasoning

Dark mode combines a Matplotlib background style with coordinated changes to series colors, baseline exclusion, annotation arrows and grid styling. [source; call_09edff22b1594ff6a2d1eb9475f285dd]

## Impact

The CLI adds -dark/--dark as a store_true flag. main calls plot only with --plot, so dark mode alone does not request a graph. Evaluation calculations and result serialization are unchanged. [source; call_09edff22b1594ff6a2d1eb9475f285dd, call_43befb449ff14d91bd14f416f6494342]

## Source Notes

The original usage-evaluation ancestor chapter was read. It establishes the comparison runner's separation between evaluation and optional plotting, and cautions that the plotted VRAM quantity represents calculated storage rather than measured peak allocation. [ancestor; call_6dfff23272dc4934abccf501ce13cf5c]

PR #26, “Superior 3INST parameters,” concerns decoder-parameter experiments and includes discussion of eval/compare_q.py graphs. Its relationship here is inferred only from that shared script and plotting workflow; it does not establish motivation for dark mode. [inference; call_ad57b34289ec4dfa8a28ed0ae93683e9, call_d3a28318b27846c98267df7562b27843, call_ac189d940afa4927907302d99476d619]

<a id="usage-evaluation"></a>

## Dark comparison plots

plot introduces col(light, dark), selecting by args.dark, and applies dark_background before figure setup. The whole-parent search found main as the only direct caller of this plot function; its CLI parser supplies the new attribute. [source; call_09edff22b1594ff6a2d1eb9475f285dd, call_77d297e2c4a844179c798a7865ee5697, call_43befb449ff14d91bd14f416f6494342]

The dark palette maps EXL2 to greenyellow, EXL3 to palevioletred, AWQ to tan, imat to darkorange, GGUF to tomato, VPTQ to cornflowerblue and QTIP to lightseagreen. Unknown labels and the **** category use silver instead of black. Scatter markers and text share these selected colors. [source; call_09edff22b1594ff6a2d1eb9475f285dd, call_43befb449ff14d91bd14f416f6494342]

Changing the baseline exclusion alongside the palette is necessary to preserve grouping: silver baseline points remain excluded from dotted connecting lines, just as black baseline points were previously. Other points remain grouped by resolved color, not by their full labels. [source; call_09edff22b1594ff6a2d1eb9475f285dd, call_43befb449ff14d91bd14f416f6494342]

Bracketed color overrides are matched against the active palette before category names. Consequently, EXL3 [green] resolves to green in light mode but palevioletred in dark mode; EXL3 [greenyellow] does the converse palette-specific override. A scalar transcription reproduced these cases and found seven distinct nonbaseline colors in each palette. [execution; call_74989f76218b4056940b1ef86616550d, call_09edff22b1594ff6a2d1eb9475f285dd]

Annotation arrows change from lightgray to dimgray. Dark grids request dimgray dashed lines with linewidth 0.5, a presentation width rather than a numerical evaluation threshold; light mode retains grid(True). Axis selection, filtering, labels and annotation-placement parameters remain unchanged. [source; call_09edff22b1594ff6a2d1eb9475f285dd, call_43befb449ff14d91bd14f416f6494342]

## Uncertainty and limits

No Matplotlib rendering, model evaluation or repository test was executed. The Python check transcribed palette selection only.

Dark mode applies a global pyplot style without a corresponding light-style reset. Repeated mixed-theme calls and interaction with user Matplotlib settings were not executed.
