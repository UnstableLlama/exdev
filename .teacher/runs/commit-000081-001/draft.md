# 46f98ca32ddf1ad82b3deeff5a2744ef9f11f1e5


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/46f98ca32ddf1ad82b3deeff5a2744ef9f11f1e5) · [Evidence ledger](draft.json)

Documents sampling-step roles and future optimization work without changing execution; the top-p description conflicts with its cutoff logic, and sorted argmax remains unchanged.

- [Document sampling steps without changing execution](#sampling)

## Problem

Sampling-step classes lacked short descriptions of their roles. [source; call_f2c6a3b52b0747b3a78d6c26fa273212]

## Reasoning

The change adds nine class docstrings and a TODO about removing redundant steps and fusing operations; it does not implement those optimizations. [source; call_f2c6a3b52b0747b3a78d6c26fa273212]

## Impact

Sampling computations, defaults and interfaces remain unchanged. The new top-p description does not match the existing cutoff implementation. [source; call_f2c6a3b52b0747b3a78d6c26fa273212, call_9542b9bdcbd84be9882f37889c84dfc5]

## Source Notes

The parent annotation identified a sorted-argmax assignment problem. [ancestor; call_68222b7dc1544971bb620caf007579d4]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” discusses extension loading. Issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” discusses quantization and regularization; neither discussion states a connection to this comments-only change. [source; call_db2d80579077475f82610cb50cbcdbb0, call_aab5f84dadc34259a702f9036fae7bf3]

<a id="sampling"></a>

## Document sampling steps without changing execution

The descriptions distinguish no-op, greedy selection, categorical sampling, temperature scaling, normalization, sorting and three truncation filters. SS_Sample adds Gumbel noise through extension calls before argmax and maps sorted positions back to token IDs. [source; call_f2c6a3b52b0747b3a78d6c26fa273212, call_9542b9bdcbd84be9882f37889c84dfc5]

Temperature divides logits or raises probability weights to the reciprocal temperature. Normalization uses softmax for logits and division by row sums for weights. Sorting records token indices alongside descending values; its new docstring ends with the unexplained fragment “state.indices”. [source; call_9542b9bdcbd84be9882f37889c84dfc5, call_f2c6a3b52b0747b3a78d6c26fa273212]

Top-k masks sorted positions after K, using zero for probabilities or negative infinity for logits. Min-p instead retains probabilities greater than or equal to min_p times the row maximum, so equality survives and sorting is unnecessary for its unsorted branch. [source; call_9542b9bdcbd84be9882f37889c84dfc5]

CustomSampler inserts prerequisites requested by each step, executes the resulting list and reshapes the final sample. Its construction-time planning state remains INIT throughout, while runtime steps track normalization and sorting. The new TODO proposes future redundancy elimination and fusion rather than changing this mechanism. [source; call_9542b9bdcbd84be9882f37889c84dfc5, call_f2c6a3b52b0747b3a78d6c26fa273212]

For probabilities [0.5, 0.25, 0.125, 0.125] and P=0.625, a scalar transcription retained only mass 0.5; the newly documented smallest prefix exceeding P would retain mass 0.75. [execution; call_445cf23a99ba4d91af3d64e94de7d7b6]

## Authoring-time findings — pending review

### top-p-description-mismatch (suspected; defect)

The new top-p docstring promises a crossing token that the existing implementation generally excludes.

Trigger: A normalized sorted distribution crosses P after its first token, for example [0.5, 0.25, 0.125, 0.125] with P=0.625.

Expected: Under the new description, retain the smallest leading set whose cumulative probability exceeds P: the first two tokens in this example.

Actual: The implementation preserves the first token unconditionally and retains subsequent tokens only when their inclusive cumulative probability is <= P, leaving just the first token in this example.

Locations: 46f98ca32ddf1ad82b3deeff5a2744ef9f11f1e5:exllamav3/generator/sampler/custom.py — SS_TopP.run

Source evidence: call_f2c6a3b52b0747b3a78d6c26fa273212, call_9542b9bdcbd84be9882f37889c84dfc5, call_5fa3b32a28624378ab7b44634f95ef02, call_e4ef472467b24b539983c7c84450a82b

source_inspection: Whole-parent-tree search found TopPSampler constructing this step in both temperature-order branches. CustomSampler.forward directly invokes step.run. The existing preset docstring describes <= P with at least one candidate; DefaultSampler uses min-p instead. [call_5fa3b32a28624378ab7b44634f95ef02, call_e4ef472467b24b539983c7c84450a82b, call_9542b9bdcbd84be9882f37889c84dfc5]. Limits: External custom compositions were not inventoried.

scalar_transcription: Computed inclusive cumulative sums and reproduced the unshifted mask, then compared it with the documented crossing-prefix rule. [call_445cf23a99ba4d91af3d64e94de7d7b6]. Limits: Standard-library scalar model, not repository execution.

### inherited-sorted-argmax (suspected; defect)

The sorted-argmax problem identified in the parent annotation is carried over unchanged despite the new selection docstring.

Trigger: A custom chain reaches SS_Argmax.run with sorted logits or probabilities.

Expected: Map each row's selected position to its token ID and populate state.sample.

Actual: Sorted branches assign indexed values to state.state instead of state.sample, then overwrite state.state with DONE. If indexing completes, forward still cannot reshape the unset sample.

Locations: 46f98ca32ddf1ad82b3deeff5a2744ef9f11f1e5:exllamav3/generator/sampler/custom.py — SS_Argmax.run

Source evidence: call_9542b9bdcbd84be9882f37889c84dfc5, call_f2c6a3b52b0747b3a78d6c26fa273212, call_d6b9528255a1468790eedcf55aea9614, call_e4ef472467b24b539983c7c84450a82b

source_inspection: Compared parent implementation with the comments-only diff. Whole-parent-tree SS_Argmax search and preset inspection found built-in constructions starting directly from INIT; CustomSampler.forward is the direct step runner. Reach therefore includes custom sorted-greedy chains, not the inspected built-in greedy branches. [call_9542b9bdcbd84be9882f37889c84dfc5, call_f2c6a3b52b0747b3a78d6c26fa273212, call_d6b9528255a1468790eedcf55aea9614, call_e4ef472467b24b539983c7c84450a82b]. Limits: No runtime reproduction or external caller inventory.

## Uncertainty and limits

The numerical check transcribes the cutoff using standard-library Python, not PyTorch or CUDA; its binary-exact inputs avoid rounding ambiguity.

No repository execution, sampling-frequency measurement or performance benchmark was performed.
