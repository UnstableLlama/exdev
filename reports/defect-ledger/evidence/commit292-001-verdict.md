# Verdict: commit-000292-001 (teacher Sol, guidance 12, unassisted; architecture commit)

Reviewer: Fable. Date: 2026-11-17 (14:03 UTC). Upstream `47d83f56` "Add Ernie 4.5 model (text only)".
Run: `.teacher/runs/commit-000292-001`. Packet: `.teacher/retrieval/000292-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. All four findings are accepted
as true as stated: `ernie-chat-template-mismatch` is new (external compatibility);
`ernie-custom-bias-export` is the 290 identity, now reached by a built-in model that sets the custom key;
the all-expert count and the fused result contract are observations of existing identities.

The entry made the central checks of an architecture commit itself, and went further than any earlier
architecture entry: it read all fifteen configurations; read headers from seven checkpoints including the
Paddle and quantized ones; and concluded from them, unprompted, that the eight Paddle repositories carry the
registered architecture strings but tensor names, fused projections, orientations and quantized forms the
new builders do not request. It also noticed that the Ernie builder leaves the router at the standard
default, so the correction-bias tensor it loads under a custom key is never used.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes
equal to the accepted set, 86 evidence calls all cited and none bad, final equals annotation, 291 of 291
ancestors, 4258 blobs, nothing after the cutoff. Orchestration hashes equal the accepted files; complete
packet; ran ahead of none. First-packet recovery used as authorised. Repair enabled, unused.

## Run checks (mine: all 658 headers of the fifteen checkpoints, and the tree at `47d83f56`)

- Every configuration value quoted for the three sizes is exact, including explicit `head_dim` 128 for
  0.3B, one and three dense prefix layers, two shared experts for 21B and none for 300B.
- Every header shape quoted is exact for the checkpoint named; the bias exists as
  `mlp.moe_statics.e_score_correction_bias` with shape [1, 64]; the Paddle and quantized layouts are as
  described.
- Source: no `router_type` is passed, so `routing_std`; `key_e_score_bias` is set; shared experts only
  when the count is positive; `calibration_all_experts` is set; ChatML `default_chat_prompt` in both
  classes. The reference templates use `<|begin_of_sentence|>` with User/Assistant labels, as the finding
  says.

## Reviewer knowledge (never to a teacher)

From my pass over every shard, beyond what the entry read:

- 21B-A3B-Base-PT stores `lm_head.weight` although its configuration is tied; 21B-A3B-PT stores none. Both
  load: `Linear` tries `lm_head` first and the embedding alternate second. The builder's
  `has_tensor("lm_head")` test can never be true (keys end in `.weight`), the same latent slip as in
  `mistral3.py`; here it only means the alternate is always offered when tied.
- The router bias is BF16 in 21B and F32 in 300B; `mlp.gate.weight` is F32 in 300B.
- The non-Base PT checkpoints carry `mtp_block` tensors the builders never read (the entry says so from
  the configurations).
- 21B Base-Paddle also carries `resampler_model.*` tensors and a second router weight.

## Must fix before canonical use

1. State the head branch per checkpoint (first item above) and the `has_tensor` key slip.
2. Say whether the reference implementation uses the correction bias in routing; the entry correctly
   leaves this open, and it decides whether "ignored" is a defect.
3. Read the PT instruction checkpoints' headers, not only the Base ones.

## Ledger

- Accepted: `base-vocab-special-token-decoding` r001 (291 follow-up, with my qualification recorded).
- File with the next request: the new template identity; an observation on `custom-bias-export-name`
  noting the built-in Ernie caller; a fix revision for `missing-ernie-registry-modules` at `47d83f56`;
  the two carried observations.
