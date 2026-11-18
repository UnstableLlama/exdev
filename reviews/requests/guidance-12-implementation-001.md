# Implementation request: guidance-12-implementation-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Author/orchestrator: gpt-6.1-sol, medium. Proposed trial teacher: gpt-6.1-sol, medium.

Please review the trial gate authorized by guidance-12-trial.decision.md. Version 12 has its own branch: guidance 11 with paragraph F replaced verbatim by the decision's revised F. It retains version 9's paragraph E, not version 10's. Contract-8 validation accepts 12. The walk prepare default remains 11. No trial has started, and replacements remain paused.

Compatibility verification compares complete initial inputs, tools and reasoning effort against the saved pre-edit implementation for versions 5–11: all are byte-identical. Version 12 validates and is exactly version 11 with F replaced; non-system inputs, tools and effort are unchanged. The fixture also checks the unchanged default and exclusion of version 10's E. These checks invoke no teacher. The patch isolates this change from previously accepted, uncommitted work; implementation edits occurred after 246's run and validation.

Full host-enabled suite: `EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests` — 287 tests in 47.681s, OK.

After acceptance only: six fresh, unassisted Sol/medium trials on packet copies differing only in guidance_version, under `.teacher/trials/guidance-12-001/`. Targets 98, 103, 110, 214; controls 243, 245. Preserve the original evidence and ancestor snapshots, confine runs as before, and never approve or publish trial entries for ancestor retrieval. No reviewer material, ledger records, expected answers or coverage hints reach teachers. File guidance-12-trial-001 with drafts, transcripts, findings side by side, calls and token totals against 98/002, 103/002, 110/002, the guidance-11 trial of 214, and approved 243/001 and 245/001. Disclose target-informed wording, one run per position, and the Astra-to-Sol model confound at 98 and 214. Adoption requires a separate user decision.

Forward 246 is awaiting review; the forward walk remains on guidance 11. This request does not lift the replacement pause or authorize a retry of replacement 110.

## SHA256

- reviews/verdicts/guidance-12-trial.decision.md: `f4b5a7d2c30dc4d67d656caa25a5aeec9007ea300bf79b3e5ff8f5d835ea9ece`
- teacher/session.py: `698c6a564df6457ba3fac71c72de0824867695f0dc07b555be9d3ba8dafb4a63`
- teacher/walk_inputs.py: `cec148b66c0d4dcb2c34bbf6dcfdf7f075fe2eeb7192629473725bd6e42f22d4`
- tests/test_walk_inputs.py: `8cdbe31e8c64d5c87d6884b204a728c3f77a684d0d5b0c824d25bcacae69f14b`
- reports/guidance-12-implementation-001.patch: `a4adbc1f383afe77d5f042f64dc4bd53b47825fb38707cc25d0427c9aac0d4da`
- reports/guidance-12-before-session.py: `780404d28779bfaee28fea23f2bb2807859fc62fd558b6eff6506a6b23ad074c`
- reports/guidance-12-before-walk_inputs.py: `35327960008029745460ab3a6fb550f92672bf783f764b22505f6103e86809f2`
- reports/guidance-12-verify-001.py: `c805d75761f826f0d678d9398bd08291da921010aa45a2771478e8da016bb0d4`
- reports/guidance-12-verification-001.json: `78bb0d855d839719c210c029dd6631f7308bad24a723576409251341eef76c11`
- reports/guidance-12-tests-001.log: `4fd029a3be0f7cefb7b073a98336a6aa7866f4a4cbf7296d39106e8b445dc37a`
