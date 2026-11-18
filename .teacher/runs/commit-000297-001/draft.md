# 6341b119efc4ef73ff2e4adcdd14a4d79b0a5e6d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6341b119efc4ef73ff2e4adcdd14a4d79b0a5e6d) · [Evidence ledger](draft.json)

Adds YAML wildcard tensor overrides and loader forwarding. Source inspection identifies missing override metrics and retained metrics/API and BF16-tail limitations.

- [YAML-controlled tensor-source routing](#loading)

## Problem

Selective tensor-source replacement previously required a programmatic prefix map. The change adds YAML-driven overrides to shared initialization and model comparison. [source; call_b2b96b609b624b048fe27ee1efa18c48, call_56bb358af7214a86bbbcc59c72f990f4, call_8c2c586a8cee4fbfb72671e2f84daec6]

## Reasoning

A default collection plus filtered replacement collections allows selective substitution without constructing a merged checkpoint. Forwarding deferred-load operations is necessary because existing model loading brackets tensor requests with those operations. [inference; call_eb5f8b3812474d3488c2f50cff9831df, call_bea39925058242c3be968c70cdd09d9b]

## Impact

Shared initialization gains -or/--override; model_diff applies it only to model A. Both dependency declarations add pyyaml for the new yaml imports. [source; call_56bb358af7214a86bbbcc59c72f990f4, call_8c2c586a8cee4fbfb72671e2f84daec6, call_7cd2e8bdf31d4b3991a2b92cba7f5aea, call_d62c808be81d4a4594bf9fe3e063ae65]

## Source Notes

The root loading-tokenization entry describes the original longest-prefix variant routing. The metrics entry records stale metrics wrappers and an odd-element CUDA BF16 conversion gap. The measures entry establishes the pre-existing model_diff diagnostics. [ancestor; call_0f64fbdd884b47feb1103da1e28d0eea, call_251da69d1def4a969c26c7e5d5091468, call_fa62a6ad591d42a0865ceeb9fddad74b]

Fresh source inspection shows that the task removes VariantSafetensorsCollection.get_metrics, leaves Model.get_load_metrics calling the absent method, and preserves the pair-only BF16 conversion reached by forwarded deferred loads. [source; call_eb5f8b3812474d3488c2f50cff9831df, call_bea39925058242c3be968c70cdd09d9b, call_b2b96b609b624b048fe27ee1efa18c48, call_f4e29b158bf34a9f9412a298d783e785, call_4b28f2dc53a146df94ec621fc5e64141]

<a id="loading"></a>

## YAML-controlled tensor-source routing

Both consumers safe-load YAML, map source IDs to model directories, resolve override keys to directories, and group filters by directory. They create one replacement collection per distinct directory and install a wrapper only when overrides are nonempty. [source; call_56bb358af7214a86bbbcc59c72f990f4, call_8c2c586a8cee4fbfb72671e2f84daec6]

The example selects attention tensors and particular layer indices from one source. These indices identify layers; they are not performance thresholds. [source; call_c250bf3fcf79450bac824e0f0cbe1d87]

VariantSafetensorsCollection now accepts a main collection. add_stc prepends filter/source pairs; find_stc returns the first fnmatch match or main. This replaces longest raw-prefix precedence with reverse source-addition precedence. Because consumers group rows by directory, priority is not simply the order of individual YAML rows. [source; call_eb5f8b3812474d3488c2f50cff9831df, call_b2b96b609b624b048fe27ee1efa18c48, call_56bb358af7214a86bbbcc59c72f990f4]

A standard-library transcription confirmed wildcard matching across dotted tensor names, B-before-A priority after grouping synthetic A/B/A rules, and main-source selection for an unmatched key. [execution; call_100f8dbe53f54c7193daa5a0f1a3342d]

Selection is authoritative: existence checks and tensor reads inspect the chosen collection without falling back when it lacks the key. Required reads retain the underlying missing-tensor error; optional reads retain None. Alternative suffix groups now support Linear.is_exl3_storage's su/suh and sv/svh checks. [source; call_eb5f8b3812474d3488c2f50cff9831df, call_b2b96b609b624b048fe27ee1efa18c48, call_1db9d6e920d049109d070b4a33b9df89]

get_tensor forwards conversion, transpose, padding and no_defer arguments. Bulk reads and metadata listings enumerate main's names and then resolve each replacement, rather than forming a union of source namespaces. Replacement-only names are therefore omitted from those bulk operations. max_key_len also remains main-based. [source; call_eb5f8b3812474d3488c2f50cff9831df, call_1db9d6e920d049109d070b4a33b9df89]

Deferred begin/end/abort and close fan out to all replacement collections and main. Model's existing loading paths use these operations; autosplit aborts pending work on exceptions. model_diff already brackets each module load with deferred begin/end. [source; call_eb5f8b3812474d3488c2f50cff9831df, call_bea39925058242c3be968c70cdd09d9b, call_80411d14ff7248f7b9c0d2d8f3b7a4f3]

Shared initialization installs the wrapper before Model.from_config. model_diff installs it after constructing model A but before loading modules; Model stores the same config object, so later config.stc accesses observe the replacement. [source; call_56bb358af7214a86bbbcc59c72f990f4, call_8c2c586a8cee4fbfb72671e2f84daec6, call_bea39925058242c3be968c70cdd09d9b]

Config's st_variants branch is removed. Whole-parent-tree searches found that constructor use only in Config and no other st_variants occurrence. External callers supplying that keyword no longer select variants. The new wrapper explicitly rejects set_new_tensors. [source; call_3ea4a873f62a40089ed8baf8efb6b1e6, call_ab30d820f3944075950fae58606af123, call_30b113363b564ecca1a0a7b3bf252c97, call_eb5f8b3812474d3488c2f50cff9831df]

The parent-tree yaml search found no occurrence. The task adds unconditional yaml imports to model_init and model_diff, including invocations that do not request overrides. [source; call_27901eb0137f48a3ac5b30be0cdbf4b7, call_56bb358af7214a86bbbcc59c72f990f4, call_8c2c586a8cee4fbfb72671e2f84daec6]

## Authoring-time findings — pending review

### override-load-metrics (suspected; defect)

The new wrapper does not supply the metrics attribute consumed by shared initialization.

Trigger: Use nonempty overrides with -lm/--load_metrics and reach the metrics block.

Expected: Print loader metrics and return initialized objects.

Actual: config.stc.metrics.print() accesses a missing attribute: the wrapper skips the base constructor and initializes only main and stcs.

Locations: 6341b119efc4ef73ff2e4adcdd14a4d79b0a5e6d:exllamav3/loader/safetensors.py — VariantSafetensorsCollection.__init__, 6341b119efc4ef73ff2e4adcdd14a4d79b0a5e6d:exllamav3/model_init.py — init

Source evidence: call_eb5f8b3812474d3488c2f50cff9831df, call_234c7be613f341509388b9646590be32, call_56bb358af7214a86bbbcc59c72f990f4

source_inspection: Compared the complete wrapper changes with the unchanged metrics consumer. The caller search locates shared initialization in six evaluation/example scripts; imgsearch directly calls init with arguments built by add_args. [call_eb5f8b3812474d3488c2f50cff9831df, call_234c7be613f341509388b9646590be32, call_741017230f8945c2aacb84aa6bb73e37, call_09e07a1ad0c04ddf99b0a11a9fa6b088]. Limits: Source-derived, conditional on reaching the metrics block; not executed.

### inherited-model-metrics-wrapper (suspected; defect)

Model.get_load_metrics remains incompatible with the collection API.

Trigger: Call Model.get_load_metrics with an ordinary or new variant collection.

Expected: Return load metrics.

Actual: Model calls stc.get_metrics(), absent from the ordinary collection and removed from the variant collection by this task.

Locations: 6341b119efc4ef73ff2e4adcdd14a4d79b0a5e6d:exllamav3/models/model.py — Model.get_load_metrics

Source evidence: call_bea39925058242c3be968c70cdd09d9b, call_b2b96b609b624b048fe27ee1efa18c48, call_eb5f8b3812474d3488c2f50cff9831df

source_inspection: Inspected Model.get_load_metrics, the complete parent collection implementation and the removal of the variant method. The tree-wide stc search identifies the stale Model call. [call_bea39925058242c3be968c70cdd09d9b, call_b2b96b609b624b048fe27ee1efa18c48, call_eb5f8b3812474d3488c2f50cff9831df, call_a2461ec13b19490290ee22e3bad944eb]. Limits: API-level trigger; no external caller or repository execution demonstrated.

### inherited-deferred-bf16-tail (suspected; defect)

The forwarded deferred-loading path retains pair-only CUDA BF16 conversion.

Trigger: Deferred CUDA loading of an odd-element BF16 tensor with allow_bf16 false.

Expected: Convert every element to FP16.

Actual: The helper converts floor(numel/2) pairs, leaving an odd final element unconverted.

Locations: 6341b119efc4ef73ff2e4adcdd14a4d79b0a5e6d:exllamav3/exllamav3_ext/stloader_cu.cu — inplace_bf16_to_fp16_cuda

Source evidence: call_f4e29b158bf34a9f9412a298d783e785, call_4b28f2dc53a146df94ec621fc5e64141, call_b2b96b609b624b048fe27ee1efa18c48, call_eb5f8b3812474d3488c2f50cff9831df

source_inspection: Located the native callers, inspected the deferred CUDA caller and conversion helper, and compared the unchanged Python deferred mechanism with the wrapper's new forwarding. [call_493a788ee49e48e298ffd0111d09168c, call_4b28f2dc53a146df94ec621fc5e64141, call_f4e29b158bf34a9f9412a298d783e785, call_b2b96b609b624b048fe27ee1efa18c48, call_eb5f8b3812474d3488c2f50cff9831df]. Limits: No affected checkpoint or GPU execution established.

scalar_transcription: Python pair-coverage arithmetic leaves one uncovered element for counts 1, 3 and 1048577, and none for count 2. [call_100f8dbe53f54c7193daa5a0f1a3342d]. Limits: Arithmetic model only; it does not execute the kernel or establish launch behavior.

## Uncertainty and limits

No repository loader, YAML parser, checkpoint load or GPU kernel was executed. The successful Python computation transcribed routing and pair-coverage arithmetic only.

Replacement checkpoint dimensions and architectural compatibility were not validated.

Searches establish inspected in-tree references, not compatibility with external callers or dynamically constructed arguments.

Only initial portions of the lengthy PR #26 and issue #33 discussions were inspected; they do not establish this change's motivation.
