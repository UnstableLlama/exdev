# f8b9ab72ae9fd4fb00d4aab34302f9eb5edd81f5


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f8b9ab72ae9fd4fb00d4aab34302f9eb5edd81f5) · [Evidence ledger](draft.json)

Disable truncation on the shared tokenizer backend during initialization, without changing wrapper encoding or padding logic.

- [Disable backend truncation at tokenizer initialization](#loading-tokenization)

## Problem

The wrapper loaded tokenizer.json without explicitly disabling backend truncation. Encoding helpers then consumed the backend's returned IDs directly. [source; call_a4d49ab8178d4c0ea5d12efb6e4b2552]

## Reasoning

Calling no_truncation() once during construction establishes the policy on the shared backend before vocabulary probes and subsequent encoding, rather than modifying each encoding call. [source; call_afd71a7732364b75acda464087d0670e, call_a4d49ab8178d4c0ea5d12efb6e4b2552]

## Impact

For tokenizers loaded with truncation enabled, the intended effect is to preserve input tokens instead of silently shortening backend encodings. This does not itself provide model-context-length enforcement. [inference; call_afd71a7732364b75acda464087d0670e, call_a4d49ab8178d4c0ea5d12efb6e4b2552]

## Source Notes

The earlier tokenizer entry describes absence-safe BOS/EOS lookup; those guards remain present and are not modified by this change. [source; call_a4d49ab8178d4c0ea5d12efb6e4b2552, call_afd71a7732364b75acda464087d0670e]

Issue #7 reports an undefined native symbol, while issue #15 reports incoherent low-bpw output and discusses quantization regularization. Neither discussion identifies tokenizer truncation as its cause. [source; call_2711fb87d01a4ff6828eadb2fbc3cc23, call_d7065e103b1c49aa93010024425f533a]

<a id="loading-tokenization"></a>

## Disable backend truncation at tokenizer initialization

Tokenizer.__init__ now calls self.tokenizer.no_truncation() after loading the backend and auxiliary JSON dictionaries, before the BPE space/newline probes. The call is unconditional and adds no wrapper option. [source; call_afd71a7732364b75acda464087d0670e, call_a4d49ab8178d4c0ea5d12efb6e4b2552]

encode_special, encode_unspecial and num_tokens all use this same backend. Public encode still adds optional BOS/EOS tokens and left-pads list inputs to the longest encoded sequence; these operations are unchanged. [source; call_a4d49ab8178d4c0ea5d12efb6e4b2552, call_afd71a7732364b75acda464087d0670e]

Removing backend shortening favors complete encodings over honoring a serialized truncation policy. Previously capped inputs may consequently produce longer tensors and require length handling by callers. [inference; call_afd71a7732364b75acda464087d0670e, call_a4d49ab8178d4c0ea5d12efb6e4b2552]

## Uncertainty and limits

No backend tokenization or complete initialization was executed; no affected tokenizer artifact or reproduced truncated input was supplied.

A standard-library scalar computation would not validate this external-backend state change, so no substitute numerical test was performed.
