# Verdict: commit-000151-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000151-001`
Packet: `.teacher/retrieval/000151-001`
Upstream: `95cfa726b63049e455e2037e1325ae6961e3be98` "top_k sampler: Fix int check for older Pythons"
Request: `reviews/requests/commit-000151-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry explains the one-line change exactly, and its reach is the right
one: the constructor runs before a disabled top-K step can be swapped for a no-op, so the fix matters even for the
default of zero. It does not claim to have reproduced the failure, which it could not on this machine, and it does
not name the version boundary, which nothing in its packet states. No findings, and I found none.

The ledger record `exllamav3-humaneval-unconditional-bos--r001` is **accepted**.

## Artifacts reviewed (sha256)

All nineteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 150 strict-ancestor entries; 2,272 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 150/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. In particular nothing in it states that `int.is_integer` arrived in Python 3.12; the entry's "unestablished" is an honest account of its evidence. |
| Catalog | Eleven open rows at 2025-05-12T00:34:32Z (33 closed then). Three closed rows: pull requests 35 and 30 and issue 21. The pull request 35 snapshot the session read runs to the comment of 21:08:59Z (edited 21:09:15Z); it does not mention this failure, and the entry labels the link as inference from the shared parameter. Correct. |
| Architecture trigger | Does not fire. |
| The change | `assert top_k.is_integer(), ...` becomes `assert isinstance(top_k, int) or top_k.is_integer(), ...`. The following `self.top_k = int(top_k)` is unchanged. It is the only use of `is_integer` in the package. Correct. |
| Reach | `ComboSampler` builds `SS_TopK(top_k)` in its non-argmax branch (`presets.py:113`), default `top_k = 0`; `TopKSampler` builds it when `top_k` is above 1 and the temperature is not 0 (line 55). Argmax branches do not. Correct. |
| Execution | Recorded output on Python 3.14.4: both forms accept 0, 1, 5 and 5.0, store integers, and reject 5.5. Matches the prose, with the stated limit that this version cannot show the difference. |
| Ledger `humaneval-unconditional-bos--r001` | Accepted. Fix-derived, introduced `543c4b27`, fixed `1e175478`; Qwen3 reach correctly not asserted at the root; no tokenizer run claimed; nothing recorded on the default-path intent. |

## Reviewer-only notes (never to a teacher)

- **This is the fix predicted at 136.** The commit title confirms the finding I recorded there from Python's
  documentation, and the short-circuit is the obvious repair. The defect lived from 136 (`a027848d`) to this
  commit's parent, and from the merge at 149 it also broke the HumanEval script's default invocation.
- The canonical-use conditions on 136 and 149 stand: those entries still lack the finding. This entry now gives a
  later reader the fact that integers needed special handling on older Pythons, in the maintainer's own words.
- How the maintainer learned of it is not in any eligible discussion I can see; pull request 35 does not mention
  it.

## Not verified

- Any execution on Python 3.10 or 3.11, before or after the fix.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: revise `exllamav3-top-k-int-is-integer-compatibility` with the fix at `95cfa726` and the commit title as
   upstream confirmation.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the ledger acceptance.
2. Continue the walk at commit 152.
