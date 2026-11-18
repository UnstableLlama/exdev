# dcae5a04be7885ad9dc9a6cfcb135ead75847695


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/dcae5a04be7885ad9dc9a6cfcb135ead75847695) · [Evidence ledger](draft.json)

Adds list-based Gemma3 image ingestion while preserving single-image returns. The inspected vision path preserves the batch axis and agrees with per-image output extraction; GPU correctness and performance remain untested.

- [Batch ingestion through the Gemma3 vision pipeline](#vision)

## Problem

Gemma3 image ingestion previously forwarded one image and returned one MMEmbedding. The change adds a list-input path that forwards several images together. [source; call_70411f6c659e4c78a2fa81329e3dc122]

## Reasoning

Fixed-size preprocessing supplies equally shaped tensors for concatenation along batch axis 0. Removing the final squeeze preserves that axis so the result can be split into one embedding container per image. [source; call_ee72740f055b48319c34f29438cc6830, call_70411f6c659e4c78a2fa81329e3dc122]

## Impact

A list returns a list of MMEmbedding objects, including for a one-element list; a single image retains the single-object return. List input rejects a supplied text_alias. Mistral3 remains single-image, and the existing multimodal example still calls ingestion separately for each image. [source; call_70411f6c659e4c78a2fa81329e3dc122, call_121c82bf84414ef8a51e0588100890c4, call_146bf1325264403ba2afc24e4f472b0c, call_d7eaf539ccc64f788b8c095a1cfaed97]

## Source Notes

The Gemma3 introduction, vision implementation and shape-comment cleanup entries were read. They establish the progression from a vision stub to the reusable image-to-token pipeline and its singleton preprocessing tensor; none records a defect in the ingestion code changed here. [ancestor; call_01042319fe10444f8687a6f1688c6eb9, call_b4e57bd159564836b77752c3d8f4772f, call_aee8226577604525a01b3e8e4b1e12e7]

Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports vocabulary/logit-width disagreement, not image batching. Its connection here is inferred from its Gemma3 source reference and shared tensor.py path; this diff does not address the reported failure. [inference; call_5d25e20a953b41069cb1a18efed6b16e, call_70411f6c659e4c78a2fa81329e3dc122]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading failure and an environment workaround. Issues #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concern quantization failures. Their relationships to this inspection are inferred only from shared model.py or linear.py paths, not evidence that image batching fixes them. [inference; call_48b765a81d8a4fcfb767ae9c9e6e7a2a, call_95ed08d609fc40b1aa88c2ca01d596ee, call_8bb45e2d98c44459b1fd01ace3559d52, call_70411f6c659e4c78a2fa81329e3dc122]

<a id="vision"></a>

## Batch ingestion through the Gemma3 vision pipeline

get_image_embeddings preprocesses each list member separately, concatenates the resulting (1, 3, height, width) tensors on axis 0, and performs one forward with causal=False. Preprocessing always resizes to the configured size, so prep_image_size is common to the batch even though only the last loop value is retained. Original sizes are taken individually from image[i]. [source; call_70411f6c659e4c78a2fa81329e3dc122, call_ee72740f055b48319c34f29438cc6830]

The ordered top-level path is patch Conv, PosEmbedding, encoder TransformerBlock instances in increasing layer index, post-LayerNorm, Gemma3MMPool, projector RMSNorm, and the final Linear projection. Gemma3VisionModel inherits Model.prepare_inputs, which stores the input without reshaping it. Model.forward visits every module in order; Module.prepare_for_device only transfers devices and does not collapse the batch axis. [source; call_ee72740f055b48319c34f29438cc6830, call_bf93f2c556bd43ae854b0c39e8b5841e, call_ea034a28258645359010843cb01b3c41]

Conv.forward (conv.py:70) selects its 2-D branch for this tower: conv2d uses patch size as stride, then flatten(2).permute(0,2,1) produces (N, spatial_tokens, vision_width). PosEmbedding.forward (pos_embedding.py:62) slices positions using x.shape[1] and adds the same positional table to every batch member. Neither operation removes axis 0. The 3-D convolution branch's unsqueeze(0) is not selected. [source; call_224eb333dab544d487eaa38d6d44baaf, call_da3bf170d3e04a4c9d833e7baa014242, call_ee72740f055b48319c34f29438cc6830, call_946b0ea8036a4f819830840f45519ddf]

Each TransformerBlock.forward (transformer.py:50) runs layer_norm1 → Attention → residual addition, then layer_norm2 → MLP → residual addition. No post-branch norms are configured for these vision blocks. LayerNorm.forward (layernorm.py:86) normalizes the last dimension, preserving N and sequence length. MLP.forward (mlp.py:64) delegates to fc1 Linear, tanh-approximate GELU and fc2 Linear, changing feature width but retaining leading dimensions. The final post-LayerNorm has the same batch-preserving behavior. [source; call_ee72740f055b48319c34f29438cc6830, call_c7db6293e625419d9376a75fe59c34fe, call_51e927f232dc4c53bbc1798e58e3abfb, call_cee4468764934cf9b8552c6b3881511c, call_946b0ea8036a4f819830840f45519ddf]

Attention.forward (attn.py:267) defaults to flash_attn_nc because ingestion supplies no attn_mode. causal=False controls masking, not dispatch. decode_flash_attn_nc (attn.py:378) projects Q/K/V, views them as (N, S, heads, head_dim), calls flash_attn_func with causal=False, then restores (N, S, query_width) before output projection. This is dense, equal-length attention: every item has the same S; there are no per-image lengths or padding masks. It neither requires N=1 nor uses a KV cache. Vision attention configures no RoPE or Q/K norms and retains the unrestricted-window and zero-softcap defaults. [source; call_1a15b53bcd8b44ac8eaaa3f64820c961, call_ee72740f055b48319c34f29438cc6830, call_70411f6c659e4c78a2fa81329e3dc122, call_946b0ea8036a4f819830840f45519ddf]

All attention and MLP Linear wrappers delegate to their loaded inner implementation. LinearFP16.forward saves x.shape[:-1], flattens batch and sequence into rows, multiplies, adds bias and restores the saved leading shape. LinearEXL3.forward likewise allocates its output with those leading dimensions. Its unchanged reconstruction crossover is more than 32 flattened rows, not more than 32 images. Attention's optional fused K/V path is limited to at most 32 flattened rows; its temporary view with leading 1 packs rows for the kernel and explicitly restores N and S afterward. [source; call_42700df4f1b2494c965b431212826656, call_7ae0d45eea7e4726bcf84978c5fb15fc, call_44eae4c4febb44d0a8305003bb7a794c, call_1a15b53bcd8b44ac8eaaa3f64820c961]

Gemma3MMPool.forward (gemma3.py:353) explicitly preserves bsz: it converts (N, P², C) to (N, C, P, P), average-pools with kernel and stride K=P//T, then returns (N, floor(P/K)², C). Here P=image_size//patch_size and T=int(sqrt(mm_tokens_per_image)); when the assumed divisibility holds, the token count is T². Despite its name, the local seq_length variable holds C. Pooling does not merge different images. [source; call_ee72740f055b48319c34f29438cc6830, call_946b0ea8036a4f819830840f45519ddf]

A standard-library scalar transcription checked 1,656 pooling index groups across N=1,2,3 and three divisible grid geometries. Every group remained within its own batch item and the derived output token count was T². This checks indexing arithmetic, not repository tensor execution. [execution; call_946b0ea8036a4f819830840f45519ddf]

Projector RMSNorm.forward (rmsnorm.py:69) allocates an output shaped like its input. Its native implementation multiplies all leading dimensions into the row count and normalizes each row independently; it checks feature divisibility by four and matching weight/output shapes, not a singleton batch. Final Linear then changes only the feature dimension. The inspected native hgemm accepts flattened 2-D matrices with matching dimensions and has no one-image constraint. [source; call_3fdefeb2e62a47e597290397c26fcb67, call_cbd91a5909a747e18349836a940bb963, call_42700df4f1b2494c965b431212826656, call_7ae0d45eea7e4726bcf84978c5fb15fc, call_661e89f5bdd448a0b56ad47f2584f0dc]

Consequently, under those existing shape preconditions, the final output is (N, pooled_tokens, projector_out_features), where Linear rounds its configured output width to its alignment. This agrees with the new shape[1] token count and embedding_tensor[i] extraction. Each extracted matrix matches MMEmbedding's documented (num_tokens, input_dim) contract; its -1 placeholders are replaced with separately allocated synthetic token IDs. [source; call_ee72740f055b48319c34f29438cc6830, call_42700df4f1b2494c965b431212826656, call_70411f6c659e4c78a2fa81329e3dc122, call_954021723a1a4aedbb2f3fb409cf36c7]

Singleton conventions remain at preprocessing's unsqueeze(0) and its shape comment, and at default_load_shape_dtype's leading 1. The former constructs one item before concatenation; the latter makes autosplit probe only one image's activation footprint. The old post-forward squeeze(0) is removed. The inspected active Python module path contains no remaining operation that forces the full image batch to one. [source; call_ee72740f055b48319c34f29438cc6830, call_70411f6c659e4c78a2fa81329e3dc122, call_bf93f2c556bd43ae854b0c39e8b5841e, call_1a15b53bcd8b44ac8eaaa3f64820c961]

Batching trades potentially fewer forward invocations for larger simultaneous activations. The unchanged example's per-image loop remains a supported lower-concurrency alternative. Neither a throughput gain nor the maximum usable batch size is established by this source inspection. [inference; call_70411f6c659e4c78a2fa81329e3dc122, call_d7eaf539ccc64f788b8c095a1cfaed97, call_bf93f2c556bd43ae854b0c39e8b5841e]

## Uncertainty and limits

No image preprocessing, PyTorch tensor operation, model loading, FlashAttention call or GPU kernel was executed. Source-level batch preservation does not establish numerical parity, backend compatibility, memory sufficiency or throughput improvement.

The scalar check models pooling indices only; it does not exercise tensor strides, floating-point averaging or CUDA execution.

The shape conclusion assumes the existing square-grid pooling and compatible loaded-weight preconditions. Checkpoint configurations and tensor headers were not independently validated in this inspection.

Native RMSNorm and hgemm implementations were inspected; the complete EXL3 native kernel chain and external FlashAttention implementation were not.
