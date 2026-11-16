# Verdict: commit-000174-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000174-001`
Packet: `.teacher/retrieval/000174-001`
Upstream: `d860f8e1e106a45536603cd8069fc9ef43105fd9` "Linear: Load scaled FP8 weights"
Request: `reviews/requests/commit-000174-001.md` (sha256 `1ef9c1d6fcdecf974c902d0f583a808d090b13c15df2a88a3c4f6fcc9d108899`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and all three findings are true as stated. The entry does not take the commit
title at its word: it says the change adds block scaling to the ordinary loading path and does not establish
complete FP8 support, which is what the source shows.

Ledger candidates **accepted**: `exllamav3-compare-q-no-reference-finalization--r004`,
`exllamav3-compare-q-cache-clear-argument-mismatch--r004` (fix `e1d2fa11` recorded),
`exllamav3-compare-q-filtered-reference-dependency--r001`.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 26 of 26 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 173 strict-ancestor entries; 2,655 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 26 of 26 recorded tool calls identical, including the `run` call and ten `web_fetch` calls. |
| Unassisted | Standing instructions byte-identical to 173/001's. Guidance 7. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Twelve open rows at 2025-05-18T14:02:48Z; my query agrees. Five closed rows, four by path alone, all selected; the draft calls every relation an inference from shared paths. Correct. |
| The change | New `apply_fp8_scales_`: both tensors two-dimensional, each weight dimension exactly 128 times the scale's, a four-dimensional view multiplied in place by the scale, return value unused by the caller. `load_fp16` loads an optional `<key>.weight_scale_inv` (no transpose, no padding) and applies it before `LinearFP16` is built. The weight and bias calls are the old ones rewritten on one line each; device and padding are unchanged. Correct. |
| Unchanged paths | EXL3 is still tried first for both keys; the fused-weight branch loads no scale. Correct. |
| Ancestor entries | The sliced-loading entry (`48747ba0`) and the initial modules chapter say what the draft attributes to them. Correct. |
| Execution | Recorded output matches the prose: 256×384 accepted and its transpose rejected for a 2×3 grid; 32,768 of 65,536 elements mismatched; the block view addresses equal the matrix addresses. Integer arithmetic only, as labelled. |
| Finding: FP8 dtype | `get_tensor` calls `convert_dtype` before anything else for a file-backed tensor; it knows `I32`, `I16`, `F16`, `BF16`, `F32` and raises `ValueError` otherwise. A weight stored with an 8-bit float dtype cannot reach the new code. True. |
| Finding: deferred read | Traced independently. With `mt_fread` and deferred mode, `get_tensor` returns an unfilled destination and queues the read; `apply_fp8_scales_` multiplies the unfilled tensors; `end_deferred_load` then writes the file's weight into the destination. The scaling is lost. `Linear.can_defer_load` is false only when sliced, and `Model._load_single` and `_load_autosplit` defer whenever the module allows it. True. |
| Finding: orientation | The weight is transposed on load and the scale is not, so a scale grid laid out like the stored weight fails the assertion when rectangular and is applied to the wrong blocks when square. True as a conditional; the draft says no file establishes the layout. |

## Not verified

- Any real checkpoint that carries `weight_scale_inv`: its weight dtype, its scale layout and whether its
  dimensions are multiples of 128. Neither the teacher nor I opened one.
- Rounding and overflow of the product in half precision.

## Must fix before canonical use

1. The deferred-read finding should say that this is the default path, not a special configuration:
   `SafetensorsCollection` falls back to `mt_fread` when no load method is given, and an unsliced `Linear` permits
   deferral. On default settings the scaling is lost for every file-backed, unsliced ordinary linear.
2. `exllamav3/models/model.py` and `eval/model_diff.py` were read in part only; the request says so. The parts
   the findings rely on were within the bytes read.

## Follow-ups

1. Ledger identities for the three findings may be filed as suspected, source-only, with the limits the draft
   states. Keep the orientation record conditional.
2. The remaining older ledger revisions and the discussion-history cache are still owed; neither blocks.

## Next

1. Record this approval with `--approve`.
2. Proceed to 175.
