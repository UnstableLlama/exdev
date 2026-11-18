# Verdict: commit-000158-002 (replacement of 158/001; teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-16. Upstream `9665ba99` "Add Mixtral architecture".

## Decision

**Approved for ancestor retrieval only. 158/002 replaces 158/001 as the entry in force for commit 158** for
packets prepared from now on; 158/001 is kept as history. Canonical and training stay false.

Both findings are **accepted as true as stated**:
- `mixtral-sparse-calibration-coverage` (new). `MixtralModel` does not set `calibration_all_experts`; the
  base default is false; conversion passes it as `activate_all_experts`, captures lazily per `qmap`, and later
  indexes `capture_H[linear.qmap]` without a guard (`convert_model.py` line 355). An expert never routed to in
  a layer therefore has no `block.mlp.{idx}.down` entry. Correctly stated as conditional on routing coverage;
  with eight experts and two selected per token it is a latent path, not an expected failure, and the entry
  does not claim more.
- `inherited-all-expert-fused-dimensions`: existing `exllamav3-all-expert-fused-shape` identity, eight
  against two here; correctly noted as not reached by ordinary Mixtral conversion.

158/001 had no findings and neither reviewer nor teacher saw the calibration gap then. The entry also adds the
comparison with the Qwen3 MoE builder that 158/001's verdict asked for, and it is that comparison that
exposes the gap. It made the central checks (builder against headers, builder against its sibling) itself.

## Artifacts

Request hashes match (31 of 31). `check.py` clean: `gpt-6.1-sol` medium, 44 implementation hashes, 52
evidence calls all cited and none bad, final equals annotation. Manifest differs from 158/001's in
`guidance_version` only.

## Run checks (mine)

- All four configurations as stated (dimensions, eight experts top two, vocabularies 32000/32768, positions
  32768/65536, SiLU, epsilon 1e-5, theta 1000000, untied, no sliding window).
- Every tensor of all four checkpoints (995 and 1739 names, all shards) is one the builder requests, with the
  stated shape, BF16; nothing missing, nothing extra, all four store `lm_head.weight`. This includes
  `Mixtral-8x7B-Instruct-v0.1`, whose headers the teacher did not open and says so.
- Builder: keys `w1`/`w3`/`w2` to gate/up/down, router `gate`, half intermediates and output, calibration
  maps, no all-expert flag. As stated.

## Must fix before canonical use (peripheral)

1. 158/001 said all four configurations omit `head_dim`, so the division fallback is the path actually used;
   158/002 describes the fallback and gives 128 but does not say the configurations omit the field.
2. Open at least one `Mixtral-8x7B-Instruct-v0.1` header, or say the family claim rests on three of four.
3. Small facts of 158/001 not repeated: the declared bfloat16 against half intermediates, and the 35/59
   module totals.

## Ledger candidates filed with this request

`exllamav3-imgsearch-empty-final-image-batch` r001 and `exllamav3-gemma-user-turn-closure` r002 (adds 250 as
an affected caller, introduction at 249 preserved): **accepted**.

## Ledger, with the next request

New record for `mixtral-sparse-calibration-coverage` at `9665ba99`; add `9665ba99` to the affected revisions
of `exllamav3-all-expert-fused-shape` (no new record).

## Next

251 at guidance 12, then replacement 164. One request at a time.
