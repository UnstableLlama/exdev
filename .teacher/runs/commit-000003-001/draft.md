# 942ecaf18bec9bd2eceb82126a26cf8c9e36ebb2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/942ecaf18bec9bd2eceb82126a26cf8c9e36ebb2) · [Evidence ledger](draft.json)

Adjusts README heading hierarchy, standardizes centered plot wrappers, shrinks the README preview and adds direct-image navigation for HumanEval.

- [Documentation hierarchy and linked plots](#documentation-presentation)

## Problem

The README used deeper heading levels and an 800-wide quantization preview; the evaluation page's HumanEval image lacked the direct image link already provided for other plots. [source; call_38b7f37473ea47dcaf00ead7ac15a548, call_683026a1a5484f149a32c6b113222761]

## Reasoning

The change adjusts documentation hierarchy and image presentation rather than quantization or evaluation logic. [source; call_38b7f37473ea47dcaf00ead7ac15a548, call_683026a1a5484f149a32c6b113222761]

## Impact

HumanEval gains a clickable link to its PNG, while the README retains its link from the preview to the detailed EXL3 documentation. [source; call_38b7f37473ea47dcaf00ead7ac15a548, call_683026a1a5484f149a32c6b113222761]

<a id="documentation-presentation"></a>

## Documentation hierarchy and linked plots

README major sections move from level-three to level-two headings; Installation, Conversion and Examples move from level four to level three, preserving their subordinate relationship to How to. [source; call_38b7f37473ea47dcaf00ead7ac15a548]

Both documents replace centered figure elements carrying class="image" with centered div elements. This retains the explicit alignment attribute but removes figure semantics and the image class hook; the resulting visual effect depends on renderer styling. [inference; call_38b7f37473ea47dcaf00ead7ac15a548, call_683026a1a5484f149a32c6b113222761]

The README preview's width attribute changes from 800 to 640. The detailed comparison plots retain width 400, and HumanEval retains width 800; these are image presentation dimensions, not benchmark parameters. [source; call_38b7f37473ea47dcaf00ead7ac15a548, call_683026a1a5484f149a32c6b113222761]

HumanEval's image is wrapped in an anchor pointing to humaneval.png with target="_blank", matching the existing direct-image navigation pattern of the paired bitrate and VRAM plots. The README preview instead continues to navigate to doc/exl3.md. [source; call_683026a1a5484f149a32c6b113222761, call_38b7f37473ea47dcaf00ead7ac15a548]

## Uncertainty and limits

No documentation renderer or browser was exercised; actual layout and target="_blank" handling remain renderer-dependent. Scalar computation would not meaningfully validate these markup changes.
