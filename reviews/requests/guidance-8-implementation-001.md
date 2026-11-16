# Implementation request: guidance-8-implementation-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements reviews/verdicts/guidance-8-trial.decision.md as a trial gate only. Guidance 7 remains the walk default. Commit 175 completed and passed its original implementation-hash validation before this patch was applied; its request is filed at reviews/requests/commit-000175-001.md. No advancement pause has been set.

FreshSession appends the exact approved fourth paragraph after guidance 7 when guidance_version >= 8. Contract-8 validation now accepts version 8 alongside 5, 6 and 7. The default remains 7; versions 5 and 6 retain their respective text. No reviewer trial criteria enter teacher instructions. The patch is relative to the immediately preceding implementation.

The administrative verification script compares the actual 174 version-7 packet against its pre-edit snapshot: system instructions, full opening, tools and reasoning effort are byte-identical. Earlier version-5 and version-6 snapshots also match. A temporary hardlinked packet copy, with its manifest unlinked before editing, validates at version 8 and changes only the appended system paragraph. That paragraph equals the decision verbatim, including line breaks. Original packets and runs were not modified; verification invoked no teacher/provider.

Required host-enabled suite: EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests — all 280 tests pass in 24.418 seconds (ResourceWarnings, no failures). The fixture checks the unchanged default, accepted version 8, exact append-only instructions and unchanged non-system inputs.

Please review the trial gate. After acceptance, four fresh unassisted sessions at 154, 140, 157 and 156 will use the approved runs' cutoff evidence under .teacher/trials/, between walk commits. No coverage requests, verdicts or ledger material will be supplied. Outputs will remain unpublished, unapproved, absent from journal attempts and ancestor retrieval; guidance-8-trial-001 will include drafts, transcripts, coverage and tool/token counts. Adoption requires a later user decision. This request does not pause the guidance-7 walk.

## SHA256

- reviews/verdicts/guidance-8-trial.decision.md: `941c51728fcf206d1757fbb943fdeaf852919139f9d2718caeaac37e2bef97b5`
- teacher/session.py: `f546b0e0407b47104c32d5e45f3e9951fc0136713d95147f0ce4c1ac42cd9f5f`
- teacher/walk_inputs.py: `8e429f04d7a3ce6b6f29b33ee3c1650dd15360f504ed1dfc84e0b77efb7246e9`
- tests/test_walk_inputs.py: `a508ea0e8e79a7b1fca2a62a90be0177e6a239c65a93d3bc1ee19a3b95c1ce1f`
- reports/guidance-8-implementation-001.patch: `564cb7a14d093cbc7e51ae32afb037e08894a89828ba56b819017d49f1defb5b`
- reports/guidance-8-implementation-001.json: `9892fcebd7c0f5d27bbad7ec55f6eadf9fa9424e43423177af9d75498e4b28ba`
- reports/guidance-8-verify-001.py: `ae54fdae943c86e1fc26cecb48f4ded14a4c18aa1f835a73203468d9cc8957f2`
- reports/guidance-8-v7-before.json: `34a355569e30030ce8529f9c5c77ec35f266e719e931fc2f992b335a86c43368`
- reports/guidance-8-staging-001.json: `db170ec427061bb4334ede7c054a98c9ed0a8c1b95a7323f8379c633aa59f628`
- reports/guidance-8-tests-001.txt: `8e7bfd09d1e7a5f0e7450a776320383c3d18b3583b969befa679bbc344ca9e78`
