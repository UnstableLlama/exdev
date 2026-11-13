# Verdict: commit-000066-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000066-001`
Packet: `.teacher/retrieval/000066-001`
Upstream: `322815f71eaf582e36fd81bc6fdf5148b27fb97a` "Quant: Refactor regularization, autodetect need for out ch scales, add switch to force enable/disable"
Request: `reviews/requests/commit-000066-001.md`
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**APPROVED for ancestor retrieval only.** Unassisted. The walk may continue from commit 67.

Canonical and training remain false.

Not thin. This is the largest change since commit 55 (four files, 141 lines added) and the entry is in proportion: the decision rule with its boundary, what is and is not switched off, the command-line and resume behaviour, the metadata, every caller of the changed signatures, and what the change does to the two findings from commit 63, whose entry it read.

## Artifacts reviewed (sha256)

- draft.json: `ab59a4f114d29fbfaed88cc5a7630b79552225e70083fd7c50a814ea9e5c57eb`
- draft.md: `a2897fa619286d1dc9149188060aac9e18a2ac76349dabc2b56f6984a1170605`
- raw-transcript.json: `5ea093b4f68e698be68974536c6ba00e17519414332c72987702b01db74657ab`
- provenance.json: `aad517c0c05b4a710c7c380c14b918e9ac7485802973ea169965820ef0243774`
- coverage.json: `c73f942d736cb478bbfe2f142063a240b9669cb883571d6abba61b98407b6544`
- packet manifest (on disk): `488e21d0ca0e91195285908b6e56d5b29c5500421146aace4311bb2f96aea583`
- unreferenced bundle: `7f32d8e41726f1347186275e5bb300007283a292c130e7cc828720248cb6721e`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 24 of 24 ledger entries match the transcript; final message equals the annotation; Markdown equals the render; assessment is full review; 37 of 37 implementation hashes match; exactly 65 strict-ancestor entries; all 962 blobs hash to their names; all four diff sections read; the parent `quantize.py` read whole. |
| Unassisted | No coverage field, no assistance flag. Standing instructions byte-identical to the unassisted guidance 4 prompt. |
| Opening context | Message, author, parent `bcc09666` and task SHA match Git. Cutoff is the committer date, 2025-04-17T18:37:25+02:00 (the author date is 26 seconds earlier). |
| Catalog | Eight rows: 1, 4, 7, 10, 14, 15, 16, 17. Against GitHub: issues 16 and 17 closed at 19:58 and 18:15 UTC that day, after the 16:37 UTC cutoff, so both are correctly still open; issue 18 was created the next morning. |
| Decision rule | Verified. `finalize_capture_H` clones the damped diagonal before the sign flips and transforms and returns it, including on the reuse path. `regularize` sorts its square root descending, sums the first `k // 50` entries over the total, and in automatic mode applies output scales only when that ratio is strictly below 0.15. A forced value overrides. |
| Flow | Verified. With scales off, `sv` keeps its random signs, and the division by `sv`, the right transform, the input scales with the codebook constant, and the left transform all still run. The blockwise in-place helpers replace the whole-matrix ones and assert float input and divisibility by 128. Output tensors are unchanged in kind. |
| Scale search | Verified. The `return` moved below the synchronisation loop and now returns the midpoint and the mean of the two retained trial errors. The progress expression is unchanged. |
| Converter and metadata | Verified. Mutually exclusive switches defaulting to None; the policy is set from the command line on every run and never read back from the saved job, so a resume without a switch is automatic; `--override_anyway` forces the override permission for every listed argument; `head_bits` and the requested policy are written to the quantisation metadata. |
| Callers | Verified by grep at the task: `finalize_capture_H` and `block_ldl` have one caller each, both updated; `g_scale_gss` is called only from `regularize`; `convert_exl3` is called from the converter and from `tests/test_quant_fn.py`. |
| Findings | Both hold. The test's dictionary has `K` and `seed` only, so `regularize` raises `KeyError` on its first line; the entry is right that the same test already lacked `devices`, so this is not evidence it passed before. The progress finding is inherited through commit 63's entry. Both suspected, unexecuted. |
| Issue 16 note | Labelled inference and bounded: the traceback passes through the calibration capture, and the entry says that does not show this change addresses it. |
| Scalar check | Re-ran: output identical (skew 0.02 and 0.1645; eleven progress updates of 100). |
| Tests | 209 passed earlier in this session on the same implementation hashes. |

## Not verified

- No conversion. Which layers of any real model fall on either side of the cutoff is unknown, and the entry claims nothing about it.

## Must fix before canonical use

Reviewer-only.

1. The entry says the converter "prints the actual decision" but not how it gets it: `quantize_exl3` writes the decision and the global scale back into the caller's `quant_args` dictionary. The converter builds a fresh dictionary per layer, so nothing leaks, but a caller that reused one dictionary would turn the first layer's automatic decision into a forced policy for the rest. A canonical entry should state the write-back.
2. Following from the resume behaviour the entry describes: a job started with a forced policy and finished after a resume without the switch records `auto` in its metadata. The entry has both halves and does not join them.
3. `g_scale_gss` is now always called with verbose off, so its own final message can no longer print; `regularize` prints the equivalent.
4. The progress finding is a further observation of commit 24's defect, not a new one.

## Next

Record this approval and continue the walk from commit 67.
