# 3c9ede55404c8ecce54494657f23f7056ea36a1a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/3c9ede55404c8ecce54494657f23f7056ea36a1a) · [Evidence ledger](draft.json)

Adds ChatML and DeepSeek HumanEval prompts and exposes ComboSampler controls, with a suspected float-versus-integer mismatch in the new top-k option.

- [HumanEval prompt and sampling controls](#usage-evaluation)

## Problem

HumanEval previously exposed only temperature and top-p sampling and lacked ChatML and DeepSeek prompt presets. [source; call_ac621791f366490eb081b691ceca7b32, call_f664c705b2dd4fd98039ee1d6f05ceec]

## Reasoning

Replacing TopPSampler with ComboSampler reuses the existing composable sampling implementation rather than adding evaluation-specific filtering logic. [source; call_f664c705b2dd4fd98039ee1d6f05ceec, call_78febdf5f7374ade9e5dc5fedfec48d6]

## Impact

The new controls enable repetition penalties, min-p, top-k and temperature-last sampling. Defaults retain temperature 0.6 and top-p 0.6, with the additional filters disabled; enabled top-k has a suspected CLI type mismatch. [source; call_f664c705b2dd4fd98039ee1d6f05ceec, call_6bb03f55f29e4f8a879e92acf7ee495e]

## Source Notes

PR #20, “Reka Flash 3 vs padding,” reports quantization shape failures and HumanEval comparisons. Its relationship here is contextual inference from the shared HumanEval evaluation and the existing reka preset, not evidence that it motivated this change. [inference; call_6fcf97e0c93f423ea23dfc127b414784, call_ac621791f366490eb081b691ceca7b32]

<a id="usage-evaluation"></a>

## HumanEval prompt and sampling controls

The chatml preset supplies system/user/assistant delimiters; deepseek uses its User and Assistant markers. Both place the problem in the request and again after an assistant-prefilled Python fence. The existing replacement and tokenizer path encodes special tokens and requests BOS; both presets retain a four-space completion prefix. [source; call_f664c705b2dd4fd98039ee1d6f05ceec, call_ac621791f366490eb081b691ceca7b32]

ComboSampler places penalties first, then temperature, min-p, top-k, top-p and categorical sampling. temp_last moves temperature after the filters, changing the distribution used to select candidates. Temperature zero instead selects argmax after penalties and bypasses those filters. [source; call_78febdf5f7374ade9e5dc5fedfec48d6, call_6bb03f55f29e4f8a879e92acf7ee495e]

Min-p compares each probability against the maximum probability times min_p; zero disables it. Top-k masks sorted positions starting at k and is disabled below one. Repetition penalty 1.0 is neutral. CustomSampler substitutes no-op steps and inserts normalization or sorting prerequisites. [source; call_6bb03f55f29e4f8a879e92acf7ee495e]

The sampler remains shared by the generated jobs. Completion termination, indentation reconstruction, JSONL writing and optional evaluate_functional_correctness invocation are unchanged; the added presets are opt-in through prompt_format. [source; call_ac621791f366490eb081b691ceca7b32, call_f664c705b2dd4fd98039ee1d6f05ceec]

## Authoring-time findings — pending review

### humaneval-top-k-float (suspected; defect)

The new top-k CLI option parses floats, but the selected sampling step uses its value directly as a slice boundary.

Trigger: Run HumanEval with --top_k 5 and nonzero temperature, reaching sampling.

Expected: Retain the five highest-ranked token candidates.

Actual: The parser produces 5.0, which passes the enabled-filter check and reaches SS_TopK.run without integer conversion; its tensor slice is expected to reject that boundary. The default 0.0 is disabled, and temperature zero bypasses top-k.

Locations: 3c9ede55404c8ecce54494657f23f7056ea36a1a:eval/humaneval.py — main, 5d470a29780927c1c8c874609597823f210ae3b9:exllamav3/generator/sampler/custom.py — SS_TopK.run

Source evidence: call_f664c705b2dd4fd98039ee1d6f05ceec, call_78febdf5f7374ade9e5dc5fedfec48d6, call_6bb03f55f29e4f8a879e92acf7ee495e, call_06f099f6aed74000ac89e3dbc18c17b4, call_aaa4136c19994d2f8fc18355ae738d89

source_inspection: Traced the script's __main__ invocation through main, ComboSampler and SS_TopK. Whole-tree SS_TopK construction search found TopKSampler, ComboSampler and an integer-valued test construction. The identified reach is the new HumanEval CLI path, not every sampler user. [call_06f099f6aed74000ac89e3dbc18c17b4, call_78febdf5f7374ade9e5dc5fedfec48d6, call_aaa4136c19994d2f8fc18355ae738d89]. Limits: No generation or tensor-indexing execution.

scalar_transcription: A standard-library reproduction parsed 5 as 5.0 and observed TypeError when using it as a list slice boundary; the default parsed as disabled 0.0. [call_a08e7a54ea57449badf382ec02976e20]. Limits: Models the argument-type mismatch, not repository or GPU execution.

## Uncertainty and limits

No model generation, CUDA sampling or HumanEval scoring was executed; prompt compatibility and benchmark effects remain unmeasured.

The scalar check exercises Python argument parsing and list slicing, not PyTorch tensor indexing or the repository sampler.
