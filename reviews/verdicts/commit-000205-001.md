# Verdict: commit-000205-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000205-001`
Packet: `.teacher/retrieval/000205-001`
Upstream: `34d2f1f5fa069b842b8791de8c8db499b3884579` "Add prequant_test script"
Request: `reviews/requests/commit-000205-001.md` (sha256 `58dce4afc10dd6ccf85e08585f33667df842fa2e27e013899b1b1163a7a691e5`)
Reviewed: 2026-11-16, working tree on top of `e9e83ff`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and both findings are true as stated. Three smaller consequences of the new
script are missing (below); none makes anything in the entry false.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 24 of 24 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 204 strict-ancestor entries; 2,955 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 24 of 24 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 204/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Fifteen open rows at 2025-05-30T17:42:49Z; my query agrees. Two closed rows by path alone. The link to issue 43 is called an inference. |
| `regularize` | `H_diag` and `pb` may be `None`; without a diagonal, output scaling is on unless forced; `skip_g_scale` (default false) replaces the scale search with 1.0. The existing caller passes neither change. Correct. |
| The script | 2,048-token windows at stride 512, optional BOS; per module: deferred load, weight inspection, forward, state inspection, unload. Defaults ten rows, device 0, 160 bins, no skipped tokens. Correct. |
| Weight inspection | Extrema, population standard deviation, inf/NaN counts, six-sigma count measured from zero; the layer is regularized on a float32 copy with random signs and compared; counts above 4 and 8. Correct. The stored weight is half precision, so `w.float()` copies and the module's own weight is not altered (my check). |
| State histograms | Half the bins for ±3σ, a quarter for each tail, exclusive mode; each chart scaled to its own maximum. Correct. |
| Perplexity | Logits cut to the actual vocabulary, shifted by one, mean log-probability exponentiated; overlapping windows scored independently. Correct. |
| Arithmetic | 2,048 − 512 = 1,536 overlap; 10 × 2,047 = 20,470 predictions; 160 bins split 40/80/40. Agreed. |
| Finding: verbose with skipped scale | The verbose block reads `mse_scale`, which the skip branch never assigns. No caller in the tree combines the two. True, with the stated reach. |
| Finding: skipped-token strides | `state[:, skip:, :].to(device)` returns the view unchanged when the state is already there; with more than one row it is not contiguous; `histogram` walks `numel` elements from `data_ptr()`. The 2 × 3 × 2 example gives 52 against 44; I agree by hand. True; reachable from `-skip` with the default ten rows. |
| Execution | Standard-library arithmetic and list indexing; labelled as a model. |

## Not verified

- Any Torch, CUDA or model execution; that `tensor.std()` on a large half-precision state stays finite.

## Must fix before canonical use

1. The stride finding also applies to `count_inf_nan` in `stats`, which is called on the same sliced state and
   likewise walks `numel` elements from `data_ptr()`. The entry names only the histogram.
2. The script imports `termplotlib`, which nothing in it uses and no requirements file lists, so the script
   fails at import where that package is absent. The entry does not mention it.
3. `--histogram_bins` below 4 makes the tail histograms zero-length (below 2, the weight ones), which is the
   zero-bin case recorded at 198, now reachable from a command-line argument. Also minor: values between 3σ
   and 3σ + 0.001 fall in no histogram, and the percentages are of the counted total.

## Follow-ups

1. Ledger: both findings may be filed as suspected, introduced at `34d2f1f5`; the 198 zero-bin record gains
   this script as a caller path. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 206.
