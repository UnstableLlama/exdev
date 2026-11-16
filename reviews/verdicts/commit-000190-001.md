# Verdict: commit-000190-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000190-001`
Packet: `.teacher/retrieval/000190-001`
Upstream: `c94905bf794f3b3bee00cd1f6645e624cc33cd12` "RMSNorm: Reduce CPU overhead"
Request: `reviews/requests/commit-000190-001.md` (sha256 `c24ccc7f46dce723f22a7220537c23230162db56bbf7c9ce7547a58a1dc79408`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and both inherited findings are true as stated. One consequence of the
removed Python view is not in the entry (below).

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 11 of 11 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 189 strict-ancestor entries; 2,828 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 11 of 11 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 189/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-25T11:53:01Z; my query agrees. One closed row by terms, selected. |
| Python | `forward` no longer flattens `x` or reshapes `y`; it allocates `empty_like(x)` with the output dtype and returns it. Correct. |
| Native | Width is the last dimension, checked divisible by four and equal to the weight length; `x` and `y` must have the same full shape; the row count is the product of the leading dimensions. The kernel is unchanged. Correct, and the two edits depend on each other as the entry says. |
| Callers | `RMSNorm.forward` passes five arguments; the three calls in `tests/test_ext_norm.py` pass four. Correct. |
| Finding: dtype dispatch | Anything that is not float is treated as half for both input and output, so the final "invalid datatypes" branch cannot be reached. True; inherited. |
| Finding: test arguments | The native function takes five parameters and the tests supply four. True; inherited; not executed. |
| Execution | Offset arithmetic for 255 small shapes; labelled as arithmetic. |

## Not verified

- Any build or GPU execution; the time saved.

## Must fix before canonical use

1. The removed `x.view(-1, x.size(-1))` did one more thing than bookkeeping: `view` raises when the tensor's
   strides do not allow flattening, so a non-contiguous input was refused. The native code reads `x.data_ptr()`
   as dense rows and has no contiguity check, so such an input is now read wrongly without an error. The entry
   lists strided layouts only as "not established". Every call site in the tree passes a freshly produced or
   viewed contiguous tensor.

## Follow-ups

1. Ledger: both inherited findings gain `c94905bf` as affected if identities exist; otherwise file them as new
   identities at their recorded introductions. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 191.
