# Verdict: commit-000336-recovery-004

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (16:13 UTC). Stopped runs: `.teacher/runs/commit-000336-001`, `-002` and `-003` (all refused by the
provider, no draft). New run: `.teacher/runs/commit-000336-004`.

## Decision

**The user has authorised the fix and one more attempt.** Asked whether to apply the reviewed fix and retry commit 336,
the user answered: "Yes, apply and retry". Both are authorised, once each. No approval of any entry is given here.

## Authorised

1. Apply `reports/codex-output-schema-implementation-001.patch`, sha256 `adcf1f27015b62ad90cf8368fac91c62c1be98733d283f5d71616470cfb91287`, exactly as reviewed in
   `reviews/verdicts/codex-output-schema-implementation-001.md`. Check the hash first. Run the test suite after applying
   and stop if it fails. Nothing else changes in this step.
2. Once no cycle process remains: `recover --retry-position 336` bound to this verdict, then the prepared forward route
   for `.teacher/runs/commit-000336-004`. One fresh unassisted attempt, contract 8, guidance 12, gpt-6.2-sol medium, with
   teacher input from `.teacher/retrieval/000336-002`, as in 336/003. Any packet content difference stops the run and
   comes back to me. Nothing from the earlier attempts, the requests or the verdicts reaches the teacher. Keep the
   artifacts of all three failed runs as they are.

## If it fails again

Stop. No fifth attempt and no change to the walk without the user. File a request with the hashes of
`codex-failure.json` from the failed run, and no payload text in the request.

## If it succeeds

Stop for review as usual, and report any repair turn caused by an unknown commit hash. Do not run past 336 until I have
reviewed it.
