# 4d0e5d3d5d10ed73ecde67d587bdc42c26c19cc0


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4d0e5d3d5d10ed73ecde67d587bdc42c26c19cc0) · [Evidence ledger](draft.json)

Adds a selectable Ernie chat template with fixed role labels, sentence markers and token-ID stops, reusing the existing chat pipeline.

- [Ernie formatting through the existing chat interface](#usage-evaluation)

## Problem

The example chat template registry lacked an Ernie option; this change adds prompt formatting rather than model architecture support. [source; call_f1627f7bb2164a6a92212a9c748e462b, call_dad1c0c78c1f47bda1035f8cd3188f3b]

## Reasoning

Registering 'ernie' lets the existing chat loop select the formatter, encode conversation history and pass its stop conditions to generation without changing chat.py. [source; call_f1627f7bb2164a6a92212a9c748e462b, call_ec1be329b0cb40b99ef0f4eae780cd4a]

## Impact

Users can select --mode ernie. Existing registry entries remain unchanged. [source; call_f1627f7bb2164a6a92212a9c748e462b, call_ec1be329b0cb40b99ef0f4eae780cd4a]

## Source Notes

The earlier Dots entry was read: it establishes the preceding template's optional-system and completed-versus-pending-turn pattern and its integration through the same registry. [ancestor; call_dcc0d0593b3848a29ac32f235297c66b]

Existing single_id callers in chat templates and examples/common.py use direct marker lookups; Gemma3 and Mistral3 image code likewise consumes lookup results without local missing-token guards. The new Ernie lookup follows that convention rather than adding validation. [source; call_7e2fc5e927574e3bb87e4d36e5fce05c, call_17e61b8bec1a4c289156072e279a7097, call_f1627f7bb2164a6a92212a9c748e462b]

Issue #48, '`RuntimeError` when requesting logprobs with Gemma 3 models', reports a logits-dimension mismatch. Its overlap with the inspected Gemma3 caller is only a shared file, not evidence connecting that failure to Ernie formatting. [inference; call_782f5147d833415fb248b35088c3f8f9, call_17e61b8bec1a4c289156072e279a7097, call_f1627f7bb2164a6a92212a9c748e462b]

<a id="usage-evaluation"></a>

## Ernie formatting through the existing chat interface

PromptFormat_ernie.format starts with <|begin_of_sentence|>, then appends a truthy system prompt followed by a newline. Its default system prompt is 'You are a helpful assistant.' Each conversation pair emits 'User: ', user text, a newline and 'Assistant: '. A non-None answer adds its text and <|end_of_sentence|>; None leaves the assistant prefix open. Completed turns receive no additional newline before the next 'User: '. [source; call_f1627f7bb2164a6a92212a9c748e462b]

The chat caller supplies exactly this pair structure: it appends (user_prompt, None), formats the context, then replaces that pair with the generated response. Custom user and bot names are stored by the base constructor but do not alter Ernie's fixed role labels. The new class inherits the base <think> and </think> tags. [source; call_ec1be329b0cb40b99ef0f4eae780cd4a, call_7e2fc5e927574e3bb87e4d36e5fce05c, call_f1627f7bb2164a6a92212a9c748e462b]

add_bos returns True. The caller also enables special-token encoding, and Tokenizer.encode prepends bos_token_id whenever it is non-None; it does not inspect whether the formatted text already begins with a BOS marker. [source; call_f1627f7bb2164a6a92212a9c748e462b, call_ec1be329b0cb40b99ef0f4eae780cd4a, call_a79694f88d524edd90f60c0f82c29165]

Stopping supplies the tokenizer EOS ID and single_id('<|end_of_sentence|>'). Unlike Dots, Ernie supplies no literal-string fallback. single_id searches extended and ordinary vocabulary dictionaries and can return None when neither contains the marker; successful exact-token lookup is therefore a tokenizer precondition. [source; call_f1627f7bb2164a6a92212a9c748e462b, call_7e2fc5e927574e3bb87e4d36e5fce05c, call_a79694f88d524edd90f60c0f82c29165]

A scalar transcription passed four assertions covering exact completed-plus-pending formatting, an empty completed answer, a pending answer and empty history. It confirms the modeled string concatenation, not tokenization or model behavior. [execution; call_0c1205c375444ede8b8d0127655223a2]

## Uncertainty and limits

No Ernie tokenizer or model was executed; checkpoint-template compatibility, generation quality and end-to-end stopping remain unverified.

The formatting check was a standard-library transcription, not execution of the added class or chat pipeline.

Whether the explicit beginning marker and requested added BOS produce duplicate checkpoint tokens was not established.
