# Verdict: guidance-11-adoption-001

Reviewer: Fable. Date: 2026-11-16.

## Decision

**Accepted.** Guidance 11 is the walk default from commit 238, per
`reviews/verdicts/guidance-11-adoption.decision.md` (user: "Adopt version 11"). Existing approvals are unchanged
and remain ancestor retrieval only.

## Artifacts

All twelve hashes in the request match.

## Run checks

- Patch read in full (44 lines). One production change: `prepare()` writes `guidance_version=11`. The test is
  renamed and now compares the default against the version-11 session.
- `teacher/session.py` has the same hash as at the accepted trial gate
  (`guidance-11-implementation-001`), so the text every existing packet receives cannot have changed: versions
  5 to 11 are as already verified there.
- My own check with the test fixture: a freshly prepared packet gets version 11 and validates; its system text
  equals the version-9 text plus a blank line plus paragraph F as written in the adoption decision file; other
  inputs, tools and reasoning effort equal version 9's.
- Astra's suite log: 282 tests, OK. I did not rerun the suite.

## Not verified

- Astra's 19-packet reproduction report was not rerun by me; the unchanged `session.py` hash covers it.

## Next

1. 237 is approved (`commit-000237-001.md`): record it, lift the pause, proceed to 238 at guidance 11 with the
   two ledger revisions owed.
2. File `guidance-11-reauthoring-plan-001`. No replacement run before it is accepted.
