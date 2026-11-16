# Verdict: commit-000155-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000155-001`
Packet: `.teacher/retrieval/000155-001`
Upstream: `ce58d99c710900b0fe78229e8b193ab50b60234a` "BlockSparseMLP: Disable padding for routing gate"
Request: `reviews/requests/commit-000155-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the inherited finding is correct. For a one-line change the entry does the
right amount: it follows the padding arithmetic into `Linear`, shows that nothing trims the router's output before
softmax and top-k, and labels the motive as inference.

Both ledger candidates are **accepted**, the second with one wording revision (follow-up 1).

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 14 of 14 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 154 strict-ancestor entries; 2,297 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 14 of 14 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 154/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-14T12:46:33Z: 1, 4, 7, 10, 14, 22, 26, 27, 28, 29, 33, 34, 38. My query agrees (33 was reopened on 13 May). No closed row qualified; nothing cut. |
| Issue 38 and the cutoff | Opened 2025-05-14T06:52:25Z, six hours before the cutoff. Its first comment is the maintainer's at 23:35:22Z the same day, after the cutoff, and is not in the packet. The entry describes only the body. Correct. |
| Architecture trigger | Does not fire. |
| The change | One added line, `pad_to = 1`, in the constructor call for the routing gate. Nothing else. Correct. |
| Padding arithmetic | `Linear` sets each dimension to `(n + pad_to - 1) // pad_to * pad_to`, default 128. With 1 it is the identity. Correct. |
| Why it matters | `load_fp16` asks the loader for the rounded shape; `LinearFP16.forward` returns `out_features` columns; `BlockSparseMLP.forward` applies softmax and `topk` over all of them and uses the indices to pick experts. Nothing in between drops padded columns. Correct, and "the likely rationale" is rightly labelled inference. |
| Unchanged | The expert projections keep the default padding; dtype, top-k, renormalisation and path selection are untouched. Correct. |
| Execution | Recorded widths old/new: 128/8, 128/64, 128/128, 256/129. Matches the prose. |
| Finding `inherited-all-expert-fused-shape` | Correct and still present: the commit touches only the constructor. Inherited and suspected are right. |
| Source notes | Issues 34 and 38 are linked only through `linear.py` and the entry says neither explains this change. Correct. |

## Ledger candidates

- `exllamav3-ppl-axis-bound--r001`: accepted. Introduced at `9575f7d8` (a search of the task's ancestry for the
  loop bound finds that commit and no other), observed at 127 and 154, effect limited to a vocabulary smaller than
  the sequence. As asked.
- `exllamav3-model-diff-unconditional-deferral--r001`: accepted as a reviewer observation. The description, the
  guard in the two model loaders and the copy in `LinearFP16.__init__` are as recorded. One sentence needs
  revising; see follow-up 1.

## Reviewer-only notes (never to a teacher)

- **For the models registered so far the change alters nothing.** `qwen3_moe.py` is the only user of
  `BlockSparseMLP`, and the seven reference configurations checked at 141 and 153 all have 128 experts, which
  the old rounding left at 128. The entry says that counts divisible by 128 are unchanged but did not fetch a
  configuration, so it does not connect the two. That is a fair limit for this entry, not a defect in it.
- **What the old padding would have done for another count.** Padded weight columns are zero, so their logits
  are 0, not `-inf`; softmax gives them real probability and `topk` can return an index at or above
  `num_experts`. The entry stops at "artificial routing candidates", which is as far as it can go without
  running anything.
- **Issue 38 is the field report of an existing reviewer record.** Its traceback ends in the loader's
  `padded[...].copy_(tensor)` with 49,920 against 399,360, during `GatedMLP.load` of an eight-way slice of a
  `DeciLMForCausalLM` model. That is `exllamav3-sliced-fp16-padding-target` (mine, from 119), which until now
  said no supported checkpoint of the required width had been identified.
- **Hindsight (after the cutoff):** the maintainer's first comment on issue 38 says the regression came in with
  the padding work and conflicts with how very wide layers are split. Expect the fix within a commit or two.

## Not verified

- Any tensor operation or model run.
- The summary of issue 34 beyond its title.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, `exllamav3-model-diff-unconditional-deferral`: file r002 replacing "no registered model at this
   revision is established to exceed it". Issue 38's body, which is inside the cutoff from 155 on, shows a
   registered architecture (`DeciLMForCausalLM`) with an MLP sliced eight ways. State the limit as it now stands:
   such a model exists, and at this revision its unquantized load fails earlier on the padding mismatch.
2. Ledger, `exllamav3-sliced-fp16-padding-target`: file a revision adding issue 38's body as cutoff-bound
   corroboration (the traceback and the two sizes), available from 2025-05-14T06:52:25Z. Status stays suspected
   until a fix is reviewed; no execution was done here.
3. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the two acceptances.
2. Continue the walk at commit 156.
