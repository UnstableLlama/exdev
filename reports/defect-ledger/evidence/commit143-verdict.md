# Verdict: commit-000143-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000143-001`
Packet: `.teacher/retrieval/000143-001`
Upstream: `ae04741f22324cc746ab78c27365e53e3f9f1cf4` "Actions: Add build action"
Request: `reviews/requests/commit-000143-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry reads the whole workflow, ties the two kinds of job to the one switch
in `setup.py` that distinguishes them, and notices the practical gap: without the release input nothing a job
builds is kept, because there is no artifact upload. No findings, and I found none.

The ledger record `exllamav3-repetition-penalty-masked-nan--r001` is **accepted**.

## Artifacts reviewed (sha256)

All twenty-four hashes in the request match the files on disk. One clerical slip in the request text: it says
"Commit 141 approval recorded"; the hash it lists, correctly, is the 142 verdict's.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 7 of 7 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; 1,903 blobs hash to their names; no evidence timestamp after the cutoff. |
| Ancestry | The parent is `c2b8516f` (position 132), not position 142. The packet holds exactly 132 strict-ancestor entries and nothing from 133 to 142. Correct for a commit on a side line. |
| Replay | 7 of 7 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 142/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Outside author | The author is kingbri. GitHub lists no pull request for this commit; it was pushed directly and joins the main line later through "Merge branch 'master' into dev" (`10222646`). So there is no pull-request discussion to leak. The only packet blobs that mention the author are the task commit itself and issue 17, where they commented in April. |
| Catalog | Eleven open rows at 2025-05-09T18:35:24Z: 1, 4, 7, 10, 14, 22, 26, 27, 28, 29, 34 (33 was closed then; 35 and 36 did not exist yet). One closed row, issue 17, closed 2025-04-17. |
| Architecture trigger | Does not fire. |
| Trigger and permissions | `workflow_dispatch` with a required string input `release`, default `'0'`; `contents: write`; `fail-fast: false`. Correct. |
| Matrix | Nine rows: Ubuntu 22.04 and Windows 2022, each with Python 3.10, 3.11, 3.12 and 3.13, CUDA 12.8.1, Torch 2.7.0 and the same architecture list; and one Ubuntu Python 3.11 row with no CUDA. `rocm` is empty in every row. Correct. |
| Steps | Disk clean-up on Linux before checkout; version parsed from `exllamav3/version.py`; pinned Build Tools on Windows; `setup-uv`; CUDA assembled from thirteen NVIDIA archives on Windows and installed by `Jimver/cuda-toolkit` on Linux; Torch from the `cu128` index; `setuptools==69.5.1`; `python -m build -n --wheel` with the build tag and `TORCH_CUDA_ARCH_LIST`. Correct. One sentence in the entry ("CUDA jobs install the toolkit through Jimver/cuda-toolkit") reads as if it covered Windows; the next sentence corrects it. |
| The other job | CPU Torch, `EXLLAMA_NOCOMPILE=1`, `python -m build -n`. In `setup.py`, `precompile` is false when that variable is present, and the extension is registered only when `precompile and torch`. Correct. |
| Upload | Runs only when the version parsed and `release == '1'`; uploads `./dist/*.whl` to tag `v<version>` with overwrite. No `upload-artifact` step and no pattern for a source archive. Correct. |
| Execution | Recorded output: version 0.0.1, tag v0.0.1, index `.../whl/cu128`, build tag `+cu128-torch2.7.0`. Matches the prose and `version.py`. |
| Ledger `repetition-penalty-masked-nan--r001` | Accepted. One identity: introduced `40863d06`, partial fix `a6538654`, fix `43383ebd`; affected revisions are 90 and 122 only; scope limited to positive finite penalties; kept apart from the presence/frequency record. |

## Reviewer-only notes (never to a teacher)

- **Relevance to the 136 record.** This workflow builds wheels for Python 3.10 and 3.11. That is the project's own
  statement that those versions are targets, which the 136 record lacked ("the repository states no minimum
  Python version"). It only applies once this side line is merged with the sampler change, at `10222646`.
- The workflow was carried over from the sibling project: its error text names `exllamav2/version.py` and a file
  called `build-wheels-release.yml`, and a matrix comment says "Ubuntu 20.04" above 22.04 rows. Cosmetic.
- The job named "sdist" uploads only whatever wheel `python -m build` leaves in `dist`; a source archive, if
  built, is not uploaded. The entry says the output set is unverified, which is the right limit.

## Not verified

- Any workflow run, build or upload, and the behaviour of the external actions.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, when the walk reaches the merge `10222646`: add the wheel matrix as evidence to
   `exllamav3-top-k-int-is-integer-compatibility` (Python 3.10 and 3.11 are build targets).
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the ledger acceptance.
2. Continue the walk at commit 144.
