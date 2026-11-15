# Verdict: commit-000091-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000091-001`
Packet: `.teacher/retrieval/000091-001`
Upstream: `c7da6b7bb7e45ad06f168594ffb374501ba818cb` "Add combo sampler preset"
Request: `reviews/requests/commit-000091-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry says what the commit repairs (the dangling import from commit 90) and
what it does not: the new preset cannot be constructed with its own defaults.

Both ledger records for commit 90 are **accepted as recorded**.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 11 of 11 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; exactly 90 strict-ancestor entries; 1,247 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 11 of 11 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 90/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path, or either new ledger id (`exllamav3-missing-combo-sampler`, `exllamav3-presfreq-zero-decay-boundary`). The ancestor entry for commit 90 that the teacher read is the approved draft, which does not contain my boundary observation. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 15, 21, 22. Matches the eight open rows. |
| Diff claims | One new class, `ComboSampler(CustomSampler)`, with the argument defaults and the fixed step order the draft gives: repetition, presence/frequency, temperature (early unless `temp_last`), min-p, top-k, top-p, temperature (late if `temp_last`), sample. Both penalty steps receive the same sustain and decay arguments. Correct. |
| Finding | `combo-default-min-p`: correct. `min_p` defaults to 0.0 and the stack builds `SS_MinP(min_p)` unconditionally; `SS_MinP.__init__` asserts `0.0 < min_p <= 1.0` and has no `alt`. So `ComboSampler()` raises with assertions on, against the comment "Steps with default parameters become no-ops". Suspected only because nobody ran it. |
| Other claims | `SS_Temperature(1.0)`, `SS_TopK(0)` and `SS_TopP(1.0)` become no-ops; history is requested before no-op substitution, so a constructed `ComboSampler` always requests past ids. Correct. |

## Ledger records

- `exllamav3-missing-combo-sampler--r001`: accepted. Suspected defect, introduced at `40863d06`, observation sourced to the
  90/001 draft, no fix claimed.
- `exllamav3-presfreq-zero-decay-boundary--r001`: accepted. Suspected defect, introduced at `40863d06`, observer Fable,
  source my 90/001 verdict, not eligible for historical context, training policy not applied. Using
  `authoring_observation` as the origin because the validator has no reviewer category is fine as long as the
  observation record keeps the observer, which it does.
- When you record 91's approval, add this commit as the fix for `exllamav3-missing-combo-sampler`: it defines the missing
  name. That is now inside the walk, not hindsight.

## Not verified

- Any import or construction. Nobody ran one; the entry says so.

## Reviewer-only note (not for any teacher)

`ComboSampler` passes one `rep_sustain_range` and `rep_decay_range` to both penalty steps, and `rep_decay_range`
defaults to 0. So `ComboSampler(freq_p=…, rep_sustain_range=N, min_p=…)` is a plain public route into the zero-decay
boundary recorded at commit 90. Worth an observation on that ledger record.

## Must fix before canonical use

None.

## Next

1. Record this approval and the ledger acceptance.
2. Continue the walk at commit 92.
