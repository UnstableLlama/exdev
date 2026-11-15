# Decision: native arm64 graph backend

Recorded by Fable (reviewer) on 2026-11-14.

## The user's words

Asked "How should graph_query be handled on ARM?", with the two options from
`reviews/verdicts/arm64-runtime-implementation-001.md` ("Native ARM backend", my recommendation, or "Go without it"),
the user answered:

> Native ARM backend

Earlier the same day, asked where the walk should run after the amd64 machine turned out to be unavailable, the user
chose "Native ARM Linux", and asked who applies the sandbox change, "Astra applies it".

## What follows from it (my interpretation, not the user's words)

1. Astra adds the publisher's official arm64 build of the same backend release, v0.12.1, from
   `https://github.com/DeusData/codebase-memory-mcp`. Record which asset (plain or `-portable`), its asset checksum and
   its binary checksum in `graph/backend.lock.json` beside the amd64 entry. The amd64 pin does not change.
2. The runner selects the backend binary and its pin by machine and still refuses a checksum mismatch.
3. Show equivalence before any teacher run: on the same snapshots, the arm64 build returns the same rows as the amd64
   build. The amd64 `result_sha256` values in `reports/teacher-boundary.json` (positions 9 and 10) are the reference.
   If a hash differs, report the difference; do not adjust the reference.
4. `python3 -m teacher.audit_boundary` must pass on arm64 and its report must keep the architecture fields.
5. File a new implementation request covering this and the sandbox change already reviewed. Teacher runs stay blocked
   until it has a verdict. Then 39/006, then commit 75, as before.
6. Runs from here on are made on Linux aarch64 and say so in provenance. Entries for positions 2 to 74 were made on
   amd64 and are not re-authored on this account.
