# Verdict: commit-000298-001 (teacher Sol, guidance 12, unassisted; no repair)

Reviewer: Fable. Date: 2026-11-17 (17:45 UTC). Upstream `6f77a334` "Add recompile utility script".
Run: `.teacher/runs/commit-000298-001`. Packet: `.teacher/retrieval/000298-001`.

## Decision

**Approved for ancestor retrieval only. 298/001 is the entry in force for commit 298.** Canonical and
training stay false. Three findings accepted, two new (`replacement-only-tensors`,
`missing-quantization-metadata`), one carried (stale output directory). Continue at 299.

Run-ahead: the packet lacked 297, the direct parent and a functional dependency. The entry stands without a
rerun: the teacher read the parent's wrapper and both earlier consumers from source and reached the same
facts 297 records (fnmatch routing, newest source first, no fallback for a matched but missing tensor,
bulk enumeration over main names only), then carried the last one through to this commit's consequence. A
canonical version should be authored with 297 visible.

The central checks are the entry's own: what the unloaded accounting counts, that `compile_model` takes
`config.stc` only under `model_stc`, that the utility supplies no calibration keys so an input without
`quantization_config` fails after the shards are written, and that a tensor present only in an override
source (for example `.mcg`) is neither counted nor written while the loader treats its absence as a zero
multiplier.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes
equal to the accepted set, 57 evidence calls all cited and none bad, final equals annotation, 296 of 297
ancestors (sparse, as disclosed), 4312 blobs, nothing after the cutoff. My plain replay matched 49 of 57;
the other 8 are all `ancestor_read` calls that my replay refuses on a sparse packet ("does not match strict
ancestry"), not differences in content. The author's queue replay reports 57 of 57.

## Run checks (mine, tree at `6f77a334`)

- Diff read in full; every described edit is as stated, including the comment-only change in `linear.py`
  and the unused local `stc`, `tsize`, `dsize` in the script.
- `compile.py`: `args["shard_size"] * 1024**2` (line 41); `cal_rows`, `cal_cols`, `apply_out_scales` read
  only in the fallback branch (lines 157 to 160), after the copy at line 122. Finding true.
- `safetensors.py`: the variant `get_tensor_sizes` and `get_tensors` enumerate `main.tensor_file_map`;
  `linear.py` lines 166 to 167 read `.mcg` and `.mul1` as optional; `exl3.py` line 60 sets the multiplier to
  0 when absent. Finding true.

## Ledger (297)

`override-load-metrics` r001, `variant-collection-loader-api` r004 and `deferred-bf16-odd-tail` r004 are
accepted. The legacy `reviewer_observation` origin on the variant record is accepted as disclosed; validator
support for that origin is still owed.

## Must fix before canonical use

Re-author with 297 visible. Nothing else.
