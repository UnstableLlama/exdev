# Verdict: commit-000081-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000081-001`
Packet: `.teacher/retrieval/000081-001`
Upstream: `46f98ca32ddf1ad82b3deeff5a2744ef9f11f1e5` "Add some comments"
Request: `reviews/requests/commit-000081-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

A comments-only commit. The entry did what such an entry should: it checked the new descriptions against the code they
describe and found one that does not match.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 9 of 9 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 80 strict-ancestor entries; 1,164 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 9 of 9 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 80/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 20. Matches the seven open rows. |
| Diff claims | Thirty added lines, no removals: nine class docstrings and one TODO in `CustomSampler.__init__`. No executable line changes. The sort docstring does end in the fragment "state.indices". Correct. |
| Finding `top-p-description-mismatch` | Correct. The new docstring says "smallest set of top tokens with a cumulative probability greater than P". The code computes `mask = cumsum <= top_p` and applies it from the second column on, so the token whose inclusion crosses P is dropped, and the first token is always kept. The existing `TopPSampler` docstring ("top probabilities <= top_p (at least 1 candidate)") describes the code; the new one does not. The worked example (0.5, 0.25, 0.125, 0.125 with P = 0.625 keeps only the first) follows from the code. |
| Finding `inherited-sorted-argmax` | Unchanged by this commit; same defect as 80 and earlier. |

## Not verified

- Any sampler execution. Nobody ran one; the entry says so.

## Must fix before canonical use

Reviewer-only.

1. `top-p-description-mismatch` is classed `defect`. It is a documentation mismatch: the code did not change and matches
   its older description. The ledger classification should say so, and should not imply which of the two is intended.

## Next

1. Record this approval.
2. Continue the walk at commit 82.
