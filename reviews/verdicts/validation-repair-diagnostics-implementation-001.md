# Verdict: validation-repair-diagnostics-implementation-001

Reviewer: Fable. Date: 2026-11-18 (05:20 UTC).

## Decision

**Accepted: `validator-claim-diagnostics-v3` may be applied.** Apply it only at a queue boundary: no teacher
run in flight and every approved run recorded, so that no approval meets a changed hash (the 299/310 problem).
If 325 is running under v2, let it finish and be recorded under v2 first. After applying, the candidate
49-hash set in `reports/validation-repair-diagnostics-implementation-001.hashes.json` is the accepted set;
say in the next request which commit is the first to run under v3.

## What I checked myself

- Request hashes 0 bad; the patch applies cleanly to the live tree (`git apply --check`).
- Read every production line of the patch (`teacher/editorial.py`, `teacher/validation_repair.py`,
  `teacher/codex_adapter.py`). The refusal category strings are unchanged; the detail is a second line added
  only under the v3 policy. The reference is rendered only if it fully matches `(call_|ancestor:)` plus hex,
  the finding id only if it matches `[a-z][a-z0-9-]*`, both capped at 64 characters, otherwise
  `[invalid identifier]`: no teacher-written free text can reach the message. No suggested call, one repair
  turn, keep-the-rest sentence unchanged. Recorded v1/v2 events still verify because the detail is omitted
  for their policies.
- Suite log: 340 tests OK. Replay report bound; both additions from the proposal decision are present with
  tests (source-inspection class names finding, check and tool kinds; bounded rendering).

## Watch for

The first v3 repair is the test: tell me in that request what message the teacher received and whether one
turn fixed it.
