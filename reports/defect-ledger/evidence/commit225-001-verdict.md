# Verdict: commit-000225-001

Reviewer: Fable (independent reviewer; file mailbox)
Run: `.teacher/runs/commit-000225-001`
Packet: `.teacher/retrieval/000225-001`
Upstream: `532d78658414d8f9aabce52cb64b982b3ec53388` "Gemma3: Add vision model"
Request: `reviews/requests/commit-000225-001.md` (sha256 `4c5cc501d6fcff30504bf3023c6d999a39c1370ff0d77ba307fd490a64c3670b`)
Reviewed: 2026-11-16, working tree on top of `39357a9`, machine `exdev-314`

## Decision

**APPROVED for ancestor retrieval only.** Canonical and training remain false.

Every statement I checked is true. No findings are filed. Two things are missing (below): a width/height order
slip that the reference image size hides, and the tensor layout, which the packet's headers settle. The ledger
item filed with this request is accepted, and I agree with the request's reach analysis of the 218 follow-up.

## Artifacts reviewed (sha256)

Every hash listed in the request matches the file on disk.

## Run checks

| Check | Result |
|---|---|
| Run integrity | 31 of 31 ledger entries match the transcript, none uncited; final message equals the annotation; Markdown equals the render; full review; 44 of 44 implementation hashes; exactly 224 strict-ancestor entries; 3,146 blobs hash to their names; no evidence timestamp after the cutoff. |
| Replay | 31 of 31 recorded tool calls identical, including eleven `hf_fetch` calls and the `run` call. |
| Unassisted | Standing instructions byte-identical to 224/001's. Guidance 9. |
| No hindsight | No blob in the packet contains `reviews/verdicts` or a defect-ledger path. |
| Catalog | Sixteen open rows at 2025-06-02T00:03:38Z; my query agrees. One closed row selected. |
| Configuration | `Gemma3Config` now reads the vision settings (heads, width, patch size, layers, intermediate width, tokens per image, image size) and opens `preprocessor_config.json` unconditionally, asserting the processor type and reading mean, deviation, resample, rescale factor and size. Correct, including that the text-only use of such a model now needs the file. |
| The tower | `Conv` patch embedding, `PosEmbedding`, then per layer LayerNorm, attention without RoPE (keys `q_proj`, `k_proj`, `v_proj`, `out_proj`), LayerNorm and a plain `MLP` (`fc1`, `fc2`, GELU, `pad_to = 1`); then post-LayerNorm, `Gemma3MMPool`, an RMSNorm with constant bias 1 and a `Linear` projector with `transposed_load = False`. Correct. |
| Pooling | Tokens are laid out as a square grid and average-pooled with kernel and stride `patches_per_side // tokens_per_side`; no weights. Correct. |
| Preprocessing | RGB on white, one resize, float32, multiply by the rescale factor, normalise, channels first, half precision, batch dimension added. Correct. |
| Embedding output | The result is moved to the CPU, wrapped between the start and end image token IDs with one placeholder per vector, and returned as an `MMEmbedding` with size metadata. Correct. |
| Autosplit hook | The override returns a half-precision image-shaped probe. Correct. |
| Reference geometry | For `gemma-3-4b-it` I read the configuration from the 164 bundle: width 1152, intermediate 4304, 16 heads, 27 layers, image 896, patch 14, 256 tokens per image. As the entry states. |
| Arithmetic | Head width 72; a 64 × 64 grid of 4,096 patches; kernel 4; 16 × 16 = 256 tokens; 258 with the two boundary tokens; 4304 would round to 4352 at 128. Agreed. |
| Execution | Integer arithmetic only; labelled. |

## Reviewer findings (not in the entry)

1. **Width and height are in opposite orders.** `preprocess` builds `size` as (height, width) from the
   configuration, compares it with PIL's `image.size`, which is (width, height), and passes it to
   `image.resize`, which also takes (width, height). For a rectangular configured size the image would be
   resized to the transposed shape, while `default_load_shape_dtype` uses height and width the right way round.
   The returned `preprocessed_size` metadata is likewise (height, width) beside an `original_size` in (width,
   height). Every reference configuration is square (896 × 896), so nothing shows. Latent; source reading only.

## Reviewer knowledge (never to a teacher)

- **Tensor layout, from the `gemma-3-4b-it` headers gathered at 164.** Every key the tower asks for exists with
  the expected shape: patch embedding [1152, 3, 14, 14] with bias; position table [4096, 1152], exactly the
  number of patches; 27 layers with weight and bias for both LayerNorms, the four attention projections
  (1152 × 1152) and `fc1` [4304, 1152] and `fc2` [1152, 4304]; post-LayerNorm; the projector norm [1152]. The
  projector weight is stored as `multi_modal_projector.mm_input_projection_weight` with shape [1152, 2560], that
  is [input, output], which is why this is the first caller of `transposed_load = False` and why 215 renamed
  the key.
- **Preprocessor file.** The 164 bundle holds no `preprocessor_config.json`, so neither the teacher nor I could
  check those fields against pinned evidence. The mirror's current copy (undated, so hindsight) has the
  processor type the code asserts, mean and deviation 0.5, resample 2, rescale factor 1/255 and size 896 × 896.
- **The 218 follow-up.** I agree with the request: ordinary conversion builds the text component and copies the
  `vision_tower` and `multi_modal_projector` tensors from the source collection under their (renamed) keys, so
  the projector keeps its stored orientation and reloads correctly. Only a direct `get_tensors` export of the
  loaded projector would transpose it. Latent; no ledger identity.

## Not verified

- Any image processing, loading or inference; numerical agreement with a reference implementation.

## Must fix before canonical use

1. State the width/height order slip and that the square reference size hides it.
2. The entry says weight layout is unestablished although tensor headers for these checkpoints exist in the
   evidence; state what they show (first reviewer-knowledge item). This is the third new-architecture entry in a
   row (213, 214, 225) that left available headers unread.

## Ledger items filed with this request

- `exllamav3-pillow-package-metadata--r001`: **accepted.** Reviewer observation, suspected, introduced at
  `07401973`, no fix, not eligible for teacher context. It fails the schema's origin check like the other
  reviewer-origin records, which is the standing validator hold.

## Follow-ups

1. Ledger, with 226's request: a reviewer-observation record for the width/height order, introduced at
   `532d7865`, suspected, source-only, no reach at the reference size.

## Next

1. Record this approval with `--approve`.
2. Proceed to 226.
