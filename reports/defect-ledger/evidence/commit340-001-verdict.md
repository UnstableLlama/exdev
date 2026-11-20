# Verdict: commit-000340-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (17:20 UTC). Run: `.teacher/runs/commit-000340-001`. Packet: `.teacher/retrieval/000340-001`.
Upstream `ea62df9eee39fd86654971a4001cb0f846b09020` "MGEMM: Allow number of matrix indices <= bsz of output tensor".

## Decision

**Approved for ancestor retrieval only.** Canonical and training remain false. The entry rightly goes past the commit title:
the new check is looser than the title says, and it admits batches the kernel cannot serve.

## What I checked myself

- Mechanical: request hashes 0 bad; `impl 47`; evidence 33 calls, 0 bad, 0 uncited; final equals annotation; 4,704 blobs,
  0 bad; 33 calls replay with 4 mismatches, equal to the 4 `ancestor_read` calls of this sparse packet. No repair turn.
- Run-ahead: the packet lacks the 339 entry. No file overlaps with 339, its source is in the parent, and it did not matter.
- Central claim, by my own enumeration of the new check and clamps against the kernel's `MAX(bszm_in, bszm_out)` loop, for input
  and output counts 1 to 8 and index counts 0 to 16: 436 accepted cases, every one runs exactly N iterations; 84 run past the
  output and 56 read past a non-broadcast input.
- All worked cases reproduce: (1,8,4) and (8,8,4) go from rejected to four iterations; (8,1,1) goes from eight to one; (4,2,4)
  overruns the output; (2,4,3) overruns the input; (1,8,0) clamps to zero, and the wrapper still builds a zero-width grid and
  launches.
- Callers: one binding and four Python calls. `Attention.project_qkv` passes no indices, behind the 32-token limit. The three
  `BlockSparseMLP` calls pass routed indices into buffers sized by `num_experts_per_tok`, `out_d` included, so top-k sizes stand.
- Kernel: `B_indices[j]`, the input broadcast only when the effective count is one, scratch and output addressed by `j`, and the
  weighted sum into slot zero are all as the entry says.
- Carried findings, rechecked: all-expert routing is still rejected at the gate call, since N exceeds both 1 and
  `num_experts_per_tok`; broadcast scratch is unchanged; `4 * 128 / 128 / 24 = 0` still reaches `total_sms / num_sms`.
- Discussions: all seven titles match the fetched text.
- Ledger, 339 records accepted: `gemm-zero-grid-cap` r003, `multi-gemm-leading-dimension-validation` r004,
  `mgemm-broadcast-scratch-capacity` r003 and `all-expert-fused-shape` r014 each add one observation at `e14fa3cf`, with earlier
  observations byte-equal and nothing else of substance changed. `gemm-k-tile-validation-gap` r001 is new, suspected, with no
  introduction claim. None is training-eligible. The older partial fix on the zero-grid record correctly stays scoped to the
  single-GEMM path.

## Not established

No native code was built or run, so the overruns are source-level. The entry says so.

## Requested next

With the next request, file the 340 ledger work: new records for the asymmetric capacity and the empty index list, persistence
for the three carried findings, and a revision of `multi-gemm-leading-dimension-validation` saying this commit narrows it (index
position is now bounded) without closing it.

## Must fix before canonical

The two Source Notes paragraphs on issues #7, #26, #33, #34, #42, #52 and #53 say only that they are unrelated. Cut them.
