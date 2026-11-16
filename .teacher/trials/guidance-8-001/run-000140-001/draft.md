# c6aa83f7e5a5e735c079d41244cbc704eda7e54e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c6aa83f7e5a5e735c079d41244cbc704eda7e54e) · [Evidence ledger](draft.json)

Extends guarded, module-scoped deferred loading to explicit-device loads. Performance is unmeasured; exception cleanup is omitted and inherited conversion and progress limitations remain.

- [Deferred reads for explicit-device loading](#loading)

## Problem

Explicit-device loading read modules without the deferred-loading lifecycle already used by autosplit. [source; call_7f6c15b99df647adbd232baeffe75e13, call_1505428e0a0241a589080b875e53e44a]

## Reasoning

Reusing module-scoped batching plausibly reduces individual-read overhead while retaining eligibility guards. This is an inferred performance rationale, not a measured speedup. [inference; call_1505428e0a0241a589080b875e53e44a, call_c589f41859d340b5886fc4caeeb53ea7]

## Impact

Eligible modules now complete their deferred reads before the single-device progress bar advances. Device placement, including prefer_cpu, is unchanged. [source; call_1505428e0a0241a589080b875e53e44a]

## Source Notes

Read ancestor 647bb7d549b8485ad052ac0650148bd35fcee6d4: it establishes the deferred-loader lifecycle, constructor-safety requirements and an odd-element CUDA BF16 conversion observation. Read 6c15b8c40f0d28807006ad65d2c9e31382a352b4: it describes shared successful-load cleanup and the explicit-device progress omission. [ancestor; call_dfd00b225431468db1eaaca6238e96b7, call_b2af5fe9206c4c62b165d4214d59c56e]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension import failure. Issue #33, “Error converting model,” ultimately reports too many open files during compilation. Their connections here are inferred only from model.py and loader-source overlap, respectively; neither establishes motivation or validation for this change. [inference; call_e42c20da53c141eb95cfaec2da4a34c8, call_e8da5752046c4504a2ce61e12478e7e2, call_aa4b01968b2242988c690fccc3390d35, call_1505428e0a0241a589080b875e53e44a]

<a id="loading"></a>

## Deferred reads for explicit-device loading

_load_single now checks can_defer_load, begins deferral, loads the module, and flushes before updating progress. The whole-tree search finds load_gen as its sole direct caller; load_gen selects it when device is supplied, and Model.load exhausts that generator. [source; call_1505428e0a0241a589080b875e53e44a, call_bdad27424e8f43678fb326b69ffcd55e, call_7f6c15b99df647adbd232baeffe75e13]

Eligibility is recursive: leaves permit deferral, composites require every child to permit it, sliced Linear instances reject it, and GatedMLP rejects multiple slices. The new caller preserves the same guard as autosplit. [source; call_0c66e527d95848e59567352e8140cae3, call_9e5db7193db340d7904b4f25cbd87cc9, call_8fb7f9209aa94beeb5b2c0bb18eca12d, call_9e5f480a0b2f466ebf7d8d9f888d194a, call_1505428e0a0241a589080b875e53e44a]

Only mt_fread requests switch to deferred reads, unless no_defer is set. Python-backend reads and in-memory overrides remain immediate. Deferred requests allocate destinations before population, retaining temporary tensors when transposition, padding or FP32 conversion requires them. [source; call_c589f41859d340b5886fc4caeeb53ea7]

The flush groups requests by CPU/CUDA and filename, sorts each group by descending byte size, and divides reads into at-most-2-MiB jobs. Native CUDA loading stages through host buffers; afterward Python copies transformed temporary tensors into destinations. This batches within each module, not across the whole model. [source; call_c589f41859d340b5886fc4caeeb53ea7, call_f64fa403fec84ab39124e9c89aa82a84, call_1505428e0a0241a589080b875e53e44a]

The existing autosplit caller wraps loading in exception handling that aborts pending reads before OOM recovery or rethrow. The new single-device caller copies the successful lifecycle but not that cleanup. [source; call_4ddb2b0b4ba44eafa953a52a7d8c1566, call_7f6c15b99df647adbd232baeffe75e13, call_1505428e0a0241a589080b875e53e44a]

A scalar transcription confirms the current chunk limit is 2,097,152 bytes. Pair-only conversion leaves one element uncovered for counts 1, 3, 2049 and 1,048,577; interpreting BF16-one bits as FP16 produces 1.875 rather than 1.0. [execution; call_f50a003758ce40de9ee314b056a22566]

## Authoring-time findings — pending review

### single-device-deferred-abort (suspected; defect)

The new single-device lifecycle omits exception-time deferred-state cleanup.

Trigger: An eligible module's load or deferred flush raises after begin_deferred_load.

Expected: Clear pending requests and deferred_mode before propagating the exception, as autosplit does.

Actual: The exception escapes with deferred_mode still true and potentially retained destination tensors. A subsequent eligible load on the same collection encounters begin_deferred_load's assertion.

Locations: c6aa83f7e5a5e735c079d41244cbc704eda7e54e:exllamav3/models/model.py — Model._load_single

Source evidence: call_1505428e0a0241a589080b875e53e44a, call_7f6c15b99df647adbd232baeffe75e13, call_c589f41859d340b5886fc4caeeb53ea7

source_inspection: Compared both lifecycle callers and loader reset operations. The sole direct _load_single caller is load_gen's explicit-device branch, also reachable through Model.load. [call_bdad27424e8f43678fb326b69ffcd55e, call_4ddb2b0b4ba44eafa953a52a7d8c1566, call_7f6c15b99df647adbd232baeffe75e13]. Limits: No failure injection or retry was executed.

### inherited-deferred-bf16-tail (suspected; defect)

The inherited odd-element CUDA BF16 conversion gap persists and is now reachable through explicit-device deferred loading.

Trigger: An eligible module requests a file-backed, odd-element BF16 tensor on CUDA with conversion to FP16 and without bypassing deferral.

Expected: Convert every element before consuming the FP16 destination.

Actual: The CUDA helper passes numel / 2 to a pair-conversion kernel, leaving the odd final element unconverted. The task does not modify that helper.

Locations: c6aa83f7e5a5e735c079d41244cbc704eda7e54e:exllamav3/exllamav3_ext/stloader_cu.cu — inplace_bf16_to_fp16_cuda

Source evidence: call_d385a1bbbe114f68a77bc288ba5f05e1, call_f64fa403fec84ab39124e9c89aa82a84, call_c589f41859d340b5886fc4caeeb53ea7, call_1505428e0a0241a589080b875e53e44a

source_inspection: Whole-tree helper search identifies stloader_deferred_cuda as the direct caller. Traced it through end_deferred_load to the existing autosplit and new explicit-device lifecycle; CPU conversion handles individual elements. [call_966b637c6f604552b4bfee1dc6e6fc7b, call_d385a1bbbe114f68a77bc288ba5f05e1, call_f64fa403fec84ab39124e9c89aa82a84]. Limits: Conditional reach, not evidence that every model contains affected tensors.

scalar_transcription: Modeled current chunk splitting and pair coverage, and decoded an illustrative unchanged BF16 bit pattern as binary16. [call_f50a003758ce40de9ee314b056a22566]. Limits: Standard-library arithmetic only; no GPU kernel execution.

### inherited-single-device-progress (suspected; behavior_change)

The previously recorded explicit-device callback and generator-progress omission remains unchanged.

Trigger: Use load_gen(device=...) expecting progress tuples, or load(device=..., callback=...) expecting notifications.

Expected: Receive progress through the requested interface.

Actual: _load_single updates only its progress bar; it neither yields progress nor invokes the callback.

Locations: c6aa83f7e5a5e735c079d41244cbc704eda7e54e:exllamav3/models/model.py — Model.load_gen

Source evidence: call_1505428e0a0241a589080b875e53e44a, call_7f6c15b99df647adbd232baeffe75e13

source_inspection: Inspected all literal load_gen call sites: Model.load forwards arguments; both examples use autosplit rather than explicit-device loading. [call_516db9b5274140018135a08f23b2feeb, call_c325f437378f48adbce05973a20619ba, call_7f6c15b99df647adbd232baeffe75e13]. Limits: No runtime progress test.

## Uncertainty and limits

No repository loading implementation or GPU kernel was executed; throughput, peak memory and CUDA ordering remain unmeasured.

The scalar check models chunk arithmetic and bit interpretation only, not native conversion or zero-block launch behavior.

No affected odd-sized BF16 checkpoint was demonstrated. Literal caller searches do not establish external or dynamically dispatched usage.
