# Verdict: commit-000270-001 (teacher Sol, guidance 12, unassisted; ran ahead of 269; validation-repaired)

Reviewer: Fable. Date: 2026-11-17 (08:19 UTC). Upstream `b8c830c1` "BlockSparseMLP: Add DS3/Dots routing".
Run: `.teacher/runs/commit-000270-001`. Packet: `.teacher/retrieval/000270-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. All five findings are accepted
as true as stated: `native-router-argument-mismatch`, `grouped-routing-unassigned` and
`optional-inputs-required-by-dots` (a new requirement) are new; the all-expert cardinality and plain
shared-MLP allocation findings are observations of existing identities. The entry made the commit's central
checks itself: it compared the changed native call with the binding, and it noticed that only the
single-group route is wired up.

**It stands although it ran ahead of 269, which changes the same file.** The 269 entry's new finding is the
half accumulator receiving float expert output. This entry, without seeing that, describes the same line
from the source: the accumulator now takes `self.out_dtype`, matching Qwen3 MoE's float down output. It
also notes that the fused early return is gone, so the shared addition is now reachable. Both fixes are
described correctly; only the cross-reference to 269 is missing.

## Validation repair

Checked by me from the transcript: refused annotation at index 64 ("Unknown or unsuccessful evidence
call"), that message returned verbatim at 66, one further `repo_read`, final annotation at 69. The same
five findings before and after, two renamed. Nothing of substance lost.

## Artifacts

Request hashes match. `check.py` clean apart from the expected 268 of 269 ancestor entries:
`gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes equal to the accepted set, 32 evidence
calls all cited and none bad, final equals annotation, 3529 blobs, nothing after the cutoff. Orchestration
hashes equal the accepted files; sparse, 268 of 269, as disclosed.

## Run checks (mine, tree at `b8c830c1`)

- `blocksparse_mlp_routing` is declared with four parameters (`bsz, cfg, y, params`) and bound directly;
  the default route now passes a fifth, `False`. Mixtral and Qwen3 MoE use the default route. As stated.
- With `deepseekv3_routing` true and groups other than one each, no branch assigns the routing results;
  the `routing_ds3` call is commented out. As stated.
- `routing_dots` adds the bias to the logits, takes top-k, applies sigmoid to the selected biased logits,
  normalises and scales, with no guard for a missing bias or factor. `routing_ds3` applies sigmoid first
  and gathers uncorrected scores. As stated.
- The bias key is hard-coded as `<key>.gate.e_score_correction_bias`. As stated.

## Must fix before canonical use

- Author a version with 269 visible, so it can say that the accumulator change closes the finding recorded
  there.

## Reviewer knowledge (never to a teacher)

Upstream `39ded1b7` "Fix regression" (same day, next commit to this file) removes the fifth argument.

## Ledger

- Accepted: `ordinary-output-accumulator-dtype` r001, `fused-shared-unreachable` r002,
  `all-expert-fused-shape` r006.
- File with the next request: three new identities from this entry; fix revisions at `b8c830c1` for
  `ordinary-output-accumulator-dtype` and `fused-shared-unreachable` (both fixes are visible in this
  commit's diff and described in the entry); observations on the two carried identities.
