# 322815f71eaf582e36fd81bc6fdf5148b27fb97a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/322815f71eaf582e36fd81bc6fdf5148b27fb97a) · [Evidence ledger](draft.json)

Adds calibration-guided output-channel scaling with forced overrides, factors preprocessing into regularize, and makes scale-search exit synchronization reachable. A test caller lacks the new required policy key, and premature progress reporting persists.

- [Calibration-guided output scaling and regularization](#quantizer)

## Problem

Quantization previously always normalized output channels. This change makes that normalization conditional on calibration-input skew and adds explicit overrides. [source; call_b01b95df90b0486985bd936b15e1b798]

## Reasoning

The source describes the cutoff as experimental: concentrate at least 15% of the summed channel RMS in the largest approximately 2% of channels, and automatic mode disables output-channel scaling. This is a heuristic, not a demonstrated optimum. [source; call_b01b95df90b0486985bd936b15e1b798]

## Impact

The converter forwards the requested policy per linear layer, prints the actual decision and global scale, and writes head_bits plus the requested always/never/auto policy into quantization metadata. The metadata policy is not a per-layer decision inventory. [source; call_9c703a488e1342e18249f24b9585a1ed, call_2717a11d2e054c4bb854f55836fd35a5, call_b01b95df90b0486985bd936b15e1b798]

## Source Notes

The earlier tile-sampling entry records unreachable exit synchronization and premature progress completion. [ancestor; call_30c8a665943747c3bd05d01cdf176bbb]

Inspection of the parent and task diff shows that exit synchronization is now reachable before the tuple return; the premature-progress expression remains unchanged. [source; call_650018a236e64899a7322064a66ff61b, call_b01b95df90b0486985bd936b15e1b798]

The inspected reports concern undefined __cxa_call_terminate (#7), incoherent cogito output at bpw <= 2.5 (#15), CUDA invalid configuration (#16), and missing torch during installation (#17). None establishes a resolution by this change. [source; call_ed57d0f32f4344859dadd655b588a3f9, call_e94bf85ecabb4ecc945301e5c3cdbf54, call_e87a07866d2c4a4baebf3a99ea1a26ae, call_8280e26303094365b5ac4c99b6f66aeb]

Issue #16 is related context because its traceback matches Linear.capture_H's addmm_ accumulation and the converter's calibration forward pass. That connection does not establish that changing subsequent regularization addresses its reported CUDA failure. [inference; call_e87a07866d2c4a4baebf3a99ea1a26ae, call_1a2f9512c934488ebd3080f4fc250143, call_2f4fbceac49a44c2a1730702562a566e]

<a id="quantizer"></a>

## Calibration-guided output scaling and regularization

Linear.capture_H accumulates XᵀX and a row count. finalize_capture_H divides by that count and adds sigma_reg times the mean diagonal, default 0.025. It now saves a clone of this regularized diagonal before sign flips and Hadamard transforms, returning it also when the captured Hessian is reused. Thus the decision uses damped input second moments, not raw weight statistics. [source; call_1a2f9512c934488ebd3080f4fc250143, call_650018a236e64899a7322064a66ff61b, call_b01b95df90b0486985bd936b15e1b798]

regularize sorts sqrt(H_diag) descending and divides the sum of its first floor(k/50) entries by the total. Automatic mode applies output scales only when this ratio is strictly below 0.15; equality disables them. Explicit True or False overrides the decision, although the statistic is still calculated. [source; call_b01b95df90b0486985bd936b15e1b798]

A scalar transcription including default diagonal damping produced skew 0.02 for 100 equal second moments, enabling scales, and approximately 0.164545 for two second moments of 100 and 98 of 1, disabling scales. [execution; call_74b1af66ec8f4defb8cb571014c9ddf1]

When enabled, output-channel RMS values are normalized by their mean and folded into sv. When disabled, sv retains random signs. Both paths divide weights by sv, apply the right Hadamard transform, derive input RMS scales in su using -codebook_scale, divide by su, and apply the left transform. Disabling output normalization therefore does not disable sign mixing, input scaling, or Hadamard preprocessing. [source; call_b01b95df90b0486985bd936b15e1b798, call_650018a236e64899a7322064a66ff61b]

The refactor selects blockwise in-place Hadamard helpers instead of whole-matrix helpers. Their implementations require float tensors and dimensions divisible by the transform size, here 128, and use normalization 1/sqrt(128). Processing one block at a time avoids a whole transformed-matrix result allocation, but no memory or speed improvement was measured. [source; call_650018a236e64899a7322064a66ff61b, call_b01b95df90b0486985bd936b15e1b798]

Global-scale search still trial-quantizes wrapped-diagonal 16×16 samples, with width 3, over [0.1, 1.9] until interval width is at most 0.01. It now returns both the midpoint scale and the average of the two retained trial errors, after synchronizing selected devices. The reported sample MSE is therefore not a fresh evaluation at the returned midpoint. regularize multiplies weights by this scale and divides su by it to preserve reconstruction scaling. [source; call_650018a236e64899a7322064a66ff61b, call_b01b95df90b0486985bd936b15e1b798]

Packed output remains suh, svh and trellis, with half-precision scale vectors. Reconstruction still reverses the transforms and applies su and sv; the decision changes their values rather than introducing a new tensor format. [source; call_650018a236e64899a7322064a66ff61b, call_b01b95df90b0486985bd936b15e1b798, call_1a2f9512c934488ebd3080f4fc250143]

The documented output-scale switches are mutually exclusive and default to None, matching automatic mode. prepare treats the policy as momentary: resuming without a switch resets it to auto rather than retaining a saved forced policy. --override_anyway permits changes to otherwise protected bitrate and calibration settings; it bypasses the guard, not the consequences of incompatible checkpoints. [source; call_8642c4502931496189ae6bb76a751bf9, call_9c703a488e1342e18249f24b9585a1ed, call_2f4fbceac49a44c2a1730702562a566e]

Whole-parent searches found the converter and test_quant_dequant as callers of Linear.convert_exl3, which forwards quant_args unchanged to quantize_exl3. The converter builder gains apply_out_scales, but the test builder does not. The located internal callers of finalize_capture_H and block_ldl are updated for their required verbose arguments. [source; call_791ef75c44af434db986e253e81e3c76, call_9bda9bd0b4c94a8ebb963145da99c7c2, call_b8a6577f581f4bcd87dea3a5f8762b18, call_8732fc7e98214bfcab03202d87647692, call_8bcfd0283b3e47619f5739611574019a, call_61ba61d8e5d34eb5a9dfbfa0de5c361e, call_1a2f9512c934488ebd3080f4fc250143, call_b01b95df90b0486985bd936b15e1b798, call_9c703a488e1342e18249f24b9585a1ed]

## Authoring-time findings — pending review

### required-scale-policy-test-caller (suspected; new_requirement)

regularize requires a policy key that the existing quantization test does not supply.

Trigger: test_quant_dequant reaches regularize with its unchanged K/seed-only quant_args dictionary.

Expected: The repository caller supplies the new policy or omission defaults to automatic mode.

Actual: quant_args['apply_out_scales'] raises KeyError. The test also already lacks devices, required later by the parent implementation; this is an additional incompatibility, not evidence that the test previously passed.

Locations: 322815f71eaf582e36fd81bc6fdf5148b27fb97a:exllamav3/modules/quant/exl3_lib/quantize.py — regularize, bcc096667169d8f34c602ce495b372e3fc9afd2b:tests/test_quant_fn.py — test_quant_dequant

Source evidence: call_b01b95df90b0486985bd936b15e1b798, call_61ba61d8e5d34eb5a9dfbfa0de5c361e, call_650018a236e64899a7322064a66ff61b

source_inspection: Whole-tree caller and quant_args searches identified the converter and test builders; Linear.convert_exl3 forwards the dictionary unchanged. The converter is updated, the test is not. [call_791ef75c44af434db986e253e81e3c76, call_9bda9bd0b4c94a8ebb963145da99c7c2, call_b8a6577f581f4bcd87dea3a5f8762b18, call_1a2f9512c934488ebd3080f4fc250143, call_9c703a488e1342e18249f24b9585a1ed]. Limits: Conditional on reaching regularize; the CUDA/model-dependent test was not run.

### inherited-premature-search-progress (suspected; defect)

Scale-search progress still reports completion at its first interval contraction.

Trigger: g_scale_gss runs with the visible progress bar supplied through quantize_exl3 and regularize.

Expected: Intermediate updates distinguish search work from completion.

Actual: int(delta2/delta1) becomes zero after contraction, making every loop update 100 while search continues.

Locations: 322815f71eaf582e36fd81bc6fdf5148b27fb97a:exllamav3/modules/quant/exl3_lib/quantize.py — g_scale_gss

Source evidence: call_650018a236e64899a7322064a66ff61b, call_b01b95df90b0486985bd936b15e1b798, call_41005f991d5f4effbcc7eff9ec6c7063

source_inspection: The parent direct caller is quantize_exl3; the task moves that call into regularize while forwarding its progress bar. ProgressBar.update interprets the supplied value as completed work. [call_68f0767188a5450d9467650b7e336a44, call_b01b95df90b0486985bd936b15e1b798, call_41005f991d5f4effbcc7eff9ec6c7063]. Limits: No terminal rendering was executed.

scalar_transcription: Modeled golden-section interval contraction: all 11 updates were 100, ending at width approximately 0.009045. [call_74b1af66ec8f4defb8cb571014c9ddf1]. Limits: Python arithmetic models progress only; it does not execute the repository search or CUDA objective.

## Uncertainty and limits

No Torch, CUDA kernel, conversion, model-quality benchmark, or terminal rendering was executed. Scalar checks use Python arithmetic rather than GPU float32 operations.

The inspected source does not derive the retained codebook_scale value 1.24371088 or establish the empirical quality of the 0.15 cutoff.

Literal whole-tree caller searches cover repository call sites, not dynamic or external callers.
