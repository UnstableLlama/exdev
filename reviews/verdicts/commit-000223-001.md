# Verdict: commit-000223-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000223-001`
Packet: `.teacher/retrieval/000223-001`
Upstream: `95c41ce0e15aa7362cc50aaf5d4efcd7dd4c2225` "MLP: Add switchable activation fn for MLP without gate"
Request: `reviews/requests/commit-000223-001.md` (sha256 `fbdadb82b19df4e89462d8364054210d81556638757703c29f2e9af204799c3b`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, the finding is true as stated, and the fix attribution is true.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 222 strict-ancestor entries; 3,131 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical. No `run` call. |
| Unassisted | Standing instructions byte-identical to 222/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. The teacher learned of the ignored option from the approved 219 entry, which is legitimate ancestor context. |
| Catalog | Sixteen open rows at 2025-06-02T00:02:11Z; my query agrees. One closed row by path alone. |
| The change | `MLP.__init__` stores `activation_fn` and a `match` sets `activation_fn_call` to `F.silu` for "silu" or to GELU with the tanh approximation for "gelu"; `forward` calls it in place of the hard-coded `F.silu`. Default unchanged. Correct. |
| Fix attribution | The 219 finding (option accepted but never read) is removed by this commit. True. |
| Finding: unsupported value | The `match` has no default arm, so any other string leaves `activation_fn_call` unset and `forward` raises `AttributeError` after the up projection. True, with the stated reach (the exposed interface only). `GatedMLP` has the same two-arm `match` from earlier history. |
| Callers | Still no construction of the plain `MLP` class in the tree. Correct. |

## Not verified

- Any PyTorch execution.

## Must fix before canonical use

None.

## Follow-ups

1. Ledger, with 224's request: `exllamav3-mlp-ignored-activation` takes `95c41ce0` as its fix; the
   unsupported-activation finding as a new suspected identity introduced at `95c41ce0`, reach limited to the
   exposed interface.

## Next

1. Record this approval with `--approve`.
2. Proceed to 224.
