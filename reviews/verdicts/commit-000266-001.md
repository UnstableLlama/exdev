# Verdict: commit-000266-001 (teacher Sol, guidance 12, unassisted; ran ahead of 265; first validation-repaired run)

Reviewer: Fable. Date: 2026-11-17 (07:20 UTC). Upstream `6bd852cc` "Linear: Remove ambiguity between sliced and padded FP16 tensors".
Run: `.teacher/runs/commit-000266-001`. Packet: `.teacher/retrieval/000266-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. All four findings are accepted
as true as stated, each from source: `reversed-slice-comparisons` and `none-full-dimensions` are new;
`inherited-deferred-bf16-tail` and `inherited-native-read-wait` are observations of existing identities.
The entry made the commit's central check itself: it tested the three changed comparisons against both
constructor callers. It stands without a rerun: 265 changes one assertion in conversion.

## Validation repair (first live use)

Checked by me from the transcript. The first final annotation (index 74) cited one call id that does not
exist in the transcript; the validator's message "Unknown or unsuccessful evidence call" went back verbatim
as the only added input (index 76); the teacher made one more read-only call and returned the final
annotation (index 79). The refused annotation is kept in the transcript. Comparing the two: same four
findings (one renamed), same 38 text fields, prose tightened from about 9,200 to 7,500 characters; I found
no statement of substance in the refused version that is absent from the final one. Provenance records the
refused hash, the feedback hash and the selected index. The mechanism did what was decided and no more.

## Artifacts

Request hashes match. `check.py` clean apart from the expected 264 of 265 ancestor entries:
`gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes equal to the accepted set, 37 evidence
calls all cited and none bad, final equals annotation, 3503 blobs, nothing after the cutoff. Orchestration
hashes equal the accepted files; sparse, 264 of 265, as disclosed.

## Run checks (mine, tree at `6bd852cc`)

- `LinearFP16.__init__`: the crop conditions are now `shape == full and shape < local`. With a full
  matrix and a smaller local size the second part is false, so no crop happens. `GatedMLP` builds exactly
  that case for split layers (`out_features = b - a`, `full_out_features = intermediate_size`, loaded from
  the unsliced key on CPU without padding). As stated.
- The fused `frange` branch of `Linear.load_fp16` constructs `LinearFP16` with no full dimensions, so
  `in_features < full_in_features` compares an integer with `None`. As stated.
- `Linear.is_sliced` now means a reduction only; it selects CPU staging, no loader padding and no deferral.
  As stated.

## Reviewer knowledge (never to a teacher)

At the tip of history (`bd1f5191`) the three comparisons in `LinearFP16.__init__` are unchanged, and a
caller there passes `full_in_features = in_features`; so the None case was dealt with on the caller side
later, and the reversed crop for split layers appears never to have been changed in this file.

## Ledger

File with the next request: two new identities (reversed slice comparisons; None full dimensions on the
fused path) and two observations on the existing odd-tail and native read-wait identities.
