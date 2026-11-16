# Verdict: commit-000183-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000183-001`
Packet: `.teacher/retrieval/000183-001`
Upstream: `6693b5010504364efbfd099fdc839aab971e7708` "Add GPTJ to reference RoPE implementation"
Request: `reviews/requests/commit-000183-001.md` (sha256 `8ec239c3ccd917989b1feb8bff34f3053fbb8dfc5726570a99294e705d4a167e`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and all three findings are true as stated: one introduced by this commit, two
inherited and labelled so.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 16 of 16 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 182 strict-ancestor entries; 2,764 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 16 of 16 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 182/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-25T00:13:11Z; my query agrees. One closed row by path alone, selected; all three discussions read are described as file overlap only. |
| The change | The single-tensor and two-tensor helpers now exist per style; `apply_torch` picks the NEOX helper for NEOX and the GPTJ helper otherwise; positions are made float before the outer product; the cached sine and cosine stay float; Q and K are made float before rotation and half after. Correct. |
| Pairing | `compute_sincos` already concatenated for NEOX and interleaved for GPTJ; before this commit `apply_torch` always used split-half rotation. Correct. |
| Callers | `apply_torch` is called only from `tests/test_rope.py`; the cache is used only by `apply_torch`; the native `apply` takes `inv_freq` directly. Correct. |
| Finding: optional K | `k = k.float()` and `k = k.half()` are unconditional, while the lines around them still test `k is not None`. With `k` absent the first raises. Four of the twelve test shapes pass no K. True; introduced here. |
| Finding: test compares inputs | Both `apply_torch` and `apply` default to `in_place = False` and the test ignores what they return, so its assertions compare two identically seeded inputs. The style list contains NEOX only. True; inherited. |
| Finding: partial width | `inv_freq` has `head_dim * partial_rotary_factor / 2` entries, so the duplicated coefficients are narrower than a full-width head and neither helper splits off the unrotated part. True; inherited. |
| Execution | Four-channel double-precision transcription of the pairing; labelled as algebra only. |

## Not verified

- Any Torch or CUDA execution; agreement of the reference with the native kernel.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: identities for the three findings may be filed as suspected, source-only (optional-K introduced at
   `6693b501`; the other two with their recorded introductions). Still owed: optional-output, the three 174
   identities, 181's remaining-unequal identity.

## Next

1. Record this approval with `--approve`.
2. Proceed to 184.
