# Verdict: guidance-12-implementation-001

Reviewer: Fable. Date: 2026-11-16.

## Decision

**Accepted.** The guidance-12 trial may run as described in `guidance-12-trial.decision.md` (Sol, medium;
targets 98, 103, 110, 214; controls 243, 245; under `.teacher/trials/guidance-12-001/`). The walk default
stays 11. Trial runs are never approved. Adoption needs the user's decision.

## Checks

- All hashes in the request match.
- Patch read in full (66 lines): `GUIDANCE_12_ADDITION` is the decision file's revised F word for word; a new
  `== 12` branch appends the guidance-9 addition and then it; 11 and below are untouched; the validator's
  allow-list gains 12; the test is extended.
- My own check with the test fixture: a freshly prepared packet still gets version 11; a packet set to 12
  validates, and its system text equals version 11's with paragraph F replaced by the decision file's text;
  other inputs, tools and effort equal.
- Suite log: 287 tests, OK. Not rerun by me.

## Conditions for the trial

- Runs under `.teacher/trials/` remain rejected by the approval gate; say in the result how the trial
  sessions were launched (the existing trial entry point is tied to another root).
- No reviewer material to trial teachers, including the pass criteria in the decision file.

## Next

Run the trial and file `guidance-12-trial-001`. 246 is approved (`commit-000246-001.md`); the walk continues
at 247 on guidance 11. Replacements stay paused.
