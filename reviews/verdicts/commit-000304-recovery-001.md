# Verdict: commit-000304-recovery-001

Reviewer: Fable. Date: 2026-11-17 (19:32 UTC). Upstream `823fd8db` "chat.py: Add Command-A template".
Stopped run: none exists (the GitHub history fetch failed before any packet or run). New run: `.teacher/runs/commit-000304-001`.

## Decision

**Authorised.** Clear the stop with the unchanged `orchestration.run_ahead recover` bound to this verdict,
then one normal detached cycle at 304. A repeated failure stops again; then keep the stderr of the failing
`gh` call in the report.

## What I checked

Request hashes match. Journal `stopped_failure`, next position 304, no 304 packet or run directory.
