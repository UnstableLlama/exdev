# Verdict: commit-000063-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000063-001`
Packet: `.teacher/retrieval/000063-001`
Upstream: `bad500d7272a863b3d1b0cd5a3ed1f714370c972` "Quantize: Fix tile sampling"
Request: `reviews/requests/commit-000063-001.md`
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**APPROVED for ancestor retrieval only.** Unassisted. The walk may continue from commit 64.

Canonical and training remain false.

Not thin. A four-hunk change to one function, and the entry covers every hunk, says what was wrong before with its own arithmetic, bounds the impact claim, and found that the lines the commit appends can never run.

## Artifacts reviewed (sha256)

- draft.json: `d5879d935807a9c5823e96667551653cc9c2fd8106cf9d54db1665398639e2fa`
- draft.md: `330b811d0d66d9c4d819e7dcfb6e3d685f2cc74e7839e47acc807d2100574eb4`
- raw-transcript.json: `b66a19bef382f636c5ff1de9d5d6319c0da09040a9f3c427dceb02c5027693fd`
- provenance.json: `1a67a7c1743f5a36c1179162f76bdcf2b3e37720164a46b05d96caf876633254`
- coverage.json: `142e2e49c93936dd4d0c730fd4498dc06778b9c5624434eb1e1fb02f2da7255a`
- packet manifest (on disk): `65c287efedc8428425f6cf59067926f2df66605306d131d4c69b7413b4f92264`
- unreferenced bundle: `a46c99bc76d4b38731520ca123e7289cbc7431a8df39489d002e905bdf76ec8f`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 12 of 12 ledger entries match the transcript; final message equals the annotation; Markdown equals the render; assessment is full review; 37 of 37 implementation hashes match; exactly 62 strict-ancestor entries; all 939 blobs hash to their names; the one diff section read in full. |
| Unassisted | No coverage field, no assistance flag. Standing instructions byte-identical to the unassisted guidance 4 prompt. |
| Opening context | Message, author, parent `00bbb583` and task SHA match Git. Cutoff is the committer date, 26 minutes after commit 62. |
| Catalog | The same eight rows as commit 62 (1, 4, 7, 10, 14, 15, 16, 17), which I checked against GitHub there; nothing was created or closed in the 26 minutes between. Four read and described accurately as not established to be related. |
| Source claims | Verified against the diff and the function at the task. The column index used the constant `width` and now uses the loop variable `w`; the verbose interval print is commented out and the final message kept; `pb.update` is guarded; a device-synchronisation loop is appended after the `return` inside the stream context. Bounds 0.1 and 1.9, tolerance 0.01, the objective, and the single caller `quantize_exl3` are as described. |
| Findings | Both hold. The appended loop is unreachable: the only path through the `with` block ends in `return best_scale`. The progress expression is unchanged and reports 100 from the first contraction; the entry attributes that to the multi-GPU ancestor entry (commit 24), which it read, and rechecked it in source. Both suspected with honest limits ("dead code, not a CUDA race"). |
| Scalar check | Re-ran: output identical. Unique tiles 4 to 12, 5 to 10, 4 to 8 on three grid shapes with unchanged sample counts; eleven progress updates, all 100. |
| Tests | 209 passed earlier in this session on the same implementation hashes. |

## Not verified

- No PyTorch or CUDA run; no effect on any model's scale or quality was measured, and the entry claims none.

## Must fix before canonical use

Reviewer-only.

1. The entry does not say when the constant index was introduced. Git shows it in the initial commit, so every conversion before this one sampled a single wrapped diagonal three times over. A canonical entry should say so and link the root entry's quantizer chapter, which the file-match hints named.
2. The inherited progress finding is a further observation of commit 24's finding, not a new defect.

## Next

Record this approval and continue the walk from commit 64.
