# Teacher model implementation003: 6.2 defaults with historical approval compatibility

Reply-to thread: 01a1eac6-cc72-7af3-9172-36689bd69fc9

Supersedes the unaccepted implementation002 request under the scope in its verdict. Review this implementation change only; ancestor retrieval remains the sole approval scope for entries. Canonical/training remain false.

MODEL and TRIAL_MODEL are gpt-6.2-sol; effort medium, contract8 and guidance12 remain unchanged. PRIOR_MODELS=('gpt-6.1-sol',) is approval-only: require_approval_model requires matching server-recorded model/effort for prior and current Sol. Only historical Astra retains the missing-runtime allowance. checked_model is unchanged and refuses new6.1 launches. Tests cover current/prior/Astra approval, mismatched or missing6.1 runtime, trial flag/path refusal, and6.1 launch/configuration refusal.

Five test files change only model expectations and gate coverage. The wire fixture must move to6.2 because it launches a local fake-provider session through checked_model; accepting6.1 there would reopen old-model launches. The validation-repair fixture also moves to6.2 because it compares the transcript of a newly authored default-model run. Neither is a historical-run replay. No teacher trial or corpus generation occurred.

Host-enabled focused suite:35 tests,0 failures/errors. Full suite:338 tests,0 failures/errors (479.808s). Full log includes ResourceWarnings concerning existing tempfile/HTTPError cleanup; suite result is OK. Logs and structured results are bound. The diff is against the exact310 provenance adapter bytes (baseline SHA verified); all45 production before/after hashes are bound, with only teacher/codex_adapter.py changed. Test diffs/hashes are included separately. Initial002 evidence is retained unchanged.

310/001 is approved by its verdict;16 request bindings and the published request hash were verified. Its unchanged6.1 provenance/transcript now pass require_approval_model. The queue implementation gate compares orchestration hashes, which are unchanged and match310. Recording is deliberately deferred until003 is accepted, as item5 directs:310 will be recorded under the accepted003 implementation set, with no temporary restoration or bypass. It has not yet been recorded, and next_position remains311 with advancement paused.

309's ledger record is accepted by310. Six310 records are filed here: three new suspected findings (stale speculative mask, conditional prefix reset/None.encode, list-valued vocabulary cache argument) and carried revisions sorted-argmax r003, checkpoint-token-attribute r004 and terminal-string-bypass r004. Existing identities/observations are preserved; source/scalar limits, conditional external reset semantics and canonical/training false remain explicit. All six passed schema/evidence validation. No reviewer notes enter teacher input. Canonical follow-ups remain administrative: sampler logits type when added to the half mask; matching active-filter f_idx iteration in submit/join loops.

STOP: no new teacher or trial. Await003 acceptance, then record310 under003, and await the user restarting the author window on6.2 before further walk work. First three6.2 entries require full-depth review and results to the user. No commit or push.

## SHA256

- reviews/verdicts/teacher-model-002.directive.md: `1604022e657eba824cea342a030ebe7ed088b6ab54545e14d51750ece5a5634e`
- reviews/verdicts/teacher-model-implementation-002.md: `180499c7d152b7618f0d9035b8904ee56bbe541449a5da86349e425ac22f0677`
- reviews/verdicts/commit-000310-001.md: `ace3878dd9b5c31909e296ecb864638740c6a20f3fc06497eb139d6b56c59b72`
- reviews/requests/teacher-model-implementation-002.md: `c331fb62c63ea7330b6caab043af5c5064e8d1f98c8576101ae2bc11730e0f95`
- reviews/requests/commit-000310-001.md: `0ea49b46aa847d1975de8a709c3df46f81f5d3fe6ea56ee23d024134ad0d7b04`
- reports/teacher-model-implementation-003.diff: `16e2d59a3b7d2b4f42932c6749d094ea5c1f6bdcd463144654f462460a2c7d05`
- reports/teacher-model-implementation-003.hashes.json: `2df714030bc9674eb66f92eccca300a77bf8d0620586acfe225cd9362b07cd46`
- reports/teacher-model-implementation-003.audit.json: `b28045088a8b2b7c38ebc145a88ace02162e92deb2b38777c36342fc63f4b452`
- reports/teacher-model-implementation-003.tests.json: `bf5a9094839ea8c4143fb89488113e5b781da89d618c5ca52364c39ddd144677`
- reports/teacher-model-implementation-003.focused.log: `0b2fea306786dec0890445bc5e682c39b3b5937d5dc470f86b7053dc201d4edc`
- reports/teacher-model-implementation-003.full.log: `bce5b4655f4ee3ee9a5bd65ec4f3a27f97e39bc1050aff3d5fe5af716145885e`
- teacher/codex_adapter.py: `14172b70b8c08acd31d9118dd243d4b5bb788344af834fb2fdbf5033910d353b`
- tests/test_author.py: `4f6c8840320b22dbb012ac2720006da897b0cef80e209c25cf0467964285a02f`
- tests/test_codex_teacher.py: `b2e16be8742151b7ccbf9674d3ceeb598243179d36efb76d52439d9f5d96a843`
- tests/test_codex_wire.py: `b8adcbf264f9d83eacdd4881133774ba5281a3b8d2fed2bc836d31ea4eae1184`
- tests/test_teacher_model_adoption.py: `d84743e8e637887206914d9f4b2b642e345987705e72c4180cae81af2b9c1cc6`
- tests/test_validation_repair.py: `914593983d57fda0500f990b12831d34681347723da4ff3363cafeec033475be`
- reports/commit-000310-ledger-001.json: `73ab13788398effc9d1abbb9963d8f72903bc8097ea6abdb104693fead82e1be`
- reports/defect-ledger/exllamav3-speculative-mask-not-refreshed--r001.json: `7cb5f740beba81828f39734c777093016e85b62dc4a0fe1ae7f37e0bf58d46ad`
- reports/defect-ledger/exllamav3-prefix-not-replayed--r001.json: `3068ee705f85c9ff9c447e1c42b915b278e0cb2a796e16b7ebe168a6e9e94b03`
- reports/defect-ledger/exllamav3-vocabulary-cache-list-argument--r001.json: `feb9631f58d128ccc26d3b9e1660cc6f25ba73a6945170320c5c87b2b4efd571`
- reports/defect-ledger/exllamav3-sorted-argmax--r003.json: `67d322352846072afc9637271f722cb195887b830a9cb7f20df236a153aaa8b7`
- reports/defect-ledger/exllamav3-checkpoint-token-attribute--r004.json: `b1a54964b9bdb1c9fb11b552248d6ab13fb2fc8a2b9df77b627243d3267bfc33`
- reports/defect-ledger/exllamav3-terminal-string-bypass--r004.json: `6f4f4104d24f2f90ef2bf9afb6e213f40cda82daa227f20fec070bcc17fc29b1`
- reports/defect-ledger/evidence/commit310-001-draft.json: `57ef485fa408c1797cd889af0f87a42d5a1f09a3b1226b7e24caf7607e71953a`
- reports/defect-ledger/evidence/commit310-001-transcript.json: `9ff63b504d2d45e99e151eac134b23958864f61cb92bc301bffcefe92fc3d503`
- reports/defect-ledger/evidence/commit310-001-verdict.md: `ace3878dd9b5c31909e296ecb864638740c6a20f3fc06497eb139d6b56c59b72`
