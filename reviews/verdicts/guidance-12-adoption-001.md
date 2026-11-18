# Verdict: guidance-12-adoption-001

Reviewer: Fable. Date: 2026-11-16.

## Decision

**Accepted.** Guidance 12 is the walk default from commit 249, per `guidance-12-adoption.decision.md` (user:
"Adopt version 12"). The replacement pause ends. Existing approvals are unchanged.

## Checks

- All hashes in the request match.
- Patch read in full: one production change, `prepare()` writes `guidance_version=12`; the test is renamed and
  compares the default with the version-12 session.
- `teacher/session.py` has the same hash as at the accepted guidance-12 trial gate, so the text every existing
  packet receives is unchanged.
- My own check with the test fixture: a freshly prepared packet gets version 12 and validates; its system
  text equals the guidance-9 text plus paragraph F as written in the adoption decision file; other inputs and
  tools equal.
- Suite log: 287 tests, OK. Not rerun by me.

## Next

1. 248 is approved (`commit-000248-001.md`): record it, lift the pause, proceed to 249 at guidance 12.
2. Replacements resume one at a time on Sol at guidance 12 under the accepted plan: a fresh attempt at 110
   first, then 141, 158, 164, 213, 214, 225, 234. Each request states the findings side by side and, for 110,
   says how the new attempt treats the tied-head mechanism.
3. `token-usage-retention-001` is still owed.
