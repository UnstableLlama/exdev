# afac0a4320d9c4df31a8747ad1061da521698117


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/afac0a4320d9c4df31a8747ad1061da521698117) · [Evidence ledger](draft.json)

Pairs K/V increments in two allocation candidates, but a remaining unequal candidate prevents a universal equality guarantee.

- [Pair K/V increments in the allocation heuristic](#conversion)

## Problem

The stated goal is equal K/V projection bitrates; two existing allocation candidates increased V alone. [source; call_2305816f3c424e77800e5a040e28b0bc]

## Reasoning

The change raises K's increment to match V in two Q/K/V/O patterns, replacing [0,0,1,0] and [0,0,2,0] with [0,1,1,0] and [0,2,2,0]. It changes the candidate search space rather than enforcing equality after selection. [source; call_2305816f3c424e77800e5a040e28b0bc, call_f8ecb2a14e2343669b960c63e6713c58]

## Impact

For those candidates, matching K to V costs additional bits proportional to K's weight count. This can change the selected allocation and the surplus returned to the caller; MLP-only allocation is unaffected. [source; call_f8ecb2a14e2343669b960c63e6713c58, call_2305816f3c424e77800e5a040e28b0bc]

## Source Notes

The root conversion entry describes allocation as a fixed size-based heuristic rather than a calibration-error search, and records an exact-budget selection boundary. [ancestor; call_d3e43f3e396344aaa1295c43ae55f0c1]

<a id="conversion"></a>

## Pair K/V increments in the allocation heuristic

allocate_transformer orders attention projections as Q/K/V/O. Its pattern entries are integer bitrate increments above floor(effective budget per weight), with a minimum base of one and a per-projection cap of eight. Attention and MLP candidates are combined, costed using projection weight counts, and sorted for budget selection. [source; call_f8ecb2a14e2343669b960c63e6713c58]

Both direct callers, TransformerBlock.allocate_q and ParallelDecoderBlock.allocate_q, pass their attention projections in that order and return the strategy and surplus unchanged. They bypass allocation only when both attention and MLP are absent. [source; call_3d418e2f67224b9985cdc583145f4bd1, call_4e8ae04fca8b491d80ab31f83eea28fe]

With four 128-weight attention projections, target 3 and incoming surplus 383, the extracted parent allocator returned Q/K/V/O = 3/3/5/3; applying the patch returned 3/4/4/3. Both returned surplus 128: this example redistributes the same bit cost from V to K. [execution; call_ae68911a0b9a4bf0ac437a5ec3a34756]

The patch leaves both the unequal [0,1,2,1] candidate and the inherited exact-cost bisect boundary intact. Thus the change does not establish universal K/V equality or correct the previously documented budget boundary. [source; call_f8ecb2a14e2343669b960c63e6713c58, call_2305816f3c424e77800e5a040e28b0bc]

## Authoring-time findings — pending review

### remaining-unequal-kv (suspected; defect)

A retained candidate can still allocate different K and V bitrates, contrary to the commit's stated goal.

Trigger: Attention-only allocation with Q/K/V/O weight counts 256/128/128/256, target 3 and incoming surplus 640.

Expected: K and V receive equal bitrates if the stated goal is universal.

Actual: The patched allocator selects 3/4/5/4 and returns surplus 1.

Locations: afac0a4320d9c4df31a8747ad1061da521698117:exllamav3/conversion/allocation.py — allocate_transformer

Source evidence: call_f8ecb2a14e2343669b960c63e6713c58, call_2305816f3c424e77800e5a040e28b0bc, call_4e8ae04fca8b491d80ab31f83eea28fe

repository_execution: Executed the extracted parent function with the two task substitutions and synthetic objects providing keys and weight counts. [call_a3aa1d3a7efd4f9e9581298e45dd4e92]. Limits: Not a complete conversion. Both inspected block callers expose this allocator; occurrence of these budgets in real models was not measured.

### inherited-exact-budget-boundary (suspected; defect)

The inherited exact-cost candidate exclusion remains unchanged.

Trigger: Four 128-weight attention projections, target 3 and incoming surplus 255 yield budget 1792, exactly matching the patched 3/4/4/3 candidate.

Expected: Select the largest candidate within budget, including an exact match.

Actual: bisect_right searches with (budget,), which sorts before equal-cost two-element tuples; allocation instead returns 3/3/3/3 with surplus 256.

Locations: afac0a4320d9c4df31a8747ad1061da521698117:exllamav3/conversion/allocation.py — allocate_transformer

Source evidence: call_f8ecb2a14e2343669b960c63e6713c58, call_2305816f3c424e77800e5a040e28b0bc, call_3d418e2f67224b9985cdc583145f4bd1

repository_execution: Executed the extracted, patched allocator on the exact-budget example. [call_ae68911a0b9a4bf0ac437a5ec3a34756]. Limits: Synthetic projection objects only. The condition applies through either inspected block caller when its budget matches a candidate cost.

## Uncertainty and limits

No model conversion, GPU execution, quality evaluation or performance measurement was performed. Checks executed an extracted allocator with synthetic projection objects and the two substitutions applied in memory.
