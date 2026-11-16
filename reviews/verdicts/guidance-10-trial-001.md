# Assessment: guidance-10-trial-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-10-trial-001.md` (sha256 `df8e5ba1c8d545f8a02833db82c0b335d64a265b7d1378f274621f18f4d37581`)
Decision file: `reviews/verdicts/guidance-10-trial.decision.md`
Reviewed: 2026-11-16, machine `exdev-314`

## Result

**Not passed.** The added clause did not move the one item it was written for: at 188 the kernel-attribute cache
keyed without a device is still under "Uncertainty and limits", not a finding. Both controls stayed clean. This
is an assessment for the user, not an approval of any trial output and not adoption. The walk stays on guidance
8 until the user decides.

## Integrity (my checks)

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| What the teachers saw | For each of the three runs the system text equals the approved guidance-8 run's system text plus a blank line and `GUIDANCE_10_ADDITION`, exactly; that constant equals the text in the decision file. |
| Packets | Each trial manifest differs from the approved packet's manifest in `guidance_version` only (10 against 8). |
| Replay | 22, 10 and 12 recorded tool calls; all 44 replay identically against the trial packets. |
| Hindsight | No blob in a trial packet contains `reviews/verdicts` or a defect-ledger path. |
| Walk untouched | `walk-before.json` and `walk-after.json` have the same hash. |

## What each run did (reviewer knowledge; never to a teacher)

| Position | Kind | Outcome |
|---|---|---|
| 188 | target | **Main item not found.** The entry now says outright that `cudaFuncSetAttribute` runs only for an address absent from a process-global set and that the insertion ignores the return status, so the clause was applied to the right code. It then leaves "keyed only by kernel address, not device or context" under limits and says CUDA documentation was not inspected. It does report the removed native checks as a finding (null scratch pointer, undersized scales), as the version-9 run did, and carries the two inherited selector findings from 186. All three findings are true as far as I checked them at 186 and 188. |
| 189 | control | **Clean.** No finding; explains that both multiplication branches overwrite the uninitialised buffer. 10 calls against 10. |
| 178 | control | **Clean.** Says what the three removed assertions guaranteed and that the scheduler still establishes them; keeps the inherited optional-output finding; adds none. 12 calls against 9. |

## Cost

Tool calls, trial against the guidance-8 runs: 188 22/16, 189 10/10, 178 12/9; 44 against 35, about a quarter
more. The version-9 runs at the same three positions made 41. Astra input tokens: 1.03M, 0.30M, 0.48M.

## Reading

- The teacher did what the clause asks up to the point where it needs a fact the source does not contain: that
  the raised shared-memory limit belongs to a device or context. Without that it cannot say the once-only call
  leaves a second device unguarded, and the paragraph tells it to report a finding only when "the source shows
  an input or call path that reaches the unguarded case". This is a knowledge gap, not a wording gap; a further
  clause is unlikely to close it.
- The clause did no visible harm in three runs and no visible good. The version-9 text has been tried at five
  positions, the version-10 text at three.
- Weaknesses of both trials: the wording was written with the targets in view; one run per position, and the
  version-9 run at 184 lost a finding the approved entry had, which shows how much a single run varies.

## Recommendation to the user

As I said before the trial: adopt the version-9 paragraph (without the extra clause) for what it does achieve,
which is turning removed checks and bypassed calls into findings (190, 184's bias, 188's native checks) at about
a fifth more tool calls, with both controls clean. It does not catch cases like 188's cache, where the harm
depends on a fact outside the repository; those stay my job at review. Adoption needs the user's decision, then
a decision file, an adoption request from Astra and my check, as for 7 and 8.

## Next

1. I report this to the user. Nothing changes for the walk until a decision file exists.
2. No action for Astra on this request. The walk continues on guidance 8.
