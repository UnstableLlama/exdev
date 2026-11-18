# Implementation request: guidance-11-implementation-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Please review the guidance-11 trial gate under reviews/verdicts/guidance-11-trial.decision.md. Version 11 has its own branch: the exact guidance-9 text followed by paragraph F verbatim. It does not receive version 10's revised paragraph E. Contract-8 validation accepts 11; prepare still defaults to 9. No reviewer criteria enter teacher input. No historical packet or run was changed.

The administrative compatibility script compares complete initial inputs, tools and reasoning effort against the saved pre-edit session implementation for each version 5 through 10. All are byte-identical. Version 11 validates and is exactly version 9 plus F; all non-system inputs are unchanged. The fixture checks the unchanged default and the absence of version 10's E. No provider was invoked for these checks.

Full host-enabled suite: EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests. Ran 282 tests in 39.756s; OK.
The first suite found the missing version-11 validator allowance; its failed log is preserved. After adding that allowance, the full suite and compatibility verification passed. The suite includes the separately pending processor-metadata implementation; that change is outside this patch.

After acceptance only, run six fresh unassisted trials under .teacher/trials/guidance-11-001/: targets 213, 214, 225, 234 and controls 229, 231, using original approved cutoff evidence. Verify bound headers at 225 and 234 first. Never approve these trials or add them to ancestor context. No reviewer notes, expected findings, ledger material or coverage hints will reach trial teachers. File guidance-11-trial-001 with drafts, transcripts, coverage, tool-call and token counts and extra-call comparison. Disclose target-informed wording and one run per position; show proposed F with the trial result. Adoption still requires a user decision. The walk continues separately on guidance 9.

Administrative disk change: .gitignore now excludes exactly the three large, untracked reports/commit-000214 reference intermediate files named in the user message. All remain locally available; git check-ignore confirms exclusion.

## SHA256

- reviews/verdicts/guidance-11-trial.decision.md: `9caadd17b4d29ae33e582d088dcb1fee6aa3d437decb6425ca9e7fa1616de4a5`
- teacher/session.py: `780404d28779bfaee28fea23f2bb2807859fc62fd558b6eff6506a6b23ad074c`
- teacher/walk_inputs.py: `3c1aafc9ab6c2b2407fcfd9867a6f514ca9446b3959275e37044383f71028fac`
- tests/test_walk_inputs.py: `48ceb9d6c799d9c0e675fa6992de69ea47b1e84760888dd147792def3c38c7d4`
- reports/guidance-11-implementation-001.patch: `45cf5045fd49f906f00119a543d9d5fc34bbf1e25f2bf55aeae09b5d0a4bdb88`
- reports/guidance-11-before-session.py: `4386aff9144f995f6fe9bc58c6ad5b0006679938c4ae7ad62dc577fb2d4098a6`
- reports/guidance-11-before-walk_inputs.py: `191d2b970f37cd62599caf4ffa1e5617797082c66912fe8d8b18efc7c885d8e9`
- reports/guidance-11-verify-001.py: `b17cd9c4b90d57932a8dc532dca3fd9426bcbdf60d406792eb1736ccb6d8d0b4`
- reports/guidance-11-verification-001.json: `49b088b3c024e6e0c69c349a50a739d1a3713f2b0c7785ea52465f9c5d8d73e8`
- reports/guidance-11-tests-001.log: `b869f6ad315e0d2b6f9333da2c999f9c83c6e7369771dd78476271b0bd6a19fa`
- reports/guidance-11-tests-initial-001.log: `b69aacceb5ce39276c31ce18baec8f218e10ad43b35baeb17319254abbfb6d06`
