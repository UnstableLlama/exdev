# Verdict: commit-000024-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000024-001`
Packet: `.teacher/retrieval/000024-001`
Upstream: `72e88aef02ac18ef080f3cc084bac6109553d322` "Multi-GPU quantization"
Request: `reviews/requests/commit-000024-001.md`
Reviewed: 2026-11-11

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

**ACCEPTED:** `reports/unreferenced-discussion-retrospective-002-023.json`.

No blockers to continuing the walk. One reviewer-found defect is missing from the draft and is a canonical blocker (item 1 below).

## Artifacts reviewed (sha256)

If any differ, this verdict does not apply.

- draft.json: `7f7a5d15043779e83c70033360e7ce61acb776536f5a08357469a3676658c72e`
- draft.md: `46a022e1dd188162b012722899f40d67de0bea26098be2982c249bb15c514a3d`
- raw-transcript.json: `d028fe2cea90c19c993a89c09646f51991ec0f7e5c382d1fbaf5ada24df438e3`
- provenance.json: `df70e912d77b32d4ec321650c2ad01a48abaf5c5028bec36de5dfe44f6ef0f5c`
- packet manifest: `cb997b38bb240d7d4d90a1813ff0ef6f8fad13eb9e72361598aac2406db4fbed`

## Run checks

| Check | Result |
|---|---|
| Opening context | Complete under contract v3: commit message, author `turboderp`, parent (commit 23), two change sections, empty referenced catalog, five-row unreferenced catalog. The cutoff is the committer date 2025-04-09T03:01:44+02:00; the author date is fifteen minutes earlier. |
| No future information in the teacher's input | Confirmed. |
| Unreferenced catalog | Same five items (bundle hash `b034b032...2725` equals the file on disk). Issue 6 now carries its two comments from before this cutoff. None concerns multi-GPU quantization; the teacher read none. |
| Draft replay | draft.md is byte-identical to `teacher.editorial.render(draft.json)`. |
| Hashes | Manifest hash matches provenance.json; every `implementation_sha256` entry matches the working tree. |
| Source coverage | Both diff sections read in full (the second in one 24 kB read), plus the whole parent `quantize.py`, the relevant part of `convert_model.py` and `progress.py`. No ancestor prose read. |
| `--devices` | Correct: string default `"0"`, parsed to a list of ints in `main`, first entry used for module loading, whole list passed in `quant_args`. |
| Resume behaviour | Correct and a good catch: because the parser default is non-None, `override` replaces a stored device list with `"0"` on resume when the flag is omitted. It prints the override warning when it does. |
| `quantize_tiles_multigpu` | Correct: single-device short-circuit; pinned host staging; even split with the whole remainder on the last device; per-device stream, wait on the input-copy event for secondary devices, a done event per slice, and the main stream waits on all of them before gathering. |
| LDLQ | Correct: the feedback loop is unchanged apart from the helper call; it runs inside the first device's stream and synchronizes every selected device on entry and before returning. |
| Scratch buffers | Correct: cached by device and K with `lru_cache`; shapes (128, 2, 65536 >> K) float and (128, 256, 65536 >> K) int16. 272,629,760 bytes at K=4 recomputed by hand. |
| Split examples | Correct: 128 over 3 gives [42, 42, 44]; 8 over 10 gives nine empty slices then 8. |
| Unused sync variant | Correct: `quantize_tiles_multigpu_sync` is defined and not called. |
| Block size | Correct: the three `block_*` helpers move their default from 16 to 32. |
| Finding `scale-progress-premature-completion` | **Confirmed by source.** `pb.update(100 - 100 * int(delta2 / delta1))`: after any contraction `delta2 < delta1`, so `int(...)` is 0 and every update is 100, against a bar whose total is 100. |
| Execution claim | Honest: scalar arithmetic only; limits say no CUDA or conversion ran. |
| Tests | 181 passed, 0 skipped with `EXDEV_SANDBOX_TESTS=1`. |

## Request-file claims

| Claim | Result |
|---|---|
| Commit 23 approval bound to the verdict at `2d6a8165...aecf` | Confirmed: equals the file on disk. |
| Catalog bundle hash and five items | Confirmed. |
| Audit 2 to 23 at `89091bc4...4012` | Confirmed. |

## Must fix before any canonical use (not blocking ancestor retrieval)

1. **`devices` is now a required key and the repository's own caller does not supply it.** `ldlq`, `g_scale_gss` and `quantize_tiles_multigpu` all read `quant_args["devices"]` with no default. `tests/test_quant_fn.py:139` builds `quant_args` with only `K` and `seed` and calls `linear.convert_exl3` at line 143. By source that path now raises `KeyError: 'devices'` at this commit. The teacher's search for `devices` was limited to the `exllamav3/` directory, so it never saw `tests/`. This belongs in the entry as a finding, with its reach: `convert_model.main` supplies the key; the test does not; no other builder of `quant_args` for `convert_exl3` exists in the tree.
2. **Cached scratch buffers accumulate across bitrates.** The draft says buffers are cached by device and K but not what follows: `lru_cache` keeps one pair per (device, K) for the life of the process. The edges buffer is 128 × 256 × (65536 >> K) × 2 bytes, which is about 2.1 GiB at K=1, 1.1 GiB at K=2, 0.5 GiB at K=3 and 0.27 GiB at K=4, per device. A conversion whose allocation uses several K values keeps all of them resident. This is arithmetic from the source; whether a given job mixes K values was not assessed.
3. **Ancestors on the same function were not read.** Commit 13's entry covers `g_scale_gss` and commit 22's covers the progress bar whose total of 100 this finding depends on. The draft's finding is right without them, but the entry should connect to them.
4. `quantize.py` now imports `cuda_sync_active` and does not use it. Trivial, and unmentioned.

## Follow-ups

5. Ledger candidate for the missing `devices` key: introduced at `72e88ae`, source-verified, reach limited to `tests/test_quant_fn.py` and any external caller of `Linear.convert_exl3`; not executed.
6. Ledger candidate for `scale-progress-premature-completion`: introduced at `72e88ae`, source-verified, display only.
7. Consider recording the resume behaviour (an omitted `--devices` resets a stored multi-device list to `"0"` with a warning) as an observation; whether it is a defect depends on intent, which is unknown.
8. Standing guidance: when a change makes a dictionary key or argument required, grep the whole tree, including `tests/`, for every place that builds that dictionary or calls that function. This run's search was restricted by path.
9. The tile-sampling observation from commit 13 is still present: the sampling loop in `g_scale_gss` is unchanged by this diff.

## Next

Proceed to commit 25; stop for full review per existing policy.
