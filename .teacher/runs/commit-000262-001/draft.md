# d97bfdf1f402326f25773143dbe07751493758c1


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d97bfdf1f402326f25773143dbe07751493758c1) · [Evidence ledger](draft.json)

Adds validated FP32-input activation kernels producing FP16 outputs, while retaining incompatible in-place FP32 callers and the inherited odd-element tail.

- [FP32 activation inputs with FP16 gated outputs](#runtime)

## Problem

The activation wrappers previously interpreted every input as FP16. They could not correctly consume FP32 gate/up results. [source; call_d825888659d24a8aa0aaf373d0ea50fd]

## Reasoning

The change adds FP32-input, FP16-output kernels alongside the existing FP16 kernels. Dtype validation and dispatch are necessary together: float inputs now select float pointer loads rather than being reinterpreted as half. [source; call_bd6399fafa704e2283b31d00cbe55c0f]

## Impact

Both wrappers accept half/half or float/float inputs, always requiring a half output. Mixed input dtypes and float outputs are rejected; this is mixed input/output precision, not arbitrary dtype mixing. [source; call_bd6399fafa704e2283b31d00cbe55c0f, call_941d2d5bde5243b5a08805d5dbfe5dae]

## Source Notes

The initial runtime entry describes paired activation processing. The FP32-output entry records an incompatible GatedMLP intermediate path, and the padding-control entry records an odd-element activation tail. [ancestor; call_c59881c7a7024fdc83fbbad24a4c118e, call_093524af0ff54d59ad21e054d743d4ac, call_4f45973f4b7b4d8f8f53f12a4bf4a009]

Inspection of the task diff shows that the FP32 pointer interpretation is corrected, but unchanged in-place Python callers still supply an FP32 destination when their intermediates are FP32. The odd-element tail is also carried over into both kernel variants. [source; call_bd6399fafa704e2283b31d00cbe55c0f, call_43e66c7b06fc4bc5bc2752f1cb5180a2, call_d7f9937b3258475cae565b94465c3209]

<a id="runtime"></a>

## FP32 activation inputs with FP16 gated outputs

silu_mul and gelu_mul retain their signatures, caller-owned output, input-device guard and current CUDA stream. The header and pybind exports require no changes. Dispatch depends on x.dtype(); y must match, while z must be FP16. [source; call_bd6399fafa704e2283b31d00cbe55c0f, call_35c6fd345c0a448e978e2cefc855ed67, call_6f07cb7028e34be9b80d3a2c51a4ac1f]

act_mul_kernel_h is the renamed existing half2 kernel. act_mul_kernel_f loads two float elements from each input, applies activation independently, multiplies in float and converts the resulting pair once with __float22half2_rn. Thus the new route delays half conversion until after the product; the half GELU route rounds the activation before half multiplication. [source; call_bd6399fafa704e2283b31d00cbe55c0f, call_d825888659d24a8aa0aaf373d0ea50fd]

Float SiLU implements x/(1+exp(-x)) using __expf and __fdividef. Float GELU follows the existing tanh approximation, 0.5*x*(1+tanh(c*(x+0.044715*x^3))). tanh_opt selects an exponential identity under USE_ROCM or the older architecture/runtime condition, otherwise tanh.approx.f32. [source; call_bd6399fafa704e2283b31d00cbe55c0f, call_837f0741b029457b8d619dd91eb89fa6]

The GELU constant c is documented as sqrt(2/pi). A standard-library calculation gives 0.7978845608028654, differing from the decimal literal by approximately 1.35e-13 before CUDA float rounding. The coefficient 0.044715 is retained rather than derived by this change. [execution; call_e2646dafbb3b458587d4eb4e9c8bdc9b, call_bd6399fafa704e2283b31d00cbe55c0f]

Both kernels use 256 threads and two elements per thread, hence ceil(numel/512) blocks. Their numel/2 guard processes complete pairs only. Scalar enumeration covered all 128 and 512 elements, but omitted the last element at lengths 1, 3, 129 and 513. [execution; call_d825888659d24a8aa0aaf373d0ea50fd, call_bd6399fafa704e2283b31d00cbe55c0f, call_e2646dafbb3b458587d4eb4e9c8bdc9b]

Whole-parent searches locate activation consumers in GatedMLP and BlockSparseMLP. GatedMLP.forward and BlockSparseMLP's ordinary expert path call activation(g,u,u), compatible for half intermediates but not float intermediates under the new output check. BlockSparseMLP's fused path instead supplies interm_a: load allocates a separate half buffer when interm_dtype is not half, so its explicit FP32 configuration agrees with the new activation contract. [source; call_505fc341039744419b1c249e0e40ecbc, call_48c75dec316f4874812aa55ad37d6a63, call_43e66c7b06fc4bc5bc2752f1cb5180a2, call_d7f9937b3258475cae565b94465c3209, call_bd6399fafa704e2283b31d00cbe55c0f]

## Authoring-time findings — pending review

### fp32-inplace-callers (suspected; defect)

Existing in-place activation callers do not implement the new FP32-input/FP16-output contract.

Trigger: Run GatedMLP with FP32 gate/up intermediates, or BlockSparseMLP with FP32 intermediates on its ordinary expert path (bsz > 1 or not fully quantized).

Expected: The supported FP32 intermediate setting supplies a half activation destination for the subsequent down projection.

Actual: Both paths pass u as the destination while u remains FP32. The newly added z dtype check rejects the call before launching the activation kernel. This changes the inherited failure from incorrect half-pointer interpretation to explicit rejection; the fused BlockSparseMLP path already has a separate half destination.

Locations: d97bfdf1f402326f25773143dbe07751493758c1:exllamav3/exllamav3_ext/activation.cu — silu_mul / gelu_mul, fce1b96e3fa533e9d3e371b640d3a48c4f97eae7:exllamav3/modules/mlp.py — GatedMLP.forward, fce1b96e3fa533e9d3e371b640d3a48c4f97eae7:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_bd6399fafa704e2283b31d00cbe55c0f, call_43e66c7b06fc4bc5bc2752f1cb5180a2, call_d7f9937b3258475cae565b94465c3209, call_3a99aefbdd834c22aa8144b783be3b46

source_inspection: Compared all activation callers found by whole-tree searches with the new destination check and inspected intermediate allocation and LinearFP16 output dtype selection. [call_505fc341039744419b1c249e0e40ecbc, call_48c75dec316f4874812aa55ad37d6a63, call_ba6f68cd2d384aa48732ae29b5d50333, call_3a99aefbdd834c22aa8144b783be3b46]. Limits: Conditional opt-in paths; no model or CUDA execution and no claim that every workflow enables FP32 intermediates.

### odd-activation-tail (suspected; defect)

Both activation kernel variants omit an odd final element.

Trigger: Call either exported activation with otherwise suitable buffers and an odd element count; an opt-in unpadded GatedMLP intermediate can expose this case.

Expected: Every destination element receives activation(x)*y.

Actual: The numel/2 guard writes only complete pairs. A separate output retains its previous last element; an in-place half output retains an ungated last up value. Neither wrapper checks evenness or launches a scalar tail.

Locations: d97bfdf1f402326f25773143dbe07751493758c1:exllamav3/exllamav3_ext/activation.cu — act_mul_kernel_h / act_mul_kernel_f

Source evidence: call_bd6399fafa704e2283b31d00cbe55c0f, call_d825888659d24a8aa0aaf373d0ea50fd, call_43e66c7b06fc4bc5bc2752f1cb5180a2, call_6f07cb7028e34be9b80d3a2c51a4ac1f

scalar_transcription: Enumerated launch and pair-index arithmetic for lengths 1, 3, 128, 129, 512 and 513. [call_e2646dafbb3b458587d4eb4e9c8bdc9b]. Limits: Integer coverage model, not repository kernel execution.

## Uncertainty and limits

No extension build, CUDA execution, numerical accuracy test or benchmark was performed. Scalar indexing checks do not reproduce GPU arithmetic, alignment, concurrency or approximate transcendental instructions.

Literal whole-tree caller searches do not establish compatibility of dynamic or external callers.

The source does not explain the choice of 256 threads or the GELU cubic coefficient, and provides no measured comparison with alternative implementations.
