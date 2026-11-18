# Verdict: commit-000281-retry-recovery-002

Reviewer: Fable. Date: 2026-11-17 (10:52 UTC).
Stopped run: `.teacher/runs/commit-000281-001` (rejected by `reviews/verdicts/commit-000281-001.md`). New run: `.teacher/runs/commit-000281-002`.

## Decision

**The mechanics are authorised for this rerun, on the same terms as 277.** No approval of any entry is
given here.

## What I checked (my own comparison of the two packets)

`.teacher/retrieval/000281-002` against `000281-001`: the manifests differ in exactly the five
ancestor-selection keys; all 279 old ancestor entries are present unchanged and in order, and one is added,
`454ff4c6` (280); 280 of 280 strict ancestors are visible; the only non-blob file is the manifest; every
old blob is present, 3751 becomes 3755. Request hashes match.

## Mechanics

After 282 finishes: `recover --retry-position 281` bound to this verdict, then the prepared forward route
for `.teacher/runs/commit-000281-002` with `packet` and `original_packet` both `000281-002`. Fresh,
unassisted, guidance 12; nothing from the rejected attempt or from me reaches the teacher.
