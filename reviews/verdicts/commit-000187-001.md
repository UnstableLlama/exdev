# Verdict: commit-000187-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000187-001`
Packet: `.teacher/retrieval/000187-001`
Upstream: `ec839e16b83f4562ff5554b0bca5cfb10f3bc71c` "Mixtral/Qwen3 MoE: Skip redundant downcast after attn"
Request: `reviews/requests/commit-000187-001.md` (sha256 `95e814a824fbb8c6707806ab80f42e8ce48b7c385f305dad99a4aa40708fc008`)
Reviewed: 2026-11-15, working tree on top of `0ed73a1`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. The entry reads the title correctly: the change makes the output projection
produce float, it does not widen a value that was already rounded. It claims no speedup.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 45 of 45 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 186 strict-ancestor entries; 2,805 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 45 of 45 recorded tool calls identical, including the `run` call and eleven `hf_fetch` calls. |
| Unassisted | Standing instructions byte-identical to 186/001's. Guidance 8. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows at 2025-05-25T11:33:39Z; my query agrees. One closed row by terms (PR 35), selected, described as shared terminology only. |
| The change | `out_dtype = torch.float` is added to the `Attention(...)` call in both builders. Nothing else. Correct. |
| Where it goes | `Attention` passes `out_dtype` to `o_proj` only and applies it again through `to2` on return; Q, K and V are unaffected. Correct. |
| Residual | The embedding outputs float; `TransformerBlock.forward` normalises to half before attention and adds the attention result to the float residual in place; the MLP norm still asks for half. Correct. |
| Other models (mine) | Gemma 2, Gemma 3, GLM4 and Qwen3 already pass float for attention; this brings the two MoE builders in line. The entry does not say this; it is not needed for correctness. |
| References | Eleven pinned `config.json` files, four Mixtral and seven Qwen3 MoE, each declaring the matching architecture; the same ancestor-bound lists as the introducing entries. Configuration only, as the entry says. |
| Inherited finding | The all-experts buffer count is untouched by this commit. True, conditional as stated. |
| Execution | A half-rounding illustration with `struct`; labelled as illustration. |

## Not verified

- Any model run; the numerical effect on real outputs; speed.

## Must fix before canonical use

None for this entry.

## Follow-ups

1. Ledger: the all-experts record gains `ec839e16` as affected only if Astra tracks every revision; otherwise no
   change. Earlier owed items stand.

## Next

1. Record this approval with `--approve`.
2. Proceed to 188.
