# Verdict: commit-000297-001 (teacher Sol, guidance 12, unassisted; validation repair used)

Reviewer: Fable. Date: 2026-11-17 (17:15 UTC). Upstream `6341b119` "Loader: Add tensor override script".
Run: `.teacher/runs/commit-000297-001`. Packet: `.teacher/retrieval/000297-001`.

## Decision

**Approved for ancestor retrieval only. 297/001 is the entry in force for commit 297.** Canonical and
training stay false. Three findings accepted: one new (`override-load-metrics`), two carried (stale
`Model.get_load_metrics`, deferred BF16 odd tail). Continue at 298.

The entry makes the central checks itself: wildcard routing with a default source, precedence by reverse
source addition after grouping by directory (so not YAML row order), no fallback when the chosen source lacks
a key, bulk operations that enumerate only the main names, where each consumer installs the wrapper, and
the missing `metrics` attribute.

## Validation repair: first run where the repair lost substance

I compared the refused annotation (transcript index 86) with the final one (index 91). The validator's only
message was about evidence on one verification, but the teacher rewrote the whole annotation and shortened
it. Nothing in the final is false. These true statements of the refused version are gone and go under "must
fix before canonical use":

1. `init()` now reads `args.override`, so a caller that builds its own namespace without `add_args` must
   supply it (the refused version said this; the final only lists the six in-tree callers).
2. In the bulk operations a chosen source that lacks a key enumerated from main can fail (`list_tensors`
   indexes `stc.tensor_file_map[key]` directly).
3. Architecture configuration and the tokenizer still come from the original model directory; model B is
   untouched in `model_diff`.
4. `model_diff` brackets each module load with deferred begin/end without the `can_defer_load` guard
   (existing condition, now also reaching the wrapper).
5. All four source notes on the fetched discussions (PR 22, PR 26, issues 2, 6, 7, 16, 17, 21, 33, 38, 49)
   were dropped; the final keeps only the limit sentence about PR 26 and issue 33.

Author: in the next request say how often a repaired final is shorter than the refused one (bytes of both,
for 266, 269, 270, 271, 297). No implementation change is ordered here; I am reporting this to the user.

## Artifacts

Request hashes match (14 of 14). `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45
implementation hashes equal to the accepted set, 43 evidence calls all cited and none bad, replay 43 of 43,
final equals annotation, 296 of 296 ancestors, 4302 blobs, nothing after the cutoff. Complete packet, ran
ahead of nothing. Repair provenance: policy `validator-only-v1`, feedback verbatim, one call after feedback,
selected final index 91.

## Run checks (mine, tree at `6341b119`)

- Diff read in full. `add_stc` prepends; `find_stc` first `fnmatch` hit or main; `has_tensor`,
  `get_tensor`, `has_tensor_group` use the chosen source only; `get_tensors`, `list_tensors`,
  `get_tensor_sizes`, `max_key_len` enumerate main. As stated.
- `VariantSafetensorsCollection.__init__` sets only `main` and `stcs`; `SafetensorsCollection.__init__`
  sets `self.metrics` (line 90); `model_init.py` line 148 reads `config.stc.metrics`. Finding true.
- `model.py` line 405 calls `config.stc.get_metrics()`; no such method remains anywhere. Finding true.
- `model_diff.py`: both models constructed before the override block; modules read `self.config.stc` at
  load time. As stated.
- Unconditional `import yaml` in both consumers; `pyyaml` added to both dependency lists. As stated.

## Must fix before canonical use

Points 1 to 5 above.
