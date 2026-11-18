# Verdict: commit-000295-retry-recovery-002

Reviewer: Fable. Date: 2026-11-17 (14:58 UTC).
Stopped run: `.teacher/runs/commit-000295-001` (rejected by `reviews/verdicts/commit-000295-001.md`). New run: `.teacher/runs/commit-000295-002`.

## Decision

**The mechanics are authorised for this rerun, on the same terms as 277 and 281.** No approval of any
entry is given here.

## What I checked (my own comparison of the two packets)

`.teacher/retrieval/000295-002` against `000295-001`: the manifests differ in exactly the five
ancestor-selection keys; all 293 old ancestor entries are present unchanged and in order, and one is added,
`6f9928b3` (294); 294 of 294 strict ancestors are visible; the only non-blob file is the manifest; every
old blob is present, 4280 becomes 4284. Request hashes match.

## Mechanics

After 296 finishes: `recover --retry-position 295` bound to this verdict, then the prepared forward route
for `.teacher/runs/commit-000295-002` with `packet` and `original_packet` both `000295-002`. Fresh,
unassisted, guidance 12; nothing from the rejected attempt or from me reaches the teacher.
