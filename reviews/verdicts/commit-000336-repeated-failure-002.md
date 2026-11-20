# Verdict: commit-000336-repeated-failure-002

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (11:07 UTC). Stopped runs: `.teacher/runs/commit-000336-001`, `-002` and `-003` (no draft from any).
Upstream `37f80fb9` "Fix typo".

## Decision

**Stopped at 336, waiting for the user. No fourth attempt and no change to the live code yet.** The cause is now known
and is not specific to this commit, so retrying unchanged cannot work. Preparing a fix for review is requested below.

## What I checked myself

- Request hashes: 13 checked, 0 bad. The working tree carries exactly the reviewed diagnostics patch (reverse check
  passes).
- `codex-failure.json` from 336/003 records one error event: HTTP 400, `invalid_json_schema`, param
  `text.format.schema`, "regex construction fuel exhausted". The request is refused before the model works, which
  matches the empty transcripts and zero tokens. The bubblewrap line in stderr is only a warning.
- `output_schema` puts every allowed commit into two enums of 40-character hashes. Comparing the schemas built from the
  packets: 335/001 to 336/001 differs by exactly one added hash in `links` and one in `locations.commit`, and nothing
  else. 335 had 330 and 332 entries and was accepted. 336/001 had 331 and 333 and was refused. 336/002 had 332 and 333.
- So the walk has reached a provider limit that grows with history. Every later commit would hit it too.

Not tested: I have not sent any schema to the API, so that the enums are the whole cause is strongly supported, not
proven. The next run is the test.

## Requested now (preparation only)

File a normal implementation request with hashes. Do not apply it and do not launch anything for 336.

- Send the provider a schema without the two long hash enums, at both `outputSchema` call sites in
  `teacher/codex_adapter.py`. Keep `links.maxItems = 0` when no link is allowed, and every other constraint.
- `validate_annotation` keeps using the full `output_schema(manifest)`. A hash outside the allowed set must still be
  refused, and go through the existing repair route. Show this with tests for both fields.
- No change to teacher prompts, tools, packet, model or guidance. State the size of the sent schema for 336, and how
  provenance records it. Say whether any recorded hash or replay check depends on the schema sent.
