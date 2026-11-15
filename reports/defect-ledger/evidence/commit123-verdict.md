# Verdict: commit-000123-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000123-001`
Packet: `.teacher/retrieval/000123-001`
Upstream: `5d470a29780927c1c8c874609597823f210ae3b9` "Refactor GEMM kernel for cooperative launch and fusions, fuse with input/output Had transforms, retune launch configs, split kernel compile into units"
Request: `reviews/requests/commit-000123-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

The largest change since 71: thirty files, a cooperative kernel, four new tile shapes, a new selector. The entry
describes the mechanisms accurately and its finding (`boolean-dimension-threshold`) is correct.

**Coverage.** The request is right to flag it: 12 of 30 sections were read. I read the other 18. Fourteen are the
compile units for bitrates 2 to 8, which are the one-bit unit with the digit changed (verified by substitution; the
only other difference is trailing blank lines in three files). The remaining four are `exl3_devctx.cuh` (the class
declaration whose `.cu` was read), `exl3_gemm.cuh` (the signature whose `.cu` was read), `util.h` (one debug macro)
and the one-bit unit's two-line header. Nothing of substance was skipped, and the entry says plainly what it did not
inspect. I accept the limitation; this is not a thin entry and gets no coverage request.

It does miss one defect in the new selector, below, which is required before canonical use.

## Artifacts reviewed (sha256)

All twelve hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 22 of 22 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review with `validation_incomplete`; 41 of 41 implementation hashes; exactly 122 strict-ancestor entries; 1,784 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 22 of 22 recorded tool calls identical, including the `run` call and the ancestor search. |
| Unassisted | Standing instructions byte-identical to 122/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 25, 26, 27, 28, 29. Matches the twelve open rows. |
| Architecture trigger | Does not fire. |
| Python caller | `LinearEXL3.forward`: the direct path is now one call, `exl3_gemm(x, trellis, y, suh, xh, svh, -1)`; the reconstruction path keeps Hadamard, `hgemm`, Hadamard; the switch is still `x.shape[0] > 32`. Correct. |
| Wrapper | Optional `suh`, `A_had`, `svh`; `suh` needs `A_had` of `A`'s shape; `suh` is checked against k and `svh` against n, while the comment says `k//16` and `n//16`; half input, int16 weights, half or float output. Correct. |
| Outer kernel | Input: one warp per 128-element segment, pre-scale then normalized Hadamard into `A_had`, grid sync, `A = A_had`. GEMM: the inner routine once per 16 rows with a grid sync after each. Output: in-place Hadamard then `svh`, float or half by output type. Correct. |
| Hadamard helpers | Four values per lane, five XOR-shuffle stages over 32 lanes; the half path multiplies scales in half and rounds before the post-scale; the float path stays in float; both standalone kernels now call the helpers. Inside the GEMM kernel the grid is one-dimensional, so the helpers' `blockIdx.y` term is zero and the caller's pointer offset supplies the position. Correct. |
| Inner routine | A move of the parent's kernel body: against the parent file the differences are the renamed thread constant, the removed `sv` parameter and the deleted, already disabled output-Hadamard block. Correct ("extracted ... retains"). |
| Shapes | Four tuples, all M = 16: (16,128), (32,128), (32,256), (16,512); stages 3/1 for shape 1 and 4/2 for the rest; block size `256 * K / 16`. The parent had six. Correct. |
| Selector | Depends on device tier, bits, k and n; `size_m` is unused; block count capped by `size_k / tile_k * size_n / tile_n / 12`. Correct. |
| Launch | `cudaLaunchCooperativeKernel`, one-dimensional grid, `SMEM_MAX` of 90 KiB. Correct. |
| Compile units | Eight units, each with a float32 and a half table of the four shapes; the dispatcher switches on bits. Correct for all eight (the entry claims only the first). |
| Benchmark | Supplies scales, passes `a[i]` as `A_had`, asks `exl3_gemm_shape_compat` for compatibility, bitrate 8 to 1, runs 200 to 50. Correct. |
| Execution | Recorded output matches: 0.08838834764831843; 0.9999999999927947; the comparison false for every modelled case. |
| Ancestor note | Reads the entry for `e9a3b6a9` (position 71), the commit that disabled the in-kernel output transform. Correct. |
| Finding `boolean-dimension-threshold` | Correct. `exl3_kernel_map.cu` line 61: `(size_k && bits >= 3) > 8192 ? 3 : 2`. The left side is 0 or 1, so the branch returns 2. Reached on Hopper and Blackwell for `bits != 8`, `size_n <= 4096`, when line 60 does not return 1. Suspected is right; the intended rule is unknown. |

One wording point: "Device SM counts, architecture tiers and lock allocation move into DevCtx" reads as if `DevCtx` were
new. The class existed at the parent inside `exl3_gemm.cu`; it moves to its own file.

## Reviewer-only finding (never to a teacher)

**The selector can choose a tile wider than the layer divides, and nothing stops it any more.** Source inspection
only; nothing was executed.

- At the parent, `launch<...>` refused a shape when `size_k % TILESIZE_K != 0` or `size_n % TILESIZE_N != 0`, and the
  old selector returned the 256-wide shape only as `mod_256 ? 2 : 3`.
- At the task, `select_gemm_shape` returns shape 3 (N tile 256) with no `mod_256` test in four places: old/Ampere with
  `bits <= 4` and `size_n > 2048`; old/Ampere with `bits >= 5`, `size_n <= 4096` and `size_k > 8192`; Ada with
  `bits <= 4` unless `size_n <= 4096 && size_k <= 12288`; Hopper/Blackwell with `bits == 8`, `size_n <= 8192` and
  `size_k > 32768`. The divisibility tests moved into `exl3_gemm_shape_compat`, which only the benchmark calls.
  `exl3_gemm` launches whatever was selected.
- The inner routine takes `size_n / TILESIZE_N` tiles, rounded down. For a width that is an odd multiple of 128 the
  last 128 output columns are never written. `C` comes from `torch.empty`, and the fused output Hadamard then runs
  over those columns too. The result is wrong values, not an error.
- Reach: `Linear` pads output widths to multiples of 128, so the condition is a padded width that is an odd multiple
  of 128 in one of those branches, on the direct path (32 rows or fewer). The clearest case is an output head: for
  example a vocabulary of 151,936 is 1187 x 128. The head's default is 6 bits, which avoids the first and third
  branches; `-hb 4` or lower does not. From memory that is the Qwen vocabulary size; I did not confirm it in the
  bundle.

Smaller: the `num_sms` cap can reach zero for a very small layer (fewer than twelve tiles). The same expression was at
the parent.

## Not verified

- Any compilation or execution, including whether the cooperative grid is always co-resident.
- The Qwen vocabulary size mentioned above.

## Must fix before canonical use

1. A canonical entry must cover the selector's unguarded shape-3 returns together with the removed launch-time
   divisibility check.
2. Say that `DevCtx` moves to its own file, not that state moves into it.

## Follow-ups

1. Ledger: file one reviewer-origin candidate from the finding above (suspected, source inspection, introduced at
   `5d470a29`), excluded from historical context and training. Send it with the next request.
2. Ledger: `boolean-dimension-threshold` is approved as drafted.

## Next

1. Record this approval.
2. Continue the walk at commit 124.
