# Verdict: commit-000172-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000172-001`
Packet: `.teacher/retrieval/000172-001`
Upstream: `07ffea7f89c5a701130e48fd0aeaefe52a660210` "compare_q.py: Fix llama.cpp bpw measurement for MoE models"
Request: `reviews/requests/commit-000172-001.md` (sha256 `a9ff856a1589d41048965045764b3629209727930a7d0ae536da1808b67daadf`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

The description of the change is correct, the recorded execution is a faithful transcription of the old and new
loops, and both findings are true as stated and correctly kept at "suspected". One subordinate sentence is
inaccurate in effect (see Must fix before canonical use); it does not change either finding.

Ledger revisions `exllamav3-compare-q-no-reference-finalization--r002` and
`exllamav3-compare-q-cache-clear-argument-mismatch--r002` are **accepted**.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 171 strict-ancestor entries; 2,636 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions differ from 171/001's only by the fourteen added lines of guidance 7 (three paragraphs). First walk run under guidance 7. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Twelve open rows at 2025-05-17T22:19:59Z; my query agrees. No closed row qualifies. |
| The change | The seven-suffix projection whitelist is removed; any other name ending in `.weight` is now counted through an `elif` after the head test; `get_storage_info` is called before `Llama(...)` instead of after. Return tuple unchanged. Correct. |
| Consumers | `load_llamacpp` is the only caller of this helper; `compare_q.test_ppl` takes the three values, converts bits to GiB and stores `layer_bpw`, `head_bpw`, `vram_gb`. Correct. |
| Ancestor entry | The initial entry's usage-evaluation chapter says what the draft attributes to it: projection names, token-embedding fallback for a tied head, calculated storage rather than measured allocation. Correct. |
| Execution | Recorded output `(8.0, 16.0, 2400.0)`, `(5.333…, 16.0, 3200.0)`, and `(8.0, 16.0, 4800.0)` with the head first. Matches the prose; labelled synthetic. |
| Finding: embedding order | Traced independently. If `output.weight` comes first, `token_embd.weight` fails the head test and falls into the new `elif`, so it is counted as a decoder weight; in the other order it is counted nowhere. The old code never counted it. True. Whether any real GGUF has that order is not established, as the draft says. |
| Finding: cached accounting | `disk_lru_cache` keys on the JSON of the arguments only, under the unchanged name `lcpp_get_storage_info`; a hit returns the stored tuple. True. |

## Not verified

- Tensor order and tensor names in real GGUF files, including MoE files; no GGUF was opened by the teacher or by me.
- Why the storage call moved ahead of model construction.

## Must fix before canonical use

1. "The comparison CLI clears only test_ppl entries" overstates what `--clear_cache` does. At this commit it still
   calls `disk_lru_cache_clear("test_ppl", test_data_spec, spec)` while the cached call takes three arguments, so
   the key does not match and nothing is cleared (the recorded 165 finding, carried by 171). The point the
   sentence supports, that the storage cache is not cleared, stands.
2. The cached-accounting finding names only the `lcpp_get_storage_info` cache. A cached `test_ppl` result already
   holds `layer_bpw`, `head_bpw` and `vram_gb` and returns without calling the loader at all, so for a model that
   was measured before this commit that is the first cache that keeps the old numbers.
3. The entry does not carry the two 165 findings in `eval/compare_q.py`, which it read in full. Both are unchanged
   at this commit.

## Follow-ups

1. Ledger: add `07ffea7f` as an affected revision of both 165 records (file unchanged at this commit).
2. Ledger identities for this entry's two findings may be filed as suspected, source-only, with the limits the
   draft states.
3. The remaining older ledger revisions and the discussion-history cache are still owed; neither blocks.

## Next

1. Record this approval with `--approve`.
2. Proceed to 173.
