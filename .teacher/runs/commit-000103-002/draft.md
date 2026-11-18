# 0ff9fd2e39f6307e54358fd1a48a50b5cf7307f8


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/0ff9fd2e39f6307e54358fd1a48a50b5cf7307f8) · [Evidence ledger](draft.json)

Adds Cohere2 dispatch and parallel-decoder assembly with repeating local rotary/global nonrotary attention, supported by optional RoPE in all attention routes.

- [Cohere2 assembly and interleaved attention](#models)

## Problem

The registry lacked Cohere2ForCausalLM. The change adds its configuration/model pair and permits attention layers without rotary embeddings. [source; call_57c4f951b3e94174a9339c9362d99fa6, call_35bc219f7301425c85fe61d55b984536, call_3d8703bd45664c7694401f6f24b7f39e]

## Reasoning

Cohere2 reuses Cohere's shared-normalization parallel decoder, but assigns local rotary attention and global nonrotary attention by layer index. The optional-RoPE changes are therefore a prerequisite for the new model, not an independent cleanup. [source; call_35bc219f7301425c85fe61d55b984536, call_3d8703bd45664c7694401f6f24b7f39e, call_40a35d13395448d78782a0d3efd4100c]

## Impact

Config.from_directory can select Cohere2Config, which supplies Cohere2Model to Model.from_config. This establishes architecture dispatch and assembly, not successful checkpoint loading or numerical equivalence. [source; call_57c4f951b3e94174a9339c9362d99fa6, call_35bc219f7301425c85fe61d55b984536, call_33b167b5dccc4930b5bbb21f7bbf37f7, call_9d61852f97fa4f2fa0fa5f71a7d116de]

## Source Notes

Read the earlier Cohere architecture, shared-Hessian, class-owned registry and initial modules entries. They establish the reused parallel-block composition, calibration-label convention, registration interface and earlier rotary limitations. [ancestor; call_561f9e67de224d908a00368bfe62f00d, call_04e03db0d0ba48b1afd6ba0956059d69, call_9bff06e8d11a4df78ba9b8e718e2ad4e, call_3592d8b803f241ba9baef3fe87b34c2b]

The initial modules entry's unfinished native GPTJ branch is no longer present in the parent: rope_kernel implements adjacent-channel GPTJ rotation. Its partial-frequency bounds concern persists, as recorded in the finding. The Torch alternative still carries its GPTJ/partial-rotation TODO and is not selected by Attention. [source; call_44de8111904e4c878b5e05cae9012f7f, call_cbd72311343c4dcd97348661ab53cd11, call_362c69f2873848e7b15fc40d238f66a0, call_3d8703bd45664c7694401f6f24b7f39e]

The earlier Cohere entry records an unsupported Q/K-normalization requirement for Command R Plus configurations. This task leaves the attention TODOs unchanged; none of the three inspected Cohere2 configurations declares use_qk_norm, so that earlier observation does not establish such a requirement for these references. [inference; call_561f9e67de224d908a00368bfe62f00d, call_362c69f2873848e7b15fc40d238f66a0, call_ce550ad2778143519dd21fb70d0a03e4, call_d90cfefb149c4c6384efe5e33c315511, call_81fa201d8f414e24b0cc65c1cbef3991]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading and a compiler/environment workaround. Its connection here is inferred only from traceback lines matching the inspected Config and RoPE imports. PR #4, “chore: update config.py,” proposes “containg -> containing”; its inferred overlap is that unchanged Config docstring, not this architecture addition. [inference; call_bb1786415f7c4c87b958cd55d40eb90a, call_3d597aba085441fca41b99395aaf72d7, call_33b167b5dccc4930b5bbb21f7bbf37f7, call_cbd72311343c4dcd97348661ab53cd11]

The other inspected failure reports are “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” concerning quantization regularization, and “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” concerning compilation. Neither discussion identifies this architecture change as its remedy. [source; call_3cea3d0bb81a46129553292fe45c38dc, call_a5335711b8274d67a0d97d3951b665d7]

<a id="models"></a>

## Cohere2 assembly and interleaved attention

Cohere2Config declares arch_string=Cohere2ForCausalLM, Cohere2Model declares config_class, and the registry adds that model to its explicit list. The new config requires hidden width, query-head count, intermediate width and layer count; KV heads default to query heads, while a missing or false head_dim falls back to hidden_size // num_attention_heads. [source; call_57c4f951b3e94174a9339c9362d99fa6, call_35bc219f7301425c85fe61d55b984536, call_33b167b5dccc4930b5bbb21f7bbf37f7]

The new keys are sliding_window, default -1, and sliding_window_pattern, default 1. order_of_interleaved_layers must be present and equal local_attn_first. Parent searches found no interleaved-order consumer; the existing Gemma2 mapping instead reads sliding_window_size. The new Cohere2 spelling is supported by all three inspected reference configs rather than inferred from Gemma's helper name. [source; call_35bc219f7301425c85fe61d55b984536, call_8c2acf045ba748078e0352c4a74a91b9, call_7229e13aa3ee46b89bfed6d9f523cffa, call_9228ea6fc20b4de6a806f90653cecdc7, call_ce550ad2778143519dd21fb70d0a03e4, call_d90cfefb149c4c6384efe5e33c315511, call_81fa201d8f414e24b0cc65c1cbef3991]

For zero-based layer idx, the constructor uses the configured window unless (idx+1) is divisible by the pattern, when it uses -1. A nonnegative assigned window also enables GPTJ RoPE; a negative window supplies rope_settings=None. Thus the two choices are coupled: these global layers omit rotary position encoding, rather than merely enlarging the local window. [source; call_35bc219f7301425c85fe61d55b984536]

Scalar transcription with window 4096 and pattern 4 produced [4096,4096,4096,-1] repeatedly. Command A's 64 layers give 48 local and 16 global layers; each 32-layer R7B gives 24 local and eight global layers. Pattern 1 produces only global layers even with window 4096, and a missing window also leaves every layer global. [execution; call_d6a770d0e2b24f47908a701c0ed6a114, call_b7d3a793ecb94170ba711ffb25658bfd]

Attention already initializes self.rope=None and resets it on unload. The patch conditionally constructs RoPE during load and guards its application in all three decode routes. Previously loading always constructed a rotary object and decoding always used it. The new guards jointly support the model's None settings. [source; call_362c69f2873848e7b15fc40d238f66a0, call_3d8703bd45664c7694401f6f24b7f39e, call_35bc219f7301425c85fe61d55b984536]

Whole-parent searches located Attention builders in Cohere, DeciLM, Gemma2, GLM4, Llama and Phi3. Each supplies a RopeSettings object, so each retains rotation; Mistral and Qwen2 inherit Llama's assembly. The external reader science/kv_quant_exp.py still calls attn.rope.apply without a guard, but does so only inside an isinstance(TransformerBlock) branch. Cohere2 supplies ParallelDecoderBlock instead, so this inspected utility does not establish a reachable None dereference for the new model. [source; call_438608ec45a74294b17ae88321d2492f, call_eca8136d74be40d18258c1af4c5bdb57, call_40a35d13395448d78782a0d3efd4100c, call_d228a52422bd489285bac1c3ff4bb5d6, call_6921900f85f842be89cb9762e22d5afb, call_35bc219f7301425c85fe61d55b984536]

The selected FlashAttention routes pass (sliding_window, sliding_window), causal masking, sm_scale=None and zero softcapping. The SDPA alternative explicitly rejects nonnegative windows, so it is not an interchangeable backend for these local layers. prepare_inputs follows all six existing model callers: store input_ids, then call prepare_for_attn, preserving its default uncached FlashAttention mode and cached-input checks. [source; call_362c69f2873848e7b15fc40d238f66a0, call_35bc219f7301425c85fe61d55b984536, call_38076a03cc8441838fe789e5bd58cde8, call_40a35d13395448d78782a0d3efd4100c]

Each decoder computes y=LayerNorm(x), then adds Attention(y) and GatedMLP(y) to the residual. The branches share input dependencies, not concurrent Python execution. The existing prefill shortcut returns after the attention addition and skips the MLP. Cohere2 supplies all three components, avoiding the optional-component cases discussed by the earlier Cohere entry. [source; call_35bc219f7301425c85fe61d55b984536, call_4f5dfa534ab84306aa36215cc9a9d771]

Both branches receive qmap=block.parallel. Attention appends .input for Q/K/V and GatedMLP appends .input for gate/up; Linear.capture_H's first_key guard therefore captures the shared normalized input once. Output and down projections retain separate suffixes. This carries the existing Cohere calibration convention into the new model. [source; call_35bc219f7301425c85fe61d55b984536, call_362c69f2873848e7b15fc40d238f66a0, call_3c0284ae005a4ab59c7d027139794d4a, call_40a35d13395448d78782a0d3efd4100c]

layer_norm_eps defaults to 1e-5 and reaches F.layer_norm. hidden_act, if supplied, must be silu. Final normalization requests half output, then Linear projects to vocabulary logits and multiplies by logit_scale after any softcap. The scale defaults to 0.0625, one sixteenth. Tied embeddings default true and permit model.embed_tokens as the head's alternative loading key; Linear still searches its primary key first within each format. [source; call_35bc219f7301425c85fe61d55b984536, call_33b167b5dccc4930b5bbb21f7bbf37f7, call_3c0284ae005a4ab59c7d027139794d4a, call_f654e62ab65c4f9495a52c160cb816bb, call_ecda46859af948ccbd483fd266deb883]

CohereLabs/c4ai-command-a-03-2025 matches the new architecture with hidden/intermediate widths 12288/36864, 96 query heads, eight KV heads, head_dim 128 and 64 layers. CohereLabs/c4ai-command-r7b-12-2024 has 4096/14336 widths, 32/eight heads and 32 layers; its additional layer_switch=4 is not read by this implementation. CohereLabs/c4ai-command-r7b-arabic-02-2025 has the same mapped dimensions as December R7B. Their maximum position counts differ: 131072, 8192 and 16384 respectively. [source; call_ce550ad2778143519dd21fb70d0a03e4, call_d90cfefb149c4c6384efe5e33c315511, call_81fa201d8f414e24b0cc65c1cbef3991, call_35bc219f7301425c85fe61d55b984536, call_1b768bdc722a4ffb8b0cfe6c4133e54e]

For each of those three models, explicit local_attn_first, sliding_window=4096 and pattern=4 agree with the new mapping. Each specifies silu, layer_norm_eps=1e-5, vocabulary 256000, rope_theta=50000 and logit_scale=0.25, overriding the scale default. Each omits tie_word_embeddings and partial_rotary_factor, taking True and full rotation respectively; rotary_pct=1.0 and use_embedding_sharing=true are not the keys consumed by those helpers. [source; call_ce550ad2778143519dd21fb70d0a03e4, call_d90cfefb149c4c6384efe5e33c315511, call_81fa201d8f414e24b0cc65c1cbef3991, call_35bc219f7301425c85fe61d55b984536, call_33b167b5dccc4930b5bbb21f7bbf37f7]

Representative BF16 headers match the model's checkpoint prefixes and output-row/input-column shapes. For Command A, Q/O are [12288,12288], K/V [1024,12288], gate/up [36864,12288], down [12288,36864], embedding [256000,12288], and norms [12288]. For both R7B models, the corresponding shapes are [4096,4096], [1024,4096], [14336,4096], [4096,14336] and [256000,4096], with inspected norms [4096]. These agree with Nq×128 and Nkv×128 projection widths. [source; call_35bc219f7301425c85fe61d55b984536, call_362c69f2873848e7b15fc40d238f66a0, call_504b7a14aaa548c7b7cd3a11c02dc51f, call_840c05da8e7c4feaaabc130a58ec1f53, call_c667c2168772463baabad870b735a3d4, call_91003204ca6a485bb5c7e611e5c23ee2, call_892309bb91f94479a46d80b05bae0557, call_650b4b3ad3774b9c9551446d1c6b7538]

Every tensor in the inspected header subsets has a corresponding embedding, normalization or projection loading path; no unused stored tensor was identified within those subsets. RoPE frequencies are computed from configuration rather than read from checkpoint tensors. Scalar arithmetic independently reproduced the projection dimensions and head_dim=128 for all three configurations. [source; call_35bc219f7301425c85fe61d55b984536, call_3c0284ae005a4ab59c7d027139794d4a, call_cbd72311343c4dcd97348661ab53cd11, call_91003204ca6a485bb5c7e611e5c23ee2, call_650b4b3ad3774b9c9551446d1c6b7538, call_504b7a14aaa548c7b7cd3a11c02dc51f, call_840c05da8e7c4feaaabc130a58ec1f53, call_c667c2168772463baabad870b735a3d4, call_892309bb91f94479a46d80b05bae0557, call_d6a770d0e2b24f47908a701c0ed6a114]

## Authoring-time findings — pending review

### inherited-config-mismatch-diagnostic (suspected; defect)

The new configuration inherits the existing undefined-variable architecture-mismatch diagnostic.

Trigger: Directly instantiate Cohere2Config against a file whose architecture differs from Cohere2ForCausalLM, with assertions enabled.

Expected: Reject the mismatch with an assertion identifying the expected architecture.

Actual: Config.__init__ evaluates an assertion message referencing undefined expect_arch, producing NameError instead. The task does not change that base implementation.

Locations: 151edc00b202b645fcfa2cc2c679d7ef381916fb:exllamav3/models/config.py — Config.__init__, 0ff9fd2e39f6307e54358fd1a48a50b5cf7307f8:exllamav3/models/cohere2.py — Cohere2Config.__init__

Source evidence: call_33b167b5dccc4930b5bbb21f7bbf37f7, call_35bc219f7301425c85fe61d55b984536, call_2b002dcd9bb04989ae52105f8f46d409, call_245470ceab204022bebec1db47c78e1c, call_4335b59088e349b99908ab5c65374a50

source_inspection: Compared the earlier recorded observation with the parent base constructor and new super call. Whole-parent searches found the configuration definitions and config_class invocation. The inspected factory chooses a matching class before construction, so ordinary selection of a stable supported config does not exercise the mismatch. [call_9bff06e8d11a4df78ba9b8e718e2ad4e, call_33b167b5dccc4930b5bbb21f7bbf37f7, call_35bc219f7301425c85fe61d55b984536, call_245470ceab204022bebec1db47c78e1c, call_4335b59088e349b99908ab5c65374a50]. Limits: The full constructor was not executed. External direct callers were not established.

### inherited-partial-rope-frequency-read (suspected; defect)

The reused native rotary path retains an unconditional frequency read beyond a partial-rotation frequency array.

Trigger: Reach a local Cohere2 layer with head_dim=128 and partial_rotary_factor=0.5, using the native RoPE path.

Expected: Rotate the configured channels and copy the remaining channels without reading outside inv_freq.

Actual: RoPE creates 32 frequencies, but rope launches 64 frequency-index threads. rope_kernel reads inv_freq[t] before checking whether the thread rotates or copies, leaving indices 32–63 outside that array.

Locations: 151edc00b202b645fcfa2cc2c679d7ef381916fb:exllamav3/exllamav3_ext/rope.cu — rope_kernel, 0ff9fd2e39f6307e54358fd1a48a50b5cf7307f8:exllamav3/models/cohere2.py — Cohere2Model.__init__

Source evidence: call_44de8111904e4c878b5e05cae9012f7f, call_cbd72311343c4dcd97348661ab53cd11, call_33b167b5dccc4930b5bbb21f7bbf37f7, call_35bc219f7301425c85fe61d55b984536, call_3d8703bd45664c7694401f6f24b7f39e, call_10b8f33069724a1695c2ef54f863c080

source_inspection: Rechecked the initial modules entry against the current parent and task diff. The helper accepts partial_rotary_factor, local layers retain RoPE, and all three Attention decode routes call its native apply method. The new presence guards do not validate frequency bounds. [call_3592d8b803f241ba9baef3fe87b34c2b, call_44de8111904e4c878b5e05cae9012f7f, call_cbd72311343c4dcd97348661ab53cd11, call_33b167b5dccc4930b5bbb21f7bbf37f7, call_35bc219f7301425c85fe61d55b984536, call_3d8703bd45664c7694401f6f24b7f39e, call_10b8f33069724a1695c2ef54f863c080]. Limits: All three inspected reference configurations take full rotation, so this trigger does not apply to their shown defaults. No GPU memory access or resulting output was measured.

scalar_transcription: Counted the launched frequency indices against full and half-width arrays: full rotation fits 64 frequencies; half rotation leaves 32 indices outside the 32-element array. [call_d6a770d0e2b24f47908a701c0ed6a114]. Limits: Integer index arithmetic only; this does not execute CUDA or establish the runtime consequence of the source-level read.

## Uncertainty and limits

No package import, checkpoint load, conversion, model inference or GPU kernel was executed. Python computations transcribe integer scheduling, shapes and frequency indexing only.

Header checks cover representative first-layer tensors and selected terminal tensors, not every shard or layer. They establish names and shapes, not weight values, dtype-conversion correctness or output quality.

The Command R7B December configuration is a pre-cutoff mirror whose identity with the gated official historical file was not verified. The other configuration objects use hash-verified mirrors.

FlashAttention's implementation was not inspected or executed; the annotation establishes the window tuple passed by this repository, not its exact boundary convention or runtime performance.
