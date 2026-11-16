# Verdict: commit-000186-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000186-001`
Packet: `.teacher/retrieval/000186-001`
Upstream: `1284d43c76349160992d42a241c81071fcc7b919` "GEMM kernel tweaks and tuning"
Request: `reviews/requests/commit-000186-001.md` (sha256 `a4be6fb8e82111f604fd11c25026397f1b13768790de1affbb74abe868df3131`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and all three findings are true as stated. The entry separates what the code
does from why, and claims no measured speedup.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 19 of 19 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 185 strict-ancestor entries; 2,795 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 19 of 19 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 185/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-25T11:33:39Z; my query agrees. One closed row by terms (issue 5), selected, described as context only. |
| Shape 1 | Tile unchanged at (16, 16, 128); stages go from 3 and 2 to 6 and 5; registered again in both kernel tables. Correct. |
| Pipeline | The repeated stage body becomes the `FSTAGE` macro with the same statements in the same order; the one- to four-fragment loops list the same load and multiply pairs as before; a five-fragment loop is added. The macro's `break` leaves the enclosing `while`. Correct. |
| Selector | Ampere and older at up to 4 bits: shape 2 when K is at most 2,048, whatever N is. Ada at up to 3 bits: shape 2 when K is at most 2,048, single GEMM only. Hopper and Blackwell at exactly 2 or 4 bits: shape 1 when K is at most 2,048, single GEMM only. Both callers pass the new flag. Correct. |
| Block caps | Single GEMM: tiles (no division), clamped to at least one. Multi-GEMM: tiles divided by 24 where it was 12, no clamp. Correct. |
| Benchmark | Bit width variable 8 to 1, runs 50 to 60, one new dimension pair, shape 1 included. Correct. |
| Finding: zero multi grid | With fewer than 24 tiles the multi cap is zero and `exl3_mgemm` computes `total_sms / num_sms` with no guard. True. The entry's example (K 512, N 128, shape 2) gives 16 tiles: one block before, none now. |
| Finding: Boolean threshold | `(size_k && bits >= 3) > 8192` is still in the Hopper and Blackwell branch. True; inherited. |
| Finding: stale declaration | `exl3_kernel_map.cuh` still declares the five-argument form; the definition takes six; both calls are in the defining file. True. |
| Execution | Fragment-order and integer models in Python; labelled as such. |

## Not verified

- Any compilation, kernel execution or timing; whether real model dimensions reach fewer than 24 tiles.

## Must fix before canonical use

1. Say that the single-GEMM clamp removes the zero-block case on that path, which earlier entries recorded for
   both; the entry reports the clamp but not that it is a repair.
2. The comment "Shape 1 not currently used anywhere" above the kernel tables is now false; the entry does not
   mention it.

## Follow-ups

1. Ledger: `exllamav3-gemm-zero-grid-cap` gains `1284d43c` as affected for the multi path, with the wider range
   (fewer than 24 tiles), and a note that the single path is clamped from this commit; whether to record that as
   a partial fix is Astra's call, provided the multi path stays open. `exllamav3-boolean-dimension-threshold`
   gains `1284d43c` as affected. The stale declaration may be filed as a new suspected compatibility identity.
2. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 187.
