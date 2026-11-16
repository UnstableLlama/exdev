# c0a2028fb579d04491db8427f1e38979a4dcd164


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c0a2028fb579d04491db8427f1e38979a4dcd164) · [Evidence ledger](draft.json)

Repairs perplexity-only finalization by guarding optional KLD work and initializing reference collection state; also updates an example tokenizer path.

- [Make reference-logit evaluation optional at finalization](#usage-evaluation)

## Problem

Perplexity-only evaluation unconditionally divided by a zero KLD count and left collect_logits undefined when no reference filename was supplied. [source; call_2a4f8d3e60294de9b6b6c11a6951dffe]

## Reasoning

The two guards work together: initializing collect_logits prevents an undefined-variable access, while conditioning KLD finalization on logits_file avoids the zero-denominator calculation. Either edit alone would leave the no-reference path broken. [source; call_1bc7d8527a1a4e7bb0182b601fda80c1, call_2a4f8d3e60294de9b6b6c11a6951dffe]

## Impact

For valid nonempty evaluation data, the patched no-reference path can finalize perplexity without calculating, printing or returning KLD. Reference collection and comparison remain available. [source; call_1bc7d8527a1a4e7bb0182b601fda80c1, call_2a4f8d3e60294de9b6b6c11a6951dffe]

## Source Notes

Read the reference-logit introduction entry and the later mask/cache entry. They record the no-reference failure and establish that cache invalidation had already been repaired before this task. [ancestor; call_0e2a0a8fc3f846e28a7ebf0d5db5a4b5, call_0b4253020d964d6f87c93064d86e7627]

Parent source plus the task diff show that the recorded no-reference failure is removed, the three-argument cache invalidation remains, and filtering can still exclude a required reference producer. [source; call_2a4f8d3e60294de9b6b6c11a6951dffe, call_1bc7d8527a1a4e7bb0182b601fda80c1]

<a id="usage-evaluation"></a>

## Make reference-logit evaluation optional at finalization

main supplies logits_file only when a model specification contains out_logits; --kld selects the plotted metric rather than enabling collection. Whole-tree search finds main as the sole direct test_ppl caller. [source; call_2a4f8d3e60294de9b6b6c11a6951dffe, call_42c0ffb59b9548eb811d79c973c672c2]

Perplexity calculation moves outside the ProgressBar context but remains after the row loop. KLD calculation and printing become conditional on logits_file. collect_logits defaults to false, so a perplexity-only run skips saving reference tensors; the result already conditionally included kld. [source; call_1bc7d8527a1a4e7bb0182b601fda80c1, call_2a4f8d3e60294de9b6b6c11a6951dffe]

The inherited KLD branch processes at most ten sequence rows. Reference collection increments its count without accumulating divergence, yielding zero for a nonempty reference run. Comparison accumulates divergence over output positions; perplexity instead uses shifted next-token targets across all rows. These metric definitions are unchanged. [source; call_2a4f8d3e60294de9b6b6c11a6951dffe, call_1bc7d8527a1a4e7bb0182b601fda80c1]

A standard-library transcription reproduced the parent's zero-over-zero failure. With synthetic log-probability sum −6 and count 3, patched finalization produced perplexity 7.389056 without KLD; synthetic reference and comparison cases produced KLD 0 and 0.5 respectively. [execution; call_a273b2ad0db94f2ca6ee1f719c4b1316]

The example data specification changes tokenizer_dir from /mnt/str/eval_models/llama3.2-1b/hf/ to /mnt/str/models/llama3.2-1b-instruct/hf/. get_test_data passes this value to tokenize_transformers, which loads AutoTokenizer from that directory. This selects tokenizer assets, not model weights, and is not a precondition of the finalization repair. [source; call_ccdc6c3cf081481d8235a0701f21c53b, call_b0275c4d37aa42bc87894ad5e2d9d6a5, call_3305d0c3fd45454ba25f04e956c8904c, call_2a4f8d3e60294de9b6b6c11a6951dffe]

## Authoring-time findings — pending review

### inherited-filtered-reference-dependency (suspected; defect)

The inherited mask path can retain reference consumers while excluding their producer; this task does not change that dependency.

Trigger: A mask excludes the out_logits producer, retains an uncached candidate, and the selected reference file is absent.

Expected: Generate the reference or reject the missing dependency before evaluating the candidate.

Actual: main retains logits_file after filtering; test_ppl loads the candidate and then attempts to open the absent reference through load_tensor.

Locations: c0a2028fb579d04491db8427f1e38979a4dcd164:eval/compare_q.py — main

Source evidence: call_2a4f8d3e60294de9b6b6c11a6951dffe, call_1bc7d8527a1a4e7bb0182b601fda80c1, call_42c0ffb59b9548eb811d79c973c672c2

source_inspection: Compared parent reference discovery, filtering and loading with the complete task diff. Whole-tree test_ppl search found main as its only direct caller. [call_2a4f8d3e60294de9b6b6c11a6951dffe, call_1bc7d8527a1a4e7bb0182b601fda80c1, call_42c0ffb59b9548eb811d79c973c672c2]. Limits: No filesystem-library behavior was executed. Existing reference files or cached candidate results avoid this trigger; external caller reach is not established.

## Uncertainty and limits

No model inference, GPU execution, cache access or safetensors round trip was executed; the arithmetic check is a scalar transcription, not execution of test_ppl.

The new tokenizer directory's availability and tokenizer compatibility with evaluated models are unestablished.

The evidence does not establish an empirical rationale for the inherited ten-row KLD cap.
