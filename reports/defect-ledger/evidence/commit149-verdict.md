# Verdict: commit-000149-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000149-001`
Packet: `.teacher/retrieval/000149-001`
Upstream: `f5127e87f800a4f11f2aa9605039896ac41d9382` "Merge branch 'master' into dev"
Request: `reviews/requests/commit-000149-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry does the one thing a merge entry most easily gets wrong: it does not
copy the second parent's explanation. It reads the first parent's sampler, sees that dev already converts top-K to
an integer, and says that on this line the merged change alters command-line validation and repairs no float
slice. No findings.

It again stops one step short on the integer check ("compatibility ... is unestablished here"). On this merge that
step matters more than at 136; see the reviewer section and follow-up 1. The statement is true, so approval for
ancestor retrieval stands, with the same canonical-use condition as 136.

The ledger revision `exllamav3-repetition-penalty-masked-nan--r002` is **accepted**.

## Artifacts reviewed (sha256)

All twenty-nine hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 10 of 10 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 148 strict-ancestor entries; 2,258 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 10 of 10 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 148/001's (both merges). |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| The merge | Parents `9c31971b` (146, dev) and `81a0a7d2` (148, master). The difference from the first parent is `eval/humaneval.py` alone, the change of 147. Git's own three-way merge of the parents gives the commit's tree: no hand edits. From here every earlier position is an ancestor. |
| Pull request 35 at the cutoff | Cutoff 2025-05-11T18:48:19Z. The snapshot is closed (merged 18:47:03Z), carries the present title, and ends with the comment of 18:46:37Z. Distinctive text of the later comments is not in the packet. Correct. |
| Catalog | Eleven open rows (33 closed then). Two closed rows, pull request 35 and issue 33. Correct. |
| Architecture trigger | Does not fire. |
| First parent's sampler | `SS_TopK.__init__` asserts `top_k.is_integer()` and stores `int(top_k)` (`custom.py:222`); the argmax branch is `temperature == 0.0 or top_k == 1`. As the entry says. |
| The change on this line | `--top_k` goes from `type = float`, default `0.0`, to `type = int`, default `0`; the penalty option and argument go; the `qwen3` preset arrives. Correct. |
| Execution | Recorded output: float parser gives `0.0` and `5.0`; int parser gives `0` and `5` and rejects `5.0`. Matches the prose. |
| Discussion | The contributor's reports and the maintainer's diagnosis are attributed and not claimed as verified. Correct. |
| Ledger `repetition-penalty-masked-nan--r002` | Accepted. Adds the maintainer's comment as an external observation with its availability time and the first eligible position on each line (144 on dev, 148 on master), and says that eligibility is not the same as the fix being present. Introduction, fixes and affected revisions unchanged. |

## Reviewer-only notes (never to a teacher)

- **This merge makes the HumanEval script fail by default on Python 3.10 and 3.11 (mine; documented behaviour, not
  executed).** At the first parent the script's default was the float `0.0`, and `float.is_integer()` exists on
  every Python, so the script worked there whatever the version. After the merge the default is the integer `0`;
  `ComboSampler` with the script's default temperature of 0.6 builds `SS_TopK(0)`; `int.is_integer()` does not
  exist before Python 3.12; the result is `AttributeError` at sampler construction. Neither parent has this
  failure in this script: master stores the integer unchanged, dev received a float. It is a defect created by the
  merge of two individually working states, and the wheel workflow on this same tree builds for 3.10 and 3.11.
- The hindsight note from 136 stands: upstream "top_k sampler: Fix int check for older Pythons" (`95cfa726`,
  2025-05-12) has not been reached yet.

## Not verified

- Any execution on Python 3.10 or 3.11, any generation or scoring.

## Must fix before canonical use

1. As at 136: the entry names the integer check as unestablished; a canonical entry should state it as a finding,
   here with the merge-specific reach.

## Follow-ups

1. Ledger: revise `exllamav3-top-k-int-is-integer-compatibility`: add `f5127e87` as affected, with the new reach
   (the HumanEval script's default invocation) and the note that it arises from the merge. Reviewer observation;
   excluded from historical context and training.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the ledger acceptance.
2. Continue the walk at commit 150.
