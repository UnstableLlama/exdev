# Verdict: commit-000138-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000138-001`
Packet: `.teacher/retrieval/000138-001`
Upstream: `538dcae365891784729d198539f72ceece5631eb` "Fix compile for unquantized linear transforms"
Request: `reviews/requests/commit-000138-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry traces the whole round trip (export transposed, request a transpose
on load, conversion reloading from memory) and its square-matrix example makes the right point: matching shapes do
not prove the orientation is right. No findings, and none are needed for the task itself. The entry does not say
which commit broke the round trip; I traced that below for the ledger.

The ledger record `exllamav3-empty-codeblock-feedback--r001` is **accepted**.

## Artifacts reviewed (sha256)

All sixteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 9 of 9 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 137 strict-ancestor entries; 1,968 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 9 of 9 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 137/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows, as at 137 (issue 33 was closed at this cutoff, 2025-05-11T13:33:15Z). No qualifying closed row. Issue 34's three comments before the cutoff are from 6 and 7 May; its fourth is from July and is not in the packet. |
| Architecture trigger | Does not fire. |
| The change | In `SafetensorsCollection.get_tensor`, the in-memory branch now moves the tensor to the device, applies `.T.contiguous()` when `transpose` is set, and returns it. Was `return self.new_tensors[key].to(device)`. Nothing else. Correct. |
| Export | `LinearFP16.get_tensors` returns `self.weight.T.contiguous()`; the stored weight is input by output. Correct. |
| Load | `Linear.load_fp16` asks for the weight with `float2half = True, transpose = True, pad_to = (in_features, out_features)`; it is the only caller that passes `transpose`. Correct. |
| Conversion | `convert_model.py:380` to `385`: `set_new_tensors(q_tensors)`, `module.load(..., source = q_tensors)`, `set_new_tensors(None)`, then the forward pass that advances the calibration states. The only caller of `set_new_tensors`. Correct. |
| File-backed paths | Untouched. Correct. |
| Remaining gap | The in-memory branch still ignores `float2half` and `pad_to`. Correct, and stated as a limit. |
| Execution | Recorded output: a 2 by 3 weight exported as 3 by 2 and transposed back is unchanged; the square example gives [31, 46] with the transpose and [23, 53] without. Matches the prose. |
| Issue 34 | Labelled inference and expressly not claimed as fixed by this change. Correct. |
| Ledger `empty-codeblock-feedback--r001` | Accepted as drafted; introduced `e0cfb2e9`. |

## Reviewer-only notes (never to a teacher)

- **Where the defect came from (mine, source reading).** Before the deferred loader (`647bb7d5`, 119),
  `LinearFP16.__init__` did the transposing itself (`self.weight = weight.T`) and the loader returned tensors as
  stored, so file and memory sources behaved alike. 119 removed the transpose from the constructor and added the
  `transpose` keyword to `get_tensor`; the in-memory branch was left returning the tensor as stored. So from 119
  to this commit's parent, an unquantized linear layer reloaded from memory during conversion had its weight the
  wrong way round. For a rectangular weight that is a shape error at the first multiply; for a square one it is a
  silently wrong calibration pass. This is a fourth defect of 119, beside the three I recorded then. I did not
  establish which modules take this path in a real conversion.
- At 119 I checked this very row ("`LinearFP16` stores what it is given; `get_tensors` still returns `weight.T`")
  and did not follow it into the in-memory branch. Lesson: when a commit moves a transformation from a consumer
  into a loader keyword, check every branch of the loader for the keyword.

## Not verified

- Any conversion, or which layers are unquantized in one.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: a fix-derived record for the ignored transpose on in-memory tensors: introduced at `647bb7d5`, fixed at
   `538dcae3`, with the two consequences above stated as source reading only.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the ledger acceptance.
2. Continue the walk at commit 139.
