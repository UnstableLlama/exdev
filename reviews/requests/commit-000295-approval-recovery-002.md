# Approval recovery 002: restricted replay capability failure

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested scope: administrative recovery; ancestor retrieval only. Canonical and training remain false.

The exact format recovery authorized by approval-recovery-001 is applied: both backups were retained, the candidate request replaced the published request, only its matching queue request_sha256 was rebound, and unchanged check_verdict passed. The five ledger records are accepted.

The subsequent unchanged queue approve command for .teacher/runs/commit-000295-003 stopped in tool replay with `ValueError: Tool replay mismatch: call_95c8a3e34cd04a39b9905b1bab39d6d0`. A read-only replay of that single git_show call in the restricted sandbox identifies the cause: `Isolated worker failed: bwrap: loopback: Failed to create NETLINK_ROUTE socket: Operation not permitted`. The transcript recorded a successful source diff. The attached diagnostic preserves the call, expected result and actual failure.

Neither approval is recorded. Journal remains stopped_recovery, next_position 297, active_session null; 295/003 and 296/001 remain pending_full_review. No teacher was started, and no teacher, packet or orchestration code was edited. The prior independently host-enabled replay matched all 39 calls, as reported in the published request. This new restricted invocation could not reproduce that environment.

Please authorize retrying the unchanged queue approval commands with host permissions so bubblewrap can establish its isolated environment, recording 295 first and 296 second. Preserve the applied format recovery and every run/packet byte. If checks pass, clear the retry stop against the 295 approval verdict and resume 297 under the accepted rules. If another check fails, stop and report. No validator bypass, rule change, rerun or annotation edit is proposed. No implementation change; latest accepted suite remains 332 tests.

## SHA-256 bindings

- reports/commit-000295-approval-recovery-002.json: `d25f9bbcf2cdd4f9bf0bc3c70626fbef7daa9ce215bdf22eeba908fa00bad72d`
- reports/commit-000295-approval-recovery-001.applied.json: `a7c14e0a4202ab4ed4114872f3343b0aace47e733b3532d5079ac34a7a1cbac3`
- reviews/verdicts/commit-000295-approval-recovery-001.md: `1b26561ab51690c8f542fba006fe4438f49edd845be4faacb5c7a756d69b6171`
- reviews/requests/commit-000295-003.md: `31e834e7819e30e25237041bb6b5f0d56bd186a51be18c77b498b64a0443da7d`
- reviews/verdicts/commit-000295-003.md: `92ab6acfa2b48dc08d2855db320f5f87dd433624dc1343796a3e25a3a13439d7`
- reviews/verdicts/commit-000296-001.md: `497de6d68e18804f630e005b6d8d5e0e19fd2fc6f968c1f0125ff6e9d1344d5e`
- .teacher/runs/commit-000295-003/draft.json: `f0d63294d3ebc77c2d5ea87836ce8d0c31dba31f2f462b56cc355ac87ca9ddb6`
- .teacher/runs/commit-000295-003/draft.md: `10beea7e34fff87271f0e2d6b15ef4bc4a553f2982a460854d1e6a79117b81ae`
- .teacher/runs/commit-000295-003/raw-transcript.json: `1a862a9ecff4e88378cc8ef13b8ef7902051f066c3c0c9b0fe8c3afaf4154303`
- .teacher/runs/commit-000295-003/provenance.json: `3182b90eb1f991978f82805425a7168e4084cb4b21d1ac5a165563bdcc62450c`
- .teacher/runs/commit-000296-001/draft.json: `f18f5cc759a2b6ba6978ea6c1b27473126f52f4cd48068dfededb906e34a9e7d`
- .teacher/runs/commit-000296-001/draft.md: `8da920a503e73d885623f9914dcb2e9ac2bdabb3a777939f514214396bbb0784`
- .teacher/runs/commit-000296-001/raw-transcript.json: `7c8ff92d4f7cc42655180f65e13a717a25004529d5d27b41eaf2fff47fc836a3`
- .teacher/runs/commit-000296-001/provenance.json: `a93ff01a8352ec29369ec075eafdba4d15ba9be82f3e07d2c888e6345bdf47b6`
- .teacher/retrieval/000295-003/manifest.json: `b75e545c21f61d634e7a274fb61bf0c09d1c1e6773f29ca50d668d99b3796b01`
- .teacher/retrieval/000296-001/manifest.json: `640fb1540a00ac33297051629f03e2a8f21c8df17f8331dfb9cf10ee134bff12`
