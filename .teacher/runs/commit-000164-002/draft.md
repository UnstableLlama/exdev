# 966762a32d1eb2c0aa5e01b02451676bca6ca7fd


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/966762a32d1eb2c0aa5e01b02451676bca6ca7fd) · [Evidence ledger](draft.json)

Adds Gemma3 text-model registration and assembly, separates local/global RoPE configuration, and preserves vision tensors during compilation without implementing vision inference.

- [Gemma3 text assembly and component preservation](#models)

## Problem

The registry did not recognize Gemma3. Its nested text configuration, checkpoint namespace and local/global attention pattern require a dedicated adapter. [source; call_69cca3607afc420c880ea66d9842c18b, call_0ce81ed200e6422cb7f20de51383aebc, call_27d2297897b64655a9b89f49e5eece61]

## Reasoning

The change combines a Gemma2-like decoder with per-head Q/K normalization and separate local/global RoPE settings. Extending the shared RoPE reader is a prerequisite for reading nested global settings while deliberately isolating local attention from that scaling. [source; call_45b7e406dc58464faea408ee8c4d86cc, call_de57fe284431446dba1b56f46eb2e3c5, call_27d2297897b64655a9b89f49e5eece61]

## Impact

Gemma3ForConditionalGeneration becomes selectable through the existing configuration factory, with text as the default component. Vision inference remains unimplemented, but compilation can preserve the vision tower and multimodal projector tensors. [source; call_0ce81ed200e6422cb7f20de51383aebc, call_724414d2227f48a49aa519be35d8aece, call_051b4483066341e4ab7e3cfdaa3c9c2b, call_27d2297897b64655a9b89f49e5eece61, call_cd15a313b6a84dba90a587dbec3c001a]

## Source Notes

Read the introducing models chapter at 543c4b27714c6a677a6e714c452d62532f634cff and the component-interface entry at 830b6a018070a327d6d261628dff496f1303cf93. They establish the Gemma2 construction pattern and the named-component/compiler-hook interface reused here. The former records Gemma2's sliding_window_size mismatch; the latter records an incomplete Qwen3 MoE component migration. [ancestor; call_21203636ef8342dc99d6e7ca573e722b, call_c6a27687de5c42ffb3ef695a6ea035d2]

The new Gemma3 path reads text_config->sliding_window, rather than copying Gemma2's sliding_window_size lookup. Gemma2 itself is unchanged. The Qwen3 MoE interface mismatch also persists, as recorded separately in findings. [source; call_45b7e406dc58464faea408ee8c4d86cc, call_27d2297897b64655a9b89f49e5eece61, call_788828d6edef41e7b64dd374c86917f3, call_051b4483066341e4ab7e3cfdaa3c9c2b]

Issue #33, “Error converting model,” initially reports a compiler file-opening failure, subsequently identified as too many open files and reported resolved. It later tracks GLM4 generation trouble; Midaychi's final comment requests separated Gemma3 language/vision support. A relationship to this task is inferred from that exact architecture request and the component split, not an explicit upstream link or evidence that this commit fixes the original error. [inference; call_69f1bd6a0912444eaac6f3d9ddbf1897, call_f86975574fef45dba0fe03c996d8efe8, call_7aaa9585dd0e4ba39e05941ab05588f3, call_27d2297897b64655a9b89f49e5eece61]

Other discussions have only inferred path-based associations: PR #4, “chore: update config.py,” is a spelling correction; issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” and closed issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” concern extension installation/import failures through config.py and rope.py. Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?,” concerns dynamic scaling, unlike this adapter's fixed local/global settings. [inference; call_abd9abeeb30d439496349e0594cba825, call_d3371b6c805740aaa63210f373bacfa8, call_49a67a1b685045d58489a991e0fe10fc, call_e910e6ba3a844697b4a33ebef0654d8a, call_27d2297897b64655a9b89f49e5eece61]

PR #26, “Superior 3INST parameters,” discusses codebook alternatives and evaluation; issue #34, “torch._C._LinAlgError on last layer of quant,” reports Command-A quantization failures. Their associations are inferred solely from inspected evaluation/linear paths. Neither establishes a Gemma3 defect, performance result or motivation for this change. [inference; call_d0ca2e96957448d59a7e604877664d47, call_dd9876cbc610478fa10fcaa93c589853, call_eb71b23c614b4fbb8aa68d5d07da4cfc, call_a2489729455043d299ec6cfd46eb6212, call_9b138039d36e424ab199c07b7463434e, call_0fc43b586a104154814ab354c9523434]

<a id="models"></a>

## Gemma3 text assembly and component preservation

Registration uses Gemma3Config.arch_string = Gemma3ForConditionalGeneration. Config.from_directory selects it from the single architectures entry; Model.from_config defaults to the text component. The new mapping supplies both Gemma3Model and Gemma3VisionModel, but only the text class assembles executable modules. This does not register Gemma3ForCausalLM. [source; call_3208bceabb864ba78375da651462bb78, call_0ce81ed200e6422cb7f20de51383aebc, call_724414d2227f48a49aa519be35d8aece, call_051b4483066341e4ab7e3cfdaa3c9c2b, call_27d2297897b64655a9b89f49e5eece61]

Gemma3Config reads decoder dimensions, layer count, normalization and attention options under text_config. Layer count and the text_config dictionary are required. The base Config already searches both top-level and nested vocab_size; Gemma3 supplies 262208 only when neither yields a value. read_dict accepts integer-valued floating-point settings and treats null like an absent value, so explicit null softcaps select the adapter's zero defaults. [source; call_724414d2227f48a49aa519be35d8aece, call_604a94796d3c415a81232f943cb1539e, call_782bcde0e9374bfea6890729894d0a9c, call_27d2297897b64655a9b89f49e5eece61]

read_rope_settings_default gains optional theta, partial-rotation and source-dictionary arguments without changing its RopeSettings return form. None selects self.config_dict; an explicitly empty dictionary remains empty. Whole-tree search found ten existing callers: Cohere, Cohere2, DeciLM, Gemma2, GLM4, Llama, Mixtral, Phi3, Qwen3 and Qwen3 MoE. Each still supplies only its original RopeStyle and retains the previous defaults. No other read_cfg definition was found, so the replacement with read_dict bypasses no inspected subclass override. [source; call_de57fe284431446dba1b56f46eb2e3c5, call_3251a73b8011477995917b9ceb50028d, call_788828d6edef41e7b64dd374c86917f3, call_45b7e406dc58464faea408ee8c4d86cc, call_45bcb02350cd4f4894ab1e54f19148e3]

Global RoPE reads text_config with a default base of 1000000. Local RoPE reads an empty dictionary with base 10000, full rotation and no scaling. Both use NEOX style. These bases govern inverse frequencies, not context-length thresholds. For the reference configurations' linear factor 8, RoPE._rope_params_linear divides global inverse frequencies by eight; the local settings avoid that division. [source; call_27d2297897b64655a9b89f49e5eece61, call_de57fe284431446dba1b56f46eb2e3c5, call_3182aa72184b4da28cc653b61581817d, call_daa996e56c424d1c87d7718372f61f84, call_74e9e98f59164e22999625e3a431aeac, call_7b68986b1b924a6b83ec3a0ed103827f, call_8ffad3fae74340eaa3aef20f858b22a5]

bool((idx + 1) % sliding_window_pattern) selects local attention. With the default pattern 6, five local blocks precede each unrestricted block. Local blocks receive sliding_window and local RoPE; global blocks receive -1 and global RoPE. The adapter's fallback window is 4096, whereas every inspected reference configuration explicitly supplies 1024. Attention forwards these values to FlashAttention's window_size; its SDPA alternative asserts against nonnegative windows and therefore is not interchangeable for the ordinary Gemma3 pattern. [source; call_27d2297897b64655a9b89f49e5eece61, call_eb011aacc52d47c38c93c5e7468d2797, call_7a7cfd8f656c4b76b0224638cd20cd9e, call_61662475e4a0472088332d7e1e407e4a, call_35320a492e494a0ba8ae31e739a9e689, call_7d72a5e5e1f240b0b8e681aace83b99e]

The text sequence is language_model.model.embed_tokens, decoder blocks under language_model.model.layers.i, language_model.model.norm and language_model.lm_head. Embedding normalization multiplies activations by sqrt(hidden_size). Each block places input normalization before attention, post-attention normalization before its residual addition, pre-feedforward normalization before the GELU gated MLP, and post-feedforward normalization before its residual addition. All these RMSNorms use weight + 1; branch post-norms request float output. [source; call_27d2297897b64655a9b89f49e5eece61, call_ce498dd27c384f26ab3bd5c21a61585e, call_e0a98ecbca444e6b9f076f1532c48678, call_e8fcfccf934a4d62b790d7b7b45c4b09, call_a0a612bfdeae4a5faffb2a3c870ddc11]

Attention applies the supplied Q/K RMSNorms after reshaping projections into heads and before RoPE; their vectors therefore have head_dim elements, not hidden_size elements. FlashAttention receives query_pre_attn_scalar**(-0.5) as softmax_scale. The head always offers the embedding as an alternate tensor key, independently of the stored tie_word_embeddings flag. Linear first tries EXL3 storage, then ordinary weights; ordinary checkpoint matrices are transposed when loaded. [source; call_27d2297897b64655a9b89f49e5eece61, call_7a7cfd8f656c4b76b0224638cd20cd9e, call_c55a4bf8435943608518de30111155d1]

All eleven listed Gemma3 configurations were read. google/gemma-3-4b-it and google/gemma-3-4b-pt map to hidden/intermediate widths 2560/10240 and 34 layers; their omitted head settings use the adapter's defaults D=256, Q=8 and K=4. google/gemma-3-4b-it-qat-int4-unquantized and google/gemma-3-4b-it-qat-q4_0-unquantized explicitly supply those same head dimensions. Each supplies window 1024 and global linear scaling factor 8. The QAT files explicitly confirm vocabulary 262208, theta 1000000, local base 10000 and pattern 6; the compact IT/PT files rely on adapter defaults for those omitted values. [source; call_61662475e4a0472088332d7e1e407e4a, call_535d509ad1cc4bd1b5ee856c44c7b0cf, call_e78556794f0245edb3f45a856bbc6103, call_08f066b816fd478e844a6ace57ff03d3, call_27d2297897b64655a9b89f49e5eece61]

google/gemma-3-12b-it and google/gemma-3-12b-pt supply widths 3840/15360, 48 layers, Q=16 and K=8, using default D=256 and attention scalar 256. google/gemma-3-12b-it-qat-int4-unquantized and google/gemma-3-12b-it-qat-q4_0-unquantized explicitly confirm those settings. Each maps window 1024 and global linear factor 8. As for 4B, the QAT configurations explicitly provide the vocabulary, RoPE bases and pattern corresponding to the adapter defaults; their null softcaps map to zero. [source; call_35320a492e494a0ba8ae31e739a9e689, call_0fd081562dd546a18c33ad2b8052ff5c, call_cb11a59da918414fab93fbd8930d54c2, call_0b723a0a17514d5597ea1be38fbd33eb, call_604a94796d3c415a81232f943cb1539e, call_27d2297897b64655a9b89f49e5eece61]

google/gemma-3-27b-it, google/gemma-3-27b-pt and google/gemma-3-27b-it-qat-q4_0-unquantized each supply widths 5376/21504, 62 layers, D=128, Q=32, K=16 and attention scalar 168. Thus the adapter must honor explicit head_dim rather than derive it from hidden_size/Q. Each supplies window 1024 and linear factor 8. The QAT configuration explicitly confirms the same vocabulary, RoPE bases and pattern defaults and uses null softcaps. These configuration artifacts are hash-verified mirror files, not runtime compatibility tests. [source; call_7d72a5e5e1f240b0b8e681aace83b99e, call_9758ca3ac23140fda667ee37fef44e18, call_e661d91bb24a41a7964a6c2133a761fb, call_27d2297897b64655a9b89f49e5eece61]

The 4B IT headers contain all 34 layers' requested q_proj/k_proj/v_proj/o_proj, gate_proj/up_proj/down_proj, four block norms and Q/K norms, plus embedding and final norm. Shapes are Q [2048,2560], K/V [1024,2560], O [2560,2048], gate/up [10240,2560], down [2560,10240], block norms [2560] and Q/K norms [256]. Embedding is [262208,2560]. The text inventory has no separate language_model.lm_head.weight, optional linear biases or EXL3 groups, so the inspected loader selects ordinary weights and the embedding fallback for the head. [source; call_e7dbeb09f18745bd8cf0edfa763f2013, call_19f81bcbdfd44a31b3fa007a7e402675, call_f8d82d8ee12343d491499bc9df2ee353, call_c55a4bf8435943608518de30111155d1, call_27d2297897b64655a9b89f49e5eece61]

First-layer header samples also match the configured projection dimensions for 12B and 27B. For 12B, Q/K/O are [4096,3840], [2048,3840], [3840,4096], with gate/up [15360,3840], down [3840,15360] and Q/K norms [256]. For 27B they are [4096,5376], [2048,5376], [5376,4096], [21504,5376], [5376,21504] and [128]. Their sampled embeddings are [262208,3840] and [262208,5376]. All sampled tensors are BF16. [source; call_2aa89261e1da42d4abdeef7aa915d0ae, call_4b8e1f43748f4c73a0be3eb458446dcc, call_27d2297897b64655a9b89f49e5eece61]

A scalar transcription of the layer-selection formula yields 29 local/5 global blocks for 4B, 40/8 for 12B and 52/10 for 27B. Global zero-based indices start at 5 and advance by six. Dimension arithmetic matches the sampled projection shapes; attention scales evaluate to 0.0625 for 4B/12B and approximately 0.077151675 for 27B. Separately, executing the repository read_dict utility confirmed that a null floating-point key returns the supplied zero default. [execution; call_c9561144c34c4d56be689f103ba60506]

Gemma3Model.prepare_inputs follows every inspected existing architecture caller: retain input_ids in params and call prepare_for_attn with the same arguments. That helper retains its existing backend/cache checks. The new Q/K normalization similarly uses Attention's existing paired-norm mechanism; both norms are supplied, satisfying its assertion. [source; call_5ff48970d4eb4b69a5be957b11b4cb9f, call_0fc43b586a104154814ab354c9523434, call_7a7cfd8f656c4b76b0224638cd20cd9e, call_27d2297897b64655a9b89f49e5eece61]

The vision class is a preservation hook, not a vision forward implementation: load and unload raise NotImplementedError. Its static hook unions list_tensors results for vision_tower and multi_modal_projector. The prior list_tensors caller in quantization metadata passes a module prefix with the same exact-or-dot-descendant semantics; the new calls retain its assertion against active new_tensors. compile_model invokes hooks on all configured classes without instantiating vision, then copies returned tensors from config.stc with BF16 allowed. The 4B header includes mm_input_projection_weight [1152,2560], mm_soft_emb_norm.weight [1152] and vision-tower tensors that the text forward path never consumes. [source; call_27d2297897b64655a9b89f49e5eece61, call_cd97aed8cc224d729b0a911f68e7908f, call_eb80998def40401fad2751696f22d0b7, call_0797ccaa5e13451ba6893d3d3fcef7a0, call_66e532f59b66442581a225e8f9c573c8, call_cd15a313b6a84dba90a587dbec3c001a, call_19f81bcbdfd44a31b3fa007a7e402675]

Preserving those additional tensors appears intended to avoid making text-only conversion discard the future multimodal components. This interpretation follows the component hook and copied namespaces; it does not establish implemented multimodal inference or an explicit author rationale. [inference; call_27d2297897b64655a9b89f49e5eece61, call_cd15a313b6a84dba90a587dbec3c001a]

## Authoring-time findings — pending review

### inherited-qwen3-moe-component-interface (suspected; defect)

The previously recorded Qwen3 MoE component-interface mismatch is carried over unchanged; the shared RoPE-reader extension does not repair it.

Trigger: Pass an otherwise valid Qwen3MoeConfig to Model.from_config, or independently reach compile_model's additional-tensor block with that configuration.

Expected: Select the text model and enumerate component compilation hooks.

Actual: Qwen3MoeConfig still passes the bare Qwen3MoeModel class, which Config stores as model_classes. The factory applies membership testing to that class, and compilation expects .items(). These operations cannot consume the stored form. Direct callers include conversion/get_base_model, quantization metadata construction, model_init, evaluation, examples and tests; the inspected calls omit component. Fixed-model examples are affected only if supplied such a configuration, not merely by this Gemma3 addition.

Locations: 966762a32d1eb2c0aa5e01b02451676bca6ca7fd:exllamav3/models/qwen3_moe.py — Qwen3MoeConfig.__init__, 966762a32d1eb2c0aa5e01b02451676bca6ca7fd:exllamav3/models/model.py — Model.from_config, 966762a32d1eb2c0aa5e01b02451676bca6ca7fd:exllamav3/conversion/compile.py — compile_model

Source evidence: call_788828d6edef41e7b64dd374c86917f3, call_724414d2227f48a49aa519be35d8aece, call_051b4483066341e4ab7e3cfdaa3c9c2b, call_cd15a313b6a84dba90a587dbec3c001a, call_6806aefd8cf14902a2eabba66fe0042f, call_0fc43b586a104154814ab354c9523434

source_inspection: Compared parent constructors, factory and compiler with all three task-diff sections; searched the whole parent tree for factory callers and inspected their surrounding code. [call_788828d6edef41e7b64dd374c86917f3, call_051b4483066341e4ab7e3cfdaa3c9c2b, call_cd15a313b6a84dba90a587dbec3c001a, call_6806aefd8cf14902a2eabba66fe0042f, call_0fc43b586a104154814ab354c9523434, call_0ce81ed200e6422cb7f20de51383aebc, call_de57fe284431446dba1b56f46eb2e3c5, call_27d2297897b64655a9b89f49e5eece61]. Limits: No Qwen3 MoE configuration or model was instantiated. This is an inherited observation, not a regression attributed to Gemma3.

## Uncertainty and limits

No Gemma3 model loading, conversion, GPU inference, output-equivalence testing or performance measurement was performed.

Tensor validation covers the 4B text tensor inventory and first-layer/embedding samples for 12B and 27B. Remaining 12B/27B layers, final norms, alternate names and optional tensor absence were not exhaustively checked; QAT and pretrained variants received configuration checks, not separate header validation.

The scalar checks use Python integers and double-precision arithmetic, not BF16/FP16 tensors or CUDA kernels. The successful read_dict check executes only that repository utility.
