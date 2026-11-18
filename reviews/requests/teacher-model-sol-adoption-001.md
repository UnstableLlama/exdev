# Teacher model: Sol adoption implementation 001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Request acceptance of the user-authorized Sol/medium default. No new teacher session has started; 242 completed on Astra/medium/guidance 11 and its request is filed separately. The journal explicitly blocks advancement pending this implementation verdict. Nine remaining replacements remain held until acceptance.

The default MODEL is now gpt-6.1-sol, effort medium. Historical gpt-6-astra remains supported. Both cycle validation and ancestor approval use the shared model gate: production Sol/medium or Astra/medium only; trial_only and .teacher/trials paths rejected. Recorded server runtime must match provenance. Compatibility qualification: old Astra transcripts predating runtime recording retain their existing eligibility when that field is absent; Sol cannot omit it. Incorrect recorded runtime is rejected for both. The audit checks all 240 active Astra/medium entries; the assembled root has no model provenance and is left untouched, not newly approved by this gate.

Transport retains the accepted cloned catalog profile for Sol (only slug/display name changed), and the exact byte copy for Astra. Existing server-model/effort verification and runtime/provenance recording remain. Instructions, tools, sandbox, budgets, guidance 11, catalog source and historical artifacts are unchanged. Cycle summaries and generated requests now name model/effort. The audit compares production source hashes against 242's provenance: only codex_adapter.py, codex_transport.py and cycle.py changed after its validation. Other dirty repository changes predate this adoption.

Tests cover both model/runtime combinations, mismatch/unsupported model/effort rejection, trial rejection, missing-runtime behavior, default configuration and existing host wire paths. The first full-suite run caught the former test expectation that Sol must be rejected; that expectation was updated. Its failed log is retained. Final full-suite result and hash follow below.

Acceptance permits future forward runs and the nine remaining replacements on Sol under the accepted replacement plan; this request does not approve any teacher output. Canonical/training status is unchanged.

## SHA256

- reviews/verdicts/teacher-model-sol-adoption.decision.md: `d83f768e25c1ba4894071335f4db31fa8736a882cbb5629eee8bf84be6a925ac`
- teacher/codex_adapter.py: `740facbdf0fd0d1d7c9d0e5ba6f35f0b6eed4d8df16c616e8ca9f7a9f443ba74`
- teacher/codex_transport.py: `1159e118ed31d274d773e3a4531c221ddcd565a47e761a05bf923975dfa94124`
- teacher/cycle.py: `4103ed73615c11dc219eac0a95bf0a48eb1d3e0a23421988245059071adf0a60`
- teacher/README.md: `2c62e9d677e5c0b28f843e2d5a77b87427386bf474b8d6eedd8d56c327a82386`
- tests/test_teacher_model_adoption.py: `affd4b018a41a790b064ea7f160264e3a62b62a1ca2e54126611cad0f7cf4186`
- tests/test_ancestor_context.py: `009079388d65bcc871f85f144cc8bff7949c5f91b4bf6f452fac1ee2dbae3fb8`
- tests/test_author.py: `5243da484eae3869f03f7eb7866b955e6f84175bb13a40809a35a4e648133661`
- tests/test_codex_teacher.py: `5a54e13d1d8316ada407beedc2e3c0b0be7e9ec797e4d924d3eeed1dfc82a0af`
- tests/test_cycle.py: `27e7123ad94e7908eb0107eb9fe889c533eb3a9320934894de91e6c2e857be51`
- reports/teacher-model-sol-adoption-audit-001.json: `4fb4b8a8087e028628482656782e56bd66b0c72a9129630305edb769e766dd02`

Validation: `EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests`: **287 tests passed**, 45.273 seconds, Linux aarch64 / Python 3.14.4. ResourceWarnings were non-fatal.

- reports/teacher-model-sol-adoption-tests-001.log: `0b0484e7747a4b62e420a3088a107098c00eb5b28f8acb1f7256d13fdf874467`
- reports/teacher-model-sol-adoption-tests-002.log: `e47abfb218211ebf4048e084d886829aa5f0e71557a391fe22b6759b293479f3`
