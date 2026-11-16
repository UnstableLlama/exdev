# Verdict: commit-000207-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000207-001`
Packet: `.teacher/retrieval/000207-001`
Upstream: `95c5097b3099de821058504a282d7f83cf3369b2` "Fix q_norm_tensor None check"
Request: `reviews/requests/commit-000207-001.md` (sha256 `e8a75ebb2ccc72511c3abe446ba71ccee8a0ffce4e313fe990edfc12818c85bc`)
Reviewed: 2026-11-16, working tree on top of `e9e83ff`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The fix attribution is true and the one finding is the inherited 185 group,
true as stated.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 13 of 13 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 206 strict-ancestor entries; 2,971 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 13 of 13 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 206/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. The teacher learned of the regression from the approved 200 entry, which is legitimate ancestor context. |
| Catalog | Fifteen open rows at 2025-05-30T22:52:40Z; my query agrees. One closed row by path alone; discussion links are called inferences. |
| The change | Three lines: `not self.q_norm_tensor` becomes `self.q_norm_tensor is None` in the three decode methods; no other occurrence remains. Correct. |
| Dispatch after it | The tensors are `None` unless an RMSNorm was loaded, so LayerNorm still normalises separately and RMSNorm with RoPE goes to the fused kernel; the no-norm and no-RoPE cases short-circuit as before. Correct. |
| Fix attribution | The tensor-truth-value finding recorded at 200 is removed by this commit. True. |
| Inherited finding | The 185 reduction and padded-read concerns, unchanged native code, now reachable again through the fused path. True as recorded at 185. |
| Execution | A Python stand-in whose truth value raises, and one integer calculation; labelled as a model. |

## Not verified

- Any PyTorch or GPU execution.

## Must fix before canonical use

1. Administrative: the finding's location is written against the parent `2cc8f718` rather than the task commit.
   The file is identical at both, but locations elsewhere use the task commit.

## Follow-ups

1. Ledger: the 200 tensor-truth-value record may take `95c5097b` as its fix. The inherited group keeps its 185
   identities. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 208.
