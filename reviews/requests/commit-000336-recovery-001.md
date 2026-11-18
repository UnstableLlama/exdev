# Failure handoff for commit 336

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Run `.teacher/runs/commit-000336-001`, packet `.teacher/retrieval/000336-001`. Upstream `37f80fb98cf6247f9da12d9b942253f38f6dbd82` — "Fix typo" (copied from Git).

The Codex app server emitted an error during authoring. The adapter raised `Codex reported an authoring error` and discarded the event payload, so the underlying cause and token usage are unavailable. The transcript contains only the system and user inputs. No tool calls, final, validation repair, or draft were recorded.

The queue is stopped at 336 and the active session has cleared. Please review one fresh unassisted 336/002 using the normal packet builder and the same cutoff, approved ancestor snapshot, pinned evidence, contract 8, guidance 12, and gpt-6.2-sol medium. Preserve 336/001 and keep this handoff out of teacher input.

## SHA256

- reports/run-ahead-detached-000336-f2c821ee320a493a85cec6d4731ac5ee.json: `070dd44f51d7b8ee4847c22872f493c591d15d1ccf2e50044d28e4aaefce539f`
- reports/run-ahead-detached-000336-f2c821ee320a493a85cec6d4731ac5ee.log: `994d8bba92aab1f1532a8c3eb426ebb6de11dcb0c25fa0da1638c0fa588819e8`
- .teacher/admin/run-ahead/87b81b77b0fb4df7912b65725c305ec9.log: `815229ae0937e8ff86e58b3bf7330073607570cb2d284ce8a72e83ab2b1256ea`
- .teacher/admin/run-ahead/87b81b77b0fb4df7912b65725c305ec9.json: `3dce2436605eafd15790d29ef0e68d28467d42fe624ff2f27c98ba3d83b5cbcf`
- reports/commit-000336-catalog-selection-001.json: `929fa8624e183a34b17c8326e273606de36c706b604181beeae407bd23380315`
- .teacher/retrieval/000336-001/manifest.json: `6cd5bf6f112969a7030e94b173d48350f7e713ec19c1205afd0ee1362b8f8ebe`
- .teacher/runs/commit-000336-001/status.json: `5c9212a8a1ae15548ed79fbbc877ae1904c6dec5e5a3e65ebfa40bd2a195696e`
- .teacher/runs/commit-000336-001/provenance.json: `25611355bb5ad8cfe53c1082f0400513fe6f352e9345815c88e2aa91e277b67e`
- .teacher/runs/commit-000336-001/raw-transcript.json: `aca14bb94a176dcd88c9c830edbcca694f123f20ac77abc6acf7afbde669f45b`
