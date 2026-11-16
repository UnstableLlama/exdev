# Verdict: commit-000203-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000203-001`
Packet: `.teacher/retrieval/000203-001`
Upstream: `f8dc9975fe88c79fcf1a12f2160974b5442695dd` "model_diff.py: Add device argument"
Request: `reviews/requests/commit-000203-001.md` (sha256 `be1cbe0b44dc0e01b9d563e56f4d75c6166f98f3ec6c5097f4f98c151701042e`)
Reviewed: 2026-11-16, working tree on top of `e9e83ff`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The one finding is the inherited `ppl-axis-bound` identity, true as stated.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 12 of 12 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 202 strict-ancestor entries; 2,938 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 12 of 12 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 202/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fifteen open rows at 2025-05-30T17:42:49Z; my query agrees. No closed row qualifies. PR 26 was read only in part and the request says so. |
| The change | `-d/--device`, integer, default 0; `torch.device(args.device)` at the top of `main`; both module loads use it in place of `"cuda:0"`, keeping the `prefer_cpu` branch. Correct. |
| Placement | `Module.load` stores the device and `prepare_for_device` moves the state to it; the script adds no transfer of its own. Correct. |
| Inherited finding | `ppl` computes a chunk of 10,240 and loops while the position is below `logits_.shape[1]`, the vocabulary size, while slicing positions. Unchanged by this commit. True. |
| Execution | An integer model: 1,024 of 2,047 positions covered for a 1,024-entry vocabulary; all 2,047 in four iterations for 32,000. I agree by hand. Labelled as a model. |

## Not verified

- Any Torch or CUDA execution, including `torch.device` built from a bare integer.

## Must fix before canonical use

None.

## Follow-ups

1. Ledger: no new identity; `ppl-axis-bound` stays open through this commit. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 204.
