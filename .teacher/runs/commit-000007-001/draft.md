# 95b4da216a7e911e0e578c241765f07934aa1f1a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/95b4da216a7e911e0e578c241765f07934aa1f1a) · [Evidence ledger](draft.json)

Adds per-row cleanup and CUDA cache clearing to perplexity comparisons, plus an explicit final progress update.

- [Per-row cleanup and evaluation completion](#usage-evaluation)

## Problem

The comparison evaluator retained input_ids through the end of each row and performed no per-row CUDA cache clearing. Its progress updates stopped at rows - 1 rather than explicitly reaching the total. [source; call_41d65f5292464960b19440f5ab11a760]

## Reasoning

The change places cleanup after the relevant tensors' last uses and adds a final progress update without changing likelihood accumulation or the perplexity formula. [source; call_7d8778037b8f452095a51ab9977394ce]

## Impact

Evaluation now requests CUDA cache clearing after every scored row and explicitly reports completion before calculating perplexity. [source; call_7d8778037b8f452095a51ab9977394ce]

## Source Notes

The ancestor explanation establishes compare_q.py as a cached, multi-backend perplexity comparison runner; this patch modifies its shared evaluation loop rather than a backend adapter. [source; call_d2ae4f30f0f44b99926ee4096add5db5, call_7d8778037b8f452095a51ab9977394ce]

<a id="usage-evaluation"></a>

## Per-row cleanup and evaluation completion

test_ppl obtains each input row from eval_ids, forwards it through the selected backend, and gathers next-token log probabilities. The new del input_ids follows creation of target_ids, so subsequent scoring uses target_ids rather than the deleted local reference. eval_ids itself remains alive until evaluation finishes; deleting the row reference does not establish that its backing storage is freed. [source; call_41d65f5292464960b19440f5ab11a760, call_7d8778037b8f452095a51ab9977394ce]

torch.cuda.empty_cache() is called after the row's probability sum and target count have been accumulated and target tensors deleted. This moves cache-clearing requests inside the loop instead of relying solely on the existing end-of-evaluation free_mem() call. [source; call_41d65f5292464960b19440f5ab11a760, call_7d8778037b8f452095a51ab9977394ce]

Per-row cache clearing favors releasing reusable allocator capacity between forwards over retaining it for later rows. Whether that tradeoff reduces memory pressure or increases evaluation time depends on the backend and workload. [inference; call_7d8778037b8f452095a51ab9977394ce]

ProgressBar.update interprets its argument as an absolute completed count. The existing loop reports zero-based row indices before processing each row; the added pb.update(rows) reports the full total after the loop. This matters because the default transient progress bar does not automatically set completion in __exit__; that automatic update is restricted to non-transient bars. [source; call_18f9e0e3e3a3402b91018ba0678cbc4d, call_41d65f5292464960b19440f5ab11a760, call_7d8778037b8f452095a51ab9977394ce]

## Uncertainty and limits

No evaluator or CUDA workload was run. Memory savings, allocator overhead and displayed progress timing were not measured.

A scalar computation would not establish CUDA allocator behavior or Rich rendering; the changed operations introduce no numerical formula requiring a scalar check.
