# Re-review of the Opus stand-in verdicts (332 to 345/002)

Reviewer: Fable. Date: 2026-11-18. Covers the 24 verdicts marked `Reviewer: Opus (stand-in)`. Those files are left
byte-identical, because ledger records bind their hashes; this file is the record that they are no longer provisional.

## Decision

**All 24 stand-in verdicts are confirmed. None is overturned.** The 14 entry approvals stand as
"Approved for ancestor retrieval only": 332/001, 333/001, 334/001, 335/001, 336/004, 337/001, 338/001, 339/001,
340/001, 341/001, 342/001, 343/001, 344/001, 345/002. Canonical and training remain false.

## Method

For each entry: the upstream diff first, then the entry's central claims and every finding (carried ones
included) against source at that commit, then the stand-in verdict. No entry states anything false about the
source that I found, and each established its commit's central point itself. Notably 338/001 found the
Gemma3/Mistral3 image-embedding breakage as its own first finding; the stand-in did not have to supply it.
Run-ahead (338 to 344) never mattered. 344 is a key rename, not a new architecture; headers and pins were checked
anyway (224 pins, all at or before the cutoff).

Ledger records bound in those requests: status suspected, training false, earlier observations byte-equal with
the superseded revision, introductions sensible, in every one checked.

Process verdicts:
- 336/001 to 003 failed with HTTP 400 `invalid_json_schema`, "regex construction fuel exhausted" (read from
  `commit-000336-003/codex-failure.json`). Full schema 34,581 bytes at 335 and 34,669 at 336, growing with the
  ancestor list. Cause as the stand-in stated.
- `codex-output-schema-implementation-001`: applied tree equals the patch; the provider schema for the 346 packet is
  5,433 bytes against 35,593 full; local validation (`editorial.py:116`) still uses the full schema with all 342
  hashes. Sound.
- `codex-failure-diagnostics-implementation-001`: applied tree equals the patch; the three `codex-failure.json`
  files are mode 0600 and hold no token. Sound.
- Full suite on the applied tree: 355 tests, OK, 13 skipped.
- The two user approvals are quoted in `commit-000336-recovery-003` and `-004`. I did not see those chat messages
  and take the quotations as recorded.

## Not re-done

The mechanical pass (replay, `check.py`, request hashes) for 332 to 345; the stand-in's large enumerations on 339
and 340 (worked examples were hand-traced instead); discussion summaries against fetched text; ledger evidence
file hashes; no native code was built or run.

## Follow-ups for the author (not blocking)

- Carried findings got no ledger observation at 333 (`inherited-override-metrics`, `inherited-deferred-bf16-tail`)
  or 335 (`proxy-oom-sentinel-passes-test-bound`, `trellis-first-pass-reads-stale-costs`); there is no
  `commit-000335-ledger-*.json` and no trellis record at all. 334 and 345 did get revisions. Say which rule
  applies and file what is missing.
- `cache-detach-count-diagnostic` was "confirmed" with no fix recorded from r003 until r005 added the fix. Check the
  r003/r004 status against the ledger rule.

## Must fix before canonical use

Unrelated discussions padded into Source Notes in every entry from 332 to 345, as each stand-in verdict lists.
