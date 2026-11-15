# Verdict: commit-000122-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000122-001`
Packet: `.teacher/retrieval/000122-001`
Upstream: `a65386545773f0e1dc66146e7050f6c0f5a9e3e4` "rep_pen: Prevent -inf*0 + -inf*1 == NaN if input logits are masked"
Request: `reviews/requests/commit-000122-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and the finding is correct and is the most useful thing in the entry: the offset
repairs the factor-zero end of the interpolation and leaves the factor-one end exactly as it was.

## Artifacts reviewed (sha256)

All twelve hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 121 strict-ancestor entries; 1,777 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 121/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 25, 26, 27, 28, 29. Matches the twelve open rows. |
| Architecture trigger | Does not fire. |
| Diff claim | In `apply_rep_pens_kernel`, `float f = factors[i];` becomes `float f = factors[i] + 1e-30;`. Nothing else. Correct. |
| Kernel | Factors start at 0; an occurrence within `sustain_range` sets 1; otherwise an atomic maximum of the linear decay; `w = v > 0 ? v / rep_p : v * rep_p`; `o = v * (1 - f) + w * f`. Correct. |
| Factor zero | Before: `-inf * 1 + (-inf) * 0` is NaN. After: `f` is about 1e-30, `1 - f` rounds to 1, both terms are `-inf`. Correct. |
| Factor one | `1 + 1e-30` rounds to 1 in float, `1 - f` is 0, `-inf * 0` is NaN, before and after. Correct. |
| Offset size | 1e-30 is above the smallest normal float (about 1.18e-38) and vanishes when added to 0.5 or 1. Correct. |
| Callers | `SS_RepP.run` calls `ext.apply_rep_pens` from `INIT` (new float32 output) and from `LOGITS` (in place); `alt()` gives a no-op for `rep_p == 1.0` or a non-positive window; the wrapper requires batch size 1 and dispatches half or float input to the same template. Correct. |
| Execution | Recorded output: NaN then `-inf` at 0; `-inf` both ways at 0.5; NaN both ways at 1; 1.0000000031710769e-30. Matches the prose. Python arithmetic rounded to float, as the entry says. |
| Ancestor note | Reads and links the entry for `40863d06` (position 90, "Add repetition, presence and frequency penalties"). Correct. |
| Finding `masked-full-penalty-endpoint` | Correct, and correctly called inherited: line 78 is unchanged since `40863d06` and no commit in between touched the file. Suspected is right, since nothing ran on a GPU. |

## Reviewer-only notes (never to a teacher)

- **How far the remaining endpoint reaches.** `SS_RepP`'s default `sustain_range` is `int(10e7)`, so by default every
  token in the history has factor exactly 1. `CustomSampler.forward` applies the vocabulary, blocked-token and
  allowed-token masks before any step. So with a repetition penalty on, any masked token that also occurs in the
  history yields NaN; an `allowed_tokens` filter makes that the ordinary case. A NaN logit then poisons any later
  normalization of the row. The entry is right to stop at "reachable through `SS_RepP`"; it executed nothing.
- **What the commit fixed was the larger half.** Before it, every masked token that was *not* in the history became
  NaN whenever the penalty step ran. Neither the entry for 90 nor my verdict there recorded it.
- The presence/frequency kernel subtracts and has no such product.

## Not verified

- Any GPU execution, including whether the compiler contracts the expression.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, when next revised: one identity, "repetition penalty turns masked logits into NaN", introduced at
   `40863d06` (90). Its factor-zero case is fixed at `a6538654` (fix-derived from this commit); its factor-one case
   remains open (this entry's finding). Record it as partially fixed, not as two defects.

## Next

1. Record this approval.
2. Continue the walk at commit 123.
