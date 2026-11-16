# Verdict: commit-000146-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000146-001`
Packet: `.teacher/retrieval/000146-001`
Upstream: `9c31971b844ffea3b077d5157225565877679171` "Merge pull request #36 from tokoba/master"
Request: `reviews/requests/commit-000146-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the carried-over finding is correct. This is the first position at which the
pull request's own text is eligible, and the entry uses it properly: the traceback in it is quoted as the
contributor's report and matched against the source line, and "it seems to work" is not turned into a test result.

Both ledger candidates are **accepted**.

## Artifacts reviewed (sha256)

All twenty-two hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 19 of 19 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 145 strict-ancestor entries; 2,232 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 19 of 19 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 144/001's, the previous merge run. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| The merge | Parents `10222646` (144) and `809b0dab` (145). The difference from the first parent is the two files of 145, three lines added and two removed. Git's own three-way merge of the parents gives the commit's tree: no hand edits. |
| Pull request 36 | Opened 2025-05-11T08:47:30Z, merged 18:09:15Z; the cutoff is the merge commit's 18:09:14Z. The session read the opening text and the one comment (maintainer, 13:38:02Z, edited 13:38:41Z). GitHub has no other comment, review comment or review on it. Both objects are before the cutoff. The quoted traceback, the Python 3.10 / CUDA 12.8 / Torch 2.7.0 build and "Seems ok, thx. Merging into dev branch in a bit" are as the entry reports them. |
| Catalog | Twelve open rows plus pull request 36 itself (issue 33 was closed at this cutoff). One closed row, issue 33; the entry draws nothing from it. Correct. |
| Architecture trigger | Does not fire. |
| Content | As verified at 145: the attribute, the assertion message that reads it only on rejection, `PAGE_SIZE` and `max_pages`, the two annotation edits, the helper and its two callers. Unchanged between the second parent and the merge. |
| Execution | Recorded output: 256, 257 and 511 give 256, 512 gives 512; `AttributeError` without the attribute and the intended `AssertionError` with it. Matches the prose; the sizes are labelled hypothetical. |
| Finding `empty-utf32-annotation` | Correct, and the same identity as 145's `empty-utf32-return-annotation`. No new record, as the request says. |
| Ledger `unset-max-total-tokens--r001` | Accepted. Fix-derived, introduced `543c4b27`, fixed `809b0dab`; consequence stated as the wrong exception type; no execution claimed. |
| Ledger `empty-utf32-return-annotation--r001` | Accepted as an annotation mismatch with no run-time effect. |

## Reviewer-only notes (never to a teacher)

- The pull request's traceback is the first external evidence in this walk that a defect from the first commit was
  hit in real use, a month after it was introduced. The ledger record may cite it at its next revision.
- The contributor built on Python 3.10. Their branch descends from 143 and so does not contain 136's integer
  check; their "works well" says nothing either way about the top-K compatibility record.

## Not verified

- Any generator construction or job submission.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, at the next revision of `exllamav3-unset-max-total-tokens`: add `9c31971b` as the merge that brings the
   fix to the development line, and the pull request's traceback as an observation.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the two ledger acceptances.
2. Continue the walk at commit 147.
