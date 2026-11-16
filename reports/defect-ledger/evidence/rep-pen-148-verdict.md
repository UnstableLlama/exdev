# Verdict: commit-000148-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000148-001`
Packet: `.teacher/retrieval/000148-001`
Upstream: `81a0a7d2409ae682522b7cf051b066b6baa6f471` "Merge pull request #35 from gakada/humaneval"
Request: `reviews/requests/commit-000148-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry reads all seven eligible objects of the pull request and reports them
as what they are: the contributor's scores, the maintainer's diagnosis of the penalty failure, and the remark that
penalties can be tested on dev. It says plainly that this diff contains no penalty repair and that it did not
inspect the kernel, which is right, because the repair (142) is not an ancestor of this merge. No findings, and I
found none.

## Artifacts reviewed (sha256)

All fourteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 18 of 18 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; 1,923 blobs hash to their names; no evidence timestamp after the cutoff. |
| Ancestry | Parents `ae04741f` (143) and `beb7bcd9` (147): this merge is on the master line, not the development line. The packet holds exactly 134 strict-ancestor entries (positions 1 to 132, 143 and 147); nothing from 133 to 142 or 144 to 146. Correct. |
| Replay | 18 of 18 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 146/001's, the previous merge run. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| The merge | The difference from the first parent is `eval/humaneval.py` alone, ten lines added and three removed, identical to 147's change. Git's own three-way merge of the parents gives the commit's tree: no hand edits. |
| Pull request 35 at the cutoff | Cutoff 2025-05-11T18:47:03Z. The session read the opening text and six comments: 05:32:04Z, 09:24:51Z, 15:11:23Z, 15:33:57Z, 18:04:49Z (as edited 18:34:08Z) and 18:46:37Z. GitHub's next comment is 20:41:37Z. I searched the packet for distinctive text of the later comments (the unsloth link, the score table, the TabbyAPI remark) and found none. Seven objects, as the request says. |
| Catalog | Eleven open rows: 1, 4, 7, 10, 14, 22, 26, 27, 28, 29, 34 (33 closed then; 35 and 36 merged by then). One closed row, pull request 36, merged 18:09:15Z. The entry claims no connection to it. Correct. |
| Architecture trigger | Does not fire. |
| Content | As verified at 147: the parser type and default, the removed option and argument, the `qwen3` preset, the sampler's defaults and argmax branch at the first parent. |
| Discussion as reported | The 0 percent report, the prompt-dependent scores, the maintainer's NaN explanation ("lerp(-inf, -inf, 1)") and "You should be able to test with repetition penalties now in the dev branch" are in the comments the session read, and are attributed, not asserted. Correct. |
| Execution | Recorded output: float parser gives 5.0 and a slice `TypeError`; int parser gives 5 and a valid slice and rejects `5.0`; both defaults disabled. Matches the prose. |

## Reviewer-only notes (never to a teacher)

- **Two lines of history.** I checked ancestry with Git. Master contains 143, 147 and this merge; dev contains
  133 to 142, 144, 145 and 146. The penalty fix (142) and the sampler-side top-K change (136) are on dev only. So on
  master the HumanEval script now passes an integer to a sampler that still stores it unchanged, which is correct
  there. The Python 3.12 problem reaches this script only when dev and master next meet.
- The maintainer's explanation is now legitimately in a teacher's view for the first time. It matches the ledger
  identity for the masked-logit NaN and names the trigger (`min_new_tokens` prohibiting the end-of-turn token).
- Hindsight from 147 still stands: later comments on this pull request discuss a BOS token degrading Qwen3 and a
  rework of the prompt formatting.

## Not verified

- Any generation or scoring.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: the pending revision of `exllamav3-repetition-penalty-masked-nan` may now cite this entry as the first
   position at which the maintainer's explanation is eligible on the master line (144 on the development line).
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval.
2. Continue the walk at commit 149.
