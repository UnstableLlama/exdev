# de83084184c34cae0aaeca5c8b024de7f148830d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/de83084184c34cae0aaeca5c8b024de7f148830d) · [Evidence ledger](draft.json)

Makes Linear input padding opt-in and enables it for GatedMLP down projections, retaining existing output padding and conditional loading incompatibilities.

- [Restrict input padding to opted-in gated MLP down projections](#modules)

## Problem

Linear automatically rounded input widths to pad_to without requiring callers to opt in. Its forward method did not correspondingly pad activations. [source; call_afc10242ccfc4443b53b3272582add27]

## Reasoning

The change adds allow_input_padding=False and asserts that input rounding leaves the width unchanged unless explicitly permitted. GatedMLP down projections opt in; the padding implementation itself is unchanged. [source; call_cd150961e05b4b58bd10fdc710149d30, call_f0abcd98e16f401ab14e2659eef707ce]

This is a conservative restriction rather than general activation-padding support: the gated MLP already produces rounded intermediate widths through its gate/up projections, whereas arbitrary Linear callers need not supply expanded inputs. [inference; call_3a1290973f0b4518bd56e14d3560a7f0, call_afc10242ccfc4443b53b3272582add27, call_f3d49f1aed7e473fb74ced10eb87ea19]

## Impact

With assertions active, non-opted-in layers reject nonaligned inputs during construction, before FP16 or EXL3 loading. Output padding remains allowed. The ordinary MLP.down constructor does not receive the exception; the implementation is narrower than allowing every MLP down projection. [source; call_cd150961e05b4b58bd10fdc710149d30, call_f0abcd98e16f401ab14e2659eef707ce, call_3a1290973f0b4518bd56e14d3560a7f0, call_afc10242ccfc4443b53b3272582add27]

## Source Notes

PR #20, “Reka Flash 3 vs padding,” reports incompatible dimensions during Reka quantization. Its connection to this task is inferred from the matching input-padding mechanism and turboderp's discussion of permitting MLP down padding while treating attention cautiously; it is not an explicit task link. [inference; call_14d2cfce02534c7dbcf808e1dc118ef9, call_cd150961e05b4b58bd10fdc710149d30, call_f0abcd98e16f401ab14e2659eef707ce]

Issue #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” concerns vocabulary/output padding and reports earlier successful fixes. Its contextual connection is inferred from the shared Linear conversion path, not evidence that this restriction fixes that issue. [inference; call_3765286bfbf343919f708426d10813a5, call_afc10242ccfc4443b53b3272582add27]

The other inspected failure discussions concern an undefined __cxa_call_terminate symbol (#7), incoherent Cogito output at bpw <= 2.5 (#15), and missing torch during requirements installation (#17). Their own accounts discuss environment setup or quantization regularization, not this input-padding guard. [source; call_dd3314f857b748e2ad33efe2ffbee941, call_e3a7fec80e3447ce8a9709b6bde7a3e3, call_5c4174daa54a4ef587a7e9e2107488af]

The earlier input-padding annotation records simultaneous-axis and padding-before-slicing incompatibilities. [ancestor; call_753001a2d2da41f0a85109e7a477926a]

<a id="modules"></a>

## Restrict input padding to opted-in gated MLP down projections

The guard compares original and rounded input widths, rather than checking a layer name. Any caller can explicitly opt in; the task adds that opt-in only to GatedMLP's down constructor inside its slice loop. [source; call_cd150961e05b4b58bd10fdc710149d30, call_f0abcd98e16f401ab14e2659eef707ce, call_3a1290973f0b4518bd56e14d3560a7f0]

GatedMLP passes each intermediate slice width to gate/up outputs and down inputs. Forward computes gate and up activations, applies the selected activation/multiplication, then passes the resulting intermediate tensor to down. Input-only weight padding adds zero columns; it does not expand that tensor. [source; call_3a1290973f0b4518bd56e14d3560a7f0, call_afc10242ccfc4443b53b3272582add27]

A standard-library transcription verified rounding for widths 1–1024: the result is the smallest multiple of 128 not below the input. Width 130 becomes 256 and fails the default guard, while aligned widths 128 and 256 pass. [execution; call_871d1998b9024fd7b61da26ee4e117a9]

Zero-column padding can preserve the original linear contribution when compatible expanded activations already exist, at the cost of larger matrices. The guard avoids silently assuming that compatibility for all callers; it does not repair the inherited loading-order or simultaneous-axis problems. [inference; call_afc10242ccfc4443b53b3272582add27, call_cd150961e05b4b58bd10fdc710149d30, call_f3d49f1aed7e473fb74ced10eb87ea19]

## Authoring-time findings — pending review

### retained-two-axis-padding (suspected; defect)

The inherited simultaneous-axis copy mismatch remains for explicitly opted-in Linear callers; the new default guard blocks it earlier for other callers.

Trigger: Load a 130-by-130 FP16 weight with pad_to=128 and allow_input_padding=True.

Expected: Either reject simultaneous-axis padding explicitly or copy the weight into the leading 130-by-130 region.

Actual: pad_out selects the output-padding branch and assigns the 130-by-130 source to a 130-by-256 destination.

Locations: de83084184c34cae0aaeca5c8b024de7f148830d:exllamav3/modules/linear.py — Linear.pad_out

Source evidence: call_afc10242ccfc4443b53b3272582add27, call_cd150961e05b4b58bd10fdc710149d30, call_a1891e4fcc0a4ac7a7fd1042f97ad1da, call_fe948152bb954066a4ad7950327a5721

source_inspection: Whole-parent searches locate pad_out calls in ordinary and fused load_fp16 paths, reached directly from Linear.load. The diff preserves those paths. Reach requires an opted-in two-axis case; normal GatedMLP construction also guards the hidden-size inputs of gate/up. [call_a1891e4fcc0a4ac7a7fd1042f97ad1da, call_fe948152bb954066a4ad7950327a5721, call_3a1290973f0b4518bd56e14d3560a7f0]. Limits: No affected model construction or tensor assignment was executed.

scalar_transcription: Calculated source and destination slice shapes. [call_871d1998b9024fd7b61da26ee4e117a9]. Limits: Integer shape arithmetic, not PyTorch execution.

### retained-padding-before-slicing (suspected; defect)

Padding still precedes feature slicing, so the input guard does not remove the inherited full-weight/local-destination mismatch.

Trigger: Request 130 outputs from a full 512-by-128 FP16 weight, with 128 inputs and first_out_feature=0.

Expected: Select the local feature region before padding it.

Actual: The aligned input passes the new guard, but load_fp16 calls pad_out on the full weight, attempting a 512-by-128 copy into a 256-by-128 destination before LinearFP16 can slice.

Locations: de83084184c34cae0aaeca5c8b024de7f148830d:exllamav3/modules/linear.py — Linear.load_fp16

Source evidence: call_afc10242ccfc4443b53b3272582add27, call_f3d49f1aed7e473fb74ced10eb87ea19, call_cd150961e05b4b58bd10fdc710149d30

source_inspection: Linear.load is the direct load_fp16 caller found by whole-parent search. Ordinary loading pads before constructing the slicing backend; neither task hunk changes that ordering. [call_fe948152bb954066a4ad7950327a5721, call_afc10242ccfc4443b53b3272582add27, call_f3d49f1aed7e473fb74ced10eb87ea19]. Limits: Conditional on a sliced request needing padding; no specific model workflow was demonstrated.

scalar_transcription: Computed the full source and bounded destination dimensions for the aligned-input example. [call_871d1998b9024fd7b61da26ee4e117a9]. Limits: Does not execute repository loading or establish an exact runtime exception.

## Uncertainty and limits

No model loading, tensor assignment, quantization or GPU kernel was executed. The Python check models integer dimensions only.

The inspected code establishes 128 as the default alignment, not a universally sufficient backend requirement.

End-to-end model compatibility and performance were not measured.
