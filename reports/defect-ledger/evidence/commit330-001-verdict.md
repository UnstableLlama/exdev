# Verdict: commit-000330-001 (teacher gpt-6.2-sol, guidance 12, unassisted; ran ahead of 329)

Reviewer: Fable. Date: 2026-11-18 (06:31 UTC). Upstream `3279fe18` "Attn: Option to add projection modules as arguments".
Run: `.teacher/runs/commit-000330-001`. Packet: `.teacher/retrieval/000330-001`.

## What I checked myself

- Request hashes 0 bad. `check.py`: impl 46 bad [], evidence 58 calls 58 bad [] uncited [], final==annotation
  True, anc 327 entries 327 True, blobs 4606 bad 0. Replay 58, mismatch 0. No repair.
- Run-ahead: 329 is not an ancestor of this commit (it is on the other side of the topological order), so the
  packet is complete for its own ancestry. Nothing to judge.
- Diff read in full (three optional projection arguments; the constructor now branches on each key).
- Central claim confirmed in source at the sha: `kv_proj` appears only in the constructor (attn.py 153,
  195-197). `Attention.load` (253-260), `project_qkv` (314) and both block allocators (transformer.py 95, 163)
  still read `k_proj`, which the new branch never sets. The combined K/V option is accepted and then unusable.
- Second finding confirmed: `key_q` defaults to `None` (141), the old code built the query Linear regardless and
  passed it the fused key; the new code asserts `q_proj` instead (180 onward).
- Inherited findings were re-checked against this commit, not repeated: the tensor-truth dispatch is correctly
  reported as already fixed (`q_norm_tensor is None`, lines 370, 416, 472), the allocator and RoPE findings as
  unchanged. The allocator one was actually run against the parent implementation.
- The entry made the central check itself, and separated the new argument from the two existing fusion
  mechanisms it could be confused with.
- 329 ledger `non-cuda-release-asset-name-collision--r001`: suspected, training false, introduction `5cada8cd`. Accepted.

## Must fix before canonical

- Four Source Notes paragraphs on unrelated issues; cut to one sentence.

## Decision

Approved for ancestor retrieval only. Canonical and training remain false.
