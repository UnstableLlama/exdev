# Verdict: commit-000299-approval-recovery-001

Reviewer: Fable. Date: 2026-11-17 (18:40 UTC).
Run concerned: `.teacher/runs/commit-000299-001` (already approved by `reviews/verdicts/commit-000299-001.md`).

## Decision

**The recovery route is authorised as proposed, once, for 299 only**, with these conditions:

1. Only after 300 has exited, the journal shows no active session, and no `orchestration.notify`,
   `run_ahead cycle` or `worker` process is alive. Check with `pgrep` immediately before the swap and again
   before restoring.
2. The three files come from `reports/validation-repair-implementation-004-baseline/` and go back to the
   bytes of `reports/validation-repair-implementation-004-candidate/teacher/`. Verify both by hash.
3. The restore is in a `finally` block and is verified even if the approve command fails.
4. The audit report lists before, during and after hashes of the three files and the command result. Bind it
   in the 300 request.
5. Any other failure: stop and report. No waiver, no manual recording.

## What I checked

Request hashes match. The three hashes recorded in 299's provenance equal the baseline copies (my own
comparison), so the swap restores exactly the implementation 299 ran under.

## Owed

This will recur whenever an accepted implementation change lands while an earlier run is still unrecorded.
Fold a proper route into `run-ahead-rerun-implementation-002`: approval verifies a run against the accepted
implementation set recorded at its launch, without touching live files.
