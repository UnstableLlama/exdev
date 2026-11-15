# Implementation review: architecture-trigger fixes before position 100

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Requested scope: implementation acceptance for future ancestor-retrieval packets.
No prose approval is requested; canonical and training remain false. Commit 99's
approval and ledger acceptance are recorded. Commit 100 has not started and stays
blocked pending this verdict.

## Changes

Implements required fixes 1 and 2 from
`reviews/verdicts/reference-evidence-and-callee-implementation-001.md`.
A `not_new_architecture` administrative outcome carries a reason. Git-detected
renames and moves preserving declared classes and identities receive an automatic
outcome. New registry keys cannot be waived. A covered merge requires hash-bound,
validated reference bundles from its merged ancestry, cutoff checks, architecture
coverage and byte-identical relevant source files. A reason alone cannot waive a
source-derived new architecture. Other administrative attestations remain subject
to review.

Architecture identities now come from parsed config-class literals and constructor
arguments, including new identities added within an existing file. If static
extraction cannot derive an identity, the bundle must explicitly list unresolved
files. No source code is executed. Fix 3's existing successor-directory support
and fail-closed behavior are retained and the known-directory move is tested.

Administrative reasons and proofs remain outside teacher-visible packet content;
the reference bundle hash still binds them. Contract 8, guidance 5 and salience-v2
remain unchanged. No teacher run or model invocation was performed.

## Validation

All 237 host-enabled tests passed on Linux aarch64, Python 3.14.4. Tests cover
rename/move outcomes, forbidden registry waivers, constructor-derived identities,
existing-file additions, explicit unresolved identities, merge coverage and hash
tampering, unknown architecture locations, and administrative packet exclusion
with bundle-hash validation. Python compilation and `git diff --check` passed.

The administrative audit found zero trigger changes across positions 1–99 and
validated the unchanged real reference bundles for 39, 72 and 98. It inspected
only the three future cases named by the original review: `151edc00` and
`d9906114` receive automatic rename/move outcomes; `b2d05c0b` cannot be waived
without prior branch coverage. No future teacher packet or reference recovery
was performed. The full suite log contains ResourceWarnings but no failures.

This request covers the four source/test/document files below. The mirror test
change only updates its trigger mock; previously accepted mirror and arm64
implementation changes elsewhere in the working tree are outside this request.

## SHA256

- teacher/architecture_evidence.py: `0a96516acce0f8170d960bb428ec30e247fdeac1c66aba9c42277ff07dcc5354`
- tests/test_architecture_evidence.py: `51ff9debf2c36c884a84a446c8e0aad17da063d3330e516081205c3c5da64b76`
- tests/test_mirror_evidence.py: `8bec2bb39d8ea72f25f29257dd0af018af764ec15a167f4db1514fe087ba9477`
- docs/ancestor-context.md: `9991a3606a0eb48ee66e938900accbee3ff95fd56aee00e88fd0b1becd7085f0`
- reports/architecture-trigger-fixes-tests-001.txt: `103b2a1eafa4e3fa1c7c8d67191b6fa7c1ad913d87b9727a34daa67ebbf13856`
- reports/architecture-trigger-fixes-audit-001.json: `caf80353e66f34a394ca7f9388f53f194d4d15a83c2974184f1f6157896e6ece`
- reviews/verdicts/reference-evidence-and-callee-implementation-001.md: `52fbe55911d0e02e4682d634f38270c8c3a2c663ce00ad6e4d342354fbaafa54`
- reviews/verdicts/commit-000099-001.md: `b42b6df0ce650090e06c0f80f3156eb7f2a7f301ebf9fa77eff8be133d0571c9`
- reports/architecture-trigger-fixes-implementation-001.json: `ef06ac5d494d8f8ba0a0dc3b4e109923c187dca39abf1d8bc51947e80fb8d7b4`

Reply in `reviews/verdicts/architecture-trigger-fixes-implementation-001.md`.
