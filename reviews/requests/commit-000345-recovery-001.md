# Failure handoff for commit 345

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Run `.teacher/runs/commit-000345-001`. Packet `.teacher/retrieval/000345-001`. Upstream `c3049627ea2cdbe7f0c8e62e2491e4eed8d37072` — “LlamaForCausalLM: Use FP32 intermediate dtype” (copied from Git).

Validation refused both finals for `Unknown or unsuccessful evidence call`. The first final (row 144, 16,646 bytes) cited the same absent ID twice. This was the first live v3 repair. Its 230-byte feedback named `chapters[0].claims[1].evidence[3]` and `call_38549430cfc44212bdb2403c3c362e` and asked the teacher to correct only that issue. The repair made one successful `repo_grep` call and replaced that citation. The second occurrence at `chapters[0].claims[3].evidence[5]` survived in the repair final (row 149, 16,648 bytes), so validation refused it. Rows are zero-based. Provider totals for both turns are 6,496,427 input tokens (6,343,552 cached) and 14,526 output tokens. The failure diagnostic recorded zero provider error events.

345 ran ahead of 344. The packet included 340 of 341 strict ancestor entries and used 344 parent source without its prose. The changed paths do not overlap. The queue is stopped at 345 with no active session and no published draft.

Please review one fresh unassisted 345/002 with the normal packet builder, the same cutoff and pinned evidence, and current approved ancestors through 344. Keep contract 8, guidance 12 and gpt-6.2-sol medium. Preserve 345/001 and keep this handoff out of teacher input. Any resulting entry would have ancestor retrieval scope only.

For separate review, the three 344 ledger candidates are the suspected Ernie old-name correction-bias preservation change r001 and the persistence observations for all-expert fused capacity r016 and fused output dtype r007.

## SHA256

- reports/run-ahead-detached-000345-e4f1d3db4be048168965b9a71fae2437.json: `57a85272b4277c6c6146b26333237eb5f69a15105899d623b18d5602f9e6ef3b`
- reports/run-ahead-detached-000345-e4f1d3db4be048168965b9a71fae2437.log: `fade15136d4dddb944936e2b28f6463db2db8b6fb8a98f95522a7d246193d155`
- .teacher/admin/run-ahead/8d0a4b6fd35446e084a91f030cfe629f.log: `4eeea015c41344d749789bca0de6ccb7453d5f773be693734bed1cd3b2680f88`
- .teacher/admin/run-ahead/8d0a4b6fd35446e084a91f030cfe629f.json: `34b345ebaee50200779656fce3745d2b81d14803198b36d2c8fb7ebd17f31b17`
- reports/commit-000345-catalog-selection-001.json: `f14e12ff6d39c7940a8be043447188af8cee18069697a38e2508f3a9bcfd6434`
- .teacher/retrieval/000345-001/manifest.json: `cdf3597ecfe8d8c9219939ee52711d10bba4c80cde4eb0e0259a5935fa8939cf`
- .teacher/runs/commit-000345-001/status.json: `5c9212a8a1ae15548ed79fbbc877ae1904c6dec5e5a3e65ebfa40bd2a195696e`
- .teacher/runs/commit-000345-001/provenance.json: `b06742a2421b406f4e5acda1b80b083199513b705de495294c26621278568d74`
- .teacher/runs/commit-000345-001/raw-transcript.json: `dbc955cf93c208746ec0d1d4432c9acf4379dbef120fca197b1120cb922dd707`
- .teacher/runs/commit-000345-001/codex-failure.json: `366940c14ea3da75364c26d785288d58c5c154842fe2374bae3826aae6b2579b`
- reports/commit-000344-ledger-001.json: `29976279c6e6a82089b62070565be823bd55fa2d7bb1e3b7e095eecb6fb6e7ce`
- reports/defect-ledger/exllamav3-ernie-old-name-correction-not-preserved--r001.json: `d601024419863207442e62d658dc22df636cb8de897fad4f476a38a04d4988a1`
- reports/defect-ledger/exllamav3-all-expert-fused-shape--r016.json: `1c74f04992fa4b394a8c4520a096910f419ad6a48083645aafa087bee9c711a1`
- reports/defect-ledger/exllamav3-fused-output-dtype-override--r007.json: `e32e68099e0ce2d17dbf665209d93ed183abfa1c58dd9c99a1d0d96f2d63f017`
