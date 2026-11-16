# Verdict: commit-000175-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000175-001`
Packet: `.teacher/retrieval/000175-001`
Upstream: `c0a2028fb579d04491db8427f1e38979a4dcd164` "compare_q.py: Fix some logic for KLD test"
Request: `reviews/requests/commit-000175-001.md` (sha256 `f54d7477ad11b6ee58a473f65fde2fc86c74c7092825347f40af759fc4096bb7`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry read the 165 and 173 entries, says correctly that the two edits
depend on each other, and carries the 173 finding unchanged.

The fix attribution is **confirmed**: `c0a2028f` fixes `exllamav3-compare-q-no-reference-finalization`.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 10 of 10 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; exactly 174 strict-ancestor entries; 2,657 blobs hash to their names; no evidence timestamp after the cutoff. |
| Implementation hashes | 42 of 44 match the files on disk. `teacher/session.py` and `teacher/walk_inputs.py` differ, and I checked why: the run's recorded hashes equal the committed files at `0ed73a1`; the working copies were modified at 20:50:21, after the draft (20:49:45) and the validation report (20:49:47), by the guidance-8 trial patch, as the request says. The run did not use the patched files. |
| Replay | 10 of 10 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 174/001's. Guidance 7. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Twelve open rows at 2025-05-18T19:55:26Z; my query agrees. No closed row qualifies. |
| The change | `collect_logits = False` before the reference branch; the perplexity lines move out of the progress-bar block; the divergence division and its print run only when `logits_file` is set. Correct. |
| Dependent edits | With only the default, the division still raises; with only the condition, `if collect_logits:` reads an unset name. Each needs the other. Correct. |
| Unchanged metric code | Divergence is computed for the first ten rows only; a collecting run adds one to the count per row and nothing to the sum, so reports zero; the result holds `kld` only when `logits_file` is set. Correct. |
| Spec edit | `tokenizer_dir` in `eval/spec/wiki2_llama3.json` changes to the instruct model's directory; `get_test_data` passes it to `tokenize_transformers`, which loads a tokenizer from it. Correct. |
| Execution | Recorded output matches the prose: 7.389056 with no divergence, 0 and 0.5 for the synthetic cases, zero-over-zero raises. Labelled synthetic. |
| Inherited finding | The mask can still drop the reference producer and keep its consumers. Unchanged. Correct. |

## Not verified

- Any real evaluation; whether the new tokenizer directory exists or matches the evaluated models.

## Must fix before canonical use

1. The entry says `--kld` only selects the plotted metric. It should add what that now means on the repaired
   path: with `--kld` and no reference spec, results have no `kld` key and `plot` reads `r["kld"]`.
2. `eval/spec/wiki2_llama3_large.json` keeps the old tokenizer directory; the entry does not say the edit is to
   one of two Llama 3 data specs.

## Follow-ups

1. Ledger: record `c0a2028f` as the fix of the no-reference record; add it as an affected revision of the
   filtered-reference record. The three 174 identities are still owed.
2. The guidance-8 implementation request is expected next or soon; the walk stays on 7.

## Next

1. Record this approval with `--approve`.
2. Proceed to 176.
