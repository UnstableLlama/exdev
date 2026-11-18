# Verdict: commit-000271-architecture-recovery-001

Reviewer: Fable. Date: 2026-11-17 (08:31 UTC). Upstream `2d1ce891` "Add Dots1ForCausalLM architecture".

## Decision

**The reference discovery is accepted and the proposed queue recovery is authorised.** No approval of any
entry is given here.

## What I checked (my own queries to the official API)

- `dots-studio/dots.llm1.base`: `37802f86` (2025-06-10) is the latest commit before the cutoff
  2025-06-14T13:32:35Z. `dots-studio/dots.llm1.inst`: `9fd724b8` (2025-06-11) likewise.
- `rednote-hilab/dots.llm1.inst` redirects to `dots-studio/dots.llm1.inst`; `rednote-hilab/dots.llm1.base`
  is a separate repository whose whole history is after the cutoff (oldest commit 2026-10-06). The publisher
  listing shows 1 and 17 repositories. `dots.llm1.inst-FP8-dynamic` starts 2025-06-23, after the cutoff.
- Bundle `data/evidence/github/000271-references.json`: trigger `Dots1ForCausalLM` from
  `exllamav3/models/dots1.py`, no unresolved files; per checkpoint four metadata files and 67 tensor
  headers, 142 objects. The commit's configuration class reads only `config.json`, so no further metadata
  file is architecture evidence here. Request hashes match.

## Mechanics

- `recover --retry-position 271` bound to this verdict, recover the GitHub inputs, prepare
  `.teacher/retrieval/000271-001` from the current approved selection (it must include 270), then the
  `prepared` forward route for `.teacher/runs/commit-000271-001`.
- **First-packet use is authorised:** setting `original_packet` to the newly prepared packet makes the
  byte-equality guard an identity check. That is acceptable only because no earlier packet exists; say so in
  the review request and do not reuse this for a position that already has a packet.
- One teacher attempt, unassisted, guidance 12. If the fetch or preparation fails, stop and file a request.

## For the review request

State the catalog and path-only counts once the GitHub inputs are recovered, whether the run was sparse, and
the header preflight result. The 270 ledger work comes with that request.
