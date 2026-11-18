# Verdict: commit-000244-001

Reviewer: Fable. Date: 2026-11-16. Upstream `ea4ef8dc` "Chat.py: Add stats". Teacher `gpt-6.1-sol`, medium,
guidance 11.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. All three findings are
**accepted as true**: `tps-toggles-multiline` and `context-count-overwritten` (new defects) and
`inherited-negative-codeblock-index` (existing identity, carried over). The three ledger items owed from 243
are **accepted**.

## Artifacts

Request hashes match. `check.py` clean: manifest and provenance agree (`gpt-6.1-sol`, medium), 44
implementation hashes, 28 evidence calls all cited, final equals annotation, 243 ancestors, 3326 blobs,
nothing after the cutoff (2025-06-06T01:43:41Z). Instructions identical to 243's run.

## Run checks

- Replay: 28 of 28 identical.
- Diff read. Both new findings are plain in it:
  - The `/tps` branch does `multiline = not multiline` and prints its message from `multiline`; `show_tps` is
    never changed. So `/tps` switches multiline input and cannot turn the statistics on or off.
  - `new_tokens` is first the uncached prompt count, used for `prompt_tps`, and is then reassigned to
    `r["new_tokens"]` before the print, so the "Context" count shows generated tokens beside the prompt
    throughput.
- The inherited code-block index finding is the recorded identity; this commit does not touch the helper.
- The missing zero-duration guard is kept as a limit rather than a finding, which is the right call without
  evidence that a zero duration occurs.
- The comment-only colour edit is described as such.

## Ledger (owed from 243)

- `shared-vocabulary-extension` r001 and `ordinal-return-removed` r001: introduced and observed at
  `64ef2a37`, no fix claimed, flags false.
- `exllamav3-tokenizer-decode-filtering` r002: 243 observation added to the existing identity.
Accepted as filed.

## Not verified

No interactive session by anyone. Eight discussion fetches were made; the entry claims no motivation from
them and I did not read them.

## Follow-ups

Ledger with the next request: new records for the two 244 defects; observation revision on the code-block
index identity. `token-usage-retention-001` still owed.

## Next

Record the approval and proceed: replacement 103, then 245.
