# bad500d7272a863b3d1b0cd5a3ed1f714370c972


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/bad500d7272a863b3d1b0cd5a3ed1f714370c972) · [Evidence ledger](draft.json)

Corrects global-scale tile sampling to use distinct wrapped offsets, guards optional progress updates, and reduces verbose output. Premature progress completion persists, and newly appended synchronization is unreachable.

- [Correct wrapped-diagonal scale-search sampling](#quantizer)

## Problem

Global-scale estimation repeated the same tile for every inner-loop iteration: its column index used the fixed sampling width instead of the loop variable. [source; call_dc6154f354074db98ec1157bc1055a1f, call_554dd2365646442ab6c3fe52d0c4ff3c]

## Reasoning

Using w selects neighboring wrapped diagonals rather than duplicating one diagonal, increasing sample diversity without increasing the number of sampled tiles. [source; call_dc6154f354074db98ec1157bc1055a1f, call_554dd2365646442ab6c3fe52d0c4ff3c]

## Impact

The changed sample can change the selected global scale and subsequent quantization. Improved model quality or conversion speed is not established. [inference; call_554dd2365646442ab6c3fe52d0c4ff3c, call_dc6154f354074db98ec1157bc1055a1f]

## Source Notes

The earlier multi-GPU entry records premature scale-search progress completion. Inspection of this patch shows that its arithmetic persists despite the new optional-progress guard. [ancestor; call_e9aa4fc96fe948c1bd352da182ddafb6]

The inspected discussions report an undefined __cxa_call_terminate symbol (#7), incoherent cogito output at bpw <= 2.5 (#15), a CUDA invalid-configuration error (#16), and missing torch during installation (#17). They do not establish that this sampling patch resolves those reports. [source; call_15e488bac11e4a368d8f21cf427bd77f, call_49594b14aa164adfb4dc0640f7a174a2, call_b14ed47303cb44c7bf4ca5e6ec6bf6a9, call_7775c71260f7478b80041f3e0c897119]

<a id="quantizer"></a>

## Correct wrapped-diagonal scale-search sampling

g_scale_gss samples 16-by-16 tiles, flattens each to 256 elements, applies tensor_core_perm, and stacks them for trial quantization. With default width 3, the corrected column index ((i + w) % tiles_n) spans three wrapped offsets per i; the old index repeated ((i + 3) % tiles_n) three times. Modulo wrapping can still produce duplicates when the tile grid is narrow. [source; call_554dd2365646442ab6c3fe52d0c4ff3c, call_dc6154f354074db98ec1157bc1055a1f]

A scalar transcription confirmed unchanged sample counts but greater distinct coverage: a 4-by-4 tile grid has 12 samples and changes from 4 to 12 unique tiles; a 2-by-5 grid changes from 5 to 10 unique tiles among 15 samples. [execution; call_bce23afe5b1048f7bcbc4071256c09db]

Each trial quantizes tiles multiplied by scale, divides reconstructed values by that scale, and minimizes mean squared error against the original samples. Golden-section search retains bounds 0.1 and 1.9 and stops when interval width is at most 0.01; these are scale-search parameters, not bitrate limits. [source; call_554dd2365646442ab6c3fe52d0c4ff3c]

The whole-parent caller search found one direct caller, quantize_exl3. It supplies a ProgressBar after channel normalization and Hadamard transforms, multiplies weight_r by the returned scale, and divides su by the same scale before LDLQ. This compensating adjustment preserves the reconstruction scaling convention while changing the values presented to quantization. [source; call_08b81e0e32f54b4593180415f8ec42fc, call_554dd2365646442ab6c3fe52d0c4ff3c]

The patch also suppresses verbose interval-by-interval printing while retaining the final scale/error message, and guards pb.update so the default pb=None no longer causes an attribute access there. The newly appended synchronization loop follows an unconditional return and is unreachable on normal completion. [source; call_dc6154f354074db98ec1157bc1055a1f, call_554dd2365646442ab6c3fe52d0c4ff3c]

## Authoring-time findings — pending review

### unreachable-final-synchronization (suspected; defect)

The newly added exit synchronization cannot execute.

Trigger: g_scale_gss completes its search normally.

Expected: If the added loop is intended to synchronize selected devices before returning, it must run before the return.

Actual: return best_scale exits inside the stream context before control can reach the appended device loop.

Locations: bad500d7272a863b3d1b0cd5a3ed1f714370c972:exllamav3/modules/quant/exl3_lib/quantize.py — g_scale_gss

Source evidence: call_dc6154f354074db98ec1157bc1055a1f, call_554dd2365646442ab6c3fe52d0c4ff3c, call_08b81e0e32f54b4593180415f8ec42fc

source_inspection: Compared the appended loop with the unconditional return and inspected quantize_exl3, the only direct caller found in the whole-parent search. [call_dc6154f354074db98ec1157bc1055a1f, call_554dd2365646442ab6c3fe52d0c4ff3c, call_08b81e0e32f54b4593180415f8ec42fc]. Limits: This establishes dead code, not a CUDA race or a requirement for additional synchronization.

### inherited-premature-progress (suspected; defect)

The optional-progress guard carries over the premature-completion calculation.

Trigger: g_scale_gss contracts its interval with a visible ProgressBar supplied by quantize_exl3.

Expected: Intermediate search progress should remain distinguishable from completion.

Actual: int(delta2 / delta1) becomes zero after the first contraction, so every loop update reports 100 even while search continues.

Locations: bad500d7272a863b3d1b0cd5a3ed1f714370c972:exllamav3/modules/quant/exl3_lib/quantize.py — g_scale_gss

Source evidence: call_dc6154f354074db98ec1157bc1055a1f, call_554dd2365646442ab6c3fe52d0c4ff3c, call_8a7456b45f9b4231a0e795e1be126057

source_inspection: The sole located direct caller supplies a progress object; ProgressBar.update forwards the number as completed work. The patch guards the update but leaves its expression unchanged. [call_08b81e0e32f54b4593180415f8ec42fc, call_554dd2365646442ab6c3fe52d0c4ff3c, call_8a7456b45f9b4231a0e795e1be126057, call_dc6154f354074db98ec1157bc1055a1f]. Limits: Visibility depends on the caller supplying progress text; terminal rendering was not executed.

scalar_transcription: Modeled golden-section contraction from interval width 1.8 to below 0.01: all 11 updates were 100, ending at approximately 0.009045. [call_bce23afe5b1048f7bcbc4071256c09db]. Limits: Standard-library arithmetic only; not execution of the repository search or CUDA objective.

## Uncertainty and limits

No PyTorch, CUDA kernel, or end-to-end conversion was executed. Scalar checks establish indexing and interval arithmetic only, not GPU numerical behavior or model quality.

The sampling comment hopes for representative coverage; neither representative distributions nor a unimodal scale-error objective were empirically established.
