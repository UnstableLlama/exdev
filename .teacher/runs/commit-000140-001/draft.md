# c6aa83f7e5a5e735c079d41244cbc704eda7e54e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c6aa83f7e5a5e735c079d41244cbc704eda7e54e) · [Evidence ledger](draft.json)

Extends module-scoped deferred loading to explicit single-device loads, preserving eligibility and placement rules; performance is unmeasured and the inherited odd-element BF16 conversion gap persists.

- [Deferred loading for explicit single-device placement](#loading)

## Problem

Explicit single-device loading performed immediate module loads, unlike autosplit loading, which already bracketed eligible modules with deferred loading. [source; call_723d1ad524674cbe8dc41d2bb9f36e8e]

## Reasoning

The change reuses the existing module-scoped batching lifecycle rather than introducing another loader. Reduced per-tensor loading overhead is a plausible rationale, not a measured improvement. [inference; call_a38a5c0f8fc349a999d3a32bb1867258, call_ff8a603cda5d4425b6bb66288a150492]

## Impact

For eligible modules, _load_single now begins deferral, constructs the module, and flushes pending reads before advancing progress. CPU-preferred placement remains unchanged. [source; call_a38a5c0f8fc349a999d3a32bb1867258]

## Source Notes

The earlier deferred-loader entry explicitly identified single-device loading as not adopting this lifecycle. [ancestor; call_d4af7425167044cf8df1bfc8f670c490]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension import failure; issue #33, “Error converting model,” ultimately reports too many open files during conversion. Their relevance here is inferred only from model.py and Safetensors-loader overlap, respectively; neither establishes motivation or validation for this change. [inference; call_8d97e797d3844251ae040faa36798815, call_f49936525f4244288c669fdd8ba082e9, call_a4e0353a8b024a2b8f56e708941a3281, call_a38a5c0f8fc349a999d3a32bb1867258]

<a id="loading"></a>

## Deferred loading for explicit single-device placement

load_gen selects _load_single when device is explicitly supplied; load consumes that generator. This is distinct from autosplit, even when autosplit happens to use only one GPU. [source; call_723d1ad524674cbe8dc41d2bb9f36e8e]

Eligibility is recursive: leaves permit deferral and composites require all children to permit it. Sliced Linear instances and multi-slice GatedMLP instances opt out. Packed EXL3 su/sv reads and fused FP16 weight reads explicitly bypass deferral where values are needed during construction. [source; call_bb343cd34e964eaf80fe4e43cfc7f4ae, call_03640904636b4ff0a51cd7b990758242, call_e0d8bf78d5e7466d99318771331d8cc6]

Only mt_fread switches to deferred reads; the Python backend and no_defer requests stay immediate. Deferred get_tensor returns allocated destinations and records pending transfers. Transposition, padding and FP32-to-FP16 conversion may require temporary storage alongside the final allocation. [source; call_ff8a603cda5d4425b6bb66288a150492]

The flush groups requests by CPU/CUDA and filename, sorts tensors by descending byte size, and splits transfers into at most 2 MiB jobs. CUDA workers stage file bytes through pinned host buffers. Temporary tensors are subsequently transposed as needed and copied into destination regions; successful completion clears deferred state. [source; call_ff8a603cda5d4425b6bb66288a150492, call_301d3610813b40cda9ac838d9aa2e0f2]

The inherited odd-element BF16 CUDA conversion gap remains unchanged and becomes reachable through eligible explicit-device loads. A scalar transcription covered all two elements for an even tensor, but left one uncovered for both three elements and 1,048,577 elements spanning two chunks. [execution; call_6bc1f94f9a9f48d7a63674640f696900, call_5f5d7e6c54f04b58a5449d7862302067, call_a38a5c0f8fc349a999d3a32bb1867258]

## Authoring-time findings — pending review

### inherited-deferred-bf16-tail (suspected; defect)

The unchanged deferred CUDA BF16 converter processes pairs only; adopting it for explicit-device loading extends exposure to its missing odd-element tail.

Trigger: An eligible module requests a file-backed, odd-element BF16 tensor on CUDA through mt_fread with conversion to FP16 enabled and without no_defer.

Expected: Every element is converted to FP16 before consumption.

Actual: The helper launches conversion for numel / 2 pairs, leaving the final odd element unconverted. A one-element final chunk computes zero launch blocks; runtime handling is untested.

Locations: 6fc153d7a062aa7f53fe13b27d008c2d90d8d62f:exllamav3/exllamav3_ext/stloader_cu.cu — inplace_bf16_to_fp16_cuda, c6aa83f7e5a5e735c079d41244cbc704eda7e54e:exllamav3/models/model.py — Model._load_single

Source evidence: call_5f5d7e6c54f04b58a5449d7862302067, call_301d3610813b40cda9ac838d9aa2e0f2, call_a38a5c0f8fc349a999d3a32bb1867258

source_inspection: Whole-parent-tree search locates the direct call in stloader_deferred_cuda. Inspection traces it through end_deferred_load and the newly bracketed _load_single. The task changes only model.py, carrying over the converter unchanged. [call_8b45474ccd6946f78c292046c4e001ba, call_301d3610813b40cda9ac838d9aa2e0f2, call_ff8a603cda5d4425b6bb66288a150492, call_a38a5c0f8fc349a999d3a32bb1867258]. Limits: Conditional reach only; no affected checkpoint was demonstrated.

scalar_transcription: Standard-library Python modeled the inspected 2 MiB chunking and integer pair counts for even, odd and multi-chunk tensors. [call_6bc1f94f9a9f48d7a63674640f696900]. Limits: Not execution of the repository kernel; bounded integer arithmetic does not test GPU conversion or synchronization.

## Uncertainty and limits

No repository loading implementation or CUDA kernel was executed; throughput, peak memory and stream behavior remain unmeasured.

The scalar check models chunk and pair coverage only, not conversion rounding or zero-block CUDA launch behavior.

Compatibility across every module constructor and checkpoint was not established.
