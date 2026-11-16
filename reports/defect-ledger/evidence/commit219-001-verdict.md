# Verdict: commit-000219-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000219-001`
Packet: `.teacher/retrieval/000219-001`
Upstream: `62e8832603ffc3c8089417f384f14d57f3ef6a52` "MLP: Allow unpadded (FP16) tensors"
Request: `reviews/requests/commit-000219-001.md` (sha256 `c7392622b6b0cb151aeeff69d34c6e6c9ce05c2ae5fb8fe2bf52dfa091410fb6`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is true as stated.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 11 of 11 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 218 strict-ancestor entries; 3,101 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 11 of 11 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 218/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-01T23:57:27Z; my query agrees. One closed row by path alone. |
| The change | `MLP.__init__` gains `activation_fn = "silu"` and `pad_to = 128`; `pad_to` is passed to both `Linear` projections; nothing else changes. Correct. |
| Why it matters | `Linear` rounds both widths up to a multiple of `pad_to` and asserts the input width was not padded unless allowed; neither MLP projection allows it, so a width that is not a multiple of 128 failed at construction. With `pad_to = 1` both widths are exact. Correct. |
| Callers | No construction of the plain `MLP` class anywhere in the tree. Correct. |
| Finding: ignored activation | The new `activation_fn` is neither stored nor read; `forward` still applies SiLU. True, with the stated reach (the exposed interface only). |
| Arithmetic | 130 and 257 round to 256 and 384 at 128 and stay exact at 1. Agreed. |
| Execution | A standard-library integer check; labelled. |

## Reviewer note (not in the entry; minor)

The constructor's `qmap` still defaults to `None` and is concatenated with a string for both projections, so
constructing the class without a `qmap` raises. An unpadded FP16 block is the case most likely to have none.
Present before this commit; source reading only.

## Not verified

- Any loading or execution of an unpadded block.

## Must fix before canonical use

None.

## Follow-ups

1. Ledger, with 220's request: the ignored-activation finding as suspected, introduced at `62e88326`, reach
   limited to the exposed interface.

## Next

1. Record this approval with `--approve`.
2. Proceed to 220.
