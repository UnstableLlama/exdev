# Verdict: commit-000176-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000176-001`
Packet: `.teacher/retrieval/000176-001`
Upstream: `d359bcc0d366c64fe7bed2e13446641d9f99c163` "Add MCG 3INST and MCG 1MAD (MUL1) experimental quant modes"
Request: `reviews/requests/commit-000176-001.md` (sha256 `e84ffcd0af90f67b657dce5a25149a982bc543d57f8d5fd48a8cb1419ed264b5`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, including the arithmetic, which I recomputed independently. The entry follows
the new codebooks through every layer and does not claim a speedup or a quality result. It misses one defect that
the source shows (below, reviewer finding); nothing it says is contradicted by it.

Ledger candidates **accepted**: `exllamav3-compare-q-no-reference-finalization--r005` (fix `c0a2028f`),
`exllamav3-compare-q-filtered-reference-dependency--r002`.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 48 of 48 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes (the accepted guidance-8 gate is in them); exactly 175 strict-ancestor entries; 2,670 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 48 of 48 recorded tool calls identical, including both `run` calls. |
| Unassisted | Standing instructions byte-identical to 175/001's. Guidance 7; the packet's version is 7 and the fourth paragraph is absent. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Twelve open rows at 2025-05-21T17:15:13Z; my query agrees. Five closed rows by path, all selected and described as path matches only. PR 26 is open, read in full, and its relation is labelled an inference. |
| Decoders | Mode 0 unchanged; mode 1 multiplies by the supplied value and drops the additive constant; mode 2 multiplies, sums the four bytes onto `0x6400` and applies a fused multiply-add. Correct. |
| Arithmetic (mine) | Independent recomputation: `0x1eee` is 0.00676727294921875, `0xc931` is -10.3828125, `0x6400+s` reads as `1024+s` for every sum 0 to 1020; RMS over the 65,536 states is 1.2437109245, 1.2064412350 (`0xCAF6A435`) and 1.0004000645 (`0xAD9A2EC5`). All equal the draft's figures. |
| Quantizer | Twenty-four kernel instances indexed `K - 1 + 8 * cb`; the selected decoder is used for scoring and for reconstruction of the chosen path. Correct. |
| Storage and loading | A nonzero multiplier is stored as a scalar under `mcg` or `mul1`; `Linear.load_exl3` reads both optionally, on CPU, without deferral; both `LinearEXL3(...)` call sites pass the two new arguments before `bias`. There are no other constructor calls in the tree. Correct. |
| GEMM tables | Index `shape_idx + 5 * cb`; shape 1 is now a null entry; `select_gemm_shape` returns only 0, 2, 3 or 4; the benchmark starts at 2. Correct. |
| Callers (mine) | Every Python call of `quantize_tiles`, `decode`, `reconstruct`, `exl3_gemm` and `exl3_mgemm` in the task tree passes the new arguments; the one `test_distribution` call is commented out. Correct. |
| Grouped experts | `MultiLinear` asserts equal multipliers across its members. Correct. |
| Unchanged constant | `codebook_scale = 1.24371088` is still used by `regularize` for every mode. Correct, and correctly reported without a judgement. |
| Inherited finding | `forward` swaps the two cost buffers, reads the incoming one and writes the other; `argmin_cost` reads the incoming one, which holds the previous step. Unchanged by this commit. True. |

## Reviewer finding (not in the entry; reviewer knowledge, never to a teacher)

The two-multiplier case is handled three different ways. `exl3_gemm` and `exl3_mgemm` refuse it. `quantize_tiles`
lets MUL1 win (two plain `if` statements, the second overrides). `decode`, `reconstruct` and `test_distribution`
let MCG win (`if` / `else if`). `quantize_exl3` stores both tensors when both are set. The command-line check in
`prepare` looks only at the current arguments, before the saved job is loaded, and both options are overridable
on resume; a job started with one and resumed with the other carries both into `quant_args`. Such a layer would
be encoded with one codebook and reconstructed with the other. Source reading only; nothing executed.

## Not verified

- Compilation, any kernel execution, conversion or benchmark. The added tests were read, not run.
- `exllamav3/conversion/convert_model.py` was read to byte 15,000 only by the teacher; the request says so.

## Must fix before canonical use

1. Add the two-multiplier inconsistency above, or at least stop short of implying the rejection in `prepare`
   covers every route to the quantizer.
2. Say that MUL1's tests use scale 1.0 while the library constant stays 1.24371088 for all modes; the entry
   reports the constant but not the contrast with the tests it describes.

## Follow-ups

1. Ledger: a new identity for the reviewer finding above (suspected, source-only, reviewer-originated). The
   inherited cost-buffer record gains `d359bcc0` as an affected revision. The three 174 identities are still owed.
2. The guidance-8 trial request is expected; the walk stays on 7.

## Next

1. Record this approval with `--approve`.
2. Proceed to 177.
