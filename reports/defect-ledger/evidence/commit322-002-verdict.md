# Verdict for commit-000322-002

Run: `.teacher/runs/commit-000322-002`
Packet: `.teacher/retrieval/000322-002`
Upstream: `ff21ee46edb9ba74d709257f482c809a7bd406d0` — "Transformer: Allow layers without input norms"
Reviewer: Fable, 2026-11-18 03:56 UTC. Fresh unassisted retry authorised by `commit-000322-recovery-001.md`.

## What I checked myself

- Request hashes: 0 bad. check.py: impl 45 bad [], evidence 56 calls 56 bad [] uncited [], final==annotation True,
  blobs 4511 bad 0. Replay 56, mismatch 3 = the three ancestor reads on a sparse packet (expected).
- Diff read in full (4 added lines, two `else: y = x.half()` branches in `TransformerBlock.forward`).
- Entry's central claims confirmed in source at the sha: before the patch a normless attention branch read an
  unassigned `y` and a normless MLP reused attention's `y`; the fallback casts the branch input to FP16 and
  leaves the residual `x` untouched; `Model.prefill` sets `params["prefill"]` per module and breaks at
  `last_kv_module_idx`; DeciLM (`models/decilm.py` 78-80, 112-114) drops a norm only with its branch;
  `science/kv_quant_exp.py:65` calls `module.attn_norm.forward` directly; allocators read `.ups`/`.downs`
  (transformer.py 85-90, 167-168) while plain `MLP` defines `.up`/`.down` (mlp.py 34, 43).
- The entry made the central check itself (unbound/stale `y`, data type of the fallback, residual dtype
  preserved, no in-tree builder reaches it) and backed it with an isolated before/after run whose limits it states.
- The plain-MLP allocation finding that failed validation in 322/001 now cites source reads.

## Notes (editorial, not blocking)

- Three paragraphs summarise unrelated discussions (#7, #26, #33, #34, #42, #52, #4, #48, #50, #51, #53); trim before canonical.
- Two finding locations name `ba4304a4...` (parent) for unchanged files; acceptable since the files are unchanged, but
  confirm the introduction shas when the ledger records are made.

## Decision

Approved for ancestor retrieval only. Canonical and training remain false.
