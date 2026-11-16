# Verdict: commit-000133-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000133-001`
Packet: `.teacher/retrieval/000133-001`
Upstream: `b73d0739044d14ebe12a73bdbd154c1f28b36f19` "Add multi-GEMM kernel"
Request: `reviews/requests/commit-000133-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and both findings are correct. The entry reads all 22 sections, notices that the
header comment was copied from the single-matrix function and does not describe the real interface, and works out
the traversal rule (the loop runs to the larger leading dimension) that the first finding rests on.

No ledger revision was requested. The answer on the root header record is accepted: it already carries its fix.

## Artifacts reviewed (sha256)

All thirty hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 36 of 36 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 132 strict-ancestor entries; 1,904 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 36 of 36 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 132/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Eleven open rows: 1, 4, 7, 10, 14, 22, 26, 27, 28, 29, 34 (issue 33 was closed at this cutoff, 2025-05-10T22:04:33Z). Two closed rows, issues 5 and 9, both closed in April. Issue 5 has two comments, both of 2025-04-07. |
| Architecture trigger | Does not fire. |
| Binding | `m.def("exl3_mgemm", ...)` added. At the task no Python file names `exl3_mgemm`; the only Python callers of the extension's GEMM are the three `exl3_gemm` sites. Correct. |
| Interface | `A` and `C` rank 3; `B`, `suh`, `svh` rank 1 and `kLong`, read as `uintptr_t` lists; `A` is half; `C` is float or half; `K` is the bit width; a missing `indices` raises "Must specify indices"; `weights` is optional. The comment block above the function is the single-matrix one, including its "(m, k)" shapes. Correct. |
| Kernel loop | `bszm = MAX(bszm_in, bszm_out)`; per iteration: `B_indices[i]`, input transform into `A_had` with that matrix's `suh`, grid sync, the inner GEMM in 16-row steps with a sync after each, output transform in place with that matrix's `svh` and scale `0.088388347648f` times `B_weights[i]` when weights are given, then a sync. Correct. |
| Advance | `A` and `A_had` advance by `size_m * size_k` only when `bszm_in > 1`; `C` by `size_m * size_n` only when `bszm_out > 1`. Correct. |
| Transforms | Always performed (no null test on the scale lists, unlike `exl3_gemm_kernel`). `had_hf_r_128_inner` converts with `__floats2half2_rn` and then applies the post-scale with `__hmul2`. Correct. |
| Tables | Sixteen new arrays (eight bit widths, two output types), each a null entry and the four existing shapes; shapes 3 and 4 are `16, 32, 256, 4, 3` and `16, 16, 512, 4, 3`. Correct. |
| Dispatch | `select_exl3_mgemm_kernel` is `select_exl3_gemm_kernel` with the new tables and message; `select_gemm_shape` is untouched; the block cap is tiles divided by 12; `SMEM_MAX` is `90 * 1024`. Correct. |
| Single-GEMM edits | A pair of braces removed around the input-transform loop body; the sync in the row loop moved below the pointer updates. Correct. |
| Execution | Recorded output: 0.08838834764831843; the four leading-dimension cases as described; nine Boolean comparisons false. Matches the prose. |
| Finding `multi-gemm-leading-dimension-validation` | Correct. The only relation checked is `indices.size(1) == C.size(0)`. With leading dimensions 2 and 1 and indices of shape (1, 1), the loop runs twice and reads `B_indices[1]`. With 2 and 3 and indices (1, 3), the third iteration reads a third input matrix that does not exist. Suspected is right. |
| Finding `inherited-boolean-shape-threshold` | Correct, and correctly tied to the existing identity `exllamav3-boolean-dimension-threshold`. The line is unchanged and has one more caller. |

## Reviewer-only notes (never to a teacher)

All by source reading; nothing was built.

- **The wrapper validates much less than the finding says.** Also unchecked: the dtype of `indices` (read as 64-bit)
  and of `weights` (read as half); the shape of `weights`; `A_had` entirely (dtype, shape, device); each index
  against the length of `B`; `size_k` and `size_n` against anything, since the matrices are bare addresses. `num_B`
  is assigned and never used, and only the first row of `indices` is read. One record for the wrapper's missing
  validation would cover these; the finding as drafted is the sharpest case and is enough.
- **In-place scratch.** The copied comment says `A_had` "may be reference to A", and the benchmark does pass the
  same tensor for both to `exl3_gemm`. In the multi-matrix kernel with one shared input (`bszm_in == 1`) that would
  transform the already transformed input again for every matrix after the first.
- **My 123 finding reaches the new path.** `exl3_mgemm` has no divisibility check either, and with a forced shape
  index neither wrapper checks compatibility.
- **Block cap can reach zero.** `size_k / tilesize_k * size_n / tilesize_n / 12` is 0 when there are fewer than
  twelve tiles, and `MIN` then sets the cooperative grid to zero blocks. The same lines are in the single-matrix
  selector before this commit; I have not traced where they came from. Only very small matrices are affected.

## Not verified

- Any compilation or execution.
- The inner kernel (`exl3_gemm_inner.cuh`) beyond the constants named above; it is unchanged by this commit.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: `multi-gemm-leading-dimension-validation` approved as drafted, introduced at `b73d0739`.
2. Ledger: add `b73d0739` to the affected revisions of `exllamav3-boolean-dimension-threshold` and of
   `exllamav3-gemm-selector-divisibility`; no new record for either.
3. The earlier ledger revisions owed are still owed.

## Next

1. Record this approval.
2. Continue the walk at commit 134.
