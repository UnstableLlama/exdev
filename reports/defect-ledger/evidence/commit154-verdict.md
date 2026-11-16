# Verdict: commit-000154-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000154-001`
Packet: `.teacher/retrieval/000154-001`
Upstream: `5c3ff204c4c5c64dc2bd897582143b116a82b767` "model_diff.py: Use deferred load and close file handles between modules"
Request: `reviews/requests/commit-000154-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the inherited finding is correct. The entry follows the six added lines into
the loader, says what deferral does and does not cover, and notices that the cleanup sits on the normal path with
no `try`/`finally`. It did not notice what the other two users of this bracket do first and this one does not
(reviewer section, follow-up 2).

The administrative ledger note `reports/commit-000153-affected-identities-001.json` is **accepted**.

## Artifacts reviewed (sha256)

All twenty-seven hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 9 of 9 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 153 strict-ancestor entries (153's being attempt 002); 2,288 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 9 of 9 recorded tool calls identical, including the `run` call. |
| Unassisted | No coverage request in the opening context; the instructions differ from 153/002's only by that run's coverage sentence and merge paragraph. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Eleven open rows at 2025-05-12T19:23:48Z (33 closed then). No closed row qualified under `salience-v3-paths`, by terms or by path; nothing cut. Reported as the acceptance condition asks. |
| Pull request 26 | Read in two pages up to the comment of 2025-05-11T14:16:07Z; the next is 15 May. Labelled inference from the shared script. Correct. |
| Architecture trigger | Does not fire. |
| The change | For each of the two models in the per-module loop: `stc.begin_deferred_load()` before `module.load(...)`, `stc.end_deferred_load()` after it, and `stc.close()` after `module.unload()`. Six lines; nothing else. Correct. |
| Loader behaviour | Deferral applies to `mt_fread` reads without `no_defer`; the flush groups, sorts by size and cuts into 2 MiB jobs; `close` closes each cached handle and sets the entry to `None`, keeping the header maps so a later read reopens. Correct. |
| Unchanged | Device choice, the forward passes, the error metrics and the perplexity helper. Correct. |
| Execution | Recorded output: with 2,047 positions, a vocabulary of 1,024 covers 1,024 and a vocabulary of 32,000 covers all 2,047 in four passes; 2,097,152 bytes; three jobs for 5 MiB. Matches the prose. |
| Finding `inherited-ppl-axis-bound` | Correct. `ppl` slices rows (`logits_[a_:b_, :]`) but bounds the loop with `logits_.shape[1]`, the vocabulary. With a real vocabulary far above 2,047 the first pass covers every position and the later passes are empty, so the number comes out right; only a vocabulary smaller than the sequence would drop positions. Suspected and inherited are right. The chunk size expression `shape[1] * 10240 // shape[1]` is just 10,240. |
| Ledger note for 153 | Eight records, one per retained finding, each naming the latest revision of its existing identity and its hash, with `a905cffb` as a source-supported affected revision. No new identity, introduction, fix or status. Accepted as the single note the 153/002 verdict allowed. |

## Reviewer-only notes (never to a teacher)

All by source reading; nothing was run.

- **No eligibility check (mine; introduced here).** `Model._load_single` and the autosplit loader both ask
  `module.can_defer_load()` and bracket the load only when it is true. This script brackets every module. The
  modules that answer false are a sliced `Linear` and a `GatedMLP` with more than one slice, and they answer
  false for a reason: `LinearFP16.__init__` slices its weight and copies the slice into a new tensor during
  construction. In deferred mode the weight has been allocated but not yet read when that copy happens, so the
  layer keeps uninitialised memory while the real data later lands in a tensor nobody uses. Slicing only occurs
  for an MLP wider than `MAX_MLP_INTERMEDIATE` (55,296), which no model registered so far has, so this is
  latent. It would be silent if reached.
- **No abort on failure.** Same shape as my 140 observation: if a load or the flush raises, the collection stays
  in deferred mode. In a script that exits on error it does not matter. The entry notes the absence of
  `try`/`finally` without drawing a consequence, which is the right weight.
- This is the second place handle closing has been added after the "too many open files" report (128 was the
  first). It closes per module for both models.
- No ledger record exists for the perplexity bound; it was approved at its own position (127) and never filed.

## Not verified

- Any model comparison run.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: file `ppl-axis-bound` as one identity introduced at `9575f7d8`, with `5c3ff204` as an affected
   revision; note that it changes results only for a vocabulary smaller than the sequence.
2. Ledger: a reviewer-observation record for the unconditional deferral in `model_diff.py`, introduced at
   `5c3ff204`, conditional on a module that cannot defer. Excluded from historical context and training.
3. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the note's acceptance.
2. Continue the walk at commit 155.
