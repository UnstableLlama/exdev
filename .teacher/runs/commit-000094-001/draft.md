# b077d49957b9bbc8f6370916cd8df9f273aabed9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b077d49957b9bbc8f6370916cd8df9f273aabed9) · [Evidence ledger](draft.json)

Adds an explicitly selectable Cohere chat template through the existing prompt-format interface, without adding model architecture support.

- [Cohere chat prompt formatting](#usage-evaluation)

## Problem

The chat template registry lacked a Cohere option; this change adds one without modifying model architecture support. [source; call_a39ea4032d35493f890961764fae62d9, call_d32ae8b3d02b48cca8abef7ecbe4e807]

## Reasoning

Registering PromptFormat_cohere under 'cohere' reuses the existing --mode dispatch, tokenization and generation loop rather than adding a separate chat implementation. [source; call_d32ae8b3d02b48cca8abef7ecbe4e807, call_38a0048a3bb64ce0a8bc1e81376d9723]

## Impact

Selecting --mode cohere supplies Cohere-style role delimiters, a default system prompt, BOS insertion and EOS/end-of-turn stop conditions. Existing registry entries remain unchanged. [source; call_d32ae8b3d02b48cca8abef7ecbe4e807, call_38a0048a3bb64ce0a8bc1e81376d9723]

## Source Notes

The parent README separately lists Cohere architecture support as work in progress; adding this prompt template does not establish that support. [source; call_65ec66f597314163a012382f72fd9735, call_d32ae8b3d02b48cca8abef7ecbe4e807]

The reviewed discussions report an undefined __cxa_call_terminate symbol (#7), incoherent cogito output at bpw <= 2.5 (#15), and Windows build failure (#21). Their framing concerns compilation or quantization, not Cohere prompt formatting; no connection to this change is established. [inference; call_77724f4372d046cca6af6aad5f749f62, call_a3b754861ec0426788818d87c3a8a5e1, call_ff4bce23ac024cda87920391d4aeadbf, call_d32ae8b3d02b48cca8abef7ecbe4e807]

<a id="usage-evaluation"></a>

## Cohere chat prompt formatting

PromptFormat_cohere.format optionally emits a SYSTEM turn, then a USER turn and CHATBOT prefix for each message pair. START_OF_TURN_TOKEN and END_OF_TURN_TOKEN delimit completed turns. An answer of None leaves the chatbot turn open for generation; even an empty-string answer closes it. [source; call_d32ae8b3d02b48cca8abef7ecbe4e807]

The default system prompt contains 'Task and Context' and 'Style Guide' sections asking for helpful interactive answers and full sentences with proper grammar. The chat caller substitutes a nonempty custom system prompt; the formatter itself omits the system turn for a falsey prompt. [source; call_d32ae8b3d02b48cca8abef7ecbe4e807, call_38a0048a3bb64ce0a8bc1e81376d9723]

The existing caller encodes the formatted text with special-token recognition enabled and the template's add_bos=True. It passes tokenizer.eos_token_id and the literal end-of-turn marker to Job as stop conditions. Cohere inherits the base <think>/</think> tags, so --think uses those rather than introducing Cohere-specific reasoning syntax. [source; call_d32ae8b3d02b48cca8abef7ecbe4e807, call_38a0048a3bb64ce0a8bc1e81376d9723, call_a39ea4032d35493f890961764fae62d9]

A bounded Python transcription verified that a system turn, one completed exchange and one pending exchange produce five turn starts and four turn ends, ending at the chatbot prefix. It also checked omitted empty system prompts and the distinction between empty and absent answers. [execution; call_488b8fe9065644e291de5c29a9d6ed35]

## Uncertainty and limits

No Cohere tokenizer or model was executed; token recognition, stop handling and generation quality remain unverified.

The Python check transcribed the formatter only; it did not execute the task implementation or the chat pipeline.
