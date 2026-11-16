# Verdict: commit-000162-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000162-001`
Packet: `.teacher/retrieval/000162-001`
Upstream: `a19538cf1e3b3f46ccdb347ff076fd4838a4910b` "compare_q.py: Some fixes"
Request: `reviews/requests/commit-000162-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only**, with a canonical-use condition. Canonical and training remain false.

Each of the three edits is described correctly, and the entry found something useful that is not on the changed
lines: results are cached on disk by arguments, so old cached numbers survive this fix unless the cache is
cleared. What it missed is how two of the three edits depend on each other (below). One sentence says they are
independent; in that respect it is wrong.

The change to `cycle_notify.notify` is accepted as made.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 14 of 14 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes (now including `cycle_notify.py`); exactly 161 strict-ancestor entries; 2,491 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 14 of 14 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 161/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path or the tracking files. |
| Catalog | Eleven open rows at 2025-05-15T22:33:48Z (issue 38 and pull request 22 are closed by then); my query agrees. No closed row qualified; nothing cut. |
| Architecture trigger | Does not fire. |
| Edit 1, head detection | `module.key == "lm_head"` becomes `module.key.endswith("lm_head")` in the V3 adapter's `get_storage_info`. Every registered model uses the exact key, as the entry says, so no affected model is shown. Correct. |
| Edit 2, masking | `output[..., model_instance.config.vocab_size:] = float("-inf")` after the forward pass in `fwd_exllamav3`. The head `Linear` pads its output width to a multiple of 128, and `compare_q.py` applies `log_softmax` over the last dimension, so padded columns were in the denominator before. Correct, including "the configured vocabulary size, not a tokenizer-derived count". |
| Edit 3, inference mode | `@torch.inference_mode()` on `main`. Correct that neither `test_ppl` nor the adapter is decorated. |
| The cache | `test_ppl` is wrapped by `disk_lru_cache("test_ppl")`, keyed on the JSON of its arguments; `--clear_cache` deletes the entries for the selected specs. Correct, and a real consequence for anyone re-running the comparison. |
| Execution | Recorded output: about 256 before and 129 after for a 129-token vocabulary padded to 256 with zero logits; the three suffix cases. Matches the prose. |
| `cycle_notify.py` | `notify` now fails only on a non-zero exit, a timeout, or output without `Queued message`. As asked. 278 tests in my run. The first live detached cycle delivered its message to your thread. |

## What the entry missed (reviewer-only; never to a teacher)

`Model.forward` is decorated with `torch.inference_mode`, so the logits it returns are inference tensors. The
new masking line writes into that tensor in place. PyTorch does not allow an in-place write to an inference
tensor outside inference mode; it raises. So edit 3 is not a separate improvement: putting `main` in inference
mode is what makes edit 2 legal on the path through `main`. It also means `fwd_exllamav3` now fails if it is
called from code that is not in inference mode, which the entry half-saw ("direct calls … do not acquire this
new context") without drawing the consequence. Source reading plus PyTorch's documented rule; this machine has
no PyTorch, so nothing was run. The only caller in the tree is `test_ppl` under `main`, so nothing is broken at
this commit.

## Not verified

- Any model evaluation, and the PyTorch behaviour above by execution.

## Must fix before canonical use

- The sentence in Reasoning that the three edits address their concerns "independently", and the missing
  dependency between the in-place mask and inference mode.

## Follow-ups

1. Ledger: a reviewer-observation record, classification `new_requirement`, introduced at `a19538cf`:
   `fwd_exllamav3` writes in place into an inference tensor and therefore requires its caller to be in inference
   mode; satisfied by `compare_q.main` at this commit. Source inspection only, not executed, excluded from
   teacher input.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval.
2. Continue at 163, detached.
