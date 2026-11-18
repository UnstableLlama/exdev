# Verdict: commit-000327-001 (teacher gpt-6.2-sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-18 (05:52 UTC). Upstream `db533103` "Fix #62, include new directory in packages".
Run: `.teacher/runs/commit-000327-001`. Packet: `.teacher/retrieval/000327-001`.

## What I checked myself

- Request hashes 0 bad. `check.py`: impl 45 bad [], evidence 38 calls 38 bad [] uncited [], final==annotation
  True, blobs 4599 bad 0. No repair. **anc 326 entries 325 False; replay 38, mismatch 6 = the six
  ancestor reads: this packet is sparse.** See the question below.
- Diff read in full (one line: `exllamav3.generator.filter` added to `packages` in `setup.py`).
- Central claims confirmed in source at the sha: the package list now names the filter subpackage (line 74);
  `exllamav3/__init__.py` imports `Filter` and `FormatronFilter` through `.generator` at import time, so the
  omission blocked every import of an installed package, as #62 reports; `exllamav3/integration/` exists with
  an initializer and is still not listed. The carried finding is true at this commit, and the entry also
  says correctly which half of the earlier integration finding no longer holds (the root no longer imports it).
- The entry made the central check itself, with a package-inventory check and stated limits.
- 326 ledger `installed-filter-package-omitted--r001`: suspected, training false, introduction `08dde73e`
  (Formatron). Accepted. This commit is its fix; record that in the next revision.

## Question you must answer in the next request (does not block recording)

The request says "327 ran after 326 was recorded", but the packet's `ancestor_entries` lack `327d1f99`
(commit 326) while `history_order` includes it and `ancestor_context_complete` is true. The manifest was
written at 05:43:13 UTC, after the 326 verdict (05:38). Either 327's packet was built before 326 was
recorded, in which case the request should have said "Ran ahead of: 326", or the selection dropped an
approved entry, which is a defect. Say which, with the times. I judged the gap myself: 326's entry recorded
the very omission this commit fixes, and this entry established it independently from source and #62, so
nothing is lost. But the disclosure must be right.

## Must fix before canonical

- Two Source Notes paragraphs on unrelated issues (#2, #21, #7, #48, #49, #52); cut, as you say.
- Link the 326 entry once it is visible to a rewrite.

## Decision

Approved for ancestor retrieval only. Canonical and training remain false.
