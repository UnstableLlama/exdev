# Verdict: commit-000200-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000200-001`
Packet: `.teacher/retrieval/000200-001`
Upstream: `f45eb4ce2090ca5db306cf863ee2f1826810e0ff` "Support QK LayerNorm"
Request: `reviews/requests/commit-000200-001.md` (sha256 `3bd5987af2bf1864a10b290c6b9308b311443793a206ca02dfa4e0026c141980`)
Reviewed: 2026-11-16, working tree on top of `e9e83ff`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and all three findings are true as stated. This is the first walk run under
guidance 9.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 29 of 29 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 199 strict-ancestor entries; 2,917 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 29 of 29 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions equal 199/001's plus a blank line plus paragraph E (`GUIDANCE_9_ADDITION`), exactly. Manifest `guidance_version` 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fifteen open rows at 2025-05-30T14:58:00Z; my query agrees. One closed row by path alone; the entry calls the discussion links inferences. |
| Constructor | Q and K norms may be RMSNorm or LayerNorm; K still required with Q; the RMSNorm branch keeps the epsilon equality check and constant bias; the LayerNorm branch takes Q's epsilon and a zero bias. Correct. |
| Load | The fused-norm tensors are set only for RMSNorm; they stay `None` for LayerNorm. Correct. |
| Decode paths | All three now normalise before RoPE when there is no RoPE or no fused tensor, replacing the former `elif` after RoPE. V is not normalised. Correct. |
| LayerNorm | Rank-one weights use the old call; otherwise the last axis is normalised without affine parameters, then multiplied by the weight and the bias added. `forward_torch` is unchanged. Correct. |
| Model builders | Qwen3, Qwen3 MoE and Gemma3 pass RMSNorm; nothing in the tree passes a LayerNorm for Q/K. Correct. |
| Worked example | Rows [1, 3] and [2, 6] normalise to [-1, 1]; with the two affine rows the results are [-1, 3] and [-1, 7]. I worked it by hand and agree. |
| Finding: tensor truth value | With RoPE and RMSNorm, `not self.q_norm_tensor` is evaluated on the weight tensor, which raises for more than one element, in all three decode methods; the three builders above reach it. True. |
| Finding: `forward_torch` | Still passes a multidimensional weight to `F.layer_norm` with a one-axis shape; no caller in the tree. True, with the stated reach. |
| Finding: inherited native | As recorded at 185 and unchanged here; kept as inherited, not a new identity. True. |
| Execution | One standard-library calculation; labelled as a model. |

## Reviewer knowledge (hindsight, never to a teacher)

Upstream `95c5097b` (2025-05-31) "Fix q_norm_tensor None check" replaces `not self.q_norm_tensor` with
`self.q_norm_tensor is None` in all three places, the day after this commit. That confirms the first finding.
Do not record the fix before the walk reaches it.

## Not verified

- Any PyTorch or GPU execution; the exception itself was not reproduced.

## Must fix before canonical use

1. Minor: the constructor branches on Q's type only. An RMSNorm Q with a LayerNorm K fails on a missing
   `rms_norm_eps`; a LayerNorm Q with an RMSNorm K is accepted. The entry does not say that mixed types are
   unchecked.

## Follow-ups

1. Ledger: the tensor-truth-value finding may be filed as suspected, introduced at `f45eb4ce`; the
   `forward_torch` one as suspected with its reach. The inherited group keeps its 185 identities. Earlier owed
   items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 201.
