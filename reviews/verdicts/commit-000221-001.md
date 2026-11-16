# Verdict: commit-000221-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000221-001`
Packet: `.teacher/retrieval/000221-001`
Upstream: `9bde46e775df21d54d78a0fbe78b1490bf311a5a` "Add convolution module (2D, 3D)"
Request: `reviews/requests/commit-000221-001.md` (sha256 `aa2658856325749ad986c207bda879949c2c6b5c3943e6afca4b25c23ad13341`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is true as stated.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 17 of 17 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 220 strict-ancestor entries; 3,114 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 17 of 17 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 220/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-01T23:59:20Z; my query agrees. No closed row qualifies. |
| The module | `Conv` stores the channel counts and `kernel_size`, refuses a `qmap`, and accepts kernels of two or three dimensions; `load` reads `key.weight` and an optional `key.bias` with `float2half`; `unload` clears them and keeps the cached element count; `get_tensors` writes them back under the same keys. Exported from `exllamav3.modules`. No caller in the tree. Correct. |
| 2D path | `F.conv2d` with `kernel_size` passed as the stride, then flatten and permute to [batch, positions, channels]. Correct. |
| 3D path | The input is viewed as patches of the kernel's size, `F.conv3d` with the same stride, and the result is reshaped to [1, patches, channels], so no separate batch dimension survives. Correct. |
| Worked examples | [2, 3, 2, 4] becomes [2, 8, 3]; 480 elements make five [3, 2, 4, 4] patches and [1, 5, 7] for seven output channels. Agreed by hand. |
| Finding: output dtype unused | The constructor stores `out_dtype` and `forward` accepts one, but neither is read; the result is returned as the convolution produced it. True, with the stated reach (the exposed interface only). |
| Execution | A standard-library layout check; labelled. |

## Not verified

- Any convolution, loading or GPU execution.

## Must fix before canonical use

None. The entry already states that the weights are loaded as half precision and the input is not cast, so a
float32 input is the caller's responsibility.

## Follow-ups

1. Ledger, with 222's request: the output-dtype finding as suspected, introduced at `9bde46e7`, reach limited
   to the exposed interface.

## Next

1. Record this approval with `--approve`.
2. Proceed to 222.
