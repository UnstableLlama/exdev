# 105cafab0e2be1b989f07b820da10f8263b9572e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/105cafab0e2be1b989f07b820da10f8263b9572e) · [Evidence ledger](draft.json)

Adds an opt-in Reka-style HumanEval prompt with comment-based reasoning instructions and an assistant code prefill, while retaining existing generation and completion extraction.

- [Reka-style HumanEval prompting](#usage-evaluation)

## Problem

HumanEval's prompt registry lacked a reka option; requesting it followed the unsupported-format exit path. [source; call_35b473a7af2d4ceba135fc88040fb828]

## Reasoning

Adding a template/prefix pair reuses the existing formatting and completion pipeline rather than introducing model-specific evaluation logic. [source; call_cab31787897b4aeda040f9747700697d, call_35b473a7af2d4ceba135fc88040fb828]

## Impact

Users can select -pf reka or --prompt_format reka. Existing formats and the default unwrapped completion prompt remain unchanged; this is prompt-format support, not an architecture implementation. [source; call_cab31787897b4aeda040f9747700697d, call_35b473a7af2d4ceba135fc88040fb828]

## Source Notes

The earlier usage/evaluation entry describes HumanEval's template selection and completion extraction as part of its evaluation protocol. [ancestor; call_72b78ad90b184a04b9161776d2262768]

The inspected discussions concern different reports: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns quantization; #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns chat.py and choosing chatml. None identifies this HumanEval Reka addition as its remedy. [source; call_7dfa0a4c5b0d42ddaae4a5ef49508720, call_abbebf3b89b24f9ca5f66032e51494a7, call_0d185b565c584ac09d8f6c61751a9d16, call_04ee9344a96b4168bdb75564a37843fb]

<a id="usage-evaluation"></a>

## Reka-style HumanEval prompting

The new reka template starts with “human: Complete the following Python function.” It requests concise reasoning in comments without second-guessing, inserts the problem, then opens “ <sep> assistant: ```python\n” and repeats the problem as the assistant's code prefill. [source; call_cab31787897b4aeda040f9747700697d]

main replaces both {{problem}} placeholders with the HumanEval prompt, encodes the resulting string with special-token handling and BOS enabled, and passes those tokens through the existing Job creation path. The template does not add separate Reka-specific stopping behavior. [source; call_cab31787897b4aeda040f9747700697d, call_35b473a7af2d4ceba135fc88040fb828]

The tuple's second value is four spaces used when saving prefix + completion.strip(), not an extra suffix appended to the model input. Existing collection still stops at EOS or a non-indented final line and saves task_id/completion records, excluding the conversational wrapper. [source; call_cab31787897b4aeda040f9747700697d, call_35b473a7af2d4ceba135fc88040fb828]

Repeating the function under the assistant's Python fence appears intended to steer generation toward continuing its body rather than producing a standalone conversational answer. Requesting reasoning as comments is consistent with retaining executable code, but model compliance is not established. [inference; call_cab31787897b4aeda040f9747700697d, call_35b473a7af2d4ceba135fc88040fb828]

A standard-library check of the transcribed template and collector expression confirmed two problem copies, the exact assistant boundary, no remaining placeholder, and a four-space-prefixed saved “return x” completion for a synthetic function. [execution; call_0c42a11be1a64ee5a73f80680c694e83]

## Uncertainty and limits

No model generation, tokenizer compatibility check, or HumanEval scoring was run. The scalar check validates transcribed string handling only.

The evidence does not establish that these delimiters match a particular Reka model's training template or that the reasoning instruction improves correctness.
