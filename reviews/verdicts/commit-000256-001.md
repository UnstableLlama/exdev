# Verdict: commit-000256-001 (teacher Sol, guidance 12, unassisted; first run under the review queue)

Reviewer: Fable. Date: 2026-11-17 (05:20 UTC). Upstream `f02c9afd` "compare_q_logits.py: Fix bug".
Run: `.teacher/runs/commit-000256-001`. Packet: `.teacher/retrieval/000256-001`. (Run line added 2026-11-17 at the author's request so the queue can bind the verdict; decision unchanged.)

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. No findings in the entry and
none found by me; the change is one line.

**256 may stand although its packet omitted 255/004.** 256 changes only `eval/compare_q_logits.py`; 255 adds
the Transformers adapter and touches nothing 256 reads. The missing entry did not matter, so no rerun.

**The journal reconciliation is accepted and advancement may resume at 257.** Before and after snapshots
differ only in `approved_entries` (adds `.teacher/runs/commit-000255-004`, removes nothing) and the pause
you recorded. Pausing and asking was right. In the 257 request, say in one or two lines why the 255
approval was not added when it was recorded (my guess: the verdict filed under the name
`commit-000255-004-review.md`) and whether the queue's `approve` path can leave the same gap.

## Artifacts

Request hashes match. `check.py` clean apart from the expected 254 of 255 ancestor entries:
`gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes equal to the accepted set, 11 evidence
calls all cited and none bad, final equals annotation, 3425 blobs, nothing after the cutoff. The new
`orchestration` object in `provenance.json` records the four orchestration hashes, which equal the files on
disk, and visible 254, strict 255, sparse true, as the request says. "Ran ahead of: none."

## Run checks (mine, tree at `f02c9afd`)

- `save_tensor` in `eval/compare_q.py`: dict, then list (numbered `tensor.N` keys), else a single
  `tensor` key. A tuple took the last branch. As stated.
- `load_tensor` rebuilds numbered keys as a list; `compare_q.py` splits a non-list reference into rows and
  indexes by row; its own producer builds a list. As stated, including the unimplemented alternative.
- The introducing commit is `8ff65b87` (2025-05-31), the only earlier commit to this file.

## Ledger

- `exllamav3-vision-floating-ceiling-overflow` r005 (table consequence from 234/002): **accepted**.
- This commit fixes the existing identity `exllamav3-compare-q-split-result-serialization`. File a revision
  recording the fix at `f02c9afd` with the next request.

## Next

257 onward with run-ahead.
