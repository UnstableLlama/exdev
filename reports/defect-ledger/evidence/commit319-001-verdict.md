# Verdict: commit-000319-001 (teacher Sol 6.2, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-18 (00:23 UTC). Upstream `5cb70f59` "model_diff.py: Add option to save IDs
and logits". Run: `.teacher/runs/commit-000319-001`. Packet: `.teacher/retrieval/000319-001`.

## Decision

**Approved for ancestor retrieval only. 319/001 is the entry in force for commit 319.** Canonical and
training stay false. Two suspected findings accepted: the inherited perplexity helper bounds a
position-axis slice by vocabulary width (an observation of the existing ppl-axis-bound identity, not a new
one), and the files are written under the keys `logits` and `input_ids`, which `compare_q.py`'s
`load_tensor` does not recognise (external compatibility; the flags promise no round trip, as the entry
says).

Ran ahead of 318 (new ppl_transformers.py); irrelevant to model_diff.py, stands; 318 is approved, so
record now. The entry makes the checks that matter itself: all three call sites take the single-tensor
branch; ids are saved before the first forward and logits after the layer report but before the metrics,
so a failed write stops the run there; what is saved is the state at the end of the zipped module walk; and
with `--keep_b` the "A" file holds B's output over the kept prefix.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.2-sol` medium, 45 implementation hashes equal the accepted
003 set, 41 evidence calls all cited, final equals annotation, 317 of 318 ancestors (sparse, as disclosed),
4492 blobs, nothing after the cutoff. My plain replay matched 34 of 41; the other 7 are the
`ancestor_read` calls it refuses on a sparse packet.

## Run checks (mine, tree at `5cb70f59`)

Diff and the loop around it read. `if idx < args.keep_b: state_a = state_b.clone()` precedes the save.
`compare_q.py` 76 to 86: `load_tensor` looks only for `tensor` and `tensor.N`. `ppl` takes its loop bound
and chunk size from `logits_.shape[1]` while slicing axis 0. As stated.

## Ledger

The five 318 records are accepted as filed: native-loader-flags-ignored r001,
nonpositive-row-count-still-appends r001, scoring-buffer-retained r001 (new at `4265c9e1`);
length-without-next-token-targets r002 and window-ending-at-corpus-boundary-skipped r002 (one observation
appended each, earlier ones equal). For 319, file the vocabulary-bound finding as a revision of
`exllamav3-ppl-axis-bound`, not a new identity.

## Must fix before canonical use

Say what is in the saved logits file: the type and shape of the final state (rows by 2048 by vocabulary,
in the head's output type), since nothing is cast or moved before writing.
