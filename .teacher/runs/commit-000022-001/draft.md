# e0f26ed129ca94cc9ea8b810849d3c68885ef51b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/e0f26ed129ca94cc9ea8b810849d3c68885ef51b) · [Evidence ledger](draft.json)

Adds consolidated module timing, remaining-time estimates, and progress-task reuse during conversion. The new time formatter can produce negative minute remainders.

- [Module timing and reusable quantization progress](#conversion)

## Problem

Conversion reported module bitrate and forward-pass error separately, without a module duration or remaining-time estimate. Scaling and quantization also used separate progress-bar contexts. [source; call_faf09829e469478d90836ace57e61c11, call_17fbaee6d5a947ab90170c4c7b4c9da9]

## Reasoning

The change consolidates module feedback and reuses the scaling progress task for quantization, adding visibility without changing the inspected quantization arithmetic. [source; call_faf09829e469478d90836ace57e61c11, call_17fbaee6d5a947ab90170c4c7b4c9da9, call_508fa6dad59a413ebc9f9375ba90f68d]

## Impact

The estimate extrapolates the latest module's duration to all remaining modules. It is inexpensive but does not account for differing module costs, subsequent unloading/checkpointing, or final compilation. [inference; call_faf09829e469478d90836ace57e61c11, call_3819f7485b4446558d8e8b1187184ad2]

## Source Notes

The new human_time import is exposed through util's existing wildcard import from misc. [source; call_dd378ccae68b46aca4f8f4f640363353, call_a272bae446fa4afebd0b3558de597456, call_faf09829e469478d90836ace57e61c11]

<a id="conversion"></a>

## Module timing and reusable quantization progress

Timing begins before loading each processed module and ends after advancing calibration state. The consolidated line reports module key, actual tensor-storage bits per weight, rfn, and elapsed seconds. The key width 47 and bitrate width 5 are minimum display widths, not truncation limits. [source; call_faf09829e469478d90836ace57e61c11, call_3819f7485b4446558d8e8b1187184ad2]

Actual module bpw remains tensor byte size multiplied by eight and divided by weights_numel(), whereas each linear's printed bpw is its assigned quantization K. The unchanged rfn calculation sums relative Frobenius errors for up to five reference states and divides by five; modules without quantized linears retain zero error. [source; call_3819f7485b4446558d8e8b1187184ad2, call_faf09829e469478d90836ace57e61c11]

For absolute module indices of at least one, the estimate is module_time × (module_count − index − 1), then formatted by human_time. This skips index zero, rather than requiring two newly processed modules after resumption. [source; call_faf09829e469478d90836ace57e61c11, call_3819f7485b4446558d8e8b1187184ad2]

quantize_exl3 now stays in the original ProgressBar context after scale selection. It explicitly sets completed work to zero, changes the description from Scaling to Quantizing, and changes the total from 100 to tiles_k, the input weight's first dimension divided by 16. new_task updates the existing task rather than allocating another task. [source; call_17fbaee6d5a947ab90170c4c7b4c9da9, call_7ff7c7094f49429690592a120d2aeac3, call_ca1020007d9c4733a843d55b131d873b, call_508fa6dad59a413ebc9f9375ba90f68d]

human_time first rounds seconds, then uses offsets of 30 before division by 60 to round minutes and hours. Rounding hours upward before subtracting their minutes can produce negative minute remainders. [source; call_a272bae446fa4afebd0b3558de597456]

## Authoring-time findings — pending review

### negative-remaining-minutes (suspected; defect)

The new duration formatter can display negative minutes for positive remaining-time estimates.

Trigger: Conversion reaches its estimate print with an estimated duration such as 1800 seconds.

Expected: A nonnegative duration representation, such as 30 minutes.

Actual: The transcribed formatter returns '1 hour, -30 minute': it rounds 30 minutes to one hour, then subtracts 60 minutes.

Locations: e0f26ed129ca94cc9ea8b810849d3c68885ef51b:exllamav3/util/misc.py — human_time, e0f26ed129ca94cc9ea8b810849d3c68885ef51b:exllamav3/conversion/convert_model.py — main

Source evidence: call_a272bae446fa4afebd0b3558de597456, call_faf09829e469478d90836ace57e61c11, call_3338161b2f1f4fd9814bad796b20c61c

source_inspection: Parent-tree search found no human_time occurrences. The task diff introduces the helper and its direct conversion-main caller, gated by idx >= 1; the observed reach is remaining-time display, not quantized tensors. [call_3338161b2f1f4fd9814bad796b20c61c, call_faf09829e469478d90836ace57e61c11, call_a272bae446fa4afebd0b3558de597456]. Limits: This identifies the introduced direct caller, not external consumers.

scalar_transcription: Standard-library Python reproduced negative minute output for 1770, 1800, and 5400 seconds, alongside boundary examples. [call_d377c3bf25de48e1ab08f38ecfd510f3]. Limits: The formatter was transcribed; conversion itself was not run.

## Uncertainty and limits

Conversion and Rich progress rendering were not executed; elapsed-time accuracy and library handling of new_task's progress keyword remain unestablished.

The scalar check executes a transcription of human_time, not the repository implementation or a GPU workflow.
