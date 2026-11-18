# Teacher-model trial implementation 001

Reply-to thread: 01a1da07-7653-7b81-8507-f69683828acb

Request acceptance of a trial-only Sol gate under the bound user decision. No Sol teacher session has run; the wire test uses a local fake provider and fixture credentials. Forward walk and replacements remain Astra/medium; further replacements are held after approved98/002.

`teacher.author.author_trial` is a supervisor API, with no CLI/walk override. It allows only gpt-6.1-sol, medium, guidance11, unassisted input, with both resolved packet and output beneath `.teacher/trials/teacher-model-001/`. Existing `author` remains Astra. The adapter and isolated transport accept the selected allowlisted model; the private transport catalog clones the existing bounded profile, changing only slug/display name for Sol. Tools, instructions, context limits, sandbox and time/call/byte budgets are unchanged. No fallback permitted; the server's returned model and effort must match. Provenance records the selected model; the transcript's first message now carries `teacher_runtime` metadata from the confirmed server response, not sent in the teacher prompt. Existing saved transcripts are untouched.

Both cycle validation and direct ancestor approval reject non-Astra/non-medium provenance, trial_only markings and trial directory paths. Trial drafts remain pending and cannot become ancestor context through approval. This is an administrative gate, not a security boundary against a programmer modifying provenance/source. No model adoption.

Validation: full `EXDEV_SANDBOX_TESTS=1 python3 -m unittest discover -s tests`: 285 tests passed. Includes a real isolated Codex app-server against a local fake provider asserting Sol on the actual wire, default Astra wire checks, isolated trial authoring/model recording, and direct approval rejection for alternate model/effort/trial markers. Existing ResourceWarnings in the log did not fail tests. No production inference was used to test the implementation.

After acceptance only: three fresh Sol/medium trials on copies of comparison packets for213 (guidance11 trial),231 and239 (approved runs), all at guidance11. No prior answers, reviews or ledger supplied. 231's original guidance differs, so disclose that confound. Result request will bind drafts/transcripts/coverage, calls/tokens side by side and account usage if readable; three positions, one run each. Walk continues Astra separately; no further replacements until user has results.

Ledger: Cohere Q/K r003 adds the approved98/002 observation, preserves r002's fix at91c7cc41 and every older observation, and records the accepted external_compatibility->defect classification. No second identity or new fix. Administrative only, never teacher input.98/002 now active;98/001 preserved as history. Both239 ledger submissions were accepted with98.

## SHA256

- teacher/author.py: `70db8a88568c1db016b80e75313c3c75f784fdcd203c4abb1bdbd072893999d2`
- teacher/codex_adapter.py: `b118904e9bc9f419c59bab0766dd0e3097a7970c15c595fcf7343331bff2dea4`
- teacher/codex_transport.py: `eef456dd55e64c73a54bf5b1a620f980ff9f5e44b99c02082d339748bf57eff7`
- teacher/ancestor_context.py: `4ddf1354efd9df4897d3f9d86cd1d2f70e5a4e89c6cd21a021dfb0c943c18f78`
- teacher/cycle.py: `ec8c2cc4a2ead6b670db28422394358880ac914d3c1cb2087385918aef47aba0`
- tests/test_author.py: `4ddfd4c244b741d8f21b22fc74b352225cbacf0a97d2bdc40b2be687081cd737`
- tests/test_codex_wire.py: `8d772d00aa514d3f661c8520583333d297ae72a4b0ff9f6f6e3c3b80fe986e6a`
- tests/test_ancestor_context.py: `823e5ddd43e23fd822000fe70dd9e75da9c772405fe7ea88a60729462bf809e1`
- reports/teacher-model-trial-implementation-001.patch: `df52d371fe5f41cc57e4f18f0d6f9104320de57b399e9212c03da41001771430`
- reports/teacher-model-trial-tests-001.log: `53d37f612d26fd12acf145356c84f0e062ea77df450c7d213068bc67e8c8f593`
- reviews/verdicts/teacher-model-trial.decision.md: `8156830a9e1a178c810527d72bf5529f32c17b993b8b24789618d82b0a5c43de`
- reports/defect-ledger/exllamav3-cohere-qk-normalization--r003.json: `a0147c2f4afd2a58b2f9c19aa95fb822c80c8938c74151d8b702fb9f1f9201ba`
- reviews/verdicts/commit-000098-002.md: `fc15afd2e0f89ea3919cd45bd84f9f1abb57d3bd4dc31687f2adcd48d64757d8`
