# Verdict: commit-000028-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000028-001`
Packet: `.teacher/retrieval/000028-001`
Upstream: `4d82aab28eb526fb387a12f1d190af6fd875b999` "Allow custom split ratio when quantizing on multiple GPUs"
Request: `reviews/requests/commit-000028-001.md`
Reviewed: 2026-11-11

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

**ACCEPTED:** `reports/defect-ledger/exllamav3-cache-docstring-contract--r001.json` (sha256 `5d9e30a5...f606`).
**ACCEPTED:** `reports/unreferenced-discussion-retrospective-002-027.json`.

No blockers to continuing the walk.

## Artifacts reviewed (sha256)

If any differ, this verdict does not apply.

- draft.json: `5e6072e392f71531893d75383eeb7e145494c8dee1d04d09c8f261278cf760c6`
- draft.md: `324d15763f3d771878341d434dca44b8a3bd443cd2625cfc0c5c347de14cc0cf`
- raw-transcript.json: `e085ffa4b7e77fdd3f76a376977cfe22c22addda623f06e6e32d71dd06696860`
- provenance.json: `889c3c94111949de75866c44a83459209270dd4d30aa78c99a4687cf036bc834`
- packet manifest: `583e719eb75915d0dd03112487d1f184907d886ef0c31aa3c41fc8bc7a34f8d8`

## Run checks

| Check | Result |
|---|---|
| Opening context | Complete under contract v3: commit message, author `turboderp`, parent (commit 27), cutoff 2025-04-10T10:42:26+02:00, two change sections, empty referenced catalog, four-row unreferenced catalog. |
| No future information in the teacher's input | Confirmed. |
| Unreferenced catalog | Same four items as commit 27 (bundle hash `be8052a5...fb43` equals the file on disk); none concerns device ratios; the teacher read none. |
| Draft replay | draft.md is byte-identical to `teacher.editorial.render(draft.json)`. |
| Hashes | Manifest hash matches provenance.json; every `implementation_sha256` entry matches the working tree. |
| Source coverage | Both diff sections read, plus the whole parent `quantize.py` and `convert_model.py`; whole-tree searches for `device_ratio`, `device_ratios` and `quantize_tiles_multigpu`. No ancestor prose read. |
| The option | Correct: `-dr/--device_ratios`, string default `""`; parsed to ints when non-empty; asserted equal in length to `--devices`; passed in `quant_args`, or None. |
| Split arithmetic | Correct: each share is `N * r / sum(r)`, rounded to a multiple of 16 tiles, with the discrepancy added to the last share. Equal split is kept when no ratios are given; a single device bypasses the splitter. |
| Empty-share guard | Correct: copy, quantize and copy-back are skipped when a share is not positive; the done event is still recorded outside the guard. |
| Callers | Correct: `ldlq` and the nested `test_scale` in `g_scale_gss`; the unused sync helper still splits equally. |
| Finding `negative-final-share` | **Confirmed.** I ran the formula: 32 tiles with ratios [3, 3, 3, 1] gives [16, 16, 16, -16], and the list reaches `torch.split` before the guard. The exact exception was not observed by the draft or by me (Torch is not installed here). |
| Other examples | Correct: [2, 2, 4] over 256 gives [64, 64, 128]; [0, 1] gives [0, 256]. |
| Tests | 182 passed, 0 skipped with `EXDEV_SANDBOX_TESTS=1`. |

## Request-file claims

| Claim | Result |
|---|---|
| Commit 27 approval bound to the verdict at `f20d9113...ac83` | Confirmed: equals the file on disk. |
| Cache-docstring r001 is limited to commit 27, includes the shelf-sharing example, makes no execution claim | Confirmed. One dependency (`5498926`); the shared `get_dataset_text` shelf is recorded and explicitly not called harmful; impact low, documentation only. Evidence hash verified. |
| Catalog bundle hash and four items | Confirmed. |
| Audit 2 to 27 at `06067341...0872` | Confirmed. |

## Must fix before any canonical use (not blocking ancestor retrieval)

1. **Resume silently discards stored ratios.** The parser default for `--device_ratios` is `""`, which is not None, so `override` reaches its final line and writes `""` over whatever a resumed job had stored. Unlike `--devices` (noted in the commit 24 entry), no warning is printed, because the warning branch requires the new value to be truthy. By source, a job started with `-d 0,1 -dr 3,1` and resumed without those flags runs on device 0 with no ratios, with a warning about the devices and none about the ratios. The draft covers the option but not its resume behaviour.
2. **How often the negative share occurs.** The draft gives one triggering case. From the arithmetic, it needs earlier shares to round up by more than the last share can absorb, which takes a small tile count against several devices. I tried nine ratio lists over tile counts 32 to 512 and only the draft's case went negative. The entry should say the condition is narrow, not leave one example to stand for the rate.
3. **A zero-sum ratio list divides by zero.** `--device_ratios 0,0` is a non-empty list, so `N * r / sum(r)` raises `ZeroDivisionError`. Not in the draft.
4. The help text's example reads `--device_ratio 2,2,4` (singular) for a flag named `--device_ratios`. It still works, because argparse accepts an unambiguous prefix; I ran it. Worth one clause.

## Follow-ups

5. Ledger candidate for `negative-final-share`: introduced at `4d82aab`, reviewer-executed against the formula text (plain Python), exception type unobserved, reach conditional on tile count and ratios.
6. Ledger: the required-`devices` record should gain a revision noting it persists at `4d82aab`. `tests/test_quant_fn.py:139` still builds `quant_args` without `devices`; the new key is read with `.get`, so it adds no second failure.
7. Consider recording the silent ratio reset on resume as an observation alongside the devices one from commit 24; intent is unknown.
8. This commit is 74 seconds after commit 27 with the same author (10:41:12 and 10:42:26 +02:00); a fact the entry may state.

## Next

Proceed to commit 29; stop for full review per existing policy.
