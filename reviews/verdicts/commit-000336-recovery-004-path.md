# Verdict: commit-000336-recovery-004-path

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (16:18 UTC). Stopped run: `.teacher/runs/commit-000336-003`. New run: `.teacher/runs/commit-000336-004`.

## Decision

**Use this file as the recovery decision for `recover --retry-position 336`.** It corrects only my shortened path in
`reviews/verdicts/commit-000336-recovery-004.md`. The authority is unchanged: the user answered "Yes, apply and retry",
which covers the schema fix, now applied, and one fresh unassisted attempt. No approval of any entry is given here.

## What I checked

Request hashes: 8 checked, 0 bad. The schema patch is applied (reverse check passes). No `.teacher/runs/commit-000336-004`
exists. `orchestration/run_ahead.py` refuses a recovery decision that does not contain the stopped run's path.

## Mechanics

All terms of `reviews/verdicts/commit-000336-recovery-004.md` still apply: packet `.teacher/retrieval/000336-002` unchanged,
contract 8, guidance 12, gpt-6.2-sol medium, nothing from earlier attempts reaches the teacher, and if it fails, stop with
no fifth attempt. If it succeeds, stop for review.
