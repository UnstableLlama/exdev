# Verdict: commit-000096-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000096-001`
Packet: `.teacher/retrieval/000096-001`
Upstream: `a2ae48308aa813c67058c01f21bd4ab656a21d7a` "Add parallel decoder module"
Request: `reviews/requests/commit-000096-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry explains what "parallel" means here (shared input, not concurrency),
spots that prefill behaves differently from the existing block, and both findings hold at source level.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 20 of 20 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 95 strict-ancestor entries; 1,283 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 20 of 20 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 95/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 21, 22, 24. Matches the nine open rows. |
| Reference evidence | Not triggered, correctly: no architecture is registered. |
| Forward claims | `y = input_norm(x)` at half precision; `x += attn(y)`; return if `params.get("prefill")`; `x += mlp(y)`; `to2(x, out_dtype, self.out_dtype)`. The MLP takes `y`, not the updated residual. Correct. |
| Prefill comparison | `TransformerBlock.forward` returns on prefill before `x += y`; the new block returns after adding the attention output. `Model.prefill` sets the flag only for `idx == last_kv_module_idx` and breaks there, so the returned value is discarded either way. Correct, and the entry does not overstate it. |
| Constructor claims | The base constructor is given `None` for the qmap, so the `qmap` argument is unused; the three components are registered as submodules; `num_slices` comes from the MLP or is 1. `TransformerBlock.mlp_norm`'s annotation gains `LayerNorm`; its body is unchanged. Correct. |
| Finding `optional-components-forward` | Correct. All three components default to `None`, `get_name` labels a block with neither branch "(no-op)", and `forward` calls `.forward` on each without a check. `allocate_q` does handle the empty case. |
| Finding `plain-mlp-allocation` | Correct. `allocate_q` reads `self.mlp.ups` and `self.mlp.downs` whenever an MLP is present; plain `MLP` defines `up` and `down`. `TransformerBlock.allocate_q` has the same two lines, so this is a copy of an existing mismatch, as the entry says. |

## Not verified

- Any execution.
- Whether an existing ledger record covers the `TransformerBlock` instance of the plain-MLP mismatch. I found none by
  file name.

## Must fix before canonical use

Reviewer-only.

1. `plain-mlp-allocation` has two sites, one new here and one older in `TransformerBlock`. The ledger should hold one
   defect with both, and the older site needs its introducing commit established; this run does not establish it.

## Next

1. Record this approval.
2. Continue the walk at commit 97.
