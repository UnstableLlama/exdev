# Verdict: codex-output-schema-implementation-001

Reviewer: Opus (stand-in). Provisional; Fable re-reviews after the token reset.
Date: 2026-11-18 (11:11 UTC). Patch: `reports/codex-output-schema-implementation-001.patch`, sha256
`adcf1f27015b62ad90cf8368fac91c62c1be98733d283f5d71616470cfb91287`.

## Decision

**The patch passes review. Do not apply it yet.** Applying it and a fourth attempt at 336 wait for the user's answer,
which I will send you. The queue stays stopped.

## What I checked myself

- Request hashes: 6 checked, 0 bad. The patch applies to the current tree and touches only `teacher/codex_adapter.py`
  and `tests/test_validation_repair.py`.
- Read the change. `provider_output_schema` removes the two hash enums and nothing else, and both `turn/start` calls
  use it. `validate_annotation` still builds the full schema, so a hash outside the allowed set is still refused locally.
- In a throwaway copy with the patch applied: 355 tests pass, 13 skipped.
- For packet `000336-002` the sent schema falls from 34,713 to 5,433 bytes. What remains is eight short enums and four
  simple patterns, all of which were already in the schema. The 40-hex patterns stay, and `links.maxItems` is kept.
- Side effect checked: the model no longer receives the allowed hashes through the schema. In the last ten runs
  (326 to 335), all 30 linked hashes also appear in the prompt or tool output, so it does not depend on the enum to find them.

## Not established

Whether the provider accepts the smaller schema is untested until a live run. A wrong hash now costs a repair turn rather
than being impossible, and a repaired run goes to full review as usual. On the next runs, report any repair caused by
an unknown hash.

## When the user approves

I will send a separate verdict with the mechanics. Do not treat this one as authority to apply or run.
