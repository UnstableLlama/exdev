# Verdict: commit-000136-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000136-001`
Packet: `.teacher/retrieval/000136-001`
Upstream: `a027848ddc37899274b540ed5ba009aa742d9d94` "Fix top-K float type"
Request: `reviews/requests/commit-000136-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry has no findings, and it missed one that I count as real: the new
assertion calls `.is_integer()` on a Python `int`, which exists only from Python 3.12. The entry came close. Its
limits section says the method's availability on older Python versions is "unestablished". That sentence is true,
so the entry stays accurate, but the fact is documented in Python's own release notes and should have been a
finding. See the reviewer section and follow-up 1.

All three ledger candidates are **accepted**.

## Artifacts reviewed (sha256)

All twenty-two hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 11 of 11 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 135 strict-ancestor entries; 1,949 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 11 of 11 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 135/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Cutoff | 2025-05-11T09:15:56Z. The PR 35 snapshot the session read has timestamps up to 06:13:49Z; the pull request's next comment on GitHub is 09:24:51Z, nine minutes after the cutoff, and is not in the session. PR 36 (opened 08:47:30Z) has no comment before the cutoff. Correct. |
| Catalog | Thirteen open rows: the eleven standing ones plus pull requests 35 and 36, both opened before the cutoff (issue 33 was closed at this cutoff). No qualifying closed row. |
| Architecture trigger | Does not fire. |
| `chat.py` | `--top_k` is parsed with `type = int` (was `float`); default 0; passed to `ComboSampler(top_k = ...)`. Correct. |
| `SS_TopK` | The constructor asserts `top_k.is_integer()` and stores `int(top_k)`. `run` masks from index `top_k` on; `alt` returns a no-op for `top_k < 1`. Correct. |
| `ComboSampler` | The argmax branch is taken for `temperature == 0.0 or top_k == 1`; the two penalty steps stay in front of it. `TopKSampler` already had the `top_k == 1` shortcut. Correct. |
| HumanEval | `eval/humaneval.py` still declares `--top_k` with `type = float` and passes it to the sampler; untouched here. Correct. |
| Argmax route | The penalty steps leave unsorted logits, so `SS_Argmax` runs its `INIT` or `LOGITS` branch. Correct, and it means the known sorted-branch defect (`inherited-sorted-argmax`, 80) is not reached by the new route. |
| PR 35, PR 22 | Both labelled inference; the entry claims no upstream link. PR 35's first comment does describe the float index problem. Correct. |
| Execution | Recorded output on Python 3.14.4: 0, 2, 0.0 and 2.0 accepted; 2.5 raises `AssertionError`; a list slice with 2.0 raises `TypeError`; the integer option parses. Matches the prose. |
| Ledger `gemm-zero-grid-cap--r001` | Accepted. One identity with three stages (123, 133, 135), as asked. I confirmed the cap and the scalar launch at `5d470a29`. |
| Ledger `mgemm-broadcast-scratch-capacity--r001` | Accepted as drafted. |
| Ledger `multi-gemm-leading-dimension-validation--r002` | Accepted. Adds 135 and the write past the output. |

## Reviewer-only notes (never to a teacher)

- **Missed finding (mine; documented behaviour, not executed here).** `int.is_integer()` was added in Python 3.12.
  On Python 3.10 and 3.11, which the code otherwise supports (it needs 3.10 for `match`), `SS_TopK(top_k)` with an
  `int` raises `AttributeError`. That is every `ComboSampler` built with an integer `top_k` unless temperature is 0
  or `top_k` is 1, including the default `top_k = 0`; `TopKSampler` with `top_k` above 1; and `SS_TopK(5)` in
  `tests/test_sampler.py`. The chat example, which this commit switches to integers, therefore fails at sampler
  construction on those versions with default settings. Before this commit an integer was simply stored. The
  repository states no minimum Python version. This machine has only Python 3.14, where the call succeeds, which
  is why the teacher's run could not show it.
- **Hindsight.** The upstream history has "top_k sampler: Fix int check for older Pythons" (`95cfa726`,
  2025-05-12). I have not read it. Expect it within the next few positions.
- With assertions disabled (`python -O`) a fractional `top_k` is truncated silently by `int()`. The entry names
  this as untested; it is a small point.

## Not verified

- Any execution on Python 3.10 or 3.11.
- Repository sampling, or tie behaviour of the argmax shortcut against top-K of one.

## Must fix before canonical use

1. The entry needs the Python 3.12 finding, or a later attempt that states it. For ancestor retrieval the present
   text is acceptable because its limits section already tells a later reader the point is open.

## Follow-ups

1. Ledger: file a reviewer-observation record for the integer check, introduced at `a027848d`, with the reach
   listed above and no fix entry yet. Like the selector-divisibility record it stays out of historical context
   and training.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval and the three ledger acceptances.
2. Continue the walk at commit 137.
