# 6f77a334156dfc5d93b5acf192b7ddfc26c38900


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6f77a334156dfc5d93b5acf192b7ddfc26c38900) · [Evidence ledger](draft.json)

Adds direct model reassembly with YAML tensor overrides and unloaded bitrate accounting, while retaining original metadata and exposing key-set and output-directory preconditions.

- [Reassemble model artifacts with optional tensor overrides](#recompile)

## Problem

Artifact assembly previously read only conversion intermediates from work_dir/qtensors. The new utility exposes assembly directly from an existing model directory, optionally substituting tensors from other directories. [source; call_dc944adf87cd421b8c54da53bfad2b81, call_d24b382b157f43d893a51bcdb01ace68]

## Reasoning

The edits work together: model_stc selects config.stc as the compiler's source; unloaded storage accounting estimates bitrate from headers; retaining existing quantization metadata avoids requiring calibration arguments that the utility does not supply. [source; call_dc944adf87cd421b8c54da53bfad2b81, call_01a94020c0054da5bbe1e5cfafb0e042, call_d24b382b157f43d893a51bcdb01ace68]

## Impact

Recompilation repackages stored tensors rather than recalibrating or requantizing weights. Override support is constrained by the variant collection's enumeration of original tensor names. [source; call_d24b382b157f43d893a51bcdb01ace68, call_528e4f822ae14d2da83a69ce7c7446e5, call_e2b82f9a5c4640a1a4af99ea7d850ef1]

## Source Notes

Read the root conversion, loading-tokenization and models entries, plus b5fb1827's head-accounting entry. They establish the inherited assembly pipeline, variant-loader interface and suffix-based head classification. The root conversion entry also records stale-output hazards. [ancestor; call_de68f82eea73407aab801f308da3fc15, call_6bae74dcad7b4ada808c97efdb746f4d, call_b618cdc913bc47e19451ce8ea4639695, call_de88534cef3d46e496196139e3041083]

Current parent source differs from the root loader description: variant routing uses fnmatch filters in collection order, with newly added collections prepended, not longest-prefix selection. [source; call_e2b82f9a5c4640a1a4af99ea7d850ef1]

Issue #33, “Error converting model,” reports an assembly-time file-open failure later identified as “Too many open files,” followed by a separate GLM inference discussion. Its connection here is inferred from the matching compile_model/get_tensors call; the inspected compiler already closes the collection after each module read. This task does not add that remedy. [inference; call_7237ef26fca64d2fb2db9bb0af9e9fc2, call_8536b1bc5485496b9b99d432d43a8b32, call_528e4f822ae14d2da83a69ce7c7446e5]

Other inspected discussions frame distinct problems: #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” and #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concern installation/import failures; #8 reports an invalid reshape; #11 reports a bias datatype assertion; #16 reports an invalid CUDA configuration and discusses tokenizer truncation; #38 reports Nemotron conversion padding/slicing incompatibility; #43 reports abliterated Qwen3 conversion failure and invalid inference states. Their relevance to this task is only inferred from shared model.py or linear.py paths, not evidence of fixes here. [inference; call_73723d04c7c04b0fb874c0c39d0159ed, call_85a6d12c2fab439885cf83549795b99f, call_45416a4e2a5a4cccb70cc6ed50de6ec2, call_eb9b778887bc4656ad4ffe385c4481f6, call_ee3768db0a29453c9e7e66741f13886a, call_f0f3e6b209164a708257bf5d59370635, call_ea3a15f2c30e4bd3bfbbfb96460912fd]

Also inspected #34, “torch._C._LinAlgError on last layer of quant”; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values”; #52, “Error converting moonshotai/Kimi-Dev-72B”; #53, “Command A support”; #55, “Possible GLM4 32B regression”; and #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT.” These discuss conversion numerical failures, support or loading regressions. Their task connection is inferred only from shared source paths; the linear.py edit here adds a comment without changing execution. [inference; call_4b8c808bdd3a4b56a0f645bb440ed89e, call_0b34d764fe114ca2b19f72e030719e9a, call_ffe15c9e798f4442b29410daa8bdb0fc, call_bd65a0bc84654181940e18cae13e4b07, call_e870197da80545fe80c59fd50fdb0e0d, call_c57665db3bec49fab443a525d963933d, call_771088a0fadb40e28294907bde24a06d, call_bf01d23f4c834e6db527ce2fcae1298f]

PR #26, “Superior 3INST parameters,” discusses experimental codebooks and per-tensor multipliers, while PR #4, “chore: update config.py,” proposes a spelling correction. Shared files and multiplier metadata provide contextual, inferred connections only; neither establishes motivation for this utility. [inference; call_c716d72ed6504e968fa20ad3b3476e56, call_76afdab4152844eabd8d071a4ce81df4, call_145cd6dab9e942228aad319aaec0c68e, call_438091307588437faa714fb297a6d6ac]

<a id="recompile"></a>

## Reassemble model artifacts with optional tensor overrides

util/recompile.py accepts input/output directories, an optional YAML override specification and an 8192 shard-size default. Neither directory option is argparse-required. main constructs Config and an unloaded default-component Model, installs overrides into config.stc, estimates decoder/head storage, then calls compile_model with model_stc=True and tokenizer=None. The separately constructed local stc and local size helpers are unused. [source; call_d24b382b157f43d893a51bcdb01ace68, call_43d35fc26216465b856ac524df6bed13]

Overrides map sources[].id to sources[].model_dir and overrides[].key to the selected source. Keys are grouped by source directory, then passed as fnmatch filters to VariantSafetensorsCollection.add_stc. A later added collection wins overlapping matches; an unmatched key falls back to the original collection. A matched but missing replacement tensor does not fall back. [source; call_d24b382b157f43d893a51bcdb01ace68, call_e2b82f9a5c4640a1a4af99ea7d850ef1]

Whole-parent search found existing variant-construction callers in model_init.init and eval/model_diff.py. Both use the same YAML grouping and routing preparation. model_init installs overrides before constructing the model; model_diff, like recompile, constructs the model first. Those paths subsequently load tensors, whereas recompile passes the collection directly to artifact assembly. None of these inspected override blocks validates replacement shapes or completeness. [source; call_36846b166f504ea0a91cbf8cbac6035c, call_6fb53b3ef44648b3965839ae915aa1d4, call_d56f097656064a2cb3eda72271d2ba38, call_d24b382b157f43d893a51bcdb01ace68]

Model.get_storage_info retains its three-value return and lm_head suffix classification. Loaded modules still count tensor payload bits; unloaded modules now sum header payload bytes under module.key and multiply by eight. Decoder BPW divides counted non-head Linear bits by their padded weight counts; head BPW is separate. vram_bits includes those selected linears, not all model tensors or runtime allocations. [source; call_01a94020c0054da5bbe1e5cfafb0e042, call_876b2d0527304b2e9c054e294df69cf9, call_68c10a5d0f3440378fa44484eaae7fd2, call_e2b82f9a5c4640a1a4af99ea7d850ef1]

This accounting change supplies a precondition for the new unloaded workflow: Module starts with device=None and Linear.get_tensors returns an empty dictionary when unloaded. Existing direct Model-method callers in eval/longctx.py, eval/ppl.py and examples/batched_translation.py all first load through model_init.init and retain the same tuple unpacking. The separate comparison-adapter helpers found by search are not calls to this Model method. [source; call_1903221e14d64437b85646226cfa6961, call_68c10a5d0f3440378fa44484eaae7fd2, call_f0b3897b3fe2481e9c5f337030a9fec1, call_cd32723caa0b4a9a9d7471ef1767f84f, call_4b31a6f4ffe14bdf9810e9f319124842, call_d006c6165fc74a6b82fbbd93e0158962, call_6fb53b3ef44648b3965839ae915aa1d4]

compile_model selects config.stc only when args.get('model_stc') is truthy; otherwise its original work_dir/qtensors source remains. The sole existing direct caller found in conversion/convert_model.py still supplies prepared conversion arguments and follows that original branch. The new utility bypasses conversion's calibration and per-module quantization work, not merely its command-line parser. [source; call_dc944adf87cd421b8c54da53bfad2b81, call_4427c98a82f143c7a6d9748be8b2b1f5, call_dac51fe42a134e58908b6ec290c503fa, call_6c23f0fd43f1447b96bdc06540601b97, call_d24b382b157f43d893a51bcdb01ace68]

Assembly still packs whole top-level modules, preserves BF16 on reads, makes tensors contiguous and writes safetensors shards. shard_size is multiplied by 1024², so the default is 8 GiB despite the MB help text. Oversized modules receive a warning rather than being split. Auxiliary files are copied from the original input directory; replacement directories contribute selected tensors, not their configuration or tokenizer files. [source; call_528e4f822ae14d2da83a69ce7c7446e5, call_d24b382b157f43d893a51bcdb01ace68]

Existing quantization_config is retained with only bits and head_bits overwritten. The utility rounds measured decoder storage BPW to two decimals and head storage BPW to an integer. When the input lacks quantization_config, the original metadata-construction branch still requires calibration and output-scale arguments. create_quantization_config_json subsequently reopens the output and derives per-leaf tensor_storage metadata from its stored tensor headers. [source; call_dc944adf87cd421b8c54da53bfad2b81, call_d24b382b157f43d893a51bcdb01ace68, call_f09daf3e1ede4122af38da04f9b7740b, call_7d2e1dadccb24fb68131b9d3c6cfc5fb]

A bounded scalar transcription confirmed the default shard target is 8589934592 bytes. It also demonstrated that original-name enumeration omits a replacement-only .mcg tensor: an illustrative 2048-weight group reports 4.0 BPW instead of 4.015625. Transcribing the utility's arguments through the metadata fallback raises KeyError('cal_rows'). These checks do not execute repository code or load tensors. [execution; call_48c5408733c541cc860ef90b43c97028]

The linear.py edit only adds “TODO: Why copy here?” to the existing FP32 capture conversion. It neither removes copy=True nor changes Hessian accumulation. [source; call_bf01d23f4c834e6db527ce2fcae1298f, call_68c10a5d0f3440378fa44484eaae7fd2]

## Authoring-time findings — pending review

### replacement-only-tensors (suspected; defect)

Recompilation can omit tensors present only in an override source.

Trigger: Select an override group whose tensor-name set adds a key absent from the original group, for example an MCG-encoded replacement adding .mcg.

Expected: The materialized replacement includes its required companion tensors, or the utility rejects incompatible key sets.

Actual: Variant get_tensor_sizes and get_tensors enumerate only main.tensor_file_map. The replacement-only key is neither counted nor emitted. Linear.load_exl3 treats absent .mcg as optional, and LinearEXL3 stores a zero multiplier when it is missing.

Locations: 6f77a334156dfc5d93b5acf192b7ddfc26c38900:util/recompile.py — main, 6341b119efc4ef73ff2e4adcdd14a4d79b0a5e6d:exllamav3/loader/safetensors.py — VariantSafetensorsCollection.get_tensors

Source evidence: call_d24b382b157f43d893a51bcdb01ace68, call_e2b82f9a5c4640a1a4af99ea7d850ef1, call_528e4f822ae14d2da83a69ce7c7446e5, call_68c10a5d0f3440378fa44484eaae7fd2, call_0766c275a1d84bc9b32a696c6836a273

source_inspection: Traced the new utility through compiler prefix enumeration and compared existing variant callers in model_init and model_diff. The observation concerns differing key sets, not same-key substitutions. [call_36846b166f504ea0a91cbf8cbac6035c, call_6fb53b3ef44648b3965839ae915aa1d4, call_d56f097656064a2cb3eda72271d2ba38, call_e2b82f9a5c4640a1a4af99ea7d850ef1]. Limits: No actual mixed-codebook checkpoint or inference output was tested.

scalar_transcription: Modeled original-key enumeration with a replacement-only .mcg key and calculated the omitted four-byte contribution. [call_48c5408733c541cc860ef90b43c97028]. Limits: Python dictionary arithmetic only; no safetensors or repository implementation executed.

### missing-quantization-metadata (suspected; new_requirement)

The utility implicitly requires existing quantization_config metadata but does not validate that precondition before writing artifacts.

Trigger: Invoke recompile on an otherwise supported input whose config.json lacks quantization_config and whose assembly reaches metadata writing.

Expected: Reject unsupported input before writing, or supply complete metadata arguments.

Actual: The utility supplies neither cal_rows nor cal_cols nor apply_out_scales. The compiler's fallback accesses cal_rows and raises KeyError after shard writing and auxiliary-file copying.

Locations: 6f77a334156dfc5d93b5acf192b7ddfc26c38900:util/recompile.py — main, 6f77a334156dfc5d93b5acf192b7ddfc26c38900:exllamav3/conversion/compile.py — compile_model

Source evidence: call_d24b382b157f43d893a51bcdb01ace68, call_dc944adf87cd421b8c54da53bfad2b81, call_528e4f822ae14d2da83a69ce7c7446e5, call_f15cffecc6f9437580a15a74537f3836

source_inspection: Compared the new argument builder with the unchanged conversion caller, whose prepare function supplies calibration and output-scale keys. [call_4427c98a82f143c7a6d9748be8b2b1f5, call_dac51fe42a134e58908b6ec290c503fa, call_d24b382b157f43d893a51bcdb01ace68]. Limits: Reach is conditional on successful earlier model construction and tensor assembly.

scalar_transcription: Transcribed the missing-key lookup and observed KeyError('cal_rows'). [call_48c5408733c541cc860ef90b43c97028]. Limits: Did not execute compile_model or filesystem writes.

### inherited-stale-output (suspected; defect)

The new utility carries over the compiler's non-cleaning output-directory behavior.

Trigger: Recompile into a nonempty directory containing shards from an earlier assembly with a different layout.

Expected: The output contains only the newly assembled tensor set, or conflicting artifacts are rejected.

Actual: compile_model only warns about existing files, never removes obsolete shards and writes an index only for multiple shards. SafetensorsCollection scans all *.safetensors rather than relying on the index, allowing stale files to reenter subsequent reads.

Locations: 6f77a334156dfc5d93b5acf192b7ddfc26c38900:exllamav3/conversion/compile.py — compile_model

Source evidence: call_528e4f822ae14d2da83a69ce7c7446e5, call_dc944adf87cd421b8c54da53bfad2b81, call_d24b382b157f43d893a51bcdb01ace68, call_e2b82f9a5c4640a1a4af99ea7d850ef1

source_inspection: Compared the root entry's recorded hazard with parent source and the complete task diff: output cleanup remains absent, and the new utility directly reaches this compiler. [call_de68f82eea73407aab801f308da3fc15, call_528e4f822ae14d2da83a69ce7c7446e5, call_dc944adf87cd421b8c54da53bfad2b81, call_4427c98a82f143c7a6d9748be8b2b1f5]. Limits: Filesystem execution and duplicate-file scan ordering were not tested.

## Uncertainty and limits

No repository recompilation, tensor loading, filesystem round trip or GPU execution was performed. The Python check transcribes bounded dictionary and size arithmetic only.

Replacement tensors are not validated for architectural or shape compatibility by the utility. No concrete checkpoint combination was tested.

The utility constructs only Model.from_config's default text component; preservation of every multimodal component was not established.

Retained calibration, version and experimental metadata describe the original input configuration, not necessarily the provenance of substituted tensors.
