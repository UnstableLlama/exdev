# Verdict: commit-000230-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000230-001`
Packet: `.teacher/retrieval/000230-001`
Upstream: `2f8254fe00445db8554ff5150db42f9b49c73687` "RoPE: Allow precomputed frequencies for special RoPE types (Pixtral etc.)"
Request: `reviews/requests/commit-000230-001.md` (sha256 `fc91aa06f1c274a6a3e87821b3df653afbe5f9339b17290080579a5078635687`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and all three findings are true as stated: one new, two inherited and
labelled so.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 24 of 24 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 229 strict-ancestor entries; 3,187 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 24 of 24 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 229/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-03T01:06:24Z; my query agrees. Four closed rows, two by path alone; discussion links are called inferences. |
| Python side | All three attention decode methods fetch `params["inv_freq"]` for their device and pass it as a new last argument; `RoPE.apply` uses it in place of its own vector when given. Existing callers omit it. Correct. |
| Native side | A one-dimensional tensor keeps `angle = inv_freq[t] × position`. A two-dimensional one must be float32 with second dimension equal to half the head width, and the kernel reads `inv_freq[pos × width + t]` as the angle itself, still taking sine and cosine and applying `attn_factor`. The rotary width now comes from the tensor's last dimension. Correct. |
| Positions | The row is the same resolved position as before: token index plus offset, plus a per-batch offset, or an explicit ID. Correct. |
| No producer | Nothing builds such a table and nothing named Pixtral exists in the tree. Correct. |
| Finding: table row bounds | The wrapper checks the table's width and nothing about its length; a (2, 64) table with position 2 reads from index 128, the element count. True; reach is a caller-supplied table. |
| Finding: padded reads (inherited) | The thread block is rounded up to whole warps and every thread reads its frequency before the rotary-width test; in table mode a padded thread reads into the next row or past the end. The 185 identity, extended. True. |
| Finding: reduction store (inherited) | Unchanged from 185. True. |
| Execution | A standard-library check that a table of position × frequency reproduces the vector path, the warp rounding for width 80, and the index 128; labelled as a model. |

## Not verified

- Any CUDA build or execution.

## Must fix before canonical use

None. Minor, for completeness: the table is also read through `data_ptr()` with no contiguity check, like the
other tensors in this wrapper.

## Follow-ups

1. Ledger, with 231's request: the table-row-bounds finding as a new suspected identity introduced at
   `2f8254fe`; the two 185 identities each gain this commit as an observation, the padded-read one noting the
   table case. No duplicates.

## Next

1. Record this approval with `--approve`.
2. Proceed to 231.
