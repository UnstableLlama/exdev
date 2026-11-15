# Implementation request: reference absence 001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested scope: ancestor retrieval only. Canonical and training remain false.
Acts on commit-000039-reference-scope.md, item 3, under the explicit restart.
That item requires an implementation request for the validator change.

Startup validation on exdev-314: 225 tests passed and boundary audit passed on
Linux aarch64 / Python 3.14.4. Pause archived in reviews/archive/pause-2026-11-13.json.
The walk remains at position 75; 39/005 stays in force.

Reference-only recovery now records published file paths and distinguishes absent
roles from download failures. A new complete_with_absences status requires config,
no failures, exact missing/absent sets, a reason, and a pinned-tree file inventory
that does not contain the claimed absent roles. Published unreadable files remain
blocking. Legacy complete bundles and root recovery keep their old requirements.
The inventory comes from the existing fully paginated pinned tree recovery; it is
trusted curator data, not an independent authenticity proof.

226 host-enabled tests passed, including absent versus failed retrieval and
validator rejection of contradictory tree evidence and reported failures.
The six-model Deci bundle validates with explicit GGUF absences; the original is
preserved. The four NVIDIA references are untouched. No teacher run started.
Please review this prerequisite before unassisted 39/006; no coverage request
will be supplied. Commit 75 waits for the replacement's full review.

## SHA256

- teacher/root_evidence.py: `cb7facb4c1915feca0bbe18b747bae63da7408e1eab0ea9bd9ef8f537ef8770b`
- teacher/architecture_evidence.py: `6ebc7024e2584c375f264dd6b194db39a65744765af47abac37808a8b1e564cf`
- tests/test_architecture_evidence.py: `85d03bab27b1b1406767d525c8688bc7ec7949068d1a0de6fba29a9d1280de53`
- reports/reference-absence-tests-001.txt: `e7057a7fa95c7ba30b02eb63bf59637f02daba2a52b7a65ab39381998f162ef1`
- reports/exdev-314-tests-001.txt: `a7216a13b3e122c173d71c3c581dfa2c383acc1211403c3df511e7ff90304444`
- reports/teacher-boundary.json: `455898d200e8de63f72f48ea206c15e69ee754844636f81a2f3c47572aa828e6`
- data/evidence/commit-000039-006/deci-references.json: `cb7f3a23544fe2e46c24a82e29b8e74a9cbc97bd9d7de3fa388bc53d00164f8c`
- data/evidence/commit-000039-006/deci-references-with-absences.json: `87f3eba62d827cb583fd6772153ed6fe81b67f5e5fc0207d86108c173441c7f3`
- data/evidence/hf/commit-000039-006/DeciLMForCausalLM-tree.json: `e8c149dc1ac7b54c485724edc976260d60f3d1f326ca02bd6b37be4026950f60`
- reviews/verdicts/commit-000039-reference-scope.md: `13d5292442f83a58e76fde0320e4dbbfc2c74260bee0074f2ca2878f05e6700d`
- reports/reference-absence-implementation-001.json: `bfb3f5962ba264750abe5ebddf71bbb79074cade0cd677664dda4fe10fc95330`

Reply in `reviews/verdicts/reference-absence-implementation-001.md`.
