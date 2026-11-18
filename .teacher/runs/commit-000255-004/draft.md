# bcaa636f66973eac4ac071ad25ef31e8586a02dc


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/bcaa636f66973eac4ac071ad25ef31e8586a02dc) · [Evidence ledger](draft.json)

Adds a header-driven Transformers EXL3 adapter with explicit registration and post-load finalization, while introducing eager undeclared imports, a packaging omission and incomplete decoder-metadata forwarding.

- [A preliminary Transformers adapter and its import boundary](#transformers-integration)

## Problem

The change adds a preliminary bridge for loading EXL3 linear layers through Transformers rather than through ExLlamaV3's model runtime. [source; call_eac9faee6db44749b8656f78918db17b, call_bd19a3625f434c1fb0e435d810d832ed]

## Reasoning

Header-derived meta buffers let Transformers load checkpoint tensors into replacement nn.Modules; post-loading finalization then constructs the existing LinearEXL3 implementation. This separates Transformers' model orchestration from EXL3 linear computation. [source; call_eac9faee6db44749b8656f78918db17b, call_7fd37a91da834d0da1479adad73dd58c, call_3bb1c93a6a7c407989881a20633a7069]

## Impact

Registration remains explicit, but importing the adapter does not: ordinary import exllamav3 now eagerly imports Transformers. Its dependency declaration and package-list omissions are recorded as suspected defects. [source; call_fc6a25f21b584d1dbdd4c7dac8d9c522, call_57b60102014f442f9b58bf0823d04c10, call_eac9faee6db44749b8656f78918db17b, call_bc70b94fcd954548a463007026d3440d]

## Source Notes

Read the earlier dtype-metadata, nullable-config and CPU-unpacking entries. They establish three prerequisites: list_tensors supplies torch_dtype, LinearEXL3 explicitly accepts an unused None configuration, and transformers_fix enables CPU packed-sign expansion followed by device restoration. [ancestor; call_86966bafd24d4f85b3bfd2609dadb732, call_b82761cffdec48a3a5b8b973c4dee614, call_09533960f82b4f2193a2cd8a609e70ce]

Those entries discuss an older packed-sign concern. The inspected parent already expands packed factors during construction, stores su/sv as None and forwards unpacked suh/svh; the task preserves that implementation and enables its CPU workaround. This is source inspection, not proof that the reported GPU assert is avoided. [source; call_3bb1c93a6a7c407989881a20633a7069, call_eac9faee6db44749b8656f78918db17b]

Closed issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” and issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” report earlier native-extension import failures. Their relationship to this change is inferred only from tracebacks through exllamav3/__init__.py and the inspected import chain; neither reports the newly introduced Transformers dependency failure. [inference; call_3d88a3400c344981b8beb09929b6817f, call_f6455cf6347849c49e668354114d057b, call_7ad7049ec53d42fcbdb87c77554c306e]

Other inspected discussions have different framing: #33, “Error converting model,” covers file-opening failures and later GLM sampling trouble; #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concern quantization failures. Their connections here are inferred from the shared loader or Linear.convert_exl3 paths, not evidence that this adapter fixes them. [inference; call_dc293a22ca5741b389410432d890bbe5, call_2b3ed441869442f694e2a6cea15b13e4, call_4bfc8d8e957b4949b932ba488e67fcb3, call_d4d4519bd0254785b921e93102a869d4, call_49311c0462ee4ed2b067962a29c9c9e2]

PR #4, “chore: update config.py,” describes a spelling correction; #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?,” discusses RoPE scaling; #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports vocabulary/head padding disagreement; #49, “running the QTIP inference code,” offers QTIP installation advice. Their inferred overlap is confined to inspected filenames or import dependencies, not an established motivation for this commit. [inference; call_7f65b6fb78e140e2b18b8b2c8557a4f3, call_1892d7242ded46fa9708dfdc917ce3fd, call_f28477366ddf49a2a2799abaa9daaeaa, call_d2ee9c6447844e9e99d01f2951cdc061]

The inspected opening of PR #26, “Superior 3INST parameters,” proposes alternative decoder multipliers and discusses metadata needed to distinguish codebooks. Its relevance to the adapter's omitted mcg/mul1 forwarding is an inference based on that shared multiplier mechanism, not an upstream link to this task. [inference; call_69081e89e20b486b9a6352aeb92daeb0, call_eac9faee6db44749b8656f78918db17b, call_3bb1c93a6a7c407989881a20633a7069]

<a id="transformers-integration"></a>

## A preliminary Transformers adapter and its import boundary

patch_transformers writes the string key exl3 into AUTO_QUANTIZER_MAPPING and AUTO_QUANTIZATION_CONFIG_MAPPING and assigns QuantizationMethod.EXL3 = "exl3". Exl3Config stores that quant_method and otherwise ignores constructor kwargs. These are process-wide mutations performed when patch_transformers is called, not automatically when the package is imported. [source; call_eac9faee6db44749b8656f78918db17b, call_57b60102014f442f9b58bf0823d04c10]

The parent root initializer imports, in textual order, models.config, models.model, tokenizer, cache, generator and generator.sampler. Package initialization expands that sequence. The task retains it and appends integration, whose initializer immediately imports integration.transformers.patch_transformers. There is no optional-import guard, deferred import, dependency probe or exception handler around these new imports. [source; call_bc70b94fcd954548a463007026d3440d, call_7ad7049ec53d42fcbdb87c77554c306e, call_fc6a25f21b584d1dbdd4c7dac8d9c522, call_57b60102014f442f9b58bf0823d04c10, call_eac9faee6db44749b8656f78918db17b]

Static first-encounter inventory of parent project modules follows. Names are relative to exllamav3; brackets list module-level third-party packages, with — meaning none: 1 root [—]; 2 models [—]; 3 models.model [torch]; 4 models.config [torch]; 5 util [—]; 6 util.misc [torch]; 7 util.rope [torch]; 8 ext [torch, plus attempted native exllamav3_ext]; 9 util.arch_list [torch]; 10 loader [—]; 11 loader.safetensors [torch, numpy]; 12 util.file [—]; 13 util.progress [rich]; 14 util.memory [torch]; 15 tokenizer [—]; 16 tokenizer.tokenizer [torch, tokenizers]; 17 util.profile_opt [—]; 18 tokenizer.mm_embedding [torch]; 19 cache [—]; 20 cache.cache [torch]; 21 modules [—]; 22 modules.module [torch]; 23 modules.linear [typing_extensions, torch, numpy]; 24 modules.quant [—]; 25 modules.quant.fp16 [typing_extensions, torch]; 26 util.tensor [torch]; 27 modules.quant.exl3 [torch]; 28 modules.quant.exl3_lib [—]; 29 modules.quant.exl3_lib.quantize [torch]; 30 util.hadamard [torch]; 31 conversion [—]; 32 conversion.allocation [—]; 33 modules.mlp [typing_extensions, torch]; 34 constants [—]; 35 modules.block_sparse_mlp [typing_extensions, torch]; 36 modules.multilinear [torch]; 37 modules.rmsnorm [typing_extensions, torch]; 38 modules.layernorm [typing_extensions, torch]; 39 modules.embedding [typing_extensions, torch]; 40 modules.attn [typing_extensions, torch, flash_attn]; 41 device [torch]; 42 modules.transformer [typing_extensions, torch]; 43 modules.conv [typing_extensions, torch]; 44 modules.pos_embedding [typing_extensions, torch]; 45 cache.fp16 [typing_extensions, torch]; 46 cache.quant [typing_extensions, torch]; 47 generator [—]; 48 generator.generator [torch, numpy]; 49 generator.pagetable [torch]; 50 generator.job [torch, numpy]; 51 generator.sampler [—]; 52 generator.sampler.sampler [torch]; 53 generator.sampler.custom [torch, typing_extensions]; 54 generator.sampler.presets [—]; 55 generator.visualizer [—]; 56 generator.async_generator [—]. This records project-module entry order, not completion order; circular references reuse modules already being initialized. ext conditionally JIT-loads the native extension if its import is missing. [source; call_44287d6056c64a5ba30b67bda40f5a83, call_7ad7049ec53d42fcbdb87c77554c306e, call_cdc0db01aa1f4979b891b4aee3eff2e4]

At the task, the same project inventory is followed by 57 integration [—] and 58 integration.transformers [torch, transformers]. The latter imports torch.nn and Transformers' quantizers.auto, quantizers.base and utils.quantization_config at module level; its SafetensorsCollection and LinearEXL3 imports refer back to already encountered project modules. Thus Transformers is newly on the ordinary root-import path, whereas the parent's named Transformers imports were in evaluation/example programs rather than this package-initializer chain. [source; call_fc6a25f21b584d1dbdd4c7dac8d9c522, call_57b60102014f442f9b58bf0823d04c10, call_eac9faee6db44749b8656f78918db17b, call_44287d6056c64a5ba30b67bda40f5a83, call_7744abe9f480419698e6af0b56efeb4d]

All discovered requirements files and setup.py were inspected. For packages imported by the new adapter, torch is declared in requirements.txt and setup.py install_requires, but not requirements_eval.txt or requirements_examples.txt. transformers appears only in requirements_eval.txt, as transformers>=4.50.0; it is absent from requirements.txt, requirements_examples.txt and install_requires. The ordinary library installation contract is setup.py's install_requires, not the separately maintained evaluation requirements. The task changes none of these declarations. [source; call_bc70b94fcd954548a463007026d3440d, call_7744abe9f480419698e6af0b56efeb4d, call_eac9faee6db44749b8656f78918db17b]

get_modules_to_replace requires model.name_or_path to be an existing local directory. SafetensorsCollection scans its *.safetensors headers, rather than consuming quantization_config.json or downloading Hub weights. It considers only torch.nn.Linear modules, requiring trellis and one member of each su/suh and sv/svh pair. Other modules remain unchanged. For names beginning model.language_model., it preserves the module path for replacement but looks up tensors under language_model.model. instead. [source; call_eac9faee6db44749b8656f78918db17b, call_7fd37a91da834d0da1479adad73dd58c]

Exl3HfLinear infers a common tensor prefix, creates meta tensors using header shape and torch_dtype, and registers trellis plus present factor/bias tensors as buffers. Missing optional factors become None. inner remains None until finalization. A one-element FP16 meta weight attribute supplies .weight.dtype compatibility without reconstructing a dense weight. [source; call_eac9faee6db44749b8656f78918db17b, call_7fd37a91da834d0da1479adad73dd58c]

replace_modules recursively collects replacements before changing children and records inserted wrappers for postprocessing. The before-loading hook builds and inserts placeholders; the after-loading hook finalizes each wrapper, clears its reference list and returns the model. finalize casts suh, svh and bias to FP16, then passes dimensions, trellis, packed/unpacked factors and bias to LinearEXL3 with config=None, out_dtype=float16 and transformers_fix=True. It does not forward scale, mcg or mul1. [source; call_eac9faee6db44749b8656f78918db17b, call_3bb1c93a6a7c407989881a20633a7069]

The existing direct LinearEXL3 constructors are Linear.load_exl3 and Linear.convert_exl3. The loader first checks the same factor/trellis group, loads optional mcg and mul1 explicitly on CPU and passes them through; conversion forwards them from quantizer outputs. Both use prepared ExLlamaV3 dimensions and leave transformers_fix disabled. The adapter instead uses Transformers' in_features/out_features directly, performs no ExLlamaV3 padding or slicing preparation, and omits multiplier forwarding. Its FP16 casts satisfy the inner constructor's factor-dtype assertions, while the preceding nullable-config and unpacking changes supply the other required interfaces. [source; call_165a49edf59948fbac6b51b82bcf6ccc, call_49311c0462ee4ed2b067962a29c9c9e2, call_3bb1c93a6a7c407989881a20633a7069, call_eac9faee6db44749b8656f78918db17b]

forward saves the incoming dtype, calls inner.forward(x.half(), {}) and casts its result back. This preserves the output dtype interface, not higher-precision linear arithmetic. The empty params dictionary leaves the existing flattened-row dispatch at its default: more than 32 rows reconstructs the inner weight and uses Hadamard transforms plus hgemm; at most 32 uses exl3_gemm. Bias addition occurs inside LinearEXL3. The wrapper does not expose capture/reconstruct controls, softcap or post_scale behavior from the outer ExLlamaV3 Linear. [source; call_eac9faee6db44749b8656f78918db17b, call_3bb1c93a6a7c407989881a20633a7069, call_49311c0462ee4ed2b067962a29c9c9e2]

The before-loading hook sets config.tie_word_embeddings=False only if a truthy config is supplied in kwargs. This is an in-memory mutation, not a config.json rewrite or explicit CPU embedding-placement mechanism. Parent source uses the exact tie_word_embeddings spelling, while conversion.update_config separately writes tied_word_embeddings=True; those are different keys and the adapter does not reconcile them. The comment frames untied loading as necessary because quantization separates the unquantized embedding and quantized output layer. [source; call_eac9faee6db44749b8656f78918db17b, call_dc1a4162ab2640ceadb26a2275d67ad4, call_4bdb730b830d408bbe162fc258fa96a5, call_7ad7049ec53d42fcbdb87c77554c306e, call_cdc0db01aa1f4979b891b4aee3eff2e4]

Bounded standard-library arithmetic confirmed that the rewritten prefix has length 21, matching name[21:], and that a 16×16 tile at three bits per weight occupies 48 sixteen-bit words. A 4096-input, 1024-output layer has a 256×64 tile grid, agreeing with the illustrative trellis shape [256,64,48]. This validates string/shape arithmetic only, not tensor packing or GPU execution. [execution; call_7ad7049ec53d42fcbdb87c77554c306e]

validate_environment rejects unavailable CUDA; update_torch_dtype substitutes FP16 only when no dtype was supplied. The quantizer declares neither calibration nor parameter quantization required, and reports training and serialization unsupported. The example explicitly patches Transformers before from_pretrained(..., device_map="auto") and demonstrates tokenization and generation. Its comments identify local-directory loading, fused q/k/v or up/gate projections and sliced Nemotron-Ultra layers as current limitations; the adapter contains no unfusing or slice-reassembly implementation. [source; call_eac9faee6db44749b8656f78918db17b, call_bd19a3625f434c1fb0e435d810d832ed]

The design reuses the existing decoder rather than duplicating it, but couples loading to Transformers' registries and lifecycle hooks. Header discovery is an alternative to the existing JSON tensor inventory; neither path by itself establishes compatibility with every model implementation. The author's “still needs some work” framing is consistent with the explicit TODOs and limited interface, not a demonstrated compatibility result. [inference; call_eac9faee6db44749b8656f78918db17b, call_bd19a3625f434c1fb0e435d810d832ed, call_cdc0db01aa1f4979b891b4aee3eff2e4]

## Authoring-time findings — pending review

### eager-undeclared-transformers (suspected; defect)

A new unconditional root-import dependency is absent from the ordinary runtime dependency declaration.

Trigger: An existing caller executes import exllamav3 in an otherwise working environment containing the declared runtime dependencies but no Transformers installation.

Expected: Import-only callers should not need an undeclared package for an integration they never invoke.

Actual: The root initializer imports integration, its initializer imports integration.transformers, and that module immediately imports Transformers symbols. If reached without Transformers installed, this raises ModuleNotFoundError before the caller can use the package. Calling patch_transformers is not required to reach the failure. The parent initializer did not have this path.

Locations: bcaa636f66973eac4ac071ad25ef31e8586a02dc:exllamav3/__init__.py — module initialization, bcaa636f66973eac4ac071ad25ef31e8586a02dc:exllamav3/integration/__init__.py — module initialization, bcaa636f66973eac4ac071ad25ef31e8586a02dc:exllamav3/integration/transformers.py — module-level imports

Source evidence: call_fc6a25f21b584d1dbdd4c7dac8d9c522, call_57b60102014f442f9b58bf0823d04c10, call_eac9faee6db44749b8656f78918db17b, call_bc70b94fcd954548a463007026d3440d, call_7744abe9f480419698e6af0b56efeb4d

source_inspection: Compared both initializer chains, the adapter imports and every discovered requirements file plus setup.py. [call_44287d6056c64a5ba30b67bda40f5a83, call_bc70b94fcd954548a463007026d3440d, call_eac9faee6db44749b8656f78918db17b]. Limits: No import was executed. Existing native-extension or other dependency failures may occur earlier; transitive installations may happen to provide Transformers, but the project's runtime declaration does not guarantee it.

### integration-not-packaged (suspected; defect)

The new eagerly imported integration package is not added to setup.py's explicit packages list.

Trigger: Build and install a distribution using the unchanged explicit package list, then import exllamav3 outside the source checkout.

Expected: The installed distribution should contain the integration package that its root initializer imports.

Actual: setup.py explicitly lists the existing packages but omits exllamav3.integration, while the task adds an unconditional import of it. The inspected packaging configuration therefore does not select the new package.

Locations: bcaa636f66973eac4ac071ad25ef31e8586a02dc:setup.py — setup(packages=...), bcaa636f66973eac4ac071ad25ef31e8586a02dc:exllamav3/__init__.py — module initialization

Source evidence: call_bc70b94fcd954548a463007026d3440d, call_fc6a25f21b584d1dbdd4c7dac8d9c522, call_57b60102014f442f9b58bf0823d04c10

source_inspection: Compared the newly added package with setup.py's explicit package enumeration; setup.py is untouched by the task. [call_bc70b94fcd954548a463007026d3440d, call_eac9faee6db44749b8656f78918db17b]. Limits: No wheel or source distribution was built or inspected. Editable/source-tree imports may mask the omission.

### decoder-multipliers-not-forwarded (suspected; defect)

The adapter drops optional decoder-selection tensors supported by the existing loader.

Trigger: Transformers replaces a qualifying linear group whose checkpoint contains a nonzero mcg or mul1 decoder multiplier.

Expected: Finalization should preserve the checkpoint's decoder parameters as Linear.load_exl3 does.

Actual: Header discovery accepts the group, but Exl3HfLinear creates no mcg/mul1 buffers and finalize passes neither argument. LinearEXL3 consequently stores zero multipliers and passes those defaults to reconstruction or exl3_gemm instead of the checkpoint's values.

Locations: bcaa636f66973eac4ac071ad25ef31e8586a02dc:exllamav3/integration/transformers.py — Exl3HfLinear.__init__, bcaa636f66973eac4ac071ad25ef31e8586a02dc:exllamav3/integration/transformers.py — Exl3HfLinear.finalize

Source evidence: call_eac9faee6db44749b8656f78918db17b, call_3bb1c93a6a7c407989881a20633a7069, call_49311c0462ee4ed2b067962a29c9c9e2, call_cdc0db01aa1f4979b891b4aee3eff2e4

source_inspection: Whole-parent constructor search found Linear.load_exl3 and Linear.convert_exl3; inspected both and compared them with the new discovery/finalization hooks. Quantizer output construction explicitly emits optional mcg/mul1 tensors. [call_165a49edf59948fbac6b51b82bcf6ccc, call_49311c0462ee4ed2b067962a29c9c9e2, call_cdc0db01aa1f4979b891b4aee3eff2e4, call_931e1fc86ffe43c88b7fec706ba58865]. Limits: Reach is limited to replaced linear groups using nondefault multipliers. Transformers may reject unexpected checkpoint tensors before forward; neither that loader behavior nor resulting numerical output was executed.

## Uncertainty and limits

No repository import, package build, Transformers loading, Torch operation or CUDA kernel was executed. Import order is a static project-source traversal, not a measured sys.modules trace; third-party internal imports and environment-dependent native loading are outside that inventory.

Transformers-version compatibility of the imported symbols, hook signatures, registry mutation and QuantizationMethod attribute assignment was not established by eligible Transformers implementation evidence.

Checkpoint loading, device placement, tied-weight behavior, numerical accuracy and the example's generation remain untested. The dummy weight is an ordinary meta tensor attribute, not an actual dense weight.

The adapter's generic tensor contract and illustrative dimensions were inspected, but no EXL3 checkpoint header was validated. No model architecture or configuration class is added by this change.

Only the opening portion of PR #26 was inspected; no conclusion relies on its unread discussion tail.
