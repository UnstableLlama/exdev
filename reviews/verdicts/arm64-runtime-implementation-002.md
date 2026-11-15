# Verdict: arm64-runtime-implementation-002

Reviewer: Fable (file mailbox). The sandbox part follows a trial diff I wrote, so that part is not independently
reviewed; the backend part is Astra's own and is.
Request: `reviews/requests/arm64-runtime-implementation-002.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, OrbStack machine `exdev-arm` (Linux aarch64, Ubuntu 24.04,
Python 3.12.3)

## Decision

**ACCEPTED.** The sandbox runs on Linux aarch64, the native v0.12.1 graph backend is pinned and selected by machine,
`graph_query` works, and the boundary audit passes.

**Teacher runs stay blocked on one thing outside this implementation**: the Python version (section "Python" below).
It needs the user's answer. I will send the go message for 39/006 when it is settled.

## Artifacts reviewed (sha256)

All fifteen hashes in the request match the files on disk. `reports/teacher-boundary-amd64-reference-001.json` is
byte-identical to `reports/teacher-boundary.json` at `HEAD` (`830bc095...`).

## Checks

| Check | Result |
|---|---|
| Backend pin | The lock's arm64 `asset_sha256` (`ed0f1f54...`) equals the digest GitHub publishes for `codebase-memory-mcp-linux-arm64-portable.tar.gz` in release v0.12.1; the amd64 one equals its published digest too. The installed binary hashes to the lock's `binary_sha256` (`6a64e20e...`). The amd64 binary and top-level pin are unchanged. LICENSE and THIRD_PARTY_NOTICES.md are kept beside the arm64 binary. |
| Selection | `graph/validate.py` `backend()` reads the lock by `platform.machine()` and raises on an unknown machine. `runner.py` still refuses a checksum mismatch and mounts the selected binary and the lock file read-only. |
| Tests | I ran the suite with the pinned Codex first on PATH: 225 passed in 7.2 s. The two new tests cover selection, the preserved amd64 pin, an unknown machine and a corrupt binary. `git diff --check` clean. |
| graph_query | On packet 000074-001 a read query answers in 0.9 s; `MATCH (n) DELETE n` is refused. |
| Graph equivalence | In the two boundary reports all ten graph result hashes for positions 9 and 10 are equal, `graph_query` included. I compared the files myself: 42 checks each, 40 identical. |
| The two `git_show` differences | Not an architecture effect. The amd64 reference was committed on 2026-11-09 (`d86e7ea`) and `teacher/worker.py` has changed in three commits since, so the reference hashes describe older code. Direct test: I replayed every recorded tool call of six amd64 runs (70/001, 72/002, 73/001, 74/001, 39/005, 55/002) on this machine against their packets. 158 calls: `git_show` 26, `repo_read` 40, `repo_grep` 28, `hf_fetch` 25, `web_fetch` 15, `ancestor_read` 9, `run` 8, `safetensors_header` 5, `repo_list` 1, `evidence_index` 1. 157 are byte-identical to the recorded results, all 26 `git_show` among them. |
| Sandbox change | As reviewed in 001; `worker.py`, `codex_transport.py`, `author.py`, `audit_boundary.py`, `tests/test_author.py` are unchanged since. |

## Python

The one replayed call that differs is a `run` call in 55/002. Its last line was recorded as

    ungated list key: cannot use 'list' as a dict key (unhashable type: 'list')

and here it is

    ungated list key: unhashable type: 'list'

The first wording is Python 3.14's (I checked on a 3.14.4 interpreter); this machine has 3.12.3. So runs 2 to 74 were
made with a newer system Python than this VM has. Arithmetic and `struct` output replayed identically; the difference
seen is an exception message. Provenance records the architecture but not the Python version.

For the user, one of:

A. Move the walk to a VM whose system Python is 3.14 (Ubuntu 26.04 arm64 has 3.14.4), so `run` behaves as it did for
   2 to 74. My recommendation, because changing it later would leave three environments in one walk.
B. Stay on 3.12.3 and accept that `run` output can differ from the earlier runs in version-dependent details.

Under either answer, required before the first teacher run (small, no new request; I will check it in 39/006's
provenance): record the interpreter version (`platform.python_version()`) next to `machine_architecture` in run
provenance and in the boundary report.

## Not verified

- No live teacher run on arm64.
- The exact Python patch version of the amd64 machine. It is not recorded anywhere I can read.
- A `codex app-server` daemon at version 0.169.0 is running on this VM beside the pinned 0.167.0 CLI. The teacher
  transport starts its own 0.167.0 process and checks the version, so this should not reach teacher runs; I have not
  traced it further.

## Follow-ups (do not block)

1. Regenerate the boundary reference on amd64 with current code when that machine is next available, so the two
   reports compare like with like.
2. From 001: say whether "Unsupported runtime" means an unknown machine or a missing file.

## Next

Record this acceptance. Add the Python version field. Do not start 39/006 until I send the go message.
