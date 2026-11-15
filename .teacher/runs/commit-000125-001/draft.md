# 57a37f2658fa2b3deac5e3404d2df7120223a69a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/57a37f2658fa2b3deac5e3404d2df7120223a69a) · [Evidence ledger](draft.json)

Integrates ChatML and DeepSeek HumanEval prompts and ComboSampler controls, retaining a suspected enabled-top-k CLI type mismatch.

- [HumanEval prompt and sampling integration](#usage-evaluation)

## Problem

HumanEval exposed only temperature and top-p and lacked ChatML and DeepSeek prompt presets. [source; call_6a9b49d7b06547a98107727f009e2245]

## Reasoning

The merge integrates PR #32 by replacing TopPSampler with the existing ComboSampler and adding two opt-in prompt formats, rather than implementing evaluation-specific sampling filters. [source; call_74011aec943f41a095c750e0b6ac82e8, call_1bc1d290f054475e8af3840cb83c9ed8, call_1d05f96919a94f63858e80480fb91e96]

## Impact

New CLI controls expose min-p, top-k, repetition penalties and temperature-last. Defaults retain temperature 0.6 and top-p 0.6, with the additional filters neutral or disabled. [source; call_1bc1d290f054475e8af3840cb83c9ed8, call_199b35ebd0734b958d6af17d185c1f68]

## Source Notes

The supplied merge comparison establishes that the tree is identical to second parent 3c9ede55404c8ecce54494657f23f7056ea36a1a: these are first-parent integration changes, not additional merge-only content. [source; call_74011aec943f41a095c750e0b6ac82e8, call_1bc1d290f054475e8af3840cb83c9ed8]

PR #32 is attributed to gakada; its available body is empty and supplies no further rationale or benchmark evidence. [source; call_82a425bbac744b77afc11eb543d1eb1a]

The second-parent annotation already records the top-k argument-type concern. [ancestor; call_eb70f8b0d3a04753ac64556ff206da20]

<a id="usage-evaluation"></a>

## HumanEval prompt and sampling integration

Both new presets repeat the problem in the request and an assistant-prefilled Python fence. ChatML supplies system/user/assistant delimiters; DeepSeek uses its User and Assistant markers. Existing encoding requests special-token recognition and BOS, and output reconstruction retains a four-space completion prefix. [source; call_1bc1d290f054475e8af3840cb83c9ed8, call_6a9b49d7b06547a98107727f009e2245]

ComboSampler places penalties before temperature, min-p, top-k, top-p and categorical sampling. temp_last moves temperature after the filters; temperature zero instead selects argmax after penalties and bypasses filtering. CustomSampler substitutes no-ops and inserts sorting or normalization prerequisites. [source; call_1d05f96919a94f63858e80480fb91e96, call_199b35ebd0734b958d6af17d185c1f68]

Min-p uses the largest probability times min_p as its cutoff; zero disables it. Top-k masks sorted positions starting at k and is disabled below one. Repetition penalty 1.0 is neutral. Thus temperature-last changes which distribution supplies probability-based filtering thresholds. [source; call_199b35ebd0734b958d6af17d185c1f68, call_1d05f96919a94f63858e80480fb91e96]

The same sampler is passed to each job. Completion termination, JSONL writing and optional functional-correctness evaluation are unchanged by this merge. [source; call_6a9b49d7b06547a98107727f009e2245, call_1bc1d290f054475e8af3840cb83c9ed8]

## Authoring-time findings — pending review

### humaneval-top-k-float (suspected; defect)

The integrated CLI retains the second parent's float-valued top-k mismatch.

Trigger: Run HumanEval with --top_k 5 and nonzero temperature, reaching sampling.

Expected: Keep the five highest-ranked candidates.

Actual: The parser produces 5.0, which passes the enabled-filter check and reaches SS_TopK.run unchanged as a tensor slice boundary, expected to raise TypeError. Default 0.0 disables this step; temperature zero bypasses it.

Locations: 57a37f2658fa2b3deac5e3404d2df7120223a69a:eval/humaneval.py — main, 5d470a29780927c1c8c874609597823f210ae3b9:exllamav3/generator/sampler/custom.py — SS_TopK.run

Source evidence: call_1bc1d290f054475e8af3840cb83c9ed8, call_199b35ebd0734b958d6af17d185c1f68, call_1d05f96919a94f63858e80480fb91e96

source_inspection: Traced the script entry through main and ComboSampler. Whole-parent-tree SS_TopK construction search found TopKSampler, ComboSampler and an integer-valued test construction. The affected reach is the new HumanEval CLI path, not all sampler users. [call_6a9b49d7b06547a98107727f009e2245, call_2e9df6be499042938d7d6b1454db7720, call_52161b083daf40269a29edfaa34075e9, call_1d05f96919a94f63858e80480fb91e96]. Limits: No tensor-indexing execution.

scalar_transcription: A standard-library reproduction parsed 5 as 5.0 and observed TypeError when slicing a list; the default remained disabled. [call_7f42520f00f848ea8157eeab28718969]. Limits: List slicing models the type mismatch but does not execute PyTorch or GPU sampling.

## Uncertainty and limits

No model generation, PyTorch indexing, CUDA sampling or HumanEval scoring was executed; prompt compatibility and benchmark effects remain unmeasured.

The bounded execution checks argparse and Python list slicing, not the repository sampler.
