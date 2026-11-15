# a61801d2785be4721ee948c60c26a41fecd2f261


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a61801d2785be4721ee948c60c26a41fecd2f261) · [Evidence ledger](draft.json)

Uses terminal rows minus two as the Markdown redraw budget, attempting to protect scrollback without changing rendering or answer accumulation.

- [Reserve terminal rows when redrawing Markdown](#usage-evaluation)

## Problem

The change attempts to improve Markdown scrollback by reducing the redraw height and taking it from the terminal rather than Rich's console dimensions. [source; call_9f8930b6db994285a6600e2a02fc2f30]

## Reasoning

Using terminal rows minus two leaves a two-row margin for redraws. This plausibly avoids rewinding into inaccessible scrollback, but the precise reason for choosing two rows is not documented. [inference; call_9f8930b6db994285a6600e2a02fc2f30, call_3d94a72f8af8407c9055d5009c249ba8]

## Impact

The change affects Markdown answer display through Streamer_rich; basic streaming, full Markdown rendering and accumulated answer text are unchanged. [source; call_9f8930b6db994285a6600e2a02fc2f30, call_3d94a72f8af8407c9055d5009c249ba8, call_159a3bec9f71498bbfbe497e409673b6]

## Source Notes

The preceding redraw entry describes the existing height-bounded suffix algorithm and records reasoning-boundary answer loss. [ancestor; call_6b3278d709bb45fd921000d398cd5c43]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading failure; issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” reports quantization quality problems. Neither provides terminal-redraw evidence. [source; call_a23adffd07f34339b186e74b50c0715a, call_651ce75d1e1746c4be341874ce7dfd62]

<a id="usage-evaluation"></a>

## Reserve terminal rows when redrawing Markdown

MarkdownConsoleStream now stores height = r - 2 from shutil.get_terminal_size(fallback=(80, 24)), rather than unpacking self.console.size. The fallback therefore gives a 22-row redraw budget. The separate two-column reduction for emoji overflow remains unchanged, and the unused self.width assignment disappears. [source; call_9f8930b6db994285a6600e2a02fc2f30, call_3d94a72f8af8407c9055d5009c249ba8]

update still renders the entire answer and computes prefix = max(common_prefix, old_count - height, new_count - height). Cursor movement, clearing and printing use the resulting suffixes; the complete new line list is retained. Even a supplied Console now uses the separately queried terminal row budget. [source; call_3d94a72f8af8407c9055d5009c249ba8, call_9f8930b6db994285a6600e2a02fc2f30]

A scalar transcription checked 357,216 combinations for the suffix-height bound. With 30 old lines, 31 new lines and no common prefix, changing height from 24 to 22 changes the preserved prefix from 7 to 9 and the old/new suffix lengths from 23/24 to 21/22. [execution; call_22f94c1aa7064e479a253dd387e21381]

The tradeoff is a smaller redraw region rather than more complete historical correction: changed lines above the selected tail remain unprinted. The margin may help scrolling, but it does not reduce full-answer rendering work. [inference; call_3d94a72f8af8407c9055d5009c249ba8, call_9f8930b6db994285a6600e2a02fc2f30]

## Authoring-time findings — pending review

### inherited-reasoning-boundary-answer-loss (suspected; defect)

The previously recorded reasoning-boundary answer loss remains unchanged.

Trigger: Rich reasoning mode receives a chunk containing the closing reasoning tag followed by answer text.

Expected: The answer suffix enters the Markdown answer and saved conversation response.

Actual: Streamer_rich.stream adds the whole chunk to think_text and calls begin without transferring the answer suffix into all_text. chat.main subsequently saves all_text.strip().

Locations: a61801d2785be4721ee948c60c26a41fecd2f261:examples/chat_console.py — Streamer_rich.stream

Source evidence: call_3d94a72f8af8407c9055d5009c249ba8, call_159a3bec9f71498bbfbe497e409673b6, call_9f8930b6db994285a6600e2a02fc2f30

source_inspection: Whole-parent-tree .stream( search located the direct chat.main call. Inspection of its streamer selection and response storage, alongside the complete task diff, establishes that this branch is carried over. [call_84428117392a48b395066960c363a41e, call_159a3bec9f71498bbfbe497e409673b6, call_3d94a72f8af8407c9055d5009c249ba8, call_9f8930b6db994285a6600e2a02fc2f30]. Limits: Reach is the inspected Rich reasoning workflow with the specified chunk boundary; dynamic or external callers and runtime reproduction were not established.

## Uncertainty and limits

No interactive terminal or Rich execution was performed; successful scrollback correction remains unverified.

Dimensions remain a construction-time snapshot, so terminal resizing is not accommodated by update.

The scalar check covers positive redraw heights only and does not model terminal cursor behavior.
