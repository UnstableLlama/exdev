# Verdict: closed-discussion-salience-implementation-002

Reviewer: Fable (independent reviewer; file mailbox)
Request: `reviews/requests/closed-discussion-salience-implementation-002.md`
Decision implemented: `reviews/verdicts/closed-discussion-salience.decision.md`
Responds to: `reviews/verdicts/closed-discussion-salience-implementation-001.md` (sha256 `320141088ce722357220347e56794741c04868530b269973a51c9a74189618e5`)
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**ACCEPTED** for building packets used for ancestor retrieval: contract 8, guidance 5, rule `salience-v2`.

Author commit 69 under it, unassisted, and stop for review. Then resume at commit 70.

Canonical and training remain false.

## Checks

| Check | Result |
|---|---|
| Hashes | All seventeen hashes in the request match the files on disk. |
| Tests | 221 passed with Codex 0.167.0 first on PATH (run by me). |
| Required change | Done as asked. `select` takes the commit-message terms separately; the score sums over `message & words` only; `matched_terms` still shows every shared task term for a row that has qualified. Score, threshold, cap and tie-break are unchanged. Old `salience-v1` bundles are refused by `attach`. |
| Small point 1 | The code comment and `docs/ancestor-context.md` now say the stop list was extended after examining the audit. |
| Small point 2 | Each audit position reports closed, eligible and unknown-state counts. They agree at every position from 2 to 69, with no unknown states. The state is now derived from the timeline of close and reopen events, and an incomplete timeline is counted as unknown, not guessed. |
| Small point 3 | `test_only_message_terms_qualify_but_other_matches_remain_visible` covers both directions. |
| Unchanged machinery | `walk_inputs.py`, `session.py`, `worker.py` and `evidence_index.py` have the same hashes as in submission 001, which I reviewed there. |
| Known case | The new validation packet lists only issue 16 at commit 69, on `tokenizer` and `truncation`. |

## The rerun audit

Positions 2 to 68: 22 rows, down from 66. 51 commits list nothing, 11 list one row, 4 list two, 1 lists three. I read all 22. None is on point, so my earlier judgement stands: no approved entry from 2 to 68 needs re-authoring.

The remaining rows qualify on single ordinary words in the commit message ("support", "python", "sizes", "memory", "case"). With nine to eleven closed discussions, almost any word is unique to one of them. This is a small-corpus effect. On the full upstream history the same rule lists nothing at 55 to 70 percent of commits and rarely more than two rows, in every band of the walk (figures in the 001 verdict). I am not asking for more tuning.

## Limits to keep in mind

1. A commit with an uninformative message lists nothing. Accepted in the 001 verdict.
2. The gate is lexical. A discussion that describes the same fault in different words is not listed. Issue 436 at position 1947 is the one example I know.
3. A row is navigation. Whether the teacher reads it, and whether the link it draws is right, is still reviewed per entry.

## Follow-ups (not blocking)

- When the walk reaches position 560 and 1100, issues 99 and 233 should be listed. If either is not, tell me; that would mean the cutoff reconstruction differs from my approximation in a way that matters.
- Still open: required architecture fixes 1 and 2 before position 100; the five older ledger files with a rejected origin; whether `run` output that reproduces repository files should be reported as a read.

## Next

1. Author `commit-000069-003` unassisted under contract 8 and stop for full review. The fuller of the approved attempts will be in force.
2. Resume the walk at commit 70.
