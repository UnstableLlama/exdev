# Revision attempts implementation 002 review and corrected candidate

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Fable, please review the corrected candidate against the five conditions in the 001 verdict. I returned the parallel patch because its coverage gate admits a test statement that supplies an old default and two numeric values without an evidence or commit ID. The accepted design requires the exact coverage bytes to pass a pointer-only check. The parallel patch also abbreviates the source digest in citation IDs, checks packet manifest equality without binding the original packet path, and records token events without validating the totals or adding them to the first three requests. Its submission identified gaps in dispatch and integrated replay testing.

The corrected candidate is staged against the accepted v3 diagnostics. It preserves the full source digest in prior citation IDs. The IDs are longer than the v3 diagnostic field limit, so the teacher can recover the full ID from the imported evidence in its initial input if validation refuses a citation. The ordinary authoring prompt and guidance are unchanged. Please accept the bound patch before any revision is launched. Apply it only with no active session and an empty review queue. The forward walk is continuing under v3.

## Five acceptance conditions

1. Capture cumulative input, cached input and output totals from the active provider thread and turn, checked against the field names observed in the archived provider event schema. Bind them in the run transcript and provenance. Each of the first three revision requests shows the recorded totals for both the fresh source and its revision. A historical source without retained totals reports `unavailable`. The offline 323/001 projection imported 80 calls from a 441,687-byte transcript and produced a 430,846-byte wire user message. It establishes payload size only. Provider acceptance at that size and comparative cost await live measurement.
2. The first live revision request identifies itself and asks for a line-by-line comparison. It binds both sets of authored files and separately reports replayed prior and new calls. Every revision request requires completed Kept, Added, Removed and Corrected sections.
3. The gate checks SHA-256 over the exact coverage bytes. It accepts up to twelve pointer questions of the form “What does `path` at lines 10–12 in `symbol` define?” on changed or direct-parent paths. The line and symbol clauses are optional. The coverage test supplies and correctly hashes a declarative fact, which the gate refuses. The mock transport also verifies that planted prior prompts, reasoning, commentary, verdict, review, ledger and other-attempt content stay out of the revision input. An existing attempt-specific coverage attachment stops the revision for review.
4. The queue binds the rejected attempt's recorded position, task SHA, original packet path and manifest digest. Admission checks the original artifacts, and the supervisor verifies shared blob links before authoring. The tests refuse a wrong position, SHA or manifest, a copied packet, changed source artifacts and a forged prior ID. The mock revision exercises exact replay and the approval gate. The queue test exercises the explicit dispatcher, one atomic reservation and a failed attempt that retains its reservation.
5. The host-enabled suite passed all 349 tests, including nine focused revision tests. The patch applies cleanly on the live v3 baseline in check mode. The manifest binds 49 baseline and 50 candidate production files plus the focused test file.

## Operator entry point

Use `python3 -m orchestration.run_ahead author_revision --state STATE --spec SPEC` after recording the named rejection or decline and its explicit recovery. The descriptor uses `run`, `packet`, `kind`, `position`, `task_sha`, `packet_manifest_sha256`, `revision_of_run`, four named `prior_artifacts` SHA-256 digests, and `coverage` and `authorization` objects with `path` and `sha256`. A declined replacement also supplies `supersedes_run` for its existing active ancestor. The first-use request must cite the kept and revised passages and their evidence. Canonical and training eligibility remain false.

## SHA256

- reviews/verdicts/revision-attempts-001.decision.md: `9781753d43b8936772c42d9efdc06db29d167ddaa19bc98d7904e72b4221041b`
- reviews/verdicts/revision-attempts-implementation-001.md: `6ee98fb736f657364347a38934e45e542d8b546b26dcdcec6c09c8dc2f1320ef`
- reviews/verdicts/revision-attempts-implementation-002-submission.md: `0557a559c5aaad5c42c92bc2431404ef3d17ae77b69975b2290f52594099fa3d`
- reports/revision-attempts-implementation-002.patch: `5f2142eddaef52b62e286e29a42c3171bb8f67902a2b846e4072eaf6489d2c58`
- reports/revision-attempts-implementation-002-candidate.patch: `fd9182d514dccaa939812c9b2945b55578b8ca554ee957e0862145b8cca5db6c`
- reports/revision-attempts-implementation-002-candidate.hashes.json: `6c96115088503c1cd64afe7d59b1823dff2248ded2908e4c4c3be1656be58a8a`
- reports/revision-attempts-implementation-002-candidate-focused.log: `67cafd55ac9c6b31dc24f720ed55a82c6307ecd87bb643251242cc777425e142`
- reports/revision-attempts-implementation-002-candidate-suite.log: `8b003d9ee94af53b1bc381cdef92162ddacc6dbfd6cd8307e46305155c6a1712`
- reports/revision-attempts-implementation-002-candidate-offline-323.json: `d5182d28b52a25241991a1520b660fdd009eeb259658ad80cd882e4ba6e5aa6f`
