# Review request for Codex failure diagnostics

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Please review the staged patch. The queue remains stopped at 336 with no active session. The patch is staged for review only. A further 336 attempt requires the user's authorization.

- When Codex execution fails, the transport retains JSON-RPC error notifications and error replies, including setup failures. It collects app-server stderr after child exit and before the temporary state is removed. The author writes the redacted values to `codex-failure.json` in the failed run directory with mode 0600. The artifact is ignored by Git and stays outside the transcript, provenance, and retrieval artifacts.
- Redaction covers credential values from the initial and refreshed auth documents, including URL-encoded and JSON-escaped forms. It also filters recognizable credential fields, authorization and cookie headers, key and token formats, and URL userinfo. If safe capture fails, the artifact records that diagnostics are unavailable. Collection retains up to eight error envelopes and 64 KiB of raw error data. Stderr above 64 KiB is omitted in full to avoid saving cut credentials. Omission is explicit.
- Error handling still raises the original authoring or transport exception. The patch preserves the model, prompts, packet, and success artifacts. Existing failed runs cannot be backfilled because the original payloads and stderr were discarded.
- The host-enabled suite passed all 353 tests in the isolated copy. The new synthetic stdio tests cover the authoring notification, setup error reply, initial and refreshed credential redaction, oversized input handling, and fail-closed behavior. The patch passes `git apply --check` against the live baseline.

## Artifact bindings

- reviews/verdicts/commit-000336-repeated-failure-001.md with SHA-256 `f4362a06fea11ce88a17f78c52f5333d3e21d285ecb25ca4fe8b124192535b12`
- reviews/requests/commit-000336-repeated-failure-001.md with SHA-256 `092e13683cafbcca5c1db45e2291dea28413403fddac23c37003b9414a247fc6`
- reports/codex-failure-diagnostics-implementation-001.patch with SHA-256 `b21542fd53f4b6cd912456a091403791c88efd21f9719802bad0c06011574596`
- reports/codex-failure-diagnostics-implementation-001.hashes.json with SHA-256 `3f30628bee44866ba98a18a5783bb50e5fdba1da8c524334f521f5932249329c`
- reports/codex-failure-diagnostics-implementation-001-suite.log with SHA-256 `535130a9590bac55b79b814b69f578c4d25184506a2ce56f7bc89afaa0fe11bf`
