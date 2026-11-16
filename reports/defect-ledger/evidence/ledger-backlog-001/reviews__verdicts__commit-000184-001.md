# Verdict: commit-000184-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000184-001`
Packet: `.teacher/retrieval/000184-001`
Upstream: `8357593c39b444f9e7e46bd90d385b6dcd7e1c62` "BlockSparseMLP: Move functionality to extension, reduce CPU overhead"
Request: `reviews/requests/commit-000184-001.md` (sha256 `516092b92d998931df4fbccbeee2578c911715a4865c2456ea247f7f040b8e78`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true, and all three findings are true as stated. The entry notes that the kernel
reduction is what makes taking the first output plane correct, and does not claim a measured speedup.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 23 of 23 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 183 strict-ancestor entries; 2,773 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 23 of 23 recorded tool calls identical, including the `run` call. |
| Unassisted | Standing instructions byte-identical to 183/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-25T00:20:06Z; my query agrees. Three closed rows by terms, all selected; described as shared context only. |
| Native routing | `blocksparse_mlp_routing` multiplies the input by the gate weight, takes the top values and applies softmax to them; for one token without the all-experts flag it writes into three buffers allocated at load, with unsorted top-k; otherwise it allocates and uses `num_experts` or `num_experts_per_tok`. Plain ATen calls, no new kernel. Correct. |
| Load-time buffers | Routing and expert buffers are allocated in `load` for one token and `num_experts_per_tok` planes, whether or not the fused path will be used, and cleared in `unload`. Correct. |
| Kernel reduction | After the last grid synchronisation, blocks with `blockIdx.z == 0` sum the planes element by element into plane zero, only when weights are supplied; float accumulation for a float output, sequential half additions otherwise. Correct. |
| Other callers | The gate and up calls and attention's K/V call pass no weights and so do not get the reduction; only the down call does. Correct. |
| Forward | `final_hidden_states = cfg.out_d[:1, ...]` replaces `out_d.sum(dim = 0)`. Correct. |
| Finding: all-experts count | One token with the flag set takes the allocating branch and returns `num_experts` indices; the persistent buffers have `num_experts_per_tok` planes; `exl3_mgemm` checks the index count against the output's first dimension. True; inherited, conditional as stated. |
| Finding: output dtype | `out_d` is allocated from `self.out_dtype` alone; the per-call `out_dtype` no longer has an effect on the fused path. True. Both decoder call sites pass none. |
| Finding: aliasing | The returned tensor is a view of `cfg.out_d`, which the next fused call overwrites. True. Both decoder call sites use the result at once. |
| Execution | Half-precision rounding example and index enumeration; labelled as illustration. |

## Not verified

- Any build, GPU execution or timing; equality of the kernel sum with the previous `torch.sum` in half precision.

## Must fix before canonical use

1. The entry leaves "optional bias" as unestablished in general. The source is specific: the previous route went
   through `LinearFP16.forward`, which adds the bias when there is one and uses `hgemm` when the input dtype
   differs from the output dtype; the native route does neither. The routing gate is built with `qmap = None`,
   `out_dtype = torch.half` and `pad_to = 1`, so it is never quantised and is always a `LinearFP16`.
2. `gate_tensor` is captured once in `load`; a later replacement of the gate's weight would not be seen. Nothing
   in the tree replaces it (the conversion swaps touch only linears that are being quantised).

## Follow-ups

1. Ledger: identities for the output-dtype and aliasing findings may be filed as suspected behaviour changes,
   source-only; the all-experts record gains `8357593c` as affected. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 185.
