# Verdict: commit-000343-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (17:48 UTC). Run: `.teacher/runs/commit-000343-001`. Packet: `.teacher/retrieval/000343-001`.
Upstream `6565dee474d3f9b247673e24dbfe3b9a72ed278c` "Add custom atexit handler".

## Decision

**Approved for ancestor retrieval only.** Canonical and training remain false.

## What I checked myself

- Mechanical: request hashes 0 bad; `impl 47`; evidence 21 calls, 0 bad, 0 uncited; final equals annotation; 4,726 blobs,
  0 bad; 21 calls replay with 3 mismatches, equal to the 3 `ancestor_read` calls of this sparse packet. No repair turn.
- Run-ahead: the packet lacks the 342 entry and both commits touch `util/misc.py`. The teacher read `find_free_port` from the parent
  source and describes it correctly, so the missing entry did not matter.
- Central claims, by my own runs of `Cleanupper` taken from Git at the commit, on the VM's Python:
  - A local instance survives return, `del` and `gc.collect()`, because the finalizer holds the bound `_shutdown`.
  - At normal exit the order is: atexit handler registered after, then the cleanup callback, then atexit handler registered before.
  - Callbacks run in registration order. A raising callback stops later ones on that instance, and a separate instance still runs.
- The parent tree has no `Cleanupper`, `register_atexit`, `_shutdown`, `atexit` or `weakref`, and this commit adds no caller.
- PR #22: title matches, and the posted server example has the interrupt handler and `server_close()` the entry describes. The entry
  rightly claims no link to this commit.
- Both findings are new, suspected and accurate as written.

## Not established

Timing against worker or thread teardown was not measured, so the docstring's "before Python starts tearing down objects/threads"
stays unverified. The entry says so.

## Requested next

File the two 343 ledger candidates with the next request.
