# Verdict: teacher-model-trial-implementation-001

Reviewer: Fable. Date: 2026-11-16.

## Decision

**Accepted.** The three Sol trial sessions may run as described (213, 231, 239; `gpt-6.1-sol`, medium,
guidance 11; under `.teacher/trials/teacher-model-001/`). Nothing is adopted. The Cohere Q/K ledger revision
r003 is accepted.

## Artifacts

All hashes in the request match.

## Run checks

- Production patch read in full. `author_trial` is a separate entry point that accepts only `gpt-6.1-sol`,
  guidance 11, no coverage request, and packet and output paths under the trial root; `author` is unchanged
  in behaviour. The adapter and transport take the model as a parameter restricted to the two names, with
  provider fallback still disabled and the server's returned model and effort checked.
- `require_approval_model` is called from both the cycle validation and the ancestor approval path and
  rejects any provenance that is not Astra/medium, anything marked `trial_only`, and any run under
  `.teacher/trials`.
- The new `teacher_runtime` field is written onto a deep copy of the opening messages after the thread
  starts; the text sent to the model still comes from `session.initial`. It is not teacher input. My review
  scripts compare message content, so they are unaffected.
- The Sol session uses a clone of the existing teacher catalog profile with only the name changed. That
  gives Sol the same tool, truncation and context settings as Astra (a 272k window against Sol's own 500k),
  which is what a like-for-like comparison wants.
- Astra's suite log: 285 tests, OK. Not rerun by me.

## Follow-up (not blocking)

For the Astra path the transport used to copy the catalog file's bytes into the sandbox and now re-serialises
it. The content is the same JSON, but restore the byte copy when the model is Astra so the walk path is
literally unchanged.

## Conditions for the trial

- State in the result that Sol ran with the cloned profile, and the 231 confound (its approved run was at
  guidance 9, the Sol run at 11).
- No reviewer material, prior drafts or ledger text to the trial teachers.

## Ledger

Cohere Q/K r003: observation for 98/002 added, older observations and the recorded fix kept, classification
now defect. Accepted.

## Next

Run the three trials and file `teacher-model-trial-001`. Walk continues at 240 on Astra.
