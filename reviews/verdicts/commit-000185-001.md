# Verdict: commit-000185-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000185-001`
Packet: `.teacher/retrieval/000185-001`
Upstream: `c82af98d57c4ffd21b67baad0eb89a5ed9091759` "New RoPE kernel with fused head norm"
Request: `reviews/requests/commit-000185-001.md` (sha256 `6f7b4c005f775a11bee6c3df9b0b34ac25bb160e90cc6dd52dffa4b05e0dbbc4`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and all six finding groups are true as stated: three introduced by this commit
and three inherited and labelled so. The entry compared the new reduction call with the existing guarded one,
which is how it found the unguarded store.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 45 of 45 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 184 strict-ancestor entries; 2,783 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 45 of 45 recorded tool calls identical, including the `run` call and the one recorded "not in this historical tree" result. |
| Unassisted | Standing instructions byte-identical to 184/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-25T11:33:39Z; my query agrees. Two closed rows by path alone, both selected; all four discussions read are described as path overlap only. |
| Wrapper and callers | `RoPE.apply` gains `q_norm`, `k_norm`, `norm_eps`, `norm_constant_bias` and passes them to `ext.rope`, its only caller. The three attention routes call it in place with the loaded norm weights; `science/kv_quant_exp.py` still passes positions only and gets no normalisation. Correct. |
| Attention | With RoPE present the separate `q_norm.forward` / `k_norm.forward` calls are skipped and the norm weights go to the kernel; without RoPE the separate calls remain. Weights are captured in `load` and cleared in `unload`. Correct. |
| Kernel | One block per token and batch element; x threads rounded up to whole warps, two half values per thread; head copied to shared memory padded to a multiple of 64, optionally normalised, rotated, stored. Normalisation is reciprocal square root of mean square plus epsilon, converted to half, then multiplied by weight plus bias in half. Correct. |
| Test | Now compares returned tensors, both styles, normalisation on and off, tolerance 3e-3 in place of 1e-6, no query-only shapes, one 80-wide shape. Correct. |
| Finding: settings overwritten | `Attention.__init__` sets `norm_eps` and `norm_constant_bias` from `q_norm`, then a few lines later sets them unconditionally to `1e-6` and `0.0`. Gemma 3 builds its head norms with `constant_bias = 1.0`. True; introduced here. |
| Finding: unguarded warp sum | `warp_reduce_sum_f` uses `__shfl_down_sync`, so only lane 0 ends with the warp total; `apply_norm` has every lane write its own result to the same `sums[...]` slot, where `block_reduce_sum_f` writes under `lane_id == 0`. True as a source finding; which write lands is not established, as the entry says. |
| Finding: padded reads | For a head of 80 the launch uses 64 x threads; every thread reads `inv_freq[t]` (40 entries at full width) and, when normalising, a pair at `norm_weight + 2t` (80 entries). True; the padded lanes' results are not stored to the output. |
| Inherited findings | `apply_torch` is unchanged (unconditional K conversion, no partial width); the block-sparse one-line edit changes neither the all-experts buffer count nor the aliasing and dtype behaviour. True. |
| Execution | Lane arithmetic and index counts in Python; labelled as models, not device execution. |

## Not verified

- Any build, test run or GPU execution; which lane's store survives; whether the padded reads fault.

## Must fix before canonical use

1. The native wrapper checks only `q_norm` (dimension and length). The kernel normalises K heads with `k_norm`
   whenever `q_norm` is given, so `q_norm` without `k_norm` dereferences a null pointer, and `k_norm`'s length and
   dtype-by-presence are not tied to the head width. The comment says they must be supplied together; nothing
   enforces it. Attention always passes both.
2. `Attention.__init__` asserts equal epsilon for the two norms but not equal bias; with the overwrite finding
   this is moot today, and should be said once that is fixed.

## Follow-ups

1. Ledger: identities for the three new findings (suspected, source-only; the warp-sum record must keep "store
   order not established"). Affected-revision additions for the inherited ones. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 186.
