# Implementation request: guidance-10-implementation-001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Implements reviews/verdicts/guidance-10-trial.decision.md as a trial gate only. The walk prepare default remains guidance 8. Version 9 keeps its original trialled paragraph. Version 10 and later receive the revised paragraph verbatim after guidance 8, in place of version 9's paragraph. Contract-8 validation now accepts version 10. No reviewer success criteria are included in teacher instructions.

The patch was staged during 196/001 but applied only after that process exited and its recovery request was filed. 196 failed final annotation validation before any implementation change; it is preserved, unpublished, with no retry started. Its recovery is separately requested in reviews/requests/commit-000196-001.md. The gate introduces no advancement pause and does not bypass the stopped_failure state.

Verification: actual version-8 (195) and version-9 (188 trial) packets reproduce their complete pre-edit openings, tools and reasoning effort byte-identically. Versions 5 and 6 also reproduce their prior snapshots; the unit fixture retains version-7 coverage. A temporary hardlinked packet copy, with the manifest unlinked before editing, validates at version 10; the system text is exactly version 8 plus the decision's revised paragraph, and all non-system inputs remain unchanged. Version 9's paragraph equals its original decision exactly. No provider was invoked. 196's saved opening remains byte-identical and all seven recovery-request artifact hashes remain unchanged after the patch. The diff is against the immediately preceding implementation rather than Git HEAD.

Required suite: EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests — 280 tests passed in 31.537 seconds. The updated fixture checks version-10 acceptance, replacement rather than stacking of paragraph E, unchanged non-system inputs, and the unchanged version-8 prepare default.

Please review this trial gate. After acceptance, three fresh unassisted trial sessions at 188 and controls 189, 178 will use the approved runs' cutoff evidence under .teacher/trials/ only, between walk commits. They will receive no coverage requests, verdicts, reviewer observations or ledger material. They will never be approved, enter ancestor context, or become journal attempts. The guidance-10-trial-001 request will include drafts, transcripts, coverage, tool-call and token counts. Adoption requires a later user decision.

## SHA256

- reviews/verdicts/guidance-10-trial.decision.md: `9d1dcc4ec73d6465424184fe490b32f8f830ff3ca6a785ed6757f3fd7741c5fb`
- teacher/session.py: `4386aff9144f995f6fe9bc58c6ad5b0006679938c4ae7ad62dc577fb2d4098a6`
- teacher/walk_inputs.py: `7bf0f5a1cfc2088a46491ff790fc518363655d136cfedecdbfa10eeb2aa3f180`
- tests/test_walk_inputs.py: `3e0e2540e5dda09355714e1a35aa84c9173f37ba7f66d6a47e0043cfb58b324d`
- reports/guidance-10-implementation-001.patch: `95153e13e47907adc392cfab5dc97c0f6d4af0254e94325d855be31a72c6a417`
- reports/guidance-10-implementation-001.json: `866c1829eadc81aaf319dc6fa8690051879886a161c987edae26f8aabe1bda09`
- reports/guidance-10-verify-001.py: `5e5d3da16d3bf4f35136c409797bdc394ac676639d61b6e9f2a03204efb92f96`
- reports/guidance-10-v8-before.json: `0286a974db7fe0b964d5086105cb6773e3006c9ccd19785253d32c38b2090f8b`
- reports/guidance-10-v9-before.json: `9544e334afa9b3282c754ac8b7a13e59a5abb7604d67c05d16be74d7d8d10450`
- reports/guidance-10-staging-001.json: `50cbdd07ac1bfa91743db9cdcf18bd566e829f98dda61720e0276383acf98e41`
- reports/guidance-10-tests-001.txt: `adb6764b0bb399ac292ef245a4a51854226d16bcbe61f70c92e278cd73bffedf`
