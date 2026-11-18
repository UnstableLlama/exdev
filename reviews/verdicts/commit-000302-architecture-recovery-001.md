# Verdict: commit-000302-architecture-recovery-001

Reviewer: Fable. Date: 2026-11-17 (19:03 UTC). Upstream `d42d6238` "Add SmolLM3 architecture".
Stopped run: none exists (302 stopped before any packet or run). New run: `.teacher/runs/commit-000302-001`.

## Decision

**The reference discovery is accepted and the proposed queue recovery is authorised, including first-packet
use.** No approval of any entry is given here.

## What I checked (my own queries to the official API)

- Request hashes match.
- `HuggingFaceTB` lists 84 repositories now, as you report.
- Pins: for `SmolLM3-3B`, `SmolLM3-3B-Base` and `SmolLM3-3B-ONNX` the latest commit at or before the cutoff
  (2025-07-09T01:25:28Z) is `b49c7713`, `01580eff` and `e706b13a`, equal to yours.
- The two other SmolLM3 repositories visible today, `SmolLM3-3B-checkpoints` (first commit 2025-07-20) and
  `SmolLM3-3B-GSM8K-SFT` (first commit 2026-04-03), have no revision before the cutoff; rightly excluded.

## Mechanics

`recover --retry-position 302` bound to this verdict; prepare `.teacher/retrieval/000302-001` with the
current approved selection including 301; preflight the four headers; one unassisted Sol medium guidance 12
attempt at `.teacher/runs/commit-000302-001` through the prepared route, with `original_packet` equal to
that same packet (identity check, first packet only). Any fetch, preparation or preflight failure stops for
review.

## For the review request

Say which config keys and which tensor facts the teacher read from each checkpoint (the ONNX repository
has no safetensors: say what was and was not established from it).
