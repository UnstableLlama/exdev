# Verdict: commit-000194-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000194-001`
Packet: `.teacher/retrieval/000194-001`
Upstream: `8b1fccf7a6bfdcce65008c1fd456994ee4423685` "Fix compiler warnings"
Request: `reviews/requests/commit-000194-001.md` (sha256 `6189667209d500794582de0201d0afddc6dbfb72056f6dfc757fa1e1ad89f64e`)
Reviewed: 2026-11-16, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry makes the one observation worth making about a cleanup this small:
the unused lane index it removes is the value a lane-zero guard would have tested, so the 185 warp-sum finding is
untouched.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 15 of 15 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 193 strict-ancestor entries; 2,858 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 15 of 15 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 193/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fourteen open rows at 2025-05-27T09:27:37Z; my query agrees. One closed row by terms, selected; the three discussions read are described as file overlap only. |
| The change | Two declarations are commented out: `POS_INF_F32` in `sampling_basic.cu` and `lane_id` inside `apply_norm` in `rope.cu`. Neither name is used anywhere else in those files. Correct. |
| Inherited findings | The store to `sums[...]` in `apply_norm` is still unconditional, and the padded reads of `inv_freq` and the norm weight are unchanged. True; both introduced at 185. |
| Execution | Launch arithmetic for a head of 80; labelled as arithmetic. |

## Not verified

- Any compilation; that the warnings are gone.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: the two 185 identities gain `8b1fccf7` as affected once they are filed. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 195.
