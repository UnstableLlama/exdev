# Verdict: commit-000092-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000092-001`
Packet: `.teacher/retrieval/000092-001`
Upstream: `fc543509c67605f64ab75bea590c5b91bad0e875` "chat.py: Add sampler args"
Request: `reviews/requests/commit-000092-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and both findings are real: two of the new command-line options fail when used as
their help text invites.

Both r002 ledger revisions are **accepted as recorded**.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 14 of 14 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 91 strict-ancestor entries; 1,254 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 14 of 14 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 91/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 21, 22. Matches the eight open rows. |
| Diff claims | One `ComboSampler` built from the arguments before the loop and passed to each `Job`. Defaults: temperature 0.8, min-p 0.08, top-k 0, top-p 1.0, penalties neutral, `temp_last = not args.temperature_first`. `penalty_range` (default 1024) is passed as both `rep_sustain_range` and `rep_decay_range`. `-rps` is removed; at the parent its only occurrence is its own declaration. Correct. |
| Comparison with the old default | `DefaultSampler` is min-p 0.08 then temperature 0.8 (commit 80). The chat defaults reproduce that order and those values. Correct. |
| Finding `chat-top-k-float` | Correct. `--top_k` is declared `type = float`; `SS_TopK.run` uses `self.top_k` as a slice bound (`state.probs[..., self.top_k:]`), and a float is not a valid slice index. The default 0 becomes a no-op and never reaches the slice. |
| Finding `chat-min-p-disable` | Correct. The help text says "0 to disable"; `ComboSampler` builds `SS_MinP(0)`, which fails the unchanged assertion. Same root as 91's finding, reached from a new caller. |

## Ledger revisions

- `exllamav3-missing-combo-sampler--r002`: accepted. Adds commit 91 as a source-verified fix, supersedes r001, r001 left
  in place.
- `exllamav3-presfreq-zero-decay-boundary--r002`: accepted. Adds the commit 91 reachability observation, same identity.

## Not verified

- Any chat session or sampler construction. Nobody ran one; the entry says so.

## Reviewer-only note (not for any teacher)

Because chat passes the same non-zero value as both sustain and decay, the chat example does not reach the zero-decay
boundary recorded at commit 90, unless a user passes `--penalty_range 0`, which makes both penalties no-ops instead.

## Must fix before canonical use

1. `chat-min-p-disable` and 91's `combo-default-min-p` are one defect (`SS_MinP` rejects 0 and has no no-op
   alternative) seen from two callers. One ledger record, two observations.

## Next

1. Record this approval and the ledger acceptance.
2. Continue the walk at commit 93.
