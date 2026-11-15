# cf0cbe0a10ae4dda9f49876df50c46c09a75567c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/cf0cbe0a10ae4dda9f49876df50c46c09a75567c) · [Evidence ledger](draft.json)

Disables explicit BOS insertion for ChatML prompts while preserving message delimiters, stop conditions and other templates.

- [ChatML without explicit BOS insertion](#chat)

## Problem

The ChatML template requested an explicit beginning-of-sequence token in addition to its own role delimiters. This change disables that request. [source; call_7902f3291dfc455c8230b4961d7a8623, call_87fa1f7887bc440e95b6a1e7fa978780]

## Reasoning

Keeping the policy in PromptFormat_chatml narrows the adjustment to ChatML rather than changing tokenizer behavior or other prompt formats. [inference; call_7902f3291dfc455c8230b4961d7a8623, call_606c501e1a3646a79cb3708886c64bda]

## Impact

With --mode chatml, chat.py now passes add_bos=False whenever it tokenizes the conversation, including after history trimming. The resulting IDs are passed to Job; formatting and stop conditions are unchanged. [source; call_7902f3291dfc455c8230b4961d7a8623, call_606c501e1a3646a79cb3708886c64bda]

## Source Notes

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports using llama3 mode for Qwen; turboderp recommends chatml. Its connection here is inferred from the shared chat.py/template-selection path, not evidence that BOS removal fixes that reported error. [inference; call_d35d3c9db13f4067ad18f4f8d71dcb31, call_7902f3291dfc455c8230b4961d7a8623]

PR #22, “OpenAI compatible API example,” contains discussion code forwarding prompt_format.add_bos() to tokenizer.encode. This is an inferred interface connection to the changed method, not an established motivation for this commit or an in-tree API caller. [inference; call_3b7a8589c0de480bb6755406645b8693, call_8926e591b13f451f8977f6791d961fe2, call_7902f3291dfc455c8230b4961d7a8623]

The earlier GLM entry describes the same template-controlled BOS interface, with GLM requesting insertion. [ancestor; call_32cee8bae10e47e18b3630ab466a1548]

<a id="chat"></a>

## ChatML without explicit BOS insertion

PromptFormat_chatml.add_bos changes from True to False. Its format method still begins with <|im_start|>system, separates messages with <|im_end|>, and leaves the unanswered assistant prefix open for generation. [source; call_7902f3291dfc455c8230b4961d7a8623, call_87fa1f7887bc440e95b6a1e7fa978780]

The whole-parent add_bos search identifies chat.py as the direct consumer of the template method. main captures its return value and get_input_ids forwards it with encode_special_tokens=True, so disabling BOS does not disable recognition of ChatML delimiters. [source; call_44d82f666daf4ae8bc8cec601085bb6f, call_606c501e1a3646a79cb3708886c64bda]

Tokenizer.encode inserts bos_token_id at position zero only when add_bos is true and that ID is not None. The patch therefore skips that explicit insertion; it does not remove tokens already present in the encoded text. [source; call_c1483fc2d6c54a6d9488f7aca5a152cc, call_7902f3291dfc455c8230b4961d7a8623]

A scalar transcription using fixed encoded IDs checked BOS values None, 0 and 42: disabling insertion shortened the sequence by one token for both defined IDs and left it unchanged for None. This was not repository tokenizer execution. [execution; call_80829f8eb60d46dda0e112ff23e12c4e, call_c1483fc2d6c54a6d9488f7aca5a152cc]

## Uncertainty and limits

The author's suggestion that omitting BOS is standard is not established by an authoritative ChatML specification or model-specific tokenizer evidence.

No real tokenizer or model inference was executed. The scalar check covers only explicit BOS insertion, not backend tokenization or response quality.
