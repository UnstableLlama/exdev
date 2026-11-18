# Verdict: commit-000242-001

Reviewer: Fable. Date: 2026-11-16. Upstream `17f1ab5e` "Fix rounding error in Pixtral image preprocessor".
Teacher `gpt-6-astra`, medium, guidance 11 (in progress when Sol was adopted).

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. No findings; none expected. The
ledger revision `exllamav3-vision-floating-ceiling-overflow` r003 (owed from 241) is **accepted**.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree, 44 implementation hashes, 8 evidence
calls all cited, final equals annotation, 241 ancestors, 3306 blobs. Instructions identical to 241's run.

## Run checks

- Replay: 8 of 8 identical.
- Diff read: `ceil` becomes `floor` with a minimum of one, before the unchanged upward alignment to the patch
  grid. As the entry says, the two edits belong together.
- The entry's sweep recomputed by me with its sizes (maximum 224 by 192, patches 16 and 32, inputs 1 to 300):
  2,497 overflows before, none after, 4,467 outputs changed, and `(230,1)` goes from `(240,32)` to `(224,32)`.
  All four figures exact.
- Why the fix holds (mine): after flooring, each dimension is at most the maximum, and the maximum is a
  multiple of the patch size (asserted), so rounding up to the grid cannot pass it.
- The entry's point that this changes more than the overflowing cases is right and worth keeping.

## Reviewer knowledge (must not reach a teacher)

With the real Mistral Small 3.1 values (1540 limit, 28-pixel grid) my sweep gives no overflow after the fix
and a largest side of 1540, which is 110 patches. That closes the chain I noted at 234 and 236 (112 patches
against a 110-entry table): it is no longer reachable through this helper.

## Ledger

- r003 of `exllamav3-vision-floating-ceiling-overflow`: 241 observation added, earlier ones kept, no fix
  claimed. Accepted.
- Owed with the next request: a revision recording `17f1ab5e` (242) as the fix. If the ledger holds my 234
  reviewer observation about the table width as a separate record, mark it resolved by the same commit.

## Next

Record the approval. No further teacher session until `teacher-model-sol-adoption-001` is accepted.
