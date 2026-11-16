# Verdict: guidance-6-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-6-implementation-001.md`
Decision acted on: `reviews/verdicts/guidance-6-trial.decision.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**ACCEPTED** as a trial gate. The walk stays on guidance 5. This accepts no trial output and adopts nothing.

## What I checked

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| The text | `GUIDANCE_6` in `teacher/session.py` equals the three paragraphs in the decision file exactly, joined by blank lines (compared programmatically). |
| The gate | Appended after every existing instruction, only when the packet's `guidance_version` is 6 or more. `prepare()` still writes 5. `validate_bundle` accepts 5 or 6 under contract 8 and nothing else changes in it. |
| Version 5 unchanged (mine) | For the approved packets of 164, 157 and 153 I rebuilt the session with the new code: the system text is byte-identical to the recorded one, the rest of the opening is identical, and the new text is absent. |
| Suite (my run) | 280 tests, OK (the usual twelve host-sandbox skips in my shell). |
| Other files | Against 164's provenance only `session.py`, `walk_inputs.py` and `cycle.py` differ; the last belongs to the replay fix. |

## Conditions on the trial

1. Each trial packet's manifest must differ from the approved run's manifest for that position in the
   `guidance_version` field and nothing else. Report that comparison for all four. For 163 the comparison is with
   163/001's packet, the unassisted one; no coverage request.
2. Trial packets and runs under `.teacher/trials/` only; not journal attempts, never approved, never ancestor
   context, never published. Show in the request that no file under `.teacher/retrieval`, `.teacher/runs`, the
   journal's `runs` or `approved_entries` changed.
3. One session per position, the first result kept whatever it says. No reruns to get a better answer. If a
   session fails for a mechanical reason (as at 113), say so and rerun once.
4. For each trial: the draft, transcript, coverage report, tool counts and the number of model turns, next to
   the same figures for the approved run.

## Next

Run the four trial sessions between commits and file `reviews/requests/guidance-6-trial-001.md`.
