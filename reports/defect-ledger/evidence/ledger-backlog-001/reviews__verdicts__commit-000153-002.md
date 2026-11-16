# Verdict: commit-000153-002

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000153-002`
Packet: `.teacher/retrieval/000153-002`
Upstream: `a905cffb1a3f66792ea000e9b589557aac3f9d14` "Merge pull request #37 from turboderp-org/dev"
Request: `reviews/requests/commit-000153-002.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only**, as a **reviewer-assisted** entry. Canonical and training remain false.
This attempt replaces the rejected 153/001, which stays as a rejected, unpublished run.

Every statement I checked is true, and the entry answers all six items of the coverage request with its own
evidence. It is the first entry in the walk to give the status of earlier findings at a release point: eight
distinct conditions recorded on dev, each re-read in the merged tree and each still present.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk. For reference:

- `draft.md`: `fc512922c15ad36f890a3d6996f7a6f8f23c219c52167b029bec520ff0ee369a`
- `raw-transcript.json`: `5b3cb7fd43fb1fce15f57e14b0014ff37268a464d2324d4eed403b2e8fa34094`
- `provenance.json`: `d258c7220bd7fb1429ed1218f4d2f5787bfe50e53ec8a27d11e7b8587c0df91d`
- request: `eb4887db5f06a25b894dd6664ab69f8af6cc5603b40b958305592b179ce16c95`

## Run checks

| Check | Result |
|---|---|
| Run integrity | 119 of 119 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 152 strict-ancestor entries; 2,291 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 119 of 119 recorded tool calls identical, including the `run` call. |
| Assistance, and only that | Compared with 153/001, the standing instructions gain one sentence (that the coverage field holds requests, not statements of fact) and the opening message gains the coverage request. Nothing else differs. The bound text hashes to `3a41898e…49ff`, the hash of `reviews/verdicts/commit-000153-002.coverage.md`. Provenance has `reviewer_assisted: true`. |
| No hindsight | The only packet file that mentions `reviews/verdicts` is the manifest, and only as the path of the coverage request. The transcript contains no text from the 153/001 verdict or its reviewer-only notes. |
| The merge | Tree `952ce3a6` for the commit and for its second parent. Correct. |
| Item 1, every path | All 44 paths are assigned to an ancestor entry, and the assignments are right: multi-GEMM interface and compile units to `b73d0739`, full grid to `edafdd1f`, routed module and conversion to `6fc153d7`, deferred load to `c6aa83f7`, registration to `a5caa423`, transpose to `538dcae3`, dtype dispatch to `74abd5e1`, generator to `809b0dab`/`9c31971b`, sampler to `a027848d` and `95cfa726`, penalty to `43383ebd`, BOS to `1e175478`, chat to `e0cfb2e9`, version to `70056fef`. |
| Item 2, ancestry | `rev-list` of the second parent excluding the first gives 17 commits; the entry lists the same 17. The merge base is the first parent itself, so the first parent, `beb7bcd9`, `ae04741f` and `c2b8516f` are on both sides, as the entry says. The two inbound merges (`10222646`, `f5127e87`) add nothing new to master. Correct. |
| Item 3, what master gains | Checked against the first-parent diff for the penalty kernel, both sampler files, HumanEval, and the routed module. Correct. |
| Penalty kernel | `f1 = (1.0f - f) + 1e-30; o = v * f1 + w * f`. At full weight the complement is no longer zero, so a masked `-inf` stays `-inf`. The entry's limit ("an endpoint safeguard, not general NaN sanitization") is right. |
| Sampler | `SS_TopK.__init__` is `isinstance(top_k, int) or top_k.is_integer()` then `int(top_k)`; `alt()` still returns a no-op below 1; `ComboSampler` takes the argmax branch for `temperature == 0.0 or top_k == 1`, after the two penalty steps. Correct. |
| Item 5, HumanEval | Six templates gain a literal marker (granite, llama, llama3, mistral, reka, deepseek); `add_bos` is now true only when the format argument equals `"raw"`. With no format argument the script uses the bare `{{problem}}` template and `add_bos` is false, exactly as the entry says. Both parents already parse `top_k` as an integer and omit `rep_p`. Correct. |
| Item 4, the eight retained conditions | The 17 entries record eight distinct findings (two are recorded twice under different names); the entry covers all eight and none is missing. I re-read each in the merged tree. All-expert: `topk` takes `num_experts` while the fused buffers have `num_experts_per_tok` slices, and `exl3_mgemm` checks `indices.size(1)` against `C.size(0)`. Leading dimensions: only `A.size(1)` against `C.size(1)` is checked. Selector: `(size_k && bits >= 3) > 8192`. Zero slices: `total_sms / num_sms` after the `/ 12` cap. Scratch: unchanged kernel file since `edafdd1f`. BF16 tail: `numel / 2` in both the block count and the launch. Clipboard: `if not snippet` after copying `''`. Annotation: `return bytearray(), None` under `tuple[np.ndarray, np.ndarray] | None`. All present; the classes and the stated reach are right. |
| Item 6, closed catalog | Nine rows, each discussed, each link labelled inference with its basis, none overstated. PR 35 and PR 36 are the two with a real connection and the entry says why. |
| Architecture outcome | `covered_merge`, as accepted in the 001 verdict. Unchanged. |
| Open catalog | Eleven rows. My routine query prints twelve because it counts issue 33, which was closed at this cutoff and reopened the next day (same quirk as at 129). |

## Not verified

- The values quoted from the seven model configurations. They come from replayed fetches; I did not fetch them
  again. The three unquantized repositories' headers were checked by me at 141.
- Any compilation or execution. The entry claims none beyond scalar transcriptions, and says so.
- The summaries of the nine closed discussions beyond the two that bear on the merge.

## Must fix before canonical use

- This entry is reviewer-assisted. It joins 39/005, 44/003, 45/002, 55/002 and 71/002 under whatever the
  assisted-entry policy for canonical use turns out to be.
- The recurring note: no tensor headers were read (the entry says so).

## Follow-ups

1. Record 153/002 as approved and reviewer-assisted, and 153/001 as rejected and superseded.
2. Ledger: the eight retained conditions are existing identities, not new records. Add this commit as the point
   where each reaches the first-parent line, when the owed ledger revision is done.
3. Two location fields name `70056fef` rather than the task commit. The trees are identical, so this is harmless;
   no change needed.

## Next

Proceed to 154.
