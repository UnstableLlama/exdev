# Verdict: commit-000306-retry-recovery-002

Reviewer: Fable. Date: 2026-11-17 (20:10 UTC).
Stopped run: `.teacher/runs/commit-000306-001` (rejected by `reviews/verdicts/commit-000306-001.md`). New run: `.teacher/runs/commit-000306-002`.

## Decision

**The mechanics are authorised for this rerun.** No approval of any entry is given here.

## What I checked (my own comparison of the two packets)

`.teacher/retrieval/000306-002` against `000306-001`: the manifests differ only in the five
ancestor-selection keys, `coverage_request`, and inside `walk_input_contract` only the coverage path and
hash. Every file of the first packet is present with the same size; four blobs are new (the 305 entry and
selection data). The bound coverage text has the hash of the file I filed. Request hashes match.

## Mechanics

After 307 exits and no cycle process remains: `recover --retry-position 306` bound to this verdict, then the
prepared forward route for `.teacher/runs/commit-000306-002` with `packet` and `original_packet` both
`000306-002`. Fresh reviewer-assisted attempt, guidance 12; nothing from attempt 001 or its verdict reaches
the teacher. If this attempt is also short of the residual step, stop and report; no third attempt without
the user.
