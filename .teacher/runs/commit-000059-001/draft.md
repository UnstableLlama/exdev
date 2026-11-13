# 872e698b8b7f5e41639022a78bc83a6e1614f0bb


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/872e698b8b7f5e41639022a78bc83a6e1614f0bb) · [Evidence ledger](draft.json)

Extracts chat console helpers and replaces Rich Live with rendered-line suffix updates; refresh-rate control becomes unused, and reasoning-boundary answer loss persists.

- [Console extraction and suffix-based Markdown streaming](#usage-evaluation)

## Problem

The previous Markdown streamer used Rich Live with visible vertical overflow. This change replaces that rendering mechanism while separating console helpers from the chat loop. [source; call_6ba487dd9cb34c8f88e82aecf1278437, call_e30c3319c1f446bbb33b8b3792e4fa57]

## Reasoning

Preserving unchanged rendered lines and rewriting only the suffix appears intended to reduce scrolling disruption. This supports the commit's reported motivation, but does not establish terminal correctness. [inference; call_e30c3319c1f446bbb33b8b3792e4fa57]

## Impact

Markdown output now updates synchronously on each streamed chunk. The unchanged --refresh_per_second option still advertises a default of 25, but the replacement renderer does not consume it. Basic output and prompt_toolkit input remain available. [source; call_93c7a45a88cc48b782d6ec7c7ed945ae, call_6ba487dd9cb34c8f88e82aecf1278437, call_e30c3319c1f446bbb33b8b3792e4fa57]

## Source Notes

The parent annotation identifies answer loss when a closing reasoning delimiter shares a chunk with answer text. [ancestor; call_c39fa385048c461ea6db2892bdc47de9]

Inspection of the relocated Streamer_rich.stream shows that this boundary behavior is carried over, not repaired. [source; call_e30c3319c1f446bbb33b8b3792e4fa57, call_93c7a45a88cc48b782d6ec7c7ed945ae]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports native-extension loading failure and a reporter-supplied environment workaround, rather than Markdown scrolling. [source; call_dbad00d0d2ce46cda18d5fc5af7d0032]

<a id="usage-evaluation"></a>

## Console extraction and suffix-based Markdown streaming

chat.py imports the extracted console helpers and passes </think> explicitly to both stream implementations. The whole-parent .stream( search identifies main's s.stream(chunk) as the chatbot call site, and the diff updates it to satisfy the new required argument. Basic streaming ignores that argument. [source; call_e6fe0681753c47cb9efcd9b8ce23ccf0, call_6ba487dd9cb34c8f88e82aecf1278437, call_e30c3319c1f446bbb33b8b3792e4fa57]

MarkdownConsoleStream captures a complete Rich Markdown rendering and splits it on newline characters. update compares this with the previous line list, preserves their common prefix, moves upward by the old suffix length, then clears and prints replacement suffix lines. It stores the new line list for the next update. [source; call_e30c3319c1f446bbb33b8b3792e4fa57]

The renderer still reformats the full accumulated Markdown on every update; only terminal rewriting is suffix-limited. Unlike Live, its context-manager exit performs no rendering cleanup. Live remains imported but is no longer instantiated. [source; call_e30c3319c1f446bbb33b8b3792e4fa57]

Terminal dimensions fall back to 80 columns and 24 rows. The default Console uses the column count minus two, explicitly reserving space for extra-wide emojis, and requests text emoji variants. The row count is unused, and width is sampled only during construction. [source; call_e30c3319c1f446bbb33b8b3792e4fa57]

Both main input branches still select read_input_ptk. The extracted, unselected stdin reader now consults args.multiline rather than args.mli; this does not change main's selected input path. [source; call_93c7a45a88cc48b782d6ec7c7ed945ae, call_e30c3319c1f446bbb33b8b3792e4fa57]

A scalar transcription retained Answer when it followed a delimiter-only chunk, but produced empty history when Answer shared the delimiter-containing chunk, including a delimiter split across chunks. A separate suffix calculation found one preserved line and two replaced lines for ['a','b',''] changing to ['a','bc','']. [execution; call_4b333618cbbb4e98b470d15d75130d8b]

## Authoring-time findings — pending review

### reasoning-boundary-answer-loss (suspected; defect)

The relocated reasoning streamer retains the parent behavior that omits answer text sharing the closing-delimiter chunk from conversation history.

Trigger: Rich output with --think receives a chunk containing </think> followed by answer text.

Expected: The suffix after </think> enters the Markdown answer and saved response.

Actual: The entire chunk enters think_text; begin starts answer rendering without transferring the suffix. main saves only all_text.strip().

Locations: 872e698b8b7f5e41639022a78bc83a6e1614f0bb:examples/chat_console.py — Streamer_rich.stream

Source evidence: call_e30c3319c1f446bbb33b8b3792e4fa57, call_93c7a45a88cc48b782d6ec7c7ed945ae, call_6ba487dd9cb34c8f88e82aecf1278437

source_inspection: Inspected the moved implementation and main's generator-to-streamer-to-history flow. The whole-parent search identifies main as the literal chatbot stream caller; the issue concerns its Rich reasoning branch, not basic streaming. [call_e6fe0681753c47cb9efcd9b8ce23ccf0, call_93c7a45a88cc48b782d6ec7c7ed945ae, call_e30c3319c1f446bbb33b8b3792e4fa57]. Limits: No generator or external caller execution.

scalar_transcription: Modeled the inspected accumulation and transition logic for separate and combined delimiter/answer chunks. [call_4b333618cbbb4e98b470d15d75130d8b]. Limits: String model only; actual generated chunk boundaries and terminal rendering were not tested.

## Uncertainty and limits

No interactive terminal, Rich rendering, scrolling, resizing, or model inference was executed; the claimed scrolling improvement remains unverified.

The standard-library checks model string routing and suffix arithmetic, not repository streamer execution or ANSI terminal behavior.

Literal whole-tree caller searches do not establish compatibility for external callers or dynamically constructed calls.
