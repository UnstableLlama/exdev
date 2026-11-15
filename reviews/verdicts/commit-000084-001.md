# Verdict: commit-000084-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000084-001`
Packet: `.teacher/retrieval/000084-001`
Upstream: `b3bd8f614b003d81d8f5f6b56b20a207d901c523` "Fix input padding for linear layers"
Request: `reviews/requests/commit-000084-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry found the new defect in the changed function (padding both axes at once
copies into the wrong region) and kept the inherited slicing defect as one identity.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 13 of 13 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 39 of 39 implementation hashes; 1,137 blobs hash to their names; no evidence timestamp after the cutoff. |
| Ancestry | This is the first commit on a side branch: author `gk`, dated 2025-04-23 21:57 +09:00, parent `1f5a43fc` (walk position 77). The packet has exactly 77 strict-ancestor entries and nothing from positions 78 to 83, which are not its ancestors. Correct. |
| Replay | 13 of 13 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 83/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Cutoff is 12:57:16 UTC on 2025-04-23. GitHub: open then are 1, 4, 7, 10, 14, 15, 19. Pull request 20 was opened at 13:00:31, three minutes later, and is correctly absent. Matches the seven open rows. |
| Diff claims | `in_features_unpadded` keeps the argument; `in_features` is rounded up to `pad_to`. `pad_out` returns early only when neither axis is padded; for a matrix it copies rows if the output is padded, else columns if the input is padded. `forward` is untouched. Correct. |
| Propagation | The padded `in_features` is what `load_fp16`, `load_exl3`, `convert_exl3`, `capture_H` and `weights_numel` now use. `is_sliced` still compares the raw arguments. Correct. |
| Finding `simultaneous-axis-padding` | Correct. With both axes padded the first branch runs: destination `padded[:rows, :]` is rows by padded-columns, the source is rows by original-columns, and the `elif` is never reached. Introduced by this commit. |
| Finding `inherited-padding-before-slicing` | `load_fp16` still calls `pad_out` on the full weight before `LinearFP16` slices it. Unchanged; same defect earlier entries record. |

## Not verified

- The exact exception PyTorch raises for the mismatched assignment. Nobody ran it; the entry says so.
- Whether any model in the reference evidence has a linear layer whose input width is not a multiple of 128.

## Must fix before canonical use

Reviewer-only. None of this goes to a teacher.

1. The entry says compatible activation widths "remain a caller-side requirement" and stops. It does not look for a
   caller that pads activations. After this commit a layer whose input width is not a multiple of 128 holds a wider
   weight than the activations it is given, and `capture_H` allocates its matrix at the padded width. A canonical entry
   should say whether anything in the tree widens the activations, or say that nothing was found.
2. The same padded width is passed to `load_exl3`, so an already converted model with such a layer is asked for a
   different input width than it was converted with. Not mentioned.

## Next

1. Record this approval.
2. Continue the walk at commit 85.
