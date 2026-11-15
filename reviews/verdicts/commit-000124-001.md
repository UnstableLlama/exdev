# Verdict: commit-000124-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000124-001`
Packet: `.teacher/retrieval/000124-001`
Upstream: `3c9ede55404c8ecce54494657f23f7056ea36a1a` "Use ComboSampler and add more prompts in HumanEval"
Request: `reviews/requests/commit-000124-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is correct.

The ledger candidate `exllamav3-gemm-selector-divisibility--r001` is **accepted as filed**.

## Artifacts reviewed (sha256)

All fourteen hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 11 of 11 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 123 strict-ancestor entries; 1,820 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 11 of 11 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 123/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path, the new record id, `reviewer_observation` or `Reviewer-only`. |
| Cutoff | The author is `gk`, not the maintainer (one of five such commits among the first 124). Its pull request, 32, was opened at 03:15:40Z, five minutes after the commit's own date (03:10:03Z, the cutoff). The packet rightly contains no trace of it: no row 32 in either catalog and no blob mentioning it. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 22, 24, 25, 26, 27, 28, 29. Matches the twelve open rows. One qualifying closed row, PR 20, closed 2025-04-25. |
| Architecture trigger | Does not fire. |
| Diff claim | `eval/humaneval.py` only: `ComboSampler` replaces `TopPSampler` with `rep_p`, `temperature`, `min_p`, `top_k`, `top_p`, `temp_last`; two prompt presets, `chatml` and `deepseek`; four new arguments (`--min_p` 0.0, `--top_k` float 0.0, `--temp_last`, `--rep_p` 1.0). Temperature and top-p keep 0.6. Correct. |
| Presets | Both put the problem in the user turn and again after a prefilled "```python" fence, with a four-space completion prefix; the existing path encodes special tokens and adds BOS. Correct. |
| Sampler | `ComboSampler` order and the zero-temperature argmax branch as verified at 111 to 115; defaults give no-ops for repetition penalty 1.0, min-p 0 and top-k below 1. One sampler object is shared by all jobs. Correct. |
| Unchanged parts | Termination on a non-indented line, sample assembly, JSONL writing and the optional evaluation call are untouched by the diff. Correct. |
| Execution | Recorded output: default 0.0 disabled; `5` parses to 5.0, not disabled; `TypeError` on a list slice. Matches the prose; Python lists, not tensors, as the entry says. |
| Discussion | PR 20 concerns padding failures and HumanEval comparisons; labelled contextual inference. Correct. |
| Finding `humaneval-top-k-float` | Correct. `--top_k` is `type = float`; `SS_TopK.alt` only substitutes below 1; `SS_TopK.run` uses `self.top_k` as a slice bound. Reached with a nonzero temperature. Suspected is right. |

## Ledger candidate (reviewer-only; never to a teacher)

`exllamav3-gemm-selector-divisibility--r001` states my 123 finding accurately: the four unguarded branches, the direct
path, the odd-multiple-of-128 width, the removed launch check and the unwritten tail; suspected; introduced at
`5d470a29`; no execution, fix or affected checkpoint claimed. Leaving my unverified recollection about a vocabulary
size out of the evidence is the right call. Accepted.

## Reviewer-only notes (never to a teacher)

- Same defect family as `chat-top-k-float` at 92 (`examples/chat.py`): a float-typed `--top_k` reaching `SS_TopK`.
  The entry read no ancestor prose and does not make the connection. Two sites, one cause; the sampler step does not
  coerce or validate.

## Revision

The first version of this file called this the first commit by an outside author. That was unchecked and wrong: `git log`
shows five non-maintainer commits up to here (three by `gk`, one each by `Async0x42` and `oobabooga`). Corrected above.
Nothing else changed; the approval stands.

## Not verified

- Any generation or scoring.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger, when next revised: record `humaneval-top-k-float` as a second site of the 92 identity, not a new defect.

## Next

1. Record this approval.
2. Continue the walk at commit 125.
