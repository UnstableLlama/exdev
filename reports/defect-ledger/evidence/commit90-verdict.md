# Verdict: commit-000090-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000090-001`
Packet: `.teacher/retrieval/000090-001`
Upstream: `40863d0690eb1cb1164bb973c9a22b1155ace172` "Add repetition, presence and frequency penalties"
Request: `reviews/requests/commit-000090-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry explains the plumbing, both kernels and the no-op changes correctly, and
found that this commit leaves the package unimportable. It missed a second, narrower defect in the presence/frequency
kernel, recorded below for the reviewer side only.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 18 of 18 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 89 strict-ancestor entries; 1,232 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 18 of 18 recorded tool calls identical, including the `run` call. |
| Diff read in full | The upstream diff is 27,863 bytes; the nine `git_show` calls cover it from offset 182 to the end. |
| Unassisted | Standing instructions byte-identical to 89/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 21, 22. Matches the eight open rows. |
| History plumbing | `Sampler.reqs_past_ids` starts false; `CustomSampler.__init__` ORs in each step's `reqs_past_ids()` before calling `alt()`, so a penalty step that turns into a no-op still requests history. `Job` allocates a pinned `(1, max_ids)` long tensor only when requested, `prepare_sampling_past_ids` copies sequence 0's ids into a prefix view, and the generator calls it for every active job before sampling. Correct. |
| `SS_RepP` | Positive logits divided by `rep_p`, others multiplied; the per-token factor is 1 inside the sustain window and otherwise the largest decay factor among occurrences (atomic max); output interpolates between original and penalised. Accepts `INIT` and `LOGITS`, leaves `LOGITS`, raises otherwise. No-op when `rep_p == 1` or the windows sum to zero or less. Correct. |
| `SS_PresFreqP` | Frequency accumulates `pen * freq_p` per occurrence (atomic add), presence takes the maximum `pen * pres_p`; both are subtracted. The docstring does say "Added". Correct. |
| Launch shape | 4,096 vocabulary entries per block, 1,024 threads; one shared float array for repetition, two for presence/frequency; both wrappers check batch size 1. Correct. |
| No-op changes | `SS_TopK` loses `assert top_k >= 1` and becomes a no-op below 1. `SS_TopP` becomes a no-op at 1.0 or 0.0, and its constructor still asserts `0 < top_p`, so the 0.0 branch is unreachable with assertions on. Correct. |
| Finding | `missing-combo-sampler`: correct. `sampler/__init__.py` line 27 imports `ComboSampler` from `.presets`; the name appears nowhere else in the task tree and `presets.py` is not in the diff. `import exllamav3` reaches that line. Suspected only because nobody ran the import. |

## Not verified

- Any import, kernel or test run.
- Whether device code can read the pinned host tensor through its host pointer on a given system. The entry lists this
  as untested, which is right.

## Reviewer-only knowledge (not for any teacher)

The presence/frequency kernel computes, for every history token inside the window,

`pen = MIN(1, MAX(0, 1 - (dist - sustain_range) / decay_range))`

with no branch for the sustain window (the repetition kernel has one). With `decay_range == 0` and a token exactly
`sustain_range` back, that is `0 / 0`. `MIN` and `MAX` are the plain ternary macros in `util.h`, which pass a NaN
through, so that token's frequency and presence become NaN and so does its output logit. Default arguments
(sustain 100,000,000, decay 0) only reach this with a history of that length, but `SS_PresFreqP(p, f, N, 0)` reaches it
as soon as the history has N tokens. Tokens strictly inside the window divide a negative number by zero and clamp to 1,
which is the intended value. Derived from source; not executed. The new tests use `(1, 0, 4, 4)` and the defaults, so
neither covers it.

Also: `shmemAtomicMaxF` is commented "val > 0". A negative `pres_p` (a presence bonus) breaks its unsigned comparison.

## Must fix before canonical use

1. The NaN case above is absent from the entry. A canonical entry needs it or an equivalent statement of what the
   presence/frequency kernel does at the window boundary with zero decay.

## Follow-ups

- Ledger: `missing-combo-sampler` is a new defect introduced at this commit. The NaN boundary is a separate one with
  origin reviewer observation; file it the way the validator accepts.

## Next

1. Record this approval.
2. Continue the walk at commit 91.
