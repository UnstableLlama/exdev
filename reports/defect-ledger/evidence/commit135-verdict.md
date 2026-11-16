# Verdict: commit-000135-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000135-001`
Packet: `.teacher/retrieval/000135-001`
Upstream: `edafdd1f3d9a966a982f54334838f4f94ee51473` "MGEMM: Use full grid when possible"
Request: `reviews/requests/commit-000135-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and both findings are correct. The teacher found the zero block cap on its own
(I had it only as a reviewer note at 133, which the packet does not contain) and saw that this commit turns it into
a division by zero. The scratch finding is right too, and "new requirement" is the right class for it.

Both ledger candidates are **accepted**.

## Artifacts reviewed (sha256)

All twenty-one hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 12 of 12 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 134 strict-ancestor entries; 1,937 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 12 of 12 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 134/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Eleven open rows: 1, 4, 7, 10, 14, 22, 26, 27, 28, 29, 34 (issue 33 was closed at this cutoff, 2025-05-11T00:04:57Z). No qualifying closed row of 23 candidates. No discussion was fetched. |
| Architecture trigger | Does not fire. |
| Launch | `total_sms` is saved before the selector lowers `num_sms`; `concurrency = MIN(total_sms / num_sms, bszm_out)`; the grid is `(num_sms, 1, concurrency)`. Correct. |
| Kernel loop | `i` advances by `gridDim.z`; `j = i + blockIdx.z`; a plane with `j >= bszm` gets a null `B` and skips the three work sections but still reaches every `sync`. All planes run the same number of loop iterations and row steps, so the barriers line up. Correct. |
| Pointers | Input: `A` when `bszm_in == 1`, else `A + j * size_m * size_k`. Scratch: always `A_had + j * size_m * size_k`. Output: always `C + j * size_m * size_n`. Weight: `B_weights[j]`. The "Advance" block is gone. Correct. |
| Locks | `lock_offs = blockIdx.z * size_n / 128`. The inner kernel indexes `locks[slice_m * blocks.n + slice2_n]` with `slice_m` now always 0, and the column-tile index is below `size_n / TILESIZE_N`, which is at most `size_n / 128`. Planes do not share locks. The buffer holds 1,048,576 entries. Correct. |
| `index_m` | Returns 0 instead of `blockIdx.y`; both wrappers launch with a y dimension of 1. Correct. |
| Selector | Only the comment changes, in both selectors; the `/ 12` cap is as before. Correct. |
| Execution | Recorded output: 120 SMs at width 32 with eight matrices gives three planes, 96 blocks and groups [0,1,2], [3,4,5], [6,7]; two matrices give 64 blocks; width 120 gives one plane; `(128//32)*(128//128)//12` is 0. Matches the prose. |
| Finding `zero-slice-division` | Correct. With shape 2 forced, `size_k = 128`, `size_n = 128`: `128 / 32 * 128 / 128 / 12` is 0 in C's left-to-right integer arithmetic, `MIN` stores 0 in `num_sms`, and the new line divides by it. Suspected is right. |
| Finding `broadcast-scratch-capacity` | Correct. At the parent the scratch pointer advanced only when `bszm_in > 1`; now every matrix has its own slice, so a shared input with several outputs needs `bszm_out` times the input's size. The copied comment still says "size and dtype as A", and nothing checks it. |
| Ledger `deferred-read-errno-reporting--r001` | Accepted. One record for both halves, introduced at `c8836d9f` (126), as my 126 verdict asked. I rechecked the source: CUDA declares the number at line 260 and never assigns it; CPU assigns it at line 240 and reports the generic text at line 250. |
| Ledger `conversion-handle-accumulation--r001` | Accepted. Fix-derived; caching at the first commit, five to eight handles at `647bb7d5` (119), normal-path fix at `4710c012` (128). Matches my 128 verdict, and it claims no measured limit. |

## Reviewer-only notes (never to a teacher)

All by source reading; nothing was built.

- **Where the zero cap comes from.** The `/ 12` line entered with the cooperative-launch rewrite at `5d470a29`
  (123), in the single-matrix selector. From 123 the single-matrix path launches a grid of zero blocks for such
  small matrices; 133 copied the line; 135 adds the division. One identity, three stages.
- **The 133 finding gets worse here.** The output offset is now unconditional. With several inputs and one output
  (leading dimensions 2 and 1), the parent overwrote the single output; the task writes the second result past the
  end of `C`. The out-of-range index read from 133 is still there.
- A scratch tensor that is the input itself, which the copied comment allows, is now also a race: plane 0 writes
  the transformed input over `A` while the other planes read `A`.

## Not verified

- Any compilation or execution, including how the division by zero shows itself.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: `zero-slice-division` approved. File it so the root is visible: the zero cap introduced at `5d470a29`
   (zero-block launch in `exl3_gemm`), carried into `exl3_mgemm` at `b73d0739`, division by zero added at
   `edafdd1f`. One record, not three.
2. Ledger: `broadcast-scratch-capacity` approved as drafted, a new requirement introduced at `edafdd1f`.
3. Ledger: add `edafdd1f` to the affected revisions of `exllamav3-multi-gemm-leading-dimension-validation`, with
   the changed consequence (write past the output).
4. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the two ledger acceptances.
2. Continue the walk at commit 136.
