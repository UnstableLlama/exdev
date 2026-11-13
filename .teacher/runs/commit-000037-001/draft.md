# d2165ca1ac914225233edbc5e31399bae7dd8378


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d2165ca1ac914225233edbc5e31399bae7dd8378) · [Evidence ledger](draft.json)

Uses a running elapsed-time average for conversion estimates and raises the default checkpoint interval to 120 seconds; prediction accuracy remains unmeasured.

- [Average elapsed conversion time instead of the latest module](#conversion)

## Problem

The converter estimated remaining time from only the latest module's duration, excluding earlier checkpoint and unload overhead from that sample. [source; call_712d99d3a80c4390967fc181d70c6123]

## Reasoning

Using elapsed time across processed modules should reduce sensitivity to an unusually fast or slow individual module and incorporate intervening checkpoint overhead. This is an inferred benefit, not measured accuracy. [inference; call_f3453e36526f4f23bdc053a02ed763d9, call_712d99d3a80c4390967fc181d70c6123]

## Impact

The patch changes progress estimation and doubles the default minimum checkpoint interval from 60 to 120 seconds; it does not change quantization calculations. [source; call_f3453e36526f4f23bdc053a02ed763d9]

## Source Notes

The earlier time-formatting entry describes a separate correction to human_time's hour/minute decomposition, rather than to the estimator. [ancestor; call_2b5a0773c36f443385b86e3cb8782310]

Issue #12 is titled “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions” and concerns chat after conversion. Its conversion log contains the same remaining-time feedback text, providing contextual overlap only—not evidence that this change addresses that issue. [inference; call_0adb57dcc6594377a2f3e8380eac29d7, call_b42cd0b98b7148fa9bd129262d9b1cc3, call_f3453e36526f4f23bdc053a02ed763d9]

Issue #7 reports “quantizing model: undefined symbol: __cxa_call_terminate”; PR #13 reports a tokenizer failure without bos_token_id. Their overlap with this change is the conversion entry path, including PR #13's matching get_base_model call. Neither report establishes a motivation for the timing changes. [inference; call_96c2c170d8764ee5854c1980159a8367, call_0d8ac7c92c0f4c2bab8ea13959d5fc97, call_712d99d3a80c4390967fc181d70c6123, call_f3453e36526f4f23bdc053a02ed763d9]

<a id="conversion"></a>

## Average elapsed conversion time instead of the latest module

main initializes start_time and timed_blocks, then resets both on reaching model.first_block_idx. In the inspected Llama layout, this boundary follows the embedding and precedes transformer blocks, excluding model setup, calibration preparation and embedding processing from the running estimate. [source; call_f3453e36526f4f23bdc053a02ed763d9, call_712d99d3a80c4390967fc181d70c6123, call_d6db6456c62c4acfa1358776f8d3ffbc]

The reset occurs before the resume-skip check. Skipped modules therefore do not increment timed_blocks, while reaching the first-block index still resets the clock on a resumed job. Each processed module at or beyond that boundary increments the counter, including trailing normalization and output-head modules—not just transformer blocks. [source; call_f3453e36526f4f23bdc053a02ed763d9, call_712d99d3a80c4390967fc181d70c6123, call_d6db6456c62c4acfa1358776f8d3ffbc]

The new formula is elapsed / timed_blocks × (module_count − idx), replacing latest_module_time × (module_count − idx − 1). Elapsed time includes previous unloads and checkpoints, but the estimate is printed before the current module's unload and checkpoint. The new multiplier includes one more unit than the number of unprocessed modules. [source; call_f3453e36526f4f23bdc053a02ed763d9, call_712d99d3a80c4390967fc181d70c6123]

A scalar transcription with six total modules and post-embedding durations of 10, 20, 10, 2 and 30 seconds produced old estimates of 40, 60, 20, 2 and 0 seconds, versus new estimates of 50, 60, 40, 21 and 14.4 seconds. This illustrates averaging and the remaining one-unit allowance after the final module; it is not a repository conversion test. [execution; call_03d780035f2d418c9a463194d85d12c6]

checkpoint_interval remains a minimum elapsed-time threshold checked only after a module finishes, not a periodic timer. The new 120-second parser default also participates in prepare's override logic on resume, so omitting the option can replace a saved interval. Less frequent eligibility trades potential checkpoint overhead reduction against more work since the last checkpoint. [inference; call_f3453e36526f4f23bdc053a02ed763d9, call_712d99d3a80c4390967fc181d70c6123, call_b44992a5083f47fb922cc11bdbb1090f]

## Uncertainty and limits

No conversion or GPU workload was executed. The numerical check models the inspected formulas with synthetic durations and does not measure prediction accuracy.

The extra average-duration allowance is not explained by the diff. Compilation still follows the module loop without its own measured estimate.
