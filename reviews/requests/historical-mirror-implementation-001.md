# Implementation review: historical mirror identity status

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements `reviews/verdicts/commit-000103-reference-access-001.md` and the mirror decision's new addendum. The changed
hash of `reviews/verdicts/commit-000098-reference-mirrors.decision.md` is acknowledged and bound below; old requests and bundles
retain their original hashes. No teacher run for commit 103 has started.
Requested scope: implementation and rebuilt reference bundle for ancestor
retrieval only. Canonical and training remain false.

## Affected file and conditions

`CohereLabs/c4ai-command-r7b-12-2024/config.json` uses
`mirror_historical_unverified_identity`. No other file uses the exception.

Recovery takes explicit immutable historical snapshots and checks two distinct
repositories, identical downloaded bytes, their file commit dates before the
cutoff, a different official current blob, and a later matching mirror copy after
the cutoff. Exactly one allowed non-weight file may differ. Every other reference
file must pass ordinary identity and cutoff checks at the primary historical
snapshot; LFS files use SHA-256, small Git files use blob IDs. Tensor files cannot
use the exception. The loader rechecks administrative proof, public proof,
companion coverage, statuses and file-set revision together.

The item's public proof records both repositories, snapshot and file revisions,
pre-cutoff dates, shared blob and content hash. Its notice and the model index row
say that this is the pre-cutoff mirror copy whose historical official identity
could not be checked because the official history is gated. The selection report
has the new status and retains the differing official blob and later matching date
plus metadata snapshots. Those administrative fields never enter items or packet
blobs. The index names the affected path even when other files are ordinarily
verified. The CLI accepts historical_copies through explicit mirror selections.

## Rebuilt bundle and validation

The commit 103 bundle contains all three models, 72 objects and 57 safetensors
headers: Command A 54 objects, Command R7B 9, Command R7B Arabic 9. The first and
third retain ordinary verified recovery. Command R7B's shared historical config
blob is `43fd683cd8fc1b67dcac6743694d5c954cbcf736`. File dates are 2024-12-14 and
2024-12-15; both are before the task cutoff. All eight companion files verify.
Only bounded header reads were used for tensors; no weight payload downloaded.

All 240 host-enabled tests passed on Linux aarch64, Python 3.14.4. New tests cover
acceptance, duplicate/future/disagreeing witnesses, invalid later evidence,
companion mismatch/omission, status tampering, weight exclusion and index leakage.
The real administrative packet audit passed 294 sandbox checks across new and
inherited mirror evidence, including index/config/header reads and mutable/weight
path denials. It verifies the uncertainty label and excludes the later official
blob and date from packet content. No model inference occurred. Reference bundles
39, 72, 98 and 102 still validate unchanged. `git diff --check` passes.

The administrative packet is `.teacher/audits/commit-000103-mirrors-001`; it is not
an authored run. Commit 103 remains blocked pending this implementation verdict.
Its eventual commit review request must name the affected config and status.

## SHA256

- teacher/historical_mirror.py: `5720ab741397cb6d40d8739e4db0490f26c6fef506c7df9f8a89c26c2617ea9b`
- teacher/mirror_evidence.py: `e39edb250a694629b67cd1512115486383b8085c0d7eab7064f99d441cbe1e36`
- teacher/architecture_evidence.py: `f33cbb27a47ae1f34c283166c59d4466571f51220c8143dae0385af12003168b`
- teacher/evidence_index.py: `aa1cf38eff85edbd0786d5695114cd42972c27cb7deebfc4cb6d3f28b75bd886`
- tests/test_historical_mirror.py: `2f40570815427dae1dd176b04fdc9695dbb34786579f3533e996c2d8d15d8f1b`
- docs/ancestor-context.md: `a4cdcad35d63c9781f91758a57c85698f1eb7ef09226ee7d1e9de8285e6300bc`
- reviews/verdicts/commit-000103-reference-access-001.md: `154cd6c6cac60803ba4566f2f45b44d403617973e426b2d5a61ce50dbbc9c76f`
- reviews/verdicts/commit-000098-reference-mirrors.decision.md: `33adbd76861e8bc4fd7c2d1e0eaca96ccde628572e1f403b92218c3b67487584`
- data/evidence/github/000103-references.json: `3a785b046ffaf9c82bdc95bd0c6f1c0f49db1fa1a5a51f3760d713cb97ee6f4d`
- reports/commit-000103-reference-selection-003.json: `601ba4b8d371fdc5d0448e37c9340aad4fce2fa4bc936233b0bfe96fac3236fa`
- reports/historical-mirror-tests-001.txt: `076ab4366ae20a639cf5e504028c919b240dc61fd3cbec15750eef11115bf1c0`
- reports/historical-mirror-boundary-001.json: `e9f54fc4834bbc97707b179360a7b4088b68cdec8269828fa947bc8b738c1038`
- .teacher/audits/commit-000103-mirrors-001/manifest.json: `984865edf812f9ad21a16dcc5ece3766be46363689c4fb1db8d07f6e6581daa8`
- reports/historical-mirror-implementation-001.json: `f33a976b9e10774b386d72516687a21f1819aa18ed566b2fc89ff6a9ad3c7cc9`

Reply in `reviews/verdicts/historical-mirror-implementation-001.md`.
