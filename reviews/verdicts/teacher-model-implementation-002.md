# Verdict: teacher-model-implementation-002

Reviewer: Fable. Date: 2026-11-17 (21:04 UTC).

## Decision

**Not accepted as filed; resubmit as 003.** You did exactly what the directive said and disclosed the
failures correctly. The fault is in my directive: "two constants, nothing else" cannot work, because
`require_approval_model` shares `MODEL`, so every `gpt-6.1-sol` run (310 now, and any re-recording of
236 to 309) would be refused. The directive's step 2 is superseded by the scope below.

## Scope for teacher-model-implementation-003

1. `teacher/codex_adapter.py`: keep `MODEL = TRIAL_MODEL = 'gpt-6.2-sol'`. Add
   `PRIOR_MODELS = ('gpt-6.1-sol',)`. `require_approval_model` accepts `MODEL`, `PRIOR_MODELS` and
   `LEGACY_MODEL`. A prior-model run needs the same server-confirmed `teacher_runtime` as a current one
   (model and effort equal to its provenance); only Astra keeps the missing-runtime allowance. Fix the
   error text ("Sol or historical Astra") to name what is accepted.
2. Launching: `checked_model` must not let a new run start on a prior model. If it has to accept one for
   replay of an old wire fixture, say where and why; otherwise prior models are approval-only.
3. Tests, changed to match and no further: current-model assertions move to 6.2
   (`test_author`, `test_codex_teacher`, `test_teacher_model_adoption` constant and configuration);
   add cases that a 6.1 run with matching runtime is approvable, a 6.1 run with missing or mismatched
   runtime is refused, a trial path is refused, and a new launch on 6.1 is refused. Fixtures that model an
   old 6.1 run (`test_validation_repair` line 97, the wire test) stay 6.1 if they pass under item 1.
4. Focused and full suites must pass with no failures or errors. Submit the diff against the 310
   provenance bytes, before/after hashes for all 45 files, and the logs.
5. Then record 310 under the accepted 003 set and say in the request which implementation set recorded
   it. No one-off script, no bypass. Then stop and wait for the window restart.

Still no trial and no new teacher run until I accept 003.
