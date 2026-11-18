# Teacher model implementation002: directed6.2 constants, failing checks disclosed

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Author/orchestrator: gpt-6.1-sol / medium. Future teacher default: gpt-6.2-sol / medium.

Request review of the exact two-constant change directed in teacher-model-002.directive.md. In teacher/codex_adapter.py, MODEL and TRIAL_MODEL are gpt-6.2-sol. EFFORT remains medium, contract8 and guidance12 unchanged. No other implementation or test file changed. The bound diff is against the exact310 provenance bytes, reconstructed and hash-checked; all45 implementation hashes are supplied before/after, only adapter differs.

309 was submitted and approved.310 had already started on6.1 before the directive arrived; it drained successfully and its unchanged request is now filed, with the309 ledger record. No teacher was active when the constants changed. No new teacher or separate trial was started. Advancement remains paused; stop here until implementation acceptance and the user restarts this author window on6.2. First three6.2 entries require full-depth review and a result to the user. No canonical/training approval, commit or push.

Tests were run host-enabled. Initial adapter/wire set:8 tests,1 failure/1 error. Expanded focused set:30 tests,3 failures/2 errors (log filename retains focused20, actual count30). Full suite:337 tests in202.613s,4 failures/3 errors. These are not passing checks. Four assertions expect6.1 in model/config/provenance/transcript; explicit6.1 wire/approval tests now fail the supported-model gate; the trial fixture reports old6.1 runtime. Logs and structured outcomes are bound below. Tests remain unchanged under the directive's “Nothing else” scope.

Compatibility issue requiring resolution before resumption: require_approval_model shares the changed MODEL constant, so it now rejects6.1 provenance, including pending310. Historical Astra remains supported. No approval bypass, recovery or broader compatibility change performed. This exact directed patch is reviewable but not ready for unqualified acceptance on the current checks. Reviewer should address the test/gate implications before author restart or new teacher work.

## SHA256

- reviews/verdicts/teacher-model-002.directive.md: `1604022e657eba824cea342a030ebe7ed088b6ab54545e14d51750ece5a5634e`
- teacher/codex_adapter.py: `818d7098dffd76b456012f1f926d7a2111ea2398e2db628c68e2c09a7020df68`
- reports/teacher-model-implementation-002.diff: `4d496132034c0b0c3e60c03e0a79166920359538c6daef66c6bd363127ad67b3`
- reports/teacher-model-implementation-002.before.json: `e64eb234e44b1489b676b9efad1af2ebd270a5305c00993054fbdc4b142af79d`
- reports/teacher-model-implementation-002.hashes.json: `fbae330bd26f6a95df187b48436117e8d4e25a0031197a32d6fc33689132d665`
- reports/teacher-model-implementation-002.audit.json: `88deaeed51b0b6e2c7ec5c0f093e729a1987c77e5394fa02a7c29bde4026e464`
- reports/teacher-model-implementation-002.tests.json: `430c69279947979d17b361bce5197ef3e946012d336097733b3f885a44db76ee`
- reports/teacher-model-implementation-002.focused.log: `5a1b2fdb3069dcfc18ee6abb17302dda33999b93be461939b8b92eda7fed4808`
- reports/teacher-model-implementation-002.focused20.log: `688680ac5350f17264df5e2c86f223d4747cf72ef0f8795b4e477b8132c3e9b7`
- reports/teacher-model-implementation-002.full.log: `f9429367997a8b6418d94ce169bd9b894e3c4c8e926c24cdb60425bd796b74c9`
- reviews/requests/commit-000310-001.md: `0ea49b46aa847d1975de8a709c3df46f81f5d3fe6ea56ee23d024134ad0d7b04`
