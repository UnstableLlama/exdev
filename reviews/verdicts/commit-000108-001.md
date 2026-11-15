# Verdict: commit-000108-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000108-001`
Packet: `.teacher/retrieval/000108-001`
Upstream: `fd934384c4a750fd5e0744ce1f9c7044f8e982a2` "Add Q/K norms"
Request: `reviews/requests/commit-000108-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry is right about the placement (after the split into heads, before RoPE,
in all three paths) and right that this adds a capability no model builder uses yet.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 13 of 13 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 107 strict-ancestor entries; 1,576 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 13 of 13 recorded tool calls identical, including all three `run` calls (one of which is a recorded failure and replays as the same failure). |
| Unassisted | Standing instructions byte-identical to 107/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 21, 22, 24, 25, 26, 27, 28, 29. Matches the thirteen open rows. |
| Architecture trigger | Does not fire. |
| Diff claims | `Attention.__init__` gains optional `q_norm` and `k_norm`. If `q_norm` is truthy it asserts `k_norm`, stores both and registers both as submodules; otherwise it sets both to `None`. Each of the three decode paths replaces its `# TODO: q/k norms` with `q = self.q_norm.forward(…, out_dtype = torch.half)` and the same for `k`, guarded by `if self.q_norm`. `rmsnorm.py` gains one TODO comment. Correct. |
| "No builder uses it" | No file under `exllamav3/models` mentions `q_norm` or `k_norm` at the task commit. Correct. |
| Finding | `asymmetric-norm-validation`: correct. A `k_norm` passed without a `q_norm` falls into the `else` and is dropped without complaint, against the assertion's own message. Reach is the constructor only, as the entry says. |

## Run file reads

The request says the failed scan's read count cannot be recovered and reports total run file reads as unknown. That is
the honest report. For the open question about counting such reads: the two scans walk every Python file in the
task tree, which is the same exposure as a whole-tree grep.

## Reviewer-only note (not for any teacher)

The ledger record `exllamav3-cohere-qk-normalization` is not closed by this commit. Nothing wires the new arguments into
`cohere.py`, and the Command R Plus checkpoints store their `q_norm` and `k_norm` weights as `[96, 128]` and `[8, 128]`,
one row per head, where `RMSNorm` loads a weight and the native routine expects it to match the last axis. Whether the
new hook can express those per-head weights is not established here. Do not record this commit as a fix.

## Not verified

- The entry's description of the native `rms_norm` kernel; the read of `norm.cu` replays, I did not re-read it.
- Any execution.

## Must fix before canonical use

None.

## Next

1. Record this approval.
2. Continue the walk at commit 109.
