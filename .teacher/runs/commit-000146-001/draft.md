# 9c31971b844ffea3b077d5157225565877679171


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/9c31971b844ffea3b077d5157225565877679171) · [Evidence ledger](draft.json)

Adds whole-page token capacity for oversized-job diagnostics and revises two annotations; the UTF-32 helper's empty-result annotation remains inaccurate.

- [Restore capacity diagnostics and refine annotations](#generation)

## Problem

Oversized-job rejection referenced Generator.max_total_tokens without initializing it, allowing an AttributeError to mask the intended capacity assertion. [source; call_bff99b28b85444259d6b99f4ee6b4e9f, call_5e710b90bf8848e6895943abaa44b439, call_2c2c469fd6e9415cb0e4af3f8bf7b0b7]

## Reasoning

Initializing the attribute from PageTable.max_pages supplies the existing diagnostic with usable whole-page capacity without changing its admission predicate. [source; call_5baa4c4da0eb4167924be38825711a88, call_0e921a2ea6064e898636ba6419c7532c, call_5e710b90bf8848e6895943abaa44b439]

## Impact

A scalar reproduction of the failing assertion changed AttributeError into the intended AssertionError after supplying the attribute. [execution; call_12f46200a6ce481ea766e99fb0bd163d]

## Source Notes

PR #36 author tokoba reported encountering the missing attribute in TabbyAPI, adding it, and successfully trying the build. This is the contributor's report, not an independent integration test. Turboderp subsequently indicated approval and planned merging into dev. [source; call_3776b6f2d95649ed9d4f70911263b61a, call_f6bb56ca0be84329a77b8cc9d2b0e431]

The reported traceback's max_total_tokens formatting expression matches the repository's oversized-job diagnostic, supporting a connection to that path rather than establishing a separate TabbyAPI-side defect. [inference; call_3776b6f2d95649ed9d4f70911263b61a, call_5e710b90bf8848e6895943abaa44b439]

Closed issue #33, “Error converting model,” concerns file opening during conversion and ultimately reports “Too many open files”; it supplies no evidence of the generator-capacity failure. [source; call_a836d124582f40cf9641da4b8b685866, call_34592ff5d542429696a75f2361569447]

<a id="generation"></a>

## Restore capacity diagnostics and refine annotations

Generator.enqueue calls Job.prepare_for_queue before appending a job. Its capacity assertion formats max_total_tokens only on rejection; adding the attribute repairs this error-reporting path, not cache allocation or scheduling. [source; call_193c64dafd5e4b03babe85f0e2437fc1, call_5e710b90bf8848e6895943abaa44b439, call_5baa4c4da0eb4167924be38825711a88]

PAGE_SIZE is 256 tokens. PageTable computes max_pages as cache.max_num_tokens // PAGE_SIZE, so the new product expresses whole-page capacity, not currently free tokens or a generation budget. [source; call_42675c1b0ba0443eba75592c823ba5de, call_0e921a2ea6064e898636ba6419c7532c, call_5baa4c4da0eb4167924be38825711a88]

Scalar arithmetic yielded capacities of 256, 256, 256 and 512 for hypothetical cache sizes of 256, 257, 511 and 512 tokens, respectively, illustrating the page rounding. [execution; call_12f46200a6ce481ea766e99fb0bd163d]

The seed annotation changes from int or None to int | None while preserving its None default. The UTF-32 helper now declares tuple[np.ndarray, np.ndarray] | None. Neither edit changes runtime assertions or return statements. [source; call_5baa4c4da0eb4167924be38825711a88, call_96ef90c32a984439a3b53e5dcc2470aa]

For nonempty input, _strings_to_utf32 concatenates UTF-32 little-endian bytes and constructs cumulative byte offsets, exposing both buffers as uint8 NumPy arrays. Job construction unpacks these for stop strings and banned strings, so the revised annotation better describes the nonempty result. [source; call_d58c1b3dee9f4f0db6fb8018912c84bd, call_b04875b7957b4fd0b1b5cc8bfc28994e]

The second-parent explanation already identified an empty-input annotation mismatch. Inspection of the merge diff and unchanged helper body shows that mismatch is carried over. [source; call_0394cce521384257b3bc343fba75ba19, call_96ef90c32a984439a3b53e5dcc2470aa, call_d58c1b3dee9f4f0db6fb8018912c84bd]

## Authoring-time findings — pending review

### empty-utf32-annotation (suspected; defect)

The revised helper annotation excludes its unchanged empty-input return value.

Trigger: _strings_to_utf32([]), including Job construction with non-None stop_conditions containing no strings.

Expected: The declared return type should include the empty-input pair, or the implementation should return a matching value.

Actual: The helper returns (bytearray(), None), neither a pair of ndarrays nor standalone None. This is a typing mismatch, not an established runtime regression.

Locations: 9c31971b844ffea3b077d5157225565877679171:exllamav3/generator/job.py — _strings_to_utf32

Source evidence: call_96ef90c32a984439a3b53e5dcc2470aa, call_d58c1b3dee9f4f0db6fb8018912c84bd, call_34c4b4104d3c421f91e24c5d225f7b3e

source_inspection: Whole-parent-tree search found two direct callers in Job.__init__. Stop-condition processing can pass an empty list; banned-string processing is truthiness-guarded. Both callers unpack the pair, and the task changes only the helper annotation. [call_343895f38bc4458e89cba949c3aeca18, call_34c4b4104d3c421f91e24c5d225f7b3e, call_b04875b7957b4fd0b1b5cc8bfc28994e, call_96ef90c32a984439a3b53e5dcc2470aa]. Limits: No static-checker or repository execution result; external callers remain unexamined.

## Uncertainty and limits

The scalar check did not instantiate Generator or run repository generation, NumPy conversion, CUDA, or TabbyAPI.

No static type checker was run; external callers of the UTF-32 helper were not inspected.
