# Verdict: commit-000201-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000201-001`
Packet: `.teacher/retrieval/000201-001`
Upstream: `91c7cc41881c50abf6608a07c53b9d888c9cf2a6` "Cohere: Add support for optional QK norms (only used by Command-R+)"
Request: `reviews/requests/commit-000201-001.md` (sha256 `6b8a522e443a26233bf2059c28dd95d01689c4c6a1ab853515cb084786c6bd9c`)
Reviewed: 2026-11-16, working tree on top of `e9e83ff`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. No findings are filed and I have none to add.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 31 of 31 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 200 strict-ancestor entries; 2,925 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 31 of 31 recorded tool calls identical, including the ten `hf_fetch` calls and the `run` call. |
| Unassisted | Standing instructions byte-identical to 200/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fifteen open rows at 2025-05-30T14:58:48Z; my query agrees. One closed row selected; discussion links are called inferences. |
| The change | `use_qk_norm` read with type `int` and default `False`; when set, each layer's attention gets a LayerNorm at `self_attn.q_norm` and one at `self_attn.k_norm` with the model's epsilon; every Cohere `GatedMLP` now gets `out_dtype = torch.float`, whatever the flag. Correct. |
| The path used | LayerNorm leaves the fused-norm tensors `None`, so the 200 truth-value condition short-circuits safely and `LayerNorm.forward` (not `forward_torch`) runs before RoPE. Correct, and the entry rightly does not claim the 200 findings are fixed. |
| MLP dtype | `out_dtype` reaches the down projections and the final conversion; the intermediate dtype is separate; the parallel block adds the result into `x` in place and returns early on prefill. Correct. |
| Configurations | Agrees with what I recomputed from the same ten configurations at 98: the three Plus models set the flag, five set it false, the two v01 ones omit it. |
| Fix attribution | The 98 finding `cohere-qk-normalization` (flag never read, no such step) is addressed by this wiring. True. |
| Execution | The repository's `read_dict` run on four inputs, plus three integer divisions; labelled as bounded. |

## Reviewer knowledge (never to a teacher)

From the tensor headers I read at 98, the Plus checkpoints store `q_norm.weight` as [96, 128] with no bias, so
they take the multidimensional branch added at 200, and that shape broadcasts against Q reshaped to heads ×
head width. The entry says tensor headers were not read, which is accurate for this run.

## Not verified

- Model loading, generation or any PyTorch execution; whether the float32 MLP output survives the in-place add
  into the residual, which depends on the residual's dtype.

## Must fix before canonical use

None.

## Follow-ups

1. Ledger: `cohere-qk-normalization` may take this commit as its fix. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 202.
