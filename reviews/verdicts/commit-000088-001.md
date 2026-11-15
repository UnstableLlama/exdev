# Verdict: commit-000088-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000088-001`
Packet: `.teacher/retrieval/000088-001`
Upstream: `de83084184c34cae0aaeca5c8b024de7f148830d` "Only allow input padding for MLP down projection (until more testing)"
Request: `reviews/requests/commit-000088-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry notices that the code is narrower than the commit message (only
`GatedMLP`'s down projection opts in, not the plain `MLP`'s), and it gives the reason the exception is safe there: the
gate and up projections already pad their outputs, so the down projection receives the wider activations. That is the
point my 84/001 verdict said was missing, reached here without being asked.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 15 of 15 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 87 strict-ancestor entries; 1,216 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 15 of 15 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 87/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 20. Matches the seven open rows. |
| Diff claims | `Linear.__init__` gains `allow_input_padding = False` and an assertion that the rounded input width equals the original unless the flag is set. `GatedMLP` passes `allow_input_padding = True` for `down` only. `pad_out` and the loaders are untouched. Correct. |
| Scope claim | `MLP.down` is built at `mlp.py:32` with no flag, so a plain MLP with an unaligned intermediate width now fails the assertion. `GatedMLP` builds gate and up with `out_features = b - a` and down with `in_features = b - a`, so down's padded input width equals gate/up's padded output width. Correct. |
| Findings | Both are carried observations with the same identities as 84/001 and 86/001. `retained-two-axis-padding` now needs an opted-in caller, as the entry says. `retained-padding-before-slicing` is unchanged. |

## Not verified

- Any model construction. Nobody ran one; the entry says so.
- Behaviour with assertions disabled (`python -O`), where the guard does nothing. The entry says "with assertions active".

## Must fix before canonical use

Reviewer-only.

1. Ledger identities: the two findings are further observations on the records that 84/001 and 86/001 feed, not new
   defects. This is the third name for the both-axes observation; keep one record.

## Next

1. Record this approval.
2. Continue the walk at commit 89.
