# Verdict: commit-000141-003 (replacement of 141/001; teacher Sol, guidance 12, reviewer-assisted)

Reviewer: Fable. Date: 2026-11-16. Upstream `a5caa423` "Add Qwen3MoeForCausalLM".

## Decision

**Approved for ancestor retrieval only. 141/003 replaces 141/001 as the entry in force for commit 141** for
packets prepared from now on; 141/001 and the declined 141/002 are kept as history. Canonical and training
stay false. It is a reviewer-assisted entry (coverage request `commit-000141-003.coverage.md`, questions only)
and joins the list of assisted entries in force.

All three findings are **accepted as true as stated**: `inherited-all-expert-fusion` (existing identity,
unchanged reach), `published-fp8-load` and `published-gptq-load` (new; both correctly classed as external
compatibility limits established from source and headers, not observed failures).

It is a superset of 141/001: every mechanism the old entry stated is present, including the calibration
maps 141/002 dropped, and it answers the old verdict's "must fix" (what the headers show and which published
variants cannot load). This time the entry made that check itself.

## Artifacts

Request hashes match (24 of 24). `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 44 implementation
hashes, 57 evidence calls all cited and none bad, final equals annotation, 140 ancestors, 2196 blobs, nothing
after the cutoff. The manifest differs from 141/002's only in `coverage_request` and `walk_input_contract`;
the bound coverage text is byte-identical to the filed file and appears in the teacher's prompt.

## Run checks (mine, against the packet and tree)

- Every header statement is exact: FP8 projections `F8_E4M3` with the stated `weight_scale_inv` shapes for
  both sizes, router and head F32; GPTQ `g_idx`/`qweight`/`qzeros`/`scales` with every stated shape and dtype
  for attention and expert projections in both sizes, no `.weight` for them, router and head F16; ordinary
  repositories BF16 throughout.
- Every configuration difference listed is real and the list is complete apart from the dimensions already
  described (intermediate_size, max_window_layers, EOS and positions for Base, torch_dtype and
  transformers_version for GPTQ, quantization metadata).
- Source: EXL3 group test `[sv|svh], [su|suh], trellis` then `.weight`; the two error paths and their
  messages; calibration labels `block.attn.input`, `block.attn.o`, `block.mlp.input`, `block.mlp.{idx}.down`,
  router `None`, head `block`; `capture_H` keyed by label with a first key; conversion passes
  `activate_all_experts` from `calibration_all_experts`. All as stated.
- Head: bare-name probe against stored `lm_head.weight`, skipped here because all seven are untied. Correct.

## Not verified

Any load, conversion or generation. The entry samples layer 0 and the head; my own pass over all shards found
no layer that departs from the sampled pattern (reviewer-only).

## Must fix before canonical use

None beyond the standing limits the entry states itself.

## Downstream

153/002, 163/002 and 187/001 read the old 141 prose. 141/003 contradicts nothing in 141/001, so none is
invalidated; no action.

## Ledger, with the next request

- `exllamav3-all-expert-fused-shape`: no new record; 141 is already an affected revision.
- New external-compatibility records for the FP8 and GPTQ limits at 141. Relate the FP8 one to
  `exllamav3-qwen3-fp8-checkpoint-format-boundary` and `exllamav3-fp8-dtype-not-loadable`; do not merge.
  Use the full repository URL, as every existing record does.

## Note on the request

First request written with the author's Codex session on `gpt-6.1-sol`. Accurate against the files, hashes
correct, limits stated, no author-model claim.

## Next

250 at guidance 12, then replacement 158. One request at a time.
