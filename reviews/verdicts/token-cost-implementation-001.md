# Verdict: token-cost-implementation-001

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/token-cost-implementation-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**ACCEPTED in substance; four small fixes required before first use.** The driver gathers the same evidence,
builds the same packets and keeps every stop. Nothing a teacher sees changes. Make the four fixes below, file
`reviews/requests/token-cost-fixes-001.md` (short: the new hashes, the test count, one line per fix), and do not
start 159 until that verdict. I apply part D at that point.

## What I checked

| Check | Result |
|---|---|
| Request hashes | All sixteen match the files on disk. |
| Existing teacher files | The 42 implementation hashes recorded in 158's provenance still match the tree. `cycle.py` is imported by nothing else under `teacher/`. |
| Suite (my run) | 267 tests, OK. Twelve skip in my shell because the host-sandbox switch is not set; your report has them enabled. |
| Packet rebuild (yours) | 156 and 157: manifests byte-identical, same opening context, tool schemas and blob names. |
| Evidence recovery (mine) | Your rebuild reused the saved bundles, so it did not exercise `recover_inputs`. I ran `recover_inputs` into scratch directories for 157, 153 and 148 and compared with the recorded bundles. 157: unreferenced and closed identical apart from `retrieved_at`; selection report identical. 153 (explicit reference, nine closed rows): eligible, unreferenced and closed identical apart from `retrieved_at`; selection report identical. 148: eligible and unreferenced identical; the closed bundle differs only because 148 was built under `salience-v2`, before the path rule, which is expected. |
| Order of steps | Read against `walk.py`: `prepare`, `attach_graphs`, the same ancestor filter, `attach_entries`, `validate_bundle`, `author`, `assess`, then the same full-review handover or `approve_mechanical`. Same order, same arguments. The cutoff now comes from `git show --format=%cI` rather than the record file; the comparison above shows the same value. |
| Stops | State and pause, half-started run, disk, unresolved class files, invalid or unresolved bundle, curator attestation, any architecture trigger, unrecognised or absent reference, a path-qualified row cut by the cap, and existing preparation files. Each raises before `author` is called; each has a test. An architecture commit always stops, which keeps discovery manual. Correct. |
| Validation inside the driver | Manifest fingerprint, implementation hashes, assistance provenance, blob hash, read-only bit and store link for every blob, and a full replay. A failure there raises before any handover. Correct. |
| `--approve` | Requires the pending run's own verdict file, an approval in the Decision section with no rejection or hold, every hash in the request, and the hashes my verdicts list. Keeps an advancement pause. Correct for a first-attempt, unassisted run. |
| Tracking file, top section | The current block, procedure and standing conditions are accurate, including the mirror rule as I ruled it at 158. |

## Required fixes

1. **The skeleton must not live in the mailbox.** `reviews/requests/commit-N-A.skeleton.md` is a `.md` file in the
   directory where a file without a verdict means "pending". My watch and anything else that pairs requests with
   verdicts will take it for a filed request. Write it under `reports/` (or anywhere outside `reviews/requests/`)
   and do not write one at all for a mechanically approved commit.
2. **Split the tracking file.** `reviews/ASTRA-TRACKING.md` is 158 KB, about forty thousand tokens. One careless
   read after a reset costs more than a whole commit should. Keep the current block, procedure, standing
   conditions and open work in `ASTRA-TRACKING.md` (it is about eighty lines now; keep it under a few hundred)
   and move the register to a second file, for example `reviews/ASTRA-REGISTER.md`. `--approve` appends to the
   register. `AUTHOR-INSTRUCTIONS.md` should say to read the first and to search the second, not read it whole.
3. **Mark a failed run as failed.** On an exception `walk.py` sets the run record's status to `failed`; the driver
   leaves it at `preparing` or `authoring` and only sets the journal status. Do what `walk.py` does, so the
   recovery rule used at 113 still finds failed runs.
4. **`--approve` must refuse what needs a hand.** Stop with a named status when the pending run is not attempt
   001, when another run exists for the same position, or when its provenance is reviewer-assisted. Those need the
   supersession and labelling steps you did by hand at 153.

## Notes, not conditions

- The manual path for an architecture commit used the `/tmp` scripts for discussion recovery. After a reset
  those are gone. A `--prepare-only` mode that runs `recover_inputs` and `index_parent` and stops would cover it;
  add it with the fixes if it is easy, otherwise say in the procedure how the manual path recovers discussions.
- The disk floor of 2 GiB is fine. Free space is far above it since the blob store.
- The discussion-history cache is still owed and is now the largest remaining wall-clock cost.

## Part D, as I will apply it

Your conversation is about 46k tokens immediately after a compaction (system text, tools and the summary), and a
commit has been adding about 12k. A limit of 60k, as I first proposed, would compact on almost every call. I will
set `model_auto_compact_token_limit = 90000` and measure; lower later if the driver makes commits small enough.
I restart your window when I write the fixes verdict, then queue the usual message.

## Next

1. Make fixes 1 to 4, run the suite, file `reviews/requests/token-cost-fixes-001.md`.
2. Wait for that verdict. Do not start 159.
