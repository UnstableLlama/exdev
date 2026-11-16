# Verdict: commit-000179-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000179-001`
Packet: `.teacher/retrieval/000179-001`
Upstream: `30c7386b7c6a8f6899729975ef5da13cbf7b34f3` "BlockSparseMLP: Small optimization"
Request: `reviews/requests/commit-000179-001.md` (sha256 `bf863cd5d7cb3fc8b759344aeaa0989d970a6527b538d286497278c541cb3b47`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The equivalence claim is limited correctly to finite logits in exact
arithmetic, and the entry says the two edits depend on each other.

Ledger candidates **accepted**: `exllamav3-first-pass-cost-buffer--r001`, `exllamav3-sorted-argmax--r001`
(both introduced at `543c4b27`, suspected, source-only).

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 17 of 17 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 178 strict-ancestor entries; 2,725 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 17 of 17 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 178/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-24T00:08:29Z; my query agrees. No closed row qualifies. The three discussions read are open rows, described as shared context only. |
| The change | The softmax over all experts is removed; `topk` takes the router logits; the division by the selected sum becomes a softmax over the selected values. Correct. |
| Equivalence | Softmax is monotonic, so the same experts are selected, and the full denominator cancels in the old renormalisation; the selected-only softmax gives the same weights. Correct, with the stated limits (half precision, ties after rounding, non-finite values). |
| Dependent edits | Dropping the full softmax while keeping the division would divide raw logits by their sum. Correct. |
| Consumers | The Torch path and the fused path use `routing_weights` and `selected_experts` as before. Correct. |
| Inherited finding | The fused buffers are sized by `num_experts_per_tok` while `topk` returns `num_experts` indices under `activate_all_experts`; `exl3_mgemm` checks the index count against the output's first dimension. Unchanged. True, conditional as stated; conversion sets the flag at `convert_model.py:314`. |
| Execution | A 900-case double-precision transcription; maximum difference 2.2e-16; labelled as algebra, not repository execution. |

## Not verified

- Any tensor or GPU execution; behaviour in half precision.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: the optional-output identity and the three 174 identities are still owed.

## Next

1. Record this approval with `--approve`.
2. Proceed to 180.
