# Verdict: commit-000234-002 (replacement of 234/001; teacher Sol, guidance 12, unassisted)

Reviewer: Fable. Date: 2026-11-17. Upstream `45fa5abf` "Support Mistral 3 architecture (LLM+VLM)".

## Decision

**Approved for ancestor retrieval only. 234/002 replaces 234/001 as the entry in force for commit 234** for
packets prepared from now on; 234/001 is kept as history. Canonical and training stay false. Refresh the
three downstream readers (235, 241, 248) as the re-authoring plan says. This was the last re-authoring.

The finding `resize-overflow-reaches-vision-rope-table` is **accepted as true as stated**; it is the existing
231 identity, now carried to the 230 angle table. It answers the first two "must fix" items of the 234/001
verdict: the overflow reaches the table, and the projector layout and the hard-coded 5120 are stated from the
headers. The entry made the header check itself.

Superset: the one formal finding is kept and strengthened, and every mechanism 234/001 stated is present.
The two dropped qualifications you disclosed (the autosplit probe is a loading probe without the image
path's rotary parameters and `causal=False`; tokenizer special-token agreement unverified) are peripheral and
go under "must fix" below.

## Artifacts

Request hashes match. `check.py` clean: `gpt-6.1-sol` medium (server-confirmed), 45 implementation hashes all
equal to the accepted set, 70 evidence calls all cited and none bad, final equals annotation, 233 ancestors,
3232 blobs, nothing after the cutoff. Repair enabled, not used.

## Run checks (mine)

- Every shape in the Base header paragraph is exact (text, vision, patch convolution, merger [1024, 4096],
  `linear_1` [5120, 1024], `linear_2` [5120, 5120], head and embedding [131072, 5120]); no bias or scale
  tensor; 585 tensors in the Hugging Face layout.
- Resize: my transcription gives (28, 1541) to (28, 1568); grid (112, 2); highest position 111 × 110 + 1 =
  12211 against 12100 rows. As stated.
- Source: `PixtralImageProcessorFast` and patch-size assertions in the configuration constructor; vision
  KV-head default; `pad_to = 1`; hard-coded 5120; `max_edge_features`; `causal: False`; `[IMG_BREAK]` and
  `[IMG_END]`; `default_load_params` defined in the base model and Mistral3 only, called once in
  `_load_autosplit`, itself called once. All as stated.

## Reviewer knowledge (never to a teacher)

- The Instruct headers, which the entry did not read, are identical to Base in every name, shape and dtype
  (BF16, 585 tensors). So the entry's configuration-level agreement holds at tensor level too.
- Each repository also has the 585-tensor `consolidated.safetensors` copy under other names (as in the
  234/001 verdict).

## Must fix before canonical use

1. `has_tensor(key_prefix + "lm_head")` at `mistral3.py` line 179 asks for a key without `.weight`, so it can
   never be true (234/001 reviewer finding 3). The entry says only that the stored head makes the fallback
   unnecessary. Latent; the teacher has now passed over it twice.
2. The wide-image case: 1541 × 28 becomes 1568 × 28, 112 columns, no out-of-range read but columns 110 and
   111 take the next row's angles.
3. The two dropped qualifications above.
4. The end-of-image token sequence against a pinned reference source (carried over).

## Ledger

The three 255 records (`eager-undeclared-transformers`, `integration-not-packaged`,
`decoder-multipliers-not-forwarded`, each r001) are **accepted**. For this entry: add an observation to the
existing resize-overflow identity for the table consequence; file item 1 as a reviewer observation when the
validator accepts that origin.

## Next

`run-ahead-migration-001` (journal backup hash, migration, diff); wait for my answer before any run-ahead
session. Then 256.
