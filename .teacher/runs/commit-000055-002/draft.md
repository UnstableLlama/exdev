# d6124d70584f83440fc8ad551f8f82bdf8479c64


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d6124d70584f83440fc8ad551f8f82bdf8479c64) · [Evidence ledger](draft.json)

Split wide gated MLPs into separately calibrated and quantized slices, offload their outputs, and reload the assembled block; retain tail-padding limitations and introduce ungated allocation incompatibilities.

- [Slice wide gated MLPs during conversion](#conversion)

## Problem

Wide gated MLPs require large weights and quadratic-size down-projection Hessians during conversion. The patch introduces a default splitting threshold of 55,296 intermediate features. [source; call_30f73a550d8e48e8b778222b023d7998, call_a9f64886943e4d3bbd310920725078a5]

## Reasoning

Quantizing one intermediate-feature slice at a time reduces the active down-projection Hessian and weight sizes, at the cost of repeated loading, calibration and attention quantization. This is a memory-versus-work tradeoff, not a measured performance improvement. [inference; call_8c9232a36a1241888bd85f12369d8957, call_8c9b6193c487430980b7816933859155, call_a9f64886943e4d3bbd310920725078a5]

## Impact

The converter now offloads each converted linear, collects tensors across slice passes, unloads the block, then reloads the complete converted block through the in-memory tensor collection before advancing calibration states. [source; call_8c9232a36a1241888bd85f12369d8957, call_66122601d0a74aeaba135e7ea2196762]

## Source Notes

The preceding entries describe CPU-staged feature slicing, memory-first loading, delayed weight restoration and explicit EXL3 offload. Their recorded observations are revisited here rather than treated as evidence of successful conversion. [ancestor; call_070ea848ffa64163a6786b7a7d0b8a1a, call_65b9af754084453ca5509027d3832743, call_2a633984b2d342399a625e80d68ca91b, call_49879c4e888f4915bcd9de2528819064]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension-import failure and a reporter-described environment workaround. It does not establish motivation for MLP splitting. [source; call_d55115b462004c4a89d2966734c9f3f7]

<a id="conversion"></a>

## Slice wide gated MLPs during conversion

GatedMLP defaults intermediate_split_size to MAX_MLP_INTERMEDIATE. Only widths strictly greater than the threshold split; None or zero disables splitting. Fused gate/up construction asserts that splitting is unnecessary or disabled. This changes the shared module, not an architecture registry. [source; call_8c9b6193c487430980b7816933859155]

For width I and threshold T, the constructor chooses ceil(I/T) slices, rounds the common width down to a multiple of 128, and puts the remainder in the last slice. Gate/up select output features; down selects the corresponding input features. Split tensors use .slice.N keys with the original unsplit key as fallback. Unsplit tensors retain their original keys. [source; call_8c9b6193c487430980b7816933859155]

Scalar checks give T=54×1024=432×128. Width 55,296 stays whole; 55,297 becomes [27,648, 27,649]; 425,984 becomes eight slices of 53,248. The 128 rounding aligns ordinary slices with Linear's output-padding granularity, but does not align an arbitrary final remainder. [execution; call_18dc6f1f14b4469090a1fa8d8bfaf074]

For an unsplit gated MLP, explicit full dimensions make Linear.is_sliced false, so ordinary FP16 weights load directly to the requested device. This removes the ancestor's default CPU-staging behavior for these constructions, but does not change Linear's default predicate for other callers. The fused-weight branch retains its separate frange mechanism. [source; call_8c9b6193c487430980b7816933859155, call_a9f64886943e4d3bbd310920725078a5, call_f716c5846d8a4d938f5c9d5c0727786c]

For aligned split layers loaded from ordinary unsplit weights, Linear stages the entire weight on CPU. LinearFP16 transposes it, selects the requested output columns for gate/up or input rows for down, copies the selected storage, then unswap_cpu transfers weight and bias to the requested device. This is not partial checkpoint I/O. Output selection also slices bias; input selection does not. [source; call_a9f64886943e4d3bbd310920725078a5, call_f716c5846d8a4d938f5c9d5c0727786c]

The inherited padding-before-slicing problem remains and now has a concrete gated-MLP caller: a non-128-aligned final gate/up slice attempts to pad the full source before selecting its local range. Successful aligned slicing must not be generalized to that tail case. [source; call_8c9b6193c487430980b7816933859155, call_a9f64886943e4d3bbd310920725078a5]

Allocation happens once for the entire module before loading. For gated lists, allocate_transformer sums all slice weight counts per projection family, chooses one bitrate per family using the existing budget options, then expands that choice to each concrete slice key. Attention retains individual keys. Empty transformer blocks now return an empty strategy and unchanged surplus. [source; call_b78929cf797c434d9d836f7765a2e43d, call_4479e0bfb7d245eea7dc4d44511545ef, call_a76c8bec58494644a1e38d2380f7fff4]

On every pass s of a block containing attention and a sliced gated MLP, recursive loading loads all present norms and all attention projections, but only gate/up/down slice s. Attention drops load kwargs rather than forwarding them. Capture executes attention plus that one MLP slice through q_mlp_slice=s; it creates a fresh capture dictionary and reference list each pass. Linear.capture_H shares a qmap's Hessian through its first_key rule, so gate/up reuse their common input capture while down captures the selected slice's activated features. [source; call_8c9232a36a1241888bd85f12369d8957, call_8c9b6193c487430980b7816933859155, call_2bcb16430ed6499c93e98070ff583cd1, call_83e52fbf4ed14cf0a88aa2842a0a4fb9, call_5f6a8d047bdf4ae28714fd11934800e5, call_a9f64886943e4d3bbd310920725078a5]

The pass quantizes every loaded Linear with a qmap: attention Q/K/V/O again on each pass and the current MLP triple, not the unloaded slices. Each converted linear is immediately swapped to CPU. Tensor collection retains earlier slice keys while later attention and norm values overwrite the same keys. module.unload recursively clears the whole block, including attention projections, current MLP tensors and norms; Attention.unload also releases its context, cache allocations and RoPE. [source; call_8c9232a36a1241888bd85f12369d8957, call_a9f64886943e4d3bbd310920725078a5, call_2bcb16430ed6499c93e98070ff583cd1, call_e0c809ff0b1e474dbb14bf3501b8b329, call_e2462b06e3a740718394bbbf928da5d9]

The converter supplies exactly two load keyword names: load_slice during pass loading and source during final reloading. Module forwards kwargs; GatedMLP consumes load_slice, with None loading all slices. Linear, RMSNorm and Embedding accept but ignore extra kwargs, while Attention discards them. No inspected loader consumes source: set_new_tensors(q_tensors), not that keyword, activates memory lookup. [source; call_4adda44920d040cdb21fdc2a7d8009fc, call_8c9232a36a1241888bd85f12369d8957, call_8c9b6193c487430980b7816933859155, call_2bcb16430ed6499c93e98070ff583cd1, call_a9f64886943e4d3bbd310920725078a5, call_83e52fbf4ed14cf0a88aa2842a0a4fb9, call_e2462b06e3a740718394bbbf928da5d9, call_0930416a4fc3436aa7e4176aeaef3f97]

Final reload creates new LinearEXL3 wrappers. Every present su, sv, suh, svh, trellis and bias is fetched using the layer's requested device; memory hits perform .to(device). Conversion currently emits suh, svh and trellis, plus any retained bias. scale remains unsupported by the constructor. Norm weights likewise load to the requested device; prefer_cpu modules still request CPU. The memory overlay is cleared after loading. [source; call_8c9232a36a1241888bd85f12369d8957, call_a9f64886943e4d3bbd310920725078a5, call_66122601d0a74aeaba135e7ea2196762, call_d118dffa6a234f58bff6ef07879c5b22, call_3f5096ff2e1a4970be9a3831a69d79b6, call_e2462b06e3a740718394bbbf928da5d9]

This reload changes the ancestor's CPU-bias observation in the converter: convert_exl3 still retains the swapped CPU bias, but the converter now reloads it onto the execution device before forward. Thus the converter's immediate post-conversion bias mismatch is removed by the new data flow, not by changing convert_exl3 itself. [source; call_a9f64886943e4d3bbd310920725078a5, call_8c9232a36a1241888bd85f12369d8957, call_66122601d0a74aeaba135e7ea2196762]

Without q_mlp_slice, GatedMLP.forward evaluates every slice and adds their down-projection outputs. Final state advancement therefore uses the assembled converted MLP. Reference-error arithmetic still compares these full outputs against ref_states retained from only the final single-slice capture: it averages ||x−ref||F/||ref||F over reference samples. The result is computed but displayed as rfn: N/A whenever num_slices exceeds one, rather than presented as a full-block reference error. [source; call_8c9b6193c487430980b7816933859155, call_8c9232a36a1241888bd85f12369d8957, call_23f8429d2c904c20aba852518fb6755f, call_f9e38b80ae644925a1f312543773714d]

The memory-loader ancestor's source-local group detection and native disk-read failure risk are carried over unchanged. Collected complete EXL3 groups avoid the split-source condition, and memory hits bypass native disk reads; initial loading and disk fallbacks do not. [source; call_66122601d0a74aeaba135e7ea2196762, call_a9f64886943e4d3bbd310920725078a5, call_6bd0ecc985094a4ba8b6439034615008, call_8c9232a36a1241888bd85f12369d8957]

The read reference configurations for Qwen/Qwen2.5-0.5B (4,864), TinyLlama/TinyLlama-1.1B-Chat-v1.0 (5,632), microsoft/Phi-3-mini-4k-instruct (8,192), mistralai/Mistral-7B-v0.1 (14,336) and unsloth/gemma-2-2b (9,216) all declare intermediate sizes below the threshold. [source; call_602801b297374f1e9e50a8b6af99d78d, call_19e5e1ac55e24ff8bfcbe2fc88a6d32c, call_fa796826ecb646aa9984b9cb6b23c8fc, call_a0c96b2307174a998c42276fd5de9577, call_76912d08b1044fd1babbd94086bf71cd]

DeciLM derives each active width as ceil-to-256(int(2×ffn_mult×hidden_size/3)). The read nvidia/Llama-3_1-Nemotron-51B-Instruct and nvidia/Llama-3_3-Nemotron-Super-49B-v1 configurations have hidden size 8,192 and maximum multiplier 5.25. Both Ultra-253B configurations—CPT-v1 and v1—have hidden size 16,384 and active multipliers 36.5625, 39, 31.40625 and 27.5625 that exceed the splitting threshold after conversion. [source; call_f54aed5e9ef243408d32ac59298135ac, call_7c05ecd72643402d8ab9bd9dc8a423df, call_921279c35c324c8d9ad99dfc5e28234e, call_9170d1b15dc246ef814d13b4b9b33d67, call_fd23068cbec44cff8fb46aeee5a6ee7e, call_b3a04413e0514b4f957dda99109f0bf2, call_19ffbfb944c8454e9182259d454eb211, call_0b858352f74e4a798233bed3ee77d538]

Scalar application of that formula gives a maximum 28,672 for the 51B and Super-49B examples, below threshold. The four large Ultra widths are 399,360, 425,984, 343,040 and 301,056. For 399,360, eight 49,920-wide slices reduce one illustrative float32 down-Hessian payload from 594.14 GiB to 9.28 GiB per active slice; these are storage calculations, not measured peak allocations. [execution; call_18dc6f1f14b4469090a1fa8d8bfaf074, call_400343c3cd444ebea32a3784ff874bf1]

## Authoring-time findings — pending review

### unaligned-tail-padding (suspected; defect)

Inherited padding-before-slicing can prevent loading the final gated-MLP slice.

Trigger: Convert an ordinary unsplit checkpoint with intermediate_size=55,297 and aligned hidden size, using the default split threshold and pad_to=128.

Expected: Select the final 27,649 output features, then pad the selected gate/up weight to 27,776 outputs.

Actual: Linear.load_fp16 calls pad_out on the complete 55,297-row source first, attempting to assign it to a 27,776-row destination before LinearFP16 can slice.

Locations: d6124d70584f83440fc8ad551f8f82bdf8479c64:exllamav3/modules/mlp.py — GatedMLP.__init__, 8e0634b6a595bc4aa6f5fbc24a1e59ffd7eaf7f6:exllamav3/modules/linear.py — Linear.load_fp16

Source evidence: call_8c9b6193c487430980b7816933859155, call_a9f64886943e4d3bbd310920725078a5, call_d396ce9d9b98427f987e4b393ef57a56

source_inspection: Whole-parent search identifies Linear.load as the direct load_fp16 caller. The new GatedMLP.load reaches it through selected gate/up linears; the ordinary FP16 branch is affected, not EXL3 loading. [call_d396ce9d9b98427f987e4b393ef57a56, call_a9f64886943e4d3bbd310920725078a5, call_8c9b6193c487430980b7816933859155]. Limits: No PyTorch assignment or conversion executed.

scalar_transcription: Computed the split and padded destination dimensions. [call_18dc6f1f14b4469090a1fa8d8bfaf074]. Limits: Integer shape arithmetic only.

### ungated-mlp-allocation-interface (suspected; defect)

Transformer allocation now expects plural projection lists even for the unchanged ungated MLP class.

Trigger: Call TransformerBlock.allocate_q with an MLP rather than GatedMLP.

Expected: Allocate the ungated up and down projections.

Actual: The new code reads self.mlp.ups and self.mlp.downs, while MLP defines only up and down.

Locations: d6124d70584f83440fc8ad551f8f82bdf8479c64:exllamav3/modules/transformer.py — TransformerBlock.allocate_q

Source evidence: call_a76c8bec58494644a1e38d2380f7fff4, call_0bb1a500d65b4bbd8b027faa15a1de32

source_inspection: Whole-parent searches find the converter calling allocate_q and model constructors using GatedMLP, not plain MLP. This is an ungated interface regression, not an established failure of those model constructors. [call_373931c50285483c9f23fdee67e07652, call_4444e1be8b5845f684d8d88f294b41e9, call_8c9232a36a1241888bd85f12369d8957]. Limits: No ungated block executed.

### ungated-list-allocation-key (suspected; defect)

The new ungated-list allocation branch appends lists instead of the constructed wildcard keys.

Trigger: Call allocate_transformer with g=None and list-valued u and d.

Expected: Build a strategy keyed by wildcard projection names and expand it to concrete slice keys.

Actual: keys += [m] stores each projection list; the strategy dictionary comprehension then attempts to use an unhashable list as a key.

Locations: d6124d70584f83440fc8ad551f8f82bdf8479c64:exllamav3/conversion/allocation.py — allocate_transformer

Source evidence: call_b78929cf797c434d9d836f7765a2e43d

source_inspection: Whole-parent search finds TransformerBlock.allocate_q as the application caller. Current model construction uses GatedMLP, which selects the separate gated branch; plain MLP encounters the missing plural attributes first. [call_2ee4a4da15aa4520b03b388ed9a82930, call_a76c8bec58494644a1e38d2380f7fff4, call_4444e1be8b5845f684d8d88f294b41e9]. Limits: Reach is conditional on supplying ungated lists.

scalar_transcription: Constructing a dictionary from a list-valued key raised TypeError. [call_18dc6f1f14b4469090a1fa8d8bfaf074]. Limits: Modeled dictionary operation, not repository allocator execution.

### inherited-split-source-group (suspected; behavior_change)

Memory-plus-disk group completeness remains source-local.

Trigger: An EXL3 group is complete only across memory and disk, such as memory su/sv with disk trellis.

Expected: If group detection mirrors individual tensor availability, recognize the combined group.

Actual: has_tensor_group requires completeness within one source, so Linear.load_exl3 declines the group.

Locations: 8e0634b6a595bc4aa6f5fbc24a1e59ffd7eaf7f6:exllamav3/loader/safetensors.py — SafetensorsCollection.has_tensor_group

Source evidence: call_66122601d0a74aeaba135e7ea2196762, call_a9f64886943e4d3bbd310920725078a5

source_inspection: Whole-parent caller search finds Linear's FP16 and EXL3 group checks. The converter collects complete converted groups, so its ordinary reload does not require cross-source composition. [call_e30669a3db0b4c3b88804667515e9743, call_8c9232a36a1241888bd85f12369d8957, call_d118dffa6a234f58bff6ef07879c5b22]. Limits: Source-local completeness may be intentional; no loading execution.

### inherited-native-read-wait (suspected; defect)

The native disk loader's failure-wakeup risk persists outside successful memory hits.

Trigger: A GPU-target native read fails while its copy worker waits on an empty queue, with no subsequent enqueue.

Expected: Wake the worker and report the I/O error.

Actual: The reader sets load_failed without notification; the wait predicate checks only queue nonemptiness, so joining the worker may not complete.

Locations: 8e0634b6a595bc4aa6f5fbc24a1e59ffd7eaf7f6:exllamav3/exllamav3_ext/stloader.cpp — stloader_read

Source evidence: call_6bd0ecc985094a4ba8b6439034615008

source_inspection: Whole-parent search locates the binding and SafetensorsCollection.get_tensor caller. Initial GPU disk loads and fallback reads remain exposed; CPU-staged weights and memory-hit reloads bypass the copy worker. [call_5136d3cb035749c1ae40417a0b05bf39, call_66122601d0a74aeaba135e7ea2196762, call_a9f64886943e4d3bbd310920725078a5]. Limits: No injected I/O failure or concurrent execution.

## Uncertainty and limits

No repository conversion, PyTorch loading, CUDA kernel, numerical-quality benchmark or peak-memory measurement was executed. Python checks transcribed dimension and dictionary operations only.

The source identifies 55,296 as a practical single-GPU limit but supplies no hardware-specific derivation or benchmark establishing that limit.

Configuration comparisons establish widths, not successful end-to-end support for the listed checkpoints.
