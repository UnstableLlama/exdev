# Run-ahead implementation 002 — completed implementation

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Please review the completed implementation against the accepted design and its five conditions. Live use is disabled until this request is accepted. The production journal is unchanged: stopped_failure at 255, no active session, no run_ahead configuration. No teacher session was started for this implementation. Nothing is committed or pushed. Revision mode remains separate and follows this implementation.

## Implementation and conditions

The opt-in `orchestration.run_ahead` driver uses the existing full-session lock and a separate short, atomic queue-update lock. Explicit migration preserves legacy handovers, sampled mechanical references, pending replacement reviews and existing pauses/stops. The combined cap is three reservations/unpublished drafts/pending requests across replacements and forward work. A completed draft must be filed before another launch. Every run under this driver requests review; it does not silently advance through mechanical approvals.

A reservation binds an approved-entry snapshot and each pending position's exact run, changed paths, overlap Boolean and overlapping paths. Root commits and merges are handled by the union of changed paths against parents. Requests disclose `Ran ahead of: N, M.` and the overlap details; these administrative dependencies never enter teacher input. The sparse packet retains complete source ancestry while its prose catalog contains only approved strict ancestors. Attachment checks approved artifact hashes; completion checks exported prose, source parents/date and launch-time approved selection. The isolated reader uses that same selection.

Rejection/hold stops new launches immediately. A session already reserved may complete; later runs remain immutable for reviewer judgement. Failure or interruption stops rather than freeing a reservation for automatic reuse. Recovery requires a bound reviewer/user decision and operator judgement; authorized retries block unrelated work until their verdict. Forward approvals require every earlier forward position to be approved. Recording an older approval preserves next_position, active_session and all other queued work. Replacement approval switches only the approved-entry selection and preserves old artifacts.

Approvals identify an exact run/request filename and hash, check the request's artifact fingerprints and verdict bindings, replay existing deep validation and retain model, trial, assisted-input and ancestor-only gates. Orchestration implementation hashes are administrative bindings checked at approval. No existing teacher module was edited by this implementation. The sequential-identity test compares the packet and blob bytes, initial prompt, runner command and provenance implementation hashes with and without the adapter; all are identical when the full ancestor selection applies.

The detached notifier reuses the accepted queue transport (exit 0 with Queued message is success), saves failure/results, terminates its child on interruption and sends one notification. Duplicate/stale completions are refused by reservation identity. Prepared replacements/retries share the same teacher lock and queue, retaining accepted-plan preflight and immutable-packet requirements.

## Reviewer watch and operation

`status == running` still means a session is reserved through preparation/execution; `active_session` is its reservation token and becomes null on completion. The stall-check assumption remains valid. Request filenames remain exact run names, so the request-without-verdict pending rule remains valid. `reviews/fable/watch.sh` only adds the new module names to its process search. Its shell syntax passes. New driver commands, migration, request disclosure and recovery limits are documented in orchestration/README.md.

After acceptance, migration is explicit and must run only while inactive. It does not lift the current 255 failure. Use this driver for state mutations after migration rather than mixing in the legacy handover-based commands. Approval writes review.json before committing the journal transaction; a crash between those writes requires manual reconciliation against the bound verdict. Architecture stops and the end of history also stop for administrative judgement. No live provider smoke run was made before acceptance.

## Validation

Full host-enabled suite: 311 tests passed in 58.741 seconds. Focused host-enabled suite: 24 tests passed, including an actual isolated sparse reader; no teacher/provider invocation. Full-suite output includes ResourceWarning diagnostics but finishes OK. Coverage includes migration, opt-in gate, mixed capacity, overlap, unfiled requests, explicit pauses, rejection during an active session, crash/stale completion, transactional concurrent updates and rollback, exact request/verdict/artifact bindings, ascending approval including historical failures/mechanical entries, replacement supersession, model-validation refusal, recovery constraints, pending-prose omission, malformed selection refusal, byte identity and notifier failures/signals. Machine: Linux aarch64, Python 3.14.4.

## Bindings

- orchestration/__init__.py: `68915857024c488a95f5e3551c720604a70120c5551b9ece25b8ddb79e88954a`
- orchestration/run_ahead.py: `93d7ba2c158d9db84fb6b38e16eed38e151377cd051fea9678c82d5f7d3b2937`
- orchestration/ancestor_selection.py: `d28216a56e79cd9ab0de457967cc5218622a8a3c198f798f1490826c06302d2c`
- orchestration/notify.py: `db348ead800ebaba14c6e1a061831ee869a733113be2765ef07ac5590948e821`
- orchestration/README.md: `24249581995808514100413ac93035975a8d91807c215ce20ee10eb0d49d547b`
- tests/test_run_ahead.py: `e3308900985cb4a7113999c99d21aa1f3799714d1155dd5717a8247583a665d0`
- tests/test_run_ahead_notify.py: `2a56d1b33ce86159131f001367897c231e8d7ae34cb58c6f11a67d27afebda46`
- reviews/fable/watch.sh: `92d0f78cd9b834a22c16be6d9a7351aa8abdc1b24a231a1a0abfce6ef9e87730`
- reports/run-ahead-implementation-002.patch: `31c66b437f15b882803c778ace67f7ddf3e595643a6d96307243440066858eb3`
- reports/run-ahead-suite-002.log: `77dbe8e8c54aa9277f3dfb8e5ee09a1e3fa7f3371d53031f18749c46d6b8991e`
- reports/run-ahead-focused-002.log: `975a24512387df77f9e51a52f4874f3082f5cf4743d4c3fe8da333087c9d1e92`
- reports/run-ahead-verification-002.json: `42dc1b549eceed037c6272bbdf92362094d48ab16c0c45a0e2c6e0445ea6bb39`
- reviews/verdicts/run-ahead-implementation-001.md: `24f728a7a01df04f167d79cfbfd6d3e7b2e7c38638f2643ec8c6c32b767314ef`
- reviews/verdicts/run-ahead-001.decision.md: `0fbb5b4728164d65bd51a5e883831e2bac825d7fcf64ddb4f0095ce0fbeeedb0`

Reply in reviews/verdicts/run-ahead-implementation-002.md. No live run-ahead until acceptance.
