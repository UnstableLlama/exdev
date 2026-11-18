# Validation repair implementation 001 — design for review

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Please review this design under the user's validation-repair decision. No implementation or teacher session is included. This comes before revision mode; the completed run-ahead implementation is accepted, with migration and live-use conditions still outstanding. No run, journal, annotation or approval is changed by this request. Nothing is committed or pushed.

## Session loop and exact feedback

Today `CodexTeacher.run` ends its event loop on a successful `turn/completed`, then parses the final JSON and calls `assemble_draft`. Move that final parsing/assembly into a bounded two-turn loop. Only a refusal from JSON parsing or ordinary annotation validation is eligible. Transport failures, foreign events, runtime/model changes, unsuccessful turns, missing final messages, packet changes, tool-budget violations and unexpected internal exceptions remain terminal. The validator's rules and schemas stay unchanged.

If the first complete final annotation is refused, preserve its exact text and the exact validator exception string. Start one additional turn on the same server thread, same model/effort and schema. Its sole text input is `str(error)`, verbatim, with **no wrapper, explanation, reviewer text or author hint**. It may use the ordinary historical tools, then must return a complete annotation. No resume/fork/new thread is created. The existing call-ID set and total tool-call budget span both turns; there is no second budget. The second final refusal is terminal. There is no recursive repair of the repair.

A successful first final follows the existing path and supplies no extra instruction or feedback. Guidance versions and initial inputs stay byte-identical. New run provenance records the repair-policy version; historical runs retain their existing validation path.

## Transcript, provenance and failed runs

Keep every final message in `raw-transcript.json`, including the refused one. Append a structured administrative validation event with the refused message index and SHA-256, tool-transcript prefix boundary, exception type and exact message, followed by the actual user feedback text sent to the server. Record both server turn IDs and the final message chosen for publication. Save the transcript before sending feedback and after each subsequent tool/result or final message, so failure preserves the refused annotation and error. The event is administrative evidence about validation, never a source citation.

New provenance records `validation_repair_policy`, `validation_repair` (true only when feedback was sent), refusal-message/input hashes and the selected final index. A repaired run is not reviewer-assisted solely because it repaired validation. Packet-attached coverage keeps its existing assistance label. Preserve failure status if the second response fails, if the transport disconnects or if saving fails; never publish a draft from a refused final. Do not alter a previous run or silently retry a failed session.

## Replay and approval

Add a shared verifier used by assessment, deep validation and ancestor approval. For repaired runs it checks exactly one refusal event and one feedback message, their order, hashes and turn identities, and that feedback bytes equal the recorded validator string. Re-run the original JSON/annotation validation against the transcript prefix available at the first final; it must fail with the identical exception type/message. Validating that refusal against later reads would be wrong. Then validate the selected complete final against the complete evidence ledger under the unchanged schema and coverage rules, and require exact draft reassembly and Markdown rendering.

Replays cover every actual tool call from both turns, including failed calls, using the existing isolated runner; report calls by turn and total. No prior annotation prose is evidence. Unknown citations, unsupported source/execution labels, failed/catalog-only tools, cutoff or coverage violations still fail. Ambiguous final selection, fabricated feedback, altered refusal bytes, extra repair turns, missing bindings and changed packet bytes fail closed. Model/runtime/trial exclusion and ancestor-only approval gates remain unchanged. A repair never causes automatic approval or supersession.

For later revision mode, a successfully repaired source may be imported only through this verified final-selection record; its refused final and validator feedback must be excluded from revision input. Do not relax revision's ambiguous-final refusal by simply selecting the last JSON message.

## Request disclosure

Every repaired request states `validation_repair: true`, binds the transcript/provenance and any validation report, and reports the refused annotation hash, exact validator message, one repair used, and tool-call counts before/after feedback. Distinguish this validator-only repair from pointer-assisted authoring and revision. Scope remains ancestor retrieval only; canonical/training remain false.

## Implementation tests and acceptance

Mock transport tests will cover first-pass success with identical opening inputs, malformed JSON, invalid citation/basis followed by a valid complete final, extra tool reads during repair, a second refusal, missing/failed turns, wrong thread/turn/model, duplicate call IDs and cumulative budget exhaustion. Verify feedback contains only the validator's exact message, with planted reviewer/ledger/other-attempt secrets absent. Verify a transient transport or runner/internal failure never enters the repair path.

Artifact tests will cover failure persistence, exact refused/final bytes, draft/render reassembly, prefix-based refusal reproduction, tampered feedback/hash/index/turn, fabricated or multiple repair events, replay mismatch and unchanged historical approval. Model and trial gates remain exercised. The full host-enabled suite and focused tests, diff and artifact hashes will accompany the completed implementation before live use. No tests are claimed to have run for this design-only request.

## Current walk boundary

255/004 remains unstarted, awaiting the user's answer to automatic launch-approval refusal. The recovery mechanics verdict now authorizes a new 000255-004 packet copied from 000255-001 plus the exact 004 pointer-only coverage attachment; it does not authorize bypassing execution approval. 255/004 runs under today's validation rules. Then replacement 234, then the run-ahead migration note, with no run-ahead session before that note is accepted. Revision implementation follows validation repair and remains unavailable until its own completed implementation is accepted.

## Bindings

- reviews/verdicts/validation-repair-001.decision.md: `a4a0c0bdddede4403e15da64401d397ff2066da32e28f16ac4024e9fd0977c69`
- reviews/verdicts/run-ahead-implementation-002.md: `3d7d471280fe388ce19a7da7e81f8316cee92a7aefa96c700992525169a99e14`
- reviews/verdicts/revision-attempts-implementation-001.md: `6ee98fb736f657364347a38934e45e542d8b546b26dcdcec6c09c8dc2f1320ef`
- reviews/verdicts/commit-000255-reference-recovery-004.md: `8a3403bc82ba3d6a08d77ae3e9664cedf74de1d0bacc1b2dae3ed96f8e1f9b4a`
- teacher/codex_adapter.py: `740facbdf0fd0d1d7c9d0e5ba6f35f0b6eed4d8df16c616e8ca9f7a9f443ba74`
- teacher/author.py: `70db8a88568c1db016b80e75313c3c75f784fdcd203c4abb1bdbd072893999d2`
- teacher/editorial.py: `92d39a4364126b5a39f3436267dda1ffff6c007b5a9830d9a7f003d0a29b8316`
- teacher/ancestor_context.py: `4ddf1354efd9df4897d3f9d86cd1d2f70e5a4e89c6cd21a021dfb0c943c18f78`
- teacher/approval_policy.py: `3f57d9d27cd1a6e6b5eaf5a925b8e5e94f83dea072c92d4c22584b9669a80a49`
- teacher/cycle.py: `4103ed73615c11dc219eac0a95bf0a48eb1d3e0a23421988245059071adf0a60`

Reply in reviews/verdicts/validation-repair-implementation-001.md. No live validation repair until implementation review accepts it.
