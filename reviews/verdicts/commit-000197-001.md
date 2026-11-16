# Verdict: commit-000197-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000197-001`
Packet: `.teacher/retrieval/000197-001`
Upstream: `9be91d644d8272db7bfd5e759084b74bc08704ae` "Generator: Periodically defragment paged cache"
Request: `reviews/requests/commit-000197-001.md` (sha256 `3c055f3dcd889c151bd1b7152e6aa791d9261bd64d9fce981bf9f9ef5c1139cc`)
Reviewed: 2026-11-16, working tree on top of `e9e83ff`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and all three findings are true as stated. Two consequences of the new
caller are missing (below); neither makes anything in the entry false.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 25 of 25 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 196 strict-ancestor entries; 2,883 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 25 of 25 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 196/002's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fifteen open rows at 2025-05-28T20:23:08Z; my query agrees. No closed row qualifies. |
| When it runs | `clear_queue` (call already present, formerly reaching the stub), `cancel` and the completed-job cleanup in the iteration, each only when the queue goes from non-empty to empty; `enable_defrag` defaults to true. Correct. |
| The gate | Skips unless `access_serial` has advanced by `max_pages` since the last attempt; the serial advances once per page assignment including reuse, so "every page touched" is stronger than the code; the attempt serial is stored before the movement threshold can return. Correct. |
| The planner | Pages indexed by hash; roots are pages with no previous hash; children sorted longest chain first; roots by ascending access serial; trimmed branches appended as further roots; chains numbered consecutively; the rest sorted by physical index and given the sorted access serials. Most common shift subtracted modulo `max_pages`; copying only when more than `max(max_pages // 10, 2)` pages move. Correct, including the remark that the wrap can split a chain. |
| Copy schedule | A cycle becomes `[-1, d0, d0, s0, s0, s1, …, s_last, -1]`: save, shift, restore. I traced it by hand for a three-cycle and agree with the exhaustive model (1! + … + 7! = 5,913). |
| The kernel | Signed int32 pairs, negative meaning the scratch page; one loop over pairs per block with `__syncthreads` after each; `block_size <= 0` on an unsigned value is the same test as before. Wrapper halves the order length. Correct. |
| Cache layers | FP16 returns K and V; quantized returns packed K, packed V and both scale tensors. Correct. |
| Visualizer | Usage is now indexed by `page_index`. Correct. |
| Tests | Rotation test converted to pairs and doubled when not full; stress script forces depth zero every third cycle, draft model off, quantized layer commented out. Correct. |
| Finding: draft cache | `PageTable.cache` is the main cache only; `defrag` moves its tensors and rewrites the shared `page_index`; draft prefill and generation pass the same block table with `draft_cache`; the partial-prefix copy in `job.py` does handle both caches. True. |
| Finding: vector boundary | 129-byte pages give two-byte blocks; block 65 begins at 130 with its end clamped to 129 and the subtraction wraps. True, and the new guard does not change it. |
| Finding: test dtype | Unchanged `dtype = torch.half`. True. |
| Execution | One standard-library model of the schedule and the unsigned subtraction; labelled as a model. |

## Reviewer findings (not in the entry; reviewer knowledge and hindsight, never to a teacher)

1. **The new caller reaches the vector-boundary case with real cache shapes.** The entry says its trigger is "not
   a demonstrated model-cache shape". The quantized layer's scale tensors are half precision with
   `token_dim // 32` values per token, so a page is `512 * (token_dim // 32)` bytes and each of the 128 blocks
   gets `4 * (token_dim // 32)` bytes. That is a multiple of 16 only when `token_dim // 32` is a multiple of
   four. Three KV heads of 64 give 24-byte blocks, five give 40: every block then copies 8 bytes that belong to
   the next block, blocks are not synchronised with each other, and the last block writes 8 bytes past the page
   (into the next page, or past the tensor or the scratch buffer). FP16 pages and the packed tensors at these
   shapes are multiples of 16. Arithmetic and source reading only; I have not established that such a model
   loads at this commit. Upstream's tip rounds the block size up to the vector width.
2. **Recursion depth equals chain length.** `measure` and `sort_seq` recurse once per page of a cached chain, so
   one cached sequence of roughly a thousand pages (about 250,000 tokens) exceeds Python's default limit of
   1,000 frames. Upstream `402ab56b` (2025-10-05) "Avoid recursive functions in defrag, should fix #78" removes
   the recursion.
3. The draft-cache finding is confirmed by hindsight: upstream's tip includes the draft cache in the tensors it
   moves.

## Not verified

- Any build, GPU execution, generation or timing; that either test passes.

## Must fix before canonical use

1. Apply the inherited vector-boundary finding to the new caller: state which cache tensors give a per-block
   length that is not a multiple of 16 (reviewer finding 1), with its limits.
2. State that the planner's two helper functions recurse to the depth of the longest cached chain.
3. Minor: the orphan pass rewrites `access_serial` and the chain trimming rewrites `children` before the
   movement threshold can return, so a skipped defragmentation still changes eviction order among orphans. The
   entry states the reassignment but not that it survives the skip.

## Follow-ups

1. Ledger: the draft-cache finding may be filed as suspected, introduced at `9be91d64`. The vector-boundary
   record from 195 gains this commit as the first library caller; do not record a fix before the walk reaches
   one. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 198.
