# 10b95addc0fc32df2f0cc94b820cbc9c83bb53b0


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/10b95addc0fc32df2f0cc94b820cbc9c83bb53b0) · [Evidence ledger](draft.json)

Adds an explicitly selected Reka chat template and moves reasoning delimiters into prompt formats, preserving existing formats' default tags.

- [Reka chat formatting and template-specific reasoning](#usage-evaluation)

## Problem

The CLI chat registry lacked a Reka format, and reasoning delimiters were globally fixed to <think> and </think>. [source; call_bed7bce09c9e4079ba2a632e18860b80, call_e6872d9a392c4053a6f093c0570402f3]

## Reasoning

Moving reasoning delimiters into PromptFormat lets Reka override them while existing formats inherit the previous pair. This keeps model-specific prompt syntax out of the shared chat loop. [source; call_31c5107b639c4511ac4ee3df90023e78, call_e6872d9a392c4053a6f093c0570402f3]

## Impact

Users can select --mode reka and optionally --think. This adds chat formatting, not a model architecture or quantization change. [source; call_1e72f88082c74a70bf0c01af3531ecbf, call_31c5107b639c4511ac4ee3df90023e78, call_e6872d9a392c4053a6f093c0570402f3]

## Source Notes

An earlier entry describes a separate Reka HumanEval prompt with comment-based reasoning and a Python-code prefill. [ancestor; call_3ba8de6208c846a98f0969bb94208a78]

PR #20, “Reka Flash 3 vs padding,” reports quantization padding problems and HumanEval results. Its relationship to this change is inferred from the shared Reka Flash 3 model name; it does not establish the correctness of this chat template. [inference; call_d1d9a1be6e284a13805580827f92928b, call_31c5107b639c4511ac4ee3df90023e78]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports using llama3 mode for Qwen; the response recommends chatml. Its contextual connection is inferred from the same chat.py mode-selection interface, not evidence that this commit fixes that report. [inference; call_bc892f799f2e40eeadecdfeaefeb7331, call_1e72f88082c74a70bf0c01af3531ecbf]

Other inspected reports concern different failures: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns low-bitrate quantization. [source; call_cbcd6b2b0b814068a9a46380f94654c1, call_a998f8bd704f4d93a703d004b6c2d729]

<a id="usage-evaluation"></a>

## Reka chat formatting and template-specific reasoning

PromptFormat_reka serializes turns as 'human: … <sep> assistant: … <sep> '. A pending answer ends at 'assistant:'. The default system prompt is empty; a supplied system prompt is prepended to the first retained human message rather than emitted as a separate role. [source; call_31c5107b639c4511ac4ee3df90023e78]

Reka disables automatic BOS insertion and supplies tokenizer.eos_token_id plus the literal '<sep>' as stop conditions. The existing chat loop encodes the formatted context with special-token handling and passes the selected stop conditions to Job. [source; call_31c5107b639c4511ac4ee3df90023e78, call_1e72f88082c74a70bf0c01af3531ecbf]

With --think, get_input_ids appends Reka's exact opening string ' <reasoning>\n'. Streaming receives '</reasoning>' as its closing marker. Streamer_rich searches its accumulated thinking text for that marker before starting Markdown output; Streamer_basic accepts but does not interpret the marker. [source; call_e6872d9a392c4053a6f093c0570402f3, call_31c5107b639c4511ac4ee3df90023e78, call_bcdf99adfff447b1a6936319db04bfc3]

The integration retains explicit mode selection rather than discovering a template from the model. Inheritance preserves the old reasoning tags for existing formats while making the new syntax selectable through the same registry. [source; call_bed7bce09c9e4079ba2a632e18860b80, call_31c5107b639c4511ac4ee3df90023e78, call_1e72f88082c74a70bf0c01af3531ecbf]

Four standard-library transcription checks passed for two-turn formatting, an empty system prompt, reattaching the system prompt after history trimming, and the exact reasoning-prefill boundary. [execution; call_ffe5858705424d86bcd1bb2d8e89bb0c]

## Uncertainty and limits

No model generation, tokenizer compatibility, or terminal rendering was tested. The Python check exercised a transcription of string formatting, not the repository implementation.

The inspected evidence does not establish agreement with Reka's training template or improved answer quality.
