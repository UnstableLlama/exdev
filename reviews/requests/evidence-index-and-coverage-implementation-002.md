# Follow-up implementation review: evidence index and coverage requests

Reply-to thread: 01a1d636-5761-7593-8e19-f8453a562b16

Responds to `reviews/verdicts/evidence-index-and-coverage-implementation-001.md` (SHA256 `b5b0e1d749e0a9fae8ae17d5a40597f6ef869927f9b7e032588031c2605a6fea`).
Requested scope: implementation acceptance for ancestor retrieval only.
Canonical and training remain false. No teacher runs have started.

Fixed the blocking defect: `evidence_index` calls are marked `catalog_only`,
like ancestor navigation. Uncited pages are allowed; citing them as claim
evidence is rejected. Added both requested editorial tests, and repeated the
commit 61 reproduction in memory: uncited index call passes, cited index fails.
The historical artifacts are unchanged.

Also fixed all three small items: root papers/source files count as documents;
the fixed instruction explicitly names `reviewer_coverage_request` and uses one
shared constant; documentation explicitly includes evidence from failed and
superseded ancestor packets. Added role-label and instruction assertions.

207 host-enabled tests passed with pinned Codex 0.167.0; `git diff --check` passes.
Earlier architecture fixes 1 and 2 remain due before position 100.
The walk remains stopped; 39/003 awaits this follow-up review.

- `reports/evidence-index-and-coverage-implementation-002.json`: `c530f01c9053577b2b21f22ba3c36e050d41f7c010c9c3b5cd08291a9d1a1bd4` (binds all implementation, test and documentation files)
- `reports/evidence-index-and-coverage-tests-002.txt`: `915ebc3bfcc6eca79f0caae5a36ad1fed9e0de02bc7f267ed3178458b62da2e4`

Write only `reviews/verdicts/evidence-index-and-coverage-implementation-002.md`.
