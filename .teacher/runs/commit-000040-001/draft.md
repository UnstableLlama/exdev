# 4c7b1e29485c7004a59be08ae8d88ebd239e36d1


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4c7b1e29485c7004a59be08ae8d88ebd239e36d1) · [Evidence ledger](draft.json)

Adds default Rich Markdown streaming with a basic-console alternative, preserving raw response history but leaving --mli ineffective on the default input path.

- [Markdown presentation for streamed chat responses](#usage-evaluation)

## Problem

The example chatbot previously printed generated chunks directly, without interpreting Markdown. [source; call_4b650460f259471da5e1a81422779254]

## Reasoning

The change separates input and response presentation from generation, selecting paired console or Rich implementations while retaining the existing Job-based inference loop. [source; call_bf5a8b056732415998818319ec64eccd]

## Impact

Markdown becomes the default presentation. --basic_console restores direct printing; --refresh_per_second defaults to 25 and is passed to Rich Live, rather than controlling token generation. [source; call_bf5a8b056732415998818319ec64eccd]

## Source Notes

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports failure at chat.py's Job construction. Its relationship here is inferred from that shared call site, not an explicit commit reference: this patch changes presentation, not stop-condition selection. [inference; call_0af6634a3f824e60b78221cf16f6ba88, call_4b650460f259471da5e1a81422779254, call_bf5a8b056732415998818319ec64eccd]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns native-extension loading and reports a toolchain-environment workaround; it supplies no Markdown-rendering evidence. [source; call_4efb501dc19d40d592ab66ce822c5459]

<a id="usage-evaluation"></a>

## Markdown presentation for streamed chat responses

The earlier usage entry describes chat.py as a template-driven, history-retokenizing Job client. This patch adds a presentation layer to that existing interface. [ancestor; call_3358b7a469404033b597143373bb81ae]

Streamer_rich starts a Live context with vertical_overflow='visible', prefixes the bot name, and constructs Markdown from the entire accumulated display string on every chunk. Rebuilding the document allows markup spanning chunks to be interpreted together, at the cost of repeatedly processing an expanding response. [inference; call_bf5a8b056732415998818319ec64eccd]

Both streamers preserve unmodified chunks in all_text and remove only one initial space from display output. History receives all_text.strip(), not the rendered Markdown or bot-name prefix. The basic streamer retains direct flushed printing and supplies a final newline when needed. [source; call_bf5a8b056732415998818319ec64eccd]

A bounded scalar transcription matched the previous and new raw-text, displayed-text and stripped-history accumulation for 343 three-chunk sequences, including empty chunks, spaces, newlines and Markdown text. [execution; call_a1d91f517534402cbbabef077bb7e201]

The max_new_tokens warning is deferred until after the streamer context exits, keeping it outside the live response display. The default response limit remains 1000 tokens. [source; call_bf5a8b056732415998818319ec64eccd, call_4b650460f259471da5e1a81422779254]

Rich imports are unconditional: selecting basic mode changes presentation but does not bypass importing Prompt, Live and Markdown. [source; call_bf5a8b056732415998818319ec64eccd]

## Authoring-time findings — pending review

### markdown-multiline-input (suspected; behavior_change)

The existing --mli option is ignored by the newly default Rich input path.

Trigger: Run the chatbot with --mli without --basic_console and reach user input.

Expected: The advertised multiline option selects the existing stdin-to-EOF input behavior.

Actual: main selects read_input_rich, which calls Prompt.ask without consulting args.mli. Only read_input_console retains sys.stdin.read().

Locations: 4c7b1e29485c7004a59be08ae8d88ebd239e36d1:examples/chat.py — read_input_rich

Source evidence: call_bf5a8b056732415998818319ec64eccd, call_4b650460f259471da5e1a81422779254, call_d06bd4bef77d45bc9738cb15d4614402

source_inspection: The parent-tree search finds no read_input_rich because it is newly introduced. The diff shows its direct caller through main's read_input_fn selection and the script's main(_args) entry point. The observed reach is this chatbot input loop; --basic_console preserves the previous multiline branch. [call_d06bd4bef77d45bc9738cb15d4614402, call_bf5a8b056732415998818319ec64eccd, call_4b650460f259471da5e1a81422779254]. Limits: No interactive input session or Rich library implementation was executed.

## Uncertainty and limits

No interactive terminal, Rich rendering, model inference or GPU execution was tested. Actual refresh timing and terminal compatibility remain unestablished.

The scalar check covers string accumulation only; it does not execute either streamer implementation or Rich.
