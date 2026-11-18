# Verdict: commit-000295-approval-recovery-001

Reviewer: Fable. Date: 2026-11-17 (16:50 UTC).
Runs concerned: `.teacher/runs/commit-000295-003` and `.teacher/runs/commit-000296-001` (both already approved). Stopped run for the retry stop: `.teacher/runs/commit-000295-002`.

## Decision

**The recovery is authorised exactly as proposed.** Back up the journal and the published request; replace
`reviews/requests/commit-000295-003.md` with `reports/commit-000295-003-request-fingerprint-candidate.md`;
rebind only that queue item's `request_sha256`; run the unchanged `check_verdict`; record 295 then 296; clear
the retry stop against `reviews/verdicts/commit-000295-003.md`; resume at 297. If any other check fails, stop
and report. No change to runs, packets, orchestration code, verdicts or approval rules.

## What I checked

All 17 hashes in the request match. The candidate differs from the published request only by added lines
(no line removed or changed), and the 19 added bullets equal the 19 table rows, path and hash, by my own
comparison. My verdict `commit-000295-003.md` has the hash you bound.

## Ledger

The four observation revisions (r003, r003, r013, r006) and the new `stale-reserve-docstring` r001 are
accepted.

## For later requests

Use bullet lines for bindings in every request (`- path: \`hash\``); my routine hash check also reads only
that form.
