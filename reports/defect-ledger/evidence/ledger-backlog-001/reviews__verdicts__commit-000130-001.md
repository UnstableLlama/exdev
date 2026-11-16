# Verdict: commit-000130-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000130-001`
Packet: `.teacher/retrieval/000130-001`
Upstream: `2e7b00d3b0d1731e86d127b992ae6298dd70a504` "Generator: Prevent particular failure mode in generator from holding output indefinitely"
Request: `reviews/requests/commit-000130-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and all three findings are correct. The entry reads a three-line change, states
exactly what it does and does not do (the threshold is measured on the re-decoded string while the text emitted is
the unchanged held text), and notices that the new early return sits in front of both string matchers.

The ledger revision `exllamav3-gemm-selector-divisibility--r002` is **accepted**.

## Artifacts reviewed (sha256)

All sixteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 9 of 9 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 129 strict-ancestor entries; 1,877 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 9 of 9 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 129/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Eleven open rows: 1, 4, 7, 10, 14, 22, 26, 27, 28, 29, 34. Correct (my routine query again counts issue 33, which was closed at this cutoff and reopened on 2025-05-13). Two closed rows, issue 21 and pull request 25, both closed before the cutoff of 2025-05-08T21:19:45Z. Issue 21's last comment is its closing one of 2025-04-30. |
| Architecture trigger | Does not fire. |
| The change | One line in `Job.receive_sample`: on a re-decode that still contains the replacement character, `return emit(results)` becomes `return emit(results, emit_held = (len(test_decode) > 20))`, plus a two-line comment. Nothing else. Correct. |
| Branch entry | `1 <= self.held_text.count("�") < 5`; a clean re-decode assigns `held_text = test_decode` and falls through to the string checks. Correct. |
| What is emitted | `emit` with `emit_held` appends `held_text` to `full_completion`, emits it with the token, probability, top-k and logit buffers, and clears them. `test_decode` is used only for the length test. `emit_eos` stays false. Correct. |
| Caller | One call site, `generator.py:461`; it completes the job only on a true EOS flag and otherwise continues with the draft comparison. Correct. |
| Issue 21 | The entry says its text does not establish a connection to this change. Correct; it is a Windows build report. |
| Execution | Recorded output: length 20 holds, length 21 flushes; the 21-character fixture ending in `bad` selects the flush. Matches the prose, and is labelled as a transcription of the predicate, not a run of the repository. |
| Finding `unicode-flush-bypasses-string-checks` | Correct. While the branch holds, every call returns before the banned-string and stop-string matchers, so the held text is never matched. At the parent that text stayed held until the character resolved, a fifth replacement character arrived, or the token budget ended the job; in the first two cases the matchers then saw all of it. At the task it is emitted and cleared once the re-decode passes 20 characters, and the matchers never see it. Suspected is right; no tokenizer was run. |
| Finding `retained-checkpoint-token-attribute` | Correct. `rewind_checkpoint` assigns `self.held_token`; nothing reads that name; `emit` reads `self.held_tokens`. Untouched by this commit. |
| Finding `retained-terminal-string-bypass` | Correct. The `max_new_tokens` return with `emit_held = True` precedes both matchers. Untouched by this commit. |
| Ledger `gemm-selector-divisibility--r002` | Differs from r001 only by the supersedes link, the 129 observation, the 129 branch list, the verdict evidence and its hash. The four branches listed for 129 are the ones in my 129 verdict. Accepted. One typo, "at129", in the observation text; fix it in the next revision, not now. |

## Reviewer-only notes (never to a teacher)

- **Where the two inherited findings come from.** Both lines are in the first commit (`543c4b27`): `self.held_token =`
  and the budget return ahead of the matchers. No ledger record exists for either yet.
- **Hindsight.** The upstream history has "Generator: Fix typo breaking rewind_checkpoint()" (`8cfa711a`, 2026-05-02),
  far beyond the current position. I have not read it.
- **Mine, source reading only, not executed.** The replacement-character branch returns without calling
  `set_checkpoint`, so a banned-string checkpoint opened before a replacement character arrives does not count the
  tokens held in that branch; a later rewind would step back fewer tokens than were generated since the checkpoint.
  This is in the first commit too. The new flush adds a second effect: it emits and clears the buffers while a
  checkpoint may still be set, so a later rewind would restore a `held_text` from before the flush. I am not asking
  for a record until I have traced it properly.

## Not verified

- Any execution of the repository, a tokenizer or the native matcher.
- Whether a real tokenizer can produce a held replacement character followed by more than 20 characters. The
  commit message says a broken generation does.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: `unicode-flush-bypasses-string-checks` approved as drafted, introduced at `2e7b00d3`.
2. Ledger: the checkpoint attribute and the terminal bypass are one record each, introduced at `543c4b27`, with
   `2e7b00d3` among the affected revisions. Do not file them as introduced here.
3. The earlier ledger revisions owed (listed in the 129 verdict and your journal) are still owed.

## Next

1. Record this approval.
2. Continue the walk at commit 131.
