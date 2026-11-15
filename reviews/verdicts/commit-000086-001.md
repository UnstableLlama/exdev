# Verdict: commit-000086-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000086-001`
Packet: `.teacher/retrieval/000086-001`
Upstream: `0a4b2b210323489b3b830668fb86e22599bf54fb` "Merge remote-tracking branch 'gakada/master'"
Request: `reviews/requests/commit-000086-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry treats the merge as an integration, ties it to pull request 20 as an
inference from matching content, and reports the participants' statements as theirs.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 15 of 15 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review (two parents); 39 of 39 implementation hashes; exactly 85 strict-ancestor entries, from both parents; 1,200 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 15 of 15 recorded tool calls identical, including the `run` call. |
| Standing instructions | Differ from 85/001's by exactly two added sentences, both about `merge_facts` ("mechanically verified Git tree comparisons" and what an identical tree means). The two earlier merge runs (11/001, 43/001) carry merge sentences too. Nothing else differs; no reviewer input. |
| Merge facts | Recomputed from Git: task tree `c8f2d66a`, first-parent tree `531ce79d`, second-parent tree `1290f3d0`, identical to neither. All three match the packet. The diff against the first parent is byte-identical to the side branch's own diff (`1f5a43fc..105cafab`), so the merge is clean and adds nothing of its own. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 20. Matches the seven open rows. |
| Pull request 20 | Read the cutoff-bound copy the teacher saw. gakada's opening post reports the Reka Flash 3 quantisation mismatch and the raw/reka HumanEval table; on 24 April gakada shows the both-axes case erroring, turboderp proposes a two-axis copy, gakada suggests leaving it an error until a model needs it, turboderp agrees (15:26 UTC). All before the cutoff. The draft's account is accurate and attributed. |
| Source claims | Same code as 84 and 85, verified there; `LinearFP16.forward` does not pad activations. Correct. |
| Findings | Both are the observations 84/001 made, carried through the merge. See "Must fix" on classification. |

## Not verified

- Any load, quantisation or evaluation. The entry says none was run.
- The scores in the pull request's table; they are the contributor's.

## Must fix before canonical use

Reviewer-only. None of this goes to a teacher.

1. The both-axes observation is `simultaneous-axis-padding (defect)` in 84/001 and
   `simultaneous-padding-restriction (new_requirement)` here. It is one identity. The reclassification is defensible:
   the discussion shows the authors chose to leave it an error. The ledger should carry one record with both
   observations and say that the limitation was accepted in pull request 20, not two records.
2. The pull request says Reka Flash 3 "has both output and input sizes that are not divisible by 128". The entry does
   not ask whether the accepted one-axis restriction then stops that very model from loading, or whether its two
   unaligned sizes fall on different layers. Worth a sentence in a canonical entry.
3. The activation-width gap noted in my 84/001 verdict applies here unchanged.

## Next

1. Record this approval.
2. Continue the walk at commit 87.
