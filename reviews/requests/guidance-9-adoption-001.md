# Implementation request: guidance-9-adoption-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements reviews/verdicts/guidance-9-adoption.decision.md. Commit 199 completed under guidance 8 and is approved for ancestor retrieval only; its verdict was recorded with --approve. Next position is 200, with an explicit advancement pause pending acceptance of this request. No 200 packet or run exists.

The production change is one default: prepare() now writes guidance_version 9. GUIDANCE_9_ADDITION and the version-10 trial text are unchanged; teacher/session.py is untouched. The attached patch is relative to the pre-adoption working tree, excluding the already accepted trial gates. The existing compatibility test now asserts default 9 while retaining the version 5–10 instruction and evidence-integrity checks.

Verification compared complete opening messages, tools and reasoning effort against pre-edit snapshots for 12 real historical packets: one each at versions 5, 6, 7 and 8, all five version-9 trial packets, and all three version-10 trial packets. Every comparison was identical and every bundle validated. A freshly prepared fixture packet selects version 9 and validates. Its instructions equal guidance 8 plus the decision's exact paragraph E, and all non-system inputs remain unchanged. No provider was invoked; existing packets and authored outputs were not edited.

Full host-enabled suite: EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests — 280 tests passed in 30.387 seconds. The log includes ResourceWarnings about cleanup of an HTTPError 401; the suite completed with OK and exit 0. The standalone adoption verification also completed with exit 0.

Please review adoption for new walk packets beginning at 200 after acceptance. Version 10 is not adopted. Prior approvals remain ancestor retrieval only; canonical/training remain false. Trial outputs remain excluded from ancestor retrieval. After a few guidance-9 commits, a cost/effect comparison against 178–198 is owed; existing ledger obligations remain open.

## SHA256

- reviews/verdicts/guidance-9-adoption.decision.md: `46a059fe240b3c320ff1f7070b3e79902539a5eb843eaeff0a885d5a72ca5e7a`
- teacher/walk_inputs.py: `191d2b970f37cd62599caf4ffa1e5617797082c66912fe8d8b18efc7c885d8e9`
- teacher/session.py: `4386aff9144f995f6fe9bc58c6ad5b0006679938c4ae7ad62dc577fb2d4098a6`
- tests/test_walk_inputs.py: `9e1f80a8fd44310a3cb404a70b8129751eb5a83d4e2ae379cfc68782b4bf7c86`
- reports/guidance-9-adoption-001.patch: `bfeb2bd9efa2061147b683ab297b0b90af426ed05206a6c7833414beeb17a1f6`
- reports/guidance-9-adoption-before.json: `c4c84d2940a2a9eca32cedf5cecc45b832614b1dcbe0415e29c0624bdc4df838`
- reports/guidance-9-adoption-verify-001.py: `ab50cfc1093927363e2aa831d2806127f296dd6dac1713eaa70e09c90c42b588`
- reports/guidance-9-adoption-verification-001.json: `14d111d4a8080ee65b9b471588392ec14acd015a20b09cadcadc0187bf77afab`
- reports/guidance-9-adoption-tests-001.txt: `3e08072e42e176e3adb28d493180db358c500c6111aa973c7dcdf04c13dd8264`
- reviews/verdicts/commit-000199-001.md: `410eef43e62b587e6fc615081f9365ddbe1b130218fa9106d5aea72a7070cb45`
