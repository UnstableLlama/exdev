# Verdict: teacher-model-implementation-003

Reviewer: Fable. Date: 2026-11-17 (22:47 UTC).

## Decision

**Accepted. The live implementation set is the 003 set** (45 hashes in
`reports/teacher-model-implementation-003.hashes.json`, "after"; only `teacher/codex_adapter.py` differs
from the 310 provenance set). Teacher for every new run: `gpt-6.2-sol` medium, contract 8, guidance 12.
`gpt-6.1-sol` is approval-only.

## Checks (mine)

Request hashes match (0 not OK); live files equal the "after" hashes. Diff read: constants, the
`PRIOR_MODELS` tuple in the approval gate, the error text; `checked_model` untouched, so a 6.1 launch is
refused (ran it). The gate passes 310/001 and 309/001 with their recorded runtime (ran it). Moving the wire
and validation-repair fixtures to 6.2 is right: both launch a new default-model session. I ran
`tests.test_teacher_model_adoption` myself: OK. Your logs: focused 35 OK, full 338 OK.

## Ledger

The six 310 records are accepted as filed (three new identities, sorted-argmax r003,
checkpoint-token-attribute r004, terminal-string-bypass r004).

## Next, in this order

1. Record 310/001 under the 003 set (approved range becomes 2 to 310, next 311).
2. Update `reviews/AUTHOR-STATE.md` is mine; do not edit it.
3. Stop. Do not start 311. I will close this window and reopen the same thread on `gpt-6.2-sol`; on
   restart re-read `reviews/AUTHOR-INSTRUCTIONS.md` and `reviews/AUTHOR-STATE.md`, then resume at 311 with
   run-ahead as before. The first three 6.2 entries get full-depth review.
