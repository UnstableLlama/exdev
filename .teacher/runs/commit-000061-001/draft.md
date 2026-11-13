# 2445cab0949fe69c5055bebe9aeefd88e41069e9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2445cab0949fe69c5055bebe9aeefd88e41069e9) · [Evidence ledger](draft.json)

Adds --mode glm to the chat example with GLM-style role markers, a default system prompt, BOS insertion and EOS/user-token stopping.

- [GLM4 chat prompt mode](#usage-evaluation)

## Problem

The chat example lacked a GLM-specific prompt mode; the change adds a registered template described as “ChatGLM(4) models.” [source; call_fcb1f3f96243455c943b41fdd5737705, call_b864b9890daa49438dc8da129de1ca6a]

## Reasoning

Implementing the existing prompt-format interface lets GLM reuse the chat loop's history, tokenization and generation plumbing rather than introducing a separate chat implementation. [inference; call_b864b9890daa49438dc8da129de1ca6a, call_3c861f3e2108484d8dde990480705348]

## Impact

Selecting --mode glm now resolves to PromptFormat_glm, and the existing mode-listing loop includes its description. The patch changes application-side prompting, not model architecture implementation. [source; call_b864b9890daa49438dc8da129de1ca6a, call_3c861f3e2108484d8dde990480705348]

## Source Notes

The earlier usage entry describes the original six chat formats as application-side templates rather than architecture validation. [ancestor; call_5fbbe9ea6eb9427d9d47d5b87a5efa73]

<a id="usage-evaluation"></a>

## GLM4 chat prompt mode

PromptFormat_glm defaults to “You are a helpful AI assistant.” Its format method starts with [gMASK]<sop><|system|>, a newline and the system prompt. Each history pair contributes <|user|> plus a newline and user text, followed by <|assistant|> and a newline. Completed answers are appended directly; a None answer leaves the assistant prefix open for generation. [source; call_b864b9890daa49438dc8da129de1ca6a]

Unlike the adjacent Phi template, GLM inserts no <|end|> separators. Turn boundaries instead use successive role markers. User and bot display names are accepted through the base constructor but do not alter GLM's fixed role markers. [source; call_b864b9890daa49438dc8da129de1ca6a, call_fcb1f3f96243455c943b41fdd5737705]

The template requests BOS insertion and returns two stop conditions: tokenizer.eos_token_id and tokenizer.single_id("<|user|>"). The existing chat loop passes add_bos to encode with encode_special_tokens=True and passes those stop conditions to Job. It uses the template's default system prompt unless a nonempty custom prompt is supplied. [source; call_b864b9890daa49438dc8da129de1ca6a, call_3c861f3e2108484d8dde990480705348]

A standard-library transcription checked a completed turn followed by an unanswered turn: the previous answer is immediately followed by the next user marker, and the resulting prompt ends with the assistant marker and newline. Empty history retains only the system-prefixed context. [execution; call_065e7b3e5205453293b551623a78f188]

## Uncertainty and limits

No GLM tokenizer artifact or authoritative template specification was supplied; compatibility of special tokens, BOS handling and stop-token IDs remains unverified.

The bounded Python check executed a transcription of string formatting only, not repository inference, tokenization or generation.
