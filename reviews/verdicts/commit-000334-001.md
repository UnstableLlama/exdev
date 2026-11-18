# Verdict: commit-000334-001 (teacher gpt-6.2-sol, unassisted; ran ahead of 333)

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (07:31 UTC). Upstream `dd053a20` "TP: Auto layer split logic".
Run: `.teacher/runs/commit-000334-001`. Packet: `.teacher/retrieval/000334-001`.

## What I checked myself

- Request hashes 0 bad. `check.py`: impl 46 bad [], evidence 97 calls 97 bad [] uncited [], final==annotation
  True, blobs 4625 bad 0. anc 329 entries 328 False and replay 97, mismatch 6 = the six ancestor reads: sparse, as
  disclosed ("Ran ahead of: 333").
- Run-ahead judged: 333 is the first parent and its entry was missing. The two commits change different files,
  and the entry took the flag and the loader stub from source. The missing entry did not matter.
- All 16 changed files read, with `tp_split.py` and `ratio_split` in full. Central claim confirmed: the commit adds
  estimators and a planner and nothing loads through them. In the extracted tree, `make_tp_allocation` is called
  only by `Module` recursion and by `BlockSparseMLP` for shared experts; `TPAllocator`, `initial_split` and
  `compile_tp_plan` have no caller. An attribute scan found every field the estimators read assigned in its class.
- Planner description confirmed line by line: accumulated storage against peak overhead, clipping, top-k device
  mask, largest-remainder split, integer proration, token multiplier on split overhead only (final component uses
  `output_num_tokens`), half-open ranges including empty ones, and `print_split` labelling GiB as "GB".
- Findings worked through by hand and all hold as suspected:
  budgets `[4, 4]` with a 5-byte replica give split `[1, 0]` and estimate `[5, 5]`; zero room and zero channels both
  reach a zero division; `CacheLayer_quant.overhead_size` covers the full cache yet is multiplied by query tokens;
  a DeciLM block with both `no_op` settings registers no children and hits the new assertion, while `allocate_q`
  returns early; `k_proj` is never assigned when `key_k` is falsy (my AST count agrees: 19 `Attention` calls, all
  named, none injected).
- Cache arithmetic reproduced: 4,194,304 FP16 bytes, and 524,288 + 786,432 + 131,072 = 1,441,792 quantized bytes.
- Inherited findings re-checked at this commit: `cache.py:137` still formats `{model_num_layers()}` on an int;
  `q_cache_kernels.cuh:43-46` still rounds the `1e-10` floor through half before `v /= s`.
- Other claims confirmed: my AST scan finds `out_dtype = None` on every concrete `forward` under `modules`, with
  `torch.half` only on the abstract method; both cache classes implement the new abstract methods; `Conv` is first
  in both vision module lists.
- Discussion claims sampled against the recorded fetches (#8, #11, #38, #43, #50, #54, #55, #58, #61): as described.
- The entry made the central check itself and states the limits of its arithmetic.
- 333 ledger: `tensor-parallel-flag-selects-stub`, `legacy-model-init-namespace` and `duplicate-tensor-p-keyword`,
  all r001, suspected, no fixes, training policy not applied, introduction `0460dda4`. Accepted.

## Must fix before canonical

- Three Source Notes paragraphs list discussions the entry itself says do not bear on the planner; keep at most
  #61, #50 and #54 as context.
- Not covered: `top_k_mask_` asserts `k <= len(lst)`, so a device limit above the device count fails. Add it to the
  planner's limits when the entry is next revised.
- Link the 333 entry once visible.

## Decision

Approved for ancestor retrieval only. Canonical and training remain false.
