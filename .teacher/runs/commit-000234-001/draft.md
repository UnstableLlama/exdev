# 45fa5abff9001ff373a612303e48ec01d34efe42


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/45fa5abff9001ff373a612303e48ec01d34efe42) · [Evidence ledger](draft.json)

Adds Mistral3 text and Pixtral vision assembly, spatial merging, image-token serialization and autosplit spatial parameters; the new preprocessing caller inherits a sizing-overflow risk.

- [Mistral3 text and Pixtral image components](#models)

## Problem

Adds Mistral3ForConditionalGeneration registration and separate text and vision components, rather than treating the checkpoint as a language-only Mistral model. [source; call_a53efb8baf8746d5ad0e2fdba20ab2da, call_00cb2dc6ce174608b1d34452e6fde068]

## Reasoning

The vision merger needs spatial dimensions after convolution has flattened the image. The new default_load_params hook supplies those dimensions during autosplit probing; it is a prerequisite for loading this assembly, not an independent cleanup. [source; call_00cb2dc6ce174608b1d34452e6fde068, call_c1c777559b8548018fb2e466fa50a402]

## Impact

Mistral3Config requires vision configuration and preprocessor_config.json even when only the text component is requested. It asserts PixtralImageProcessorFast and matching model/preprocessor patch sizes. [source; call_00cb2dc6ce174608b1d34452e6fde068, call_5ac37882aa864606863f3b087f512fa5]

## Source Notes

Read the Gemma3 vision introduction, image-sizing helper introduction, and independent MLP-output-width entries. They establish the preceding multimodal interface, sizing primitive, and projector-width capability reused here. [ancestor; call_ba09173379ed4e918266c1ee9e66ab94, call_c9b01c8b03614e22881a674ad74541ed, call_2659acaaf77744e0aeef7a573a08bdf3]

The earlier MLP entry's unsupported-activation concern remains in the unchanged implementation, but this new projector explicitly selects supported GELU. The earlier sizing overflow remains reachable through the new preprocessing caller. [source; call_574a5a8dac524774baeb7afc97ead013, call_81514a70349245709df4ca0760d83bb2, call_00cb2dc6ce174608b1d34452e6fde068]

PR #25, “Language layers for Mistral Small 3.1 and InternVL3,” was opened by gakada. Turboderp discussed delaying language-only support to preserve future component-model compatibility. Its relationship to this change is inferred from the matching Mistral3 architecture and component design, not an explicit commit reference. [inference; call_5d273a550d094a788d8a7d733559c639, call_00cb2dc6ce174608b1d34452e6fde068]

Issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” and #7, “quantizing model: undefined symbol: __cxa_call_terminate,” report installation/import failures. Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, discusses context-dependent scaling. Their relevance is inferred only from shared model.py or rope.py paths; none establishes a defect fixed by this adapter. [inference; call_549cba3b3a004fc8ab8db8a5128604f3, call_65ef63f02bf84d0fb77919e68c37c9a3, call_ae476381e0de497abfd1218306c3a690]

<a id="models"></a>

## Mistral3 text and Pixtral image components

The text component uses language_model-prefixed embeddings, RMS-normalized attention and SiLU gated-MLP blocks, final RMSNorm and an LM head. Nested text_config supplies dimensions and RoPE settings; explicit head_dim is respected rather than assuming hidden_size divided by head count. [source; call_00cb2dc6ce174608b1d34452e6fde068, call_a1bbfea6844d4be2b4857371c4ebbd97]

mistralai/Mistral-Small-3.1-24B-Base-2503 specifies text width 5120, head dimension 128, 32 query heads, eight KV heads and 40 layers; its vision tower has width 1024, head dimension 64, 16 heads, 24 layers, patch size 14 and merge size two. The inspected Instruct-2503 configuration independently has identical values. Both agree with SiLU text/vision blocks, GELU projector selection, three channels and final-layer features; omitted vision KV-head count defaults to 16. [source; call_c757633b68334e428c31d8899fcfae0e, call_1e5e08f07c1645099a6b787315156d40, call_00cb2dc6ce174608b1d34452e6fde068]

Preprocessing composites transparency onto white, aligns resized dimensions to patch_size times spatial_merge_size, rescales float32 pixels and normalizes channels before producing a half-precision BCHW tensor. Alignment prepares complete merger neighborhoods; the sizing helper requires the maximum edge to be divisible by that combined patch size. [source; call_00cb2dc6ce174608b1d34452e6fde068, call_81514a70349245709df4ca0760d83bb2]

The vision tower uses patch convolution, RMSNorm and attention/SiLU gated-MLP blocks. get_image_embeddings selects noncausal attention without a cache. The default selected implementation is decode_flash_attn_nc, which forwards causal=False to FlashAttention; the inherited SDPA alternative rejects sliding windows and softcaps, neither configured by this tower. [source; call_00cb2dc6ce174608b1d34452e6fde068, call_23c766e977214793b12bda00d0461246]

Vision rotary angles split alternating frequency components between height and width, concatenate their spatial tables, and flatten the grid. Position IDs use row times maximum-grid-width plus column, selecting image-specific coordinates from that table. Attention passes the table to RoPE.apply instead of its ordinary frequency vector. This is source-level data-flow correspondence, not verified parity with Transformers. [source; call_00cb2dc6ce174608b1d34452e6fde068, call_23c766e977214793b12bda00d0461246, call_14cf5916d5e24fef9d4236df49c5c30e]

After projector RMSNorm, Mistral3PatchMerger requires batch size one and reshapes tokens using features_size. Nonoverlapping unfold neighborhoods concatenate merge² patches per channel, then a learned Linear reduces that width to the vision width. An ordinary MLP maps vision width through fixed intermediate width 5120 to text width, using the existing tanh-approximate GELU implementation. [source; call_00cb2dc6ce174608b1d34452e6fde068, call_574a5a8dac524774baeb7afc97ead013]

The resulting vectors move to CPU. Each merged row contributes image placeholders followed by [IMG_BREAK], with [IMG_END] after the last row. MMEmbedding replaces placeholders with allocated synthetic IDs and retains vectors, alias and metadata. The existing multimodal example uses this interface but remains configured for Gemma3, not Mistral3. [source; call_00cb2dc6ce174608b1d34452e6fde068, call_263c022a395546ab95f5e9dad0a3db05, call_ce5552b985394f79962389b6c72a47f0]

For an assumed preprocessing edge of 1540, patch size 14 and merge size two, scalar arithmetic gives a 110×110 patch grid, a 12100×32 rotary table, 3025 merged vectors, and 3081 serialized tokens including row breaks and the end token. Merger input width is 4096. A rectangular-grid check also verified the flattened-index inverse. [execution; call_5f745d75c2c145bb9f4a7b041252f90b]

Autosplit now creates one parameter dictionary from default_load_params and shares it across device preparation and module forwards. The base hook returns an empty dictionary; Mistral3 vision supplies square feature dimensions matching its image-shaped probe. The probe does not supply the actual image's rotary table or causal=False, so it remains a loading probe rather than equivalent image inference. Single-device loading does not perform this probe. [source; call_c1c777559b8548018fb2e466fa50a402, call_00cb2dc6ce174608b1d34452e6fde068, call_5ac37882aa864606863f3b087f512fa5, call_d50be758b6984a4b8334adc5b55cfc44]

## Authoring-time findings — pending review

### inherited-resize-overflow (suspected; defect)

The new preprocessing path inherits floating-point ceiling overflow from the unchanged image-sizing helper.

Trigger: Call Mistral3VisionModel.get_image_embeddings with a 1541×1000 image and preprocessing longest_edge=1540, patch_size=14, spatial_merge_size=2.

Expected: Resize to a grid-aligned image whose dimensions do not exceed 1540.

Actual: The scalar transcription yields 1568×1008: division rounds the limiting dimension slightly above 1540, ceiling preserves 1541, and alignment raises it to 1568. Neither the helper nor the new caller clamps the result. The parent had no caller of this sizing helper; the task adds a direct preprocessing call reached by get_image_embeddings. The existing example invokes the same interface on Gemma3, so it is not itself evidence of a Mistral3 execution.

Locations: 16df3fd1810c4f0747ff4fd5fbcc1dc94c4d6628:exllamav3/util/vision.py — size_to_longest_edge_and_patch_size, 45fa5abff9001ff373a612303e48ec01d34efe42:exllamav3/models/mistral3.py — Mistral3VisionModel.preprocess

Source evidence: call_81514a70349245709df4ca0760d83bb2, call_00cb2dc6ce174608b1d34452e6fde068, call_8857efb6fa79405987eb3bd93934e709, call_be44b0637a904356893dc98f3eab6468, call_ce5552b985394f79962389b6c72a47f0

scalar_transcription: Transcribed ratio, ceiling and alignment using Python floats and math.ceil; the first tested overflowing width was 1541. [call_5f745d75c2c145bb9f4a7b041252f90b]. Limits: Did not execute NumPy, Pillow, the repository helper or rotary kernels. The preprocessing edge is an explicit test assumption, not a verified checkpoint preprocessing value.

## Uncertainty and limits

No checkpoint loading, image-library operation, tensor operation, or GPU inference was executed. Scalar checks model arithmetic only.

The requested pinned preprocessor_config.json was unavailable; actual preprocessing values and tokenizer special-token agreement remain unverified.

The hard-coded projector intermediate width 5120 matches text width in both inspected configs, but neither config establishes the projector's weight dimensions. Tensor headers and numerical parity were not checked.

Whole-tree compatibility inspection covered the new loading hook, sizing helper and image-embedding entry point, but not every inherited module caller or configuration-key variant.
