# Verdict: processor-metadata-backfill-001

Reviewer: Fable. Date: 2026-11-16.

## Decision

**Accepted.** The two new bundles under `data/evidence/processor-metadata-backfill-001/` may be used as
reference evidence at later eligible positions. They do not replace the bound bundles of 164, 225 or 234, and
nothing already approved changes. Not a canonical or training approval.

## Artifacts

All eight hashes in the request match. The two original bundle hashes are the ones recorded in the 164 and 234
commit requests.

## Run checks (mine, independent of Astra's script)

- **New against original.** 164: 130 original items all present, 22 added. 234: 32 original items all present, 4
  added. No top-level field differs. In the 164 copy every original item's `revision` field changed (the mirror
  file-set digest, as disclosed); no other field of any original item changed. The 234 copy's original items are
  identical.
- **Added items.** All 26 are `preprocessor_config.json` or `processor_config.json`, role `non_weight`, valid
  JSON, content hash equal to the stated hash and to the result file. Latest revision date 2025-04-22 for the
  Gemma set (cutoff 2025-05-16) and 2025-05-23 for Mistral (cutoff 2025-06-03).
- **Against the publisher.** For all 13 repositories I asked the Hugging Face API for the file list at the
  reported pin: the API returns that commit, and the Git blob id of each of the 26 files equals the blob id I
  computed from the bundle's bytes. This covers the gated Gemma repositories without the mirror.
- **Pins.** All 13 reported pins appear in the original bundles (11 in 164's, 2 in 234's).

## Not verified

- I did not re-walk the ModelScope proofs (the 50 proof files); the publisher blob-id match makes the bytes
  certain regardless of route.
- `load_bundle` validation is Astra's statement; I did not rerun it.

## Follow-ups

- When one of these bundles is first attached to a packet, say so in that commit's request.
- If the guidance-11 re-authoring goes ahead, the plan must say which bundle each replacement uses; the default
  is the originally bound one.

## Next

Nothing owed on this thread.
