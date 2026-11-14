# Implementation review: reference discovery 001

Reply-to thread: 01a1d636-5761-7593-8e19-f8453a562b16

Acts on the Required list in reviews/verdicts/commit-000072-001.md.
Please review the selection change alongside fresh unassisted 72/002. No change
to contract 8, guidance 5, salience-v2, or teacher tools/instructions. This is an
administrative discovery CLI replacing the ad hoc name-filtered scripts.

It enumerates all visible repositories of the official organization with pagination,
checks complete revision histories, and tests the latest pre-cutoff config for the
exact architecture string. It reports unavailable configs and never silently calls
them non-matches. Selection metadata contains only inspected pre-cutoff candidates.
Regression tests cover an unrelated repository name on a later page, newer-revision
exclusion, pinned architecture selection, and unavailable configs. Full suite:
223 host-enabled tests passed with pinned Codex 0.167.0.

GLM4: 154 enumerated repositories, six matching configs, 25 unavailable configs
(all HTTP 404 at the pinned config URL). The recovered six-model bundle has 94
objects, and the three Z1 revision pins independently match the verdict. The
original 72/001 bundle is preserved and still validates. Current visibility and
unavailable configs limit any exhaustive historical claim.

Earlier-selection audit: 1044 NVIDIA repositories enumerated;
4 readable matching configs, 0 additional matches relative to
39's bundle, 210 unavailable candidates. See the full report
for names and failure reasons. Initial audit hit rate limits; the final audit
reused successful pinned reads, used creation metadata to exclude repositories
created after cutoff, and retried failures with throttling/backoff. The original
name filter could omit candidates; no prior entry has been re-authored. Root
reference recovery uses fixed explicit mappings rather than that name filter.
Only 39 and 72 used the architecture-reference bundle mechanism.

Please assess whether any audit result warrants a separate user decision; do not
feed these administrative reports or review text to a teacher.

## SHA256

- reports/reference-discovery-implementation-001.json: `4cfea900ffb5a03e39e1363becb21415e54615d62a2b5eab40b9355ca9868018`
- teacher/reference_discovery.py: `a678bd7d3fa12201139c976e247d23a408c825583b06d6e6845c65fa9f30fa8c`
- tests/test_reference_discovery.py: `481d7263b7377dfed0528f0bbdc0d75af54888c7b09d61d91574e720d692a51c`
- teacher/README.md: `904719a6994d96b4a19da54f3b087870bfb92c03824781eef7e951bc6f175471`
- reports/reference-discovery-tests-001.txt: `4aee1b28e543c2da49108cf1f28bd2a7fec73491975f91f1704eb0143ebb07c7`
- reports/commit-000039-reference-discovery-audit-003.json: `9f3001a00cfd50c2c66b46a1b55ed9aff505b19b9a606e31746b309450f0287b`
- reports/commit-000072-reference-discovery-002.json: `307d46654960e874798064f61e28bd8714d3b618bd8747953fee958c9c663c4a`
- reports/commit-000072-reference-selection-002.json: `8cbf2aa69960fa871ec165077a04b83d3283b451cd14c1409048041e534bf986`
- reviews/verdicts/commit-000072-001.md: `1132dd92e88c238621c1791eac2b0551286bce395c2ec80c5759f4db7c5799a1`

Reply in `reviews/verdicts/reference-discovery-implementation-001.md`.
