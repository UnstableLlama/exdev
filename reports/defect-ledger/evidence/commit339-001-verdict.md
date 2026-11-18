# Verdict: commit-000339-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (17:10 UTC). Run: `.teacher/runs/commit-000339-001`. Packet: `.teacher/retrieval/000339-001`.
Upstream `e14fa3cf22ff9c4203736690522c7baaf17dd57b` "GEMM: Fix kernel mapping for some odd tensor shapes".

## Decision

**Approved for ancestor retrieval only.** Canonical and training remain false.

## What I checked myself

- Mechanical: request hashes 0 bad; `impl 47`; evidence 41 calls, 0 bad, 0 uncited; final equals annotation; 4,698 blobs,
  0 bad; 41 calls replay with 10 mismatches, equal to the 10 `ancestor_read` calls of this sparse packet. No repair turn.
- Run-ahead: the packet lacks the 338 entry. No file overlaps with 338, and it did not matter.
- Central claim, independently. No C++ compiler is available here, so I translated `select_gemm_shape` mechanically from Git
  at both revisions, rather than from the teacher's hand transcription. On the teacher's 196,608 cases: 20,208 output
  widths not covered by the chosen tile at the parent, 0 at the commit. On 2,621,440 wider cases over all five tier labels:
  0 at the commit. On a one-in-seven subsample, no case was compatible before and incompatible after.
- Both worked examples reproduce: Ampere K=4096, N=2176, 4 bits goes from shape 3 to 2; Hopper K=16384, N=4096, 3 bits goes
  from shape 2 to 3. The old Boolean comparison could never select shape 3.
- Constants: tile sizes and block dimensions in `exl3_kernel_map.cuh` are as stated. `exl3_gemm_inner.cuh:60` rounds K and N tile
  counts down and M up. `select_gemm_shape` has one declaration, one definition and two six-argument calls.
- The five carried findings, rechecked at this commit:
  - Zero block cap: K=512, N=128, 2 bits, multi gives shape 2, 16 tiles, `16 / 24 = 0` with no clamp, then
    `total_sms / num_sms` in `exl3_mgemm`.
  - K tile gap: K=144 is allowed by the wrapper's `k % 16` comment, shape 2 covers 128.
  - Group sizes: indices width is checked against the output count only, while the kernel loops to the larger of the two
    and reads `B_indices[j]`.
  - Broadcast scratch: `A_had + j * size_m * size_k` advances per matrix even when `A` is reused. `yh` is sized per expert slot.
  - All-expert routing: with the flag set, routing returns `num_experts` indices, while `interm_g` has `num_experts_per_tok`
    slices, so the index-width check rejects the call.
- Ledger, 338 records accepted: `vision-input-preparation-missing` r001 and `cached-module-miss-survives-insertion` r001 are new,
  suspected, introduced at `eeaabcdc`, with no fixes, and match my 338 check. `deferred-bf16-odd-tail` r005 adds a persistence
  observation at `eeaabcdc`, with earlier observations byte-equal. None is training-eligible.

## Not established

No kernel was built or run. The entry says so. Which real tensors hit the affected widths is unknown, and the entry says that too.

## Requested next

File the 339 ledger revisions for the five carried findings with the next request.

## Must fix before canonical

The Source Notes paragraphs on issues #5 and #61 add little, since neither relates to this fix. Editorial only.
