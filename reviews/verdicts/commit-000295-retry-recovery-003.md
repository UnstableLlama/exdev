# Verdict: commit-000295-retry-recovery-003

Reviewer: Fable. Date: 2026-11-17 (15:16 UTC).
Stopped run: `.teacher/runs/commit-000295-002` (rejected by `reviews/verdicts/commit-000295-002.md`). New run: `.teacher/runs/commit-000295-003`.

## Decision

**The mechanics are authorised for this rerun.** No approval of any entry is given here.

## What I checked (my own comparison of the two packets)

`.teacher/retrieval/000295-003` against `000295-002`: the manifests differ only in `coverage_request` and,
inside `walk_input_contract`, in `coverage_request_path` and `coverage_request_sha256`. The 294 ancestor
entries are identical. The bound coverage text has the hash of the file I filed
(`reviews/verdicts/commit-000295-003.coverage.md`). The blob set is unchanged (4284). Request hashes match.

## Mechanics

`recover --retry-position 295` bound to this verdict, then the prepared forward route for
`.teacher/runs/commit-000295-003` with `packet` and `original_packet` both `000295-003`. Fresh
reviewer-assisted attempt, guidance 12; nothing from attempts 001 or 002 or their verdicts reaches the
teacher. If this attempt is also short of the reach, stop and report; do not start a fourth.
