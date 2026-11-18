# Verdict: commit-000241-001

Reviewer: Fable. Date: 2026-11-16. Upstream `93cb21ca` "Cleanup and comments". Guidance 11.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. The finding
`inherited-bounding-box-overflow` is **accepted as true** and is the existing ledger identity
`exllamav3-vision-floating-ceiling-overflow`, not a new defect.

## Artifacts

Request hashes match. `check.py` clean (the implementation hash list is current again): manifest and
provenance agree, 16 evidence calls all cited, final equals annotation, 240 ancestors, 3297 blobs, nothing
after the cutoff (2025-06-05T00:26:00Z). Instructions identical to 240's run.

## Run checks

- Replay: 16 of 16 identical.
- Diff read: four comment or docstring edits (a class name in a docstring, one sampling TODO removed, two
  preprocessing docstrings). No executable change, as the entry says.
- The finding: the new Mistral3 docstring promises a fit inside a `longest_edge` square. I recomputed the
  entry's example: 1541 by 1000 with a 1540 limit divides to `1540.0000000000002`, ceilings to 1541 and aligns
  to 28 pixels as 1568 by 1008. Correct. The entry is right to raise it here: this commit writes down the
  guarantee that the unchanged helper does not keep. It correctly says the 1540/14/2 values are assumed, not
  read from a checkpoint.
- Discussion links are stated as inference only.

## Reviewer knowledge (must not reach a teacher)

1540 and 14 are in fact the Mistral Small 3.1 preprocessor values (I fetched the files at 234; they are now in
the backfill bundle, not attached here). With them the overshoot gives 112 patches on a side against the
110-entry table noted at 234.

## Follow-ups

Ledger, with the next request: observation revision on `exllamav3-vision-floating-ceiling-overflow` for 241
(the documented guarantee).

## Next

Record the approval and proceed to 242. Replacements stay on hold.
