# Verdict: commit-000164-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000164-001`
Packet: `.teacher/retrieval/000164-001`
Upstream: `966762a32d1eb2c0aa5e01b02451676bca6ca7fd` "Add Gemma3 architecture (text)"
Request: `reviews/requests/commit-000164-001.md`
Reviewed: 2026-11-15, working tree on top of `d980d21`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. No findings in the entry, and my own comparison of the builder with the
eleven reference models found none: the text tensors match exactly. The entry read all three diff sections and
all eleven configurations, and went model by model through which adapter defaults are actually used.

The mirror-based recovery, the validation recovery and ledger record
`exllamav3-extra-tensor-warning-name--r001` are **accepted**.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 35 of 35 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 163 strict-ancestor entries (163's being attempt 002); 2,557 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay (mine) | 34 of 35 identical through `Runner`. The remaining call is the recorded error `Invalid max_bytes` for `evidence_index` with 24,000; replayed, the runner raises `ValueError: Invalid max_bytes`. Same outcome, different wrapping. |
| Validation recovery | Accepted. The driver's validator compared a raised exception with the stored error object and stopped; the session, the draft and the run files are untouched (the hashes in the request match). Your adapter reproduces the session's own serialisation. The permanent fix is an implementation change; file it as you say. My routine script has had the same quirk since the start. |
| Unassisted | Standing instructions byte-identical to 163/001's, the last unassisted run. The one ancestor entry read is 163/002, which is approved prose. |
| No hindsight | No blob in the packet contains `reviews/verdicts`, a defect-ledger path or the tracking files. |
| Catalog | Eleven open rows at 2025-05-16T10:14:47Z; my query agrees. One closed row, by path, selected; nothing cut. |
| Architecture trigger | Fires for `Gemma3ForConditionalGeneration`. No unresolved file, no curator attestation. |
| Reference list (mine) | I listed the publisher's organisation myself: 1,136 repositories. Exactly eleven declare `Gemma3ForConditionalGeneration` and were created before the cutoff (4b, 12b, 27b in `it` and `pt`; 4b and 12b `it-qat-int4-unquantized`; 4b, 12b, 27b `it-qat-q4_0-unquantized`). The bundle has those eleven. The next matching repositories are from 19 May 2025, after the cutoff. |
| Mirror identity (mine) | All sixty-six non-weight files in the bundle checked against what Hugging Face publishes without a login: 55 by Git blob id, and the eleven `tokenizer.json` files, which are large-file objects, by their SHA-256. All match. Selection dates are 21 and 22 April 2025. |
| Headers against the builder (mine) | For each of the eleven I built the list of text tensors the constructor asks for (embedding, per layer four norms, q and k norms, four attention projections, three MLP projections, final norm) and compared names and shapes with the recovered headers: 444 of 444 for the 4b models, 626 of 626 for 12b, 808 of 808 for 27b; nothing missing, no wrong shape. Everything left over is `vision_tower` (437) or `multi_modal_projector` (2), which are exactly the two prefixes the vision class's hook collects. No `lm_head` tensor exists; the head loads through its alternate key. All BF16. |
| Registration and config | `Gemma3Config` passes `{"text": Gemma3Model, "vision": Gemma3VisionModel}`; reads `text_config->…` with the defaults the entry lists; vocabulary falls back to 262,208; `num_hidden_layers` has no default. Correct. |
| RoPE helper | `read_rope_settings_default` gains default theta, default partial factor and an optional dictionary; `None` means the top-level configuration, `{}` means all defaults. Global settings read `text_config` with theta 1e6; local settings read `{}` with theta 1e4 and no scaling. Existing callers are unaffected. Correct. |
| Local and global layers | `bool((idx + 1) % sliding_window_pattern)`; local layers get the window and local RoPE, global layers get -1 and global RoPE; scale is `query_pre_attn_scalar ** -0.5`. Correct. |
| Per-model statements | 4b `it`/`pt`: 2560/10240, 34 layers, head counts and head size from defaults. 12b: 3840/15360, 48 layers, 16 and 8 heads given, head size from default. 27b: 5376/21504, 62 layers, 32 and 16 heads, head size 128, scalar 168. All: window 1024, linear RoPE factor 8. Correct against the bundle. |
| Activation | The builder passes `"gelu"`, which selects `gelu_mul`; that kernel is the tanh approximation, which is what the QAT configurations name. The entry says "GELU-gated"; fine. |
| Vision stub | `load` and `unload` raise `NotImplementedError`; the hook returns `list_tensors` for the two prefixes, whose entries carry the `n_bytes` that `compile_model` reads. Correct. |
| Execution | Recorded output: 29/5, 40/8 and 52/10 local/global layers; scales 0.0625 and about 0.0772. Matches the prose. |

## Ledger

- `exllamav3-extra-tensor-warning-name--r001`: accepted. Authoring origin from the rejected 163/001, reviewer
  confirmation stated, source only.

## Reviewer-only notes (never to a teacher)

- **The head is wider than the generator's logits buffer for these models.** 262,208 is a multiple of 32 and
  not of 128. The head `Linear` pads to 262,272; `Generator.padded_vocab_size` rounds to 32 and stays at
  262,208. That is the existing record `exllamav3-logits-padding-width-mismatch` (introduced at `1d77c052`),
  which until now had no reference model that triggers it. Sampling is not affected (the sampler masks beyond
  the tokenizer's vocabulary); the `return_logits` path is.
- **The 163 warning-name record now has a non-empty hook.** Gemma 3's vision class returns 439 tensors, so the
  additional-tensor loop runs for real from this commit. The wrong name only shows if one of them exceeds a
  shard, which these do not.
- `Gemma3ForCausalLM` (the 1b models, four repositories before the cutoff) is not registered by this commit.
  Expect it later. Qwen3 MoE is still broken at this commit; `qwen3_moe.py` is untouched.

## Not verified

- Any model load, conversion or generation.
- The vision tensors' shapes (the commit does not build them).

## Must fix before canonical use

- The recurring note: the teacher read no tensor headers and says so. The header comparison above is mine.

## Follow-ups

1. Ledger, `exllamav3-logits-padding-width-mismatch`: file a revision adding `966762a3` as an affected revision
   with the concrete case (vocabulary 262,208, head width 262,272, buffer width 262,208, eleven reference
   configurations). Reviewer observation, source only.
2. Implementation: the replay fix in `cycle.validate_run`, as its own request.
3. The remaining older ledger revisions are still owed.

## Next

1. Record this approval by hand (architecture commits are manual).
2. Then, in either order between commits: the guidance-6 implementation request, and 165.
