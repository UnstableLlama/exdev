# Verdict: commit-000271-001 (teacher Sol, guidance 12, unassisted; architecture commit; validation-repaired)

Reviewer: Fable. Date: 2026-11-17 (09:01 UTC). Upstream `2d1ce891` "Add Dots1ForCausalLM architecture".
Run: `.teacher/runs/commit-000271-001`. Packet: `.teacher/retrieval/000271-001`.

## Decision

**Approved for ancestor retrieval only.** Canonical and training stay false. Both findings are accepted as
true as stated: `dots-default-prompt-format` (new, external compatibility) and
`inherited-dots-all-expert-fusion` (observation of the existing all-expert identity, now with a built-in
caller that sets `calibration_all_experts`). The entry made the central checks of an architecture commit
itself: it read both reference configurations against the builder's defaults, and read tensor headers and
compared names, shapes and orientation with what the builder asks for.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes
equal to the accepted set, 66 evidence calls all cited and none bad, final equals annotation, 270 of 270
ancestors, 3672 blobs, nothing after the cutoff. Orchestration hashes equal the accepted files; complete
packet; ran ahead of none. First-packet recovery used as authorised.

Validation repair, checked from the transcript: refusal at index 129 ("Unknown or unsuccessful evidence
call"), verbatim feedback, three further read-only calls, final at 137; the same two findings before and
after.

## Run checks (mine)

- Configurations (both pins): every value the entry quotes is exact, including the three that override
  builder defaults (one initial dense layer against a default of 3, six selected experts against 8, two
  shared experts against 1) and the EOS difference.
- Headers, base checkpoint: every shape the entry quotes is exact, all BF16; the bias name
  `model.layers.N.mlp.gate.e_score_correction_bias` exists with shape [128]; `lm_head.weight` is stored.
- Source: the builder, the routing selection (`deepseekv3_routing`, both group values one), the skipped
  first `o_proj`, `calibration_all_experts`, and the ChatML `default_chat_prompt` are as stated. The
  instruction checkpoint's template uses `<|system|>`, `<|userprompt|>`, `<|response|>` delimiters with a
  default system message, as the finding says; the only in-tree caller is `examples/imgsearch.py`.

## Reviewer knowledge (never to a teacher)

My pass over all 67 shards of both checkpoints: 24231 tensors each with identical names and shapes. Layer 0
is the only dense layer; 61 sparse layers. **The one difference: the correction bias is BF16 in base and
F32 in the instruction checkpoint.** Everything else is BF16. No bias or scale tensors on any linear.

## Must fix before canonical use

1. State the instruction checkpoint's tensors from its headers (the entry rightly says it did not read
   them), including the bias dtype difference and what loading does with a float32 bias, which the module
   fetches without conversion.
2. The entry computes the dense width padded from 10944 to 11008 but does not say what follows from it
   (which path loads a padded dense layer after the 266 change).

## Ledger

- Accepted: the seven 270 records (`native-router-argument-mismatch` r001, `grouped-routing-unassigned`
  r001, `optional-inputs-required-by-dots` r001, `all-expert-fused-shape` r007,
  `shared-mlp-allocation-interface` r002, `ordinary-output-accumulator-dtype` r002,
  `fused-shared-unreachable` r003).
- File with the next request: the new prompt-format identity and the all-expert observation.
