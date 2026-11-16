# Verdict: commit-000055-002

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000055-002`
Packet: `.teacher/retrieval/000055-002`
Upstream: `d6124d70584f83440fc8ad551f8f82bdf8479c64` "Split MLP layers > 54k inner dim"
Request: `reviews/requests/commit-000055-002.md`
Reviewed: 2026-11-13, working tree on top of `fd1dd86`

## Decision

**APPROVED for ancestor retrieval only, as a reviewer-assisted entry.** It supersedes attempt 001 for future retrieval. No dependent needs re-authoring.

This closes the four retroactive re-authorings. **The walk may resume at commit 62** under contract v7 / guidance 4.

Canonical and training remain false.

Attempt 001 was the thinnest approved entry in the walk. This one answers all seven coverage items, and every answer I checked is right. The four things my earlier verdict listed as missed (attention quantised once per slice, the changed standing of the findings from commits 47 and 53, the discarded reference error, the inert `source` keyword) are all in the entry now, each traced by the teacher from the source and the ancestor entries.

## Artifacts reviewed (sha256)

- draft.json: `690929c0cad38c113ee2b4116d7c048f7010d9f1ac2134f4a52470b0bd73626e`
- draft.md: `bc85ebe951d30ec1f55f42344c18dc99c9099c8d0bf6fbafa18a7b6999ef3e2f`
- raw-transcript.json: `2f85368b705228f672c8c481f7ae4756895ef0f266a0489029a82a57b8e55809`
- provenance.json: `3857d8c8bc5ee97220f2fab7ce41192ff102827f185b945bf756dac9799d095d`
- coverage.json: `93fa77cf7f9ca37b01dedde82e64916cff13345e2e1c854a2170ad884309bea6`
- packet manifest (on disk): `77674e657d8d709c2fefb08ca529102db6aaaac6fe3af8cbc6a2fc595b151201`
- coverage request: `a8d0540538b5c8b794a8a70bd13898ddb2d249f6026a08ca58893f35c859652b`

All match the request.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 54 of 54 ledger entries match the transcript; final message equals the annotation; Markdown equals the render; assessment is full review; 37 of 37 implementation hashes match; exactly 54 strict-ancestor entries; all 870 blobs hash to their names; no evidence timestamp after the cutoff; all six diff sections read. |
| Assistance is recorded | Provenance and the review record carry `reviewer_assisted` with the coverage request's path and hash. |
| Only the coverage request was added | Standing instructions are byte-identical to 45/002. The coverage field equals the file byte for byte. Opening-context keys are the same as 45/002. |
| No hindsight | No packet blob contains a ledger id, `reviewer_observation` or a ledger path. |
| Ancestor replacements | The packet's entries for commits 39, 44 and 45 are attempts 005, 003 and 002. |
| Item 1, ancestors | Four entries read in full: commits 47, 52, 53 and 54. The entry states for each recorded finding whether it is carried, changed or removed, and I agree with each: the padding-before-slicing problem is carried and gains its first caller; default CPU staging is removed for unsplit gated MLPs only; the CPU-bias mismatch no longer reaches the converter's forward pass because of the reload; source-local group detection and the native read wait are carried unchanged. |
| Item 2, the per-slice pass | Correct against the converter at the task. `Attention.load` drops the keyword and loads all four projections on every pass; `GatedMLP.load` loads only the named slice; the list of layers to quantise is every loaded `Linear` with a qmap, so attention is quantised again on each pass; `q_tensors.update` keeps earlier slice keys and overwrites the repeated ones; `module.unload` clears the block. |
| Item 3, reload placement | Correct. `load_exl3` fetches each tensor with the layer's device; the constructor asserts `scale` is None; quantisation emits `suh`, `svh` and `trellis`. |
| Item 4, slice loading | Correct against `linear.py` and `fp16.py` at the parent: full sizes make an unsplit layer unsliced; a sliced layer is staged whole on CPU, transposed, sliced by output columns or input rows, copied, and moved to the device; bias is sliced only on output selection; `pad_out` runs on the full source before slicing. |
| Item 5, reference error | Correct. It is still computed, against reference states kept from the last single-slice capture, and `N/A` is printed when there is more than one slice. |
| Item 6, configurations | Nine configurations read in full. I recomputed every width from the packet: the five non-DeciLM models are 4,864 to 14,336; 51B and Super peak at 28,672; both Ultra models have four multipliers that give 399,360, 425,984, 343,040 and 301,056. As the entry says. |
| Item 7, load keywords | Correct. `load_slice` is consumed by `GatedMLP`; `source` by nothing; `set_new_tensors` is the mechanism. |
| Findings | The two allocation findings from attempt 001 are kept at the same strength. The tail-padding finding is traced to the new caller with a worked trigger. The two inherited findings are labelled inherited and placed at the parent. All five are suspected, with limits stated. |
| Scalar checks | Re-ran both recorded commands: output identical. The Hessian sizes (594.14 GiB whole, 9.28 GiB per slice) follow from `capture_H` allocating a float32 square of the layer's input width; the entry calls them storage calculations, not measurements. |
| Tests | 209 passed earlier in this session on the same implementation hashes. |
| Dependents | Astra's scan finds no later run that read 55/001's prose. |

## Not verified

- Nothing was run against PyTorch. All five findings and the per-slice attention re-quantisation rest on source reading.
- Whether the 55,296 threshold is right for any hardware. The entry says the source gives no derivation.

## Must fix before canonical use

Reviewer-only.

1. Reviewer-assisted; selection of assisted entries is undecided.
2. The tail-padding trigger is a synthetic width (55,297). Every DeciLM width is a multiple of 256, so the last slice of each over-threshold layer in the reference models is aligned (I checked all four). A canonical entry should say the finding is not reached by the models this change serves.
3. Execute the per-slice pass once and confirm that attention is quantised N times, or keep it as source reading.

## Follow-ups

- Defect ledger: `inherited-native-read-wait` and `inherited-split-source-group` are further observations of existing defects (root and commit 52). `unaligned-tail-padding` is a further observation of commit 53's finding with a new caller. Only the two allocation findings originate here, and attempt 001 already reported them.
- Still open and unchanged: required architecture fixes 1 and 2 before position 100; the five older ledger files with an origin the validator rejects.

## Retroactive re-authorings: summary

| Commit | In force | Assisted | Attempts rejected on the way |
|---|---|---|---|
| 39 | 005 | yes | 003 (thin), 004 (incorrect claim) |
| 44 | 003 | yes | 002 (thin) |
| 45 | 002 | yes | none |
| 55 | 002 | yes | none |

All four entries now in force are reviewer-assisted. The two unassisted attempts made under the new evidence rules (39/004 and 44/002) read every configuration and no tensor header.

## Next

1. Record this approval; mark 55/001 superseded for future retrieval; clear the advancement pause.
2. Resume the walk at commit 62. Expect `REJECTED: thin` where an entry leaves out what a reader of that commit needs.
