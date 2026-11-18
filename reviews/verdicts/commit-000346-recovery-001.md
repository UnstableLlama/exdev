# Verdict: commit-000346-recovery-001

Reviewer: Fable. Date: 2026-11-18. Stopped run: `.teacher/runs/commit-000346-001` (validation failure, no draft
published; nothing to judge as an entry). New run: `.teacher/runs/commit-000346-002`.
Upstream `67e0fd74413228c85e1edc65cfc7c39365b1a6ca` "TP: Refactor/fix auto allocation".

## Decision

**Recovery authorised: one fresh unassisted attempt, 346/002.** No approval of any entry is given here.

## What I checked myself

- Request hashes: 13 of 13 match. Status `failed`, not published, walk `stopped_failure` at 346 with 345 approved.
- First refusal (row 117): `source_notes[2].evidence[2]` cites `call_968078768ae1495397521c6c063ca77f`. No such call
  exists; the real one ends `...ca77d`. One mistyped character.
- Repair (row 119): differs from row 116 only in `source_notes`, where that one reference was removed. Every
  remaining citation in it resolves to a successful call.
- Second refusal: `findings[6].verification[0]` (`combined-kv-still-fails-allocation-query`) is `source_inspection`
  and cites three `run` calls (rows 112, 106, 46). `teacher/editorial.py` requires at least one source-tool result
  there. The same three references are in the first final, so this problem was present from the start and was
  hidden behind the first one. `findings[7]` has the same method with a `repo_read` among its evidence and passes.
- `codex-failure.json`: zero provider error events. The provider schema change played no part.
- The request's account of the failure is accurate in every point I checked.

## Why 345 and 346 both failed

The validator raises on the first problem it meets and the teacher has one repair turn. A final with two problems
therefore cannot pass: 345/001 had the same mistyped ID in two places, 346/001 had a mistyped ID and an unrelated
method/evidence mismatch. In both the teacher fixed exactly what it was told. This is a property of the repair
loop, not a change in the teacher.

## Authorised

`recover --retry-position 346` bound to this verdict (stopped run in full: `.teacher/runs/commit-000346-001`), then
one fresh unassisted 346/002: normal packet builder, same cutoff and pinned evidence, approved ancestors through
345, same contract, guidance and model as 345/002. The new packet may differ from 000346-001 only by what the
builder requires; record the comparison, and bring any other difference to me first. Nothing from 346/001, the
request or this verdict reaches the teacher. Keep the 346/001 artifacts.

If it fails, stop and file it. There is no automatic third attempt.

## Ledger, 345 records accepted

- `activation-odd-tail` r006: the five earlier observations are byte-equal with r005, introductions unchanged, no
  fixes, status suspected, training false. The new observation's source claim holds at `c8ed45c6`: both
  `act_mul_kernel_h` and `act_mul_kernel_f` return at `idx >= numel / 2`.
- `mistral-sliding-window-omission` r001: new, suspected, training false, no introduction claimed. Source claim holds
  at `c3049627`: `LlamaModel` builds `Attention` without `sliding_window`, the default is -1, and `MistralModel`
  only calls the parent constructor. `mistral.py` dates from the initial commit, so the two verified revisions
  are a floor and the record rightly claims no range.

## Proposal only, not in force

Have the validator collect every problem in a final (all locations of a rejected reference and all independent
refusals) and report them together in the one repair message. That would have saved both 345/001 and 346/001.
It changes what the teacher is told, so file it as a normal implementation request; it needs my review and the
user's word before it is applied. It does not block 346/002.

## Reviewer-only, never to a teacher

From memory, not checked here: the reference Transformers Mistral implementation also does not apply
`sliding_window` to its attention mask. If so the omission matches the reference and "defect" is too strong. Keep
the record at suspected.
