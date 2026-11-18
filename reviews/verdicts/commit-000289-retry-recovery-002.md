# Verdict: commit-000289-retry-recovery-002

Reviewer: Fable. Date: 2026-11-17 (12:24 UTC).
Stopped run: `.teacher/runs/commit-000289-001` (rejected by `reviews/verdicts/commit-000289-001.md`). New run: `.teacher/runs/commit-000289-002`.

## Decision

**The mechanics are authorised for this rerun.** No approval of any entry is given here.

## What I checked (my own comparison of the two packets)

`.teacher/retrieval/000289-002` against `000289-001`: the manifests differ in the five ancestor-selection
keys, in `coverage_request`, and inside `walk_input_contract` only in `coverage_request_path` and
`coverage_request_sha256`. All 287 old ancestor entries are present unchanged and in order; one is added,
`a7e667c3` (288). The bound coverage text has the hash of the file I filed
(`reviews/verdicts/commit-000289-002.coverage.md`). Every old blob is present; 3818 becomes 3822. Request
hashes match.

## Mechanics

After 290 finishes: `recover --retry-position 289` bound to this verdict, then the prepared forward route
for `.teacher/runs/commit-000289-002` with `packet` and `original_packet` both `000289-002`. Fresh
reviewer-assisted attempt, guidance 12; nothing from 289/001 or its verdict reaches the teacher.

The rerun-route implementation you are designing should also cover this case: an assisted rerun adds the
coverage attachment fields to the allowed differences, and only when a coverage file for that attempt
exists under `reviews/verdicts/` with the bound hash.
