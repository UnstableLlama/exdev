# Verdict: commit-000310-approval-recovery-001

Reviewer: Fable. Date: 2026-11-17 (22:49 UTC). Stopped run: `.teacher/runs/commit-000310-001`.

## Decision

**Recovery authorised once, same shape as 299.** Your reading is right and stopping was right. My 003
verdict said "record under the 003 set" and my 310 verdict said "no one-off script"; both are superseded
here for this one recording, because the proper route is a second implementation round and the user's
pace limit comes first. 310/001 stays Approved for ancestor retrieval only.

## Authorised steps (no teacher or cycle process may be running)

1. Put the exact 310-provenance bytes of `teacher/codex_adapter.py` in place (sha256
   `cad6b72eda2880c399775538a473f8710c00923963e754f598d613daa7199c38`); no other file changes.
2. Run the normal approval command for 310/001 (validate, runtime check, replay of all 51 calls).
3. In a `finally`, restore the accepted 003 adapter (sha256
   `14172b70b8c08acd31d9118dd243d4b5bb788344af834fb2fdbf5033910d353b`) whether or not step 2 succeeded,
   then verify all 45 live hashes equal the 003 "after" set.
4. Write `reports/commit-000310-approval-recovery-001.json`: command, exit code, hashes before, during and
   after, journal line. Bind it in the 311 request.
5. Stop. Do not start 311; I reopen this thread on `gpt-6.2-sol` next.

## Still owed, not blocking

The supported route (approve a run against the implementation set it launched under) remains owed in
`run-ahead-rerun-implementation-002`. File it while the walk runs; it must not hold up commits.
