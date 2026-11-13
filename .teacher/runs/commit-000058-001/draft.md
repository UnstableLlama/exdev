# 3129b748ff0f61ef43e8176805b9ea87862feaa4


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3129b748ff0f61ef43e8176805b9ea87862feaa4) · [Evidence ledger](draft.json)

Adds shared prompt_toolkit multiline input and opt-in reasoning presentation, with a chunk-boundary risk that can omit answer text from history.

- [Multiline input and simple reasoning presentation](#usage-evaluation)

## Problem

The default Rich input path did not consult the multiline flag, and response presentation had no separate handling for <think> reasoning. [source; call_4d5e65bc840d41fa896b9b07c915d6e1]

## Reasoning

The change unifies input through prompt_toolkit while retaining separate basic and Markdown output paths. Reasoning mode appends <think> to the formatted prompt and delays Markdown rendering until </think> appears. [source; call_d4490acea4c042d5ade4324241b0649d]

## Impact

requirements_examples.txt adds prompt_toolkit, matching the new unconditional imports in chat.py. The whole-parent search found no existing literal prompt_toolkit references; it does not exclude dynamic imports or external users. [source; call_99e310fc72644f95a38b1cb24be47451, call_a130e82cfe274fad945759561a333241, call_d4490acea4c042d5ade4324241b0649d]

The parser now declares --multiline instead of --mli, retaining -mli. Both output modes use prompt_toolkit input, so basic mode no longer selects the old stdin reader. [source; call_d4490acea4c042d5ade4324241b0649d]

## Source Notes

The earlier Markdown entry records the default input path ignoring --mli. [ancestor; call_0a2d8351472549599405b6097932484b]

That active-path omission is removed: both branches now select read_input_ptk, which passes args.multiline to prompt(). The old readers remain defined but are no longer selected by main. [source; call_4d5e65bc840d41fa896b9b07c915d6e1, call_d4490acea4c042d5ade4324241b0649d]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports native-extension loading failure and an environment workaround, not multiline input or reasoning presentation. [source; call_9f7b151d5bc045ec9e4bf4d94880000b]

<a id="usage-evaluation"></a>

## Multiline input and simple reasoning presentation

read_input_ptk wraps the colored user label in ANSI and forwards the store_true multiline option, which defaults to false. This replaces both the stdin-based reader and Prompt.ask in main's dispatch. [source; call_d4490acea4c042d5ade4324241b0649d, call_4d5e65bc840d41fa896b9b07c915d6e1]

get_input_ids appends <think> after template formatting and before tokenization, including when context is re-tokenized during trimming. This is prompt conditioning, not a change to sampling or the model. [source; call_d4490acea4c042d5ade4324241b0649d, call_4d5e65bc840d41fa896b9b07c915d6e1]

With --think, Streamer_rich initially prints a magenta Thinking label and accumulates flushed plain text in think_text. It searches that accumulated string for </think>, allowing detection across chunks, then starts Live. Subsequent chunks populate all_text and the Markdown display; history stores all_text.strip(), excluding the thinking buffer. [source; call_d4490acea4c042d5ade4324241b0649d]

Without --think, Rich begins immediately as before. Live retains a default refresh limit of 25 updates per second, not a token-generation limit. Basic output does not implement the reasoning split: it prints and retains every generated chunk even when the prompt receives <think>. [source; call_d4490acea4c042d5ade4324241b0649d, call_4d5e65bc840d41fa896b9b07c915d6e1]

The implementation favors a small delimiter-driven presentation state machine over structured reasoning parsing. It requires a closing delimiter to enter answer rendering and treats the entire delimiter-containing chunk as thinking. [inference; call_d4490acea4c042d5ade4324241b0649d]

A scalar transcription retained Answer when it arrived after a delimiter-only chunk, but produced empty history when Answer shared the closing-delimiter chunk, including when the delimiter itself spanned chunks. A stream without a closing delimiter also left history empty. [execution; call_39ef3ddd916f4821ac1e4576911fcb19]

## Authoring-time findings — pending review

### reasoning-boundary-answer-loss (suspected; defect)

Answer text sharing the closing-reasoning chunk is omitted from answer history.

Trigger: Use Rich output with --think and receive a chunk containing </think> followed by answer text.

Expected: Text after the closing delimiter enters the Markdown answer and saved conversation response.

Actual: stream prints and stores the entire chunk in think_text, then begins Live without transferring its suffix. Only later chunks enter all_text, which main uses for history.

Locations: 3129b748ff0f61ef43e8176805b9ea87862feaa4:examples/chat.py — Streamer_rich.stream

Source evidence: call_d4490acea4c042d5ade4324241b0649d, call_4d5e65bc840d41fa896b9b07c915d6e1, call_3ca1b848e91c498aae29bf6d04bdbc5d

source_inspection: The whole-parent .stream( search identifies main's s.stream(chunk) as the chatbot call site. Main supplies generator result text and saves s.all_text.strip(); the diff selects Streamer_rich only outside basic mode. [call_3ca1b848e91c498aae29bf6d04bdbc5d, call_4d5e65bc840d41fa896b9b07c915d6e1, call_d4490acea4c042d5ade4324241b0649d]. Limits: Literal call-site search does not establish external or dynamically dispatched callers.

scalar_transcription: Modeled the inspected accumulation and delimiter transition with separate and combined delimiter/answer chunks; combined chunks lost Answer from history. [call_39ef3ddd916f4821ac1e4576911fcb19]. Limits: Standard-library string model only; no repository streamer, terminal or generator execution.

## Uncertainty and limits

No interactive terminal, prompt_toolkit key bindings, Rich rendering or model inference was executed. Alt+Enter submission is advertised by the parser but not independently verified.

The bounded Python check models string routing only; it does not execute Streamer_rich or establish which chunk boundaries a model will produce.
