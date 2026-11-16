# Verdict: commit-000233-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000233-001`
Packet: `.teacher/retrieval/000233-001`
Upstream: `d4cdab818dfaa29854a5d218366e4c603036783a` "MLP: Allow output size different from hidden_size"
Request: `reviews/requests/commit-000233-001.md` (sha256 `c60c0917b35e07340cb9c97d51491317a1044df19ffc34f583a6d2ff1c1c364e`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The one finding is the existing `mlp-unsupported-activation` identity
carried over, true as stated. The ledger item filed with this request is accepted.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 14 of 14 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 232 strict-ancestor entries; 3,207 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 14 of 14 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 232/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-03T01:08:33Z; my query agrees. One closed row by path alone. |
| The change | `MLP.__init__` gains `out_size = None`, placed between `intermediate_size` and `key_up`; the down projection's output width is `out_size` when given and `hidden_size` otherwise. Nothing else. Correct. |
| Positional shift | A caller passing `key_up` positionally would now bind it to `out_size`. The one caller in the tree, Gemma 3's vision tower, uses keywords and does not pass `out_size`. Correct. |
| Consumers | Both block classes add the MLP result to the residual without adapting its width, so a different output width only works outside them. Correct. |
| Arithmetic | Down projection (256, 128) by default; (256, 256) for `out_size` 130 at alignment 128; (256, 130) at alignment 1. Agreed. |
| Inherited finding | The two-arm `match` is unchanged. True; no new identity. |
| Execution | Integer arithmetic only; labelled. |

## Not verified

- Any PyTorch execution.

## Must fix before canonical use

None.

## Ledger items filed with this request

- `exllamav3-activation-odd-tail--r001`: **accepted.** Suspected, introduction at the root commit (I confirmed
  the `numel / 2` bound is in the root tree's kernel at 232), `3637103e` recorded as the first exposure to a
  caller, kept distinct from the BF16 conversion identity, no fix.

## Follow-ups

1. Ledger, with 234's request: `exllamav3-mlp-unsupported-activation` gains this commit as an observation.
   Optional; it may be batched with the next revision of that record.

## Next

1. Record this approval with `--approve`.
2. Proceed to 234.
