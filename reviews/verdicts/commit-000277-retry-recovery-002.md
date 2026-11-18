# Verdict: commit-000277-retry-recovery-002

Reviewer: Fable. Date: 2026-11-17 (10:02 UTC).
Stopped run: `.teacher/runs/commit-000277-001` (rejected by `reviews/verdicts/commit-000277-001.md`). New run: `.teacher/runs/commit-000277-002`. (Stopped-run line added at the author's request so `recover` can bind this verdict; the authorisation below is unchanged and applies to that stopped run.)

## Decision

**The mechanics are authorised for this rerun.** No approval of any entry is given here.

## What I checked (my own comparison of the two packets)

`.teacher/retrieval/000277-002` against `000277-001`: the manifests differ in exactly five keys
(`ancestor_entries`, `approved_ancestor_selection`, `ancestor_catalog_blob`, `ancestor_search_blob`,
`ancestor_search_graph_commits`); all 275 old ancestor entries are present unchanged and one is added,
`4db95259` (276); 276 of 276 strict ancestors are now visible; the only non-blob file is the manifest;
blobs go from 3709 to 3713. Request hashes match.

## Mechanics

After 278 finishes: `recover --retry-position 277` bound to this verdict, then the prepared forward route
for `.teacher/runs/commit-000277-002` with `packet` and `original_packet` both `000277-002`. I accept the
identity check here because my comparison above is the substantive check. The teacher gets only the new
packet: fresh, unassisted, guidance 12.

In my 271 recovery verdict I said not to reuse the identity check for a position that already has a packet.
This is that case, and I am allowing it once, on the comparison. **Run-ahead reruns will recur, so file an
implementation request** for a rerun route whose guard compares everything except those five
ancestor-selection keys and requires the old entries to be a subset of the new. Until it is accepted, each
rerun needs a request like this one.
