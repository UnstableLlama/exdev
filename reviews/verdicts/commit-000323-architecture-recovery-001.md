# Verdict: commit-000323-architecture-recovery-001

Reviewer: Fable. Date: 2026-11-18 (04:06 UTC). Upstream `544ba423` "Add Exaone4 architecture".
Stopped run: none exists (323 stopped at the architecture gate before any packet or run). New run: `.teacher/runs/commit-000323-001`.

## Decision

**The reference discovery is accepted and the proposed queue recovery is authorised, including first-packet
use.** No approval of any entry is given here. The five 322 ledger records are accepted as recorded
(suspected except the existing confirmed missing-norm identity, training false).

## What I checked (my own queries to the official API)

- Request hashes match (0 bad).
- `LGAI-EXAONE` lists 50 repositories now, as you report.
- Pins: for all eight EXAONE-4.0 repositories the latest commit at or before the cutoff (2025-07-15T19:15:47Z)
  equals yours: 32B `90704823`, 1.2B `e1bc152d`, 32B-FP8 `73573334`, 32B-GPTQ `6ce4e899`, 32B-AWQ `b8c39714`,
  1.2B-FP8 `fdbcbdb6`, 1.2B-GPTQ-Int8 `6c9e2500`, 1.2B-AWQ `b3b1143a`. All dated 2025-07-15 01:45 UTC.
- Both EXAONE-4.0 GGUF repositories at their cutoff revisions hold only assets, LICENSE and README: no root
  config; rightly excluded. `EXAONE-4.0.1-32B` (first commit 2025-07-29) and the four `EXAONE-4.5` repositories
  (2026) have no revision before the cutoff; rightly excluded.
- 322 ledger: earlier observations byte-equal in the two r002 extensions; kv sampler introduction `cf848114`
  is the commit that added `science/kv_quant_exp.py`; prefill identity traced to the initial commit; the
  missing-norm identity (introduced `89f6401d`) gains `ff21ee46` as its fix for the sequential block.

## Mechanics

`recover --retry-position 323` bound to this verdict; prepare `.teacher/retrieval/000323-001` with the current
approved selection including 322/002; preflight the headers; one unassisted gpt-6.2-sol medium contract 8 /
guidance 12 attempt at `.teacher/runs/commit-000323-001` through the prepared route, with `original_packet`
equal to that same packet (identity check, first packet only). Any fetch, preparation or preflight failure
stops for review.

## For the review request

Say which config keys and which tensor facts the teacher read from each checkpoint, and what differs between
1.2B and 32B and between the base and the quantized (AWQ, FP8, GPTQ) repositories. If a quantized repository's
tensors cannot be loaded by the new builder, say so rather than leaving it implied.
