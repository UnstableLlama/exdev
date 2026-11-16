# 809b0dab40c5f576bd84e38b0712cc5c3011f21e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/809b0dab40c5f576bd84e38b0712cc5c3011f21e) · [Evidence ledger](draft.json)

Initializes whole-page cache capacity for oversized-job diagnostics and revises two annotations; the UTF-32 helper's empty-result annotation remains inaccurate.

- [Restore cache-capacity diagnostics and adjust annotations](#generation)

## Problem

Oversized jobs could fail while formatting their rejection message: Job.prepare_for_queue referenced generator.max_total_tokens, but Generator did not initialize it. [source; call_42b655755b8d4256b947154afb276ab6, call_8a39a76bb7d84a88bcb11f33d706e4aa, call_4a4a6a4209b84d7bb0aed6b031e4e221]

## Reasoning

Initializing max_total_tokens immediately after PageTable construction supplies the existing diagnostic with capacity derived from the actual page count; it does not change the admission predicate. [source; call_a35f3d62e78c4642846b8e9825a75272, call_42b655755b8d4256b947154afb276ab6]

## Impact

The bounded scalar reproduction changed the oversized-request failure from AttributeError to the intended AssertionError after supplying the new attribute. [execution; call_9fdaf3443cae4b5aab3f2f633e8ab3be]

## Source Notes

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns conversion and tokenizer truncation. Its discussion does not establish a connection to this generator change. [source; call_c1b7c0c7379c460598cf412a370bbde3]

<a id="generation"></a>

## Restore cache-capacity diagnostics and adjust annotations

Generator.enqueue calls Job.prepare_for_queue before appending the job. When its page-capacity assertion fails, the message reads max_total_tokens. The new initialization repairs that diagnostic path without allocating additional cache or changing scheduling. [source; call_4a4a6a4209b84d7bb0aed6b031e4e221, call_42b655755b8d4256b947154afb276ab6, call_a35f3d62e78c4642846b8e9825a75272]

PAGE_SIZE is 256 tokens, and PageTable computes max_pages by integer-dividing cache.max_num_tokens by PAGE_SIZE. Thus the new attribute represents whole-page token capacity, not currently free space or a per-job output budget. [source; call_0886e02a1d464110b0e0281451a76f01, call_c162102c4581470183ab4474514aed3f, call_a35f3d62e78c4642846b8e9825a75272]

Scalar arithmetic confirmed capacities of 256 and 256 for hypothetical cache sizes of 256 and 257 tokens respectively, illustrating the whole-page rounding. [execution; call_9fdaf3443cae4b5aab3f2f633e8ab3be]

The seed annotation changes from int or None to int | None while retaining the None default. The UTF-32 helper annotation changes to tuple[np.ndarray, np.ndarray] | None. These edits change annotations, not runtime assertions or helper return statements. [source; call_a35f3d62e78c4642846b8e9825a75272, call_adc164e336ad47c8b77603995bfcfa15]

For nonempty input, _strings_to_utf32 concatenates UTF-32 little-endian bytes and builds cumulative byte offsets, exposing both as uint8 NumPy arrays. Job construction unpacks these buffers for stop strings and nonempty banned strings; the new annotation describes that nonempty result more accurately. [source; call_908683cc5c224485b57b095a58a45ab1, call_91851ebb5e2d4a51895013fb160c6ba6]

## Authoring-time findings — pending review

### empty-utf32-return-annotation (suspected; defect)

The revised return annotation still excludes the helper's empty-input result.

Trigger: Calling _strings_to_utf32([]), including Job construction with a non-None stop_conditions collection containing no strings.

Expected: The annotation should include the actual empty-input pair, or the implementation should return a value matching its declared type.

Actual: The unchanged branch returns (bytearray(), None), not a pair of ndarrays or standalone None. Existing callers unpack the pair, so this is an annotation mismatch rather than an established runtime regression.

Locations: 809b0dab40c5f576bd84e38b0712cc5c3011f21e:exllamav3/generator/job.py — _strings_to_utf32

Source evidence: call_adc164e336ad47c8b77603995bfcfa15, call_908683cc5c224485b57b095a58a45ab1, call_6956ace6837e4e5f8ee396e339965cb8, call_91851ebb5e2d4a51895013fb160c6ba6

source_inspection: Whole-parent-tree search found two direct calls, both in Job.__init__. The stop-condition path can pass an empty string list; the banned-string path is guarded by truthiness. The task changes only the helper annotation. [call_6956ace6837e4e5f8ee396e339965cb8, call_91851ebb5e2d4a51895013fb160c6ba6, call_adc164e336ad47c8b77603995bfcfa15]. Limits: No static-checker diagnostic or repository execution was obtained; external callers were not inspected.

## Uncertainty and limits

The scalar reproduction did not instantiate Generator or execute repository generation, NumPy conversion, or GPU code.

No static type checker was run.
