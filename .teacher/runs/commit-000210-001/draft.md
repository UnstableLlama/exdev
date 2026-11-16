# 49ac13c04f4c622582e2d519f2d135a53c1c4eaf


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/49ac13c04f4c622582e2d519f2d135a53c1c4eaf) · [Evidence ledger](draft.json)

Replaces zero-filled reconstruction storage with torch.empty, avoiding redundant initialization for supported shapes while exposing unwritten contents for an inherited unsupported-width case.

- [Reconstruct without zero-filling](#quantized-inference)

## Problem

Inner-weight reconstruction zero-initialized a full FP16 matrix immediately before a kernel overwrote it. [source; call_b933a75f6c7047b9a1dd28f156b96eda, call_9e33d352c5654444895d57910d627e3f]

## Reasoning

Using torch.empty avoids redundant initialization when reconstruction covers the whole output. This is a performance interpretation, not a measured speedup. [inference; call_b933a75f6c7047b9a1dd28f156b96eda, call_9e33d352c5654444895d57910d627e3f]

## Impact

Shape, FP16 dtype, device placement, reconstruction arguments and return value remain unchanged. Direct callers are forward's reconstruction branch and get_weight_tensor; direct quantized GEMM does not use this allocation. [source; call_b256bacec3d84919b4ad665993c909b8, call_fd92a1dd8abf4e23af57083162458b94, call_b933a75f6c7047b9a1dd28f156b96eda]

## Source Notes

The root quantized-inference entry describes the two execution paths and records missing reconstruction-width validation. [ancestor; call_a0c88aa80a194505bc317560b31895c1]

Issue #11, “AssertionError: bias is wrong datatype,” concerns a constructor assertion, not reconstruction allocation. Its connection here is only inferred from the shared exl3.py path; it does not establish motivation for this change. [inference; call_a5b33537cb2b4697a3bd5961063ee973, call_b933a75f6c7047b9a1dd28f156b96eda]

<a id="quantized-inference"></a>

## Reconstruct without zero-filling

get_inner_weight_tensor now allocates uninitialized storage and passes it to ext.reconstruct. forward uses that helper when params['reconstruct'] is true, defaulting to more than 32 flattened input rows; get_weight_tensor additionally applies Hadamards and channel factors. [source; call_b933a75f6c7047b9a1dd28f156b96eda, call_b256bacec3d84919b4ad665993c909b8]

Each reconstruction block uses 256 threads to write a 16×128 region: each thread stores eight half values through int4. Stores replace destination values rather than accumulating into them. Complete coverage requires packed column count divisible by eight, corresponding to output width divisible by 128. [source; call_9e33d352c5654444895d57910d627e3f]

A standard-library transcription of global store addresses found exactly one write per output element for two packed rows and 8 or 16 packed columns. With 9 packed columns it covered 4096 of 4608 elements, leaving 512 unwritten. [execution; call_b4f660785ba547f0bc7bbb7eb05f44c7]

The inherited width-validation gap persists: the launcher still truncates cols/8, while deriving its output stride from that truncated grid. Zero initialization previously supplied zeros to unwritten storage, though it did not repair the incorrect layout; empty allocation removes that fallback. [source; call_9e33d352c5654444895d57910d627e3f, call_b933a75f6c7047b9a1dd28f156b96eda]

## Authoring-time findings — pending review

### incomplete-reconstruction-width (suspected; defect)

A previously unguarded partial-width reconstruction can now return unwritten allocation contents.

Trigger: Construct LinearEXL3 with compatible scales, in_features=32, out_features=144 and an int16 trellis of shape (2,9,16), then call get_inner_weight_tensor with valid device storage.

Expected: Reject unsupported dimensions or reconstruct every element using the actual output stride.

Actual: The inspected constructor and native shape checks permit these dimensions. The kernel launches one column block, uses a 128-element row stride and writes only 4096 of 4608 allocated elements; the remaining storage is no longer initialized to zero.

Locations: 49ac13c04f4c622582e2d519f2d135a53c1c4eaf:exllamav3/modules/quant/exl3.py — LinearEXL3.get_inner_weight_tensor, 8ff65b874202176c1449e6a51998094ef60f94f0:exllamav3/exllamav3_ext/quant/reconstruct.cu — reconstruct

Source evidence: call_b256bacec3d84919b4ad665993c909b8, call_9e33d352c5654444895d57910d627e3f, call_b933a75f6c7047b9a1dd28f156b96eda, call_fd92a1dd8abf4e23af57083162458b94

source_inspection: Inspected constructor, helper, both direct callers and native launch checks. No width-divisibility check protects a direct helper call. [call_b256bacec3d84919b4ad665993c909b8, call_9e33d352c5654444895d57910d627e3f, call_fd92a1dd8abf4e23af57083162458b94]. Limits: Normal model-loading reach was not established.

scalar_transcription: Enumerated kernel output addresses for complete and incomplete column groups. [call_b4f660785ba547f0bc7bbb7eb05f44c7]. Limits: CPU integer indexing model only; no repository kernel ran.

## Uncertainty and limits

No CUDA execution, numerical comparison or performance benchmark was performed. The scalar check models output addressing only, not decoding, synchronization or allocator behavior.

The malformed-width observation establishes a callable constructor/helper path, not that normal model loading produces such dimensions.
