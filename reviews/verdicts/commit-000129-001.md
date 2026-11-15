# Verdict: commit-000129-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000129-001`
Packet: `.teacher/retrieval/000129-001`
Upstream: `c4867edd0d31ea9fb052668874ae52fad0e91a0f` "GEMM kernel optimizations"
Request: `reviews/requests/commit-000129-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and all three findings are correct. This is the strongest entry of the session:
all fifteen diff sections read, the old and new forms of each rewritten expression compared, and two real defects
found by reading eleven changed lines carefully.

## Artifacts reviewed (sha256)

All fourteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 33 of 33 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 128 strict-ancestor entries; 1,855 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 33 of 33 recorded tool calls identical, including the `run` call and the one recorded error (the read of the missing header, which the runner refuses the same way). |
| Unassisted | Standing instructions byte-identical to 128/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Cutoff | PR 26's snapshot ends with the comment of 2025-05-07T18:59:17Z. The cutoff is 2025-05-08T20:44:26Z; the maintainer's comment three minutes later about the compiler not producing LOP3 is not in the packet or the session. The LOP3 suggestion the entry cites is in an earlier comment by the pull request's author. Labelled inference. Correct. |
| Catalog | Eleven open rows: 1, 4, 7, 10, 14, 22, 26, 27, 28, 29, 34. Correct. My routine query printed twelve because it counted issue 33; GitHub's timeline shows 33 was closed on 2025-05-07 and reopened on 2025-05-13, so it was closed at this cutoff. The catalog is right and my query was wrong. |
| Architecture trigger | Does not fire. |
| Decoders | `decode_3inst_2`: the two AND/XOR pairs are commented out and replaced by `lop3.b32` with `0x8fff8fff`, `0x3b603b60`, table `0x6a`. `decode_3inst`: a new line `x = (x & 0x8FFF8FFFu) ^ 0x3B603B60u;` is followed by the same `lop3`. The constants equal the old binary literals; `0x6a` is the table for `(a & b) ^ c`. Correct. |
| `fshift` | Old: `__funnelshift_r(b, a, shift)` below 32, else `a >> (shift - 32)`. New: `(((uint64_t)a << 32) | b) >> shift`, truncated. Same value for shifts 0 to 63. Correct. |
| Shapes | Fragment stages 1, 2, 2, 2 become 2, 3, 3, 3; tiles unchanged; a `FRAG_STAGES == 4` loop is added to the inner routine and no shape uses it. Correct. |
| Compile units | All eight use `EXL3_GEMM_KERNEL_INSTANCES(bits, fp32)`; the macro lists the same four kernels after a null entry; `EXL3_GEMM_BLOCKDIM` is 0, 256, 512, 512, 256, equal to the old `256 * K / 16`. Correct. |
| Selector | Old/Ampere above 4 bits: `size_n < 4096` (was `<=`), shape 4 needs `mod_512 && size_n * size_k > 4096 * 4096 && bits <= 6`. Ada: low-bit branch is `bits <= 3` (was 4), `size_n < 4096`. Hopper/Blackwell: first branch `bits >= 7` (was `== 8`), the shape-1 line is gone, the last two conditions lose their bit tests. Unknown bit counts now raise. Correct. |
| Benchmark, helper | K 1 to 8, m values 17 and 32 dropped, two more devices enabled; `#pragma once` on the Hadamard helper. Correct. |
| Execution | Recorded output: masks equal; 65,502 of 65,536 states differ; state 0 gives 0.76806640625 once and 1.07421875 twice; table 0x6a; 192 shift cases pass; Boolean comparison false; block sizes 256, 512, 512, 256. Matches the prose. |
| Finding `scalar-codebook-double-transform` | Correct. In `decode_3inst` the transform is applied in C++ and then again by the instruction. Applying `(x & M) ^ C` twice gives `(x & M) ^ 0x30003000`, not `(x & M) ^ C`. The scalar decoder serves `decode_pcb*` (quantization cost, tile output, `decode`, the distribution count) and one function in `exl3_dq.cuh`; the GEMM fragment decoders use `decode_3inst_2`, which is applied once. Suspected is right; nothing was built. |
| Finding `missing-gemv-header` | Correct. All eight units add `#include "../exl3_gemv_kernel.cuh"`; no file of that name is in the tree at the parent or the task. Suspected is right. |
| Finding `inherited-boolean-threshold` | Correct, and correctly tied to 123's identity: the line is unchanged, and removing the shape-1 line before it widens the cases that reach it. |

## Reviewer-only notes (never to a teacher)

- **Hindsight.** Later history has "Fix regression" (`456f14f9`) about two hours after this commit and "Fix bad
  include" (`c2b8516f`) the next evening, both touching these files. I have not read them; expect them at the next
  positions, and expect them to be the fixes for the first two findings.
- **Not the same record as the existing header defect.** The ledger's `exllamav3-missing-exl3-gemv-header` concerns
  `quant/exl3_gemv.cuh` in `bindings.cpp` at the first commit. This is a different file name in different
  translation units, introduced here.
- **My 123 finding still holds.** The unguarded returns of the 256-wide shape are all still present (old/Ampere
  `bits <= 4`; old/Ampere `size_n < 4096 && size_k > 8192`; Ada low-bit branch, now `bits <= 3`; Hopper/Blackwell
  `bits >= 7` with `size_k > 32768`), and `exl3_gemm` still launches without a divisibility check.
- `size_n * size_k` in the new shape-4 condition is `int` arithmetic and overflows at 2^31, for example 262,144 by
  8,192. Latent.

## Not verified

- Any compilation or execution.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: `scalar-codebook-double-transform` and `missing-gemv-header` approved as drafted, both introduced at
   `c4867edd`. Keep the header record separate from the first-commit one.
2. Ledger: no new record for the Boolean threshold; add `c4867edd` to the 123 identity's affected revisions, and to
   `exllamav3-gemm-selector-divisibility`.

## Next

1. Record this approval.
2. Continue the walk at commit 130.
