# Verdict: arm64-runtime-implementation-001

Reviewer: Fable (file mailbox). Not an independent review of the three sandbox files: I wrote the trial diff they follow.
Request: `reviews/requests/arm64-runtime-implementation-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, OrbStack machine `exdev-arm` (Linux aarch64, Ubuntu 24.04,
Python 3.12.3, bubblewrap 0.9.0, Codex 0.167.0 aarch64 musl)

## Decision

**HELD: needs a user decision. No teacher run is authorized yet.**

The code change is correct as far as it goes and I would accept it. What holds it is the point the request raises
itself: `graph_query` does not work on this machine, so the boundary audit fails and one of the tools offered to every
teacher would time out. That is not caused by this diff and cannot be fixed inside it.

## Artifacts reviewed (sha256)

All eleven hashes in the request match the files on disk.

## Checks

| Check | Result |
|---|---|
| Diff read | Six files. `runner.py`: library directory and loader chosen by `platform.machine()`, x86_64 values unchanged, any other machine refused. `codex_transport.py`: one more optional read-only bind. `worker.py`: `fork` and `vfork` skipped only when unresolved **and** the machine is aarch64, which is tighter than my trial; `clone`, `clone3`, `unshare`, `setns`, `ptrace` still mandatory. `author.py` and `audit_boundary.py` record `machine_architecture` and `operating_system`. `tests/test_author.py` asserts the two provenance fields. |
| Tests | I ran the suite on the working checkout with the pinned Codex first on PATH: 223 passed in 7.3 s. `git diff --check` clean. |
| Fork filter | `test_run_cannot_fork` passes on aarch64, so `clone` denial covers what `fork`/`vfork` covered on amd64. |
| Replay | 74/001's recorded `run` call returns the recorded stdout byte for byte on aarch64 (done on my trial copy, same sandbox code path). |
| Boundary audit | Reproduced. Positions 9 and 74: `graph_search`, `graph_trace`, `symbol_history`, `repo_map` answer in about 0.2 s; `graph_query` hits the 30 s wall-time budget every time. |

## The graph backend on arm64

- Only `graph_query` executes the pinned backend binary. The other four graph tools read the packet's timeline and
  never start it. My proposal said the graph tools "run through Rosetta" on the strength of `repo_map` and
  `graph_search`. That was wrong: I had not exercised the binary. Corrected here.
- Outside the sandbox, with no resource limits, the x86-64 binary answers `--version` and `cli --help` under Rosetta
  but hangs on every real `cli` call (`query_graph`, `list_projects`, `search_graph`), with one worker or four. The
  last debug line is `mem.init budget_mb=2000`. So the cause is the binary under Rosetta, not Bubblewrap, not the
  rlimits and not this diff.
- The backend's publisher ships a native build of the same release: `codebase-memory-mcp-linux-arm64.tar.gz` and a
  `-portable` variant under v0.12.1. I have not downloaded or run either.
- Across all 90 recorded teacher runs (positions 2 to 74) no teacher has called any graph tool. The failure has cost
  nothing so far, but the tool is advertised to every teacher and a call would burn 30 s and return an error.

## For the user

Choose one:

A. **Native arm64 backend.** Astra adds the publisher's arm64 v0.12.1 build with its own asset and binary checksums in
   `graph/backend.lock.json`, selects the binary by machine, and shows that it returns the same rows as the amd64
   build on the same snapshot (the amd64 results in `reports/teacher-boundary.json` are the reference). New
   implementation request. This is my recommendation.
B. **Proceed without `graph_query` on arm64.** The tool stays advertised and fails closed. Provenance already records
   the architecture, so affected runs can be identified. Cheaper, but teachers on this machine have one tool fewer
   than teachers on amd64 had.

## Not verified

- No live teacher run on arm64.
- Whether the native arm64 backend works here, and whether its results equal the amd64 build's.
- Codex's own outer sandbox blocks nested Bubblewrap (the request's NETLINK_ROUTE note). Tests and teacher runs must be
  started outside it; how Astra's session is permitted to do that is the user's setting.

## Follow-ups (do not block)

1. `runner.py` raises the same "Unsupported runtime" text for an unknown machine and for a missing file. Say which.
2. `reports/arm64-runtime-boundary-001.json` has no `checks`; keep the passed checks up to the failure next time.

## Next

Wait for the user's choice. Do not start 39/006 or commit 75. Keep the working tree as it is; nothing here needs to
be undone under either answer.
