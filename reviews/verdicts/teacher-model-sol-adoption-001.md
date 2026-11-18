# Verdict: teacher-model-sol-adoption-001

Reviewer: Fable. Date: 2026-11-16.

## Decision

**Accepted.** Walk teacher sessions run on `gpt-6.1-sol`, medium, guidance 11 from the next commit, per
`teacher-model-sol-adoption.decision.md` (user: "Switch teacher to Sol"). The replacement hold ends: the nine
remaining replacements may run on Sol under the accepted plan. No teacher output is approved by this.

## Artifacts

All thirteen hashes in the request match.

## Run checks

- Code read as it now stands (`codex_adapter.py`, `codex_transport.py`, `author.py`, `codex_preflight.py`).
  The default model is Sol; Astra is kept as the legacy model. The approval gate accepts Sol/medium or
  Astra/medium only, rejects `trial_only` runs and anything under `.teacher/trials`, and requires the
  server-confirmed runtime in the transcript to equal the provenance. The one exemption is an Astra run whose
  transcript predates runtime recording; a Sol run without the runtime record is rejected.
- Transport: the cloned catalog profile for Sol as in the trial; the byte copy for Astra.
- Instructions, tools, sandbox and budgets: untouched (the long instruction text is unchanged in the file).
- Audit report: 240 Astra/medium approved runs pass the new gate; the root assembly has no model provenance
  and is left as it is. Three implementation files changed since 242's run, as listed.
- Astra's suite log: 287 tests, OK. Not rerun by me.

## Notes

- The exemption for runtime-less Astra transcripts would also admit a new Astra run made without the record.
  The default is now Sol and every current code path writes the record, so I accept it; do not widen it.
- `TRIAL_MODEL` now equals the default. Any future model trial needs its own name and root.

## Conditions

- Every review request states the teacher model and effort (the request says generated requests now do).
- For the first Sol walk commit, include the session's token totals in the request.

## Next

Record 242's approval if not yet recorded, then proceed: 243 on Sol, and replacement 103 on Sol at the next
opportunity, with the 242 ledger fix revision.
