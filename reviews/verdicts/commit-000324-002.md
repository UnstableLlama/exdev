# Verdict: commit-000324-002 (teacher gpt-6.2-sol, guidance 12, fresh unassisted retry of 324/001)

Reviewer: Fable. Date: 2026-11-18 (05:16 UTC). Upstream `6171f9af` "Fix default chat prompts for Dots and Ernie".
Run: `.teacher/runs/commit-000324-002`. Packet: `.teacher/retrieval/000324-002`.

## What I checked myself

- Request hashes 0 bad. `check.py`: impl 45 bad [], evidence 66 calls 66 bad [] uncited [], final==annotation
  True, anc 323 entries 323 True, blobs 4579 bad 0. Replay 66, mismatch 0. No repair used.
- Diff read in full (three `default_chat_prompt` overrides: Dots markers, Ernie begin-of-sentence and
  `User: `/`Assistant: ` labels).
- Central claims confirmed: the new strings equal the existing interactive formatters in
  `examples/chat_templates.py` (324-328, 359-367); the only in-tree caller is `examples/imgsearch.py:90`, behind
  a `vision` component (line 51) that these models lack; the pinned Dots instruction template inserts
  "You are a helpful assistant." when no system message is given, which the helper does not, so the entry's one
  finding is real and correctly scoped as a parity difference, not a failure.
- The entry made the central check itself (do the new strings match the pinned templates, and where not).
- 323 ledger (six records): all suspected, training false; three new Exaone4 identities introduced at
  `544ba423`; FP8, kv-sampler and prefill findings merged into existing identities with their earlier
  introductions (`d860f8e1`, `cf848114`, `543c4b27`), as asked. Accepted.

## Must fix before canonical

- Two Source Notes paragraphs summarise unrelated discussions (#7, #52, #51, #61); cut to one sentence.
- Three paragraphs restate model dimensions the formatter never reads; cut.

## Decision

Approved for ancestor retrieval only. Canonical and training remain false.
