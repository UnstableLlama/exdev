# 45fa5abff9001ff373a612303e48ec01d34efe42


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/45fa5abff9001ff373a612303e48ec01d34efe42) · [Evidence ledger](draft.json)

Adds component-aware Mistral3 text and Pixtral vision assembly, spatial patch merging, image-token serialization and autosplit parameters; source inspection identifies an inherited resize overflow reaching the new RoPE-table path.

- [Mistral3 text and Pixtral image components](#models)

## Problem

Adds registry support for Mistral3ForConditionalGeneration with separately selectable text and vision components. The parent registry supported ordinary Mistral, but not this conditional-generation architecture. [source; call_900f9b083ed742df9f6596fdcb86add8, call_3e30be17b6284c9b95e8ae7daa523b29, call_9a66b6e9eba342c98779102183e73705]

## Reasoning

The architecture assembly and loader change are complementary: the new patch merger requires spatial feature dimensions, so autosplit gains a default_load_params hook and passes its dictionary through the dummy forward pass. [source; call_3e30be17b6284c9b95e8ae7daa523b29, call_c8f51d5b633a4059b2309453ce7e1d93, call_4dafbcf1e73f4762a3226152a4c9cbd4]

## Impact

Configuration construction requires vision settings and preprocessor_config.json even when subsequently selecting only the text component. It accepts only PixtralImageProcessorFast and requires matching model/preprocessor patch sizes. [source; call_3e30be17b6284c9b95e8ae7daa523b29, call_f03a68ac347b4a488403ee79f832bbb0]

The vision compilation hook preserves vision_tower and multi_modal_projector tensors through the existing additional-tensor mechanism, without requiring the vision component to be instantiated for text-model compilation. [source; call_3e30be17b6284c9b95e8ae7daa523b29, call_7aad9092658247febabdbd5a987ae2cd, call_1458d5c2819a4936a3edcc993c7322f7]

## Source Notes

Read the Gemma3 vision, component-model, independently sized MLP, image-sizing and precomputed-RoPE ancestor entries. They establish the existing multimodal container/component interfaces, projector output sizing, image-alignment helper and position-indexed angle-table mechanism reused here. [ancestor; call_13ff89483f88432f9fb03de735cdd1ee, call_99975df7f58f4d72aa4f99f3727b2c7a, call_bb1e5a30a290475e9a2330f4d2570375, call_d9c3814451084691aad9597e7b6c2337, call_584036b8ccc4456da3f4a270bbf2a649]

The earlier image-sizing overflow remains in the unchanged helper and now has an integrated Mistral3 caller. The earlier RoPE row-bound omission also remains. The inspected reference head dimensions, 64 and 128, avoid the recorded warp-padding case, and this architecture supplies no fused Q/K normalization weights. Ordinary MLP's unsupported-activation omission remains unchanged, but the new projector selects its implemented GELU branch. [source; call_0035c45b902448e4b3b28252bf05770f, call_36539a2c2a5d44d4a63f2dc53dae6b66, call_531e028617cd4572a2e0fbdd300756ee, call_3e30be17b6284c9b95e8ae7daa523b29, call_54232fc7e3db4e4daec08c4223fc08a1]

The component-model ancestor's Qwen3 MoE migration observation is no longer present in the inspected parent constructor: it already supplies a text-component dictionary. This task leaves that constructor unchanged. [source; call_ee3c3fcc77aa492c95e05fa7cdede889, call_c8f51d5b633a4059b2309453ce7e1d93]

PR #25, “Language layers for Mistral Small 3.1 and InternVL3,” proposes language-layer support; turboderp's response favors component-aware multimodal support over language-only patches. Its relationship to this task is inferred from the exact Mistral3 architecture identifier and the new component mapping, not an explicit commit reference. [inference; call_00db62ede54642e09d60fe7b31b1fc92, call_3e30be17b6284c9b95e8ae7daa523b29]

Other inspected discussions have only inferred source-path connections: #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” and #7, “quantizing model: undefined symbol: __cxa_call_terminate,” report installation/import failures; #4, “chore: update config.py,” corrects spelling; #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?,” discusses scaling policy. None establishes a Mistral3 failure addressed here. [inference; call_f79e7a261b714710af26c5b458a308ad, call_e372c8cbeb1445fcad00e7ebeebaa456, call_c06dc7b85a384050bd9ee69f85d3ea12, call_2465b3bfe30c4a60b5d293165b478c27]

The inspected opening of PR #26, “Superior 3INST parameters,” concerns decoder multipliers. Issue #33, “Error converting model,” reports a compiler tensor-loading failure; #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” report quantization failures. Connections here are inferred from shared linear.py or compile.py paths, not evidence that this architecture addition fixes those reports. [inference; call_791000a6105545e89edefdf5bc984dee, call_57e27040c56644bf8e2523a1578e0248, call_29c0df55d9ba4221989b61a9fed1ec8d, call_1fd811d5c6df476fabd7cc6320fe5cdd]

<a id="models"></a>

## Mistral3 text and Pixtral image components

Mistral3Config maps text to Mistral3Model and vision to Mistral3VisionModel. Existing Config.from_directory dispatches through the newly extended registry; Model.from_config selects the requested component, defaulting to text. Text tensors use the language_model. prefix and an embedding → RMS-normalized attention/SiLU-gated-MLP blocks → RMSNorm → logits projection pipeline. [source; call_900f9b083ed742df9f6596fdcb86add8, call_3e30be17b6284c9b95e8ae7daa523b29, call_f03a68ac347b4a488403ee79f832bbb0, call_4dafbcf1e73f4762a3226152a4c9cbd4, call_531e028617cd4572a2e0fbdd300756ee]

Individually, mistralai/Mistral-Small-3.1-24B-Base-2503 and mistralai/Mistral-Small-3.1-24B-Instruct-2503 specify the registered architecture and identical relevant dimensions: text width 5120, 40 layers, head dimension 128, 32 query heads, 8 KV heads, intermediate width 32768 and vocabulary 131072; vision width 1024, 24 layers, head dimension 64, 16 heads, intermediate width 4096 and patch side 14. Both specify merge size 2, three channels, final-layer features and no projector bias. Both omit vision KV-head count, so the adapter defaults it to 16; both omit text tying, so it defaults to false. [source; call_54232fc7e3db4e4daec08c4223fc08a1, call_b486662162e148e9bf1494376431429c, call_3e30be17b6284c9b95e8ae7daa523b29]

Preprocessing composites transparency onto white, converts to RGB, and chooses dimensions aligned to patch_size × spatial_merge_size. This prepares complete merge neighborhoods, rather than merely complete convolution patches. It then rescales float32 pixels, applies channel normalization, transposes to channels-first and returns a singleton-batch FP16 tensor. The helper asserts that the maximum dimensions are divisible by that alignment quantum; it does not provide a final maximum-size clamp. [source; call_3e30be17b6284c9b95e8ae7daa523b29, call_0035c45b902448e4b3b28252bf05770f, call_6c79721059194cfca1c96eb08b067701, call_ff34699dcb8445a19f8865da2111e459]

The vision tower uses patch-strided Conv, pre-RMSNorm and 24 configured transformer blocks with RMSNorm, rotary attention and SiLU-gated MLPs. Conv flattens its spatial result into row-major tokens. The vision MLPs request pad_to=1, preserving exact dimensions. get_image_embeddings supplies causal=False and no cache; Attention consequently defaults to its no-cache FlashAttention route. The existing SDPA alternative rejects sliding windows and softcaps, neither of which this tower configures. [source; call_3e30be17b6284c9b95e8ae7daa523b29, call_f12d287918294e5a9bda518ab78ac214, call_531e028617cd4572a2e0fbdd300756ee, call_2c6322bba0b744bb8f74173efb9b4a4d]

The vision constructor builds a two-dimensional RoPE angle table: alternating entries of the ordinary inverse-frequency sequence go to height and width, then their outer products are concatenated. For maximum patch-grid side N, token (row,column) selects table row row×N+column. Attention transfers the supplied table to its device and RoPE.apply forwards it to CUDA, where table entries are angles evaluated with sine/cosine, not frequencies multiplied by position again. The tower constructs its actual RopeSettings directly from vision head dimension and theta; the separately parsed vision.rope_settings object is not used by that constructor. [source; call_3e30be17b6284c9b95e8ae7daa523b29, call_2c6322bba0b744bb8f74173efb9b4a4d, call_adc22881a5fd439ca23f194d9c7ee194, call_36539a2c2a5d44d4a63f2dc53dae6b66]

After projector RMSNorm, Mistral3PatchMerger requires batch size one and features_size=(height,width). It reshapes the sequence into a spatial grid, unfolds nonoverlapping merge×merge neighborhoods, and projects hidden_size×merge² back to hidden_size. An ordinary GELU MLP then maps vision width through a hardcoded 5120 intermediate to text width. The existing MLP out_size feature supplies the unequal endpoint widths; its GELU implementation uses the tanh approximation. The 5120 specialization agrees with the inspected Base projector tensors rather than being a general configuration-derived width. [source; call_3e30be17b6284c9b95e8ae7daa523b29, call_531e028617cd4572a2e0fbdd300756ee, call_d88f92a99e054b67b42e5f91bd823b19]

The Base shard headers contain every requested primary weight across text layers 0–39 and vision layers 0–23. Text Q is [4096,5120], K/V [1024,5120], O [5120,4096], gate/up [32768,5120], down [5120,32768], with [5120] norms and [131072,5120] embedding/head weights. Vision attention matrices are [1024,1024], gate/up [4096,1024], down [1024,4096], norms [1024], and patch convolution [1024,3,14,14]. Projector merger, linear_1 and linear_2 weights are respectively [1024,4096], [5120,1024] and [5120,5120]. These stored output-by-input linear shapes agree with Linear's default transposed loading. [source; call_d88f92a99e054b67b42e5f91bd823b19, call_3972d2bf561d43b888ee58f3c6672bd9, call_072876b4831c4c99b4bc329a5c7db2b2, call_66e339f7f4794bb593fbb446f38625d9, call_fb02e115b28e402f856bae31e7546c5f, call_fe86553ce34a4fccaf735ea5bdf43b51, call_ea96fae4364240079d3674dd5bbcce2e, call_2276c688701f4d9cb484f8dd6e1270d7, call_9251c6db5c204782bb171f90cc6887d8, call_c122c927a48541e4a1e267bcd984fdb9, call_c9aa688c05cd45479dee680046d09c36]

Those Base headers contain weights only: optional convolution/linear biases and linear weight_scale_inv tensors are absent, so their loaders take the no-bias/no-FP8-scale path. EXL3 storage groups are absent, selecting ordinary weight loading. The untied language head exists, so no embedding fallback is needed. No stored weight in the inspected Hugging Face-format shards is left without a corresponding component module. [source; call_d88f92a99e054b67b42e5f91bd823b19, call_3972d2bf561d43b888ee58f3c6672bd9, call_072876b4831c4c99b4bc329a5c7db2b2, call_66e339f7f4794bb593fbb446f38625d9, call_fb02e115b28e402f856bae31e7546c5f, call_fe86553ce34a4fccaf735ea5bdf43b51, call_ea96fae4364240079d3674dd5bbcce2e, call_2276c688701f4d9cb484f8dd6e1270d7, call_9251c6db5c204782bb171f90cc6887d8, call_c122c927a48541e4a1e267bcd984fdb9, call_c9aa688c05cd45479dee680046d09c36, call_f12d287918294e5a9bda518ab78ac214, call_8c4c05a47fb3480f9560492a160bd6e4, call_2a7b3ffc387446f8b161ed80984d4e3e, call_3e30be17b6284c9b95e8ae7daa523b29]

get_image_embeddings moves projected vectors to CPU and constructs one -1 placeholder per merged patch, an [IMG_BREAK] after each row, then [IMG_END]. MMEmbedding replaces placeholders with synthetic token IDs while retaining the vectors and alias. This agrees with the existing container interface and Embedding's indexed-vector reader. The parent has one other MMEmbedding builder, Gemma3, which instead surrounds its placeholders with start/end image IDs. The existing multimodal example uses this interface but remains configured for Gemma3; the task adds no Mistral3 prompt example. [source; call_3e30be17b6284c9b95e8ae7daa523b29, call_8367c490480c4f9b864f6d5ef785e847, call_935cd1bc887f49ffb270f723ab6fda09, call_2a7b3ffc387446f8b161ed80984d4e3e, call_837ef18a54354c309262e3373987250d, call_0092066ba32448afa8b3cf1bd73238f3, call_4f8e1f7022b34e32b56cd621ce3bf576]

A standard-library arithmetic transcription, conditional on preprocessor longest_edge=1540, gives a 110×110 patch grid, a [12100,32] angle table, merger input width 4096, and 55×55=3025 image vectors serialized into 3081 tokens. It also checks rectangular row×N+column indexing without aliasing inside the valid grid. These are shape/index calculations, not tensor or model execution. [execution; call_e12d0a063ac5492a81225a19678ba15f]

Autosplit now creates one params dictionary from default_load_params and shares it through module device preparation and forward calls, instead of passing fresh empty dictionaries. Mistral3VisionModel supplies the maximum feature-grid dimensions needed by its merger; the base hook returns {}. Whole-parent searches found no existing hook collision, only the base/Gemma3 load-shape implementations, and only load_gen calling _load_autosplit. Gemma3 remains on the empty-parameter default. Explicit single-device loading does not run this probe. [source; call_c8f51d5b633a4059b2309453ce7e1d93, call_3e30be17b6284c9b95e8ae7daa523b29, call_70d824adf82d42618e2d5d257bd88663, call_2203c455a2f44daa8c817bd1e57d7c12, call_03354cd65ce94ab192cd836a9faa1fbc, call_869de16301f34a0fb1c2868a58168a27, call_4dafbcf1e73f4762a3226152a4c9cbd4, call_837ef18a54354c309262e3373987250d]

## Authoring-time findings — pending review

### resize-overflow-reaches-vision-rope-table (suspected; defect)

The new image pipeline inherits an unclamped floating-point resize overflow, allowing feature positions outside its precomputed RoPE table.

Trigger: Use an otherwise valid processor configuration with longest_edge=1540, patch_size=14 and spatial_merge_size=2, then call Mistral3VisionModel.get_image_embeddings with a 28×1541 image.

Expected: Resize to merge-aligned dimensions within the configured maximum, keeping every generated position ID inside the angle table.

Actual: The scalar transcription rounds the limiting height to 1541 before alignment and returns 28×1568. The new caller therefore builds features_size=(112,2), with position IDs reaching 12211 despite only 12100 table rows. Neither the image caller nor the inspected CUDA wrapper validates row bounds. Source reach is the new get_image_embeddings → preprocess → helper → vision attention path; the parent had no caller of the sizing helper. No resulting image-library behavior or GPU fault was observed.

Locations: 45fa5abff9001ff373a612303e48ec01d34efe42:exllamav3/models/mistral3.py — Mistral3VisionModel.preprocess / get_image_embeddings, 45fa5abff9001ff373a612303e48ec01d34efe42:exllamav3/util/vision.py — size_to_longest_edge_and_patch_size

Source evidence: call_3e30be17b6284c9b95e8ae7daa523b29, call_0035c45b902448e4b3b28252bf05770f, call_6c79721059194cfca1c96eb08b067701, call_36539a2c2a5d44d4a63f2dc53dae6b66

source_inspection: Compared the unchanged helper with the new caller, position-grid construction, attention forwarding and native table-indexing guards. [call_0035c45b902448e4b3b28252bf05770f, call_3e30be17b6284c9b95e8ae7daa523b29, call_2c6322bba0b744bb8f74173efb9b4a4d, call_36539a2c2a5d44d4a63f2dc53dae6b66]. Limits: The trigger specifies processor settings; the reference preprocessor file was unavailable.

scalar_transcription: Transcribed scaling, ceiling, patch alignment and position indexing using Python floats and math.ceil; obtained output (28,1568), feature grid (112,2), and maximum position 12211. [call_197426d9e2ef4fa4a603d55384080a36]. Limits: Did not execute NumPy, Pillow, repository code or CUDA; does not measure an actual out-of-bounds load.

## Uncertainty and limits

No repository model, PyTorch operation, image resize, CUDA kernel, conversion or inference was executed. Python checks transcribe scalar arithmetic and do not establish numerical parity, GPU safety or performance.

Both reference config.json files were read, but no approved preprocessor_config.json was available. Consequently actual preprocessing dimensions, normalization values and processor-type compatibility for those downloads remain unverified.

Tensor compatibility was checked against all ten Hugging Face-format Base checkpoint shard headers. The alternative consolidated checkpoint layout and Instruct tensor headers were not inspected; Instruct agreement reported here is configuration-level only.

Literal whole-tree searches do not establish compatibility for external or dynamically selected callers.
