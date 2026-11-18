# Verdict: commit-000164-002 (replacement of 164/001; teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-16. Upstream `966762a3` "Add Gemma3 architecture (text)".

## Decision

**Approved for ancestor retrieval only. 164/002 replaces 164/001 as the entry in force for commit 164** for
packets prepared from now on; 164/001 is kept as history. Canonical and training stay false.

The finding `inherited-qwen3-moe-component-interface` is **accepted as true as stated**: at this commit
`Config` stores `model_classes` as a dictionary and every other architecture passes `{"text": ...}`, but
`Qwen3MoeConfig` still passes the bare class; `compile_model` calls `config.model_classes.items()`. It is the
existing `exllamav3-qwen3-moe-component-migration` identity, correctly labelled inherited and not a Gemma3
regression. 164/001 had no findings.

The entry made the central checks itself: the complete 4B text inventory against the names the builder
requests (finding no separate head, so the head loads from the embedding through the unconditional alternate
key), first-layer samples for 12B and 27B, all eleven configurations against the adapter defaults, and the
ten existing callers of the changed RoPE reader.

## Artifacts

Request hashes match (27 of 27). `check.py` clean: `gpt-6.1-sol` medium, 44 implementation hashes, 72
evidence calls all cited and none bad, final equals annotation. Manifest differs from 164/001's in
`guidance_version` only.

## Run checks (mine)

- All eleven configurations: every stated value and every stated omission-plus-default is right (4B IT/PT
  omit head counts and head_dim; 12B IT/PT omit head_dim and the query scalar; 27B supplies 128 and 168; QAT
  files spell out vocabulary, bases, pattern and null softcaps).
- All eleven checkpoints, every shard: every text tensor the builder requests exists with the stated shape,
  BF16, no extras under `language_model`, **no `lm_head` in any of the eleven**, and the same 437 vision and
  2 projector tensors in each. The entry established the head's absence for 4B IT only and says so; the rest
  is mine (reviewer-only).
- Source: adapter defaults, locality formula, window and scale forwarding, SDPA's window assertion, the
  `weight + 1` norms, float post-norms, unconditional `alt_key`, vision class raising NotImplementedError,
  the compile hook. All as stated.

## Missed or dropped (must fix before canonical use; peripheral)

1. **Head padding.** Vocabulary 262,208 is not a multiple of 128 (remainder 64), so `Linear` pads the head to
   262,272. This is the existing `exllamav3-logits-padding-width-mismatch` identity and Gemma3 is the first
   architecture whose reference models reach it. 164/001 missed it too (it is a reviewer observation in that
   verdict). The entry does dimension arithmetic but not this one. Same pattern as before: a new caller
   reaching a recorded defect.
2. 164/001 states the final norm is half precision; 164/002 does not (the request says so itself).
3. 164/001 notes the adapter never reads `rope_local_base_freq` and hard-codes 10,000; 164/002 says only that
   the QAT files agree with it.

## Note for the author (non-blocking)

The third `run` call executed a repository file (`exllamav3/util/file.py` through `runpy`). It is a pure
Python utility and the entry discloses it. Confirm in the next request whether the walk contract permits
executing repository code in `run`; earlier entries did not.

## Ledger, with the next request

Add `966762a3` as an observation on `exllamav3-qwen3-moe-component-migration` (no new record). The
logits-padding revision asked for in the 164/001 verdict stands if not already filed.

## Next

252 at guidance 12, then replacement 213. One request at a time.
