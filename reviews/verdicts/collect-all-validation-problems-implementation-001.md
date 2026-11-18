# Verdict: collect-all-validation-problems-implementation-001

Reviewer: Opus. Date: 2026-11-18. Patch: `reports/collect-all-validation-problems-implementation-001.patch`.

## Decision

**The patch passes review. It is not applied and must not be applied until the user says so.** When they do, I will quote
their words in a separate verdict. Apply it at a queue boundary, with no teacher run active.

## What I checked myself, on an isolated patched copy

- Request hashes 0 bad; the patch applies cleanly to the live tree; live `teacher/` has no v4 code.
- All six conditions of the proposal verdict are met: one repair turn; rejected references give path and rejected value only;
  method refusals give path, finding ID and tool kinds; dependent checks are skipped and documented in `teacher/README.md`; new policy
  `validator-collect-all-v4` with older policies intact; feedback capped at 4,096 bytes with total and omitted counts.
- Differential test I wrote: 3,000 randomly corrupted copies of the real finals of 338, 344, 345/002 and 346/002, comparing old
  strict validation with v4 collection. They agreed on accept or refuse every time (94 accepted, 2,906 refused). No crash, no
  refusal lost its repair eligibility, the strict refusal was always among those collected, and the longest feedback was 1,029 bytes.
- Five bad citations placed at random were all reported, in 200 of 200 trials.
- Historical replay through patched `verify_final`: 54 runs pass, none fail, including all nine repaired runs that have a
  published draft (266, 269, 270, 271, 297, 299, 314, 323/002, 325).
- The dropped chapter-assignment check in collect mode is safe: for chapter tasks `output_schema` already fixes one chapter with
  the assigned ID, so a mismatch is a shape refusal.
- The author's replay shows 345/001 getting both bad positions and 346/001 getting both independent problems. I read the messages.
- Full suite on a complete patched copy outside the live tree, with `EXDEV_SANDBOX_TESTS=1` and `codex` on `PATH`: 358 tests, OK.

## Noted, not blocking

1. `Findings require successful prior or current evidence` is not repairable today and becomes repairable under v4, because every
   collected refusal is eligible. It affects only the unused revision route and the second final is still fully checked.
   Say so in the patch notes or keep it terminal.
2. After a failed repair the run error keeps only the first problem's category. The transcript does not hold the full list for the
   second final. A later diagnostic could record it.
3. The patch adds three test methods. Failed-repair and historical-replay cases rest on existing tests and on the replays above.

## Not verified

No live teacher turn was run, so whether the teacher fixes several problems in one turn is untested. Watch the first real use.
