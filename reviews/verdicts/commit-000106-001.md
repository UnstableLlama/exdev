# Verdict: commit-000106-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000106-001`
Packet: `.teacher/retrieval/000106-001`
Upstream: `045603ffbdc8cf40a324bdc157c43517bc3a8ca5` "chat.py: Nicer formatting for reasoning model output"
Request: `reviews/requests/commit-000106-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry sees that this commit is the other half of 105 (it gives both stream
methods the argument 105 started passing) and describes the formatting changes as the code has them.

The ledger record `exllamav3-chat-stream-argument-mismatch--r001` is **accepted as recorded**.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 105 strict-ancestor entries; 1,562 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 8 of 8 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 105/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path or the new ledger id. |
| Catalog | Same committer timestamp as 104 and 105; the same thirteen rows are open. |
| Diff claims | Both `stream` methods become `(self, text, think_tag, end_think_tag)`. In the rich streamer's thinking branch the first chunk is `lstrip`ped; when the closing tag has been seen the chunk is printed `rstrip`ped followed by a blank line and the Markdown console starts. In the answer branch leading whitespace is stripped until something non-blank has accumulated, a chunk starting with three backticks gets a leading newline, and both tags are wrapped in backticks in the text handed to the live display only. `all_text` still accumulates the raw chunks. Correct. |
| Repair claim | With three parameters after `self`, the call introduced at 105 binds. Correct. |
| Findings | None reported. See "Must fix". |

## Ledger

- `exllamav3-chat-stream-argument-mismatch--r001`: accepted. Suspected defect introduced at `7488d82c`, chat example only,
  no fix claimed yet.
- Add this commit as its source-verified fix in an r002: both signatures now accept the call.

## Not verified

- Any terminal rendering. The entry says its string checks used literal escape sequences and are not a layout test.

## Must fix before canonical use

1. The entry rewrites the description of the rich streamer's thinking branch and does not carry the inherited
   `reasoning-boundary-answer-loss` finding that 73/001 and 78/001 record. It still holds at this commit: when the
   closing tag arrives in the same chunk as the start of the answer, the whole chunk is added to `think_text` and the
   answer part never reaches `all_text`. The entry read only 105's ancestor entry. Not false, but a canonical entry
   for a commit that edits this exact branch should say the defect survives.

## Next

1. Record this approval, the ledger acceptance and the r002 fix attribution.
2. Continue the walk at commit 107.
