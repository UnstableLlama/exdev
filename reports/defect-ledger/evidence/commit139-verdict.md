# Verdict: commit-000139-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000139-001`
Packet: `.teacher/retrieval/000139-001`
Upstream: `6fc153d7a062aa7f53fe13b27d008c2d90d8d62f` "Add block-sparse MLP module"
Request: `reviews/requests/commit-000139-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is correct. The entry reads all six sections, describes both
execution paths accurately, and is careful about what the commit does not do: no architecture uses the module yet
and the all-expert flag is off by default. I found two further points by reading the source (reviewer section);
the entry's limits touch one of them without drawing the conclusion.

The ledger record `exllamav3-in-memory-weight-transpose--r001` is **accepted**.

## Artifacts reviewed (sha256)

All sixteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 20 of 20 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 138 strict-ancestor entries; 1,976 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 20 of 20 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 138/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows, as at 138 (issue 33 was closed at this cutoff, 2025-05-11T13:34:50Z). One closed row, pull request 20, closed 2025-04-25. Issue 7's last comment is from 22 April. |
| Architecture trigger | Does not fire, correctly: no model file names the new module. |
| New file | `modules/block_sparse_mlp.py` has no same-stem sibling. |
| Routing | Router `Linear` to `num_experts` scores, softmax, `topk` of `num_experts` when `activate_all_experts` else `num_experts_per_tok`, renormalise. Correct. |
| Ordinary path | Taken when more than one flattened token or not fully EXL3. One-hot mask, per expert `gate`, `up`, `activation_fn_call(g, u, u)`, `down`, times the routing weight, `index_add_`. The activation is `ext.silu_mul` or `ext.gelu_mul`. Correct. |
| Fused path | One token and `is_quantized`. `MultiLinear` asserts EXL3, no bias, no softcap, unit post-scale, equal `K` and dimensions, and collects three pointer tables. Three `exl3_mgemm` calls (gate, up, down) with `selected_experts`, weights only on the last, shape index -1; then `out_d.sum(dim = 0)`. Correct. |
| `is_quantized` | True only when every gate, up and down is EXL3; a mixture prints a warning and uses the ordinary path. Correct. |
| Calibration maps | Gate and up of every expert share `qmap + ".input"`; each down has `qmap + ".{idx}.down"`. `Linear.capture_H` adds to `H` only when the key equals the map's `first_key`. Correct. |
| Conversion | The capture pass sets `activate_all_experts` from `model.calibration_all_experts` (default `False`, set in `Model.__init__`); when it is true the reference state is recomputed without it. Correct. |
| Allocation | `.experts.0.` becomes `.experts.*.` in both branches; both decoder blocks pass `gates` for `BlockSparseMLP` as for `GatedMLP`. Correct. |
| Native check | `exl3_mgemm` requires `indices.size(1) == C.size(0)`. Correct. |
| Execution | Recorded output: indices (1, 2) against two output slices pass; (1, 8) against two fail. Matches the prose. |
| Finding `all-expert-fused-shape` | Correct. With one token, a fully EXL3 module and the flag set, `topk` returns `num_experts` indices while the four buffers are sized by `num_experts_per_tok`, so the first `exl3_mgemm` call fails its check. The conversion capture pass does not reach it (the module is not yet quantized there and sees many tokens), which the entry says. |
| Ledger `in-memory-weight-transpose--r001` | Accepted. Fix-derived, introduced `647bb7d5`, fixed `538dcae3`, consequences stated as source reading only, float-to-half and padding gaps expressly not claimed fixed. |

## Reviewer-only notes (never to a teacher)

All by source reading; nothing was run.

- **Fused path and the default intermediate dtype (mine).** `interm_dtype` defaults to `None`. In the ordinary
  path that is harmless: the gate and up `Linear`s fall back to half. In the fused path `torch.empty(...,
  dtype = None)` allocates float32, `exl3_mgemm` then writes float32 gate and up outputs, and `silu_mul` or
  `gelu_mul`, which have no dtype check and read their arguments as half, reinterpret those bytes. The result is
  silently wrong unless the caller passes `interm_dtype = torch.half`, as the two existing gated-MLP
  architectures do. The entry's last limit ("broader intermediate-dtype compatibility is not established") is the
  same spot. Worth a reviewer-observation record.
- **Default calibration feeds the shared input map from one expert (mine).** Because only the map's first key
  accumulates `H`, and all experts' gates and ups share one map, with the flag off the shared Hessian is built
  only from the tokens routed to whichever expert ran first. An expert that receives no calibration token gets no
  entry for its down map at all. The new comment in `convert_model.py` says as much. So an architecture that uses
  this module needs `calibration_all_experts = True`; check that when one is registered.
- **Padding.** `Linear` rounds both feature counts up to a multiple of 128, and the down projection is created
  with `allow_input_padding`. The fused path sizes its buffers from the unpadded `hidden_size` and
  `intermediate_size`. Models whose sizes are not multiples of 128 would not fit; untested and probably moot for
  the intended models.
- **Earlier multi-GEMM records.** The fused path is the first caller of `exl3_mgemm`. It satisfies the scratch
  requirement from 135 (`yh` has one slice per selected expert) and passes matching leading dimensions. The down
  call uses its input as its own scratch, with one slice per plane, which is in-place per plane and not the race
  I noted at 135.

## Not verified

- Any execution, and numerical agreement between the two paths.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: `all-expert-fused-shape` approved as drafted, introduced at `6fc153d7`.
2. Ledger: a reviewer-observation record for the fused path's intermediate dtype, introduced at `6fc153d7`,
   conditional on a caller leaving `interm_dtype` unset or not half. Excluded from historical context and training
   like the other reviewer records.
3. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the ledger acceptance.
2. Continue the walk at commit 140.
