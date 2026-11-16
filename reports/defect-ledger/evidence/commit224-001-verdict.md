# Verdict: commit-000224-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000224-001`
Packet: `.teacher/retrieval/000224-001`
Upstream: `074019737caac1c6e6a457e3bed7e4a30e0a5877` "VLM util functions"
Request: `reviews/requests/commit-000224-001.md` (sha256 `3f9e9ae89381efee4b929af5912d04d9c5af49dedfe070f11e6610650599dae2`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. No findings are filed; one packaging consequence is missing (below). Both
ledger items filed with this request are accepted.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 12 of 12 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 223 strict-ancestor entries; 3,141 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 12 of 12 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 223/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-02T00:02:38Z; my query agrees. Four closed rows, three by path alone, none cut. |
| `convert_to_rgb` | Returns an RGB image as is; otherwise converts to RGBA, pastes it over a white canvas using its own alpha, and converts to RGB. Correct. |
| `normalize_image` | Requires three means and three deviations; casts a non-floating image to float32 and keeps a floating one; returns `(image - mean) / std` with no rescaling and no axis handling. The docstring's "mean(image)" is not what the code does. Correct. |
| Requirements | `pillow` is appended to `requirements.txt`. Correct. |
| Callers | Neither helper is called anywhere; the module is not imported by the package's `__init__` files. Correct. |
| Worked example | (-1, 255, 509) without rescaling; (-1, 0.00392, 1) after dividing by 255. Agreed by hand. |
| Execution | Scalar arithmetic only; labelled. |

## Reviewer finding (not in the entry)

**Pillow is declared in `requirements.txt` but not in `setup.py`.** `install_requires` at this commit lists
torch, flash_attn, tokenizers, numpy, rich, typing_extensions, ninja and safetensors. The new module imports
`PIL` at the top, so an installation made from the package metadata (a wheel or `pip install .`) does not bring
Pillow, and importing `exllamav3.util.vision` then fails. The entry read the earlier dependency-alignment entry,
which records that the two lists had been made to match and that Pillow had been removed from the metadata, but
does not say that this commit makes them differ again. Source reading only; the failure appears only when the
new module is imported.

## Not verified

- Any Pillow or NumPy execution; any installation.

## Must fix before canonical use

1. State the packaging mismatch above.

## Ledger items filed with this request

- `exllamav3-mlp-ignored-activation--r002`: **accepted.** Supersedes r001; fix at `95c41ce0`.
- `exllamav3-mlp-unsupported-activation--r001`: **accepted.** Suspected, introduced at `95c41ce0`, no fix.

## Follow-ups

1. Ledger, with 225's request: a reviewer-observation record for the Pillow declaration mismatch, introduced at
   `07401973`, suspected, source-only, reach limited to installs from package metadata that import the vision
   helpers. Not teacher input.

## Next

1. Record this approval with `--approve`.
2. Proceed to 225.
