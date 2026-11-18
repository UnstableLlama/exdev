# 4f0414a1e9f76d654204e2bbfefb72074743cfa7


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4f0414a1e9f76d654204e2bbfefb72074743cfa7) · [Evidence ledger](draft.json)

Adds a manually selected SmolLM3 ChatML template with reasoning-dependent default instructions, and threads the existing think flag through all default-system-prompt implementations.

- [SmolLM3 prompts through the existing chat interface](#chat)

## Problem

The chat example had no SmolLM3 mode, and its default-system-prompt interface could not receive the existing reasoning flag. [source; call_5f952f6cc9d24b2eb0d10d8ad6aabbe8, call_ea327921e041451b99155aa01c1875ca]

## Reasoning

The edits are coupled: passing args.think enables SmolLM3-specific defaults, while updating every existing template signature preserves compatibility with that shared call. [source; call_ea327921e041451b99155aa01c1875ca, call_5f952f6cc9d24b2eb0d10d8ad6aabbe8]

## Impact

Selecting --mode smollm3 adds an application-side prompt template, not a model architecture or automatic checkpoint-template selection. [source; call_5f952f6cc9d24b2eb0d10d8ad6aabbe8, call_4ef9b13d1c7c4ae4823ad72df3c628cd]

## Source Notes

The root usage entry establishes the pre-existing template-controlled formatting, BOS and stopping interface. The earlier ChatML entry records disabling explicit BOS insertion; SmolLM3 follows that existing policy. [ancestor; call_433da1ee39554cdfae40e0abb7d59d93, call_ef8d38a79a1742f0a69e289f9b345c5f]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns incorrect template selection; PR #22, “OpenAI compatible API example,” includes discussion code calling default_system_prompt without arguments. Their relevance is inferred from the shared template interface, not an established link to this commit. That discussion example would need the new argument when used with these changed classes; it is not an additional in-tree caller. [inference; call_bfccbfa475874f50b4421cecb0d04ee3, call_62bfb871399844a08742fda884fa727f, call_031148d3f46d47a78d1c4ad97024f627, call_5f952f6cc9d24b2eb0d10d8ad6aabbe8]

Other inspected discussions retain distinct framing: #6 reports “No ROCm runtime is found, using ROCM_HOME='/usr'”; #39 asks “Gemma 3 architecture not in list?”; #43 reports “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated.” Their connection is only inferred shared chat.py usage, including a chatml -think diagnostic command in #43—not evidence that this template addresses those failures. [inference; call_371eed21ea7c49e8b233766e62100d92, call_87d59a77e6454b7b9e2c5e798a1ef010, call_1738e9a19e5c448dadc0b099ee47e6c1, call_e33e6bab0c584637a55ec8da535c9031]

<a id="chat"></a>

## SmolLM3 prompts through the existing chat interface

PromptFormat_smollm3 is registered as smollm3. Its format method exactly follows the existing ChatML formatter: emit a system turn, serialize each user/assistant pair, terminate completed answers with <|im_end|>, and leave the final unanswered assistant prefix open. It requests no explicit BOS token and supplies EOS, the exact <|im_end|> token ID, and its text as stop conditions. [source; call_5f952f6cc9d24b2eb0d10d8ad6aabbe8, call_b6f2af125c68437c8bae0c22e90b4e8b]

The default system prompt contains a literal June 2025 knowledge-cutoff label, a local datetime.today() date formatted as day/month-name/year, and Reasoning Mode /think or /no_think. These are prompt metadata, not runtime capability checks. The true branch adds detailed reasoning instructions; the false branch uses a short SmolLM identity instruction. [source; call_5f952f6cc9d24b2eb0d10d8ad6aabbe8]

main computes this default once at startup using args.think. A truthy custom --system_prompt replaces the entire default, including metadata and reasoning instructions. Independently, the existing get_input_ids appends the inherited <think> opening tag when --think is enabled, then encodes special tokens. --no_think separately supplies banned tag strings to Job; it does not select the system-prompt branch, and the parser does not make the two flags mutually exclusive. [source; call_ea327921e041451b99155aa01c1875ca, call_4ef9b13d1c7c4ae4823ad72df3c628cd, call_b6f2af125c68437c8bae0c22e90b4e8b]

Whole-parent searches found one executable default_system_prompt caller, in chat.py. The base class and all eleven existing subclasses—raw, llama3, chatml, phi, glm, mistral, gemma, reka, cohere, dots and ernie—receive the required think parameter without changing their returned prompts. The remaining same-name definitions are text in standard_cal_data/code.utf8, with a different historical interface; the patch leaves that calibration material unchanged rather than making it a runtime subclass. [source; call_031148d3f46d47a78d1c4ad97024f627, call_082970abf2d34a1d96fb10276fd855b4, call_b6e62cc2d5b1421ab465d493860e59e5, call_5f952f6cc9d24b2eb0d10d8ad6aabbe8]

The copied stopping code has the same preparation as ChatML: no additional token-existence guard. Tokenizer.single_id performs exact dictionary lookup, so the template assumes an appropriate tokenizer contains its delimiter. The string stop condition accompanies, rather than replaces, that ID lookup. [source; call_b6f2af125c68437c8bae0c22e90b4e8b, call_e59f2778cbf34973b65f85940289c1bb, call_5f952f6cc9d24b2eb0d10d8ad6aabbe8]

A standard-library check applied the signature-only change to the parent templates and verified all 22 combinations of eleven modes and two boolean values preserve their previous default text. Executing the parent ChatML formatter also verified a completed turn followed by an open assistant prefix and add_bos=False. This supports the unchanged-template interface and copied serialization, not SmolLM3 inference. [execution; call_cf62dd38d6d74328b7e5ab8dfccd19d1]

## Uncertainty and limits

No SmolLM3 checkpoint tokenizer or authoritative template specification was inspected; token availability, template fidelity and response quality remain unverified.

The bounded Python check executed parent template code and an AST transcription of the signature changes, not the complete patched chat application, tokenizer, generator or model.
