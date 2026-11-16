# 532d78658414d8f9aabce52cb64b982b3ec53388


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/532d78658414d8f9aabce52cb64b982b3ec53388) · [Evidence ledger](draft.json)

Implements Gemma3's vision component, from normalized images through pooled vision features to synthetic-token embeddings, while adding mandatory vision preprocessing configuration.

- [Gemma3 image-to-token embedding pipeline](#models)

## Problem

Gemma3's vision component previously contained load/unload stubs. This change supplies image preprocessing, a vision tower and projection into text-model embedding space. [source; call_99741885323c4ebdad7d1f1e30f8f002]

## Reasoning

The implementation connects existing convolution, positional embedding, attention and MLP modules rather than adding a separate execution engine. Configuration parsing, module assembly and the image-shaped autosplit input are mutually supporting parts of that integration. [source; call_99741885323c4ebdad7d1f1e30f8f002, call_47a15fac148f483b8bb60649800b7506]

## Impact

Gemma3Config now unconditionally requires vision dimensions and preprocessor_config.json, including an asserted Gemma3ImageProcessor type. These requirements apply when constructing the conditional-generation configuration even if the caller selects its text component. The separate Gemma3TextConfig is not changed. [source; call_99741885323c4ebdad7d1f1e30f8f002, call_47a15fac148f483b8bb60649800b7506]

## Source Notes

The Gemma3 introduction entry was read: it establishes the earlier text implementation and explicitly unfinished vision component. The vision-helper entry was also read: it records that pixel rescaling and integration were previously caller responsibilities. [ancestor; call_f4784c8810c8487a90f74e65f70c94a2, call_879c8faa36da47ab8288e80e37043eda]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and a reporter-provided environment workaround. Its relationship here is only an inferred shared model.py path, not evidence of a vision-model failure or a fix in this change. [inference; call_20d0986976fc477e95eab139a404f412, call_99741885323c4ebdad7d1f1e30f8f002]

<a id="models"></a>

## Gemma3 image-to-token embedding pipeline

Preprocessing converts transparency onto white through convert_to_rgb, resizes once, converts pixels to float32, applies the configured rescale factor, then channelwise (image − mean) / std. Only afterward does it transpose channels first and create a half-precision tensor with a leading batch dimension. Rescaling before normalization supplies the value-scale preparation the existing helper does not perform. [source; call_99741885323c4ebdad7d1f1e30f8f002, call_da03695ac8ca4ed2810c93286e0c5604]

Conv uses patch size as convolution stride and returns flattened spatial tokens. PosEmbedding adds consecutive learned position vectors from index zero. The tower then uses pre-attention and pre-MLP LayerNorm, attention without RoPE, and ordinary fc1/GELU/fc2 MLPs. The selected GELU implementation uses the tanh approximation; pad_to=1 preserves the checkpoint's unaligned intermediate width. [source; call_99741885323c4ebdad7d1f1e30f8f002, call_740f84e5344e4acb855b54ce06630df9, call_2bb4a18850384696ae626220f6fd1c79, call_59647c70cc01484681a0dc42da9baa29]

get_image_embeddings invokes the inherited sequential forward with causal=False. Attention defaults to the no-cache FlashAttention path, which passes that flag to flash_attn_func. It does not select the cache-bearing decoder. The existing SDPA alternative rejects sliding windows and softcaps, neither of which this tower configures. [source; call_99741885323c4ebdad7d1f1e30f8f002, call_47a15fac148f483b8bb60649800b7506, call_7d66692fb1e1466fa15bd7cfc2a11f3d]

After post-LayerNorm, Gemma3MMPool reshapes tokens into a spatial grid and average-pools nonoverlapping neighborhoods. RMSNorm with constant_bias=1 follows, then a linear projection to text hidden width. The projector explicitly requests transposed_load=False. The pool has no weights and no loading work. [source; call_99741885323c4ebdad7d1f1e30f8f002]

All eleven inspected conditional-generation configurations specify the same vision geometry: width 1152, intermediate width 4304, 16 attention heads, 27 layers, image side 896, patch side 14 and 256 image tokens. This holds individually for google/gemma-3-4b-it, google/gemma-3-4b-pt, google/gemma-3-12b-it, google/gemma-3-12b-pt, google/gemma-3-27b-it and google/gemma-3-27b-pt. Their projector output widths are respectively 2560, 2560, 3840, 3840, 5376 and 5376. [source; call_9a8fccb3b9df410587a75a024ccac693, call_0a925d399669437ebdf7ccee7a27b52b, call_8257be1a4dd5483bbb885ff0f891fea7, call_a578415257334e0c8cf073d4f76a0ef7, call_b60591316b8c49068f8ea9904459bc87, call_cee7548a5ce74dbaa34b140326c9b994, call_99741885323c4ebdad7d1f1e30f8f002]

The same vision dimensions hold individually for google/gemma-3-4b-it-qat-int4-unquantized, google/gemma-3-4b-it-qat-q4_0-unquantized, google/gemma-3-12b-it-qat-int4-unquantized, google/gemma-3-12b-it-qat-q4_0-unquantized and google/gemma-3-27b-it-qat-q4_0-unquantized; their text widths are 2560, 2560, 3840, 3840 and 5376. These five explicitly specify three channels, LayerNorm epsilon 1e-6 and tanh GELU, agreeing with the implementation's fixed choices. All eleven omit vision KV-head count and head dimension, so the adapter defaults them to 16 and 1152/16 rather than using text-attention dimensions. [source; call_9835266bd9244ceba3ca4e5f8ada00bd, call_0526c190d1ed48b587579fea857e1886, call_1333953733be4139bdffdc1796912100, call_2f2c2c46b68d48f7a616d6e621fda7d9, call_be77a8a1c626457ba169df19a28a9952, call_99741885323c4ebdad7d1f1e30f8f002]

A standard-library arithmetic transcription gives head dimension 72, a 64×64 patch grid containing 4096 tokens, and a 4×4 pooling kernel producing 16×16 = 256 tokens. Adding the image boundary tokens gives a 258-token representation. It also shows that ordinary 128-alignment would round intermediate width 4304 to 4352, explaining the practical significance of pad_to=1. [execution; call_5501d8bd6a4a466c86f64ec0ec9879f9]

The final image vectors move to CPU and lose the singleton batch dimension. The method surrounds one -1 placeholder per vector with tokenizer IDs for <start_of_image> and <end_of_image>, then constructs MMEmbedding. That container replaces placeholders with allocated synthetic IDs and stores the original vectors and alias. The new method adds original size, preprocessed size and architecture metadata; no existing literal MMEmbedding constructor call was found in the parent tree. [source; call_99741885323c4ebdad7d1f1e30f8f002, call_b199b575b7f0416fa2160d86b76c5bdf, call_8702d1966214415aa9413821acbdb980]

The autosplit override supplies a half-precision (1, channels, height, width) probe instead of integer token IDs. Model._load_autosplit consumes this hook before forwarding through modules, so this edit enables the convolution-first assembly to participate in the existing memory-probing loader. [source; call_99741885323c4ebdad7d1f1e30f8f002, call_47a15fac148f483b8bb60649800b7506]

## Uncertainty and limits

No model loading, image-library operation, tensor operation or GPU inference was executed. The computation checks integer shape arithmetic only.

Checkpoint configuration agreement does not establish numerical parity or weight-layout compatibility; tensor headers and preprocessor configuration files were not inspected.

Pooling assumes a square patch grid and suitable divisibility by the requested token-grid side. Nonstandard configurations and rectangular preprocessing sizes were not validated.

Whole-tree compatibility inspection was incomplete for configuration consumers and inherited module interfaces.
