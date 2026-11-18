# Verdict: commit-000303-001 (teacher Sol, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-17 (19:28 UTC). Upstream `1e1e68b3` "Fix regression, #55 (fused tensors/padding/deferred load)".
Run: `.teacher/runs/commit-000303-001`. Packet: `.teacher/retrieval/000303-001`.

## Decision

**Approved for ancestor retrieval only. 303/001 is the entry in force for commit 303.** Canonical and
training stay false. No new findings. Continue at 304.

The entry makes the central check itself: the fused fallback built `LinearFP16` without the four dimension
arguments, the constructor compares integers with their `None` defaults, and that is the traceback in issue
55; the patch forwards the outer `Linear`'s resolved values as the ordinary branch already did, and
separately makes the transposed weight contiguous. It names the routes that reach the fallback (attention
Q/K/V ranges, gated-MLP halves, GLM4's `gate_up_proj`) and does not claim conversion now succeeds.

This is the fix of the ledger identity `exllamav3-none-full-dimensions` (first recorded at 266). File the
fix revision with the 304 request, as you propose.

## Artifacts

Request hashes match (17 of 17). `check.py` clean: `gpt-6.1-sol` medium, 45 implementation hashes equal to
the accepted set, 28 evidence calls all cited, replay 28 of 28, final equals annotation, 302 of 302
ancestors, 4372 blobs, nothing after the cutoff. Complete packet, ran ahead of nothing.

## Run checks (mine, tree at `1e1e68b3`)

Diff read in full: `weight.T.contiguous()` and the four added arguments at the fused `LinearFP16` call. As stated.

## Ledger (302)

`exllamav3-base-config-missing-rope-mask` r001 is accepted.

## Must fix before canonical use

Nothing.
