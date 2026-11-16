# Verdict: commit-000165-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000165-001`
Packet: `.teacher/retrieval/000165-001`
Upstream: `3873d40ae2734261f72aa85261ac06b6e307c1e4` "compare_q.py: Add KLD test and some other tweaks"
Request: `reviews/requests/commit-000165-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and both findings are correct. This is a strong entry: it noticed that the
ordinary perplexity-only run now divides zero by zero, and, by reading the 162 entry about the disk cache, that
`--clear_cache` no longer clears what the changed function stores. Both are real regressions in a script the
commit presents as improved.

Ledger revision `exllamav3-logits-padding-width-mismatch--r002` is **accepted**.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 21 of 21 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review, with `validation_incomplete` correctly raised for the two image sections; 44 of 44 implementation hashes; exactly 164 strict-ancestor entries; 2,565 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 21 of 21 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 164/001's. Guidance 5. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path or the tracking files. |
| Catalog | Eleven open rows at 2025-05-16T14:13:26Z; my query agrees. No closed row qualified. |
| Architecture trigger | Does not fire. |
| Sections | Nine of eleven read; the two unread are the PNG files, and the entry draws nothing from them. Right. |
| Reference selection | `main` takes the last spec with `out_logits`, makes the directory, names the file by a hash of the data spec, and moves that spec to the front. Correct, including "identifies the dataset specification rather than the reference model". |
| The KLD loop | First ten rows only; softmax of each side; both cut to the smaller vocabulary width without renormalising; `F.kl_div(log(candidate + 1e-10), reference, reduction="sum")` per position; the reference run only counts rows and so reports zero. Correct. |
| Loader and adapter | `transformers_auto_bf16` added; the HF spec uses `transformers_auto`, which stays FP16; `max_output_factor` 3 to 7 in the V3 adapter; six spec files move model paths. Correct. The reason given for 7 is labelled inference. |
| Finding `no-reference-finalization` | Correct. With no `out_logits` spec, `logits_file` is `None`, the KLD block never runs, and `kl_div_sum_ab / kl_div_count` is `0.0 / 0.0` on Python floats, which raises. Had it not, `if collect_logits:` on the next line would raise on an unbound name. The only caller is `main`, independent of `--kld`. So the plain perplexity comparison that worked at 162 fails at this commit. Suspected is right: nothing was run. |
| Finding `cache-clear-argument-mismatch` | Correct. `disk_lru_cache_clear("test_ppl", test_data_spec, spec)` builds a two-argument key; `test_ppl` is now cached under three. The clear also runs before `logits_file` is computed. |
| Execution | Recorded output: the keys differ; zero over zero raises; two and six extra copies. Matches the prose. |

## Ledger

- `exllamav3-logits-padding-width-mismatch--r002`: accepted. Adds 164's concrete Gemma 3 case as a reviewer
  observation and `966762a3` as an affected revision; root origin and status unchanged.

## Not verified

- Any evaluation run, and the two images.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: file both findings, introduced at `3873d40a`. For the first, record that it turns a working path
   (perplexity without a reference, as of 162) into a failing one.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval with `--approve`.
2. Run the four guidance-6 trial sessions and file `guidance-6-trial-001`; continue at 166.
