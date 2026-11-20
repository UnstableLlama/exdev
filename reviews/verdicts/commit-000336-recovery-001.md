# Verdict: commit-000336-recovery-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (07:58 UTC). Stopped run: `.teacher/runs/commit-000336-001` (no draft published; nothing to judge
as an entry). Packet: `.teacher/retrieval/000336-001`. Upstream `37f80fb9` "Fix typo".

## What I checked myself

- Request hashes: 9 checked, 0 bad.
- The failure is as reported. The transcript holds only the system and user messages, `status.json` says failed with
  `ValueError`, `token_usage` is empty, and the run log ends at `codex_adapter.py:242`, which raises on an `error`
  event without keeping its payload. The cause cannot be established from what was saved.
- This is the only one of 83 run-ahead logs with this error. The weekly quota read 94% in the author's log at the
  time, so the limit was not reached.
- One difference from the request: packet 336/001 holds 331 of the 332 strict ancestors and lacks direct parent
  `3be1ea10` (335). 335 is now approved, and 336/001 produced nothing that a matching snapshot would be compared with.

## Decision

**Recovery authorised: one fresh unassisted attempt, 336/002, to start now.** Normal packet builder, same cutoff,
pinned evidence, contract 8, guidance 12, gpt-6.2-sol medium. Use the current approved ancestors, through 335, rather
than the 336/001 snapshot, so the direct parent is included. If the builder cannot do that, say so in the 336/002
request and run with what it gives. Keep 336/001 and its transcript as they are; keep this handoff out of teacher
input.

If 336/002 stops with the same error, stop and file both failures.

## Proposal (does not block 336/002)

Keep the `error` event's payload in the failed run's record, so the next failure of this kind has a cause. This
touches diagnostics only and must not reach teacher input. File it as a normal implementation request with hashes.
