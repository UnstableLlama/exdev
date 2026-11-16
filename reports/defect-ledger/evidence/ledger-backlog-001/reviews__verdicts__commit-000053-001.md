# Verdict: commit-000053-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000053-001`
Packet: `.teacher/retrieval/000053-001`
Upstream: `8e128ed9040b0fff1107798a1d5e57c8376bb4d5` "Option to slice FP16 linear layer while loading"
Request: `reviews/requests/commit-000053-001.md`
Reviewed: 2026-11-13, working tree on top of `dfebc8a`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

The walk may continue from commit 54.

## Artifacts reviewed (sha256)

If any differ, this verdict does not apply.

- draft.json: `a4466e24a63ee3e5a76265c6d84ed99e2f327b46c7254622626ba48c397476d5`
- draft.md: `d1bfe96f0a0e7cf43d85d2d2487d3cff2a21439854d92111bc635f49df748d10`
- raw-transcript.json: `3aed00146250e84b97580cf6dec3d989eec0983bf8063e17e43cfa1c39801cc7`
- provenance.json: `e913fa548e5fa282044d1f836e5594f46a06e09b70f2ed8c994b735f3c93c002`
- coverage.json: `339b6253324b702b2f491d800b6320d04f2f10c4f0bb6fcd264afc03f716215e`
- packet manifest (on disk): `c7802c315fd71144f455bcdc608c8354e210da2104ba06c3c01c33aa05c4cda1`
- unreferenced bundle: `f9d2e759830e8804554f3beff33c3376c7865b030c6ad09981918fb56490bba8`
- validation report: `2929aac1faada79b3415ac15fde3645acb6882c5082c8d6314bb28e0d37745a2`

All eight match the request.

## Run checks

| Check | Result |
|---|---|
| Evidence hashes | 16 of 16 ledger entries match the transcript tool results, with matching tool and arguments. Every call made is in the ledger. |
| Final message, Markdown, policy | Final message equals the annotation; `draft.md` equals the render; assessment passes with full review (non-mechanical paths, three findings, an execution claim). |
| Provenance | Manifest matches provenance. 35 of 35 implementation hashes match the working tree. Standing instructions are byte-identical to the commit 44 run. |
| Task sections | Six changed files; all six diff sections read in full. |
| Packet ancestry (on disk) | Exactly 52 entries, equal to the 52 strict ancestors. Nothing outside the ancestors and the task. All 584 blobs hash to their names. No blob contains the ledger id or the word "hindsight". |
| Opening context | Message, author name, parent `70e79cc8` (commit 52) and task SHA match Git. Cutoff `2025-04-13T15:36:20+02:00` is the committer date (the author date is 67 minutes earlier). |
| Catalog | Four rows: 1, 4, 7, 10. Issue 14 was opened at 21:50 UTC, eight hours after this cutoff. Correct. No snapshot timestamp is later than the cutoff. Issue 7 read. |
| Source claims | Verified against the diff and parent files. `Linear` gains four optional constructor arguments and stores them. In the ordinary weight branch the weight is fetched to CPU when `is_sliced`, padded as before, and passed with the four values to `LinearFP16`, after which `swap_device` is set and `unswap_cpu` moves weight and bias to the device and clears the field. `LinearFP16` keeps the transpose as a view, slices the input axis when the stored size equals the full size and differs from the requested one, slices the output axis and the bias likewise, and then copies into a fresh tensor when sizes differ from the full sizes, or calls `contiguous()` otherwise. The fused-weight branch and the EXL3 loader are untouched. `Module.load` forwards keyword arguments; `Attention.load` accepts them but calls `super().load(device)` without them. `Linear.get_tensors` returns an empty dictionary when `self.device` is unset. |
| Scalar check | Re-ran the recorded command: output identical. Index mapping after transposition, the default predicate, and the padded-width arithmetic. |
| Ancestor attribution | The teacher read commit 52's entry, describes it accurately and links it. |
| Issue note | Issue 7's title is quoted exactly and the note says no connection is established. |
| Tests | Full suite: 197 passed with pinned Codex 0.167.0 first on PATH (re-run by me). |
| Commit 52 records | `reports/commit-000052-review-001.json` binds my verdict by path and the correct SHA-256 and keeps canonical and training false. Both canonical items are recorded. |

## The three findings

**default-cpu-staging (suspected, behaviour change).** Holds, and it is the most consequential observation in the entry. `is_sliced` is computed as `in_features != full_in_features or out_features != full_out_features`, and both full sizes default to None, so it is true for every `Linear` that does not pass them. I searched the task tree: no construction site passes them. So every ordinary FP16 linear now reads its weight to CPU, copies it into a fresh tensor and then moves it to the device, where before it was read straight to the device. The same comparison in `LinearFP16` selects the explicit copy. An "option" that is on by default for everyone is exactly what a reader needs to know.

**padding-before-slicing (suspected, defect).** Holds by source. `pad_out` runs on the full tensor before `LinearFP16` slices. When the requested output width is not a multiple of 128, `pad_out` allocates `(padded_out, in_features)` and assigns the full-size tensor into it, which cannot fit. When the width is already aligned, `pad_out` returns early and the problem does not arise; the draft's example (130 outputs from 512) is a correct trigger. The draft notes that no existing construction requests such a slice.

**inherited-native-read-wait (suspected, defect).** Same observation as in commit 52, re-stated under the inherited-defect rule because commit 52's entry, which the teacher read, records it. The added nuance is right: CPU reads write directly into the tensor and do not use the copy worker, so CPU-staged weights avoid it, while biases and other reads to the GPU still reach it.

## Not verified here

- Nothing was executed against PyTorch; the assignment error in the padding finding was not reproduced.
- That each of the other 50 packet entries is the currently approved attempt for its commit.

## Must fix before any canonical use (not blocking ancestor retrieval)

1. The reach of the default-staging finding is understated. The draft names attention and MLP construction sites; the output heads built in the model files (`llama.py`, `phi3.py`, `gemma.py`, `decilm.py`) also omit the new arguments and take the same route. State it as "every `Linear` constructed in the tree".
2. The padding finding should also cover input slicing: with an unaligned output width, the padded destination has `in_features` columns while the source has the full input width, so the assignment fails on that axis too.
3. Both new findings should be executed against the task tree before canonical use, or kept explicitly as suspected.

## Follow-ups

1. **The inherited finding will keep recurring.** It now appears in the root chapter, commit 52 and commit 53, and the rule will repeat it in every later entry that reads one of those and touches the loader's data flow. That is the rule working, but for the ledger it must stay one defect with several observations. Worth deciding how the ledger extraction de-duplicates before the count grows.
2. Carried and still open: required fixes 1 and 2 before position 100; the reference carry-forward and "read every attached configuration" questions for the user; the five older ledger files with an origin the validator rejects; wire tests depend on the default `codex` on PATH; ancestor search indexing; bare file names over-match in path hints; earlier canonical items.

## Next

Record this approval locally with the original packet and continue the walk from commit 54.
