# Verdict: commit-000329-001 (teacher gpt-6.2-sol, guidance 12, unassisted; ran ahead of 328)

Reviewer: Fable. Date: 2026-11-18 (06:15 UTC). Upstream `5cada8cd` "Actions: Add Torch 2.8 support".
Run: `.teacher/runs/commit-000329-001`. Packet: `.teacher/retrieval/000329-001`.

## What I checked myself

- Request hashes 0 bad. `check.py`: impl 46 bad [], evidence 25 calls 25 bad [] uncited [], final==annotation
  True, blobs 4613 bad 0. anc 328 entries 327 False and replay 25, mismatch 4 = the four ancestor reads:
  sparse, as disclosed ("Ran ahead of: 328").
- Run-ahead judged: 328 is the 0.0.5 version bump, no shared file; this entry reads the version only through
  the workflow's regex, which it describes from source. The missing entry did not matter.
- Diff read in full (nine added matrix rows, each a 2.8.0 twin of a 2.7.0 row).
- Central claims confirmed in source at the sha: `matrix.torch` is used in the job name (line 17), the Torch
  install (177) and the CUDA build tag (191-194) only; the non-CUDA branch (198-199) is selected by empty
  `cuda` and `rocm`, not by the `sdist` label, and passes no Torch-specific tag. So the finding's premise
  holds: the two non-CUDA rows are not distinguished in what they build or upload.
- The entry made the central check itself (9 to 18 rows by execution, same index, distinct CUDA tags) and
  found the one real consequence of duplicating the non-CUDA row. Limits are stated.

## Must fix before canonical

- Three Source Notes paragraphs on unrelated issues (#17, #57, #49, #34, #64); cut, as you say.
- Link the 328 entry once visible.

## Decision

Approved for ancestor retrieval only. Canonical and training remain false.
