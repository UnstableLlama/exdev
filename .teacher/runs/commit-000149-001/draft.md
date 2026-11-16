# f5127e87f800a4f11f2aa9605039896ac41d9382


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f5127e87f800a4f11f2aa9605039896ac41d9382) · [Evidence ledger](draft.json)

Integrates HumanEval's stricter integer top-k CLI, neutral-only repetition setting and optional Qwen3 empty-thinking prefill; dev already converted top-k before slicing.

- [Integrating HumanEval sampling and Qwen3 prompting](#usage-evaluation)

## Problem

This merge brings HumanEval's integer top-k CLI, removal of its repetition-penalty option, and Qwen3 prompt preset into dev. [source; call_058c768bb1c246f0a1257e52c1fd4f56]

## Reasoning

The reported top-k motivation needs branch-specific qualification: the first-parent SS_TopK already validates integer-valued input and converts it with int(top_k) before slicing. Consequently, this merge changes CLI validation rather than repairing an unconverted float slice in that parent. [source; call_172fb4fd6893426fb16fa25c017f2871, call_058c768bb1c246f0a1257e52c1fd4f56]

## Impact

HumanEval no longer exposes non-neutral repetition penalties; omitting rep_p selects ComboSampler's default 1.0, which SS_RepP replaces with a no-op. The shared penalty API remains. [source; call_058c768bb1c246f0a1257e52c1fd4f56, call_a9931bc867104419aed8cb9b0e200963, call_172fb4fd6893426fb16fa25c017f2871]

## Source Notes

The second-parent annotation describes the same three HumanEval edits, but its float-slicing explanation does not describe the inspected dev-parent constructor. [ancestor; call_c6ffa083198745bb96297afc9186c731]

In PR #35, “humaneval.py: fix top_k type, remove rep_p, add qwen3,” opener gakada also reports the index mistake, penalty failures and prompt-dependent scores. Turboderp reports a separate penalty-kernel diagnosis. These are discussion reports, not reproduced results. [source; call_46c01e3a14bd40e18b5066a51a507857]

The relationship to PR #35 is supported by the matching file and all three edits. Issue #33, “Error converting model,” instead concerns conversion failing with too many open files; shared Qwen3 terminology does not establish a connection to this HumanEval merge. [inference; call_058c768bb1c246f0a1257e52c1fd4f56, call_46c01e3a14bd40e18b5066a51a507857, call_deeea1939dd64b19b9ad6d896d8b8d7b, call_665dfe11fa084ef9ac82ff5c826ddb74]

<a id="usage-evaluation"></a>

## Integrating HumanEval sampling and Qwen3 prompting

main forwards top_k directly to ComboSampler. Its greedy branch selects argmax when temperature is zero or top_k is one; otherwise SS_TopK sorts candidates and masks positions starting at k. Values below one disable that step. The parser now uses int and default 0 instead of float and 0.0. [source; call_5e3ee30c58f443318341b69bd9ae9f42, call_a9931bc867104419aed8cb9b0e200963, call_172fb4fd6893426fb16fa25c017f2871, call_058c768bb1c246f0a1257e52c1fd4f56]

A standard-library transcription of the parser declarations confirmed that 5 changes from float 5.0 to integer 5, the default becomes integer zero, and the decimal spelling 5.0 is now rejected. [execution; call_b66b46b8a89b4289affac665d42aa13f]

The opt-in qwen3 template follows ChatML but adds an empty, already-closed <think> block before the assistant's Python-code prefill. Existing substitution inserts the problem into both the user request and assistant code fence; encoding requests special tokens and BOS. Saved completions retain the four-space indentation prefix. Default prompt selection is unchanged. [source; call_058c768bb1c246f0a1257e52c1fd4f56, call_5e3ee30c58f443318341b69bd9ae9f42]

The prefill steers generation toward an immediate function body rather than a generated reasoning stage. PR #35 discusses generating through </think> before injecting the function header as an alternative; this merge does not implement that staged workflow. [inference; call_058c768bb1c246f0a1257e52c1fd4f56, call_46c01e3a14bd40e18b5066a51a507857]

## Uncertainty and limits

No model generation, CUDA sampling or HumanEval scoring was executed; the bounded execution checks argparse only.

SS_TopK calls top_k.is_integer() even for the newly supplied integer. Compatibility of that method across supported Python versions is unestablished here.

Discussion claims about penalty-kernel repairs and score improvements were not independently verified.
