# 69f8f9a07b95142878997f79e0053b1c1e08422f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/69f8f9a07b95142878997f79e0053b1c1e08422f) · [Evidence ledger](draft.json)

Clamps FP32-input SiLU/GELU gated products to finite FP16 bounds after conversion. Half-input execution is unchanged, and inherited destination and odd-tail limitations remain.

- [Saturate FP32 gated activations at the FP16 output boundary](#runtime)

## Problem

The FP32-input gated activation kernel converted activation(x) * y directly to FP16 without saturation. Products exceeding FP16's finite range could therefore overflow at the output boundary. [source; call_ab1906e0d2c94fbf9ad21e7239179dfb, call_da7e0ad950b9465b9c04e4333f243555]

## Reasoning

The change clamps the converted half2 pair rather than changing activation evaluation or FP32 multiplication. This confines saturation to the existing FP32-to-FP16 boundary. [source; call_da7e0ad950b9465b9c04e4333f243555, call_ab1906e0d2c94fbf9ad21e7239179dfb]

## Impact

Both SiLU and GELU FP32-input routes receive the clamp. The FP16-input kernel and standalone PyTorch activations in MLP remain unchanged, so the commit message's scope is broader than the implementation. [source; call_da7e0ad950b9465b9c04e4333f243555, call_ab1906e0d2c94fbf9ad21e7239179dfb, call_3d865a1dac3640e99cc03117977687ee]

## Source Notes

The FP32 activation introduction entry records incompatible in-place FP32 destinations and an odd-element tail omission. [ancestor; call_c1275454a5524207971bd45997c07a17]

Current source narrows that inherited assessment: BlockSparseMLP now supplies a separate half destination when needed in both ordinary and fused execution. GatedMLP still passes u as its destination, and the paired-kernel tail omission remains. This task changes neither condition. [source; call_75f636278b16497fb257d5e0b223b11b, call_3d865a1dac3640e99cc03117977687ee, call_ab1906e0d2c94fbf9ad21e7239179dfb, call_da7e0ad950b9465b9c04e4333f243555]

Issue 55, “Possible GLM4 32B regression,” reports a loading-time int/NoneType comparison failure; issue 31, “TypeError with presence penalty,” reports incompatible sampler arguments. Neither discussion establishes motivation for this activation clamp. The inspected overlap with issue 55 is the mlp.py pathname, not a matching activation failure. [inference; call_f454daa4a2f542cf89954d3ef79c5dcb, call_53d97c139fda4c65a0cbeadca4267291, call_da7e0ad950b9465b9c04e4333f243555]

<a id="runtime"></a>

## Saturate FP32 gated activations at the FP16 output boundary

act_mul_kernel_f loads float2 gate and up values, evaluates the selected activation on the gate lanes, multiplies by the up lanes in float, and converts the pair with __float22half2_rn. The new clamp_half2_to_finite then applies an upper and lower half2 bound before storage. It clamps the gated product, not the activation alone. [source; call_ab1906e0d2c94fbf9ad21e7239179dfb, call_da7e0ad950b9465b9c04e4333f243555]

The bounds ±65504 are the finite binary16 endpoints: (2 − 2^-10) × 2^15 = 65504. A standard-library scalar model produced SiLU products ±1000000, modeled their half conversion as ±infinity, and saturated them to ±65504; an ordinary small product retained its rounded half value. [execution; call_bb255bcdf3c64846bb6da708a1cd45e6]

Saturation trades the magnitude of out-of-range products for a bounded FP16 value. Its placement preserves FP32 intermediates until conversion rather than clipping gate or up projections earlier; improved downstream stability is a plausible consequence, not a measured result. [inference; call_da7e0ad950b9465b9c04e4333f243555, call_ab1906e0d2c94fbf9ad21e7239179dfb]

silu_mul and gelu_mul dispatch on x.dtype(), require matching input dtypes and always require a half destination. Their FP32 branches share the changed kernel; half branches still use the unchanged half2 multiplication. The new helper is called only from act_mul_kernel_f. [source; call_ab1906e0d2c94fbf9ad21e7239179dfb, call_da7e0ad950b9465b9c04e4333f243555]

Whole-tree searches locate extension activation selection in GatedMLP and BlockSparseMLP. BlockSparseMLP's ordinary expert path uses a half temporary for non-half intermediates; its fully quantized single-token path uses the half interm_a buffer. Both feed that result to the down projection. GatedMLP instead calls activation(g, u, u), retaining the incompatible FP32-destination case. Plain MLP uses PyTorch activation functions and does not reach this clamp. [source; call_689d16399d114d4c967672d25775d71a, call_b22f58fd42bc488cbd073947eb1aaa14, call_459c1bb5801a4ea78dcd725dee6fbfb5, call_75f636278b16497fb257d5e0b223b11b, call_3d865a1dac3640e99cc03117977687ee]

## Authoring-time findings — pending review

### inherited-fp32-inplace-destination (suspected; defect)

GatedMLP retains an in-place destination incompatible with the extension's FP32-input contract.

Trigger: GatedMLP gate/up projections produce FP32 tensors.

Expected: Provide a half activation destination so execution can reach the clamped FP32-input kernel.

Actual: GatedMLP.forward passes FP32 u as z; the wrapper's half-destination check rejects it before launch. BlockSparseMLP's inspected ordinary and fused paths avoid this mismatch.

Locations: 69f8f9a07b95142878997f79e0053b1c1e08422f:exllamav3/modules/mlp.py — GatedMLP.forward

Source evidence: call_3d865a1dac3640e99cc03117977687ee, call_ab1906e0d2c94fbf9ad21e7239179dfb, call_da7e0ad950b9465b9c04e4333f243555, call_459c1bb5801a4ea78dcd725dee6fbfb5

source_inspection: Compared searched activation callers with wrapper dtype validation and the task's kernel-only change. [call_459c1bb5801a4ea78dcd725dee6fbfb5, call_3d865a1dac3640e99cc03117977687ee, call_75f636278b16497fb257d5e0b223b11b, call_ab1906e0d2c94fbf9ad21e7239179dfb]. Limits: Conditional on FP32 projection outputs; no model execution.

### inherited-odd-element-tail (suspected; defect)

Both paired activation kernels still omit an odd final element.

Trigger: An exported activation receives otherwise suitable buffers with odd numel; GatedMLP exposes configurable padding that can permit odd intermediate lengths.

Expected: Write activation(x) * y to every output element.

Actual: The numel/2 guard processes complete pairs only. The final destination element remains untouched; the clamp does not repair coverage.

Locations: 69f8f9a07b95142878997f79e0053b1c1e08422f:exllamav3/exllamav3_ext/activation.cu — act_mul_kernel_h / act_mul_kernel_f

Source evidence: call_ab1906e0d2c94fbf9ad21e7239179dfb, call_3d865a1dac3640e99cc03117977687ee, call_da7e0ad950b9465b9c04e4333f243555, call_459c1bb5801a4ea78dcd725dee6fbfb5

scalar_transcription: Enumerated the 256-thread, two-elements-per-thread launch and guard. Lengths 1, 3, 129 and 513 each left their final element unwritten; 128 and 512 were fully covered. [call_bb255bcdf3c64846bb6da708a1cd45e6, call_ab1906e0d2c94fbf9ad21e7239179dfb]. Limits: Integer coverage model only, not CUDA execution; ordinarily padded internal buffers can avoid this trigger.

## Uncertainty and limits

No CUDA compilation, repository kernel execution, numerical accuracy evaluation or performance measurement was performed.

The scalar model uses Python arithmetic and explicit overflow substitution; it does not reproduce CUDA approximate activation instructions or establish CUDA min/max behavior for NaNs.

Whole-tree literal searches establish the inspected internal callers, not dynamically selected or external consumers.
