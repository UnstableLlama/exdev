# Implementation review: arm64 runtime 002

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested scope: ancestor retrieval only; canonical and training remain false.
Acts on reviews/verdicts/arm64-graph-backend.decision.md following HELD request 001.
Covers both the sandbox change reviewed in 001 and the native graph backend.

Downloaded the official v0.12.1 arm64 portable archive from
https://github.com/DeusData/codebase-memory-mcp/releases/download/v0.12.1/codebase-memory-mcp-linux-arm64-portable.tar.gz.
Archive and binary SHA256 are pinned beside the unchanged amd64 pin in
 graph/backend.lock.json. Installed under .tools/cbm-v0.12.1-arm64, retaining
LICENSE and THIRD_PARTY_NOTICES.md. Runtime selection uses platform.machine();
unsupported machines and binary checksum mismatches fail closed. The sandbox
mounts the selected binary and lock file. No Rosetta dependency for native queries.

The host-enabled full suite passed 225 tests. New tests cover native selection,
legacy pin preservation, unsupported machines and rejection of a corrupt binary.
The administrative boundary audit passed all 42 checks on Linux aarch64.
Every graph result hash for positions 9 and 10 equals the original amd64 report,
including graph_query on the same prepared snapshots. The original report is
preserved byte-for-byte as teacher-boundary-amd64-reference-001.json.
Two non-graph git_show result hashes differ; the implementation report lists both
pairs. Cause is not established because the reference contains hashes, not bodies.
The reference was not adjusted. Please assess this discrepancy explicitly.

No live teacher run, new draft, packet, or ledger change. Historical authored runs
and journal remain unchanged. 39/006 and commit 75 stay blocked pending verdict.
Fable authored the initial sandbox trial; that part of review is not independent.

## SHA256

- graph/backend.lock.json: `c47eacd116ec7bec9203c5011bcb91c4efa820ffe1b2ea1c22e4eb0f37af3ef7`
- graph/validate.py: `07d710c915db5b42fb14b05836b0efd42544deccec62c9a4d52d80c5efd10f6c`
- graph/README.md: `db632762814c34b66c38ceddf5b4f08914ba72bc0b29f0473ffde9fd765103cb`
- teacher/runner.py: `163c51faa4b94fc1a45c5f6e3b0d649a8e46faef82d1b3897230a4632f7225d5`
- teacher/worker.py: `ee6bae2f3178b29770efdf33b3a634c3c0ad848c856eb8e69f39d762ea864e49`
- teacher/codex_transport.py: `474f4d635165a2c329a1c79c87a8869457b04790aa80a3062431ff14997d2ebf`
- teacher/author.py: `133de2e944f8356145cf466e9f21408cdf51533d672b00fb05269d4373cc5753`
- teacher/audit_boundary.py: `b6793e685fac37f2b27bbe9f8b5c42005e34de674169b5e9127c9c34b7508a97`
- tests/test_author.py: `85f193506d7160fcce1bcd892abc31bcdefd3d092fd8e1e0493354f803d40e35`
- tests/test_backend_runtime.py: `24a57d9be7f7a1bfb93b861279e9d6d43051daeac897e8cffc19ef868c0400fa`
- reports/arm64-runtime-tests-002.txt: `a8c5fa0066fb525497924484abda3fd15e3c893259a5a12cc6333d7eca3674d8`
- reports/arm64-runtime-implementation-002.json: `be28858b3ca4c96a7611ba91ef09c0dd71297513c83479199c410c82bb3e517a`
- reports/teacher-boundary.json: `1e6ebd4de32f7f834d26049eb1e4d6ae3413c826214794d3cf99f0cc5d06b74a`
- reports/teacher-boundary-amd64-reference-001.json: `830bc095000fddce8919c05d691ebf70551fb2b14f14206ff56e1a73b7d97179`
- reviews/verdicts/arm64-graph-backend.decision.md: `68caf4b9f449e7ac56072eb7b51d59b4b5865103026d4107f5edd6ddc45b5b9e`

Reply in `reviews/verdicts/arm64-runtime-implementation-002.md`.
