# Verdict: commit-000069-003

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000069-003`
Packet: `.teacher/retrieval/000069-003`
Upstream: `f8b9ab72ae9fd4fb00d4aab34302f9eb5edd81f5` "Tokenizer: Disable truncation"
Request: `reviews/requests/commit-000069-003.md`
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**APPROVED for ancestor retrieval only. Unassisted. It supersedes attempt 002 and is the entry in force for commit 69.** Commit 69 is closed.

**Then pause.** Record this approval and stop before commit 70. The user is moving to another machine for the weekend and I am committing and pushing the tree. Resume at commit 70 when he restarts the loop.

Canonical and training remain false.

This is the first entry authored under contract 8, and the closed catalog did what it was built for: issue 16 was listed, the teacher read it in full, and the entry now states the commit's actual motivation, attributed to the people who wrote it, with the link labelled inference.

## Why 003 and not 002

Both are true. Attempt 002 (assisted) lists every caller of the encoding helpers. Attempt 003 (unassisted) has the reason for the change, the one calibration path that shows the mechanism, and a worked example at the reported numbers, in about a third of the length. For a reader of this commit 003 is the fuller answer to "why", and it carries no assistance flag. Attempt 002 stays on record as approved and superseded.

## Artifacts reviewed (sha256)

- draft.json: `ab688c392d204f65bd0087df4078760d63be186a9fe564ea87b4504e62320c5c`
- draft.md: `b331bede24ed3443870a07d8708e5542513d270cdf512a70feb738f932de1931`
- raw-transcript.json: `ed2d23aab8403fb92facf3ffbe316e89581f19363e044643f0bfcde2d7400d7f`
- provenance.json: `77e0a430027a007ee852def610c1dcc4b535219c9983a2000fbc23d1c98917a6`
- coverage.json: `37d9511e1d0cde1f9d29625cb6183ac04efa27ba1ad7f389099401c16831f423`
- packet manifest (on disk): `950cc94d237a2300937534d2b20291bf6390abe1482bb77b913b0e8726ecfa27`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 11 of 11 ledger entries match the transcript; final message equals the annotation; Markdown equals the render; assessment is full review; 38 of 38 implementation hashes match; exactly 68 strict-ancestor entries; all 984 blobs hash to their names; no evidence timestamp after the cutoff. |
| Unassisted | No coverage field, no assistance flag in provenance or the review record. |
| What changed in the inputs | Against attempt 001: the standing instructions gain exactly the one closed-catalog sentence; the opening context gains exactly one field, `closed_discussion_catalog`; every other field is identical. |
| Closed catalog | One row: issue 16, closed 2025-04-17T19:58:31Z, matched on `tokenizer` and `truncation`. |
| Issue 16 as served | The fetch returned the whole snapshot (8,701 bytes). Its last timestamp is the closing comment, fourteen seconds before the cutoff. Nothing later. |
| No hindsight | No packet blob contains a ledger id, a ledger path or a path under `reviews/verdicts`. |
| Attribution and framing | Correct. The issue's own title is quoted. DekoMoon is named as the reporter and turboderp as the source of the diagnosis (a `truncation` block with `max_length` 4096 in the model's `tokenizer.json`). The link to this commit is labelled inference, with its basis: the diagnosis and the final comment about overriding the feature at load time. The entry says the discussion is not a local reproduction. I checked each of these against the snapshot. |
| Source claims | Verified at the parent, as in the earlier attempts: placement of `no_truncation()`; `split_raw` encodes the whole text and slices rows; `get_default_calibration` gives `code.utf8` and `technical.utf8` weights 15 and 10 of 128 and routes both through `split_raw`. |
| Scalar check | Re-ran: output identical. At 100 rows, 2,048 columns and a 4,096-token cap: 11 and 7 requested rows, two full slices each, the rest empty. The entry says this supports the reported mechanism "without establishing the CUDA failure chain". Right. |
| A failed read | One `repo_read` asked for `exllamav3/conversion/calibration.py`, which does not exist; the teacher then found `calibration_data.py` by search. Harmless. |
| Tests | 221 passed in this session on the accepted implementation. |

## Not verified

- That an empty calibration row causes the reported CUDA error. Nobody ran it; the entry does not claim it.
- What `no_truncation()` does inside the tokenizers library.

## Must fix before canonical use

Reviewer-only.

1. The entry covers `split_raw` only. Attempt 002 found that the article-based path and both evaluation scripts are affected in the same way. A canonical entry should take one sentence from 002 for them.
2. `num_tokens` is listed under what the override covers. True, and it has no caller, as 002 established.

## Follow-ups

- Defect ledger: issue 16 is a reported failure with a maintainer diagnosis and this commit as its remedy, all before the cutoff. It can be recorded without hindsight.
- The audit expectation stands: issues 99 and 233 should appear at positions 560 and 1100.

## Next

1. Record this approval; mark 69/002 superseded for future retrieval.
2. Stop. Do not author commit 70 until the user restarts the loop.
