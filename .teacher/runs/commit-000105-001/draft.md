# 7488d82c241a1b9880fb3972cd7105ee4b8cd2c0


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/7488d82c241a1b9880fb3972cd7105ee4b8cd2c0) · [Evidence ledger](draft.json)

Adds optional generation-side suppression of reasoning tags, but also introduces a stream-call argument mismatch affecting both chat console modes.

- [Optional reasoning-tag suppression](#chat)

## Problem

The chat example lacked a command-line switch to suppress generation of reasoning delimiters. [source; call_b076763735824b54872469e73ff0f7e0, call_68b0b7bb6eaa4628925ff34c88fd3098]

## Reasoning

The patch reuses Job.banned_strings rather than removing tags from displayed output. This constrains generated text, not whether a model produces reasoning without delimiters. [source; call_68b0b7bb6eaa4628925ff34c88fd3098, call_e8b8f0ed8d22446ba6b8928ff1033318, call_0e2ac6f3dc3146668776d0ba71282869]

## Impact

The accompanying streaming-call change is incompatible with both existing console implementations and affects chat even when --no_think is absent. [source; call_68b0b7bb6eaa4628925ff34c88fd3098, call_bc8cca0f681b4822ae385550f35b833e]

## Source Notes

PR #22, “OpenAI compatible API example,” proposes an API endpoint and discusses prompt-template integration and problematic model output. Its relationship here is only inferred from its explicit examples/chat.py usage and reasoning-mode discussion; it does not establish the motivation for this patch. [inference; call_bf87ecd16fc74ce09030b2972cc1e971, call_564dc8d404d3481a8208f00bbe47aba8, call_68b0b7bb6eaa4628925ff34c88fd3098]

<a id="chat"></a>

## Optional reasoning-tag suppression

The new -no_think/--no_think store_true option selects [tt[0], tt[1]] as each response job's banned strings; otherwise the job receives None. tt is obtained once per response from prompt_format.thinktag(). [source; call_68b0b7bb6eaa4628925ff34c88fd3098]

The base template returns <think> and </think>; the alternative override returns an opening string containing a leading space and trailing newline, ' <reasoning>\n', and </reasoning>. The patch passes these strings unchanged rather than normalizing delimiter whitespace. [source; call_37a6a80c8a494bdbbad0f152051a5252, call_6aab00400f594859997a505ef5cd31a3, call_68b0b7bb6eaa4628925ff34c88fd3098]

Job lowercases banned strings and prepares UTF-32 matching buffers. Its output path checks lowercased held text, retains a checkpoint for partial matches, and rewinds on completed matches while reporting suppressed text and tokens. This is generation-side suppression, unlike stop strings, whose matching branch terminates the response. [source; call_e8b8f0ed8d22446ba6b8928ff1033318, call_0e2ac6f3dc3146668776d0ba71282869]

--think remains independent: it still appends the opening delimiter to the input prompt. --no_think neither removes that prompt text nor disables --think; the new help explicitly cautions that suppressing tags need not prevent reasoning. [source; call_b076763735824b54872469e73ff0f7e0, call_68b0b7bb6eaa4628925ff34c88fd3098]

A standard-library check extracted both console method signatures and tested argument binding. The parent call shape was accepted for both; the patched call shape failed with 'too many positional arguments'. [execution; call_306e4435fcee41b6a3eb21db5bbb6dab]

## Authoring-time findings — pending review

### stream-argument-mismatch (suspected; defect)

The updated chat loop passes both delimiters to stream(), but neither console method accepts the additional argument.

Trigger: Any generator result reaches s.stream(chunk, tt[0], tt[1]) in examples/chat.py, in either basic or rich console mode, regardless of --no_think.

Expected: The selected console consumes the generated chunk and continues the response loop.

Actual: Argument binding raises TypeError before the stream method body runs. The whole-parent search found the chat loop as the only matching Python console .stream call; this observation concerns the interactive example, not all Generator users.

Locations: 7488d82c241a1b9880fb3972cd7105ee4b8cd2c0:examples/chat.py — main, 0b2dba5ac5aab77fb9d9aabdda72ceb5befa8b11:examples/chat_console.py — Streamer_basic.stream, 0b2dba5ac5aab77fb9d9aabdda72ceb5befa8b11:examples/chat_console.py — Streamer_rich.stream

Source evidence: call_68b0b7bb6eaa4628925ff34c88fd3098, call_bc8cca0f681b4822ae385550f35b833e, call_2233efaad1f9455bb110636c0b5c35de, call_b076763735824b54872469e73ff0f7e0

source_inspection: Compared the changed call with both unchanged stream signatures and inspected console selection and the whole-parent call search. [call_68b0b7bb6eaa4628925ff34c88fd3098, call_bc8cca0f681b4822ae385550f35b833e, call_2233efaad1f9455bb110636c0b5c35de, call_b076763735824b54872469e73ff0f7e0]. Limits: No end-to-end chat execution.

scalar_transcription: Extracted method parameters using ast and modeled parent and patched positional calls with inspect.Signature.bind. [call_306e4435fcee41b6a3eb21db5bbb6dab]. Limits: Tests Python argument compatibility, not repository method execution or GPU generation.

## Uncertainty and limits

No model generation, native banned-string matching, or interactive console session was executed. The bounded Python check validates argument binding only.
