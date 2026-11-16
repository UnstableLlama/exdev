# Assessment: guidance-9-trial-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/guidance-9-trial-001.md` (sha256 `081185c33f65e2c81507e9c85c814e5ef7098b62ac60dbb7048e68f9361e4d8b`)
Decision file: `reviews/verdicts/guidance-9-trial.decision.md`
Reviewed: 2026-11-16, machine `exdev-314`

## Result

**Mixed: a partial pass.** The paragraph moved two of the three target items from "not established" to findings
and added no finding to either control, but it did not move the one that mattered most (188's device-less
cache). This is an assessment for the user, not an approval of any trial output and not adoption. The walk stays
on guidance 8 until the user decides.

## Integrity (my checks)

| Check | Result |
|---|---|
| Request hashes | All match the files on disk. |
| What the teachers saw | For each of the five runs the system text equals the approved guidance-8 run's system text plus a blank line and the fifth paragraph, exactly. |
| Packets | Each trial manifest differs from the approved packet's manifest in `guidance_version` only. |
| Replay | 24, 20, 18, 9 and 12 recorded tool calls. All replay identically except one recorded tool error at 184 (`web_fetch` with an invalid `max_bytes`), which my script shows as a mismatch because the tool raises where the transcript stored the error; the error text is the same. |
| Walk untouched | `walk-before.json` and `walk-after.json` are identical. |

## What each run did (reviewer knowledge; never to a teacher)

| Position | Kind | Outcome |
|---|---|---|
| 184 | target | **Target item found.** The dropped router bias is now a suspected finding, from comparing the bypassed `LinearFP16.forward` with the native helper. The dtype-override and all-experts findings are kept. **But** the approved entry's aliasing finding is gone: retained outputs appear only under limits. One gained, one lost. |
| 188 | target | **Main item not found.** The cache keyed by function pointer alone is still under "Uncertainty and limits", almost word for word as in the approved entry. A new finding does appear for the commented-out native checks (short output, missing or undersized scratch and transforms), which the approved entry only listed. |
| 190 | target | **Found.** The removed flattening view's rejection of incompatible strides is a suspected finding, with a concrete shape and stride example and the honest limit that no in-tree producer of such an input was found. |
| 189 | control | **Clean.** No finding; explains why the removed zero-fill is safe. 9 calls against 10. |
| 178 | control | **Clean.** Says what the three removed assertions guaranteed and that the scheduler still filters; adds no finding for them. 12 calls against 9. |

## Cost

Tool calls, trial against the guidance-8 runs: 184 24/23, 188 20/16, 190 18/11, 189 9/10, 178 12/9; 83 against
69, about a fifth more. Every comparison here is against guidance 8, so the difference is the fifth paragraph and
run-to-run variation.

## Reading

- The paragraph works for what it literally names: a removed check (190, 188's native checks) and a bypassed call
  that did extra work (184's bias).
- It did not reach 188's cache. That case is not a removed check; it is a call that used to run every time and
  now runs once per process. The wording says "bypasses … initialisation", which the teacher did not apply to it.
- 184 losing a finding it had before shows how much one run varies. One run per position cannot separate a
  paragraph's effect from that variation.

## Next

1. I report this to the user with options. Nothing changes for the walk until a decision file exists.
