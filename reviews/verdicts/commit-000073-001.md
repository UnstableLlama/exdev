# Verdict: commit-000073-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000073-001`
Packet: `.teacher/retrieval/000073-001`
Upstream: `fc5b39c2bb56be8654db7f4a6a7fd4f56a1db0ca` "chat.py: Limit redraw to area of console that can be redrawn"
Request: `reviews/requests/commit-000073-001.md`
Reviewed: 2026-11-13, working tree on top of `41010aa`

## Decision

**APPROVED for ancestor retrieval only.** Unassisted. The walk may continue from commit 74.

Canonical and training remain false.

Not thin. Two changed lines; the entry gives the rule, works an example through it, and says what the rule gives up.

## Artifacts reviewed (sha256)

- draft.json: `5e90c62bdecb9088d2b1f1765fb858eaea6b62c058bd019d4f558694b4e26ab7`
- draft.md: `8058178df39b0d5f2d4569985023ce2a240d20e11822ace5d7a91fd1c9d64b31`
- raw-transcript.json: `f015235446b789e5c9571a5af3d872183b122b28c31672086ccaed6885b25a5c`
- provenance.json: `9600ff4fc221e8b87ea25626e44a2ae819ac0ffe7f7f8a8ef2cc819a87bdb3e3`
- coverage.json: `239eb4f84dd9c1f20ec8a9a96e0b171eb258e354f32ff622b66b0c5845814f9d`
- packet manifest (on disk): `5d86f5616e1d9680a48245f6948ceaba25a772f48b2f1927152abbb62303b9b6`
- unreferenced bundle: `efb7583fe39911a858b5c91da407f87c81ddb468331538b14c0d9312ea5afa68`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 8 of 8 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; assessment is full review; 39 of 39 implementation hashes match; exactly 72 strict-ancestor entries (72/002 in force); all 1066 blobs hash to their names; the diff read in full; no content timestamp after the cutoff. |
| Unassisted | No coverage, no assistance flag. Standing instructions byte-identical to 72/002. |
| Opening context | Message, author, parent `c44e56c7` (commit 72) and task SHA match Git. Cutoff is the committer date, 2025-04-22T21:47:41+02:00, four and a half days after commit 72. |
| Open catalog | **Seven** rows: 1, 4, 7, 10, 14, 15 and the new issue 19 (opened 16:40 UTC on the cutoff day). GitHub agrees. The request says six; the bundle is right and the request's count is a slip. |
| Closed catalog | One row, issue 5, on the terms "limit" and "size", from 12 closed candidates (GitHub agrees on the 12, now including 18). The match is incidental and the teacher did not read it; the reading rule did not require it. |
| Source claims | Verified against the parent and the task. The constructor stores `self.console.size`; only the height is used. `update` raises the common prefix to `max(p, old - height, new - height)`, so each suffix is at most `height` lines; the cursor-up, clear and print loop is unchanged and works on the shortened suffixes; `_last_lines` still holds the full render. The emoji comment on the width reduction is quoted correctly. |
| Execution claim | Replayed the `run` call: identical output (178,608 combinations; the three worked cases). Arithmetic only. |
| Inherited finding | The reasoning-boundary answer loss is carried from the entry for `addeaaaa`, which the run read, and is labelled inherited. This diff does not touch `Streamer_rich.stream`. Treat it as the existing defect, as the request says. |

## Not verified

- No terminal was driven. Whether moving the cursor up exactly `height` lines behaves on a full screen is not something
  either of us tested; the entry says terminal behaviour is unverified.

## Must fix before canonical use

Reviewer-only.

1. Issue 19 ("Any chance of a single model file?") is new in the catalog and is neither read nor mentioned. Its title
   reports no failure, so the rule did not require it. A canonical entry need not mention it.
2. The request text should give the catalog count from the bundle, not from memory.

## Next

Record this approval and continue the walk from commit 74.
