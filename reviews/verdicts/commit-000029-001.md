# Verdict: commit-000029-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000029-001`
Packet: `.teacher/retrieval/000029-001`
Upstream: `ae9f910be23209c761505373e24b91adb6033c39` "Help for conversion script"
Request: `reviews/requests/commit-000029-001.md`
Reviewed: 2026-11-11

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

**ACCEPTED:** `reports/defect-ledger/exllamav3-negative-final-device-share--r001.json` (sha256 `525ba55c...48ad`).
**ACCEPTED:** `reports/defect-ledger/exllamav3-required-devices-key-test-caller--r002.json` (sha256 `2dbde231...cec2`).

No blockers to continuing the walk. The draft checks one documented option against the code and finds it wrong; it leaves several others unchecked, listed below as canonical blockers.

## Artifacts reviewed (sha256)

If any differ, this verdict does not apply.

- draft.json: `9453224ec861f6f7f660a4d98e1ee369940a38d5626d3be4a99e87ffdb00d8e7`
- draft.md: `7d3e6a964e20bc543feb31d94e0c636734535e835c62b4b8ecc66c747f08c065`
- raw-transcript.json: `f8307e6a85d19bacd8f05e14b87043aaf448e30d5891d78f92d0802db07f18ae`
- provenance.json: `327a92ebdaa57dca85fc01a7d47df5cc1a38e3fcec95ccd6b17491ff831a9383`
- packet manifest: `c866131b06596ee941793fb7cdd61c0c278d07eaf8760a793fd1cd15e9eee756`

## Run checks

| Check | Result |
|---|---|
| Opening context | Complete under contract v3: commit message, author `turboderp`, parent (commit 28), cutoff 2025-04-11T00:26:03+02:00, two change sections, empty referenced catalog, eight-row unreferenced catalog. |
| No future information in the teacher's input | Confirmed. |
| Unreferenced catalog | Eight items: issues 1, 7, 8, 9, 10, 11, 12 and PR 4 (bundle hash `6b6de3ed...6fe0` equals the file on disk). The teacher read none. I read the five newest as of the cutoff. Issue 9 ("measurements.json") asks whether work can be reused across bitrates, a conversion-workflow question the new guide does not address. Issues 8, 11 and 12 are conversion or runtime errors on specific models. None reports a problem with the documented options, so none is on point for what this commit says; issue 9 is the nearest context. |
| Draft replay | draft.md is byte-identical to `teacher.editorial.render(draft.json)`. |
| Hashes | Manifest hash matches provenance.json; every `implementation_sha256` entry matches the working tree. |
| Source coverage | Both diff sections read, plus the whole parent `convert_model.py` and `compile.py`; searches for `shard_size` and `compile_model(`. No ancestor prose read. |
| The change | Correct: adds `doc/convert.md` (101 lines) and one README line linking to it. No code changes. |
| Finding `shard-size-documentation` | **Confirmed on both counts.** The guide says `--shard_size` takes a float; the parser declares `type = int`. The guide says 0 disables sharding; `compile_model` computes `max_shard_bytes = 0` and starts a new shard whenever the running size is positive, so every module with tensors after the first gets its own file. There is no disabling branch. |
| Multi-GPU example | Correct: `-d 2,0,1` makes device 2 primary; `-dr 3,4,5` sums to 12. |
| Execution claim | Honest: argparse on the one option and a transcription of the shard loop. |
| Tests | 182 passed, 0 skipped with `EXDEV_SANDBOX_TESTS=1`. |

## Request-file claims

| Claim | Result |
|---|---|
| Commit 28 approval bound to the verdict at `a14da6a1...80e9` | Confirmed: equals the file on disk. |
| Negative-share r001: commit 28 only, plain-Python transcription, exception unobserved, condition narrow | Confirmed. One dependency (`4d82aab`); limits say the triggering space was sampled, not enumerated. Evidence hash verified. Impact medium: acceptable given the failure precedes any GPU work. |
| Required-devices r002 supersedes accepted r001 and adds only commit 28 | Confirmed. r001 is byte-identical to the accepted version; r002 adds `4d82aab` as still affected and notes the `.get` on the new key. Both evidence hashes verified. |
| Catalog bundle hash and eight items | Confirmed. |

## The guide against the code, option by option

The request asked for this. Verified from `convert_model.py` and `compile.py` at this commit; the argparse checks were run against a copy of the parser declarations.

| Documented statement | Code | Verdict |
|---|---|---|
| `-r / --resume` | Declared as `"-resume", "--resume"`. | Works: argparse resolves `-r` as an unambiguous prefix of `-resume`. The guide's short flag is not the declared one. |
| `--shard_size` float, 0 disables | `type = int`; no disabling branch. | Wrong (the draft's finding). |
| `--shard_size` default 8192 | `override` default 8192. | Correct. |
| `--head_bits` integer 1 to 8, default 6 | `type = int`, default 6 via `override`. | Default correct; no range check exists in the parser or `prepare`. |
| `--out_dir` created, "or overwritten if it does" exist | Created if missing; otherwise written into with a warning when non-empty. Nothing is cleared. | Loose: same-named files are replaced, other files remain. |
| `--work_dir` the only required argument with resume | `prepare` requires it, and requires `in_dir`/`out_dir` only without resume. | Correct. |
| On resume, other arguments are restored, "though some can be overridden" | Restored from `args.json`; but any option with a non-None parser default is written over the stored value on every resume. | **Incomplete in a way that matters.** `--checkpoint_interval` (default 60), `--devices` (default `"0"`) and `--device_ratios` (default `""`) are reset when omitted. The guide's own resume example, `python convert.py -w /mnt/temp/exl3 -r`, run after its multi-GPU example, would continue on device 0 alone with no ratios. Devices print a warning; ratios do not. |
| `--devices` default device 0 | Default `"0"`. | Correct. |
| "very little memory is used on the others" | Each extra device holds cached scratch buffers of 128 × 256 × (65536 >> K) × 2 bytes plus a small cost buffer: about 0.27 GiB at K=4 and 2.1 GiB at K=1, per K used. | A documentation claim the source arithmetic does not support at low bitrates. Not measured. |
| `--device_ratios` relative, `1,1,3` same as `3,3,9` | Shares are `N * r / sum(r)`. | Correct, before the rounding to multiples of 16 tiles. |
| `--last_checkpoint_index`, `--cal_rows`, `--cal_cols`, `--verbose` | Present with those meanings. | Correct. |
| `--checkpoint_interval` "interval between checkpoints" | A minimum interval, checked after each module. | Loose; the parser help says "Minimum". |

## Must fix before any canonical use (not blocking ancestor retrieval)

1. **Resume.** The draft says resume "allows selected overrides" and stops there. It should state that three options are reset by their parser defaults when omitted, and that the guide's resume example therefore does not restore a multi-GPU job. The commit 24 entry already notes this for `--devices`; the teacher read no ancestor entries in this run.
2. **The memory claim.** The draft repeats the guide's framing that extra GPUs use very little memory without setting it against the per-device scratch buffers described in the commit 24 entry.
3. **The remaining rows above** (`-r` versus `-resume`, the missing `--head_bits` range check, "overwritten", "interval"). Each is small; together they are the difference between an entry that checked one option and one that checked the guide.

## Follow-ups

4. Ledger candidate for `shard-size-documentation`: introduced at `ae9f910` as a documentation defect; the underlying `type = int` and zero-threshold behaviour predate it (verify the introduction of the latter from the root tree). Source-verified, not executed.
5. Consider one ledger observation covering the resume resets (devices with a warning from commit 24, ratios silently from commit 28, checkpoint interval from earlier), now that the guide documents resume as restoring arguments.
6. Standing guidance for documentation commits: when a change documents options or defaults, check every documented statement against the parser and its consumers, not only the ones that look suspicious.

## Next

Proceed to commit 30; stop for full review per existing policy.
