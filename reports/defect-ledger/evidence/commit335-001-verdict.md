# Verdict: commit-000335-001 (teacher gpt-6.2-sol, unassisted; ran ahead of 334)

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (07:51 UTC). Upstream `3be1ea10` "Merge branch 'dev' into dev_tp".
Run: `.teacher/runs/commit-000335-001`. Packet: `.teacher/retrieval/000335-001`.

## What I checked myself

- Request hashes 0 bad. `check.py`: impl 46 bad [], evidence 43 calls 43 bad [] uncited [], final==annotation
  True, blobs 4649 bad 0. anc 331 entries 330 False and replay 43, mismatch 4 = the four ancestor reads: sparse, as
  disclosed ("Ran ahead of: 334").
- Run-ahead judged: 334 is the first parent and its entry was missing. The merge's first-parent change is only
  `quant/exl3_lib/quantize.py`, which 334 did not touch. The missing entry did not matter.
- Merge shape confirmed in Git: against first parent `dd053a20` one file changes, and its added and removed lines
  are identical to second parent `69e728ef`; the merged `quantize.py` blob equals the second parent's. Against the
  second parent 17 paths differ: 334's 16 plus `model_init.py` from 333.
- Central claim confirmed at `quantize.py:834-854`: `block_trace` slices Hessian columns and the matching rows of the
  right operand on `j`, leaves the left operand whole, and so keeps cross-block terms. It is the same trace in exact
  arithmetic, and full operands still move to the device, with `E` cleared before `W` moves.
- Surrounding claims confirmed: `5e8` CPU rule (`:823`), `1e-8` floor, `-1.0` on `torch.OutOfMemoryError` (`:855-860`),
  `finalize_capture_H` normalise, damp, sign flips and input Hadamards, one direct `quantize_exl3` caller, and
  `convert_model.py:428` printing `(OoM)`.
- Inherited findings re-checked at this commit. `test_quant_fn.py:171` is a strict upper bound and all eight bounds
  are positive, so `-1.0` passes. `quantize.cu` swaps at the top of each step (`:46-48`), writes `temp_costs` (`:78`), and
  `argmin_cost` reads `temp_costs_inc` (`:95`), which holds step 254 after the first `forward(128, -1)`.
- The entry's correction of the root chapter holds: the root `g_scale_mse_gridsearch` used `(i + width) % tiles_n`,
  and the active `g_scale_gss:532` uses `(i + w) % tiles_n`.
- Discussion claims sampled against the recorded fetches (#8, #34, #42, #52, #53, #58): as described, and the entry
  is careful that the #34 chunking comment is context only.
- The entry made the central check itself.
- 334 ledger: seven records. Four new (`split-can-exceed-budget`, `zero-split-denominator`,
  `cache-scratch-scaled-by-query-tokens`, `empty-block-cannot-emit-empty-plan`): r001, suspected, no fixes, training
  policy not applied, introduction `dd053a20`. Three revisions (`combined-kv-child-not-consumed` r002,
  `zero-block-scale` r002, `cache-detach-count-diagnostic` r004): earlier observations equal, introductions and fixes
  unchanged, one new 334 observation each, status unchanged (the last stays confirmed as in r003). Accepted.

## Must fix before canonical

- Three Source Notes paragraphs (#8/#43/#58, #42/#52/#53, #26/#33/#7) cover discussions the entry itself says do not
  bear on the metric; keep the #34 note.
- Link the 334 entry once visible.

## Decision

Approved for ancestor retrieval only. Canonical and training remain false.
