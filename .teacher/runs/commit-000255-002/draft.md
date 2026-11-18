# bcaa636f66973eac4ac071ad25ef31e8586a02dc


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/bcaa636f66973eac4ac071ad25ef31e8586a02dc) · [Evidence ledger](draft.json)

Adds explicit Transformers EXL3 registration, header-driven Linear replacement, post-load finalization and a generation example. The adapter remains local-directory/GPU-only and omits existing experimental decoder metadata.

- [Load EXL3 layers through Transformers quantization hooks](#transformers-integration)

## Problem

The change introduces an EXL3 quantizer adapter for Transformers, with an example explicitly calling patch_transformers before AutoModelForCausalLM.from_pretrained. [source; call_57a40af67db046ef8cf035b38cdf1708, call_374256cc61ae414fa55f8c34e09df96b]

## Reasoning

The adapter separates module discovery, checkpoint loading and executable-layer construction: header metadata creates meta-device buffers before loading, and a post-load hook constructs LinearEXL3 afterward. These stages are prerequisites for one another rather than independent features. [source; call_374256cc61ae414fa55f8c34e09df96b]

## Impact

Registration is explicit, but importing the integration is eager: the package initializer imports integration, whose initializer imports the Transformers adapter and its Transformers quantizer APIs. Thus those imports enter ordinary exllamav3 package initialization even when patch_transformers is never called. [source; call_fcd276e3b49841b58b0f978a4fb1a5af, call_96f692ba29a14b56860018f0f8a13e9e, call_374256cc61ae414fa55f8c34e09df96b]

The adapter requires CUDA availability and a local model directory, declares itself nontrainable and nonserializable, and does not implement direct Hub checkpoint discovery. [source; call_374256cc61ae414fa55f8c34e09df96b]

## Source Notes

Read the earlier packed-sign workaround, dtype-metadata and experimental-codebook entries. They establish the opt-in CPU expansion mechanism, the torch_dtype metadata field, and the requirement to preserve per-layer decoder multipliers. [ancestor; call_760a58b9ba344673bfff174364655e5e, call_b3dd2cbb1a2d4028bdf960312fbd435b, call_b9138eed849d4734884fe2c1f9713065]

Also read the original quantized-inference chapter and indexed-embeddings entry. The former records historical packed-sign and launch limitations; the latter concerns the existing package export context, not the new Transformers adapter. [ancestor; call_0df70c8270634614bcc4d7da2cf8fa4b, call_4d5d3ed3167546eb88fe4a2494c397b9]

Current source changes the original chapter's packed-sign and zero-slice concerns: construction already expands packed factors into suh/svh, and single-GEMM selection clamps its grid count to at least one. The reconstruction wrapper still uses cols / 8 without a remainder check, and LinearEXL3.forward still does not inspect a zero native GEMM return. This integration supplies no additional dimensional validation or fallback. [source; call_8fe2f56c631a459cb48ecc453b1ebeda, call_dc4973deb71a441b8bc1de24e47de8fa, call_8d4746bc2d664aa78842eff205e05a89, call_101b083f457c4ec8b9d608040f8a05a3, call_374256cc61ae414fa55f8c34e09df96b]

Discussion relationships are contextual inferences, not upstream links to this commit. Issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” and #7, “quantizing model: undefined symbol: __cxa_call_terminate,” traverse the touched package initializer but report installation/toolchain failures. PR #4, “chore: update config.py,” proposes a spelling correction in the inspected configuration file. [inference; call_ef227a46d0f64a90908a82b8eefada1c, call_c23b235e09924bc09878cc7cec3d087c, call_b251e56680b949baacc8de83c8d71668, call_fcd276e3b49841b58b0f978a4fb1a5af, call_86968aaa43b9470383f86c1e0bb7655e]

Issue #33, “Error converting model,” reports file-opening trouble and later GLM output trouble; #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” report conversion failures. Their inferred overlap is through the inspected loader and Linear conversion code, not evidence that this adapter fixes them. PR #26, “Superior 3INST parameters,” is more directly relevant by inference because it discusses the per-tensor codebook metadata omitted by this adapter. [inference; call_05aaf33b59f54cab9ab3daf38b176579, call_b53b0373704648598c19114edfb5f5a8, call_871db2d1eec241ca92c1e22c3cb5d34e, call_e9599504dfe1487990b3d4a30a0799e5, call_221b26c5cfcb45d39ac2b206875a6d7c, call_09051de02c644dd6b3cd895cd8335af9, call_374256cc61ae414fa55f8c34e09df96b]

<a id="transformers-integration"></a>

## Load EXL3 layers through Transformers quantization hooks

patch_transformers writes the exl3 entries into AUTO_QUANTIZER_MAPPING and AUTO_QUANTIZATION_CONFIG_MAPPING and assigns QuantizationMethod.EXL3 = 'exl3'. Exl3Config stores that value as quant_method. This is process-local registration, not a new model architecture implementation. [source; call_374256cc61ae414fa55f8c34e09df96b]

get_modules_to_replace requires model.name_or_path to be a directory, scans its safetensors headers and considers only torch.nn.Linear instances. Replacement requires trellis plus either su or suh and either sv or svh. Other modules remain untouched. The collection's group check tests names, not tensor dimensions. [source; call_374256cc61ae414fa55f8c34e09df96b, call_8d54601e5b6b4532859bf13dac2fd4de]

Discovery translates a model.language_model. module prefix to language_model.model. for checkpoint lookup while retaining the original module path for replacement. A scalar transcription verified that the hardcoded slice index 21 exactly removes the former prefix. [execution; call_74bc44df4ff141b1b988b1232275116a]

Exl3HfLinear builds registered meta buffers from header shape and torch_dtype metadata for trellis, optional bias and the packed/unpacked factor alternatives. Its separate one-element meta weight is only a dtype placeholder, not a reconstructed dense weight. replace_modules recursively inserts wrappers and records them for post-load finalization. [source; call_374256cc61ae414fa55f8c34e09df96b, call_8d54601e5b6b4532859bf13dac2fd4de]

The documented 4096-input, 1024-output example uses 256 by 64 tiles of 16 by 16 weights, with 48 sixteen-bit storage words per tile. Scalar arithmetic confirmed 786432 words and exactly three packed bits per weight; factor and bias storage are additional overhead. [execution; call_74bc44df4ff141b1b988b1232275116a]

finalize casts unpacked factors and bias to FP16, then constructs LinearEXL3 with config=None, FP16 output and transformers_fix=True. Compared with the existing Linear.load_exl3 and convert_exl3 construction sites, it enables the CPU packed-sign workaround but omits their mcg/mul1 propagation. LinearEXL3's existing datatype and required-factor assertions still execute. [source; call_374256cc61ae414fa55f8c34e09df96b, call_8fe2f56c631a459cb48ecc453b1ebeda, call_2cf5e61d6ef74060997a72b7076ddf3b, call_4d6b4ee2ada2450c97981fc8bbbe646d]

The wrapper saves the input dtype, calls the inner forward with x.half() and an empty parameter dictionary, then casts the result back. Unlike the existing Linear.forward caller, it exposes neither reconstruct nor output-dtype overrides and adds no ExLlama module-level softcap/post_scale processing. The inherited default reconstructs for more than 32 flattened rows; otherwise it uses direct EXL3 GEMM. Reconstruction allocates an FP16 inner matrix and uses native reconstruction and hgemm rather than retaining a permanent dense weight. [source; call_374256cc61ae414fa55f8c34e09df96b, call_043c49af47444751a0c5310a4eb2700f, call_4d6b4ee2ada2450c97981fc8bbbe646d, call_8fe2f56c631a459cb48ecc453b1ebeda, call_8d4746bc2d664aa78842eff205e05a89]

The before-load hook conditionally sets the config supplied through kwargs to tie_word_embeddings=False; it does not unconditionally mutate model.config. The after-load hook finalizes every recorded replacement, clears the list and returns the model. The source therefore establishes the mutation and ordering, not whether every Transformers loading path supplies that config argument. [source; call_374256cc61ae414fa55f8c34e09df96b, call_bc324407446c409db289a6b099cf001e, call_4d456af2191f4606bc836fdb2aa0ffa7]

Existing SafetensorsCollection callers include configuration loading, variant collections, compilation and the index utility. Configuration can supply a load method or variant map; compilation reads payloads and closes handles after groups; the index utility uses headers only. The adapter follows the header-only use, explicitly closes its collection on the normal path, and leaves actual checkpoint payload loading to Transformers. [source; call_2ea1c4261edb41e394631fe0140f368f, call_86968aaa43b9470383f86c1e0bb7655e, call_55414f2339e94a9eace28dc241204a14, call_055bd00672764d0f8946780bc1396099, call_5de2ea119fae4527a763c121faac2a38, call_374256cc61ae414fa55f8c34e09df96b]

## Authoring-time findings — pending review

### decoder-metadata-not-forwarded (suspected; defect)

The Transformers wrapper drops optional per-layer codebook multiplier tensors supported by the existing EXL3 loader.

Trigger: A local checkpoint contains an otherwise matching Linear tensor group encoded with a nonzero mcg or mul1 multiplier.

Expected: Preserve the stored multiplier when constructing LinearEXL3, or reject the unsupported codebook explicitly.

Actual: Discovery accepts the group, but Exl3HfLinear registers neither multiplier buffer and finalize passes neither argument. LinearEXL3 therefore stores zero multipliers and selects the original decoder in both direct GEMM and reconstruction, rather than the checkpoint's selected codebook.

Locations: bcaa636f66973eac4ac071ad25ef31e8586a02dc:exllamav3/integration/transformers.py — Exl3HfLinear.finalize

Source evidence: call_374256cc61ae414fa55f8c34e09df96b, call_4d6b4ee2ada2450c97981fc8bbbe646d, call_77f9f0e1519b4631af98672fde95cf5e, call_8fe2f56c631a459cb48ecc453b1ebeda, call_101b083f457c4ec8b9d608040f8a05a3, call_8d4746bc2d664aa78842eff205e05a89

source_inspection: Whole-parent-tree search found no existing Exl3Hf definitions. The task's before-load hook constructs wrappers and its after-load hook directly calls finalize. Compared that path with both existing LinearEXL3 construction sites, quantizer tensor emission and native decoder selection. [call_0cc4217b3465433ba665e21132c37226, call_2cf5e61d6ef74060997a72b7076ddf3b, call_374256cc61ae414fa55f8c34e09df96b, call_4d6b4ee2ada2450c97981fc8bbbe646d, call_77f9f0e1519b4631af98672fde95cf5e, call_101b083f457c4ec8b9d608040f8a05a3, call_8d4746bc2d664aa78842eff205e05a89]. Limits: No affected checkpoint was loaded. Reach is limited to replaced layers carrying experimental multiplier metadata; original-codebook layers do not trigger this discrepancy. Transformers' treatment of the unregistered checkpoint keys was not executed.

## Uncertainty and limits

No Transformers loading, Torch execution, CUDA kernel, generation or performance test ran. The successful computation checked only scalar indexing and storage arithmetic.

Compatibility of the imported Transformers APIs, registry mutation and dynamically assigned QuantizationMethod.EXL3 across library versions is unestablished.

The example warns about fused projections and sliced Nemotron-Ultra layers; its broader suggestion that other supported models should work is not established by end-to-end testing.

The indexed reference checkpoints do not provide an EXL3 packed checkpoint matching the example's local directory; its actual tensor inventory and dimensions were not validated.

Post-load device movement, CPU/disk offloading, tied-embedding behavior in Transformers and preservation of numerics through FP16 downcasts remain untested.
