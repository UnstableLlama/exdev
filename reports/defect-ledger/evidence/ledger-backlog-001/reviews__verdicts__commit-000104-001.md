# Verdict: commit-000104-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000104-001`
Packet: `.teacher/retrieval/000104-001`
Upstream: `0b2dba5ac5aab77fb9d9aabdda72ceb5befa8b11` "Add image output during quantization (debug stuff)"
Request: `reviews/requests/commit-000104-001.md`
Reviewed: 2026-11-14, working tree on top of `d0a2d08`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry is clear that the images are of original and regularised weights before
quantisation, not of quantised results, and that each image is normalised on its own scale.

## Artifacts reviewed (sha256)

All hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 14 of 14 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 41 of 41 implementation hashes; exactly 103 strict-ancestor entries; 1,545 blobs hash to their names; no evidence timestamp after the cutoff. |
| Cutoff | Author date 18:04 and committer date 22:34 (+02:00) differ on this commit. The packet uses the committer date, as throughout the walk. |
| Replay | 14 of 14 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 103/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | GitHub: open at the cutoff are 1, 4, 7, 10, 14, 21, 22, 24, 25, 26, 27, 28, 29 (15 closed since 103). Matches the thirteen open rows. |
| Architecture trigger | Does not fire. |
| Diff claims | New `-img` / `--image_dump` flag stored into the job arguments; `images` directory created unconditionally; when set, each selected linear's weight is saved to `images/<key>.jpg` and a `.reg.jpg` path is passed through `Linear.convert_exl3` to `quantize_exl3`, which saves `weight_r` there; both functions gain `save_reg = None`. Correct. |
| `save_tensor_image` | Lazy imports of `matplotlib.cm` and `PIL.Image`; detached float32 CPU copy; clamp to mean ± 3 standard deviations; subtract the low bound and divide by the span plus 1e-8; `gnuplot2` colour map; RGB times 255 as `uint8`; save. Correct. |
| Finding | `documentation-dump-scope`: correct as far as it goes. The new line in `doc/convert.md` reads "-img / image_dump" and "Save all tensors"; the parser registers `--image_dump` and only the selected linear layers are dumped. |

## Not verified

- Where in `quantize_exl3` the regularised save sits relative to the later steps; the entry says after `regularize` and
  before `ldlq`, from a read that replays. I did not re-read that function.
- Any image output. Nobody produced one; the entry says so.

## Must fix before canonical use

1. `documentation-dump-scope` is classed `defect`. It is a documentation inaccuracy of the smallest kind; the ledger
   classification should say documentation.

## Next

1. Record this approval.
2. Continue the walk at commit 105.
