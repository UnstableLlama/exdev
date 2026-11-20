# Verdict: commit-000344-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (18:02 UTC). Run: `.teacher/runs/commit-000344-001`. Packet: `.teacher/retrieval/000344-001`.
Upstream `c8ed45c6152fd6050a2a3f2f9035120fac35cb94` "Ernie4_5_MoeForCausalLM: Fix e_score_correction_bias key name (not used)".

## Decision

**Approved for ancestor retrieval only.** Canonical and training remain false. The entry finds what the one-line title hides: the new
name matches ExLlamaV3's own exports, but Baidu's sampled PT checkpoints use the old name, so the tensor is no longer picked up from them.

## What I checked myself

- Mechanical: request hashes 0 bad; `impl 47`; evidence 72 calls, 0 bad, 0 uncited; final equals annotation; 4,732 blobs,
  0 bad; 72 calls replay with 5 mismatches. No repair turn.
- Replay: I looked at all 5 mismatches. 4 are the `ancestor_read` calls of this sparse packet. The fifth is a refused `evidence_index` call
  (`Invalid max_bytes`), the same refusal in both runs, which the replay script reports as an exception rather than as the recorded error.
- Run-ahead: the packet lacks the 343 entry. The changed paths do not overlap, and it did not matter.
- Source: the exporter always writes `gate.e_score_correction_bias`, and the shared default is that name. `load` makes one exact lookup
  with `optional = True`. Ernie leaves `router_type` at `std`, and `routing_std` does not use the tensor; `routing_ds3` and `routing_dots` do.
- Overlay: `set_new_tensors` lays the converted tensors over the original file map, so conversion can still fall back by exact key.
- Pinned evidence, read from the replayed tool results: all eleven Baidu configs match the entry on architecture, hidden size, layers,
  dense prefix, experts, `moe_k`, expert width, shared experts and query heads, and none has `head_dim` or `moe_gate_act`. Headers: 21B PT
  samples hold the old name as BF16 `[1,64]`, 300B PT samples as F32 `[1,64]`, `gate.weight` is `[64,hidden]`, and no sampled header holds
  the new name. The 21B Base-Paddle sample has `gate.weight` and `gate.weight_1` at `[2560,64]` under an `ernie` prefix. The other Paddle samples
  show the fused and `quant_weight` names described. The entry correctly limits this to sampled shards.
- Carried findings: all-expert routing returns 64 indices against 6 or 8 output slots, and the fused branch returns a view of `cfg.out_d`
  without `to2`. Both as stated. The `default_chat_prompt` statement is also right.
- Discussions: all six titles match.
- Ledger, 343 records accepted: `cleanupper-bound-finalizer-retains-owner` r001 and `cleanupper-callback-error-skips-remaining-cleanup`
  r001, suspected, introduced at `6565dee4`, matching my 343 runs, not training-eligible.

## Requested next

File the 344 ledger work with the next request: the new old-name preservation record, and persistence for `all-expert-fused-shape` and
`fused-output-dtype-override`.

## Must fix before canonical

Cut the Source Notes paragraph on #26, #33, #34, #42, #52 and #53. It only rules them out.
