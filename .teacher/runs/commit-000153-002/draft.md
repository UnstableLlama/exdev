# a905cffb1a3f66792ea000e9b589557aac3f9d14


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a905cffb1a3f66792ea000e9b589557aac3f9d14) · [Evidence ledger](draft.json)

Integrates dev’s 0.0.2 tree unchanged into master: Qwen3 MoE, indexed expert GEMM, loading and sampling changes, and chat commands. All 44 paths map to ancestor explanations; eight distinct inherited observations remain conditional or untested.

- [Dev-to-master integration and retained conditions](#integration)

## Problem

Merge #37 brings dev's accumulated changes into master. The supplied tree comparisons show that the result is identical to second parent 70056fef5f1f841612023027f6abe6f2b295ce57: the 44-path first-parent diff is integration, not additional merge-specific implementation. [source; call_4e5aa29b6fa2426bbb6e2a38d00bcea9]

## Reasoning

The main integrated feature connects Qwen3 MoE model construction to routed expert modules, all-expert calibration and indexed multi-GEMM. Other changes independently improve loading, sampling, chat interaction and release identification. [source; call_a1e4aa144d08495b9f9f2839fa535659, call_2a63fe8a936c48828f6511fa87d0dcb7, call_aea4fdc625214afeb8004830e68bc7e0, call_8731c2dcde3e402cbd00f539ac283fb5]

The parent graph identifies 17 commits newly reachable from the first-parent line: 70056fef5f1f841612023027f6abe6f2b295ce57, 95cfa726b63049e455e2037e1325ae6961e3be98, 1e1754787e52f416252a36ea3ebf7177d2e11f2a, f5127e87f800a4f11f2aa9605039896ac41d9382, 9c31971b844ffea3b077d5157225565877679171, 809b0dab40c5f576bd84e38b0712cc5c3011f21e, 10222646d08f8bbdeebf0813d1cbf9e641154a99, 43383ebdbcc2bc79113e6e9d4da2541f7860f92a, a5caa423bbd9d8a61266a88fb237c18fb77ec0b8, c6aa83f7e5a5e735c079d41244cbc704eda7e54e, 6fc153d7a062aa7f53fe13b27d008c2d90d8d62f, 538dcae365891784729d198539f72ceece5631eb, e0cfb2e93c6ddd1e347711f544d1e0750a0acc45, a027848ddc37899274b540ed5ba009aa742d9d94, edafdd1f3d9a966a982f54334838f4f94ee51473, 74abd5e135f574f958faa6507f40c12c3f0cadba and b73d0739044d14ebe12a73bdbd154c1f28b36f19. The first parent itself, beb7bcd96d0d54ee2511a84f63632d0fe3590050, ae04741f22324cc746ab78c27365e53e3f9f1cf4 and c2b8516f17487d060163f841cf83340e007ced4f are already reachable from both sides. [source; call_bb53b804fdc941fc961ac0e74a494107]

The newly reachable merge entries 10222646 and f5127e87 describe importing master’s build workflow and HumanEval edits into dev. Those imports do not constitute new first-parent functionality here: master already had them. [ancestor; call_53bd0f6f2b874d0eae0b12680e1933d6, call_62ae1a8b8502408ca32a2b8eaae6b644]

## Impact

Master gains Qwen3MoeForCausalLM registration, expert execution and calibration support, single-device deferred loading, replacement-tensor transposition, dtype-based FP16 matmul dispatch, sampling corrections, chat clipboard commands and version 0.0.2. These are source-level capabilities, not demonstrated end-to-end compatibility or performance results. [source; call_0840366731814ca2b6cffdab180f8a9a, call_adfe3bf10ce740de8dc57c96f17d565f, call_aeedb77f6bcd4f28af3117e77bdfeec6, call_43ce941d725d41f4836f6722f77864b9, call_93e72b03586a49c6ac257ad5996031a6, call_2eeef843d5f34a35aa37a84772afc1c0, call_9285bf7e22d84dff8a05bfa61a2ade47]

## Source Notes

The task attributes the merge to Brian; the supplied PR #37 evidence identifies opener kingbri1 but contains an empty body. It supplies no additional technical explanation or test report. [source; call_0ac8f59afd9a49c5bee9bae3c28fa3c1]

Closed issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” reports an extension-build assertion and later installation recovery. Its inferred connection is only the shared chat.py/model.py traceback paths; the integrated edits do not address that reported build mechanism. [inference; call_5cc9acb467ce44279622f3f41dde3230, call_2eeef843d5f34a35aa37a84772afc1c0, call_adfe3bf10ce740de8dc57c96f17d565f]

Closed issue #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” concerns vocabulary padding during quantization. Closed issue #11, “AssertionError: bias is wrong datatype,” concerns bias conversion. Both report earlier recovery. Their inferred overlap here is convert_model.py, not the all-expert capture changes, and neither establishes a fix newly delivered by this merge. [inference; call_4718261c41184781bf54a90c0787cf96, call_13438a132aca4be3bf333a7da0851498, call_aea4fdc625214afeb8004830e68bc7e0]

Closed issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” is framed around using the wrong chat template; discussion recommends chatml. Its inferred relationship is shared chat.py/job.py paths, not evidence that clipboard handling or the UTF-32 annotation fixes the report. [inference; call_ab551bf0c11d4236b146328caf05756c, call_77d68c957bbe48e8aea0a9d9e34cc5a8, call_3e9bf605cfe3441dbcf47bc2ce69630b]

Closed issue #16, “RuntimeError: CUDA error: invalid configuration argument,” discusses conversion failure traced to tokenizer truncation. Closed issue #33, “Error converting model,” ultimately reports too many open files and subsequent recovery. Their inferred overlap is conversion/transformer and Safetensors loading respectively; neither report validates the new MoE or deferred-load behavior. [inference; call_682fc626d32645c8a8f4d17ad2e88c57, call_7ca62774c23d49f1b6865c2748571749, call_aea4fdc625214afeb8004830e68bc7e0, call_aeedb77f6bcd4f28af3117e77bdfeec6]

Closed PR #13, “Fix a tokenizer issue while converting models without a bos_token_id defined,” reports None being passed to id_to_token. Shared conversion and BOS terminology provide only an inferred association: this merge changes HumanEval BOS insertion, not that tokenizer initialization expression. [inference; call_14a6c65bac534bf8b667b69eb25e2986, call_7e1ff7cae00b455bbf38a93aca0250d7]

Closed PR #35, “humaneval.py: fix top_k type, remove rep_p, add qwen3,” contains gakada’s indexing and penalty reports, followed by turboderp’s masked-infinity interpolation diagnosis and later BOS discussion. A relationship to this merge is inferred from the exact penalty expression and HumanEval BOS edits. Its original CLI/preset changes were already on master; the penalty-kernel and BOS follow-ups now arrive from dev. Reported scores are not independently reproduced measurements. [inference; call_23ab2f487c3f476a98de7b1754b3015f, call_7bdd4636633b4967bab8615151a71407, call_bdf43c1942c74e609210ce2d89aeace2, call_d926333e75114e0299154fa1bc31001e]

Closed PR #36, “added max_total_tokens variable to class Generator, fixed type assert…,” directly reports the missing attribute. Tokoba is both the reporter/opener and the contributor who says they added and tested the fix, rather than independent corroborating reporters. The inferred task connection is the matching attribute initialization and diagnostic expression; the reported TabbyAPI success is not a test performed here. [inference; call_a90b4f7ce7ad4201b8361419acf8e2d6, call_909f49d19c154865a3f1daba3ae69065, call_0cbe97bc3fac487c8e3aac4ae1a136e1]

The unreferenced items read were #7, “quantizing model: undefined symbol: __cxa_call_terminate”; #22, “OpenAI compatible API example”; and #34, “torch._C._LinAlgError on last layer of quant.” They concern toolchain loading, an API proposal and Cholesky/overflow problems. Connections are inferred only from shared model.py, chat.py/sampler and convert_model.py paths respectively; none establishes motivation or validation for the integrated changes. [inference; call_009d58cfe9ea4018a79cd2a15aad8eb2, call_8aec572441034fc59af3f811dbd95058, call_85af76c28db544e8ab465a86dfffee45, call_3bbfc96e42534705b10e9b9b3e88a021]

<a id="integration"></a>

## Dev-to-master integration and retained conditions

Path correspondence, native interface: exllamav3/exllamav3_ext/bindings.cpp, quant/exl3_gemm.cuh and quant/exl3_kernel_map.cuh carry the indexed multi-GEMM interface explained by b73d0739. quant/exl3_gemm.cu, quant/exl3_gemm_kernel.cuh and quant/exl3_kernel_map.cu combine that entry’s implementation with edafdd1f’s concurrent-grid changes. quant/exl3_gemm_inner.cuh carries edafdd1f’s zero row-index change. These are the same interface, dispatch, pointer-offset and synchronization lines described by those entries. [source; call_94b849d4736e4aa7934d9c8273d79561, call_ff908d40494f4d5494c01a420f2bf820, call_7476597e2d54443aa94f31f6b8f020f6, call_8731c2dcde3e402cbd00f539ac283fb5, call_fdbbe22649f54336850707d5fd50a7f1, call_e4d32fa6023848d897560bcd20d1fde2, call_9499f2a3308f4fb281185dc91d1a4b81, call_4f58808284d04f5da2f046c4146c8030, call_042cf722d9bb40368d9363f856c929c5]

Path correspondence, compilation units: under exllamav3/exllamav3_ext/quant/comp_units/, exl3_comp_unit_1.cu/.cuh, exl3_comp_unit_2.cu/.cuh, exl3_comp_unit_3.cu/.cuh, exl3_comp_unit_4.cu/.cuh, exl3_comp_unit_5.cu/.cuh, exl3_comp_unit_6.cu/.cuh, exl3_comp_unit_7.cu/.cuh and exl3_comp_unit_8.cu/.cuh are all explained by b73d0739. Each pair adds the corresponding bit-width’s FP16/FP32 multi-GEMM table and declarations, matching that entry’s table-instantiation explanation. [source; call_94b849d4736e4aa7934d9c8273d79561, call_b35491d357254521a8ad249f4004b38a, call_ae6e6d47ea2c4c57a414cbec41b067ef, call_423b0fb8896b485ea3d2eebce09387a6, call_e523b8eae82e40e9ae7590695fbb34c2, call_7b3dd924208e4b1e89775be126474428, call_f724414377874ca3b7722b26bb97b0ae, call_315adae4d33e4584b6069f285aa6316c, call_bf72df3e749b48fd825bdec19370dadc, call_1b0aad3667504b60954f3f99ae0db666, call_11e166f5d8e146b89bffaed1b9c658a6, call_846e03129e3e43fdb7b15df6651eb1c9, call_108fbcc015fb441bab596dfe492db6d4, call_24a8b7d192c741aa8b443d27886543a6, call_7d3598fe06b846ada7aeac8444e3a21f, call_070b6f0aa07e4b07af12b5850cf36066, call_fc5a8debc5574a1dad290736e7a912e7]

Multi-GEMM accepts rank-three FP16 inputs and FP16/FP32 outputs, with int64 device-address tables for quantized weights and scales. Indices select experts; optional weights scale their outputs. Input leading dimension one broadcasts the token, while scratch and output have separate expert slices. Grid z-planes run independent matrices, with concurrency min(total_sms/num_sms, output expert count), and whole-grid barriers separate transforms and 16-row GEMM steps. The selector’s divisor 12 remains an explicitly experimental slice heuristic, not a demonstrated universal optimum. [source; call_8731c2dcde3e402cbd00f539ac283fb5, call_9499f2a3308f4fb281185dc91d1a4b81, call_41d7bdac40bf4632a912fc560421f23d]

Path correspondence, modules and conversion: exllamav3/modules/__init__.py, modules/block_sparse_mlp.py, modules/transformer.py, conversion/allocation.py and conversion/convert_model.py match 6fc153d7’s public routed module, decoder allocation, expert-key grouping and calibration changes. exllamav3/models/model.py combines that entry’s default calibration flag with c6aa83f7’s deferred-load brackets. These are the same changed lines described by those entries. [source; call_d58b2a8053654f2eb1db73699cd42cc4, call_5eba0d3b8af34399bc4095dee958ad38, call_b20e2630d20e49f98420913e501e298f, call_2a63fe8a936c48828f6511fa87d0dcb7, call_2ff55a3934244b6ab0237642df88ce32, call_7963e91c75e4468e88e5f109da577082, call_aea4fdc625214afeb8004830e68bc7e0, call_adfe3bf10ce740de8dc57c96f17d565f]

BlockSparseMLP flattens tokens, computes router softmax, selects and renormalizes expert weights, and accumulates weighted down(SiLU(gate(x)) × up(x)). Multiple tokens or non-fully-EXL3 experts use expert-grouped Linear calls. One-token fully EXL3 execution uses three indexed multi-GEMMs; fusion requires uniform dimensions and bit widths per projection group, no bias/softcap and unit post-scale. Only the down call receives routing weights. Calibration requests every expert for capture, then recomputes reference outputs with ordinary routing, trading extra capture work for down-projection coverage. [source; call_2a63fe8a936c48828f6511fa87d0dcb7, call_945669b181674c44b08c51a5e7fff895, call_f3b47aabb7ee43859accc5c30dd48403]

Path correspondence, model registration: exllamav3/models/architectures.py and models/qwen3_moe.py match a5caa423’s registration and complete model builder. The builder combines Q/K-normalized attention with routed MLPs, maps experts.{expert_idx}.{gate,up,down}_proj and the mlp.gate router, requests half intermediates and float MLP output, and enables all-expert calibration. [source; call_98d93591a80d486f9ab70838696fcf73, call_0840366731814ca2b6cffdab180f8a9a, call_a1e4aa144d08495b9f9f2839fa535659]

All seven indexed Qwen3 MoE configs were read successfully. Qwen/Qwen3-235B-A22B, Qwen/Qwen3-235B-A22B-FP8 and Qwen/Qwen3-235B-A22B-GPTQ-Int4 each match the registration and specify hidden size 4096, expert width 1536, 94 layers, 64 query heads, four KV heads and head_dim 128. Qwen/Qwen3-30B-A3B, Qwen/Qwen3-30B-A3B-Base, Qwen/Qwen3-30B-A3B-FP8 and Qwen/Qwen3-30B-A3B-GPTQ-Int4 each match it with hidden size 2048, expert width 768, 48 layers, 32 query heads, four KV heads and head_dim 128. Each explicitly supplies SiLU, normalized top-k probabilities, 128 experts, eight selected experts and untied embeddings; therefore the head-dimension, KV-head and tying defaults are not needed for these models. FP8/GPTQ declarations do not establish loader compatibility. [source; call_a1e4aa144d08495b9f9f2839fa535659, call_ead24191d12146929b0b27f2e13684c1, call_8451c9cc2c634fb7b2c11d0b73c130e0, call_278a3387e13c45e1830b07eae0e25ced, call_6d095ad657e5445f987059a645a9bcc1, call_39207fc5bd024491b4491aedb686d6d0, call_cc6726dba5be40528fd6192ef26d8ba3, call_07e441a56766405c91aef0ea6f1a45f3]

Path correspondence, loading and unquantized multiplication: exllamav3/loader/safetensors.py matches 538dcae3’s transpose correction for in-memory replacement tensors. exllamav3/modules/quant/fp16.py matches 74abd5e1’s dtype dispatch. These lines implement the mechanisms described by the entries: replacement tensors now honor transpose=True, and matching input/output dtypes select torch.matmul(out=y), while differing dtypes retain ext.hgemm. The latter requires rank-two half inputs and supports half output through cublasHgemm or float output through cublasGemmEx. [source; call_07468ed8895f49ceb474a9a9b0768a5c, call_30f66c4e8e9b43789356fec606e95cc5, call_aeedb77f6bcd4f28af3117e77bdfeec6, call_43ce941d725d41f4836f6722f77864b9, call_910bde424f1d4f16b108c61039f05cb8]

Explicit single-device loading now brackets eligible modules with begin_deferred_load/end_deferred_load. The existing mt_fread loader queues allocated destinations, groups transfers and flushes before progress advances; Python and no_defer reads remain immediate. This reuses the existing batching facility rather than changing checkpoint storage. The inherited odd-element BF16 conversion condition remains present. [source; call_adfe3bf10ce740de8dc57c96f17d565f, call_bddfe1708ffe49e3a7232186e6fd5249, call_78169ba73cd64472912ea9e907c6973b]

Path correspondence, generation: exllamav3/generator/generator.py and generator/job.py match 809b0dab and its integration entry 9c31971b: whole-page capacity initialization and annotation edits. generator/sampler/custom.py combines a027848d’s integer normalization with 95cfa726’s integer short-circuit; generator/sampler/presets.py matches a027848d’s top_k=1 greedy shortcut. exllamav3/exllamav3_ext/generator/rep_pen.cu matches 43383ebd’s complementary-weight offset. The changed lines are those explained by these entries. [source; call_909f49d19c154865a3f1daba3ae69065, call_3b796214009e42aeaf2b388b6004878c, call_3bcc4aeab2c84f10ad62e61099a6b964, call_e5fd4d4ed28a4d0885cbcc90e5f6db69, call_c5682bbcf4294daf91ca2d04ef5473ac, call_0cbe97bc3fac487c8e3aac4ae1a136e1, call_3e9bf605cfe3441dbcf47bc2ce69630b, call_93e72b03586a49c6ac257ad5996031a6, call_ea5b722923c24d259d83fca61e46ddcb, call_7bdd4636633b4967bab8615151a71407]

Both parents’ HumanEval scripts already use integer top-k parsing, omit rep_p and provide the Qwen3 empty-thinking prefill. The actual new script behavior is template-specific BOS: granite/reka gain <|endoftext|>, llama/mistral <s>, llama3 <|begin_of_text|>, and deepseek its sentence marker. Gemma retains its literal BOS; ChatML/Qwen3 gain none. Automatic insertion remains only for explicit raw, not the no-option unwrapped-completion path. [source; call_bdf43c1942c74e609210ce2d89aeace2, call_d926333e75114e0299154fa1bc31001e, call_7e1ff7cae00b455bbf38a93aca0250d7]

The first-parent sampler stored top_k unchanged; the merged constructor accepts integers without invoking is_integer and converts accepted integral floats to int, rejecting fractional floats with assertions enabled. Values below one still disable top-k. ComboSampler now treats top_k=1 like temperature zero: penalty steps remain, but filtering, temperature and categorical sampling are bypassed for argmax on initial or penalty-adjusted unsorted logits. HumanEval’s removed repetition control is not restored by the kernel fix. [source; call_e5f581497a8c40da8f7b8da9170be6c4, call_cc7863323934480da75a88d3a04c9f02, call_6488893086f4471e8c8df548571fb1a5, call_402a81b5c52f4184950fdac74fdae968, call_d926333e75114e0299154fa1bc31001e]

The earlier first-parent explanation described fixing HumanEval’s CLI boundary without changing its shared sampler; the dev integration explanation already distinguished its normalized sampler. Reading both parents confirms that branch distinction rather than treating the old HumanEval float bug as newly fixed here. [ancestor; call_2e71f40709b54ded8c003b58a9c7ce50, call_62ae1a8b8502408ca32a2b8eaae6b644]

The repetition kernel now adds 1e-30 to both interpolation weights separately. At full penalty weight, the complementary coefficient no longer becomes zero, avoiding the masked-infinity zero product for positive finite penalties. This is an endpoint safeguard, not general NaN sanitization. [source; call_7bdd4636633b4967bab8615151a71407, call_e5f581497a8c40da8f7b8da9170be6c4]

Path correspondence, examples and release: eval/humaneval.py matches 1e175478’s BOS edits. examples/chat.py combines a027848d’s integer CLI change with e0cfb2e9’s command interception; examples/chat_console.py, examples/chat_util.py and requirements_examples.txt match e0cfb2e9’s feedback helpers, extraction helper and pyperclip dependency. exllamav3/version.py matches 70056fef’s 0.0.2 constant. Together with the preceding groups, all 44 changed paths have an explaining ancestor entry; no changed path is left without one. [source; call_74c18f7156664332bdb6d389485f7cac, call_27f8f8481b114567bb446259c5e3ebdf, call_3bcc4aeab2c84f10ad62e61099a6b964, call_25da45dc77634d8185f6b693c88a8ab3, call_7e1ff7cae00b455bbf38a93aca0250d7, call_2eeef843d5f34a35aa37a84772afc1c0, call_f27bed859a4749149c431b834b1796a0, call_1448c4153fb44b96b09653650ce40979, call_737fa406e7f645e1ad318ff9432b799b, call_9285bf7e22d84dff8a05bfa61a2ade47]

Chat intercepts slash commands before context insertion: /x exits, /cc extracts the last complete newline-delimited triple-backtick block, and unknown commands are not sent to the model. Extraction strips boundary whitespace and calls pyperclip.copy. The new example dependency is imported eagerly; package and module are both named pyperclip. A whole-first-parent search found no prior literal occurrence, without excluding dynamic or external use. [source; call_2eeef843d5f34a35aa37a84772afc1c0, call_1448c4153fb44b96b09653650ce40979, call_737fa406e7f645e1ad318ff9432b799b, call_913cd1037d4d430ba3ebc930b0668b0a]

The version ancestor explains that the shared constant feeds package metadata, conversion provenance and release naming; changing it does not itself execute a build or publish a release. [ancestor; call_25da45dc77634d8185f6b693c88a8ab3]

Bounded Python transcriptions reproduced full-weight negative-infinity interpolation changing from NaN to -inf, obtained 1/sqrt(128)=0.08838834764831843, and calculated query widths 4096/8192 and KV width 512 for the inspected model groups. They also reproduced zero small-workload slices, the false Boolean threshold, 128-versus-eight expert cardinality, two-of-three BF16 pair coverage and empty-block false success feedback. These are arithmetic/string checks, not repository or GPU execution. [execution; call_ed06e06a5e7242c1a152484c15d48939]

All distinct findings recorded by the 17 newly reachable entries were compared with source represented by this merge. The all-expert fused mismatch, invalid multi-GEMM leading dimensions, Boolean selector threshold, zero-slice division, broadcast scratch requirement, odd BF16 tail, empty clipboard feedback and empty UTF-32 annotation remain present. Duplicate reports in the Qwen3 and generator merge entries describe the same retained conditions; their concrete triggers and reach are recorded in findings. [source; call_2a63fe8a936c48828f6511fa87d0dcb7, call_8731c2dcde3e402cbd00f539ac283fb5, call_9499f2a3308f4fb281185dc91d1a4b81, call_41d7bdac40bf4632a912fc560421f23d, call_78169ba73cd64472912ea9e907c6973b, call_1448c4153fb44b96b09653650ce40979, call_cd409c0b44de4a2784cd56d1e161103c]

## Authoring-time findings — pending review

### retained-all-expert-fused-shape (suspected; defect)

The all-expert routing/fused-buffer mismatch recorded by 6fc153d7 and a5caa423 persists.

Trigger: One flattened token, fully EXL3 experts, activate_all_experts=True and num_experts != num_experts_per_tok.

Expected: Evaluate all experts using sufficient buffers or the expert-grouped path.

Actual: Routing emits num_experts indices, but fused buffers have num_experts_per_tok slots; exl3_mgemm checks equality. The inspected configs give 128 versus eight. TransformerBlock and ParallelDecoderBlock forward params to their MLP. Conversion supplies the flag during pre-quantization capture, so ordinary conversion is not demonstrated to hit the fully EXL3 trigger.

Locations: a905cffb1a3f66792ea000e9b589557aac3f9d14:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_d58b2a8053654f2eb1db73699cd42cc4, call_98d93591a80d486f9ab70838696fcf73, call_2a63fe8a936c48828f6511fa87d0dcb7, call_8731c2dcde3e402cbd00f539ac283fb5, call_4e868c3d8e444aa6a4cebfc5bcb634f6, call_3b8e9568ef8e4073b29af4f6a74f0179, call_8e23b64d63c243599c311d1cd4b689bf, call_945669b181674c44b08c51a5e7fff895

source_inspection: Compared routing, allocations, native shape validation and decoder/conversion call sites. [call_2a63fe8a936c48828f6511fa87d0dcb7, call_8731c2dcde3e402cbd00f539ac283fb5, call_8e23b64d63c243599c311d1cd4b689bf]. Limits: Conditional source reach; no tensor execution.

### retained-mgemm-leading-dimensions (suspected; defect)

Multi-GEMM still lacks validation of compatible input/output leading dimensions.

Trigger: Otherwise suitable tensors with A leading dimension two, C leading dimension one and indices shape (1,1), or A/C leading dimensions two/three.

Expected: Reject incompatible leading dimensions before accessing buffers.

Actual: The kernel traverses max(bszm_in, bszm_out). The first case reads an unavailable second index and addresses a second output; the second advances beyond A. The current BlockSparseMLP caller instead uses broadcast (1,k) or paired (k,k) dimensions, so these triggers concern the exported interface rather than its ordinary calls.

Locations: a905cffb1a3f66792ea000e9b589557aac3f9d14:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm

Source evidence: call_94b849d4736e4aa7934d9c8273d79561, call_8731c2dcde3e402cbd00f539ac283fb5, call_9499f2a3308f4fb281185dc91d1a4b81, call_d39e2746d4cb4b9abcdaad6075213217, call_8d59430784734cba80ef5ca913655445, call_2a63fe8a936c48828f6511fa87d0dcb7

source_inspection: Compared wrapper checks, maximum-length traversal and all three located Python calls. [call_8731c2dcde3e402cbd00f539ac283fb5, call_9499f2a3308f4fb281185dc91d1a4b81, call_2a63fe8a936c48828f6511fa87d0dcb7]. Limits: No GPU memory-access test.

### retained-boolean-selector (suspected; defect)

The inherited Boolean-versus-dimension threshold remains in automatic GEMM selection.

Trigger: Hopper/Blackwell automatic selection with bits<=6 and n<=4096.

Expected: A dimensional threshold should distinguish qualifying dimensions; the intended replacement is not established.

Actual: (size_k && bits >= 3) is Boolean and cannot exceed 8192, so the branch always chooses shape two. Both single- and multi-GEMM dispatch use it; positive forced shape indices bypass it.

Locations: 70056fef5f1f841612023027f6abe6f2b295ce57:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cu — select_gemm_shape

Source evidence: call_94b849d4736e4aa7934d9c8273d79561, call_41d7bdac40bf4632a912fc560421f23d, call_5c2a031283544dd29dd84eee3600da6c

scalar_transcription: Evaluated the Boolean threshold for k=16384 and bits=3; it is false. [call_ed06e06a5e7242c1a152484c15d48939]. Limits: Not repository dispatch execution or a performance measurement.

### retained-zero-slice-division (suspected; defect)

The concurrency calculation retains a possible zero divisor.

Trigger: Multi-GEMM with shape two forced and k=n=128.

Expected: Reject an unsupported workload or retain positive launch width.

Actual: The selector computes (128/32)*(128/128)/12=0; the wrapper then evaluates total_sms/num_sms. Reach is the exported binding; the located BlockSparseMLP calls use automatic selection and do not establish this particular trigger.

Locations: a905cffb1a3f66792ea000e9b589557aac3f9d14:exllamav3/exllamav3_ext/quant/exl3_gemm.cu — exl3_mgemm

Source evidence: call_ff908d40494f4d5494c01a420f2bf820, call_8731c2dcde3e402cbd00f539ac283fb5, call_41d7bdac40bf4632a912fc560421f23d, call_8d59430784734cba80ef5ca913655445, call_2a63fe8a936c48828f6511fa87d0dcb7

scalar_transcription: Computed the selector's small-workload slice count as zero. [call_ed06e06a5e7242c1a152484c15d48939]. Limits: Did not execute C++ division or CUDA launch.

### retained-broadcast-scratch-contract (suspected; new_requirement)

Broadcast-input scratch must cover every selected matrix, unlike the retained input-sized comment.

Trigger: bszm_in=1, bszm_out>1 and A_had allocated only as large as A.

Expected: Document and validate the expanded scratch requirement, or preserve the old allocation contract.

Actual: The kernel addresses A_had+j*m*k for each matrix without checking capacity. BlockSparseMLP's gate/up calls allocate per-selected-expert scratch and satisfy this requirement; external binding callers following the comment remain exposed.

Locations: a905cffb1a3f66792ea000e9b589557aac3f9d14:exllamav3/exllamav3_ext/quant/exl3_gemm_kernel.cuh — exl3_mgemm_kernel

Source evidence: call_ff908d40494f4d5494c01a420f2bf820, call_8731c2dcde3e402cbd00f539ac283fb5, call_9499f2a3308f4fb281185dc91d1a4b81, call_8d59430784734cba80ef5ca913655445, call_2a63fe8a936c48828f6511fa87d0dcb7

source_inspection: Compared interface comment, scratch offsets and located caller allocations. [call_8731c2dcde3e402cbd00f539ac283fb5, call_9499f2a3308f4fb281185dc91d1a4b81, call_2a63fe8a936c48828f6511fa87d0dcb7]. Limits: No external caller or GPU overwrite observed.

### retained-deferred-bf16-tail (suspected; defect)

Single-device deferral inherits the pair-only BF16 conversion tail gap.

Trigger: Eligible file-backed odd-element BF16 tensor loaded on CUDA through deferred mt_fread with BF16-to-FP16 conversion enabled.

Expected: Convert every element before consumption.

Actual: The CUDA helper launches numel/2 pairs, leaving the final odd element unconverted. A one-element chunk gives zero blocks. Source traces the direct stloader_deferred_cuda call through end_deferred_load to the newly bracketed model loader; no affected checkpoint was demonstrated.

Locations: 70056fef5f1f841612023027f6abe6f2b295ce57:exllamav3/exllamav3_ext/stloader_cu.cu — inplace_bf16_to_fp16_cuda

Source evidence: call_5eba0d3b8af34399bc4095dee958ad38, call_179609bb0dac4d47823700351a87f2d1, call_78169ba73cd64472912ea9e907c6973b, call_af98f461862b401b8caee485c9e871b0, call_bddfe1708ffe49e3a7232186e6fd5249, call_adfe3bf10ce740de8dc57c96f17d565f

source_inspection: Inspected unchanged converter and its deferred-loading call chain. [call_78169ba73cd64472912ea9e907c6973b, call_af98f461862b401b8caee485c9e871b0, call_bddfe1708ffe49e3a7232186e6fd5249]. Limits: No GPU conversion or zero-block launch was executed.

### retained-empty-clipboard-feedback (suspected; defect)

An empty matched code block is copied but reported as absent.

Trigger: /cc after a response whose last matched fenced block contains only whitespace, assuming the clipboard write succeeds.

Expected: Distinguish an empty block from a missing block and report the write consistently.

Actual: The helper copies '' and returns it; chat.main treats it as false and prints 'No code block found in last response'. The located direct caller is chat.main’s /cc branch; the first parent contains no helper.

Locations: a905cffb1a3f66792ea000e9b589557aac3f9d14:examples/chat_util.py — copy_last_codeblock, a905cffb1a3f66792ea000e9b589557aac3f9d14:examples/chat.py — main

Source evidence: call_27f8f8481b114567bb446259c5e3ebdf, call_0bcb9f8cb7bc46f4b2cdfd3f4ab3725f, call_3ef3cc5b730845c2bef5a1ac5f1c1bc9, call_1448c4153fb44b96b09653650ce40979, call_2eeef843d5f34a35aa37a84772afc1c0

scalar_transcription: Reimplemented regex extraction, strip and caller truthiness; the empty match produced '' and false feedback. [call_ed06e06a5e7242c1a152484c15d48939]. Limits: No clipboard backend or chat session executed.

### retained-empty-utf32-annotation (suspected; defect)

The revised UTF-32 return annotation still excludes its empty-input result.

Trigger: _strings_to_utf32([]), including non-None stop_conditions containing no strings.

Expected: The declared return type should cover the actual empty-input pair.

Actual: The helper returns (bytearray(), None), not two ndarrays or standalone None. Both located callers in Job.__init__ unpack the pair; banned-string processing is truthiness-guarded. This is an annotation mismatch, not an established runtime regression.

Locations: a905cffb1a3f66792ea000e9b589557aac3f9d14:exllamav3/generator/job.py — _strings_to_utf32

Source evidence: call_909f49d19c154865a3f1daba3ae69065, call_3b796214009e42aeaf2b388b6004878c, call_aa44e5175d46486ba4cac30ae18e1175, call_cd409c0b44de4a2784cd56d1e161103c, call_3e9bf605cfe3441dbcf47bc2ce69630b

source_inspection: Compared the changed annotation with the unchanged return branch and both caller constructions. [call_cd409c0b44de4a2784cd56d1e161103c, call_3e9bf605cfe3441dbcf47bc2ce69630b]. Limits: No static checker or repository helper execution.

## Uncertainty and limits

No CUDA compilation, repository generation, model conversion, clipboard operation or performance benchmark was executed. Python checks transcribe scalar arithmetic and extraction logic only.

Configuration compatibility was inspected for seven Qwen3 MoE models; tensor layouts and FP8/GPTQ checkpoint loading were not validated.

Torch’s internal matmul kernel and the reported Blackwell speed advantage remain unestablished. The precise historical Python-version boundary for int.is_integer was not established.

Literal caller searches do not exclude dynamic or external use. Native-interface findings do not establish that ordinary Qwen3 generation or conversion triggers every condition.

Literal BOS markers depend on the selected tokenizer; token-sequence equivalence and HumanEval score improvements were not measured.
