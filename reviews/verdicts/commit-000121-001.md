# Verdict: commit-000121-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000121-001`
Packet: `.teacher/retrieval/000121-001`
Upstream: `3c801c61b01407d13e609524941333c9a9198f80` "Fix object filename conflict"
Request: `reviews/requests/commit-000121-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and the entry is properly modest: what the rename does is stated as source fact,
why it helps is stated as inference, and the actual object-naming rule is left unestablished.

Like 117, it read no ancestor prose and so does not say where the conflict came from. It came from commit 119.

## Artifacts reviewed (sha256)

All twelve hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 120 strict-ancestor entries; 1,769 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical. No `run` call. |
| Unassisted | Standing instructions byte-identical to 120/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 25, 26, 27, 28, 29 (31 has closed). Matches the twelve open rows. |
| Architecture trigger | Does not fire. |
| Diff claim | `stloader.cu` is renamed `stloader_cu.cu` (97% similar: its one `#include` changes) and `stloader.cuh` is renamed `stloader_cu.cuh` (100% identical); `stloader.cpp`'s include changes to match. Nothing else. Correct. |
| References | At the task no file mentions `stloader.cuh`; the two includes are the only references to the header. Correct. |
| Build discovery | `setup.py` and `ext.py` both walk the extension directory and take every `.c`, `.cpp` and `.cu`; the first feeds `CUDAExtension` with `BuildExtension`, the second `torch.utils.cpp_extension.load`. No source list to update. Correct. |
| Collision inference | Labelled inference, with the naming rule left open. Consistent with the tree: at the parent the only same-stem source pairs are `stloader.cpp`/`stloader.cu` (same directory) and `hadamard.cpp`/`quant/hadamard.cu` (different directories, present since the first commit and untouched here). So the conflict being fixed is between same-stem sources in one directory. |
| Discussion | Issue 7 as at 118 to 120; the entry says the link is only shared build context. Correct. |
| Findings | None, and none needed: the commit removes a defect, it adds none. |

## Reviewer-only notes (never to a teacher)

- The conflict was introduced by `647bb7d5` (position 119), which added `stloader.cu` beside `stloader.cpp`. The 119
  entry did not notice it, and neither did my 119 verdict. It lived for two commits (119 and 120).
- I did not establish which build path failed or how (overwritten object or a build-system error). PyTorch is not
  installed in this machine, so its build helper could not be read.

## Not verified

- Any build.

## Must fix before canonical use

1. A canonical entry should name `647bb7d5` as the commit that created the same-stem pair, and link to it.

## Follow-ups

1. Ledger, when next revised: one record for the same-directory same-stem object conflict, introduced at `647bb7d5`,
   fixed at `3c801c61` (fix-derived from this commit; suspected, since no build was run). It also belongs in 119's
   canonical-use list alongside the three findings already there.

## Next

1. Record this approval.
2. Continue the walk at commit 122.
