# Verdict: commit-000181-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000181-001`
Packet: `.teacher/retrieval/000181-001`
Upstream: `afac0a4320d9c4df31a8747ad1061da521698117` "Keep k_proj and v_proj bitrate equal"
Request: `reviews/requests/commit-000181-001.md` (sha256 `e9ad7dc05341ef6ff2788087cbe7642f8ab2b47cdd909ae206aa30238c504f03`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

The description of the change is correct and every number in the entry reproduces when I run the task's own
`allocate_transformer`. The new finding is true. The inherited finding reports the code's behaviour correctly
but its "expected" side needs a qualification before canonical use (below).

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 9 of 9 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 180 strict-ancestor entries; 2,745 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 9 of 9 recorded tool calls identical, including the three `run` calls. |
| Unassisted | Standing instructions byte-identical to 180/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-24T11:30:23Z; my query agrees. No closed row qualifies. |
| The change | Two Q/K/V/O increment patterns change: `[0,0,1,0]` to `[0,1,1,0]` and `[0,0,2,0]` to `[0,2,2,0]`. Nothing else. Correct. |
| Callers | `TransformerBlock.allocate_q` and `ParallelDecoderBlock.allocate_q` are the direct callers. Correct. |
| Execution (mine) | Running the task file's function with four 128-weight projections, target 3, surplus 383 gives 3/4/4/3 and surplus 128; with sizes 256/128/128/256, target 3, surplus 640 it gives 3/4/5/4 and surplus 1; with four 128-weight projections and surplus 255 it gives 3/3/3/3 and surplus 256. All equal the entry's figures. |
| Finding: remaining unequal K/V | The pattern `[0,1,2,1]` is still in the table and is selected in the second case above. True. Whether the commit meant equality in every case is a reading of its title, as the entry says. |
| Inherited finding | `bisect_right(options, (budget,))` sorts the one-element tuple before an equal-cost candidate, so a candidate whose cost equals `budget` is not selected. True of the code. |

## Not verified

- Any model conversion; which budgets real models produce.

## Must fix before canonical use

1. The inherited finding's "expected" side should say that `budget` is `int(bpw * numel) + surplus_bits + 1`:
   it is already one bit more than the target plus the bits carried in. In the entry's example the bits actually
   available are 1,791, and the "exact" candidate costs 1,792, so excluding it keeps the allocation within the
   real total. What the extra bit does do is come back out in the returned surplus: called five times in a row
   with nothing spent beyond the base, the function returns surplus 1, 2, 3, 4, 5 (my run). The defect, if it is
   one, is that drift, not a missed exact fit. The root entry's wording has the same gap.

## Follow-ups

1. Ledger: an identity for the remaining-unequal finding (suspected; executed on the extracted function with
   synthetic sizes). For the inherited boundary, file it with the qualification above or hold it; do not file it
   as "exact match excluded" without the plus-one.
2. The optional-output identity and the three 174 identities are still owed.

## Next

1. Record this approval with `--approve`.
2. Proceed to 182.
