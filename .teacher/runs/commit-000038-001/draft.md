# 29060addb5a3994cec3867e1f2f6b30ecda7b8a3


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/29060addb5a3994cec3867e1f2f6b30ecda7b8a3) · [Evidence ledger](draft.json)

Repairs negative weighted GPU tile shares by propagating deficits backward, preserving the total and allowing existing zero-work guards to handle emptied devices.

- [Repair negative multi-GPU tile shares](#quantizer)

## Problem

Weighted multi-GPU allocation rounds individual shares to multiples of 16 tiles, then assigns the discrepancy to the last device. Earlier shares can exceed the available tiles, leaving a negative final split before torch.split. [source; call_c6f56dda4e4b4adcb8ecb175231b53a5]

## Reasoning

The patch walks backward through the shares, subtracting each negative share from its predecessor and setting the negative share to zero. Backward traversal allows a deficit to propagate across several devices. [source; call_3c4568c551b348c1b04001040ce35d0a]

## Impact

The corrected partition is used consistently for input tiles, reconstructed tiles and indices. Existing positive-share guards skip quantization for devices reduced to zero work. [source; call_3c4568c551b348c1b04001040ce35d0a, call_c6f56dda4e4b4adcb8ecb175231b53a5]

## Source Notes

The earlier weighted-allocation entry identified the negative-final-share case. Inspection of the parent and this patch shows that the allocation defect is addressed rather than carried over for nonnegative ratios with a positive sum. [source; call_c6f56dda4e4b4adcb8ecb175231b53a5, call_3c4568c551b348c1b04001040ce35d0a]

The earlier entry records the illustrative 32-tile, [3,3,3,1] ratio case as a suspected defect. [ancestor; call_152bdc1e0d604be5b738125789aa3b9b]

<a id="quantizer"></a>

## Repair negative multi-GPU tile shares

The repair runs after both allocation branches and before all three pinned-buffer splits. Equal splitting already produces nonnegative shares for a nonempty device list; single-device execution bypasses this code entirely. [source; call_c6f56dda4e4b4adcb8ecb175231b53a5, call_3c4568c551b348c1b04001040ce35d0a]

Each adjustment preserves the total tile count. Unlike simply clamping the last share to zero, it also removes the excess assigned elsewhere. It preferentially reduces later devices rather than recomputing proportional shares, so requested ratios remain approximate. [inference; call_3c4568c551b348c1b04001040ce35d0a, call_c6f56dda4e4b4adcb8ecb175231b53a5]

Scalar transcription changed 32 tiles with ratios [3,3,3,1] from [16,16,16,-16] to [16,16,0,0]. A cascading case changed [16,16,16,16,16,-32] to [16,16,16,0,0,0]. Across 175,440 cases covering 0–128 tiles, 2–5 devices and integer ratios 1–4, every corrected partition was nonnegative and preserved its total; already-valid partitions were unchanged. [execution; call_c5a8c7f4e979406da7f348915aab4a59]

Whole-parent-tree search found direct calls from ldlq and g_scale_gss.test_scale. LDLQ supplies size_n/16 tiles per call, each containing 256 values, so width 512 supplies the illustrative 32 tiles. Scale-search trials share the same repair; the separate synchronous splitter is unchanged. [source; call_60ff930585c14df0b9e880e09bf7137b, call_c6f56dda4e4b4adcb8ecb175231b53a5, call_3c4568c551b348c1b04001040ce35d0a]

## Uncertainty and limits

Checks executed scalar Python transcriptions, not repository quantization, torch.split or CUDA kernels; end-to-end success and performance remain unmeasured.

The inspected source establishes 16-tile rounding granularity but does not explain its rationale. Allocation guarantees here assume nonnegative ratios with positive sum and a ratio count matching the devices.
