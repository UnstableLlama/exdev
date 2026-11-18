# Verdict: commit-000225-002 (replacement of 225/001; teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-16. Upstream `532d7865` "Gemma3: Add vision model".

## Decision

**Approved for ancestor retrieval only. 225/002 replaces 225/001 as the entry in force for commit 225** for
packets prepared from now on; 225/001 is kept as history. Canonical and training stay false.

The finding `gemma3-preprocessor-required-for-text` is **accepted as true as stated** and the classification
(new requirement) is right: `Gemma3Config.__init__` opens `preprocessor_config.json` and asserts the
processor type unconditionally, before any caller can choose the text component; `Gemma3TextConfig` is
unaffected. 225/001 said this in its Impact text without filing it; nothing is lost and nothing about the old
narrative is contradicted.

The entry made the header check this replacement exists for (second "must fix" of the 225/001 verdict): the
complete vision tensor inventory of `gemma-3-4b-it` against the names the tower requests, the projector
stored under the legacy name with shape `[input, output]` and loaded through the header normalisation with
`transposed_load = False`, and the reason for `pad_to = 1` (4304 would round to 4352). It is a superset of
225/001 apart from one small statement listed below.

## Artifacts

Request hashes match (32 of 32). `check.py` clean: `gpt-6.1-sol` medium, 44 implementation hashes, 66
evidence calls all cited and none bad, final equals annotation. Manifest differs from 225/001's in
`guidance_version` only (9 to 12). The failed `preprocessor_config.json` fetch is honest: the packet holds
none for these models, so those values stay unverified, as the entry says.

## Run checks (mine)

- All eleven vision configurations: 1152/4304, 27 layers, 16 heads, 896, patch 14, 256 image tokens; KV heads
  and head dimension absent in all eleven; the five QAT files spell out channels 3, epsilon 1e-6 and the GELU
  variant. As stated.
- All eleven checkpoints: the 437 vision-tower tensors are identical in name, shape and dtype across all of
  them and are exactly the families the entry lists (patch weight `[1152, 3, 14, 14]` and bias, positions
  `[4096, 1152]`, 27 layers with weight and bias for both norms, four attention projections and `fc1`/`fc2`,
  post-norm). Projector `mm_input_projection_weight` is `[1152, 2560 | 3840 | 5376]` with the norm `[1152]`
  and no bias. The entry read 4B in full and sampled 12B and 27B; the rest is mine (reviewer-only).
- Source: unconditional preprocessor read, `pad_to = 1`, `transposed_load = False`, `causal = False` in
  `get_image_embeddings`. As stated.

## Still open (must fix before canonical use)

1. **Width and height order.** First "must fix" of the 225/001 verdict, still not in the entry. `preprocess`
   builds `size` as (height, width), compares it with PIL's `image.size` and passes it to `image.resize`,
   both of which use (width, height). Hidden because every reference size is square (896). The entry says
   only "resizes to its configured tuple". Already recorded as
   `exllamav3-gemma3-preprocess-width-height-order` (reviewer observation); no new ledger work.
2. 225/001 says outright that all eleven configurations omit the KV-head and head-dimension fields; 225/002
   gives the derived values without that statement (the request notes this itself).

## Ledger

- Filed with this request: `exllamav3-normalized-index-key` r001: **accepted**.
- With the next request: a new record for `gemma3-preprocessor-required-for-text` at `532d7865`
  (new requirement, source only).

## Next

255 at guidance 12, then replacement 234 (the last one). One request at a time.
