# b3bd8f614b003d81d8f5f6b56b20a207d901c523


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b3bd8f614b003d81d8f5f6b56b20a207d901c523) · [Evidence ledger](draft.json)

Adds input-width rounding and input-only weight padding, but simultaneous two-axis padding remains incompatible and padding-before-slicing is unchanged.

- [Extend linear weight padding to input channels](#modules)

## Problem

Linear previously rounded only output width. Input widths remained unpadded, and pad_out returned immediately when output padding was unnecessary. [source; call_1bb33e4332a64818abe291d434d85689]

## Reasoning

The change retains the original input width separately and rounds the operational width to pad_to, defaulting to 128. It extends weight padding to input-only cases without changing the forward method. [source; call_f1df2971d15f478fab23f8a5d8910d55, call_1bb33e4332a64818abe291d434d85689]

## Impact

The padded input width propagates to FP16 and EXL3 layer construction, Hessian allocation and weights_numel. Forward still delegates without explicitly padding activations, so compatible activation widths remain a caller-side requirement. [source; call_f1df2971d15f478fab23f8a5d8910d55, call_1bb33e4332a64818abe291d434d85689, call_ca69d16cd32e4c5b8b94e01001bf190f]

## Source Notes

Issue #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” reports vocabulary/output-padding failures and successful fixes before this task. Its relationship here is contextual inference based on the shared Linear conversion path and padding concern, not evidence that this input-padding change fixed that report. [inference; call_862d7ff9853c469d909843c32f1ee4c0, call_f1df2971d15f478fab23f8a5d8910d55]

Issue #7 reports an undefined-symbol import failure and an environment workaround; issue #15 reports incoherent Cogito output at bpw <= 2.5 and discusses regularization. Neither discussion establishes an input-padding cause. [source; call_5026f93b9a094672adbf3acaf1c041b7, call_2a417809bdcb4d93974e00088730d8f5]

The earlier slicing entry records padding-before-slicing and default CPU-staging concerns. [ancestor; call_36fa395f638c4beaa747e3a194659ae0]

<a id="modules"></a>

## Extend linear weight padding to input channels

For input-only padding, pad_out allocates an output-by-padded-input zero tensor and copies the original columns into its prefix. Existing output-only padding copies rows; one-dimensional biases retain output-width padding. Both ordinary and fused FP16 loading call this helper before constructing LinearFP16. [source; call_f1df2971d15f478fab23f8a5d8910d55, call_1bb33e4332a64818abe291d434d85689, call_a668fc70fe9b4392bc5428c2c949cb8b]

The rounding expression computes the smallest pad_to multiple not below the requested width. A standard-library transcription checked the default-128 invariant for widths 1–1024 and matching copy shapes for input-only and output-only examples. [execution; call_2d087df8304f4296af71a97b0d257d1e]

Zero-filled added weight columns preserve the original contribution when inputs already have the corresponding expanded width. The tradeoff is a larger stored matrix; this helper does not itself expand activation tensors. [inference; call_f1df2971d15f478fab23f8a5d8910d55, call_ca69d16cd32e4c5b8b94e01001bf190f]

Inspection of the parent plus task diff shows that padding still precedes feature slicing, preserving the earlier slicing incompatibility. The default is_sliced comparison against optional None dimensions also remains unchanged. [source; call_1bb33e4332a64818abe291d434d85689, call_f1df2971d15f478fab23f8a5d8910d55, call_ca69d16cd32e4c5b8b94e01001bf190f]

## Authoring-time findings — pending review

### simultaneous-axis-padding (suspected; defect)

The output-padding branch prevents simultaneous input padding from copying into a correctly bounded destination.

Trigger: Load an ordinary 130-by-130 weight with default pad_to=128.

Expected: Copy into the leading 130-by-130 region of a zero-filled 256-by-256 matrix.

Actual: The output-width condition selects padded[:130, :], a 130-by-256 destination, for the 130-by-130 source; the input-column branch is skipped.

Locations: b3bd8f614b003d81d8f5f6b56b20a207d901c523:exllamav3/modules/linear.py — Linear.pad_out

Source evidence: call_f1df2971d15f478fab23f8a5d8910d55, call_a668fc70fe9b4392bc5428c2c949cb8b

source_inspection: Whole-parent literal searches locate pad_out calls only in ordinary and fused load_fp16 branches; Linear.load directly invokes load_fp16 after EXL3 lookup. The finding concerns weights needing both axes padded, not all model loads. [call_a668fc70fe9b4392bc5428c2c949cb8b, call_0d402bd48e0a4f76855d518d88ec01fb, call_1bb33e4332a64818abe291d434d85689]. Limits: No model exhibiting these dimensions was executed.

scalar_transcription: Computed the incompatible source and destination slice shapes. [call_2d087df8304f4296af71a97b0d257d1e]. Limits: Does not execute tensor assignment or establish its exact exception.

### inherited-padding-before-slicing (suspected; defect)

The inherited full-weight padding-before-slicing incompatibility persists, with input padding now changing the destination width too.

Trigger: Load a full 512-by-64 weight while requesting 130 outputs and 64 inputs, full_out_features=512 and first_out_feature=0.

Expected: Select the requested feature region before padding the local matrix.

Actual: pad_out allocates 256-by-128 and attempts to copy the full 512-by-64 source before LinearFP16 can slice it.

Locations: b3bd8f614b003d81d8f5f6b56b20a207d901c523:exllamav3/modules/linear.py — Linear.load_fp16

Source evidence: call_1bb33e4332a64818abe291d434d85689, call_f1df2971d15f478fab23f8a5d8910d55, call_ca69d16cd32e4c5b8b94e01001bf190f

source_inspection: The ordinary FP16 loader still pads before constructing the slicing backend. Whole-parent search identifies Linear.load as its direct caller. [call_0d402bd48e0a4f76855d518d88ec01fb, call_1bb33e4332a64818abe291d434d85689]. Limits: Reach is conditional on an explicit sliced request; no existing model construction with this request was demonstrated.

scalar_transcription: Checked the full source and padded destination slice dimensions. [call_2d087df8304f4296af71a97b0d257d1e]. Limits: Shape arithmetic, not repository execution.

## Uncertainty and limits

No PyTorch assignment, model loading, quantization or CUDA kernel was executed; the executed check models integer dimensions and slice shapes only.

End-to-end activation-width compatibility, memory cost and performance were not measured.

The inspected source establishes 128 as the existing padding default, not a universally sufficient alignment for every backend.
