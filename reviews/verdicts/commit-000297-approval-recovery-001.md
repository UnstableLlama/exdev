# Verdict: commit-000297-approval-recovery-001

Reviewer: Fable. Date: 2026-11-17 (17:12 UTC).
Run concerned: `.teacher/runs/commit-000297-001` (already approved).

## Decision

**The recovery is authorised exactly as proposed**: back up the request and journal, replace
`reviews/requests/commit-000297-001.md` with the bound candidate, rebind only 297's `request_sha256` under
the journal transaction after 298 exits, then the unchanged `check_verdict` and approval commands with host
permissions. If any further check fails, stop and report.

## What I checked

All 11 hashes match. The candidate equals the published request with only the backticks around the 14
binding paths removed (my own comparison, no other difference).

## Repair sizes

Received; four of five repaired finals are shorter. I am taking this to the user. No change to the repair
policy until they decide. Bindings in requests: plain paths in bullets, always.
