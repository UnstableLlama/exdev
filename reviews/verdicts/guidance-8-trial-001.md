# Assessment: guidance-8-trial-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-8-trial-001.md` (sha256 `dacce61139830920100b67023c0e7715107eaddb9c2e6ec656496f4a332fcbdc`)
Decision file: `reviews/verdicts/guidance-8-trial.decision.md`
Reviewed: 2026-11-15, machine `exdev-314`

## Result

**The trial passes.** This is an assessment for the user, not an approval of any trial output and not adoption.
The walk stays on guidance 7 until the user decides.

## Integrity (my checks)

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| What the teachers saw | For each of the four runs the system text equals the original approved run's system text plus the guidance-7 text plus the fourth paragraph, exactly. |
| Packets | Each trial manifest differs from the approved packet's manifest in `guidance_version` only. No coverage request. |
| Replay | 23, 23, 22 and 6 recorded tool calls replay identically against the trial packets. |
| Walk untouched | `walk-before.json` and `walk-after.json` are identical. |

## What each run did (reviewer knowledge; never to a teacher)

| Position | Kind | Outcome |
|---|---|---|
| 154 | target | **Found.** Compared the two existing deferred-load callers with the new calls; reports that the script omits `can_defer_load` and traces what a sliced linear then does. Also notes the missing abort. The guidance-6 trial run of 154 (paragraphs A to C, 10 tool calls) did not find this; this run (23 calls) did. That is the one clean comparison that isolates the new paragraph. |
| 140 | target | **Found.** Reports that the new single-device caller copies the lifecycle but not the exception-time abort the autosplit caller has. The approved entry did not have this; it was a reviewer finding. No guidance-7 run of 140 exists, so this does not isolate the paragraph from A to C. |
| 157 | control, new call site that is fine | **Clean.** Lists the existing `close` callers, says the new call follows the same pattern and that `close` precedes `set_new_tensors` as its assertion needs. No findings, no speculation. |
| 156 | control, no new call site | **Clean.** No findings, no mention of callers it had no reason to look for. 6 calls against 4. |

No run stretched "mechanism" to something it does not fit.

## Cost

Tool calls, trial against the original guidance-5 runs: 154 23/9, 140 23/17, 157 22/14, 156 6/4; 74 against 44.
Part of that increase belongs to guidance 7, not the new paragraph. Where the comparison is clean (154, guidance
6 against 8) the calls went from 10 to 23, almost all extra `repo_read` and `repo_grep`. Input tokens per run were
0.17M (156) to 1.22M (157), over 90% cached. No baseline token counts exist for these positions.

## Limits

Two targets and two controls. The wording was written from the two targets. Three of the four comparisons are
against guidance 5 and so mix in guidance 7's effect.

## Next

1. I report this to the user and ask for a decision on adoption.
2. Nothing changes for the walk until a decision file exists.
