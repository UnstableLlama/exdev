# f93b0103038c2577abf743a429c45fe448443ff3


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f93b0103038c2577abf743a429c45fe448443ff3) · [Evidence ledger](draft.json)

Adds an opt-in amnesia flag that clears prior chat exchanges before each new prompt while preserving the loaded session and system-prompt input.

- [Optional per-prompt conversation reset](#usage-evaluation)

## Problem

The chat example retains completed exchanges for subsequent prompts; it previously offered no amnesia switch. [source; call_225e7dc6bf4546959bb185ca877e1168, call_fa29328b66e9467f9ac0fd32ca29f1dd]

## Reasoning

Resetting context before appending the new prompt removes prior exchanges without changing prompt formatting, tokenization or response streaming. [source; call_fa29328b66e9467f9ac0fd32ca29f1dd, call_225e7dc6bf4546959bb185ca877e1168]

## Impact

Users can opt into independent conversational turns with -amnesia or --amnesia; ordinary history accumulation remains the default. [source; call_fa29328b66e9467f9ac0fd32ca29f1dd]

## Source Notes

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reports a chat Job-construction failure and receives advice to use chatml. Its relationship here is inferred solely from the shared examples/chat.py Job call; this patch does not alter stop conditions or template selection. [inference; call_1b9fbb415a2a40528ec6eaa74e332a93, call_225e7dc6bf4546959bb185ca877e1168, call_fa29328b66e9467f9ac0fd32ca29f1dd]

The other error reports inspected concern an undefined __cxa_call_terminate symbol during quantization (#7) and incoherent cogito output at bpw <= 2.5 (#15). Neither supplies evidence that amnesia addresses those problems. [inference; call_2d4e3836c0d547deba3436507e624fd4, call_1da6f8aa20c041269d7407b492060b44, call_fa29328b66e9467f9ac0fd32ca29f1dd]

<a id="usage-evaluation"></a>

## Optional per-prompt conversation reset

The new store_true option gates context = [] at the top of every chat-loop iteration. The current user prompt is appended afterward, so it is retained while previous user/assistant pairs are discarded. [source; call_fa29328b66e9467f9ac0fd32ca29f1dd, call_225e7dc6bf4546959bb185ca877e1168]

get_input_ids still passes the separately stored system_prompt and current context to the selected formatter, then tokenizes the result for Job. The completed answer is still written to context[-1], but amnesia discards that pair on the next iteration. Model, generator and cache initialization remain outside the loop. [source; call_225e7dc6bf4546959bb185ca877e1168, call_fa29328b66e9467f9ac0fd32ca29f1dd]

This provides a lightweight alternative to retaining multi-turn history while reusing the loaded session; the tradeoff is loss of preceding conversational references, not removal of the system-prompt argument. [inference; call_225e7dc6bf4546959bb185ca877e1168, call_fa29328b66e9467f9ac0fd32ca29f1dd]

A standard-library transcription over three turns produced context lengths [1, 2, 3] without the option and [1, 1, 1] with either spelling. Parsing returned False by default and True for both aliases. [execution; call_d8d6cbd2aadb4053961ae4463707ebf8]

## Uncertainty and limits

The bounded check transcribed argument parsing and context-list updates; it did not execute chat.py, tokenization, model inference or GPU cache operations.

Amnesia changes conversational history, not a demonstrated memory-erasure or cache-clearing guarantee.
