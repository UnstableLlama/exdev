# 6aa1449169a7076d61223fcf74b4e6ceb849327d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6aa1449169a7076d61223fcf74b4e6ceb849327d) · [Evidence ledger](draft.json)

Registers MiMoForCausalLM through thin Llama-derived classes, matching the inspected reference configurations and Base tensor layout while deliberately ignoring MTP tensors.

- [MiMo dispatch through the existing Llama decoder](#models)

## Problem

The parent registry does not recognize MiMoForCausalLM, so Config.from_directory rejects that architecture before model construction. [source; call_b667d5bae8644f8ba3f6ecf32e2f1d41, call_b3545801d07748f39d651248f60b35c2]

## Reasoning

The change adds a thin Llama-derived adapter and registers it. Reusing the existing construction avoids a separate implementation of the ordinary decoder; the explicit tradeoff is leaving MTP layers unused. [source; call_6b902011e50c414bbb17d791f7d8422c, call_203f91f3039048fe92c63e666da90779, call_9f5c3e14b0b54f838838d38f1c6f18ab]

## Impact

Directory dispatch can now select MiMoConfig, whose text component constructs MiMoModel. This establishes the configuration and construction route, not measured inference correctness. [source; call_6b902011e50c414bbb17d791f7d8422c, call_203f91f3039048fe92c63e666da90779, call_b3545801d07748f39d651248f60b35c2, call_df72981899454a42a70a58309d074416]

## Source Notes

The introducing models chapter and the architecture-metadata and component-selection entries were read. They establish the inherited Llama mapping, class-owned registration metadata and named-component interface. [ancestor; call_5a54f14a59b345d5a82098a21d2e5501, call_dece70ee28214da993753b8c734ea43e, call_cb23e22b5d97455497aad466fdf96027]

The metadata entry's undefined expect_arch diagnostic is no longer present in the inspected parent: Config.__init__ formats self.arch_string instead. The MiMo diff does not change that corrected code. [source; call_b3545801d07748f39d651248f60b35c2, call_6b902011e50c414bbb17d791f7d8422c, call_203f91f3039048fe92c63e666da90779]

Discussion overlap is inferred from inspected paths, not an upstream link to this change. PR #4, “chore: update config.py,” proposes a spelling correction. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading and an environment workaround. Issue #33, “Error converting model,” tracks file-opening failure and later GLM4 generation trouble. Issues #34 and #42 report quantization factorization failures; PR #26, “Superior 3INST parameters,” concerns codebook parameters. None supplies MiMo-specific validation. [inference; call_6d7a7f56e4a0408985f7afbfab579c74, call_58afbaf27439499cb3fdfa9887ce766c, call_0c7d84fb261e406cbe77666d2ee7b7ba, call_1d69e6345811486c9c3eba367ef0977e, call_37cdaf1687594ba78aa26bdf681d4bcb, call_3943e5d5f6644e999c59878b99148f28, call_602bfd53ca17432698591c948f66353a, call_fff9fd7bad5c4a88895919166db9b920]

<a id="models"></a>

## MiMo dispatch through the existing Llama decoder

The registry derives its architecture/config/model records from model-class attributes. Adding MiMoModel therefore creates the MiMoForCausalLM entry through MiMoModel.config_class = MiMoConfig and MiMoConfig.arch_string. Registration and the new classes are complementary: Config.from_directory selects the config, while Model.from_config selects its text component. [source; call_b667d5bae8644f8ba3f6ecf32e2f1d41, call_6b902011e50c414bbb17d791f7d8422c, call_203f91f3039048fe92c63e666da90779, call_b3545801d07748f39d651248f60b35c2, call_df72981899454a42a70a58309d074416]

MiMoConfig forwards derived_model={"text": MiMoModel} into LlamaConfig; MiMoModel delegates construction unchanged to LlamaModel. Existing MistralConfig and Qwen2Config use the same override pattern, with no additional guards or argument preparation omitted by MiMo. Config stores the mapping verbatim; both Model.from_config and compile_model's component-hook iteration accept this dictionary form. [source; call_203f91f3039048fe92c63e666da90779, call_9f5c3e14b0b54f838838d38f1c6f18ab, call_d948162cd7f74716abe50067a941df7e, call_212af8d4a52d44a6aed55f87e2294bb0, call_cc5754aaeb604c469b520d5b57df470f, call_b02489911776484294d100644572ee27, call_df72981899454a42a70a58309d074416, call_1ec449fb27164c1a977df7571a87a2bc]

The inherited decoder constructs model.embed_tokens, 36 model.layers.i blocks, model.norm and lm_head for the reference configurations. Each block uses input_layernorm, separate q_proj/k_proj/v_proj/o_proj attention projections, post_attention_layernorm and gate_proj/up_proj/down_proj MLP projections. prepare_inputs retains the input IDs and invokes the shared attention preparation mechanism; there is no MiMo-specific forward implementation. [source; call_203f91f3039048fe92c63e666da90779, call_9f5c3e14b0b54f838838d38f1c6f18ab, call_d0ad27171eb14676879a34da23c61d28, call_877612bba7a4495688c2cb94ff8bd1bb, call_e5fbe8a85e614ffc97c0a9cb871c8f4e]

All five inspected XiaomiMiMo configurations—MiMo-7B-Base, MiMo-7B-RL, MiMo-7B-RL-0530, MiMo-7B-RL-Zero and MiMo-7B-SFT—declare the new identifier and agree on hidden width 4096, intermediate width 11008, 36 layers, 32 query heads, eight KV heads, explicit head width 128, SiLU, RMS epsilon 1e-5, theta 640000 and untied embeddings. Thus each fits the inherited dimensional mapping without using the missing-head-width or missing-KV-head defaults. [source; call_e5fbe8a85e614ffc97c0a9cb871c8f4e, call_64c62fc64166484093ec2088a7573974, call_bbe039d6ff8f4fc3b2a11371a6e8303d, call_09253f45d00045119c8ffd2115e90a92, call_3e0611600f1a4238982117ba2db89c53, call_9f5c3e14b0b54f838838d38f1c6f18ab]

Base, RL, RL-Zero and SFT supply a 32768-position limit; RL-0530 supplies 65536 and null rope_scaling. The shared RoPE reader propagates these limits and theta using NEOX style. All five disable sliding-window attention, consistent with LlamaModel not supplying a window. RL and SFT explicitly supply BOS/EOS IDs, whereas Base and RL-Zero omit them and receive Config's None defaults; RL-0530 also supplies them. [source; call_e5fbe8a85e614ffc97c0a9cb871c8f4e, call_64c62fc64166484093ec2088a7573974, call_bbe039d6ff8f4fc3b2a11371a6e8303d, call_09253f45d00045119c8ffd2115e90a92, call_3e0611600f1a4238982117ba2db89c53, call_b3545801d07748f39d651248f60b35c2, call_9f5c3e14b0b54f838838d38f1c6f18ab]

Across all four Base headers, the requested ordinary weights exist: embedding/head [151680,4096], Q/O [4096,4096], K/V [1024,4096], gate/up [11008,4096], down [4096,11008], and norm vectors [4096]. Q/K/V biases have widths 4096/1024/1024. Linear.load_fp16 detects these biases directly, transposes checkpoint matrices, and permits absent biases and weight_scale_inv; O, MLP and head biases and scale tensors are absent. The untied head exists, so the embedding alternate is unnecessary; separate projections exist, so fused-weight fallback is unnecessary. [source; call_abbe7a1183344e05a1e25cdd7ea1377e, call_c140a19fabef4811ad833de7423c8429, call_34504703a94443f9996b5c35d5a7e6f6, call_eef3eb74b02e46f5aeb5026504bbce77, call_9ef27f408b114a2c9787e48e81367711, call_9f5c3e14b0b54f838838d38f1c6f18ab]

“No MTP yet” is implemented by omission, not by a runtime flag. The adapter never reads num_nextn_predict_layers and constructs no model.mtp_layers modules. Base and RL-0530 final-shard headers contain 16 such tensors: five norm vectors, input_proj [4096,8192], three MLP matrices and seven attention weight/bias tensors. Those stored tensors are outside the inherited decoder's requested names. [source; call_203f91f3039048fe92c63e666da90779, call_9f5c3e14b0b54f838838d38f1c6f18ab, call_eef3eb74b02e46f5aeb5026504bbce77, call_42de2152b8534ac18572a8d01aa08781]

A standard-library metadata calculation reproduced projection dimensions, four query heads per KV head, 39 top-level modules and 435 ordinary tensors. Adding the 16 ignored MTP tensors yields 451, matching the four Base header counts. All matrix dimensions are multiples of Linear's 128-element padding unit. This is scalar metadata validation, not model execution. [execution; call_d21232be41f548f68fcb99d0f296b6f9]

## Uncertainty and limits

No package import, checkpoint loading, conversion, GPU execution, output-equivalence test or performance benchmark was run.

Complete tensor headers were inspected for MiMo-7B-Base; only the final shard was inspected for RL-0530. RL, RL-Zero and SFT comparisons establish configuration compatibility, not complete tensor inventories.

The Python calculation checks transcribed metadata with integer arithmetic; it does not execute repository model code or test BF16/FP16 numerics.
