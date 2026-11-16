# Verdict: commit-000209-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000209-001`
Packet: `.teacher/retrieval/000209-001`
Upstream: `8ff65b874202176c1449e6a51998094ef60f94f0` "compare_q.py: Option to capture logits in streaming mode (for large unquantized models)"
Request: `reviews/requests/commit-000209-001.md` (sha256 `70c4048f88bf15e55002575f4d1e5073f54f34cffcc8ac524246585d5d29325c`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and both findings are true as stated. Two consequences are missing (below).
The ledger correction filed with this request is accepted.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 36 of 36 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 208 strict-ancestor entries; 2,987 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 35 of 36 identical. The one difference is the recorded tool error (`web_fetch` with `max_bytes` 110000), declared in the request. |
| Unassisted | Standing instructions byte-identical to 207/001's (208 was a merge and carried the extra merge sentences). Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fifteen open rows at 2025-05-30T23:11:56Z; my query agrees. Three closed rows selected; discussion links are called inferences. |
| The new script | Builds the model without loading it, takes the first `--rows` rows of the data specification's tokens, splits them into batches, and for each batch loads, runs and unloads every module in turn; batch logits go to the CPU, are concatenated, split into single rows and passed to `save_tensor`. Defaults ten rows, five per batch, device 0. Correct, including that all logits are held in memory before writing and that every module is reloaded for every batch. |
| The consumer | `--logits_file` replaces the automatic reference search and the reordering; a loaded dense tensor is split into rows; a loaded list is left alone. Correct. |
| Deferred loading | The script does not consult `can_defer_load` or retry, unlike the general loader. Correct. |
| Finding: split result | `Tensor.split` returns a tuple; `save_tensor` handles `dict` and `list` only, so the tuple reaches `save_file({"tensor": tuple}, …)`. True. This is the script's only output step, so as written it cannot save what it captured. |
| Finding: filtered reference | The existing `compare-q-filtered-reference-dependency` identity, unchanged in the automatic branch. True; no second identity. |
| Execution | The parent's `save_tensor` extracted by AST and run with a stub writer on a list and a tuple; labelled, with the limit that no tensor or file was involved. |

## Reviewer knowledge (hindsight, never to a teacher)

Upstream `f02c9afd` (2025-06-08) "compare_q_logits.py: Fix bug" wraps the split in `list(...)`. That confirms the
first finding. Do not record the fix before the walk reaches it.

## Not verified

- Any Torch, safetensors or model execution.

## Must fix before canonical use

1. With `--logits_file` given and a model specification that contains `out_logits`, `test_ppl` still treats that
   model as the producer and at the end calls `save_tensor(ref_logits, logits_file)`, overwriting the reference
   file the user supplied. The entry states the rule ("a specification containing out_logits is a producer") but
   not this consequence.
2. `--dataspec` is not marked required and has no default, but the script opens it unconditionally. The entry
   says only that the model and output paths are required.

## Ledger items filed with this request

- `exllamav3-layernorm-reference-shape--r002`: **accepted.** Supersedes r001, introduction `f45eb4ce`
  source-supported, still suspected, not eligible for teacher context.

## Follow-ups

1. Ledger, with 210's request: the split-result finding as suspected, introduced at `8ff65b87`; the
   filtered-reference identity gains this commit as an observation.

## Next

1. Record this approval with `--approve`.
2. Proceed to 210.
