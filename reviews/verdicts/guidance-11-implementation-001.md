# Verdict: guidance-11-implementation-001

Reviewer: Fable. Date: 2026-11-16.

## Decision

**Accepted.** Version 11 is implemented as the decision file asks. The trial may run as described in the request
(targets 213, 214, 225, 234; controls 229, 231; under `.teacher/trials/guidance-11-001/` only). The walk default
stays 9. Trial runs are never approved and never become ancestor context. Adoption needs the user's decision
after the trial.

## Artifacts

All eleven hashes in the request match the files on disk. The two "before" copies are byte-identical to
`teacher/session.py` and `teacher/walk_inputs.py` at `HEAD` (`9eaf68e`), so the comparison baseline is the
committed implementation.

## Run checks

- Patch read in full (70 lines). `GUIDANCE_11_ADDITION` is paragraph F word for word. A new `== 11` branch
  appends the guidance-9 addition and then F; the `>= 10` branch is now an `elif`, so 10 is unchanged and 11
  does not receive the revised E. The validator's allow-list gains 11. `prepare` still writes 9.
- I reran `reports/guidance-11-verify-001.py` (it needs `PYTHONPATH=.`): exit 0 and the report file is
  reproduced byte for byte. Versions 5 to 10: initial inputs, tools and reasoning effort equal to the committed
  implementation. Version 11: system text is version 9's plus a blank line plus F; everything else equal to 9.
- Astra's suite log: 282 tests, OK. I ran the suite an hour earlier with the processor-metadata change (280
  pass; the two `test_codex_wire` errors were my shell lacking `codex`) and did not repeat it here.
- `.gitignore`: the three large 214 intermediates are ignored (`git check-ignore` lists all three).

## Not verified

- A version above 11 would fall into the `>= 10` branch; the validator rejects it, so this is unreachable now.
  Keep it in mind if a version 12 is ever added.

## Conditions for the trial

- Confirm before running that tensor headers are bound in the 225 and 234 packets; say so in the trial request.
- No reviewer material (the pass criteria in the decision file, ledger notes, coverage hints) reaches a trial
  teacher.
- Report tool-call and token counts beside the approved runs' figures, and state the two weaknesses (wording
  written with the targets in view; one run per position).

## Next

Run the trial and file `guidance-11-trial-001`. The walk continues on guidance 9.
