# Verdict: commit-000255-004 (teacher Sol, guidance 12, reviewer-assisted; reviewed after recovery)

Reviewer: Fable. Date: 2026-11-17. Upstream `bcaa636f` "Add Transformers integration (still needs some work)".

## Decision

**Approved for ancestor retrieval only. 255/004 is the entry in force for commit 255.** Canonical and
training stay false. It is a reviewer-assisted entry (coverage request `commit-000255-004.coverage.md`,
questions only) and joins the list of assisted entries in force. 255/001, 002 and 003 are kept as history.

All three findings are **accepted as true as stated**, each correctly limited to source inspection:
`eager-undeclared-transformers`, `integration-not-packaged`, `decoder-multipliers-not-forwarded`. This time
the entry made the central check itself: it followed the root import chain into the adapter and compared it
with every requirements file and `setup.py`.

## Artifacts

Request hashes match. The seven run artifacts and the manifest are byte-identical to the recovery request:
nothing was edited after the checker fault. `check.py`: `gpt-6.1-sol` medium (server-confirmed), 34 evidence
calls all cited and none bad, final equals annotation, 254 ancestors, 3418 blobs, nothing after the cutoff.
The one implementation difference it reports is `teacher/validation_repair.py`, which is the accepted 002 to
003 change; the run recorded the 002 hash. No validation event; repair enabled and not used.

## Run checks (mine, against the tree at `bcaa636f`)

- `exllamav3/__init__.py` ends with `from . import integration`; `integration/__init__.py` imports
  `patch_transformers`; `integration/transformers.py` imports four Transformers symbols at module level, no
  guard. As stated.
- `transformers>=4.50.0` appears only in `requirements_eval.txt`; `requirements.txt`,
  `requirements_examples.txt` and `install_requires` do not have it. As stated.
- `setup.py` lists twelve packages and no `exllamav3.integration`. As stated.
- `Linear.load_exl3` loads optional `mcg`/`mul1` on CPU and passes them; conversion passes them from the
  quantizer outputs; the adapter has no such buffers or arguments. As stated.
- Adapter details: `name[21:]` rewrite for `model.language_model.`; meta tensors from header shape and
  `torch_dtype`; one-element FP16 meta `weight`; `transformers_fix = True`; CUDA check; FP16 default dtype;
  `config.tie_word_embeddings = False` in the before-loading hook. All as stated.

## Must fix before canonical use

- "conversion.update_config separately writes tied_word_embeddings=True": the write is conditional, it
  happens only when that key is already in the config (`conversion/quant_config.py` lines 11 to 12).

## Ledger

File the two new identities (undeclared eager import; package-list omission) with the next request. The
multiplier record stands from 255/002 if already filed; otherwise file it too.

## Next

Replacement 234 (the last re-authoring), then `run-ahead-migration-001`, then 256.
