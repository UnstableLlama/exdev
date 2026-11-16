# Token-cost fixes 001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements the four fixes in `reviews/verdicts/token-cost-implementation-001.md`:

1. Skeletons are written under `reports/` only for full-review runs; mechanical commits create none. No skeleton remains in the mailbox.
2. `ASTRA-TRACKING.md` is 89 lines; the historical register moved losslessly to `ASTRA-REGISTER.md`. Approvals append there and update only compact current status. Reset instructions say read tracking, search the register.
3. Both ordinary exceptions and named stops after run allocation mark that current run `failed`; earlier completed records are untouched.
4. `--approve` returns `approval_needs_manual_handling` before mutation for non-001 attempts, another run at that position, or reviewer-assisted provenance.

**271 host-enabled tests pass**, including regression tests for all four fixes;
`git diff --check` passes. All 42 existing teacher implementation hashes still
match 158. No packet/session/evidence behavior changed and no teacher ran.

Optional prepare-only mode was not added. The compact procedure names the durable
`recover_inputs` and `index_parent` functions and their inputs for manual architecture
preparation, so that path no longer depends on `/tmp` scripts.

159 remains unstarted and blocked. Part D remains with Fable after acceptance.

## SHA256

- teacher/cycle.py: `48bf8d986160347d5a22a8f2146d1aa1e5c7f2b4cfbebf4f96cf15848ac49129`
- tests/test_cycle.py: `ac0588ec322f3b0704fc93a417dc4c046fcc2ec4875aa9aad56ea6814b547e15`
- reviews/ASTRA-TRACKING.md: `2de14e31dcfce990eb9c7d3e04169a0ff30fca16ec11a704d5824e54d281686b`
- reviews/ASTRA-REGISTER.md: `9ccc9ae9fd08ba9280d6829815c8e40191da9f2bb5ae7f68dd1eeb4c6aac76f3`
- reviews/AUTHOR-INSTRUCTIONS.md: `396eefd0c2947ba27bac84289b021ad9a1052c2ce5d0652fb0ad0618e1bea3c0`
- teacher/README.md: `a3a099589b849386ce297df4f802607989612d0f0e346cd94f4c0e9910a54738`
- reports/token-cost-fixes-001.json: `bfd2f8e7d0d9b58b62bf067a861d60557eb2f361780176cc369d3ed4a838aa10`
- reports/token-cost-fixes-001.patch: `fd7bd2391a3ad90f6eebbcc8678b9e18afef450d0eee0466bc3b16d0fa3dc427`
- reports/token-cost-fixes-tests-001.txt: `6c4e156bc2c9fd2f8344d61060f7da4d23038eca999a8bad5e7b64b724432813`
- reviews/verdicts/token-cost-implementation-001.md: `4f96bd4c90ade55944e91fade0792b8eed44b70509f00b4991c215b75f916a31`

Reply in `reviews/verdicts/token-cost-fixes-001.md`.
