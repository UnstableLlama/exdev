# User decision: re-author commits 39 and 41 before commit 44

Recorded by: Fable (independent reviewer; file mailbox)
Decided by: the user, in chat, 2026-11-13. I recommended re-authoring both before commit 44. The user replied: "do you want me to authorize the re author? i trust your judgement". I am recording that as authorization of the recommendation.
Completes: the "Not decided here" section of `reviews/verdicts/reference-evidence-and-callee.decision.md` (sha256 `e2a1425cc6f30db79646f2bead50be26e0a2500f63c3d0400b835ce5947f3fa7`). That file is not edited, so existing bindings to its hash stay valid.

Canonical and training remain false throughout.

## Decision

Re-author both, each stopping for full review, before authoring commit 44.

- **Commit 39** as `commit-000039-002`: contract v5, guidance version 2, with reference configurations attached under Decision 1 of the earlier file.
- **Commit 41** as `commit-000041-002`: contract v5, guidance version 2. No reference trigger applies.

## Rules, same as the catalog-hints re-authoring

- **No hindsight.** Each packet is built for its own commit: ancestor entries strictly before it (through 38 for commit 39, through 40 for commit 41), evidence and catalog as of its own cutoff, nothing from later commits or from reviews. The verdicts for 39 and 41, including the hindsight section in the commit 39 verdict, are not teacher input in any form.
- **Order.** Do 39 first. Commit 41's packet must then use the approved replacement for 39 as its ancestor entry, and commit 40's existing entry as is.
- The currently approved attempts (`commit-000039-001`, `commit-000041-001`) stay approved and unchanged until a replacement is approved. On approval the replacement supersedes the old attempt for future retrieval.
- **Dependents.** List the later runs whose transcripts read the superseded entries (40 to 43 for commit 39; 42 and 43 for commit 41). Do not re-author them automatically; the reviewer will say whether any needs it.
- **Reference selection for commit 39.** Follow the earlier decision: choose from what the commit message names and what was public before the cutoff, record every candidate considered and the reason, attach more than one where there is a real choice. The selection is reviewed against that rule, not against any outcome. This is also the first live recovery; report the pinned revision and its date, the objects fetched, and confirm no weight bytes were requested.
- If either re-authoring produces a result the request cannot explain, or building it conflicts with the no-hindsight boundary, stop and say so in the request.

## After both are reviewed

Resume the walk at commit 44 under contract v5 and guidance version 2. Required fixes 1 and 2 from the implementation verdict remain due before position 100.
