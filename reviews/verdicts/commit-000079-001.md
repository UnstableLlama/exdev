# Verdict: commit-000079-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000079-001`
Packet: `.teacher/retrieval/000079-001`
Upstream: `8fa88a230b2c6d241ee2aabc7259f5d458d0e0f2` "Switch to function pointer tables for kernel launches, mitigate template issues on older of VC++ older than 17.13"
Request: `reviews/requests/commit-000079-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The dispatch change is described correctly, the compiler claim is attributed to the
author, and the entry found that direct indexing removes the old dispatch's harmless no-match behaviour. Its finding is
narrower than the code warrants; see "Must fix".

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 14 of 14 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 78 strict-ancestor entries; 1,145 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 14 of 14 recorded tool calls identical, including the `run` call. |
| Diff read in full | The upstream diff is 15,699 bytes; the single `git_show` call asked for 17,000 from offset 0. |
| Unassisted | Standing instructions byte-identical to 78/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 19, 20. Matches the eight open rows. |
| Table claims | Four eight-entry tables (`pack_trellis`, `unpack_trellis`, `quantize_tiles`, `reconstruct`) listed 1 to 8 and indexed `K - 1`. Two seven-entry contiguous cache tables listed 2 to 8 and indexed `bits - 2`. Two 7 x 7 paged tables whose rows are the first template argument, indexed `[k_bits - 2][v_bits - 2]`. Correct. |
| Selector equivalence | I compared old and new by hand, not by the teacher's transcription. The old paged dispatch tested `k_bits == i && v_bits == j` and launched `kernel<i, j>`; the new one launches the `<k_bits, v_bits>` entry. Same kernel for every pair. The single-index tables are in ascending order, so `K - 1` and `bits - 2` select the same specialisation as the old equality tests. Launch arguments are unchanged in all eight sites. |
| Range checks | Paged quantise and dequantise gain a `TORCH_CHECK` for 2 to 8 on both bit counts. The contiguous wrappers already had one; only its message changes. Correct as the Impact section says. |
| Error checks | `cuda_check(cudaPeekAtLastError())` is added after `pack_trellis`, `unpack_trellis`, `pack_signs` and `reconstruct`. Not after `quantize_tiles`. The draft's list is exactly right. |
| `util.h` | `static_for_pack` stays; a commented example table and the VC++ note are added. Correct. |
| Finding | `unchecked-pack-bitrate`: correct. `pack_trellis` and `unpack_trellis` check only `packed.size(2) == 256 * K / 16`, which K = 9 satisfies with 144, then index entry 8 of an eight-entry array. Before this commit an unmatched K launched nothing. Suspected is the right status. |

## Not verified

- Any compilation or launch. Nobody ran it; the entry says so.
- The compiler-version claim. It is the author's, and labelled so.

## Must fix before canonical use

Reviewer-only. None of this goes to a teacher.

1. The finding names two of the four sites. `reconstruct` and `quantize_tiles` index their tables with `K - 1` in the same
   way and have no range check on K either (`reconstruct` checks only the packed width; `quantize_tiles` derives
   `edges = 65536 >> K` and checks tensor shapes against it). `reconstruct` is the one on the model-loading path:
   `exllamav3/modules/quant/exl3.py` calls `ext.reconstruct(w, self.trellis, self.K)`. A canonical entry should state
   the finding for all four, and say where `self.K` comes from.
2. The finding gives K = 9 as the trigger. K = 0 or negative indexes before the array in the same way.

## Follow-ups

- When this finding goes to the defect ledger, record it as one defect covering the four `K - 1` sites, introduced at
  this commit, with this run as the observation for two of them and this verdict as the pointer to the other two.

## Next

1. Record this approval.
2. Continue the walk at commit 80.
