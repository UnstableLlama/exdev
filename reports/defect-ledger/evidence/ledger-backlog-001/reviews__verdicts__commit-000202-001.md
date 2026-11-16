# Verdict: commit-000202-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000202-001`
Packet: `.teacher/retrieval/000202-001`
Upstream: `dc69b16752a9ee25e6dca731b9db5d7b5da26878` "GEMM: Set kernel attribute per device"
Request: `reviews/requests/commit-000202-001.md` (sha256 `000d3075e21660432c7f1972566042cc0739d844fce3869ff7199e3b8db3eeeb`)
Reviewed: 2026-11-16, working tree on top of `e9e83ff`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. No findings are filed and I have none to add.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 12 of 12 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 201 strict-ancestor entries; 2,933 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 12 of 12 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 201/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. The reviewer-observation ledger record for the 188 cache did not reach the teacher. |
| Catalog | Fifteen open rows at 2025-05-30T17:42:49Z; my query agrees. Two closed rows selected; the entry says neither names this change. |
| The change | One set becomes an array of `MAX_DEVICES` (32) sets; both launchers index it with the `device` they already obtained from `cudaGetDevice` after guarding `A.device()`; lookup and insertion both use it. Nothing else changes. Correct. |
| Other users | `kernel_attr_set` is used only in these two launchers; `MAX_DEVICES` also sizes `DevCtx`'s arrays. Correct. |
| Shared-memory figure | `SMEM_MAX` is 90 × 1024 = 92,160 bytes, the same value the launch requests. Correct. |
| Execution | A set-bookkeeping model: two set-ups under the old cache, four under the new for two kernels on two devices. I agree by hand. Labelled as a model. |
| Limits | The unchecked `cudaFuncSetAttribute` status and the unchecked device index are stated as unchanged. Correct. |

## Reviewer knowledge (never to a teacher)

- This is the fix I recorded as hindsight at 188. The teacher did not read the 188 entry (its ancestor reads were
  the two older GEMM entries), and that entry lists the cache only under limits, so no fix attribution appears in
  this entry. The Problem section nonetheless states the defect exactly.
- The sets are still modified without a lock, as since 188.

## Not verified

- Any CUDA build or multi-GPU execution.

## Must fix before canonical use

None for this entry. The 188 condition (state the cache as a finding) stands on 188.

## Follow-ups

1. Ledger: `exllamav3-kernel-attribute-cache-device` may now take `dc69b167` as its fix. Earlier owed items
   stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 203.
