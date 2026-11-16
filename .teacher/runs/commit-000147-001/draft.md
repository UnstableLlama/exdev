# beb7bcd96d0d54ee2511a84f63632d0fe3590050


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/beb7bcd96d0d54ee2511a84f63632d0fe3590050) · [Evidence ledger](draft.json)

Fixes HumanEval's top-k argument type, removes its repetition-penalty control, and adds a Qwen3 prompt preset with an empty thinking block.

- [HumanEval sampling correction and Qwen3 prompting](#usage-evaluation)

## Problem

HumanEval parsed top_k as float but passed it unchanged to SS_TopK, which uses it as a slice boundary when enabled. [source; call_1596f744eb944e58958effc4bd21b246, call_ebd621cb2128404fa1e6ee0f57c81904]

## Reasoning

Parsing top_k as int fixes the mismatch at the CLI boundary without changing the shared sampler. Removing the repetition-penalty argument instead falls back to ComboSampler's neutral default. [source; call_7c2b195c96644d09b8fbb11950664924, call_d6a600bf65ad4121a26ec5dbb4034aae, call_ebd621cb2128404fa1e6ee0f57c81904]

## Impact

The script gains an opt-in qwen3 prompt preset and loses its -repp/--rep_p CLI control; repetition-penalty support remains in ComboSampler. [source; call_7c2b195c96644d09b8fbb11950664924, call_d6a600bf65ad4121a26ec5dbb4034aae]

## Source Notes

PR #35, “humaneval.py: fix top_k type and remove rep_p,” contains gakada's index-type diagnosis and report of 0% results with several non-neutral repetition penalties. Together with the supplied author attribution, this identifies the reporter, PR opener and fix author as the same contributor, not independent corroboration. Its relationship to this task is inferred from the matching filename and edits. [inference; call_f73e5ff4e89b460b82b695c6819adb78, call_7c2b195c96644d09b8fbb11950664924]

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, concerns context scaling; closed issue #33, “Error converting model,” concerns conversion failing with too many open files. Their connection here is only inferred shared Qwen3 terminology, not evidence that this HumanEval patch addresses either issue. [inference; call_7829c6eef7324245a69d2c2170c3495b, call_7a0b6500d5c44d11a4342217184dcc72, call_eb625b9e38b94583a731a8d7bd51fb0a, call_7c2b195c96644d09b8fbb11950664924]

<a id="usage-evaluation"></a>

## HumanEval sampling correction and Qwen3 prompting

The parent annotation recorded the enabled top-k float mismatch as a suspected defect. [ancestor; call_ab36f5e982ed4721b90b5421435c9de5]

The patch removes that CLI mismatch by changing both type=float to type=int and default=0.0 to default=0. SS_TopK disables itself below one; otherwise it sorts candidates and masks positions starting at k. Temperature zero bypasses this filter through ComboSampler's argmax branch. [source; call_7c2b195c96644d09b8fbb11950664924, call_d6a600bf65ad4121a26ec5dbb4034aae, call_ebd621cb2128404fa1e6ee0f57c81904]

A standard-library transcription parsed --top_k 5 as 5.0 before the change and observed a list-slicing TypeError; the revised parser produced integer 5 and a valid slice. Both defaults disabled the modeled filter. The revised parser rejected decimal spelling 5.0. [execution; call_e6022c9060f0450f8604987794e8080c]

Omitting rep_p selects the existing default 1.0, whose SS_RepP.alt returns a no-op. Thus default penalty behavior is preserved while this script no longer exposes non-neutral penalties; the underlying penalty implementation is not repaired or removed. [source; call_7c2b195c96644d09b8fbb11950664924, call_d6a600bf65ad4121a26ec5dbb4034aae, call_ebd621cb2128404fa1e6ee0f57c81904]

The qwen3 preset follows the existing ChatML structure but inserts an empty <think> block before the assistant's answer prefill. It repeats the problem in the user request and after the Python fence. The existing path substitutes both placeholders, encodes special tokens with BOS requested, and reconstructs saved completions with a four-space prefix. [source; call_7c2b195c96644d09b8fbb11950664924, call_1596f744eb944e58958effc4bd21b246]

The empty, already-closed thinking block appears intended to steer directly into code completion rather than generated reasoning. This is prompt steering, not a new architectural implementation: the parent already imports Qwen3Model in its architecture registry. [inference; call_7c2b195c96644d09b8fbb11950664924, call_158189061e1643c5988df61fb93f9202]

## Uncertainty and limits

No model generation, PyTorch tensor indexing, CUDA sampling or HumanEval scoring was executed. The scalar check tests argparse and Python list slicing only.

The reported repetition-penalty failure and the Qwen3 preset's effect on generation quality remain unverified.
