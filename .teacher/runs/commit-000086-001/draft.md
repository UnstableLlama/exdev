# 0a4b2b210323489b3b830668fb86e22599bf54fb


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/0a4b2b210323489b3b830668fb86e22599bf54fb) · [Evidence ledger](draft.json)

Integrates input-only linear padding and an optional Reka HumanEval prompt, retaining the one-axis restriction and padding-before-slicing incompatibility.

- [Integrate input padding and Reka evaluation prompting](#integration)

## Problem

Relative to the first parent, Linear rounds only output widths and HumanEval has no reka prompt format. The merge incorporates input-width padding and that optional template. [source; call_8748291cbab541d2922b477ae6ade06d, call_4c6686508f56483abb89ce97d580233b]

## Reasoning

Input padding retains the original width and rounds the operational width to a pad_to multiple, default 128. For input-only padding, pad_out copies the original columns into a larger zero-filled matrix; output-only padding retains its row-copy branch. [source; call_8748291cbab541d2922b477ae6ade06d, call_78e47c24e4584e6798b102bb83ba4359]

PR #20, “Reka Flash 3 vs padding,” plausibly explains these paired changes: it reports Reka quantization dimension mismatches and compares raw/reka HumanEval prompts. This relationship is inferred from those concrete matches, not an explicit PR reference in the merge message. [inference; call_17574189b5ce4d5d907ec2448d83d688, call_8748291cbab541d2922b477ae6ade06d, call_4c6686508f56483abb89ce97d580233b]

## Impact

The padded input width reaches FP16/EXL3 construction, Hessian allocation and weight counts. Neither Linear.forward nor LinearFP16.forward explicitly pads activations, so expanding weights alone does not establish end-to-end shape compatibility. [source; call_78e47c24e4584e6798b102bb83ba4359, call_76025b02820a4442866780a60d4a78d1, call_8748291cbab541d2922b477ae6ade06d]

## Source Notes

In PR #20, gakada reports the quantization problem and the simultaneous-padding failure. After discussing a two-axis copy alternative, gakada suggests retaining the restriction pending a model needing it, and turboderp agrees. These are participant reports, not independent execution here. [source; call_17574189b5ce4d5d907ec2448d83d688]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns an extension import/environment failure. Issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” discusses regularization. Neither report establishes a padding cause. [source; call_9de431bbe87743b487faca4fca333f99, call_8825209a64e94ef8aaf35b6d6d7a5403]

The earlier input-padding entry records simultaneous-axis and padding-before-slicing incompatibilities. Inspection of the merge diff and unchanged loading/backend sequence shows both remain present. [source; call_12c3c7b986eb4bb99bc18b98c4dce3eb, call_8748291cbab541d2922b477ae6ade06d, call_78e47c24e4584e6798b102bb83ba4359, call_76025b02820a4442866780a60d4a78d1]

<a id="integration"></a>

## Integrate input padding and Reka evaluation prompting

Ordinary and fused FP16 loading call pad_out for weights and biases. Added zero columns can accommodate an already expanded activation width without adding contributions, at the cost of larger matrices; this is not automatic activation padding. [inference; call_78e47c24e4584e6798b102bb83ba4359, call_8748291cbab541d2922b477ae6ade06d, call_76025b02820a4442866780a60d4a78d1]

A standard-library transcription verified round-up-to-128 invariants for widths 1–1024. It also computed the incompatible 130×130 source versus 130×256 destination slice when both dimensions require padding. [execution; call_68bd2ffbc69141be895743eeec7607a1]

The optional -pf reka template requests concise reasoning in comments, places the problem in the human turn and repeats it after an assistant Python-code prefill. The existing selector substitutes both occurrences and retains the four-space completion prefix. Default prompting, sampling and completion extraction are unchanged. [source; call_4c6686508f56483abb89ce97d580233b, call_632bd37218a7402697db6fea04f03cf9]

## Authoring-time findings — pending review

### simultaneous-padding-restriction (suspected; new_requirement)

The integrated helper supports one-axis padding, not general simultaneous padding; the discussion explicitly accepts retaining this restriction.

Trigger: Load a 130×130 FP16 weight with pad_to=128.

Expected: General two-axis support would copy into the leading 130×130 region of a 256×256 matrix.

Actual: The output-padding branch instead selects a 130×256 destination for the 130×130 source, skipping the input-padding branch.

Locations: 0a4b2b210323489b3b830668fb86e22599bf54fb:exllamav3/modules/linear.py — Linear.pad_out

Source evidence: call_8748291cbab541d2922b477ae6ade06d, call_17574189b5ce4d5d907ec2448d83d688

source_inspection: Whole-parent searches locate calls in ordinary and fused load_fp16 branches; Linear.load invokes load_fp16 after EXL3 lookup. Reach is conditional on both dimensions needing padding. [call_ca1ab9b26e23429e9f94b5045c96c005, call_afbe37e3d73a467b9f92500251c82baa, call_78e47c24e4584e6798b102bb83ba4359]. Limits: No affected model load was executed.

scalar_transcription: Computed source and destination slice shapes. [call_68bd2ffbc69141be895743eeec7607a1]. Limits: Does not execute tensor assignment or establish its exact exception.

### padding-before-slicing (suspected; defect)

The inherited ordinary-loader ordering pads a full weight before the backend can select a requested feature slice.

Trigger: Request 130 outputs and 64 inputs from a full 512×64 weight, with full_out_features=512 and first_out_feature=0.

Expected: Select the requested feature region before padding the local matrix.

Actual: pad_out attempts to copy the full 512×64 source into a 256×128 destination before LinearFP16 performs slicing.

Locations: 0a4b2b210323489b3b830668fb86e22599bf54fb:exllamav3/modules/linear.py — Linear.load_fp16

Source evidence: call_78e47c24e4584e6798b102bb83ba4359, call_8748291cbab541d2922b477ae6ade06d, call_76025b02820a4442866780a60d4a78d1

source_inspection: Inspected loading order and backend slicing. Whole-parent search finds Linear.load as the direct load_fp16 caller. [call_afbe37e3d73a467b9f92500251c82baa, call_78e47c24e4584e6798b102bb83ba4359, call_76025b02820a4442866780a60d4a78d1]. Limits: Conditional on an explicit sliced request; no existing model construction with this request was demonstrated.

scalar_transcription: Computed the full source and padded destination slice dimensions. [call_68bd2ffbc69141be895743eeec7607a1]. Limits: Shape arithmetic only, not repository execution.

## Uncertainty and limits

No model loading, quantization, HumanEval, PyTorch assignment or CUDA execution was performed. The computation checks integer rounding and modeled slice dimensions only.

The inspected source establishes 128 as the existing default alignment, not universal sufficiency for every backend. Model-wide activation compatibility and performance remain unmeasured.
