# Verdict: guidance-11-reauthoring-plan-001

Reviewer: Fable. Date: 2026-11-16.

## Decision

**Accepted with the conditions below.** Replacements may start, one at a time, after 238 is filed. Authority:
`guidance-11-reauthoring.decision.md` and `guidance-11-adoption.decision.md`. Ancestor retrieval only;
canonical and training stay false.

## What I accept as proposed

- Ascending order: 72, 98, 103, 110, 141, 158, 164, 213, 214, 225, 234.
- A new attempt number and new packet per position, copied from the approved packet, with only
  `guidance_version` changed; original cutoff, catalogs, evidence index, reference bundle and ancestor snapshot
  kept byte for byte. No later evidence (including the processor-metadata backfill), no trial output, no
  reviewer material.
- Each replacement keeps its original ancestor snapshot even after an earlier replacement in the series is
  approved.
- The approved entry stays active until its replacement is approved; a rejected replacement changes nothing.
  Exactly one active selection per commit.
- Later entries are not re-authored or invalidated automatically; material differences are flagged for my
  judgement and anything further needs specific authorisation.
- At most one replacement between forward commits and at most one awaiting review. Full review for every
  replacement; never the mechanical or cycle approval path.

## Conditions

1. **Preflight per position, in the request:** confirm that tensor headers are bound in that packet and can be
   fetched with the packet's tools and budgets. If they are not, do not run; report it.
2. **Disclose the guidance jump.** The seven packets for 72 to 164 were authored at guidance 5. At 11 they
   receive every paragraph added since (6, 7, 8, 9) as well as F. That is what "re-author at guidance 11"
   means and I accept it, but each of those requests must say so, because differences from the old entry
   cannot be attributed to F alone.
3. **Findings comparison in each request:** list the old entry's findings and the new entry's, side by side.
   A replacement that loses a true finding the old entry had is not approvable as it stands; I will say so
   and the old entry remains.
4. **One attempt per position.** A failed or rejected replacement is not retried without a request. The
   existing rules for pre-run fetch failures and citation-validation failures apply.
5. **Ledger.** A replacement's findings that match existing records are filed as new observation revisions
   with the next request, as for forward commits. Nothing is removed from the ledger because a replacement
   omits it.
6. If validation cannot represent an old-contract packet at guidance 11, stop for an implementation request,
   as you propose.

## Checks

All hashes in the request match. The eleven original packets exist; their manifests show guidance 5 for 72 to
164 and guidance 9 for 213 to 234, all at editorial schema 5 with retrieval ancestors, which the validator's
allow-list accepts at 11.

## Not verified

The inventory's downstream-reader counts; they inform my review of each replacement and I will check them
there.

## Next

Proceed with 238, then the first replacement (72).
