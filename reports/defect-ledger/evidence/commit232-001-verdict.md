# Verdict: commit-000232-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000232-001`
Packet: `.teacher/retrieval/000232-001`
Upstream: `3637103e2ff4a736544774606ddc964fc4f71362` "GatedMLP: Allow unpadded FP16 tensors"
Request: `reviews/requests/commit-000232-001.md` (sha256 `bbd9f8a22f8b99875e09f9173a6787214c78e5ad364d0d6f7b8396ea89de92b3`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is true as stated. The ledger item filed with this request is
accepted, and so is the one pre-run retry described in the request.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 16 of 16 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 231 strict-ancestor entries; 3,200 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 16 of 16 recorded tool calls identical, including both `run` calls and the recorded error for a file that does not exist. |
| Unassisted | Standing instructions byte-identical to 231/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-03T01:07:57Z; my query agrees. One closed row by path alone. |
| The change | `GatedMLP.__init__` gains `pad_to = 128` and passes it to each gate, up and down projection. Nothing else. Correct. |
| Callers | No model constructor passes it, so every existing model keeps 128. Correct. |
| Finding: odd tail | `act_mul_kernel` returns for `idx >= numel / 2` and works on pairs, so with an odd element count the last element is never written; the call is in place on the up projection's output, so that element reaches the down projection ungated. With padding to 128 the count is always even; with `pad_to = 1`, one token and an odd intermediate width (129) it is odd. True, and the trigger is stated precisely (an odd total, so an even number of tokens hides it). The kernel has been this way since the root commit; this commit is the first that lets a caller reach it. |
| Execution | A constructor scan and an integer coverage model (128 of 129 elements); labelled. |

## The pre-run retry

The first launch for 232 failed while fetching GitHub edit history, before any packet, evidence bundle or run
existed; the failed supervisor's log is kept and hashed. Astra probed the API and made one retry, which is the
only teacher attempt. No authored artifact was involved. Accepted. A fetch failure before a run exists may be
retried once without a request in future as well, provided it is reported like this; a second failure needs a
request.

## Reviewer note (for the user's report; never to a teacher)

This is the kind of case I had flagged twice (197, 205): a new option or caller reaching a defect recorded in an
earlier entry. Here the teacher made the connection itself, from the root entry's note about the pairwise
kernel.

## Not verified

- Any GPU execution.

## Must fix before canonical use

1. Administrative: the second location is written against the parent commit; use the task commit.

## Ledger items filed with this request

- `exllamav3-vision-floating-ceiling-overflow--r001`: **accepted.** Suspected, introduced at `16df3fd1`, reach
  limited to direct use of the helper, no fix; my exact-arithmetic count is recorded as administrative.

## Follow-ups

1. Ledger, with 233's request: one identity for the activation kernel's missing odd tail. Introduction at the
   root (the kernel's `numel / 2` bound is there; verify from the root tree), with `3637103e` as the commit that
   first exposes it to a caller. Suspected, source-only, opt-in reach.

## Next

1. Record this approval with `--approve`.
2. Proceed to 233.
