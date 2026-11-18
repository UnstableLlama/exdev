# Verdict: commit-000272-001 (teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-17 (09:17 UTC). Upstream `39ded1b7` "Fix regression".
Run: `.teacher/runs/commit-000272-001`. Packet: `.teacher/retrieval/000272-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. The four findings are accepted
as observations of existing identities (all-expert fused shape, grouped routing unassigned, optional inputs
required by Dots, fused output dtype and lifetime); none is new. The entry made the central check itself:
it compared the repaired call with the declaration, definition and binding, and named which models use
that route.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes
equal to the accepted set, 21 evidence calls all cited and none bad, final equals annotation, 271 of 271
ancestors, 3680 blobs, nothing after the cutoff. Orchestration hashes equal the accepted files; complete
packet; ran ahead of none. Repair enabled, unused.

## Run checks (mine, tree at `39ded1b7`)

The one Python call to `blocksparse_mlp_routing` now passes four arguments, matching the four-parameter
declaration I read at 270. Mixtral and Qwen3 MoE use this route; Dots1 uses `routing_dots`. As stated.

## Ledger

- Accepted: `dots-default-prompt-format` r001, `all-expert-fused-shape` r008.
- File with the next request: the fix revision for `native-router-argument-mismatch` at `39ded1b7`, and
  this entry's four observations.
