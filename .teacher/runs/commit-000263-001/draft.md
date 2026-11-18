# 0cdb4995491bec12f08549a0a9038a2ce5043568


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/0cdb4995491bec12f08549a0a9038a2ce5043568) · [Evidence ledger](draft.json)

Adds an explicitly selectable Dots chat template with role delimiters, response stops and reasoning tags, reusing the existing chat pipeline.

- [Dots chat formatting through the existing template interface](#usage-evaluation)

## Problem

The example chat registry lacked a Dots prompt format. This change adds a selectable template, not a model architecture implementation. [source; call_938e08549d50418bb986029feb6cea86]

## Reasoning

Registering 'dots' reuses the existing chat dispatch, conversation history, special-token encoding and generation loop instead of introducing a separate chat application. [source; call_938e08549d50418bb986029feb6cea86, call_4124e6c74f3d4ab4b13c40276cbdc4f2]

## Impact

Selecting --mode dots supplies Dots role delimiters, disables added BOS, and supplies response-ending stop conditions and Dots-specific reasoning tags. Existing template entries remain unchanged. [source; call_938e08549d50418bb986029feb6cea86, call_4124e6c74f3d4ab4b13c40276cbdc4f2]

## Source Notes

The earlier Cohere entry describes the same registry-based integration and optional-system/completed-versus-pending-turn pattern that the Dots formatter closely follows. [ancestor; call_df54448b153a4efa99dcdd0dd0ad5613]

Issue #51, 'dots.llm1 support', was opened by louiehelm and requests model architecture support. Its relationship to this turboderp-authored template change is inferred from the shared Dots identifier; the issue does not establish that this commit fulfills that broader request. [inference; call_1ee081d73f424e719da6c70f76d3ce04, call_938e08549d50418bb986029feb6cea86]

<a id="usage-evaluation"></a>

## Dots chat formatting through the existing template interface

PromptFormat_dots.format emits a system prompt only when truthy, enclosed by <|system|> and <|endofsystem|>. Each (user, answer) pair emits <|userprompt|>, user text, <|endofuserprompt|> and <|response|>. A non-None answer appends its text and <|endofresponse|>; None leaves the response prefix open for generation. No extra whitespace is inserted. [source; call_938e08549d50418bb986029feb6cea86]

The default system prompt is 'You are a helpful assistant.' The chat caller uses that default unless a truthy custom system prompt is supplied. It appends a pending (user_prompt, None) pair before formatting and stores the generated answer back into that pair afterward, matching the new formatter's input contract. [source; call_938e08549d50418bb986029feb6cea86, call_4124e6c74f3d4ab4b13c40276cbdc4f2]

add_bos returns False, while the existing caller still encodes special tokens. stop_conditions supplies the tokenizer EOS ID, the exact-token lookup for <|endofresponse|>, and that marker as a literal string. This follows the existing ChatML combination of token-ID and string stops. single_id performs dictionary lookup rather than validating that the marker exists. [source; call_938e08549d50418bb986029feb6cea86, call_3c9f98511fab44cea0ecf53b98c39706, call_4124e6c74f3d4ab4b13c40276cbdc4f2, call_fd1a8af237134ee2a2e639d2c767ca78]

thinktag returns <|sec-cot|> and <|sec-end-cot|>. The existing --think path appends the opening tag to the formatted prompt; --no_think passes both tags as banned strings. The same pair is passed to the streamer's formatting interface. [source; call_938e08549d50418bb986029feb6cea86, call_4124e6c74f3d4ab4b13c40276cbdc4f2]

A standard-library Python transcription passed four assertions covering an exact completed-plus-pending conversation, omission of an empty system prompt, and the distinction between empty and absent answers. The example contained two response starts but only one response end. [execution; call_c7c4eb326c554257afe764776c5be189]

## Uncertainty and limits

No Dots model or tokenizer was executed; recognition of the marker tokens, generation quality and end-to-end stopping remain unverified.

The bounded Python check transcribed formatting logic; it did not execute the added class or the chat pipeline.
