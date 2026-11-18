# Review of Fable’s staged revision-attempts-implementation-002

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

**Changes required.** This reviews `reports/revision-attempts-implementation-002.patch` at SHA-256 `5f2142eddaef52b62e286e29a42c3171bb8f67902a2b846e4072eaf6489d2c58`. Fable subsequently withdrew those bytes and endorsed the separately staged author candidate in `reviews/verdicts/revision-attempts-implementation-002-review.md`. Deployment of that candidate remains pending patch selection under the user’s roles swap. The 327 session continues on v3.

1. **Coverage admission.** The fixture `test_coverage_gate_runs_on_exact_bytes_and_refuses_facts` deliberately admits a sentence telling the teacher to check 1024 and 4096 for a default. The filter only detects identifiers. Require exact-hash coverage in a bounded pointer-question format tied to task or parent paths. Test refusal of that sentence and a plain declarative fact containing no identifiers, before reserving an attempt.
2. **The revision source.** `prepared()` accepts a forward retry at the right position and matches the supplied manifests. `author_revision()` then accepts a same-position name and an authorization file digest. Tie the revision to the specific stopped queue token and its recorded rejected run and verdict, the original packet and manifest digest, the task SHA and the coverage digest. Exercise the prepared dispatcher with an incorrect same-position source, a copied packet and an eligible source. The decision also permits revising a declined replacement. Exercise that route with the previously approved ancestor still active through approval of the revision.
3. **Replay and approval.** Drive a revision from `prepared()` through `validate_run()` and publish and approval, including a changed imported result and coverage attachment. The standalone `ancestor_context.approve_run()` currently reads imported evidence through `prior_view()` and verifies citations without re-deriving the revision input or replaying the original records. Require the revision checks at that entry point or route revision approvals exclusively through the queue. Bind both transcripts and include the kept, added, removed and corrected sections in each request. Flag the first live revision for line-by-line review.
4. **Token totals and evidence IDs.** Scope usage events to the active thread and turn. Record input, cached-input and output totals from validated cumulative fields. Report comparable totals for both runs in each of the first three requests, with unavailable totals explicit for older sources. Preserve the accepted full source transcript digest in evidence IDs, or get approval for a versioned shorter form.

## Verification

Live v3 passed all 340 host-enabled tests. The exact submitted patch passed all 357 host-enabled tests in isolation, including all 17 focused revision tests. It also passed the live apply check.

- reviews/archive/revision-attempts-implementation-002-author-candidate-request.md with SHA-256 `44893a51aa946b719c677db20b6331d4597a6098e9fd00c542671a3cfd7685b3`
- reviews/verdicts/revision-attempts-implementation-002-submission.md with SHA-256 `0557a559c5aaad5c42c92bc2431404ef3d17ae77b69975b2290f52594099fa3d`
- reviews/verdicts/revision-attempts-implementation-002-review.md with SHA-256 `db0dc2c9486ed4eef6c7983e58b743850d30f6e1ee8340861e823bbe6a9e2c35`
- reports/revision-attempts-implementation-002-review-isolated-focused.log with SHA-256 `49d2338c83d6fa941bdf72683748114ad7b33a2e916285f0cb26a22eae8e6096`
- reports/revision-attempts-implementation-002-review-isolated-suite.log with SHA-256 `e691ea418ff9347fdd8139035d35927cf0862a7f28ece9d459e5d5967f8215c0`
- reports/revision-attempts-implementation-002-review-live-suite.log with SHA-256 `406dedef7c9d258efdf53eae5ab95cb4568f810ff9a6f9937e010647ab82dc6a`
