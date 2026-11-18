# Implementation request: guidance-12-adoption-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Author/orchestrator: gpt-6.1-sol / medium. Production teacher remains gpt-6.1-sol / medium.

Commit248 finished under guidance11 and its request is filed; its verdict is pending. An explicit journal advancement pause prevents any further teacher session until this adoption is accepted. No249 or replacement has started.

The only production change is prepare() writing guidance_version12 for new packets. The attached patch is relative to the pre-adoption working tree, excluding accepted trial-gate changes. teacher/session.py is byte-identical to the accepted guidance12 implementation (SHA256 698c6a564df6457ba3fac71c72de0824867695f0dc07b555be9d3ba8dafb4a63), preserving all version branches and the exact trialled paragraph F. The existing compatibility test now compares the default with version12 and retains historical-version checks.

Complete opening messages, tools and reasoning effort reproduce identically for26 historical packets spanning versions5–12, including all six guidance12 trial packets and248. All26 bundles validate. A freshly prepared fixture selects12 and validates; its system instructions equal guidance9 plus the adoption decision's exact paragraph F. Non-system inputs, tools and effort remain identical. No historical packet/run was edited and no teacher/provider invoked by verification. The snapshot, verification script and result are bound below.

Full host-enabled suite: EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests — 287 tests in54.979s, OK, exit0. Non-failing HTTPError401 cleanup ResourceWarnings appear in the log.

Please accept the default from249, subject to248 approval. After acceptance, the replacement pause ends: fresh110 (110/002 remains declined), then141,158,164,213,214,225,234, one at a time on Sol/medium/guidance12 under the accepted plan.72/003,98/002,103/002 stand. Cross-checkpoint comparisons remain reviewer work. Canonical/training flags remain false; trial outputs stay excluded from ancestor retrieval.

## SHA256

- reviews/verdicts/guidance-12-adoption.decision.md: `6743ea4d2b4ed2021f12297884fd2ef1de46783483429e62e2d436056a2fc748`
- teacher/walk_inputs.py: `8b7ee5628711f6fbca4d7338694ec2e7dbed0e160690546623dbb16c393646b4`
- teacher/session.py: `698c6a564df6457ba3fac71c72de0824867695f0dc07b555be9d3ba8dafb4a63`
- tests/test_walk_inputs.py: `6f16a9dacc4a6775be1bb50952c9d731b954c4d52c5173746030d8f1a2a40a65`
- reports/guidance-12-adoption-001.patch: `6fff3762c31660824636cd9967ae2bc33150f31d45581c55a5cbcfc4b55343ac`
- reports/guidance-12-adoption-before.json: `edde7fc3c41402501c9f3d625bfba20e4f8d8babb2991bda496f8651538784b1`
- reports/guidance-12-adoption-verify-001.py: `b13dfb47fac6354138f87ee5fc024a231bbf85b740ab91e0c8fb48b6a74caf1c`
- reports/guidance-12-adoption-verification-001.json: `53ab7e8fd6469b28bfe8bf93df538d87f222a0a87a5fd06b6f8e002ef1b23efe`
- reports/guidance-12-adoption-tests-001.txt: `25f63f4ff8d0e6af7634a863145f1224966dbc310333b118e21cb5c0e835ee36`
- reviews/requests/commit-000248-001.md: `65507220136b4dc4714bf36cee5f7f6167db07831dd4b76ef463bde7bc901563`
