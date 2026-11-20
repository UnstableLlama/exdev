# Review request for Codex output schema

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Please review the staged patch. The provider refused the 336/003 schema at compile time with `invalid_json_schema` and `regex construction fuel exhausted`. The candidate removes only the packet-dependent commit-hash enums from `links.items` and `findings.items.properties.locations.items.properties.commit` in both Codex `turn/start` requests. It preserves the 40-hex patterns, all other constraints, and `links.maxItems = 0` for packets with no approved links. The model, prompts, tools, packets and guidance remain unchanged.

For both 336 packets the candidate `outputSchema` serializes to **5,433 bytes** using the app-server transport's JSON encoding, down from 34,669 bytes for 336/001 and 34,713 bytes for the packet reused by 336/003. These sizes count the schema value alone. The checks report includes the manifest and candidate schema digests. Provider acceptance still needs a separately authorized live attempt.

`validate_annotation` still builds the full schema from the manifest. The transport tests submit a well-formed unknown hash in each field, observe the local refusal and existing repair turn, and replay the corrected result. Schema equality tests cover versions 2–5, empty and nonempty links, and chapter constraints. The isolated host-enabled suite passed all **355 tests**. The candidate also reproduced 335/001's saved draft and Markdown through annotation replay. `git apply --check` passed against the live baseline.

Run provenance identifies the schema construction inputs through `packet_manifest_sha256` and the adapter and base schema file digests in `implementation_sha256`. The adapter digest changes with this patch. Existing run provenance and replay checks do not hash or compare the outbound schema bytes. Replay checks the saved annotation and repair against the full schema and manifest. The outbound schema digest in the checks report is an offline measurement.

The queue is stopped at 336 with no active session. Application and any further attempt await review and the user's answer.

## Artifact bindings

- reviews/verdicts/commit-000336-repeated-failure-002.md with SHA-256 `a7e3a260364c80114c740624358c9d1c8263c2110dd17f6fe68ed647c564caf0`
- reviews/requests/commit-000336-repeated-failure-002.md with SHA-256 `e55b3788a73a0f4373a15fcb9f15627fa64c67cd4570264fbcc468697936da2c`
- reports/codex-output-schema-implementation-001.patch with SHA-256 `adcf1f27015b62ad90cf8368fac91c62c1be98733d283f5d71616470cfb91287`
- reports/codex-output-schema-implementation-001.hashes.json with SHA-256 `93ccfd8127eb3fda07359be9cc15793f921f14c57321eedbdde79dd14f67bfe9`
- reports/codex-output-schema-implementation-001-checks.json with SHA-256 `1c32a48788996de5dc51e658a23ef2694a16c9b3e5c026dbfd8ee9acc399cb67`
- reports/codex-output-schema-implementation-001-suite.log with SHA-256 `5efdee414bfb422b7cf91d9a0951551e56ae38f094b07948298e6930a9850273`
