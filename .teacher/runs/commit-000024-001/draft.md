# 72e88aef02ac18ef080f3cc084bac6109553d322


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/72e88aef02ac18ef080f3cc084bac6109553d322) · [Evidence ledger](draft.json)

Adds selectable multi-GPU tile quantization using cached streams, scratch buffers and pinned-host staging while retaining first-device LDLQ feedback. A scalar check identifies premature scale-search progress completion; GPU behavior and speedup were not tested.

- [Distribute tile quantization while retaining first-device feedback](#quantizer)

## Problem

Conversion previously selected cuda:0 unconditionally, and LDLQ quantized each tile batch on one device. The change exposes device selection and distributes tile quantization across the selected GPUs. [source; call_1d87ab6a29d24c44b6b1e5e81a55e8f3, call_ba2ac6b3cb6449cebe5b500bfc055e3e]

## Reasoning

Parallelism is confined to independent tiles within a quantization call: LDLQ's reverse-row error feedback remains sequential on the first device. This avoids distributing its dependency-bearing matrix updates. [source; call_ba2ac6b3cb6449cebe5b500bfc055e3e]

## Impact

The default remains device 0. Multiple devices add pinned-host transfers and per-device scratch storage, so the source establishes a parallel execution design, not a measured speedup or reduced primary-device memory requirement. [inference; call_1d87ab6a29d24c44b6b1e5e81a55e8f3, call_ba2ac6b3cb6449cebe5b500bfc055e3e]

<a id="quantizer"></a>

## Distribute tile quantization while retaining first-device feedback

--devices accepts comma-separated integer IDs, defaults to "0", and is added to the resumable argument override list. main selects its first entry for module loading and passes the whole list through Linear.convert_exl3's quant_args. Because the parser supplies a non-None default, resuming without an explicit selection can override a previously stored device list with "0". [source; call_1d87ab6a29d24c44b6b1e5e81a55e8f3, call_cb646eadf9ae4c9abf49ffa87a4ab2b7]

quantize_tiles_multigpu preserves the direct quantize_tiles path for a single device. Otherwise it copies contiguous input tiles from the first device to reusable pinned CPU storage, divides the leading tile dimension evenly, and assigns the entire remainder to the last device. Each device receives a contiguous slice and returns reconstructed float tiles plus int16 indices to corresponding pinned slices. [source; call_ba2ac6b3cb6449cebe5b500bfc055e3e]

A cached stream per device and explicit events order the host-staged pipeline: secondary streams wait for the input copy; each records completion after copying its outputs back; the first stream waits for all slice events before gathering full results onto the first device. Both LDLQ and scale search run their dependent operations within that first stream after synchronizing selected devices on entry; LDLQ also synchronizes before returning. [source; call_ba2ac6b3cb6449cebe5b500bfc055e3e]

LDLQ still forms compensated 16-by-16 tiles, hence 256 values per tile, applies the tensor-core permutation, and reverses that permutation only for reconstructed weights. Encoded indices retain tensor-core order. The distributed call replaces the tile quantizer without changing this representation contract or the subsequent error-cache update. [source; call_1a3aeae02ded47c1b07d93ba130e7e9d, call_ba2ac6b3cb6449cebe5b500bfc055e3e]

get_temp_buffers caches scratch allocations by device and bitrate K rather than allocating them on every call. It retains the existing 128-batch allocation with costs shaped (128, 2, 65536 >> K) and edges shaped (128, 256, 65536 >> K). Pinned input, reconstructed output and index buffers grow to the largest requested tile count and are reused. [source; call_ba2ac6b3cb6449cebe5b500bfc055e3e]

A scalar calculation gives 272,629,760 scratch bytes at K=4 using four-byte costs and two-byte edges. Split examples preserve the tile count but put unequal extra work on the last device: 128 tiles across three devices becomes [42, 42, 44], while eight tiles across ten becomes nine empty slices followed by eight tiles. [execution; call_a03d362ceadb4669bf8bd60647ee22f4]

The added quantize_tiles_multigpu_sync supplies a more explicitly synchronized alternative using device transfers and concatenation. The inspected task call sites instead choose the pinned-memory implementation. Its host staging trades additional copies and persistent host storage for an event-ordered multi-device path. [inference; call_ba2ac6b3cb6449cebe5b500bfc055e3e]

Global-scale search now distributes its sampled-tile objective through the same helper. Its objective remains mean squared reconstruction error after undoing the trial scale, and its unchanged [0.1, 1.9] interval and 0.01 stopping tolerance govern scale search rather than quantization bitrate. Separately, block_rms, block_rms_n and block_nmse double their default reduction chunk size from 16 to 32 without changing their formulas. [source; call_1a3aeae02ded47c1b07d93ba130e7e9d, call_ba2ac6b3cb6449cebe5b500bfc055e3e]

## Authoring-time findings — pending review

### scale-progress-premature-completion (suspected; defect)

The new scale-search progress expression reports completion on every iteration, including the first.

Trigger: g_scale_gss performs its first interval contraction with a visible ProgressBar.

Expected: Progress should distinguish an intermediate interval contraction from search completion.

Actual: The contracted-width ratio is between zero and one, so int(delta2 / delta1) is zero and the reported value is 100. Search continues despite the completion display.

Locations: 72e88aef02ac18ef080f3cc084bac6109553d322:exllamav3/modules/quant/exl3_lib/quantize.py — g_scale_gss

Source evidence: call_ba2ac6b3cb6449cebe5b500bfc055e3e, call_f323b2bb276b4097a5c0b7e9c1422194, call_47b4b00cb40747668c60c24076075880, call_1a3aeae02ded47c1b07d93ba130e7e9d

source_inspection: Parent-tree caller search found quantize_exl3 supplying its ProgressBar to g_scale_gss. ProgressBar.update treats the supplied number as completed work. Conversion supplies a visible progress string, so this reaches normal conversion scaling feedback; it does not change the search objective. [call_47b4b00cb40747668c60c24076075880, call_1a3aeae02ded47c1b07d93ba130e7e9d, call_f323b2bb276b4097a5c0b7e9c1422194, call_cb646eadf9ae4c9abf49ffa87a4ab2b7]. Limits: No terminal rendering or conversion was executed.

scalar_transcription: Modeled golden-section width contraction from 1.8 to below 0.01: all eleven progress updates were 100, with final width approximately 0.009045. [call_a03d362ceadb4669bf8bd60647ee22f4]. Limits: Standard-library scalar arithmetic, not repository or GPU execution.

## Uncertainty and limits

No CUDA kernels or end-to-end conversion were executed. Stream ordering, transfer overlap, numerical equivalence and performance remain unmeasured.

Scalar checks model split arithmetic, scratch sizes and golden-section interval contraction only; they do not execute PyTorch or establish GPU floating-point behavior.

Native handling of empty tile slices, possible when devices outnumber tiles, was not inspected.
