# Verdict: commit-000345-recovery-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (18:16 UTC). Stopped run: `.teacher/runs/commit-000345-001` (validation failure, no draft). New run:
`.teacher/runs/commit-000345-002`. Upstream `c3049627ea2cdbe7f0c8e62e2491e4eed8d37072` "LlamaForCausalLM: Use FP32 intermediate dtype".

## Decision

**One fresh unassisted attempt is authorised.** There is no draft to judge, and no approval of any entry is given here.

## What I checked myself

- Request hashes 0 bad. Status `failed`, not published, no cycle process, no 345/002 run yet.
- Cause: the first final (row 144) cites `call_38549430cfc44212bdb2403c3c362e` twice. It is 35 characters, every real call ID is 37, and it
  is a mistyped copy of `call_38549430cfc44212bdb2403e8459867d`. The validator refused it, and the repair message named only the first
  location. The repair fixed that one and left the second in the final at row 149, which was refused.
- This is a citation slip by the teacher. It is unrelated to the provider schema change: `codex-failure.json` has zero error events, and
  evidence IDs were never in the removed enums.
- 344 and 345 touch different files, so the run-ahead played no part.

## Authorised

`recover --retry-position 345` bound to this verdict, then one fresh unassisted 345/002: normal packet builder, same cutoff and pinned
evidence, approved ancestors through 344, contract 8, guidance 12, gpt-6.2-sol medium. The new packet may differ from 000345-001 only by
adding the approved 344 entry and what that requires in the ancestor catalog and search data. Record that comparison; any other difference
comes back to me first. Nothing from 345/001, this request or this verdict reaches the teacher. Keep the 345/001 artifacts.

If it fails, stop and file it. There is no automatic third attempt.

## Ledger, 344 records accepted

`ernie-old-name-correction-not-preserved` r001 is new, suspected, a behavior change introduced at `c8ed45c6`. `all-expert-fused-shape` r016 and
`fused-output-dtype-override` r007 each add one observation at `c8ed45c6`, with a matching verification step and a qualification naming my
provisional approval. Earlier observations are byte-equal, there are no fixes, and none is training-eligible.

## Proposal only, not in force

The repair message reports one location, though the same bad ID appeared twice. Reporting every location of a rejected reference would
have saved this run. If you agree, file it as a normal implementation request. It changes what the teacher is told, so it would need
review and the user's word.
