# cf848114852240a51fb6b9e77c686051c39302b2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/cf848114852240a51fb6b9e77c686051c39302b2) · [Evidence ledger](draft.json)

Adds independently configurable 2–8-bit paged KV storage using 32-value Hadamard quantization, with FP16 reconstruction around FlashAttention. Storage arithmetic was checked scalarly; GPU performance and accuracy remain unmeasured.

- [Paged KV compression around FP16 attention](#cache)

## Problem

KV storage previously used persistent FP16 tensors. This change adds independently selectable 2–8-bit key and value storage while retaining the FP16 attention interface. [source; call_c07cd04b64a34774b29ef310a894da89, call_10015b634e9844e49dd392f2881b571e, call_05b5778c22574a8bb297b195df08e7e9]

## Reasoning

Compression is placed around cached FlashAttention rather than inside attention: reconstruct existing tokens, let attention consume and extend the FP16 cache, then compress only the newly appended positions. [source; call_05b5778c22574a8bb297b195df08e7e9, call_10015b634e9844e49dd392f2881b571e, call_d5a77cbbf026422a95e3b0fd2cfba7a7]

## Impact

The shared model initializer accepts -cq/--cache_quant as one bitrate for both tensors or a comma-separated K,V pair. Omission retains FP16; the quantized constructor asserts that both rates are between 2 and 8. [source; call_7cba3804b86d4916abd3e9ed8026f0e2, call_10015b634e9844e49dd392f2881b571e]

Custom cache layers must accept the expanded get_kv interface and implement update_kv. Whole-parent-tree literal searches found only the built-in get_layer/get_kv calls, which the patch updates. [source; call_cd378533b51148b19ac5ae91aa4eef12, call_e5ba610e73804e5fb25cc88e26e32c0c, call_7af81df753d64cc09b81412d6c14b4de, call_fc46274a05bb4f589c519d1e08eb3342, call_05b5778c22574a8bb297b195df08e7e9]

## Source Notes

Issue #1, “Cache Quantization Strategy,” asks about retaining ExLlamaV2's approach; turboderp replies that alternatives remain exploratory. Its relationship to this change is inferred from the shared KV-cache topic, not an explicit commit reference or evidence of a particular paper implementation. [inference; call_c2499d41b6b644c5ae490b913eff6d7e, call_d5a77cbbf026422a95e3b0fd2cfba7a7]

The inspected failure discussions concern different mechanisms: #7 reports “quantizing model: undefined symbol: __cxa_call_terminate”; #15 reports incoherent cogito output at bpw <= 2.5; #16 reports “RuntimeError: CUDA error: invalid configuration argument” during conversion, subsequently attributed in discussion to tokenizer truncation. They do not establish failures or validation of the new cache codec. [source; call_fda80e3ec10244a4a951ad018f00bce4, call_ad2eefcfe320462e815345a6db73ec08, call_ae3df51cc5a34287b1434b2e277ad99a]

The earlier cache entry records a mismatched-layer detachment diagnostic defect. [ancestor; call_6d14797597764ae994efa7c1110adb9c]

<a id="cache"></a>

## Paged KV compression around FP16 attention

Cache forwards constructor keyword arguments to each layer and routes sequence lengths and block tables through get_layer and update_layer. FP16 layers return their persistent tensors and make update_kv a no-op; quantized layers allocate temporary FP16 tensors, decompress into them, and subsequently encode their updated contents. [source; call_7af81df753d64cc09b81412d6c14b4de, call_fc46274a05bb4f589c519d1e08eb3342, call_10015b634e9844e49dd392f2881b571e]

For D = num_kv_heads × head_dim, each token stores D/32 groups. Each group has b int32 bitplanes and one FP16 scale per K or V tensor. Page copying transfers compressed keys, values and both scale arrays directly, requiring matching compressed shapes. [source; call_10015b634e9844e49dd392f2881b571e]

The scalar storage calculation gives b + 0.5 bits per value, including scales: 4-bit payloads therefore use 4.5 bits per value, excluding temporaries and allocation overhead. A scalar transcription also verified bitplane packing/unpacking for rates 2 through 8. [execution; call_15e79daccb92483180100f7340b25074]

quant_block rotates 32 values with a warp-shuffle Hadamard transform, multiplies by approximately 1/sqrt(32), and stores the maximum absolute transformed value as a half-precision scale. It rounds scaled values to signed levels [-2^(b-1), 2^(b-1)-1], offsets them to unsigned codes and ballots each bitplane. dequant_block reverses packing and scaling, then applies the same rotation. [source; call_d5a77cbbf026422a95e3b0fd2cfba7a7]

The scalar Hadamard transcription squared to 32 times the input. The source constant 0.17678 approximates 1/sqrt(32) = 0.1767766953; applying that rounded normalization twice gives a gain of approximately 1.00003739 before quantization and floating-point rounding. [execution; call_15e79daccb92483180100f7340b25074]

Paged encoding maps logical positions starting at cache_seqlens through block_table and writes seq_len new tokens. Decoding maps positions strictly before cache_seqlens back into physical FP16 pages. Native paged wrappers require the flattened token dimension to be divisible by 32 and dispatch separate K/V bitrate specializations; contiguous wrappers instead require the last dimension to be divisible by 32. [source; call_0c1b67ccbc774f94922123500b4d341c, call_d5a77cbbf026422a95e3b0fd2cfba7a7]

Keeping the ordinary attention call avoids introducing a compressed-attention implementation, but requires reconstruction of the active prefix and full-capacity temporary buffers on each quantized get_kv. Thus persistent storage reduction should not be equated with the same reduction in peak memory or attention work. [inference; call_10015b634e9844e49dd392f2881b571e, call_05b5778c22574a8bb297b195df08e7e9, call_d5a77cbbf026422a95e3b0fd2cfba7a7]

The added paging test uses cuda:1 and 8-bit payloads, exercises several head dimensions and batch/page layouts, permutes pages and appends five tokens. It compares reconstructed tensors with atol=0.08 and rtol=0.01; it is not evidence of lower-bitrate model accuracy. The exploratory script separately compares integer, rotated, channel-scaled and FP8 alternatives using attention-output NMSE and score-distribution KL divergence. [source; call_c5700dac0f824c4f964b8b47124e77a9, call_69a7833202514631bdb0fff82814996b]

## Authoring-time findings — pending review

### zero-block-scale (suspected; defect)

The small additive scale floor disappears when converted to FP16, leaving zero-block normalization without a nonzero denominator.

Trigger: Encode a 32-value block containing only zeros.

Expected: Represent the zero block without division by zero or non-finite intermediate quantization values.

Actual: quant_block computes a scale near 1e-10, rounds it to half zero, reloads it and evaluates v /= s with zero numerator and denominator before lrintf. Final GPU integer conversion and decoded output were not established.

Locations: cf848114852240a51fb6b9e77c686051c39302b2:exllamav3/exllamav3_ext/cache/q_cache_kernels.cuh — quant_block

Source evidence: call_d5a77cbbf026422a95e3b0fd2cfba7a7, call_a82169ffd6df47e4bccd6fbaf732341d, call_10015b634e9844e49dd392f2881b571e, call_15e79daccb92483180100f7340b25074

source_inspection: The new contiguous and paged quantization kernels both call quant_block. Parent-tree search found no existing quant_block; new paged calls are reachable through CacheLayer_quant.update_kv, while the experiment also calls the contiguous API. [call_d5a77cbbf026422a95e3b0fd2cfba7a7, call_a82169ffd6df47e4bccd6fbaf732341d, call_10015b634e9844e49dd392f2881b571e, call_69a7833202514631bdb0fff82814996b]. Limits: Reach is conditional on a zero input block; no model-level failure was reproduced.

scalar_transcription: Python struct binary16 conversion rounded 1e-10 to 0.0. [call_15e79daccb92483180100f7340b25074]. Limits: This checks scale representability, not CUDA lrintf behavior or end-to-end reconstruction.

### inherited-detach-diagnostic (suspected; defect)

The previously noted detachment diagnostic is carried over unchanged.

Trigger: Call Cache.detach_from_model with assertions enabled and a model having a different cache-layer count.

Expected: Raise an AssertionError describing the incompatible counts.

Actual: The assertion message calls integer model_num_layers as model_num_layers(), producing a TypeError instead. Matching counts bypass this expression.

Locations: cf848114852240a51fb6b9e77c686051c39302b2:exllamav3/cache/cache.py — Cache.detach_from_model

Source evidence: call_63d001a62d714d479e1f4570f327a1f1, call_7af81df753d64cc09b81412d6c14b4de, call_b67c4f836bb54cea9d29bdd96956c51c

source_inspection: The parent contains the integer call and the task diff leaves it unchanged. Whole-parent-tree search found only the definition and its documentation reference, not direct repository callers. [call_63d001a62d714d479e1f4570f327a1f1, call_7af81df753d64cc09b81412d6c14b4de, call_b67c4f836bb54cea9d29bdd96956c51c]. Limits: No detachment workflow was executed; ordinary cache allocation does not itself trigger this diagnostic.

## Uncertainty and limits

No CUDA kernel, PyTorch allocation, FlashAttention call, repository test or model-quality benchmark was executed. Scalar checks use Python arithmetic and binary16 conversion, not GPU execution.

Peak VRAM savings and throughput are unmeasured; quantized get_kv still allocates full-capacity FP16 K/V temporaries.

The binary Humaneval image was not interpreted; no quality result is inferred from its addition.

Literal caller searches do not establish compatibility for external subclasses or dynamically selected calls.
