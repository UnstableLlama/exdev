# Verdict: commit-000204-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000204-001`
Packet: `.teacher/retrieval/000204-001`
Upstream: `1ad855ada6db1e3ad06b679acd08737f6edd101b` "convert.py: Tolerate OoM while computing proxy_err"
Request: `reviews/requests/commit-000204-001.md` (sha256 `3db377f959ed706eaede6eabc9d697faf9e6ea7877afadad551b40e49c75b9c4`)
Reviewed: 2026-11-16, working tree on top of `e9e83ff`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is true as stated.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 29 of 29 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 203 strict-ancestor entries; 2,952 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 28 of 29 identical. The one difference is the recorded tool error (`web_fetch` with `max_bytes` 110000, "Invalid max_bytes"), which my script shows as a mismatch because the tool raises where the transcript stored the error; the request declares it. |
| Unassisted | Standing instructions byte-identical to 203/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fifteen open rows at 2025-05-30T17:42:49Z; my query agrees. Seven closed rows selected, six by path alone, none cut; every discussion link is called an inference. |
| The change | The metric block (difference, transfers, two contractions, division) moves unchanged into a `try`; `del` becomes assignment of `None`; on `torch.OutOfMemoryError` the four names are cleared and `proxy_err` is -1.0. The conversion printout shows "(OoM)" for a negative value. Correct. |
| Scope of the handler | Quantization before it and reconstruction and packing after it are outside the `try`; no chunking or CPU retry. Correct. |
| Consumers | `quantize_exl3` is called only by `Linear.convert_exl3`, which returns the value unchanged to conversion `main` and to `test_quant_dequant`. Correct. |
| Worked example | With E = 0.1 W the ratio is 0.01. Agreed. |
| Finding: sentinel in the test | The test asserts only `proxy_err < max_proxy_err_per_K[K]`; -1.0 is below all eight thresholds. True, with the stated reach (the test, after a caught failure). |
| Execution | Standard-library arithmetic only; labelled as a model. |

## Not verified

- Any PyTorch execution or a real allocation failure; whether `torch.OutOfMemoryError` exists as a name in the
  oldest PyTorch this commit supports.

## Must fix before canonical use

None.

## Follow-ups

1. Ledger: the sentinel finding may be filed as suspected, introduced at `1ad855ad`, reach limited to the test.
   Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 205.
