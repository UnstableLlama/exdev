# Verdict: commit-000234-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000234-001`
Packet: `.teacher/retrieval/000234-001`
Upstream: `45fa5abff9001ff373a612303e48ec01d34efe42` "Support Mistral 3 architecture (LLM+VLM)"
Request: `reviews/requests/commit-000234-001.md` (sha256 `24fadce293a5e44f8285be47b851a05d68dcb56c07317dddc1c18b4ef4220bbe`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true and the finding is true as stated. It stops one step short: the same
overflow, in this caller, reaches the angle table added at 230 (below). The manual reference recovery is
accepted, with one gap in what it gathered. The ledger item filed with this request is accepted.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 35 of 35 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 233 strict-ancestor entries; 3,232 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 34 of 35 identical. The one difference is the recorded tool error (`evidence_index` with `max_bytes` 24000), declared in the request. |
| Unassisted | Standing instructions byte-identical to 233/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-03T01:09:39Z; my query agrees. Two closed rows selected; PR 25's link is called an inference. |
| Loader change | `default_load_params` (empty by default) now supplies one parameter dictionary used for every module in the automatic-split probe, in place of a fresh empty one per call. Correct. |
| Text model | Embedding, RMSNorm/attention/gated-MLP blocks, final norm and head under `language_model.`, settings from `text_config`. Correct. |
| Vision tower | `patch_conv`, `ln_pre`, blocks with RMSNorm, attention with RoPE and a gated MLP (`pad_to = 1`), then projector norm, `Mistral3PatchMerger` (unfold into merge × merge neighbourhoods, then a linear layer) and a plain `MLP` with GELU and `out_size` equal to the text width. Correct. |
| Angle table | Half of the frequencies go to rows and half to columns; the table has (longest edge / patch)² rows of width head/2; position IDs are row × that edge + column; passed through the 230 interface. Correct. |
| Token string | One placeholder per merged vector, `[IMG_BREAK]` after every row and `[IMG_END]` at the end. Correct as a description of the code. |
| Configurations | From the bundle, Instruct-2503: text width 5120, head 128, 32/8 heads, 40 layers; vision width 1024, head 64, 16 heads, 24 layers, patch 14, image 1540, merge 2. As stated. `vision_config.rope_theta` is the float 10000.0 read as `int`; `read_dict` converts a whole-number float, so it loads. |
| Arithmetic | 110 × 110 patches, 12,100 table rows of width 32, 3,025 merged vectors, 3,081 tokens, merger input width 4,096. Agreed. |
| Finding: resize overflow | A 1541 × 1000 image gives 1568 × 1008 with longest edge 1540 and a 28-pixel grid (my run). True; the 231 identity, now with a caller. |
| Execution | Scalar arithmetic and an index check; labelled. |

## Reference evidence

| Check | Result |
|---|---|
| Enumeration | 83 repositories under `mistralai`, 83 candidate rows, none unavailable; two match. |
| Pins (my own query) | Instruct-2503 `73ce7c62` (2025-05-09) and Base-2503 `db7c9687` (2025-05-23) are each repository's latest commit before the cutoff. |
| Bundle | 32 objects: five metadata files and eleven tensor headers per model, official source, no mirror. Nothing in the packet names the mirror-inspected non-match. |
| **Gap** | Both repositories have `preprocessor_config.json` and `processor_config.json` at the pinned revisions; neither is in the bundle. The commit's configuration class opens the first unconditionally and asserts on it, so it is architecture evidence. The teacher asked for it, was told no approved object exists, and said so. |

## Reviewer findings (not in the entry)

1. **The overflow reaches the 230 table.** The table and `max_edge_features` are built for 110 patches per side.
   When the 231 overflow makes the resized image 1568 on one side, that side has 112 patches.
   - Tall image (1000 × 1541 becomes 1008 × 1568): 112 rows, so position IDs run to 111 × 110 + 71 = 12,281,
     past the table's 12,100 rows. This is the 230 table-row-bounds finding reached from the ordinary
     `get_image_embeddings` path: an out-of-range read on the GPU.
   - Wide image (1541 × 1000 becomes 1568 × 1008): 112 columns, so columns 110 and 111 take the angles of the
     next row's columns 0 and 1. No out-of-range read, but wrong positions.
   Of the heights 1541 to 5999 at width 1000, 198 overflow (my count). Arithmetic and source reading only.
2. **The projector's middle width is hard-coded to 5120.** The code comment asks whether it is hard-coded. The
   headers answer: `linear_1` is [5120, 1024] and `linear_2` [5120, 5120], so the width is the text width,
   which is 5120 for these two models. Another text width would not fit. Latent.
3. **`has_tensor` is asked for a key without `.weight`.** `has_tensor(key_prefix + "lm_head")` can never be true,
   so with tied embeddings the head would always take the embedding even if a head tensor exists. The
   reference models are not tied. Latent.

## Reviewer knowledge (never to a teacher)

- **Headers.** Every key the code asks for exists with the expected shape under `language_model.`,
  `vision_tower.` and `multi_modal_projector.`; none has a bias; the merger's layer is [1024, 4096]. Each
  repository also carries a second, differently named copy of all weights (`consolidated.safetensors`:
  `layers.N.attention.wq`, `vision_encoder.…`, `vision_language_adapter.…`). The loader indexes every
  `.safetensors` file in the directory, so both sets are indexed; the names do not collide.
- **Preprocessor file at the pins (fetched by me from the official repositories).** Both have processor type
  `PixtralImageProcessorFast`, longest edge 1540, patch size 14, resample 3, rescale 1/255 and CLIP mean and
  deviation; `processor_config.json` has merge size 2 and the three image tokens. So the entry's assumed 1540
  is the real value.
- **Token string, from memory and not checked against a pinned source:** I recall the reference processor
  replacing the last row's break token with the end token, where this code emits both. Check before canonical
  use; I am not asserting it.
- **Hindsight.** Upstream `a7e667c3` (2025-06-19) later accepts `PixtralImageProcessor` as well as the "Fast"
  type, so some checkpoint failed the assertion added here.

## Not verified

- Any loading, image processing or inference; numerical agreement with a reference implementation.

## Must fix before canonical use

1. Carry the overflow finding through to the angle table (reviewer finding 1).
2. State the projector width and layout from the headers instead of leaving them unestablished (finding 2 and
   the first knowledge item). This is the fourth architecture entry (213, 214, 225, 234) that left headers in
   its packet unread.
3. Check the end-of-image token sequence against a pinned reference source.

## Requests to Astra (not blocking 235)

1. **Evidence gap.** File an implementation request so that reference recovery also gathers
   `preprocessor_config.json` and `processor_config.json` (pinned, like the other metadata) whenever they
   exist. Do this before the next architecture commit that reads either file. Say in that request whether you
   propose to backfill 164/225 and 234; backfilled files would serve later positions only, never re-author an
   approved entry.

## Ledger items filed with this request

- `exllamav3-mlp-unsupported-activation--r002`: **accepted.** Supersedes r001; adds 233 as an observation.

## Follow-ups

1. Ledger, with 235's request: `exllamav3-vision-floating-ceiling-overflow` gains this commit as its first
   caller; `exllamav3-rope-table-row-bounds` gains a reviewer observation that the Mistral 3 path reaches it
   through that overflow (reviewer finding 1), marked reviewer-only. One reviewer-observation record for the
   hard-coded projector width; the `has_tensor` slip may ride on the same record or be left in this verdict.

## Next

1. Record this approval with `--approve`.
2. Proceed to 235.
