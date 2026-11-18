# Verdict: commit-000293-001 (teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-17 (14:20 UTC). Upstream `b2b09809` "chat.py: Fix t/s display".
Run: `.teacher/runs/commit-000293-001`. Packet: `.teacher/retrieval/000293-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. Both findings are accepted as
observations of existing identities (`chat-tps-toggles-multiline` and `nonpositive-codeblock-index`);
neither is new. The entry states the fix correctly (the uncached context count is no longer overwritten by
the generated count before printing) and ties it to the earlier entry that recorded the slip.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes
equal to the accepted set, 20 evidence calls all cited and none bad, final equals annotation, 292 of 292
ancestors, 4271 blobs, nothing after the cutoff. Orchestration hashes equal the accepted files; complete
packet; ran ahead of none. Repair enabled, unused.

## Run checks (mine, tree at `b2b09809`)

- The diff is the rename and its two uses. As stated.
- `/tps` still flips `multiline` (lines 118 to 120); the report is gated on `show_tps`. As stated.
- `copy_last_codeblock` checks only the upper bound before `matches[-num]`. As stated.

## Ledger

- Accepted: `ernie-chat-template-mismatch` r001, `custom-bias-export-name` r002,
  `missing-ernie-registry-modules` r002 (fix at 292), `all-expert-fused-shape` r011,
  `fused-output-dtype-override` r004.
- File with the next request: a fix revision for `chat-context-count-overwritten` at `b2b09809`, and the
  two observations.
