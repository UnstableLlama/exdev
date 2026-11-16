# Verdict: commit-000166-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000166-001`
Packet: `.teacher/retrieval/000166-001`
Upstream: `08858bc8e35b6350516507a4f01435bd4e76e25b` "Fix regression"
Request: `reviews/requests/commit-000166-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. No findings, and none are missing. The commit message says only "Fix
regression"; the entry says which one, because it read 163's approved entry, and it shows by a stand-in check
that the dictionary form passes both consumers that the bare class failed.

Both ledger candidates from 165 are **accepted**.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 22 of 22 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 165 strict-ancestor entries; 2,582 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 22 of 22 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 165/001's. Guidance 5. No trial output is among the ancestors. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path or the tracking files. |
| Catalog | Eleven open rows at 2025-05-16T20:25:14Z; my query agrees. No closed row qualified. |
| The change | `Qwen3MoeConfig.__init__` passes `{"text": Qwen3MoeModel}` instead of `Qwen3MoeModel`. One line. Correct. |
| What it repairs | `Model.from_config` can test membership and select the class; `compile_model` can iterate `.items()` and reaches the inherited hook, which returns nothing. Correct, and "repairs the producer rather than adding a compatibility branch" is right. |
| The ancestor | 163's entry (attempt 002), which recorded the omission. The entry says this specific mismatch is removed. Correct. |
| Configurations | Seven reference configurations read; all declare `Qwen3MoeForCausalLM`. The entry is careful that this shows identity only, not that FP8 or GPTQ variants load. Right: by the headers I checked at 141 they do not. |
| Execution | Recorded output: the two errors for the bare class, success for the dictionary. Matches the prose. |

## Ledger

- `exllamav3-compare-q-no-reference-finalization--r001` and
  `exllamav3-compare-q-cache-clear-argument-mismatch--r001`: accepted, both introduced at `3873d40a`.
- `exllamav3-qwen3-moe-component-migration`: please file r002 with the fix at `08858bc8`, reviewer-confirmed by
  source inspection. Affected revisions: 163, 164 and 165 (`qwen3_moe.py` is unchanged across them).

## Reviewer-only notes

- Hindsight confirmed: the fix came three commits and about twenty hours after the break.
- 165's two regressions in `compare_q.py` are not touched here. Watch for their fix.

## Not verified

- Any model load or conversion.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. The ledger revision above.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval with `--approve`.
2. Continue at 167 on guidance 5.
