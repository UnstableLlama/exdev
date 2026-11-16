# Verdict: commit-000147-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000147-001`
Packet: `.teacher/retrieval/000147-001`
Upstream: `beb7bcd96d0d54ee2511a84f63632d0fe3590050` "humaneval.py: fix top_k type, remove rep_p, add qwen3"
Request: `reviews/requests/commit-000147-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry keeps three things apart that the commit title runs together: a real
fix at the command line (top-K parsed as an integer), the removal of a control that the contributor found broken
(which repairs nothing underneath), and a prompt preset that is steering, not architecture support. It also sees
that the reporter, the pull request's author and the patch's author are one person. No findings, and I found none.

The ledger revision `exllamav3-unset-max-total-tokens--r002` is **accepted**.

## Artifacts reviewed (sha256)

All twenty-four hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 12 of 12 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; 1,827 blobs hash to their names; no evidence timestamp after the cutoff. |
| Ancestry | The parent is `3c9ede55` (position 124, "Use ComboSampler and add more prompts in HumanEval"). The packet holds exactly 124 strict-ancestor entries; nothing from 125 on is in it. Correct for a pull request branched from there. |
| Replay | 12 of 12 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 145/001's, the previous non-merge run. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Pull request 35 at the cutoff | Cutoff 2025-05-11T08:42:55Z, the commit's own date. The snapshot has the opening text (03:34:41Z) and the contributor's comment of 05:32:04Z as edited at 06:13:49Z, and nothing later. Its title is "humaneval.py: fix top_k type and remove rep_p". GitHub's timeline shows the title was changed to the present one at 08:45:23Z, after the cutoff, so the packet's title is the right one for this position. The next comment is 09:24:51Z. I searched the packet for text of the later comments and found none. |
| Catalog | Twelve open rows: 1, 4, 7, 10, 14, 22, 26, 27, 28, 29, 34, 35 (33 was closed then; 36 was opened five minutes later). One closed row, issue 33. Correct. |
| Architecture trigger | Does not fire. `Qwen3Model` is already in the registry at this parent. |
| The change | A `qwen3` entry in `prompt_formats` (ChatML with `<think>\n\n</think>\n\n` before the answer prefill, four-space prefix); `rep_p = args.rep_p` removed from the `ComboSampler` call; `--top_k` becomes `type = int`, default 0; the `-repp` option removed. Nothing else. Correct. |
| Sampler at this parent | `rep_p` defaults to 1.0, for which `SS_RepP.alt` gives a no-op; the argmax branch is taken for a temperature of 0 only (this line of history does not contain 136). Correct. |
| Execution | Recorded output: with the float parser, `--top_k 5` and `5.0` give 5.0 and a slice `TypeError`; with the int parser, `5` gives a valid slice and `5.0` is rejected; both defaults disable the filter. Matches the prose. |
| Source notes | The 0 percent report and the same-person observation are as in the pull request. Issues 29 and 33 are named only as shared vocabulary. Correct. |
| Ledger `unset-max-total-tokens--r002` | Accepted. Adds the merge `9c31971b` as the clean arrival of the fix and the pull request 36 traceback as a contributor report, with the limits stated. |

## Reviewer-only notes (never to a teacher)

- **Hindsight, read by me on GitHub.** Later comments on this pull request explain the 0 percent result. At
  2025-05-11T15:33:57Z the maintainer writes that the penalty kernel turned a masked token into NaN, the masked
  token being the end-of-turn token prohibited by `min_new_tokens`, and that a fix would follow in dev. That is the
  defect fixed at 142 (cutoff 15:27:10Z, six and a half minutes before the comment, so 142's teacher could not
  have had it). It confirms the ledger identity `exllamav3-repetition-penalty-masked-nan` and gives it a concrete
  trigger. The comment is eligible evidence only from position 144 on.
- **Also hindsight:** the same thread later attributes poor Qwen3 scores to a BOS token being added, and the
  maintainer says the prompt formatting was reworked. This script requests BOS, as the entry notes. Expect a
  change to that.
- **Two fixes for one mismatch.** This commit fixes the float top-K at the script; 136 fixed it in the sampler
  (and introduced the Python 3.12 problem). When they meet at the merge, an integer from this parser is exactly
  the input that fails on Python 3.10 and 3.11.

## Not verified

- Any generation or scoring, and the contributor's figures.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: at the next revision of `exllamav3-repetition-penalty-masked-nan`, add the maintainer's explanation as an
   external observation, marked as eligible only from 144 on.
2. Ledger: the `humaneval-top-k-float` site (second site of 92's record) is fixed here at `beb7bcd9`; record it when
   that revision is written.
3. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the ledger acceptance.
2. Continue the walk at commit 148.
