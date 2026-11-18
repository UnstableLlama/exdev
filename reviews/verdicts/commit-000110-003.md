# Verdict: commit-000110-003 (replacement of 110/001; teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-16. Upstream `1db3dce0` "Add Qwen3 architecture (Qwen3ForCausalLM)".

## Decision

**Approved for ancestor retrieval only. 110/003 replaces 110/001 as the entry in force for commit 110** for
packets prepared from now on; 110/001 and the declined 110/002 are kept as history. Canonical and training
stay false.

Both findings are **accepted as true as stated**: `inherited-architecture-mismatch-diagnostic` (existing
identity; undefined `expect_arch` in the base constructor's assertion message, not reached through
`Config.from_directory`) and `fp8-checkpoint-format-boundary` (new; `convert_dtype` knows I32, I16, F16, BF16
and F32 only, the FP8 projections are `F8_E4M3`, and their `weight_scale_inv` tensors are never read). The
entry is right to class the second as a compatibility limit and not a promise the commit broke. 110/001 had
no findings, so none was lost.

The entry made the commit's central check itself, which is why this is an approval under the stricter
standard: it compared the name the builder probes (`lm_head`) with the name the headers store
(`lm_head.weight`), concluded that tying is a loading fallback whose alternate key is armed even when a head
is stored, and confirmed from `Linear.load` that the stored head is still tried first. That restores the
mechanism 110/002 dropped and corrects the impression 110/001 left (that the alternate key is armed only for
checkpoints without a head). This is the gap guidance 12 was adopted to close; first entry at version 12.

## Artifacts

Request hashes match (22 of 22). `check.py` clean: manifest and provenance agree, server-confirmed runtime
`gpt-6.1-sol` medium, 44 implementation hashes, 70 evidence calls all cited and none bad, final equals
annotation, 109 ancestors, 1670 blobs, nothing after the original cutoff (2025-04-29T20:37:14Z). The manifest
differs from 110/001's in `guidance_version` only (5 to 12). The system text carries the version 12 sentence.

## Run checks (mine, against the packet and the upstream tree)

- All 17 configurations: architecture string, D=128, K=8, SiLU, epsilon 1e-6, vocabulary 151936, theta
  1000000, null `rope_scaling`, sliding window off; H, I, Q, layer counts and tying per size as stated; Base
  variants 32768 positions and EOS 151643, the rest 40960 and 151645. All correct.
- Every layer of every one of the 17 checkpoints (all shards merged): the seven projection shapes, both block
  norms and the Q/K norm weights `[128]` match the entry's formulas. No mismatch, nothing missing, no biases.
- Query-to-KV ratios 2, 2, 4, 4, 5, 8 and fallback head widths 64 / 80 / 80: correct.
- Source: `has_tensor` is an exact-name lookup; `Linear.load` tries the primary key before the alternate;
  K-only norm silently dropped in `Attention.__init__`; norms applied in all three attention paths before
  RoPE; native RMSNorm checks half weights and width divisible by four; seven existing `prepare_inputs`
  hooks in the parent; `q_norm` appears nowhere in the parent outside `attn.py`; `science/kv_quant_exp.py`
  is the only other consumer. All as stated.

## Not verified by the entry (stays with the reviewer, as agreed; reviewer-only facts)

The entry states head presence for ordinary 0.6B only and says so. Across the checkpoints: `Qwen3-0.6B-Base`,
`Qwen3-1.7B-Base`, `Qwen3-4B` and `Qwen3-4B-Base` store no `lm_head.weight` and load through the fallback;
the other thirteen store one, including the tied 0.6B, 1.7B and all FP8 variants. Consistent with the entry.

## Must fix before canonical use (peripheral; not grounds to reject)

1. 110/001 said the builder keeps the calibration mappings `block.attn`, `block.mlp` and `block`; 110/003
   does not mention them.
2. 110/001 spelled out the `prepare_for_attn` mode selection (uncached FlashAttention by default; uncached
   paths reject a cache); 110/003 keeps only the cached-parameter requirement.
3. "This can enable the alternate embedding key even when the head exists" understates it: for any tied
   checkpoint with ordinary tensor names the probe never matches, so the alternate key is always armed.

## Next

Proceed with 249 at guidance 12, then replacement 141, one request at a time. File the accepted
`fp8-checkpoint-format-boundary` record with the next request, per the standing rule.
