# addeaaaaa76f5d9f9fc28d7d3b9125244235173d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/addeaaaaa76f5d9f9fc28d7d3b9125244235173d) · [Evidence ledger](draft.json)

Normalize captured Markdown lines to suppress consecutive blanks before suffix-based display updates, without changing saved response text.

- [Collapse consecutive blank Markdown display lines](#usage-evaluation)

## Problem

The Markdown streamer previously split captured output directly on newlines, retaining repeated blank lines and a trailing empty element. [source; call_e7bd2ed06ba3473da7d3d94a257c47c5]

## Reasoning

Normalizing rendered lines before prefix comparison makes blank-line suppression part of the streamer's stored display state, rather than modifying generated response text. [source; call_e7bd2ed06ba3473da7d3d94a257c47c5, call_3a6071c7d79e4acab96eada108f6ecac]

## Impact

The change affects Markdown answer rendering. Basic output, directly printed reasoning text, and accumulated conversation text are unchanged. [source; call_e7bd2ed06ba3473da7d3d94a257c47c5, call_3a6071c7d79e4acab96eada108f6ecac, call_0bb771f4ac614aa3a8ad7cf3b522465d]

## Source Notes

The preceding entry records reasoning-boundary answer loss in Streamer_rich.stream. [ancestor; call_78fac77dacd84a5ab3348c098577057e]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports native-extension import failure and a reporter-supplied environment workaround, not blank-line rendering. [source; call_690607ebe1c64bf3bb5b4d0463115adb]

<a id="usage-evaluation"></a>

## Collapse consecutive blank Markdown display lines

_render_to_lines still captures a complete Rich Markdown rendering. It now removes terminal newline characters, splits the result, and strips trailing whitespace from each line. A line is retained if nonempty, first, or preceded by a nonempty retained line, so each run of empty strings contributes at most one line. [source; call_e7bd2ed06ba3473da7d3d94a257c47c5, call_3a6071c7d79e4acab96eada108f6ecac]

update compares the normalized list with _last_lines, preserves their common prefix, and clears and rewrites the changed suffix. Trailing whitespace previously stripped only when printing is now also absent from comparison state. Full Markdown rendering still occurs on every update. [source; call_3a6071c7d79e4acab96eada108f6ecac, call_e7bd2ed06ba3473da7d3d94a257c47c5]

The display-level approach preserves generated text but applies equally to every rendered region; it does not distinguish intentional spacing in code blocks from other blank lines. [source; call_e7bd2ed06ba3473da7d3d94a257c47c5, call_3a6071c7d79e4acab96eada108f6ecac]

A scalar transcription produced ['a', '', ' b'] from 'a\n\n\n b  \n\n' and found no adjacent empty strings across 1,093 generated cases. Empty input still yields ['']; a trailing whitespace-only line can leave one blank line. ANSI reset-only lines remain nonempty. [execution; call_1791fb2bd0b849efa4458eda7bc396a6]

## Authoring-time findings — pending review

### inherited-reasoning-boundary-answer-loss (suspected; defect)

The existing reasoning-boundary answer loss is carried over; this patch changes only rendered-line normalization.

Trigger: Rich reasoning mode receives a chunk containing </think> followed by answer text.

Expected: The suffix after the delimiter enters the Markdown answer and saved conversation response.

Actual: Streamer_rich.stream appends the entire chunk to think_text and calls begin without transferring the answer suffix. main saves all_text.strip(), which lacks that suffix.

Locations: addeaaaaa76f5d9f9fc28d7d3b9125244235173d:examples/chat_console.py — Streamer_rich.stream

Source evidence: call_3a6071c7d79e4acab96eada108f6ecac, call_0bb771f4ac614aa3a8ad7cf3b522465d, call_e7bd2ed06ba3473da7d3d94a257c47c5

source_inspection: Compared the parent implementation and complete task diff. Whole-tree .stream( search identifies main's s.stream(chunk, thinktag[1]) as the chatbot call site; inspection follows it through Rich selection and response storage. The finding concerns Rich reasoning mode, not basic streaming. [call_e45aa6731f6f4df0a4e4a6eeacadc2bf, call_0bb771f4ac614aa3a8ad7cf3b522465d, call_3a6071c7d79e4acab96eada108f6ecac, call_e7bd2ed06ba3473da7d3d94a257c47c5]. Limits: No generator or streamer execution; actual generated chunk boundaries were not tested.

## Uncertainty and limits

No Rich rendering or interactive terminal behavior was executed; the computation transcribed only the string-normalization loop.

Blankness is determined by Python string whitespace stripping, not terminal appearance; ANSI-only lines are not collapsed.

The caller search covers literal repository calls, not dynamically constructed or external callers.
