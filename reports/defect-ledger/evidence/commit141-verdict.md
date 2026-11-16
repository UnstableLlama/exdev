# Verdict: commit-000141-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000141-001`
Packet: `.teacher/retrieval/000141-001`
Upstream: `a5caa423bbd9d8a61266a88fb237c18fb77ec0b8` "Add Qwen3MoeForCausalLM"
Request: `reviews/requests/commit-000141-001.md`
Reviewed: 2026-11-14, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the inherited finding is correct. The entry reads all seven configurations
and reports them accurately, explains what the builder reuses, and is exact about the finding's reach: the
all-expert flag is used in the capture pass, where the module is not yet quantized, so ordinary conversion does not
hit the fused-path failure.

As at 98, 103 and 110, the teacher read no tensor headers, and says so. I read them (below). Nothing is hidden this
time: the three unquantized repositories match the builder exactly.

## Artifacts reviewed (sha256)

All twenty hashes in the request match the files on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 37 of 37 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 42 of 42 implementation hashes; exactly 140 strict-ancestor entries; 2,196 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 37 of 37 recorded tool calls identical, including both `run` calls. |
| Unassisted | Standing instructions byte-identical to 140/001's. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Thirteen open rows (issue 33 was closed at this cutoff, 2025-05-11T13:35:38Z). No qualifying closed row of 23 candidates. |
| Architecture trigger | Fires on the derived identity `Qwen3MoeForCausalLM` from `models/qwen3_moe.py`. No unresolved file, no `curator_attestation`. |
| Reference list | Checked in `header-budget-implementation-001`: 469 Qwen repositories listed, seven declaring this class before the cutoff, all seven pinned to their latest revision at or before the cutoff. The packet's bundle is that one (239 items). |
| Registry | Import and one list entry in `architectures.py`. Correct. |
| Builder against dense Qwen3 | `qwen3_moe.py` differs from `qwen3.py` only in the class names, the three expert settings and the `norm_topk_prob` assertion in place of `intermediate_size`, `BlockSparseMLP` with its keys in place of `GatedMLP`, and the final `calibration_all_experts = True`. Attention, norms, head and `prepare_inputs` are identical. Correct. |
| Configuration | `head_dim` read with fallback `hidden_size // num_attention_heads`; KV heads default to query heads; `hidden_act` and `norm_topk_prob` asserted with omission allowed; three required expert settings; NEOX RoPE through the default helper. Correct. |
| MLP wiring | Router key `mlp.gate`; expert keys `experts.{expert_idx}.gate_proj`, `up_proj`, `down_proj`; `qmap = "block.mlp"`; `interm_dtype = torch.half`; `out_dtype = torch.float`. Correct. |
| Dtypes through the block | `TransformerBlock.forward` asks the MLP norm for half output, so the module receives half; the ordinary path converts its sum to float at the end and the fused path writes float directly. Consistent. |
| Calibration | The flag set here is the one `convert_model.py` reads for the capture pass, with the reference state recomputed without it. Correct. |
| The seven configurations | All seven: `Qwen3MoeForCausalLM`, 128 experts, 8 per token, `silu`, `norm_topk_prob` true, untied embeddings, head dimension 128, 4 KV heads. 235B (three repositories): hidden 4096, expert intermediate 1536, 94 layers, 64 heads. 30B (four): hidden 2048, expert intermediate 768, 48 layers, 32 heads; maximum positions 32768 for Base and 40960 for the others. FP8 and GPTQ carry a `quantization_config`. Equal to the entry. |
| Execution | Recorded output: query widths 4096 and 8192, KV width 512, fallback head dimension 64, 8 of 128 is 0.0625, and 128 against 8 for the shape check. Matches the prose. |
| Finding `inherited-all-expert-fused-shape` | Correct, and correctly tied to the 139 identity. With these configurations the mismatch is 128 against 8. Reach as the entry states. |

## Headers against the builder (mine)

I built the tensor list the constructor declares (embedding, final norm, head, and per layer two norms, four
attention projections, two Q/K norms, the router and three projections per expert) from each configuration and
compared it with every header in the bundle.

| Repository | Tensors | Missing | Extra | Shape mismatches | Dtypes |
|---|---|---|---|---|---|
| Qwen3-30B-A3B | 18,867 | 0 | 0 | 0 | BF16 |
| Qwen3-30B-A3B-Base | 18,867 | 0 | 0 | 0 | BF16 |
| Qwen3-235B-A22B | 36,945 | 0 | 0 | 0 | BF16 |
| Qwen3-30B-A3B-FP8 | 37,491 | 0 | 18,624 | 0 | F32 and F8_E4M3 |
| Qwen3-235B-A22B-FP8 | 73,417 | 0 | 36,472 | 0 | F32 and F8_E4M3 |
| Qwen3-30B-A3B-GPTQ-Int4 | 74,739 | 18,624 | 74,496 | 0 | F16 and I32 |
| Qwen3-235B-A22B-GPTQ-Int4 | 146,361 | 36,472 | 145,888 | 0 | F16 and I32 |

The three unquantized repositories match name for name and shape for shape, with nothing left over. The router is
`[128, hidden]` with no bias, no projection has a bias, and all sizes are multiples of 128.

## Reviewer-only notes (never to a teacher)

- **FP8 and GPTQ cannot load.** The FP8 repositories store every attention and expert projection as `F8_E4M3`
  with a block-wise `weight_scale_inv` beside it (the extras). The GPTQ repositories have no `.weight` for those
  projections at all; they store `qweight`, `qzeros`, `scales` and `g_idx`. Same situation as the dense Qwen3 FP8
  repositories at 110. The entry's limit ("does not establish FP8 or GPTQ checkpoint compatibility") is the honest
  statement of this without the headers.
- **My two 139 concerns are met by this builder.** It passes `interm_dtype = torch.half`, so the fused path's
  activation reads what was written, and it sets `calibration_all_experts = True`, so the shared input map and
  every down map get data. The 139 dtype record stays as a property of the module's default.
- **Shapes at these sizes.** For 2048/768 and 4096/1536 the automatic kernel selection never returns a tile count
  of zero and the 256-wide shape always divides, so neither the zero-cap record nor my divisibility record is
  reached by these models. Arithmetic only.
- With all experts active the capture pass runs each of the 128 experts on every calibration token, and each
  layer holds 128 down-projection Hessians. That is cost, not a defect.

## Not verified

- Any load, conversion or generation.
- `Config.from_directory`'s rejection of an unregistered architecture, beyond what I verified for the same
  mechanism at 110.

## Must fix before canonical use

1. As for 98, 103 and 110: a canonical entry for an architecture commit should state what the headers show,
   including which published variants cannot load.

## Follow-ups

1. Ledger: add `a5caa423` to the affected revisions of `exllamav3-all-expert-fused-shape`, with the concrete
   128 against 8; no new record.
2. The remaining older ledger revisions are still owed.

## Next

1. Record this approval.
2. Continue the walk at commit 142.
