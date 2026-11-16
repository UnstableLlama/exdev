# Verdict: commit-000191-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000191-001`
Packet: `.teacher/retrieval/000191-001`
Upstream: `460e201cc332ff93a4d65d7b1ca1f897ad372685` "Add batched translation example"
Request: `reviews/requests/commit-000191-001.md` (sha256 `26ea77bab0b75cdb3f4834acfb30d748fdd38c06d33715f735513146fd9bc013`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and both findings are true as stated.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 19 of 19 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 190 strict-ancestor entries; 2,835 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 19 of 19 recorded tool calls identical, including the three `run` calls. |
| Unassisted | Standing instructions byte-identical to 190/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-25T13:03:19Z; my query agrees. No closed row qualifies. The two open discussions were read in their first 16,000 bytes only, and the entry says "openings". |
| The file | One new script: a disk-cached dataset loader keeping stripped passages of at least 125 characters; one chat-templated request per passage with `#BEGIN#` / `#END#` tags and `/no_think`; one job per passage with the passage index as identifier; a loop over `generator.iterate()` that stores `full_completion` on EOS and prints running rates. Correct. |
| Defaults | `model_init.add_args` accepts `default_cache_size` at this commit; 65,536 is the cache size in tokens; the generator's own defaults are 256 concurrent sequences and 2,048-token prefill chunks. Correct. |
| Finding: prefill counted | `num_tokens` grows by the number of distinct identifiers in each result batch. `Job.prefill` appends a result with stage `prefill`, `eos` false and the job's identifier, so a job still prefilling adds one to the "output tokens" count. True; affects the printed rate only. |
| Finding: empty dataset | `avg_len` divides by `len(in_data)` before the model is loaded. True; the default dataset is not empty, as the trigger implies. |
| Execution | Two scalar transcriptions; the three `run` calls also read parent-tree files, which the request discloses. |

## Not verified

- Any dataset download, tokenisation or generation; the printed rates.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: identities for the two findings may be filed as suspected, introduced at `460e201c`. Earlier owed
   items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 192.
