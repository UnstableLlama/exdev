# Verdict: guidance-8-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-8-implementation-001.md` (sha256 `bbabf0f43d2e92da99b30bc293b0ac7bf1b9a1a32ddddcb77049f08b35965542`)
Decision file: `reviews/verdicts/guidance-8-trial.decision.md`
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**ACCEPTED** as a trial gate. Guidance 7 remains the walk default. This is not adoption.

## What I checked

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| The text | `GUIDANCE_8_ADDITION` equals paragraph D in the decision file exactly (compared programmatically). |
| Selection | Version 8 and above get the guidance-7 text, a blank line, then the paragraph. Version 7 gets the guidance-7 text alone, 6 the trialled text, below that nothing. |
| Default | `prepare()` still writes 7. Validation accepts 5, 6, 7 and 8 under contract 8 and is otherwise unchanged. |
| Older packets unchanged (mine) | Rebuilding the session with the new code for 175 and 172 (version 7) and for 171 and 160 (version 5) gives system text identical to each run's recorded transcript; none contains the paragraph. |
| Whole change (mine) | Against `0ed73a1` only `teacher/session.py` (seven added lines), `teacher/walk_inputs.py` (one line) and `tests/test_walk_inputs.py` differ under `teacher/` and `tests/`. |
| Suite (my run) | 280 tests, OK, with `codex` on the path. Without it two wire tests error in my shell because the executable is not found; that is my shell, not the change. |
| No reviewer material | The paragraph is the only new teacher-facing text. The pass criteria in the decision file are not in the code. |

## Conditions for the trial

1. Positions 154, 140, 157 and 156; fresh, unassisted, version 8, the approved runs' cutoff evidence; under
   `.teacher/trials/` only. Never approved, never ancestor context, not journal attempts.
2. No coverage request, verdict text or ledger material to a trial teacher.
3. Walk runs from 176 on will record hashes for the patched `session.py` and `walk_inputs.py`; that is expected.
   Each walk packet must still carry `guidance_version` 7.

## Next

1. The walk continues on 7.
2. Run the four trial sessions between commits and file `reviews/requests/guidance-8-trial-001.md`.
