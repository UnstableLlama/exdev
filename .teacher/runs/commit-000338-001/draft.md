# eeaabcdc457efa53ad56314c79e27bae06e7a88c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/eeaabcdc457efa53ad56314c79e27bae06e7a88c) · [Evidence ledger](draft.json)

Mostly formatting and a deferred-loader variable rename. The substantive edits cache Model.find_module and replace the base input pass-through with NotImplementedError, leaving Gemma3 and Mistral3 vision embedding paths without a required override.

- [Cache model lookups and require input preparation overrides](#model-and-loader-cleanup)

## Problem

Turboderp titled the change “Formatting, cleanup, typos.” Most of the diff fits that description, but two edits in the shared Model class change behavior: module lookup is memoized, and input preparation stops providing a default implementation. [source; call_43f65cd1c87543399e5b0fb9bcb0825e]

## Reasoning

Model.find_module still recursively walks registered modules and returns the first matching key, or None. The added @lru_cache lets another lookup for the same model and key reuse that result without walking the tree. It uses the existing functools import, which was already used for get_cache_layers. The separate Module.find_module, which includes the receiver itself in its walk, is not decorated. [source; call_43f65cd1c87543399e5b0fb9bcb0825e, call_66db9b4a925d46699ce7a51e61a6c248, call_d66ae5d9e6a648e9857b936aec677eaa]

The cache trades repeated tree walks for retained lookup results, including misses. It fits a stable module tree, but the patch does not add invalidation. By contrast, making prepare_inputs an override requirement does not depend on the lookup cache. That edit needs each component that uses the shared forward or prefill to provide its own input preparation; the diff does not supply the missing vision overrides. [inference; call_43f65cd1c87543399e5b0fb9bcb0825e, call_66db9b4a925d46699ce7a51e61a6c248, call_6a2b8d14aaa14f83b79e9d67681a4c6a, call_aa0076a51eb043ccbbaf8a6d7f38ac4c]

## Impact

The visible model-level lookup callers are test_qgemm, which finds a linear and optionally a norm, and test_quant_fn's test_quant_dequant, which finds a linear. They still pass string keys. The conversion match is different: mod_strategy finds submodules on the current conversion Module to read qbits_mod_key, so it does not gain the Model cache. [source; call_d926053e9dee4bb88b2f0cdf45440866, call_7fce1a9183c24975b970533cc2c3b3c8, call_d66ae5d9e6a648e9857b936aec677eaa, call_6801228d877a4f569fc20417579bdbff, call_43f65cd1c87543399e5b0fb9bcb0825e]

Text preprocessing remains on the existing architecture overrides. Gemma3 and Mistral3 image embedding instead reach the base prepare_inputs through inherited forward and would now stop before executing the vision tower. Loading is a separate path: single-device loading loads modules directly, and autosplit probes individual modules with dummy input and load parameters rather than calling Model.forward. A successful load therefore would not show that image embedding still works. [inference; call_43f65cd1c87543399e5b0fb9bcb0825e, call_66db9b4a925d46699ce7a51e61a6c248, call_6a2b8d14aaa14f83b79e9d67681a4c6a, call_d66ae5d9e6a648e9857b936aec677eaa, call_976ae661598e4f258a4c66ff35d144fb]

## Source Notes

The initial models chapter describes the shared forward/prefill hooks. The component-selection entry introduced the named factory mapping and recorded a Qwen3 MoE constructor that still passed a bare class. The Gemma3 introduction entry describes the original vision stub; the later Gemma3 and Mistral3 entries describe the executable image towers and their use of shared model execution. The deferred-loader entry describes its allocation/flush contract and records an odd-element CUDA BF16 conversion gap. [ancestor; call_85280bb8ee7940889848ad76a5d13fe5, call_a5c7e56d72ff4a01ad44369a36770239, call_8396bb542f234f4abc61397976c16aec, call_52aed327bca4445291e3faa9f862680e, call_70c832ff5b2c47a790e544db378bf07e, call_419438de120343aea62228c62fed2412]

The Qwen3 MoE mapping mismatch is already absent in the parent: its constructor supplies a text-component dictionary, and the task removes only a TODO from the factory docstring. Gemma3's previously recorded preprocessing-file requirement is still present in its constructor. The earlier Mistral3 resize finding used ceiling at the bounding-box step; the parent now uses floor before alignment, and the task leaves that helper alone. The new vision exception would also stop inherited forward before its attention layers. [source; call_4bfefa870a924acaaf769751e3600de7, call_cb3eef489cf6495cbcf4f3d8bf677526, call_6801228d877a4f569fc20417579bdbff, call_d66ae5d9e6a648e9857b936aec677eaa, call_43f65cd1c87543399e5b0fb9bcb0825e]

A scalar resize check using the earlier Mistral3 trigger (28×1541 input, 1540 maximum, 28-pixel alignment) gave 28×1568 with ceiling and 28×1540 with the inspected floor formula. This checks that example, not Pillow or arbitrary image sizes. [execution; call_cb3eef489cf6495cbcf4f3d8bf677526, call_be2156758ae14c1390098fbf65867226]

Closed issues #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” and open #7, “quantizing model: undefined symbol: __cxa_call_terminate,” both pass through model.py's Config import in their traces. #6 ends in a native build assertion; #7 ends in a native extension import failure. Closed #61, “Run ERNIE-4.5-300B-A47B-PT 2.25bpw with 5x20G 3080 got 'Insufficient VRAM',” and open #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” match the autosplit exception; #61's reporter said changing allocator backend worked. These are inferred associations from the traceback and exact exception text, not fixes made by the model edits. [inference; call_705fb2724bb24a2ebd525f32afe8945b, call_f0fb93f827234133b61a0dae53f5654d, call_f613e3cb3c834f0c9117ce4f1a862f71, call_c28b27ddd51c4ff7adac2449b001e8dd, call_6801228d877a4f569fc20417579bdbff, call_43f65cd1c87543399e5b0fb9bcb0825e]

Closed #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” reaches Job's matching exception when using the wrong chat mode. Open #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reaches the unchanged held_logits append with a width mismatch. Closed #62, “Dev branch 15JUL2025 - ModuleNotFoundError: No module named 'exllamav3.generator.filter',” traces Generator's import of Job and Job's import of the missing installed subpackage. The inferred connection is those unchanged calls or imports, not the duplicate profiling imports. [inference; call_8357fd7f6b1948b59a30eb2498ff83c1, call_6e697072f2da4eb68fc6bb44b85fc98a, call_9526be0240754176a05b4e273b5fa1ef, call_783c2fb2c6a84bd7b7afd63116bf89a0, call_6801228d877a4f569fc20417579bdbff, call_43f65cd1c87543399e5b0fb9bcb0825e]

The earlier “Fix #62, include new directory in packages” entry explains the packaging remedy: explicitly include the existing filter package without changing the import chain. [ancestor; call_3d5d3e51967247058a4f2dd676feafec]

Closed #16, “RuntimeError: CUDA error: invalid configuration argument,” traces uncached attention into linear Hessian capture; the discussion attributes the problem to tokenizer truncation, not attention method formatting. Open #27, “Attention Backend,” asks for comparative FlashInfer support. Closed #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports a tensor-size mismatch in get_tensor's padding copy; open #33, “Error converting model,” opens with a compilation-time failure at get_tensor's native file-open call. The associations are inferred from the named attention paths and matching loader operations; the task changes neither backend selection nor file opening or padding. [inference; call_e6d5b92b94b046deac8f4fdca94aa817, call_27d7f833b9d04109b1cf03209067a888, call_b5a7627e301b44ada9854b11cb2e38da, call_b40c2e9d3b464d9982bf1981b9c54897, call_720d9bd5911a4346a4a3a76692993078, call_6801228d877a4f569fc20417579bdbff, call_43f65cd1c87543399e5b0fb9bcb0825e]

PR #26, “Superior 3INST parameters,” proposes a decoder multiplier; #34, “torch._C._LinAlgError on last layer of quant,” reports a factorization failure; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” reports a bitrate-specific conversion failure; #52, “Error converting moonshotai/Kimi-Dev-72B,” reports Cholesky failures for several bitrates; and #53, “Command A support,” asks for Command A support or available quants. Their inferred overlaps are the inspected conversion file or its Cohere2/Llama model paths, not evidence that this task changes codebook parameters, factorization, or architecture support. [inference; call_8d64ed0320d24c27ade9e03ccb126d62, call_c46ccfa6ac4245cba725ad7de37aa410, call_bf233abfe37e4b1f8720779723e77173, call_fd847bf9a6024c3ca4e402ab5cad51e7, call_260e51da0e4443f3a6d3a41c21751baf, call_7fce1a9183c24975b970533cc2c3b3c8, call_6a2b8d14aaa14f83b79e9d67681a4c6a, call_43f65cd1c87543399e5b0fb9bcb0825e]

<a id="model-and-loader-cleanup"></a>

## Cache model lookups and require input preparation overrides

The base prepare_inputs used to record the original tensor in params["input_ids"] and return it unchanged. The task replaces both operations with NotImplementedError. Model.forward and Model.prefill call this hook before any module runs; the other direct call found is science/kv_quant_exp.py's sample_qkv, which uses a factory-created text model and then walks the modules itself. The literal input_ids-key search found no in-tree params reader; the other quoted-key match is a tensor export name in eval/model_diff.py. [source; call_43f65cd1c87543399e5b0fb9bcb0825e, call_66db9b4a925d46699ce7a51e61a6c248, call_80ceda838d7745bfa1e373537fb9075a, call_7fce1a9183c24975b970533cc2c3b3c8, call_05bdab523f7c40ceaf23d55aa1fda1ea, call_6eabf7ed89474de08758639e1298ff30]

Cohere, Cohere2, DeciLM, Dots1, Ernie4_5, Ernie4_5MoE, Exaone4, Gemma2, Gemma3 text, GLM4, Llama, Mistral3 text, Mixtral, Phi3, Qwen3, Qwen3 MoE and SmolLM3 each override the hook by returning prepare_for_attn's result without calling the base. Qwen2, Mistral and MiMo inherit Llama's override; Gemma3TextModel inherits Gemma3Model's. The helper still handles attention/cache preparation for text. Gemma3VisionModel and Mistral3VisionModel have no such override and pass preprocessed images, not token sequences, to inherited forward. [source; call_d80e5b624d5a4d898d2419548fc1d67a, call_6a2b8d14aaa14f83b79e9d67681a4c6a, call_976ae661598e4f258a4c66ff35d144fb, call_d66ae5d9e6a648e9857b936aec677eaa, call_43f65cd1c87543399e5b0fb9bcb0825e]

Keeping a base pass-through would preserve the shared tensor-forward interface. If the base should require an override instead, explicit vision pass-throughs would preserve the prepared image tensors and their caller-supplied parameters without routing them through token-oriented attention setup. [inference; call_66db9b4a925d46699ce7a51e61a6c248, call_d66ae5d9e6a648e9857b936aec677eaa, call_43f65cd1c87543399e5b0fb9bcb0825e]

An isolated Python run extracted the parent method bodies and applied the two task edits in memory. With a stand-in layer and no component override, the original returned the input and wrote input_ids; the edited path raised without setting the entry. Inserting a layer after a miss made the uncached lookup find it, but the edited lookup still returned None. The local Python's decorator reported maxsize 128 and typed=False; no claim about other interpreter versions is needed. [execution; call_aa0076a51eb043ccbbaf8a6d7f38ac4c, call_43f65cd1c87543399e5b0fb9bcb0825e]

The loader renames the local filenmame to filename consistently. The deferred-record key was always "filename". CPU and CUDA requests still go into separate per-file buckets; within each bucket they are sorted by descending byte size, chunked for native reads, and copied from temporary buffers when needed. The immediate Python backend only loses a blank line. Attention, block-sparse MLP, and memory utility edits also change only spacing. Generator and Job each add a second identical profile_opt import, rather than adding new profiling instrumentation. [source; call_43f65cd1c87543399e5b0fb9bcb0825e, call_d66ae5d9e6a648e9857b936aec677eaa, call_6801228d877a4f569fc20417579bdbff]

## Authoring-time findings — pending review

### vision-input-preparation-missing (suspected; defect)

The shared input hook becomes mandatory without migrating either existing vision component.

Trigger: Call Gemma3VisionModel.get_image_embeddings or Mistral3VisionModel.get_image_embeddings with an otherwise valid loaded component and an image that reaches forward.

Expected: Forward the preprocessed image tensor into the first vision module and continue toward an image embedding.

Actual: Both components invoke inherited Model.forward, which calls the new base prepare_inputs and raises NotImplementedError before entering the module loop. The direct caller is Model.forward; Model.prefill has the same dependency on an override if invoked. The inspected multimodal and image-search examples call get_image_embeddings, so they can reach the failure when using an affected component. This does not establish failure of model loading or text-only generation.

Locations: eeaabcdc457efa53ad56314c79e27bae06e7a88c:exllamav3/models/model.py — Model.prepare_inputs, eeaabcdc457efa53ad56314c79e27bae06e7a88c:exllamav3/models/gemma3.py — Gemma3VisionModel.get_image_embeddings, eeaabcdc457efa53ad56314c79e27bae06e7a88c:exllamav3/models/mistral3.py — Mistral3VisionModel.get_image_embeddings

Source evidence: call_43f65cd1c87543399e5b0fb9bcb0825e, call_66db9b4a925d46699ce7a51e61a6c248, call_6a2b8d14aaa14f83b79e9d67681a4c6a, call_d66ae5d9e6a648e9857b936aec677eaa, call_4b8e518636724bb8ae25467106437e7c, call_976ae661598e4f258a4c66ff35d144fb

source_inspection: Searched the full parent tree for hook calls and overrides, then followed the two vision embedding methods into the unchanged forward and the edited base hook. [call_80ceda838d7745bfa1e373537fb9075a, call_d66ae5d9e6a648e9857b936aec677eaa, call_43f65cd1c87543399e5b0fb9bcb0825e]. Limits: Literal search does not cover dynamic or external overrides.

scalar_transcription: Ran isolated method bodies with a dummy layer, a no-op inference decorator, and the task's hook replacement applied in memory. [call_aa0076a51eb043ccbbaf8a6d7f38ac4c]. Limits: No vision model, checkpoint, PyTorch operation, or image library executed.

### cached-module-miss-survives-insertion (suspected; behavior_change)

Model.find_module can return an old lookup result after the registered module tree is edited.

Trigger: Look up an absent string key, insert a module with that key into the public module tree, then repeat the same lookup on the same model while the miss is cached.

Expected: The prior scan would observe the newly inserted module.

Actual: The decorated method returns the cached None. Replacing a previously found module can similarly leave a cached reference to the old object. The directly observed in-tree callers in test_qgemm and test_quant_fn use existing keys, not this mutation sequence; the conversion lookup uses the separate Module method.

Locations: eeaabcdc457efa53ad56314c79e27bae06e7a88c:exllamav3/models/model.py — Model.find_module

Source evidence: call_43f65cd1c87543399e5b0fb9bcb0825e, call_66db9b4a925d46699ce7a51e61a6c248, call_d926053e9dee4bb88b2f0cdf45440866, call_7fce1a9183c24975b970533cc2c3b3c8, call_d66ae5d9e6a648e9857b936aec677eaa

scalar_transcription: Applied the decorator to the extracted lookup and repeated a miss after inserting a stand-in layer. Only the undecorated version observed the new layer. [call_aa0076a51eb043ccbbaf8a6d7f38ac4c]. Limits: This is a conditional API behavior check, not evidence that any inspected caller edits the tree between lookups.

### deferred-cuda-bf16-odd-tail-carried-over (suspected; defect)

The deferred-loader rename carries over the earlier pair-only CUDA BF16 conversion.

Trigger: Queue a file-backed tensor with an odd BF16 element count for deferred loading to CUDA with allow_bf16 false, then flush.

Expected: Convert every source element to FP16 before the destination is consumed.

Actual: The loader still sends the same conversion flag and byte count to the native CUDA path. A full 2 MiB chunk holds an even 1,048,576 BF16 elements, so an odd tensor leaves an odd final chunk. The conversion processes only numel/2 pairs and has no scalar tail; one element is not converted, and a one-element chunk computes zero launch blocks. The native helper is called by stloader_deferred_cuda; eligible Model single-device and autosplit loads call the flush, and literal matches also exist in evaluation utilities. Eager loads and CPU conversion do not take this CUDA helper.

Locations: eeaabcdc457efa53ad56314c79e27bae06e7a88c:exllamav3/loader/safetensors.py — SafetensorsCollection.end_deferred_load, fb63886b9a9909ab78822780e82fd10d001dcd02:exllamav3/exllamav3_ext/stloader_cu.cu — inplace_bf16_to_fp16_cuda

Source evidence: call_43f65cd1c87543399e5b0fb9bcb0825e, call_d66ae5d9e6a648e9857b936aec677eaa, call_9396695084514ca3a4a689942a8b3c7f, call_6801228d877a4f569fc20417579bdbff, call_976ae661598e4f258a4c66ff35d144fb, call_181aae9160aa43e4bc477020baa95a84, call_389aa096c8a949e1b9fb77ccb762a4c8

source_inspection: Compared the queue record and dispatch with the task diff and followed the native conversion flag to the unchanged pair kernel. [call_976ae661598e4f258a4c66ff35d144fb, call_43f65cd1c87543399e5b0fb9bcb0825e, call_6801228d877a4f569fc20417579bdbff, call_9396695084514ca3a4a689942a8b3c7f]. Limits: No affected checkpoint or outcome of a zero-block CUDA launch was established.

scalar_transcription: Checked chunk parity and pair coverage. Counts 1, 3 and 2049 leave one element; count 2 leaves none. The bit pattern for BF16 one, interpreted as binary16, gives 1.875. [call_aa0076a51eb043ccbbaf8a6d7f38ac4c, call_be2156758ae14c1390098fbf65867226]. Limits: Python integer and bit-pattern checks; they do not execute the CUDA conversion or model native arithmetic and launch error handling.

## Uncertainty and limits

The Python checks use source extraction, stubbed model methods, or scalar arithmetic. No installed package import, real checkpoint load, image preprocessing, generation, or CUDA kernel was executed. Lookup speed and cache retention in normal use were not measured.

Literal searches and static class inspection do not cover external subclasses, dynamically selected callers, or downstream code that reads the removed params entry. No in-tree caller was shown to mutate the module tree between repeated model lookups.

Discussion reports provide historical context, not reproduction results or proof of the author's rationale. For long threads, the notes are limited to the portions inspected.
