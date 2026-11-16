# e1d2fa11d6573ea1aeaddacffc028e08a83f91b1


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/e1d2fa11d6573ea1aeaddacffc028e08a83f91b1) · [Evidence ledger](draft.json)

Adds case-insensitive model-label filtering and repairs evaluation cache invalidation; reference dependencies remain unchecked and the inherited no-reference failure persists.

- [Selective comparison runs and matching cache invalidation](#usage-evaluation)

## Problem

Comparison runs lacked a command-line label filter; cache clearing also omitted the reference-logit argument used in evaluation cache keys. [source; call_4847b060da13498384eea32408647675, call_2591ebe7f57e4ff8857d6e0a97816fe7]

## Reasoning

Filtering before invalidation and evaluation makes the selected models define both operations. Moving invalidation after reference discovery supplies the logits_file argument needed to match evaluation keys. [source; call_4847b060da13498384eea32408647675, call_f542e5d58b3242898d1434a0eee891cb, call_2591ebe7f57e4ff8857d6e0a97816fe7]

## Impact

--mask selects models by case-insensitive substring alternatives separated by semicolons. --clear_cache now targets only retained specifications and includes the full evaluation argument tuple. [source; call_4847b060da13498384eea32408647675]

## Source Notes

The reference-logit introduction entry was read. It records both the cache-key mismatch and a no-reference finalization defect. Inspection shows this change repairs the former but carries over the latter. [source; call_81c07c741bf54d3b9508587f91bd84bf, call_4847b060da13498384eea32408647675, call_f542e5d58b3242898d1434a0eee891cb]

PR #30, “fix: don't add min_p and top_p samplers to stack if falsy,” discusses sampler assertions and disabled values. Its shared word “mask” does not establish a relationship to this model-label filter. [inference; call_9d012106ab1f461abab3adc1a2ba92f6, call_4847b060da13498384eea32408647675]

<a id="usage-evaluation"></a>

## Selective comparison runs and matching cache invalidation

The optional -mask/--mask string is applied after model specifications are loaded and the last out_logits reference is moved first. Matching preserves that ordering, uses uppercase substring comparisons with OR semantics, and does not interpret regular expressions or trim whitespace. An omitted or empty mask bypasses filtering. [source; call_4847b060da13498384eea32408647675, call_f542e5d58b3242898d1434a0eee891cb]

A trailing semicolon introduces an empty substring, which matches every label. The scalar check retained all three sample labels for 'exl3;', retained only EXL3 and EXL2 for 'exl3;exl2', and retained none for ' exl3'. [execution; call_8b198cf92547498e997f3c56dc6653e5]

Reference discovery remains independent of filtering: logits_file survives even when the selected reference model is excluded. Retained candidates can therefore use an existing reference file without evaluating its producer, but the filter does not ensure that file exists. [source; call_4847b060da13498384eea32408647675, call_f542e5d58b3242898d1434a0eee891cb]

The disk cache serializes positional and keyword arguments into its key. Passing data specification, model specification and logits_file to invalidation now matches test_ppl's call, including when logits_file is None. This is a coordinated cache repair, not merely relocation of the old clearing loop. [source; call_4847b060da13498384eea32408647675, call_2591ebe7f57e4ff8857d6e0a97816fe7]

A standard-library transcription verified that the former two-argument clearing key differs from the three-argument evaluation key. [execution; call_8b198cf92547498e997f3c56dc6653e5]

## Authoring-time findings — pending review

### filtered-reference-dependency (suspected; defect)

Filtering can remove the reference producer while retaining its consumers.

Trigger: A mask excludes the out_logits reference but retains an uncached candidate, and the computed reference file does not exist.

Expected: Generate the required reference logits or reject the selection before candidate evaluation.

Actual: main preserves logits_file but removes its producer; test_ppl loads the candidate and then attempts to open the absent reference file.

Locations: e1d2fa11d6573ea1aeaddacffc028e08a83f91b1:eval/compare_q.py — main

Source evidence: call_4847b060da13498384eea32408647675, call_f542e5d58b3242898d1434a0eee891cb

source_inspection: Traced CLI main through filtering to test_ppl and load_tensor. Whole-tree searches found main as the sole direct test_ppl caller and no compare_q importer. [call_b5e5461b4ea04a08af8f54a321af5b68, call_72d97861c3be4144b732ef7af5521b59, call_f542e5d58b3242898d1434a0eee891cb]. Limits: No filesystem-library execution; an existing reference file or cached candidate result avoids this trigger.

### inherited-no-reference-finalization (suspected; defect)

The existing no-reference finalization failure remains unchanged.

Trigger: An uncached evaluation completes its forward passes with nonempty valid data and logits_file=None.

Expected: Return perplexity without requiring reference logits.

Actual: kl_div_count remains zero and unconditional finalization divides 0.0 by 0.0. collect_logits is also left uninitialized, although division fails first.

Locations: e1d2fa11d6573ea1aeaddacffc028e08a83f91b1:eval/compare_q.py — test_ppl

Source evidence: call_f542e5d58b3242898d1434a0eee891cb, call_4847b060da13498384eea32408647675

source_inspection: The unchanged test_ppl body remains reachable from main, its only direct caller found by whole-tree search, independently of the plotting flag --kld. [call_b5e5461b4ea04a08af8f54a321af5b68, call_f542e5d58b3242898d1434a0eee891cb]. Limits: Model inference was not executed.

scalar_transcription: Evaluating the final zero-over-zero expression raised ZeroDivisionError. [call_8b198cf92547498e997f3c56dc6653e5]. Limits: This arithmetic check did not execute test_ppl.

## Uncertainty and limits

No model evaluation, GPU execution, shelve invalidation or safetensors access was executed. Standard-library checks transcribed filtering, serialization and arithmetic only.

Caller reach is established for the inspected comparison script and literal repository searches, not external integrations.
