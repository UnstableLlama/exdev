# Failure handoff for commit 346

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Run `.teacher/runs/commit-000346-001`. Packet `.teacher/retrieval/000346-001`. Upstream `67e0fd74413228c85e1edc65cfc7c39365b1a6ca` — “TP: Refactor/fix auto allocation” (copied from Git).

The first final (transcript row 116, 26,860 bytes) failed on an absent citation at `source_notes[2].evidence[2]`. The 226-byte v3 feedback identified that citation. The teacher removed it without making any tool calls or changing other annotation fields. Validation then rejected the repair final (row 119, 26,819 bytes) because `findings[6].verification[0]` uses `source_inspection` and cites only three `run` results. The finding’s verification references were identical in both finals. Transcript rows are zero-based. Provider totals were 2,928,286 input tokens (2,832,640 cached) and 18,994 output tokens across the two turns. The redacted failure diagnostic recorded zero provider error events.

The packet covered all 342 strict ancestor entries. The run did not run ahead of any position. Salience v3 selected 8 of 8 qualifying rows, including all 7 path-only rows, with no truncation. The queue stopped at 346 with no active session and no published draft.

Please review authorization for one fresh unassisted 346/002 using the normal packet builder, unchanged cutoff and pinned evidence, and approved ancestors through 345. Preserve 346/001 and keep this handoff out of teacher input. Any resulting entry would be for ancestor retrieval only.

For separate review, the two 345 ledger candidates are activation odd-tail r006 and Mistral sliding-window omission r001. Both are suspected carried observations.

## SHA256

- reports/run-ahead-detached-000346-7a711d334f67424b90788f3fba4f856d.json: `c40dbb453798a6b81b9cf57f0e600d84bde9f9412c911df956fc44869a1c4ed4`
- reports/run-ahead-detached-000346-7a711d334f67424b90788f3fba4f856d.log: `80cdf055e9e90027da1b5cd101073da1a99c5e2d57bfe24b81fb19d6c9073564`
- .teacher/admin/run-ahead/2dd6a88adfee4c63ac47f587ad6b4b9d.log: `782d1fa2d63ba2ad0d9ac4fdc9509897a4cf9a87d8ec296bfda89319aa6c6d8e`
- .teacher/admin/run-ahead/2dd6a88adfee4c63ac47f587ad6b4b9d.json: `da01c79749f3a6902356f1cd972f2fde7df35da24b63fb3e17fa46dbe75283df`
- reports/commit-000346-catalog-selection-001.json: `e4cc5f728dcac993a255ee70fefca1109661b3b9f788bf0378699b488a085089`
- .teacher/retrieval/000346-001/manifest.json: `0bde98440836a31ce9bb253acc46cbd54cad3140f1fa37150f8b5dea29939ed7`
- .teacher/runs/commit-000346-001/status.json: `5c9212a8a1ae15548ed79fbbc877ae1904c6dec5e5a3e65ebfa40bd2a195696e`
- .teacher/runs/commit-000346-001/provenance.json: `aac3d7518a226d2c2ea40b17b09f7d26e209e800d02042e7aca62d4fdc89be19`
- .teacher/runs/commit-000346-001/raw-transcript.json: `45c09ef8079eb56973a97693a3b62beaa69cacefae538730bf57e948189c3305`
- .teacher/runs/commit-000346-001/codex-failure.json: `47170bd67dd28ec4d4419bef2cca448834b22bb248771f4a9b2260bf9f541c9f`
- reports/commit-000345-ledger-001.json: `733557c54f4d20b5f2a1c84b32e7e131d9e68787a9d2243688c549d2092861b2`
- reports/defect-ledger/exllamav3-activation-odd-tail--r006.json: `26830a472c09a53249c50cb7249a06db6f778d4a681005d1fbe8ca360782b2a6`
- reports/defect-ledger/exllamav3-mistral-sliding-window-omission--r001.json: `e7c1cb3b3eb938289c35b77b3ca126b59a62af6ad6bbd27fc78b38bd75dccab9`
