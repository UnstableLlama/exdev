# Verdict: commit-000254-001 (teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-16. Upstream `f6e2de2a` "Add utility to build model_safetensors_index.json
for older quants that don't have one by default".

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false.

The finding `normalized-index-key` is **accepted as true as stated**. `read_header` renames
`multi_modal_projector.mm_input_projection_weight` to `...mm_input_projection.weight` in memory
(`tensor_name_fixes`), `add_tensor_files` maps the renamed key, and the new utility writes that key into
`weight_map` while the shard on disk keeps the old name. Correctly classed as external compatibility,
conditional on the alias being present, with no consumer failure claimed. It is a good catch: the utility is
aimed at older quantised models, which are the ones that can still carry the old projector name.

The entry made the commit's central checks itself: what the utility indexes (the collection's selected
entries, so later files win on duplicates), what `total_size` counts (payload bytes of selected tensors),
when it writes (never with zero files; one file only with `--force`; overwrites an existing index), and how
it differs from the compiler's writer.

## Artifacts

Request hashes match (13 of 13). `check.py` clean: `gpt-6.1-sol` medium, 44 implementation hashes, 15
evidence calls all cited and none bad, final equals annotation.

## Run checks (mine)

- New file read in full (49 lines); behaviour as described.
- I checked the one thing that could have broken it outright: `add_tensor_files` skips `__metadata__` and the
  synthetic `_header_offset`, so the loop over `tensor_file_map` never indexes a non-tensor entry. The entry
  states this.
- `compile.py` writes the same schema and only when there is more than one file. As stated.

## Must fix before canonical use

None. (The commit title says `model_safetensors_index.json`; the file written is
`model.safetensors.index.json`. Cosmetic, upstream's wording.)

## Ledger, with the next request

New external-compatibility record for `normalized-index-key` at `f6e2de2a`; relate it to the existing
header-name-collision / tensor-key identity from 215, do not merge.

## Next

Replacement 225 at guidance 12, then 255. One request at a time.
