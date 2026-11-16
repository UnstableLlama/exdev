# Verdict: guidance-9-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-9-implementation-001.md` (sha256 `56ab0cd2b0675ce7a3364cf5d92c239d9b0ec35c2796495711e04ba7bbc4237d`)
Decision file: `reviews/verdicts/guidance-9-trial.decision.md`
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**ACCEPTED** as a trial gate. Guidance 8 remains the walk default. This is not adoption.

## What I checked

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| The text | `GUIDANCE_9_ADDITION` equals paragraph E in the decision file exactly (compared programmatically). |
| Selection | Version 9 and above get the guidance-8 instructions, a blank line, then the paragraph. Versions 5 to 8 are selected as before. |
| Default | `prepare()` still writes 8. Validation accepts 5 to 9 under contract 8 and is otherwise unchanged. |
| Older packets unchanged (mine) | Rebuilding the session with the new code for 192 (version 8), 177 (version 7), 171 (version 5) and the guidance-6 trial packet for 154 gives system text identical to each recorded transcript; none contains the paragraph. |
| Suite (my run) | 280 tests, OK, with `codex` on the path. |
| No reviewer material | The paragraph is the only new teacher-facing text; the pass criteria in the decision file are not in the code. |

## Conditions for the trial

1. Positions 184, 188, 190 and controls 189, 178; fresh, unassisted, version 9, the approved runs' cutoff
   evidence; under `.teacher/trials/` only. Never approved, never ancestor context, not journal attempts.
2. No coverage request, verdict text or ledger material to a trial teacher.
3. Walk packets keep `guidance_version` 8. Walk runs from 193 on will record the patched implementation hashes.

## Next

1. The walk continues on 8.
2. Run the five trial sessions between commits and file `reviews/requests/guidance-9-trial-001.md`.
