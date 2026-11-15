# Implementation review: arm64 runtime 001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested scope: ancestor retrieval only; canonical and training remain false.
User authorized this implementation during the walk pause. No teacher run was started;
39/005 remains in force, 39/006 and commit 75 remain blocked pending your verdict.
The journal and pause ACK are preserved; this is not a walk restart.

Implemented the proposed runtime mounts, with the unresolved fork/vfork exception
restricted to aarch64. Future author provenance and boundary reports record the
machine architecture and OS. Existing authored artifacts are unchanged.

Full host-enabled suite: 223 tests passed on Linux aarch64 (7.540 seconds),
including provenance assertions. Execution required leaving the outer sandbox,
which otherwise prevents Bubblewrap NETLINK_ROUTE creation. git diff --check passed.

The separate historical boundary audit FAILED at packet 9 graph_query with
"Isolated tool exceeded wall-time budget". See the new architecture-bearing
boundary report; the old successful historical report was not overwritten.
Please assess this unresolved graph runtime limitation before authorizing runs.
The pinned x86-64 backend still requires Rosetta. No live Codex run was performed.

Fable authored the trial patch, so review of that patch is not independent;
the host-enabled tests provide the boundary checks. No draft or new packet exists
for this implementation request. No ledger changes are requested.

## SHA256

- teacher/runner.py: `d14b2c3610c8ad06dc1c8db636143612d343d42133ed8b74d6c08af112307af0`
- teacher/worker.py: `ee6bae2f3178b29770efdf33b3a634c3c0ad848c856eb8e69f39d762ea864e49`
- teacher/codex_transport.py: `474f4d635165a2c329a1c79c87a8869457b04790aa80a3062431ff14997d2ebf`
- teacher/author.py: `133de2e944f8356145cf466e9f21408cdf51533d672b00fb05269d4373cc5753`
- teacher/audit_boundary.py: `b6793e685fac37f2b27bbe9f8b5c42005e34de674169b5e9127c9c34b7508a97`
- tests/test_author.py: `85f193506d7160fcce1bcd892abc31bcdefd3d092fd8e1e0493354f803d40e35`
- reports/arm64-runtime-implementation-001.json: `9d36d2e7f79babe8fed6cae4d379fb8b4bb11d7ea12c2f6c8a045476639816c0`
- reports/arm64-runtime-boundary-001.json: `3b0c8b6dd71f65c30817c06db23e77c30ff7a80c8dddb2d073b448627526122a`
- reports/arm64-runtime-tests-001.txt: `77b3614c4c82f2e87274e36fbf769adfb99bdc5349e5a6fcd0433670416602e6`
- reviews/fable/ARM64-RUNTIME-PROPOSAL.md: `df44aa2cde6ac34950a6d4c50f892ae50d15b40bf30d4f295b369c50c3270dbb`
- reviews/fable/arm64-runtime-trial.patch: `b9eb110c862a6737563028c2e370dd74386a100b10e4874ff3e482c56a937b21`

Reply in `reviews/verdicts/arm64-runtime-implementation-001.md`.
