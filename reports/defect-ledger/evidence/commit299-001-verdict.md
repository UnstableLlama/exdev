# Verdict: commit-000299-001 (teacher Sol, guidance 12, unassisted; validation repair used, old policy)

Reviewer: Fable. Date: 2026-11-17 (18:45 UTC). Upstream `e370ed28` "safetensors: Add trie search for tensor file map (marisa_trie)".
Run: `.teacher/runs/commit-000299-001`. Packet: `.teacher/retrieval/000299-001`.

## Decision

**Approved for ancestor retrieval only. 299/001 is the entry in force for commit 299.** Canonical and
training stay false. Three findings accepted, two new (`exact-prefix-uses-filename`,
`cached-index-after-additions`), one carried (metrics interface). Continue at 300.

The central checks are the entry's own: which four selectors moved to the trie and which two did not; that
the exact-prefix branch appends the map's value (a filename) where the old code kept the tensor name, so an
exact-key prefix now fails; and that the `lru_cache` trie is never invalidated although `add_tensor_files`
can add names.

Run-ahead: the packet lacked 298, whose recompile path consumes these selectors. The entry read
`compile_model` and `Model.get_storage_info` from source and names both as consumers; it stands without a
rerun. A canonical version should be authored with 298 visible.

## Validation repair (old policy `validator-only-v1`, last run under it)

I compared refused (transcript index 76) with final (index 85). Nothing in the final is false and all three
findings survive. Dropped, to restore before canonical use:

1. The namespace-boundary remark: querying `prefix + "."` keeps `layer` from matching `layer2`.
2. The wider list of inspected consumers (quantization metadata generation, Transformers integration,
   Gemma3 and Mistral3 additional-tensor metadata).
3. The source note on closed issues 2, 16, 17, 21 and 49.

## Artifacts

Request hashes match. `check.py`: `gpt-6.1-sol` medium (server-confirmed), 40 evidence calls all cited and
none bad, final equals annotation, 297 of 298 ancestors (sparse, as disclosed), 4321 blobs, nothing after
the cutoff. Three implementation hashes differ from the live files (`codex_adapter.py`, `cycle.py`,
`validation_repair.py`): expected, because the accepted repair change was applied after this run exited; the
run's recorded hashes are the previously accepted set. My plain replay matched 37 of 40; the other 3 are the
three `ancestor_read` calls my replay refuses on a sparse packet.

## Run checks (mine, tree at `e370ed28`)

Diff read in full. `keys = [self.tensor_file_map.get(prefix)]` in all four rewritten selectors;
`tensor_file_map` maps tensor name to filename, so the appended item is a filename. `@lru_cache` on
`get_tensor_file_map_trie`; no invalidation anywhere in the diff. Ordinary `get_tensor_sizes` and variant
`get_tensors` are untouched. `marisa_trie` added to both dependency lists. All as stated.

## Ledger (298)

`recompile-replacement-only-tensors` and `recompile-missing-quantization-metadata` are accepted.

## Must fix before canonical use

Points 1 to 3 above; re-author with 298 visible.
