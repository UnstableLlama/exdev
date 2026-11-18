# Validation repair implementation 002 — completed change

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Please review the implementation of the accepted design. No live teacher session used this change. Nothing is committed or pushed; journal, packets, authored runs and approvals are untouched. Live validation repair remains blocked until this request is accepted. Scope remains ancestor retrieval only; canonical/training stay false.

## Behavior and boundaries

`CodexTeacher.run` validates a completed final inside its event loop. An eligible first refusal preserves the exact final text and exception, then starts one additional turn on the same server thread, with the same model, effort and output schema. The sole input is `str(error)` verbatim: no prefix, suffix, explanation or other message. Further historical tool calls are permitted. The existing call-ID set and budget span both turns. The second refusal is terminal.

A successful first final retains identical opening inputs, transcript shape and draft bytes; only provenance gains the policy/repair fields. Versions of guidance, editorial rules and JSON schemas are unchanged. `author(..., validation_repair=False)` disables feedback for 255/004, which must retain its previously authorized rules. This opt-out is tested and recorded as `validation_repair_enabled`.

Protocol/runtime errors, failed or missing turns, foreign thread/turn events, native tools, duplicate calls, budget exhaustion, packet mutation, transcript-integrity errors and unexpected internal errors remain terminal. Failed runs retain their transcript and failed status and publish no draft. The transcript is saved before feedback is attempted and after subsequent events. `feedback_sent` records the successful turn-start acknowledgement; a disconnect with uncertain delivery leaves a failed run, never an approvable repair.

The shared `validation_repair.verify_final` is used by authoring, assessment, deep validation (through assessment) and ancestor approval. It requires exactly one structured refusal event, exact refused bytes/hash, exact adjacent feedback, distinct turn identities, an unambiguous selected final, and matching provenance. It reproduces the original exception type and message against the transcript prefix available at the first final, then validates the selected complete annotation against all evidence. The published annotation and rendered Markdown must match reassembly. Fabricated refusals of already-valid annotations, extra turns/messages, altered feedback and ambiguous selection fail closed. Historical unmarked runs retain their old path. Model/runtime/trial gates are unchanged. A repaired run always requires full review.

Replay invokes every tool from both turns, including failed tool calls, through the existing runner. Reports/skeletons disclose `validation_repair`, refused/input hashes, selected index, exact message, one repair, calls before/after and total. The FIRST LIVE REPAIRED request will explicitly flag that status so Fable can compare refused and final annotations. This feedback does not itself create reviewer assistance; packet coverage assistance remains separately labelled. Future revision import must use this verified final selection; revision mode is not implemented here.

## Complete validator-message audit

The unchanged `teacher/editorial.py` has these nineteen fixed annotation refusals (none interpolates external text):

- `Duplicate ancestor link`
- `Links require approved, supplied ancestor prose`
- `Chapter output does not match assigned subsystem`
- `Duplicate chapter ID`
- `Duplicate chapter reference`
- `Claims, including inferences, need evidence anchors`
- `Duplicate evidence anchor`
- `Duplicate finding evidence`
- `Findings require successful current-session evidence`
- `Duplicate finding ID`
- `Findings require inspected source evidence`
- `Ancestor links require a successful nonempty prose read in this session`
- `Unknown or unsuccessful evidence call`
- `Ancestor-only claims require basis ancestor`
- `Ancestor basis requires ancestor prose evidence`
- `Execution claims require successful run evidence`
- `Finding locations require repository-relative paths`
- `Source inspection requires source evidence`
- `Computational verification requires successful run evidence`

Schema-shape refusals are a fixed schema path rooted at `annotation`, followed by one of `: wrong type`, `: incorrect version`, `: unknown value`, `: missing or protected fields`, `: invalid number of items`, `: invalid length`, `: invalid format`. Paths come from schema keys and array positions, not reviewer content or arbitrary annotation keys.

Assembly coverage additionally permits `Required evidence not fully read: ` followed by the missing historical section headers/source IDs, and `Assigned computation requires a successful run`. Internal messages `Read metadata does not match returned bytes`, `Assigned external evidence missing from packet: <source_id>`, `Duplicate evidence call ID`, `Unmatched evidence result`, and `Unsupported editorial schema version` are terminal. Evidence-ledger and observed-read integrity checks run outside the feedback catch. Tool-result JSON errors encountered there also remain terminal.

The JSON path permits the original `json.JSONDecodeError`, without rewriting its string. Python 3.14 decoder families are `Invalid \uXXXX escape`, `Unterminated string starting at`, `Invalid control character ... at`, `Invalid \escape...`, `Expecting property name enclosed in double quotes`, `Expecting ':' delimiter`, `Expecting value`, `Expecting ',' delimiter`, `Illegal trailing comma before end of object`, `Illegal trailing comma before end of array`, `Extra data`, and `Unexpected UTF-8 BOM (decode using utf-8-sig)`, with the decoder's line/column/character suffix. Accelerator wording can differ; the exact emitted string is preserved and must reproduce. Invalid-character/escape messages may contain the teacher's offending character; offsets and line numbers derive from its final JSON.

Python's integer-conversion `ValueError` is also permitted in its exact emitted form: `Exceeds the limit (N digits) for integer string conversion: value has M digits; use sys.set_int_max_str_digits() to increase the limit`. N is the host limit and M the teacher's digit count. Other ValueErrors and non-ValueError internal exceptions remain terminal. No eligible error obtains reviewer, ledger or other-attempt text. The only variable feedback is schema location, historical missing-evidence identifiers, teacher JSON characters/positions or digit counts.

## Validation and diff scope

The focused suite covers unchanged first-pass bytes, exact same-thread feedback with planted-secret exclusion, additional reads and prefix-only refusal reproduction, complete-final selection, terminal second refusal, cumulative budget/duplicate IDs, initial and repair-turn failures, packet mutation/internal/save failures, failure persistence, strict metadata, disabled repair, forged/altered events and rendering, failed/catalog-only/unknown evidence, source/execution requirements, and exact replay of both turns including failed tools. Legacy author/editorial/model/approval tests run with it. 42 focused tests passed in 0.539 seconds; all 326 host-enabled tests passed in 54.545 seconds. The bound report records commands, runtime and hashes. Mock transports exercise the repair; no quota-consuming/live teacher test was run.

The scoped patch uses the five source-file SHA-256 baselines bound in design 001, rather than including unrelated uncommitted changes. It adds the shared module and focused tests and a README paragraph. The results report binds old/new source hashes, unchanged editorial/schema hashes, test commands/counts and logs. The full suite exercises the final implementation; the README addition is documentation only.

## Walk and remaining work

255/004 is unstarted and separately awaiting direct launch authorization after automatic approval review rejected the detached launch. This implementation does not bypass that stop; 255/004 must disable repair. Then replacement 234, sequentially. Run-ahead migration remains subject to its accepted conditions and separate migration request. Revision implementation 002, including production token retention, follows this review and remains unavailable until accepted.

## Bindings

- reviews/verdicts/validation-repair-001.decision.md: `a4a0c0bdddede4403e15da64401d397ff2066da32e28f16ac4024e9fd0977c69`
- reviews/requests/validation-repair-implementation-001.md: `3a0fff160c1ada017881b2755aa1422d3c5525843af8453503d80df248abac01`
- reviews/verdicts/validation-repair-implementation-001.md: `68be4272366bd905008ef11c3bd15d554bf72af590b78223ef3eb6fef9f82de5`
- reports/validation-repair-implementation-002.patch: `fd9372eef66fea63181600a694d576d3994025dca28ab8e7080092e0020d55ef`
- reports/validation-repair-implementation-002.json: `0cd98a9ffeabd4ceb1673ea99136bc2263933d66b11b4f1d25a825758a32d253`
- reports/validation-repair-focused-002.log: `4da35be5103e8a7e58aaa4d387a19da3217d3b39e488fb18908e95acd259f730`
- reports/validation-repair-suite-002.log: `3dfe3a0961d4bcd33aa5e68f9932df2d3919d65e918f6fb0c9ea876c645f827b`
- teacher/codex_adapter.py: `9540b6701d5ceb44c28af78ec9f38fa80038637a37e10563c181c0696b14e190`
- teacher/author.py: `65ed85016638dddb7cf0c2a023b1a6e231203d8326179dc4aa921c2730670372`
- teacher/ancestor_context.py: `17a638083469556bdae037ea71abd878e3c99b8ae6d42ddf6beab97d61f7a076`
- teacher/approval_policy.py: `ab93fe1210d2956141631522b9d7fb94313aaad89151f55c43db0b6b40f39bd9`
- teacher/cycle.py: `5c3768624cb16f134a5428a34687bea7eb70bc2626f909065d3676626a246e9e`
- teacher/validation_repair.py: `08ee8fa35a6dbf1cb2e3fddeea9ab89f92652d95668f5cfeedc1581cc0e9b8c3`
- tests/test_validation_repair.py: `942d118c9fb550cee5e1c18c0b3956cca31070b6c63d809d4351bdda2b13b68a`
- teacher/README.md: `4cf1c0ca435e8887734ec1d5b8281f928c4b194f39981c16e0e0bca514d442a3`
- teacher/editorial.py: `92d39a4364126b5a39f3436267dda1ffff6c007b5a9830d9a7f003d0a29b8316`
- schema/editorial-annotation-v2.json: `9d2a79c70520903be88f08a59e5b5510971c09582267d090cc573bbff85d0c05`
- schema/editorial-annotation-v3.json: `6f12144c1bf4a856523eb0e6d3c4fe7e0658e2f28bd769c17d69f337c9df47f1`
- schema/editorial-annotation-v4.json: `bdb7970bd32a795d5ebd47da93ae48537297603a1b30c8efcddbecd6a697fab7`
- schema/editorial-annotation-v5.json: `fcc2fd50c4a093b3bfd78cef0b75c31ce6aec09b4111ffa83e3b48cb9136b68b`

Reply in reviews/verdicts/validation-repair-implementation-002.md. No live repair before acceptance.
