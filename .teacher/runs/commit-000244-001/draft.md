# ea4ef8dcbb58d3afc5cffadcb90a01204af7036e


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ea4ef8dcbb58d3afc5cffadcb90a01204af7036e) · [Evidence ledger](draft.json)

Adds opt-in chat throughput statistics and a /tps command, but the command toggles multiline input and the Context count repeats generated tokens. The console change is comment-only.

- [Optional chat throughput statistics](#usage-evaluation)

## Problem

The interactive chat loop streamed replies without reporting prompt-processing throughput, cache reuse or generation throughput. [source; call_b1ec83f347484f02a7d8bdcf4eba5c83]

## Reasoning

The change reuses the generator's completion metadata rather than introducing chat-side timers. It separates uncached prompt work from cached tokens and generated tokens. [source; call_dc56863f51dc4d1f902f6c76557a2052, call_5f1add737a6743d7b6da902b7daf10c1]

## Impact

-tps/--show_tps enables a statistics line after replies; the new /tps command mistakenly toggles multiline input instead. The displayed Context token count also mistakenly repeats the generated-token count. [source; call_dc56863f51dc4d1f902f6c76557a2052]

## Source Notes

Read the initial usage-evaluation entry and the interactive-controls entry. They establish the earlier conversation-generation pipeline and local command-state design; the latter also records an unchecked code-block index. [ancestor; call_15deb0b0c1e54aa7ba8ad93e76d23d5a, call_552588e13f4640d8a59f62de78469ec9]

The recorded code-block index problem is carried over: the parent helper indexes matches[-num] without a lower bound, main forwards negative integers, and neither task section changes that path. [source; call_1c6bef24dcaa45209b13440c5f90f554, call_b1ec83f347484f02a7d8bdcf4eba5c83, call_dc56863f51dc4d1f902f6c76557a2052, call_bbb2444427324f96a9d683e2ee8cf6f1]

Closed discussions retain distinct framing: #6, “No ROCm runtime is found, using ROCM_HOME='/usr'”, concerns startup; #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions”, concerns prompt mode; #39, “Gemma 3 architecture not in list?”, concerns branch availability and frontend behavior; #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated”, concerns conversion; and PR #22, “OpenAI compatible API example”, proposes an endpoint. Their connection to this task is inferred only from references to chat.py, not evidence that they motivated statistics. [inference; call_0bc45a0b658e44df9f3c4953fcbe87e0, call_89deaf6c17404f57b11fe2d8943618c2, call_45f1a0b9511540dc8cdc8e3779e15190, call_eedf8e33593a412ebf06574170b797d5, call_91bfa1eb22b84cbabb343504bee1bac8, call_5e9654b61ace4301819e001af27cf511, call_56aae416793f4b73ae7e91d69a1c7d33, call_2d6af700af4a4ecea3c37d8727fef833, call_dc56863f51dc4d1f902f6c76557a2052]

<a id="usage-evaluation"></a>

## Optional chat throughput statistics

The parser adds a store_true -tps/--show_tps option, so reporting is opt-in. main snapshots args.show_tps and prints after streaming finishes and after any response-length warning, before storing the reply in conversation history. [source; call_dc56863f51dc4d1f902f6c76557a2052, call_b1ec83f347484f02a7d8bdcf4eba5c83]

The statistics use the trimmed, formatted input's ids.shape[-1]. Subtracting cached_tokens gives the numerator for prompt throughput; generation throughput uses r['new_tokens']. Job's EOS result supplies these counts and durations: time_prefill spans first prefill to first token, while time_generate spans first token to completion. These are application timing intervals, not isolated kernel benchmarks. [source; call_dc56863f51dc4d1f902f6c76557a2052, call_b1ec83f347484f02a7d8bdcf4eba5c83, call_5f1add737a6743d7b6da902b7daf10c1]

The existing dynamic_gen statistics consumer gates access on streaming EOS results and adds 1e-10 seconds to throughput denominators. Chat instead reads the final loop result after its single job drains and divides directly. Its .3f formatting selects three decimal places, not a measurement-accuracy guarantee. [source; call_75e84d7fa63a4d2d968603676a130157, call_b1ec83f347484f02a7d8bdcf4eba5c83, call_dc56863f51dc4d1f902f6c76557a2052]

The command follows the existing command-before-generation structure and continues without creating a model turn. However, its assignment and status-message condition use multiline, whereas the reporting gate uses show_tps. Both console-output modes pass multiline to read_input_ptk, which forwards it to prompt_toolkit. [source; call_dc56863f51dc4d1f902f6c76557a2052, call_b1ec83f347484f02a7d8bdcf4eba5c83, call_81d535641e2f4a048c00cd4b73813e7d]

A standard-library transcription with 100 prompt tokens, 40 cached tokens, a two-second prefill and ten generated tokens in half a second produced “Context: 10 new tokens at 30.000 t/s”, although uncached context work was 60 tokens. It also preserved show_tps across /tps for both initial boolean values while changing multiline. [execution; call_0b482d12f3c642c78677525a2c46d925]

The console edit changes only the col_info comment from “Bright red” to “Green”; the ANSI value remains unchanged. It supplies no runtime prerequisite for statistics. [source; call_bbb2444427324f96a9d683e2ee8cf6f1]

Whole-tree searches found no existing show_tps occurrence or chat-module import caller. The script's own parser-to-main call supplies the newly accessed attribute; external Namespace builders were not established. [source; call_87bbbe11c766435db6eb8b3c30ed3120, call_1e899e8849d44035af6b4c6cd8bcbb2b, call_3150db59a9df4891923e7036cced8634, call_fa439f9189a24d29ab0ee93ba675ac44, call_dc56863f51dc4d1f902f6c76557a2052]

## Authoring-time findings — pending review

### tps-toggles-multiline (suspected; defect)

/tps changes input mode rather than statistics visibility.

Trigger: Enter /tps in an active chat session.

Expected: Toggle tokens-per-second reporting without changing multiline input.

Actual: multiline flips, its value controls the confirmation message, and show_tps remains unchanged. This reaches both basic and rich output modes through main's shared command branch.

Locations: ea4ef8dcbb58d3afc5cffadcb90a01204af7036e:examples/chat.py — main

Source evidence: call_dc56863f51dc4d1f902f6c76557a2052, call_b1ec83f347484f02a7d8bdcf4eba5c83, call_81d535641e2f4a048c00cd4b73813e7d, call_fa439f9189a24d29ab0ee93ba675ac44

scalar_transcription: Transcribed the assignment for both initial show_tps values; reporting state stayed fixed while multiline became true. [call_0b482d12f3c642c78677525a2c46d925]. Limits: No interactive application execution.

### context-count-overwritten (suspected; defect)

The Context count reports generated tokens rather than uncached prompt tokens.

Trigger: Enable --show_tps and complete a reply whose generated-token count differs from prompt_tokens minus cached_tokens.

Expected: Display the uncached prompt count alongside the prompt throughput computed from that count.

Actual: new_tokens is overwritten with r['new_tokens'] before formatting both Context and Generate, pairing the generated count with prompt throughput. The script entry point reaches this shared post-stream block in either output mode.

Locations: ea4ef8dcbb58d3afc5cffadcb90a01204af7036e:examples/chat.py — main

Source evidence: call_dc56863f51dc4d1f902f6c76557a2052, call_b1ec83f347484f02a7d8bdcf4eba5c83, call_fa439f9189a24d29ab0ee93ba675ac44

scalar_transcription: For 60 uncached prompt tokens and ten generated tokens, the transcribed output displayed Context: 10 while retaining 60/2 = 30 t/s. [call_0b482d12f3c642c78677525a2c46d925]. Limits: Synthetic metadata; no inference or timing measurement.

### inherited-negative-codeblock-index (suspected; defect)

The previously recorded unchecked negative code-block index persists unchanged.

Trigger: Enter /cc -2 after a response containing exactly two matched fenced code blocks.

Expected: Reject or normalize the invalid block number without terminating chat.

Actual: The helper indexes matches[2] and raises IndexError before copying. main catches integer parsing failures only. Whole-tree search found its /cc branch as the sole literal helper caller.

Locations: ea4ef8dcbb58d3afc5cffadcb90a01204af7036e:examples/chat_util.py — copy_last_codeblock

Source evidence: call_1c6bef24dcaa45209b13440c5f90f554, call_5199154c9ad246b58a062744988bc968, call_b1ec83f347484f02a7d8bdcf4eba5c83, call_dc56863f51dc4d1f902f6c76557a2052

scalar_transcription: Transcribed fenced-block matching and negative indexing with two blocks; observed IndexError. [call_0b482d12f3c642c78677525a2c46d925]. Limits: Did not execute the helper, clipboard backend or chat session.

## Uncertainty and limits

No model generation or interactive terminal session was executed. The Python check transcribed state changes, statistics arithmetic and indexing only.

The new throughput divisions have no zero-duration guard. Actual timer resolution and occurrence of zero durations were not established.

Whole-parent-tree literal caller searches establish the script entry point, not compatibility with external or dynamically resolved callers.
