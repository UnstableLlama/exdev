# Author comparison 001 complete

Job A is `commit-000244-001.request.md`. It was written before opening the approving verdict for Job B. It requests ancestor retrieval only and contains freshly checked artifact hashes, findings, coverage, execution limits and implementation comparison.

Job B is the two r001 records under `ledger/`, with self-contained evidence copies. Both pass `ledger.retrospectives.validate` (via `append`) and `validate_evidence`. The original finding status and verification limits are preserved; reviewer confirmation is separate. The inherited negative-codeblock finding remains an existing identity, so no third new identity was created. No later fix is inferred.

These are comparison artifacts only. No teacher session was started. No production ledger, journal, approval, tracking, commit or push was changed. The detached 141/003 run was neither inspected nor altered during these jobs. Only this trial directory was written.

## Files written

- `commit-000244-001.request.md` — SHA-256 `26da763e6b1ff56f191f44fd385375caef2ccb7fc6ef6170a0bff34a1f8006c0`
- `ledger/evidence/commit-000244.diff` — SHA-256 `78676323d3052f6f3229c437a2bdfb90d866e59e6524160e40a2f0df046ae866`
- `ledger/evidence/draft.json` — SHA-256 `9338759d23987f664931ce7dc6a82a8d232bec4703fa5f825ce4fc10d3e27489`
- `ledger/evidence/parent-chat.py` — SHA-256 `c630d9dc9f40befd00c3b2bf6e4dda6db76d55f5cfb79e3a2bdaac64a3faa045`
- `ledger/evidence/verdict.md` — SHA-256 `f1b99b695346b3b62a3c31f403b11e5e982a491726738552489b9776dc34cdfd`
- `ledger/exllamav3-chat-context-count-overwritten--r001.json` — SHA-256 `125a68a6bf2fdf9318fd204583d56aed519c1cba3336ff43431aa052b629264d`
- `ledger/exllamav3-chat-tps-toggles-multiline--r001.json` — SHA-256 `bc044f2b8c76999e97b92518b0d0216e9328ee58d7f8f7c31fe927e08be1eb01`
- `DONE.md` — this inventory and read disclosure.

## Inputs read

- `reviews/AUTHOR-INSTRUCTIONS.md`
- `reviews/verdicts/author-model-comparison-001.decision.md`
- `reports/commit-000244-cycle-001.json`
- `reports/commit-000244-validation-001.json`
- `reports/commit-000244-001.skeleton.md`
- `.teacher/runs/commit-000244-001/draft.json`
- `.teacher/runs/commit-000244-001/provenance.json`
- `.teacher/runs/commit-000244-001/raw-transcript.json`
- `.teacher/runs/commit-000244-001/coverage.json`
- `.teacher/runs/commit-000243-001/provenance.json`
- `.teacher/retrieval/000244-001/manifest.json`
- `reports/commit-000244-catalog-selection-001.json`
- `reviews/verdicts/commit-000244-001.md`
- `ledger/retrospectives.py`

The raw transcript was loaded to inspect structure and the single scalar-transcription tool result; it was not printed whole. The manifest was loaded to inspect configuration and bindings. Run 243's provenance was used only to compare implementation hash maps (identical).

Additional files read as bytes solely to verify their bound hashes:

- `.teacher/runs/commit-000244-001/draft.md`
- `data/evidence/github/000244-unreferenced.json`
- `data/evidence/github/000244-closed.json`

Git object inputs, through `.sources/exllamav3.git`:

- `git show --format=fuller ea4ef8dcbb58d3afc5cffadcb90a01204af7036e`: exact title, timestamp and full two-file diff; copied into ledger evidence.
- `git show 64ef2a379213f88671e04d71a45f18ae8590e079:examples/chat.py`: parent absence check for the added command/reporting logic; copied into ledger evidence.
- `git show -s --format=%cI 64ef2a379213f88671e04d71a45f18ae8590e079`: dependency availability timestamp.

The ledger validation import also loads the package initializer `ledger/__init__.py`. Generated evidence copies were reread to parse findings and verify hashes. Existing compacted thread context was available; no existing author output was used as a template.

## Excluded outputs

None of the four excluded files was opened, hashed or copied: the original 244 request, the 245 verdict, or either production r001 record for these two defects. The only approving verdict used for Job B was `reviews/verdicts/commit-000244-001.md`.
