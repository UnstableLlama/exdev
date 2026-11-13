# Implementation review: evidence index and coverage requests

Reply-to thread: 01a1d636-5761-7593-8e19-f8453a562b16

Requested scope: implementation acceptance for ancestor-retrieval authoring only.
Canonical and training remain false. No replacement or commit 62 has been authored.
Commit 61 approval is recorded in `reports/commit-000061-review-001.json`.

## Decisions

- `reviews/verdicts/evidence-index-and-config-reading.decision.md`: `3ee7c2ca36719b021e5d90124751bfa6ffd86bb434213fce81c357805ff57b6b`
- `reviews/verdicts/thin-entries-and-retroactive.decision.md`: `805d83465f08e7e9d1ec59670962f934aadb768b41b264ece36c65cea15e09f9`

## Implementation

Walk contract v6 / guidance v3 adds the configuration-reading sentence from the
user decision. Model sources are grouped by pinned repository/revision with date,
attaching commits and role counts; bodies and headers remain on demand. The 8 KiB
opening page has truncation/next-offset fields; `evidence_index` pages source rows
and per-source object metadata. Existing fetch tools serve indexed content, with
an optional source_id for exact historical-object selection. Index navigation
cannot support claim citations.

Preparation discovers historical packet manifests and filters to strict ancestors;
it rechecks object dates, copies only allowlisted evidence metadata and verified
blobs, and binds the complete index/object inventory to the contract. Direct task
web listings remain unchanged; task model files use compact grouping too.
Discussion titles use cutoff-reconstructed cached title histories when available.
Absent legacy titles are not invented. Separate unreferenced catalogs retain their
existing open-discussion policy; this does not add closed unreferenced discussions.

Coverage requests are verbatim in a separate opening field with the fixed
not-statements-of-fact sentence. Their path/hash are bound, provenance records
both, and provenance/review mark reviewer_assisted. Position and attempt checks
prevent cross-run use. The author must inspect semantics before supplying the
exact approved digest: automated gates cannot prove prose contains no implied
conclusion. I read the supplied 45/002 and 55/002 requests and found them within
the authorized pointer/question scope. No verdict or canonical observations are
in teacher input. Old attempts and packets are unchanged.

The policy now documents REJECTED: thin and the narrow coverage exception.
The walk refuses any advancement_pause even if status is set ready.

## Validation

204 host-enabled tests passed with pinned Codex 0.167.0, including isolated tool
and wire checks. Focused cases cover ancestry, cutoff rejection, source/object
paging, HF/web/header fetch, cutoff title reconstruction, compact task references,
index/blob tampering, coverage hash/attempt checks, verbatim opening content,
assistance provenance/review flags and legacy guidance/tools. Historical 39/002
and 61/001 assessments still pass. `git diff --check` passes.

A no-authoring dry run over the historical commit 61 packet discovers 279 objects
in 18 sources; its compact opening index fits the 8 KiB cap. No new teacher run
was started. Implementation files and test log are hash-bound in the report.

Earlier architecture fixes 1 and 2 remain due before position 100 and are not
claimed closed. After acceptance, replacements are 39/003, 44/002, 45/002, 55/002,
each stopping for full review and reporting dependents. Commit 62 remains blocked.

## Artifacts

- `reports/evidence-index-and-coverage-implementation-001.json`: `783624ed09b5d84502a4c5a96c631446bfff793642e8f676fc62d8f44f9f7e21`
- `reports/evidence-index-and-coverage-tests-001.txt`: `b13c2c4c4bfd2ea337dce938b9746dd769f3fb74a83a6dcc2ccb653fb5ca9e6a`
- `reviews/verdicts/commit-000045-002.coverage.md`: `f0187fdaafe109c5e9c7795ff8e974d0730385ef5ff5496e65286246e4c1df5a`
- `reviews/verdicts/commit-000055-002.coverage.md`: `a8d0540538b5c8b794a8a70bd13898ddb2d249f6026a08ca58893f35c859652b`

Write only `reviews/verdicts/evidence-index-and-coverage-implementation-001.md`.
