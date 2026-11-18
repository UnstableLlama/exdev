# b2b0980972f07a2117d805aa37afbdaa6899ff42


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b2b0980972f07a2117d805aa37afbdaa6899ff42) · [Evidence ledger](draft.json)

Fixes chat's Context token count by retaining uncached prompt tokens separately from generated tokens; throughput calculations remain unchanged.

- [Separate context and generation counts in chat statistics](#usage-evaluation)

## Problem

Chat's statistics overwrote the uncached context-token count with the generated-token count before printing Context, pairing the wrong count with correctly computed prompt throughput. [source; call_e868ae1a4f864cb9928df10dd924a585, call_dc9d138634544eb99544a5413bca2746]

## Reasoning

Keeping uncached prompt work in new_ctx_tokens separates it from new_tokens, which continues to represent generated output. Both the prompt-rate numerator and Context display now use the same value. [source; call_dc9d138634544eb99544a5413bca2746]

## Impact

Corrects the displayed Context count when statistics are enabled; neither throughput formula, cached count nor generation count changes. [source; call_dc9d138634544eb99544a5413bca2746]

## Source Notes

Read the earlier optional-statistics entry ea4ef8d. It establishes the introduction of this block and records both the overwritten Context count and the separate /tps state-toggle problem. [ancestor; call_fa6d16e018c1440592cf5a2b369d2f34]

Closed discussions have distinct framing: #6, “No ROCm runtime is found, using ROCM_HOME='/usr'”, reports startup failure; #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions”, concerns prompt mode; #39, “Gemma 3 architecture not in list?”, concerns branch availability and frontend behavior; #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated”, concerns conversion; PR #22, “OpenAI compatible API example”, proposes an endpoint. Their connection to this change is inference from their references to chat.py, not evidence that they motivated this display fix. [inference; call_02ac09cd4e3c431eb86bb237b091f879, call_d639f5b9dcff456e9fdc54fba90cfbd5, call_db850ba9801345589b7f83cb32c1e1cf, call_328c3a6e438c455c8ad216d699d996d5, call_e2c9de87193f4fd684a00acf2c3caad5, call_e75baeb0cf8a42bbb7027971a6285607, call_9fca9ad1e9fb4b7187705ad0b7349761, call_45587a12bbfa4f47bb3bf438437dba72, call_0e50684b14534df49efa532a8537aab1]

<a id="usage-evaluation"></a>

## Separate context and generation counts in chat statistics

main reports statistics after its single queued job drains, gated by show_tps initialized from the opt-in -tps/--show_tps argument. The shared post-stream block serves both console-output modes. [source; call_e868ae1a4f864cb9928df10dd924a585]

The context count is the formatted, trimmed input length ids.shape[-1] minus r['cached_tokens']. Job's EOS metadata supplies cached tokens, generated tokens, prefill duration from first prefill to first token, and generation duration from first token to completion. These are application timing intervals, not isolated kernel timings. [source; call_e868ae1a4f864cb9928df10dd924a585, call_1b045f27cf3f48f6888700b64d716b47]

The rename and formatting substitution are complementary: merely renaming the prompt numerator would leave Context displaying generated tokens. Together they preserve the prompt count until formatting without altering generation accounting. Existing .3f formatting means three decimal places, not guaranteed measurement accuracy. [source; call_dc9d138634544eb99544a5413bca2746]

A scalar transcription using 100 prompt tokens, 40 cached tokens, ten generated tokens, two seconds of prefill and half a second of generation changed Context from 10 to 60 while retaining prompt throughput 30.000 t/s and generation throughput 20.000 t/s. [execution; call_19cac2e63d97454abe27caa7733020b7]

Source comparison shows the earlier Context-count observation is removed by this diff. The separately recorded /tps toggle and unchecked negative code-block index remain unchanged; the display correction does not repair those paths. [source; call_dc9d138634544eb99544a5413bca2746, call_e868ae1a4f864cb9928df10dd924a585, call_feb7be7aa01b453abbe8166e1fa2103d]

## Authoring-time findings — pending review

### inherited-tps-toggle (suspected; defect)

The inherited /tps command still toggles multiline input rather than statistics visibility.

Trigger: Enter /tps during an active chat session.

Expected: Toggle throughput reporting without changing input mode.

Actual: The branch flips multiline and bases its confirmation on multiline; show_tps remains unchanged. The script entry point reaches this shared branch in either console-output mode.

Locations: b2b0980972f07a2117d805aa37afbdaa6899ff42:examples/chat.py — main

Source evidence: call_e868ae1a4f864cb9928df10dd924a585, call_dc9d138634544eb99544a5413bca2746, call_a8a4d2ea68714a8583d19ea55ffcb5d4, call_44ec1c06450e44e8a102c95a1100b74d

source_inspection: Compared the command's assignment with the reporting gate and the complete task diff. [call_e868ae1a4f864cb9928df10dd924a585, call_dc9d138634544eb99544a5413bca2746]. Limits: No interactive execution; literal caller searches do not establish external invocation.

### inherited-negative-codeblock-index (suspected; defect)

The inherited code-block helper still accepts an unchecked negative block number.

Trigger: Enter /cc -2 after a response containing exactly two matched fenced code blocks.

Expected: Reject or normalize the invalid block number without terminating chat.

Actual: main passes -2 to copy_last_codeblock, whose upper-bound-only check leaves it unchanged; matches[-num] becomes matches[2] and raises IndexError before copying. The sole literal helper caller is main's /cc branch, which catches parsing failures but not this indexing failure.

Locations: b2b0980972f07a2117d805aa37afbdaa6899ff42:examples/chat_util.py — copy_last_codeblock

Source evidence: call_d3d2503e77674c528c78def081feb8ed, call_feb7be7aa01b453abbe8166e1fa2103d, call_e868ae1a4f864cb9928df10dd924a585, call_dc9d138634544eb99544a5413bca2746

source_inspection: Inspected the helper, its whole-tree literal caller search, the caller's exception handling and the unchanged path in the task diff. [call_d3d2503e77674c528c78def081feb8ed, call_feb7be7aa01b453abbe8166e1fa2103d, call_e868ae1a4f864cb9928df10dd924a585, call_dc9d138634544eb99544a5413bca2746]. Limits: No clipboard or interactive application execution.

## Uncertainty and limits

No model generation or interactive terminal session was executed. The bounded Python check transcribed statistics arithmetic with synthetic metadata, not measured inference performance.

Throughput divisions remain unguarded against zero durations; whether real executions produce such durations was not established.

Literal caller searches establish the script entry point and local helper caller, not external or dynamically resolved callers.
