# Verdict: commit-000336-recovery-003

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (11:01 UTC). Stopped runs: `.teacher/runs/commit-000336-001` and `.teacher/runs/commit-000336-002`
(both failed with `Codex reported an authoring error`, no draft). New run: `.teacher/runs/commit-000336-003`.

## Decision

**The user has lifted the limit set in `reviews/verdicts/commit-000336-recovery-002.md`.** Asked whether to apply the
error-saving change and try commit 336 one more time, the user answered: "Yes, do both". Both are authorised, once each.
No approval of any entry is given here.

## Authorised

1. Apply `reports/codex-failure-diagnostics-implementation-001.patch`, sha256 `b21542fd53f4b6cd912456a091403791c88efd21f9719802bad0c06011574596`, exactly as reviewed in
   `reviews/verdicts/codex-failure-diagnostics-implementation-001.md`. Check the hash first. Run the test suite after
   applying and stop if it fails. Nothing else changes in this step.
2. Once no cycle process remains: `recover --retry-position 336` bound to this verdict, then the prepared forward route
   for `.teacher/runs/commit-000336-003`. One fresh unassisted attempt, contract 8, guidance 12, gpt-6.2-sol medium.
   Teacher input must match the 336/002 packet, `.teacher/retrieval/000336-002`: same approved ancestors through 335.
   If the route needs a new packet directory, compare it with 002 and record the comparison; any content difference
   stops the run and comes back to me. Nothing from 336/001, 336/002, the requests or the verdicts reaches the teacher.
   Keep the artifacts of both failed runs as they are.

## If it fails again

Stop. No fourth attempt and no change to the walk without the user. File a request with the hashes of
`codex-failure.json` from the failed run. Do not put credentials or unredacted payload text in the request.

## If it succeeds

Stop for review as usual. The implementation check should now read `impl 47`.
