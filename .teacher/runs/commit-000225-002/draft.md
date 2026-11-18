# 532d78658414d8f9aabce52cb64b982b3ec53388


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/532d78658414d8f9aabce52cb64b982b3ec53388) · [Evidence ledger](draft.json)

Replaces Gemma3's vision stub with a configurable image tower, spatial pooling and projector, returning indexed multimodal embeddings; shared configuration now also requires vision preprocessing assets.

- [Gemma3 images become indexed language-space embeddings](#models)

## Problem

Gemma3 already exposed a vision component, but its constructor was unfinished and its load/unload methods raised NotImplementedError. This change replaces that stub with image preprocessing, a vision tower and language-space embedding production. [source; call_e33d4e849d3d47cebe447df61f21d1ce, call_548584d10c9a4ef88e1549ac8513de44]

## Reasoning

The implementation composes existing modules rather than adding a separate execution engine. Configuration supplies their dimensions; preprocessing supplies half-precision image inputs; pooling reduces patch sequences before projection into the text model's hidden width. [source; call_548584d10c9a4ef88e1549ac8513de44, call_10e645ef0d604682820fdc3a931f8b97]

## Impact

The vision component gains image_input capability and get_image_embeddings, returning an MMEmbedding containing CPU vectors, image-boundary tokens, an alias and size metadata. The text-only Gemma3TextModel is relocated without changing its prefix-free construction. [source; call_548584d10c9a4ef88e1549ac8513de44, call_40dca287017b4fcf979309ddf839766b]

## Source Notes

The Gemma3 introduction entry establishes the prior text/vision component separation and unfinished vision implementation. The RGB utility entry establishes that normalization alone did not rescale pixels; this task supplies that missing caller-side step. [ancestor; call_57b59beb37454803b550020ff3e53ccc, call_7cce593dee194569ba7d507d11e161dc]

The Conv, PosEmbedding, MLP-activation and Linear-orientation entries were read. They document the token-shaped convolution output, consecutive positional lookup, tanh-approximate GELU and already-oriented weight loading used here. [ancestor; call_a8a34d1462574a23beca7013f4599eb1, call_4fd0ed3d3eed4462a7c8999bdac6e4bc, call_588495609c554421aca5fbc2f1ac7393, call_48c22047e12048bfb17957947a2c8864]

Conv's recorded unused output-dtype controls remain unchanged, but this caller requests neither control. MLP's unsupported-activation case also remains unchanged, but the new caller supplies the supported literal "gelu". PosEmbedding still starts at position zero, fitting the new whole-image rather than chunked input path. [source; call_548584d10c9a4ef88e1549ac8513de44, call_581cf55ece66405694d6847c7490bcf5, call_ca5debbe4b7245189b7f0f0bd1647843, call_e33b45c7a4ef4940b090236fdfc6dfb6]

PR #25, “Language layers for Mistral Small 3.1 and InternVL3,” discusses component-model compatibility and later reports missing Gemma3ForCausalLM support. Its relationship to this task is inferred from that architecture reference and the shared component design, not an explicit link to this commit. [inference; call_9c3f8a370c344cc688d31133c11fa6f8, call_548584d10c9a4ef88e1549ac8513de44]

Issue #33, “Error converting model,” initially concerns file-opening failures and later GLM4 sampling. Its later discussion explicitly says Gemma3 vision_config was then ignored. That is relevant historical context by inference from the matching Gemma3 architecture and configuration identifiers, not evidence that this task fixes the reported conversion or sampling failures. [inference; call_b51296f6a128455a86c905d5207f3771, call_2351eb7c491d492188d0256371652ba8, call_12292f377d9f427f9eab4db8573c0a34, call_548584d10c9a4ef88e1549ac8513de44]

Other inspected reports concern different failures: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading; #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concern quantization/factorization. Connections here are inferred only from shared model.py or linear.py paths; none establishes a vision-model failure. [inference; call_66aa4fad67d043cfbe435856ae679d22, call_55a220df2a3d421fbab46acc0b03a009, call_07c027ddc147453980936c255e81b58f, call_10e645ef0d604682820fdc3a931f8b97, call_af1131ba1626423c9a9f4564fb6bdb74]

<a id="models"></a>

## Gemma3 images become indexed language-space embeddings

Gemma3Config now reads a separate vision namespace. Required fields include attention heads, hidden width, patch size and mm_tokens_per_image. KV heads default to query heads; head dimension defaults to hidden_size // num_q_heads. Other fallbacks include 24 layers, intermediate width equal to hidden width and image size 896. Three RGB channels and LayerNorm epsilon 1e-6 are fixed in code; multimodal_projector_bias is stored but not consumed by the new assembly. [source; call_548584d10c9a4ef88e1549ac8513de44, call_3e67c98524c14cd19b4e1cde65219fa2, call_b505de01527c4ce09f7ae1eeddd93308, call_3d855a8d6f51498183157c6b0edcb99b]

Configuration also unconditionally opens directory/preprocessor_config.json, requires image_processor_type == "Gemma3ImageProcessor", and reads image_mean, image_std, resample, rescale_factor and size. These settings are not optional merely because only the text component will subsequently be constructed. [source; call_548584d10c9a4ef88e1549ac8513de44, call_e33d4e849d3d47cebe447df61f21d1ce, call_10e645ef0d604682820fdc3a931f8b97, call_1258ba2e0e9b4bdc86d64ac87fcff2ef, call_70b1b269d2554500bff5b57e9d71f9ac]

preprocess converts transparency to white-backed RGB, resizes to its configured tuple, converts pixels to float32, multiplies by rescale_factor, then applies (image - mean) / std while channels are last. It finally transposes to channel-first, converts to half precision and adds batch dimension one. This is a single resized image path; the function adds no crop or multi-resolution expansion. [source; call_548584d10c9a4ef88e1549ac8513de44, call_d022e0ea3ab14746a9933d106be796a8]

Whole-parent-tree searches found no existing preprocess/get_image_embeddings methods, Conv or PosEmbedding construction sites, ordinary MLP construction sites, or callers of the two image utilities. The new vision implementation therefore integrates previously exposed primitives rather than copying an established image workflow with additional guards. [source; call_70b1b269d2554500bff5b57e9d71f9ac, call_14eec8167554444dbc569ff856aea5c7, call_927fc3c39c50416f8a814efff77d0b58, call_6ff01d5d65f344c28a5de0567156bb59, call_be7d78a8faf14c65bf9680083e5afed9]

The tower starts with a stride-equals-patch-size Conv, which flattens its spatial output into [batch, patches, hidden], followed by learned consecutive position vectors. Each encoder layer uses LayerNorm before attention and before an ordinary two-projection MLP, with residual additions supplied by TransformerBlock. Attention has no RoPE, and get_image_embeddings explicitly supplies causal=False. The inherited attention dispatcher selects uncached FlashAttention by default; its SDPA alternative permits this tower's absent sliding window and zero softcap. [source; call_548584d10c9a4ef88e1549ac8513de44, call_581cf55ece66405694d6847c7490bcf5, call_e33b45c7a4ef4940b090236fdfc6dfb6, call_e7cb53b6ec604481ab9b13854deb1fda, call_748c95e5c7e94af3a4f753ac54e87466]

The MLP selects tanh-approximate GELU and pad_to=1. These choices work together: the checkpoint intermediate width is 4304, whereas default 128-element alignment would round it to 4352 and the down projection rejects unapproved input padding. Keeping exact dimensions avoids that constructor precondition rather than merely reducing storage. [source; call_548584d10c9a4ef88e1549ac8513de44, call_ca5debbe4b7245189b7f0f0bd1647843, call_af1131ba1626423c9a9f4564fb6bdb74, call_c6c3581fc79b4140befb0a7663bc6f4d]

After post-LayerNorm, Gemma3MMPool transposes [B,P²,D] to channel-first spatial form, averages nonoverlapping square regions, and returns contiguous [B,T²,D]. The constructor derives P from image_size // patch_size and T from the integer square root of mm_tokens_per_image. A Gemma-style RMSNorm uses weight + 1, then Linear maps vision width to text width with transposed_load=False. [source; call_548584d10c9a4ef88e1549ac8513de44, call_61014b3fa80e4c1ca5a34439407ed1c9, call_af1131ba1626423c9a9f4564fb6bdb74]

A bounded scalar transcription calculated 896/14 = 64 patches per side, 4096 patch tokens, 1152/16 = 72 channels per head, a pooling kernel/stride of 4 and 256 pooled tokens. It checked raster-order averaging on two synthetic channels and obtained [1,256,2]. The resulting image token string has 258 positions including its two boundaries. This was not execution of PyTorch pooling or the model. [execution; call_2c2edfb56f2c49d49fae2c35f30119b4]

google/gemma-3-4b-it, google/gemma-3-4b-pt, google/gemma-3-4b-it-qat-int4-unquantized and google/gemma-3-4b-it-qat-q4_0-unquantized each explicitly provide the same tower: hidden/intermediate widths 1152/4304, 27 layers, 16 heads, image size 896, patch size 14 and 256 image tokens. Each therefore overrides the layer/intermediate defaults, derives 72-wide heads and equal query/KV head counts, and projects to text width 2560. The QAT files explicitly agree with the fixed three channels, epsilon 1e-6 and selected GELU variant. [source; call_c6c3581fc79b4140befb0a7663bc6f4d, call_43ff457cb2594365abc53e4ed74c1267, call_77501d7c2e3f4aa58d691d2500dfa21a, call_ac6eb37f134f41699bd399a8be9df506, call_548584d10c9a4ef88e1549ac8513de44]

google/gemma-3-12b-it, google/gemma-3-12b-pt, google/gemma-3-12b-it-qat-int4-unquantized and google/gemma-3-12b-it-qat-q4_0-unquantized each provide that same vision geometry and defaults, but project to text width 3840. google/gemma-3-27b-it, google/gemma-3-27b-pt and google/gemma-3-27b-it-qat-q4_0-unquantized likewise share the tower and project to width 5376. The three QAT files explicitly agree with the fixed channel count, epsilon and activation selection. [source; call_dc649946f096464c973d5fcf59b07ef0, call_8bd1f7bb7bc44eb29ca973161b452d32, call_8e82afeb4b1c4cefa9f2cfb515dc12ea, call_63333c70196d4494a78039f99977a001, call_8897baa9fe5a4235a2d780c700ccd188, call_378da604a809439b84e7e357fe1aa784, call_3f03f7acae004373a96426bb198d7ed4]

The 4B reference header contains patch weights [1152,3,14,14], patch bias [1152], positions [4096,1152], and all 27 layers' requested norm, q/k/v/out and fc1/fc2 weights and biases. Attention weights are [1152,1152]; fc1/fc2 weights are [4304,1152] and [1152,4304]. Post-LayerNorm and projector RMSNorm have width 1152. These vision tensors are all consumed by the assembly; pooling requests no checkpoint tensors. [source; call_c4bbbf9e97b44c4d85a129a150602f31, call_50df7cb4f1314337a58236a4619e3cce, call_548584d10c9a4ef88e1549ac8513de44, call_5ac945500a954f189dc6216283e4694c]

The reference projector is stored as mm_input_projection_weight with shape [1152,2560], [1152,3840] or [1152,5376] for the inspected 4B, 12B and 27B checkpoints. The existing header normalization changes that spelling to mm_input_projection.weight; transposed_load=False then preserves its input-by-output orientation. The sampled headers contain no projector bias or FP8 scale alongside these weights, so those optional reads have no supplied tensor. No alternate projector key is configured. [source; call_c4bbbf9e97b44c4d85a129a150602f31, call_19b7b8119f5d4f0ab5b2dc79efa80005, call_e77d0f1a5d1d4bce8cbf520609e266dc, call_02d95f143dac476e9fa5a812f1b9eedd, call_af1131ba1626423c9a9f4564fb6bdb74, call_548584d10c9a4ef88e1549ac8513de44]

The header-normalization ancestor records a collision when both projector spellings occur. That normalization remains unchanged in the inspected parent and is not repaired by this task; the inspected reference projector entries instead use the legacy spelling alone. [source; call_02d95f143dac476e9fa5a812f1b9eedd, call_c4bbbf9e97b44c4d85a129a150602f31, call_19b7b8119f5d4f0ab5b2dc79efa80005, call_e77d0f1a5d1d4bce8cbf520609e266dc, call_548584d10c9a4ef88e1549ac8513de44]

get_image_embeddings runs the tower noncausally, moves the result to CPU and removes its batch dimension. It constructs <start_of_image>, one -1 placeholder per vector, and <end_of_image>. MMEmbedding replaces placeholders with allocated synthetic IDs. Existing tokenization expands aliases to that token list, and Embedding.forward can replace synthetic IDs with the supplied vectors without applying the text embedding's square-root-width normalization to them. [source; call_548584d10c9a4ef88e1549ac8513de44, call_40dca287017b4fcf979309ddf839766b, call_02f657a704c844b2aa0344dcc315788f, call_988bfe927e8643d293119b4c93f8f657]

The autosplit hook now returns a half-precision [1,3,height,width] image probe instead of token IDs. Model._load_autosplit uses that metadata before loading and forwarding each module. Its dummy forwards use empty parameters, unlike get_image_embeddings' explicit causal=False, so the hook establishes input shape compatibility but not equivalent attention semantics during probing. [source; call_548584d10c9a4ef88e1549ac8513de44, call_10e645ef0d604682820fdc3a931f8b97, call_748c95e5c7e94af3a4f753ac54e87466]

## Authoring-time findings — pending review

### gemma3-preprocessor-required-for-text (suspected; new_requirement)

The shared multimodal configuration now requires preprocessing assets even for text-only use of its text component.

Trigger: Construct Gemma3Config from a directory with previously sufficient text configuration and tensors but no preprocessor_config.json.

Expected: The prior constructor could configure the text component without opening a vision preprocessor file.

Actual: The new constructor unconditionally opens preprocessor_config.json before a caller can select the text component; a missing file prevents configuration construction.

Locations: 532d78658414d8f9aabce52cb64b982b3ec53388:exllamav3/models/gemma3.py — Gemma3Config.__init__

Source evidence: call_e33d4e849d3d47cebe447df61f21d1ce, call_548584d10c9a4ef88e1549ac8513de44, call_5f640712b3b24086b33a7d6de51230c0, call_10e645ef0d604682820fdc3a931f8b97

source_inspection: Compared both constructors and searched the whole parent tree for Gemma3 references. Gemma3Model uses Gemma3Config, which supplies both component classes; Model.from_config defaults to text but receives an already-created configuration. Gemma3TextConfig is separate and is not changed by these new reads. [call_e33d4e849d3d47cebe447df61f21d1ce, call_548584d10c9a4ef88e1549ac8513de44, call_5f640712b3b24086b33a7d6de51230c0, call_10e645ef0d604682820fdc3a931f8b97]. Limits: No missing-file execution or affected packaged checkpoint was demonstrated; this records a new source-level requirement, not a confirmed deployment failure.

## Uncertainty and limits

No repository model, Pillow/NumPy preprocessing, checkpoint loading or GPU kernel was executed. The scalar check models pooling/indexing and dimension arithmetic only, without FP16 rounding.

The approved preprocessor_config.json retrieval failed. Actual checkpoint preprocessing statistics, resampling values and size settings therefore remain unverified.

Complete vision tensor-name coverage was inspected for the 4B reference; 12B and 27B header inspection sampled their vision tensors and verified their distinct projector widths. Other checkpoint variants were checked through configuration files, not exhaustive tensor headers.

Successful image-conditioned generation, conversion of the vision component, autosplit memory estimates and compatibility with dynamic or external callers were not demonstrated.

Gemma3MMPool assumes a square patch grid and compatible pooling geometry; the inspected reference configurations satisfy its dimension arithmetic, but arbitrary configuration support is not established.
