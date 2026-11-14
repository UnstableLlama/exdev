# fc5b39c2bb56be8654db7f4a6a7fd4f56a1db0ca


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/fc5b39c2bb56be8654db7f4a6a7fd4f56a1db0ca) · [Evidence ledger](draft.json)

Limits Markdown redraw suffixes to the console height captured at construction, leaving full rendering and conversation storage unchanged.

- [Bound Markdown redraws to console height](#usage-evaluation)

## Problem

Markdown updates previously rewound and redrew the entire changed suffix, even when it exceeded the console height. [source; call_c3515b8b31f047ee8324747270057d8e, call_ca6dcbe50ebb4936a444b383447f0b9d]

## Reasoning

The change bounds redraw work by treating lines before the visible tail as preserved, even if their rendered contents changed. [source; call_ca6dcbe50ebb4936a444b383447f0b9d, call_c3515b8b31f047ee8324747270057d8e]

## Impact

This affects Rich Markdown answer display, not basic streaming or generated conversation text. Full Markdown rendering and storage of the complete rendered line list remain unchanged. [source; call_ca6dcbe50ebb4936a444b383447f0b9d, call_c3515b8b31f047ee8324747270057d8e, call_d4382505426e454fab0280a2f42e2860]

## Source Notes

The earlier blank-line normalization entry records reasoning-boundary answer loss. [ancestor; call_92f24f778d1240bca4c774dd04f4eef0]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns quantization quality. Neither supplies evidence of terminal redraw behavior. [source; call_ecc5a58b86004c7cbf38569ec806b3da, call_43d5839833614daa90701ab48c436b0c]

<a id="usage-evaluation"></a>

## Bound Markdown redraws to console height

Construction now stores width and height from self.console.size. The existing two-column width reduction is documented as protection against extra-wide emojis; the new redraw limit uses height, not the stored width. [source; call_ca6dcbe50ebb4936a444b383447f0b9d, call_c3515b8b31f047ee8324747270057d8e]

After rendering and finding the common prefix p, update replaces p with max(p, old_line_count − height, new_line_count − height). Both suffix lengths therefore have an upper bound of height. Existing cursor-up, line clearing and printing operate on those shortened suffixes. [source; call_ca6dcbe50ebb4936a444b383447f0b9d, call_c3515b8b31f047ee8324747270057d8e]

A scalar transcription checked 178,608 combinations of height, line counts and endpoint prefix lengths. For 30 old lines, 31 new lines, no common prefix and height 24, the new prefix is 7, yielding 23 old and 24 new suffix lines. For an initial 30-line update at height 24, only the last 24 lines are selected. [execution; call_14758fd286de4ea3901a4f9d4573fc54]

The tradeoff is bounded terminal rewriting rather than complete historical display correction: changes above the selected tail are not printed. This is consistent with avoiding attempts to rewrite content outside the redrawable console area, but does not establish correct behavior on every terminal. [inference; call_ca6dcbe50ebb4936a444b383447f0b9d, call_c3515b8b31f047ee8324747270057d8e]

## Authoring-time findings — pending review

### inherited-reasoning-boundary-answer-loss (suspected; defect)

The previously noted reasoning-boundary answer loss is carried over unchanged.

Trigger: Rich reasoning mode receives a chunk containing the closing reasoning tag followed by answer text.

Expected: The answer suffix enters the Markdown answer and saved conversation response.

Actual: Streamer_rich.stream adds the whole chunk to think_text and calls begin without transferring the answer suffix to all_text; main subsequently saves all_text.strip().

Locations: fc5b39c2bb56be8654db7f4a6a7fd4f56a1db0ca:examples/chat_console.py — Streamer_rich.stream

Source evidence: call_c3515b8b31f047ee8324747270057d8e, call_d4382505426e454fab0280a2f42e2860, call_ca6dcbe50ebb4936a444b383447f0b9d

source_inspection: Whole-parent-tree .stream( search located the chat main call. Its Rich selection and response storage were inspected alongside the complete task diff, which changes only dimension capture and redraw-prefix calculation. [call_3be51e330c564013b84dbb86e4256ebe, call_d4382505426e454fab0280a2f42e2860, call_c3515b8b31f047ee8324747270057d8e, call_ca6dcbe50ebb4936a444b383447f0b9d]. Limits: Applies to Rich reasoning mode with the specified chunk boundary; no generator or streamer execution was performed.

## Uncertainty and limits

No Rich rendering or interactive terminal execution was performed; cursor positioning, scrolling and resize behavior remain unverified.

Console dimensions are captured at construction and not refreshed by update.

Caller coverage is limited to literal repository searches, not dynamic or external callers.
