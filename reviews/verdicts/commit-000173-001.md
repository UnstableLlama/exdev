# Verdict: commit-000173-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000173-001`
Packet: `.teacher/retrieval/000173-001`
Upstream: `e1d2fa11d6573ea1aeaddacffc028e08a83f91b1` "compare_q.py: Add -mask arg"
Request: `reviews/requests/commit-000173-001.md` (sha256 `cec572c47141f5ec06c93c06956cf96dc35786bf3a1f1ac12e5582e9a9760c8e`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry read 165's entry, recognised that the moved clearing loop now passes
the third argument, and said correctly that this repairs the recorded key mismatch while the no-reference
division remains. The new finding is true as stated and correctly kept at "suspected".

Ledger candidates **accepted**: `exllamav3-compare-q-no-reference-finalization--r003`,
`exllamav3-compare-q-cache-clear-argument-mismatch--r003`, `exllamav3-llamacpp-embedding-order--r001`,
`exllamav3-llamacpp-cached-accounting--r001`.

The fix attribution is **confirmed**: `e1d2fa11` fixes `exllamav3-compare-q-cache-clear-argument-mismatch`.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 172 strict-ancestor entries; 2,644 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical, including the `run` and `web_fetch` calls. |
| Unassisted | Standing instructions byte-identical to 172/001's. Guidance 7. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Twelve open rows at 2025-05-18T08:58:14Z; my query agrees. One closed row by terms (PR 30), selected, fetched and said to be unrelated. Correct. |
| The filter | Applied after the reference spec is moved first; `split(";")`, upper-cased substring test, any alternative; no trimming, no regular expressions; skipped when the option is absent or empty. An empty alternative matches every label. Correct. |
| Cache clearing | The loop moved below reference discovery and the filter, and now passes `logits_file`, so its arguments equal the `test_ppl` call's and the keys match, including when `logits_file` is `None`. Only retained specs are cleared. Correct; this fixes the 165 mismatch. |
| Execution | Recorded output matches the prose: all three labels for `exl3;`, two for `exl3;exl2`, none for ` exl3`; old key differs, new key equal; zero-over-zero raises. |
| Finding: filtered reference | Traced independently. `logits_file` is computed before the filter and kept; a retained spec without `out_logits` reaches `load_tensor(logits_file)` after the model is loaded. If the producer was filtered out and the file was never written, that read fails. True, with the limits the draft states. |
| Inherited finding | `kl_div = kl_div_sum_ab / kl_div_count` is still unconditional and `collect_logits` is still set only inside `if logits_file:`. Unchanged. Correct. |
| Callers | `main` is the only caller of `test_ppl`; nothing imports `compare_q`. Correct. |

## Not verified

- `load_tensor`'s exact failure on a missing file, and any real evaluation or shelve behaviour.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: record `e1d2fa11` as the fix of the cache-clear record, and add it as an affected revision of the
   no-reference record. A ledger identity for the filtered-reference finding may be filed as suspected.
2. The remaining older ledger revisions and the discussion-history cache are still owed; neither blocks.

## Next

1. Record this approval with `--approve`.
2. Proceed to 174.
