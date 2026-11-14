# c44e56c73b2c67eee087c7195c9093520494d3bf


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c44e56c73b2c67eee087c7195c9093520494d3bf) · [Evidence ledger](draft.json)

Adds Glm4ForCausalLM registration and a shared-module decoder with four norms per block, GPTJ rotary settings and selected FP32 branch outputs. All three indexed GLM4 configurations were inspected; runtime compatibility remains untested.

- [GLM4 configuration and decoder composition](#models)

## Problem

GLM4 checkpoints need an architecture registry entry and a constructor expressing their normalization, projection and rotary-position layout. [source; call_d2f199a5de2149de859feeb25279e582, call_ae1bbfd8361e46898f3ad771b7d8b4cd]

## Reasoning

The implementation composes existing modules rather than introducing GLM-specific kernels. Registry lookup in Config.from_directory now selects Glm4Config, which supplies Glm4Model. [source; call_d2f199a5de2149de859feeb25279e582, call_63b00422ed69474c98a8cb27eb7953a2, call_ae1bbfd8361e46898f3ad771b7d8b4cd]

## Impact

The change makes Glm4ForCausalLM discoverable through normal configuration loading; registration alone does not establish successful checkpoint loading or generation. [source; call_d2f199a5de2149de859feeb25279e582, call_63b00422ed69474c98a8cb27eb7953a2]

## Source Notes

The parent already contains a chat-template description for ChatGLM(4), distinct from the architecture registration added here. [source; call_cb1421d86ec74503ab64d10b831d43ff]

Inspected discussions have different framing: issue 7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure; issue 15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerns low-bitrate quantization; PR 4, “chore: update config.py,” proposes a spelling correction. None reports GLM4 execution. [source; call_959a62639200473a9a952de62ea3f77a, call_596cf785bfc2406e9af87f71e39c0b63, call_10f9f04883e04bb984e8079e6532a170]

<a id="models"></a>

## GLM4 configuration and decoder composition

Glm4Config reads head and layer dimensions, requires normalization epsilon and intermediate width, accepts absent hidden_act but rejects a present value other than silu, defaults KV heads to query heads and tied embeddings to false, and derives a missing or zero head_dim as hidden_size // num_attention_heads. [source; call_ae1bbfd8361e46898f3ad771b7d8b4cd, call_63b00422ed69474c98a8cb27eb7953a2, call_1b584a7952674089b3f163142aa1beb7]

Each block performs input RMSNorm → attention → post_self_attn_layernorm → residual addition, followed by post_attention_layernorm → gated MLP → post_mlp_layernorm → residual addition. TransformerBlock explicitly requests FP16 from both input norms; GLM4 requests FP32 from both post-norms and the MLP output, while retaining FP16 gate/up intermediates. Residual additions remain in place on x. [source; call_ae1bbfd8361e46898f3ad771b7d8b4cd, call_37fd8a400d2a467686c5f132e92530a1, call_f024acb197be4c4688f255fd7f937778]

Attention maps separate q_proj, k_proj, v_proj and o_proj keys under each self_attn prefix. The gated MLP maps gate_proj/up_proj/down_proj and additionally supports gate_up_proj through contiguous gate-first, up-second slices. Its fused-key option prohibits intermediate slicing above the inherited 55,296-wide limit, documented as a practical single-GPU quantization limit. [source; call_ae1bbfd8361e46898f3ad771b7d8b4cd, call_0ec99ef30c1e4c8bbfd9d3f928fb2d93, call_f024acb197be4c4688f255fd7f937778, call_ed3407075ddc492388eb76e9faa46d0b, call_24aacdb56f0549c49f92d1c06b91e212]

GLM4 selects GPTJ rotary style through the existing settings reader. That reader preserves partial_rotary_factor and rope_theta; the default frequency builder uses dim = int(head_dim * partial_rotary_factor) and inverse frequencies theta^(-2j/dim). Attention calls the native-backed RoPE.apply path, not apply_torch. [source; call_ae1bbfd8361e46898f3ad771b7d8b4cd, call_63b00422ed69474c98a8cb27eb7953a2, call_f5b16af16570431ea52e5fd5e7d290d0, call_0ec99ef30c1e4c8bbfd9d3f928fb2d93]

zai-org/GLM-4-32B-0414 declares hidden width 6144, 48 query heads, 2 KV heads, 61 layers and intermediate width 23040. Separately, zai-org/GLM-4-32B-Base-0414 declares the same values. zai-org/GLM-4-9B-0414 instead declares width 4096, 32 query heads, 2 KV heads, 40 layers and intermediate width 13696. All three declare the registered architecture, head_dim 128, SiLU, epsilon 1e-5, untied embeddings, rotary factor 0.5 and theta 10000; their explicit values agree with the constructor's configuration mapping. [source; call_fd091dec118344b7aa20e540b933dc95, call_c2bb36555c7549c590939b1f61bfa1d5, call_e8de9896e873472aa272c9e97c8715d6, call_ae1bbfd8361e46898f3ad771b7d8b4cd]

A scalar transcription gives Q widths 6144 for each 32B model and 4096 for 9B, with K/V widths 256 for all three. Each has 64 rotary channels and 32 frequencies. Fused gate/up widths are 46080, 46080 and 27392 respectively; each intermediate width fits the inherited unsliced-MLP limit. [execution; call_add4e58dea604dcd9326a8161672f7d4]

The two 32B configurations disable attention_bias, whereas 9B enables it. Glm4Config does not branch on that flag: the shared Linear loader reads optional per-projection bias tensors. Consequently the flag difference alone is not evidence that the 9B bias is omitted. [source; call_fd091dec118344b7aa20e540b933dc95, call_c2bb36555c7549c590939b1f61bfa1d5, call_e8de9896e873472aa272c9e97c8715d6, call_ae1bbfd8361e46898f3ad771b7d8b4cd, call_ed3407075ddc492388eb76e9faa46d0b]

The surrounding model sequence is model.embed_tokens, indexed decoder blocks, FP16-output model.norm and lm_head. The output head can fall back to embedding weights when configured as tied. prepare_inputs stores the original IDs and delegates to existing attention preparation, whose default is uncached FlashAttention; cached preparation retains its existing cache-capacity, position and page-alignment requirements. [source; call_ae1bbfd8361e46898f3ad771b7d8b4cd, call_0ec99ef30c1e4c8bbfd9d3f928fb2d93]

## Uncertainty and limits

No repository model execution, checkpoint loading, conversion or GPU testing was performed. The executed check transcribed integer shape arithmetic only.

Checkpoint configuration compatibility was inspected for all three indexed GLM4 models, but tensor names and stored shapes were not verified against tensor headers.

The reason for choosing FP32 branch outputs is not documented in the inspected evidence; numerical-quality or performance benefits remain unmeasured.
