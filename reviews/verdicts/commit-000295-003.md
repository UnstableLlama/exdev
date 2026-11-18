# Verdict: commit-000295-003 (teacher Sol, guidance 12, reviewer-assisted; fresh third attempt)

Reviewer: Fable. Date: 2026-11-17 (16:45 UTC). Upstream `69f8f9a0` "Clamp output of activation functions to float16 range".
Run: `.teacher/runs/commit-000295-003`. Packet: `.teacher/retrieval/000295-003`.

## Decision

**Approved for ancestor retrieval only. 295/003 is the entry in force for commit 295.** Canonical and
training stay false. It is a reviewer-assisted entry (coverage request `commit-000295-003.coverage.md`,
questions only) and joins the list of assisted entries in force. 295/001 and 295/002 are kept as history.
You may now record 296's approval, then continue at 297.

This time the entry makes the central check itself: only the FP32-input kernel changes; the deciding
argument is `interm_dtype`; of the shipped builders only `Ernie4_5MoEModel`'s routed experts pass float, on
both the ordinary and the fused path, each with a separate half destination; that argument value came from
the immediate parent `6f9928b3`, whose entry it read and related to this change. It states that the reach
is therefore narrower than the commit title and that no checkpoint is shown to produce such values.

## Findings

The four items are carried conditions (FP32 GatedMLP destination, odd activation tail, all-expert fused
capacity, workspace-backed fused return), each bounded correctly. Accepted as observations of existing
ledger identities; no new identity. File ledger records as usual.

## Artifacts

Request hashes match (19 of 19). `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45
implementation hashes equal to the accepted set, 39 evidence calls all cited and none bad, replay 39 of 39,
final equals annotation, 294 of 294 ancestors, 4284 blobs, nothing after the cutoff. Complete packet; it is
the one I compared with 000295-002 before the run. Repair enabled, unused. The run survived the machine
restart unchanged (file times 15:23 UTC, before the restart).

## Run checks (mine, tree at `69f8f9a0`)

- Diff: helper `clamp_half2_to_finite` (`__hmin2` then `__hmax2`, bounds 65504) applied after
  `__float22half2_rn` in `act_mul_kernel_f` only. As stated.
- `interm_dtype` in `exllamav3/models`: float only at `ernie4_5_moe.py` line 133; half at ten other sites;
  absent in cohere, cohere2, decilm, gemma2, gemma3, llama, phi3, mistral3 (two sites). The entry's
  constructor audit equals this list.
- `block_sparse_mlp.py`: line 305 (fused `interm_a` separate half when not half), line 364 (ordinary `a`),
  line 421 (fused activation call). As stated.

## Must fix before canonical use

Nothing new.
