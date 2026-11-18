# fce1b96e3fa533e9d3e371b640d3a48c4f97eae7


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/fce1b96e3fa533e9d3e371b640d3a48c4f97eae7) · [Evidence ledger](draft.json)

Adds half-open module-position bounds and a weight-inspection disable switch while retaining full forwarding and perplexity evaluation. Weight histogram ranges widen to ±4σ; selected state inspections retain an inherited conditional stride mismatch.

- [Select diagnostic modules while retaining the complete forward pass](#prequant-test)

## Problem

The prequantization diagnostic inspected every module and its output state unconditionally. This change adds controls for restricting diagnostic output without restricting the forward pass. [source; call_06db37a9495548c99eef4359033f6794, call_c4188ea4b5714da1a4fe20be5f500026]

## Reasoning

Keeping loading and forwarding outside the new inspection predicates preserves the state needed by later modules and by final perplexity evaluation. The options select observations, not a partial model execution. [source; call_06db37a9495548c99eef4359033f6794, call_c4188ea4b5714da1a4fe20be5f500026]

## Impact

Default arguments retain inspection of all modules and states. Weight comparison histograms change even with defaults: their displayed range expands from ±3 to ±4 population standard deviations. [source; call_06db37a9495548c99eef4359033f6794, call_c4188ea4b5714da1a4fe20be5f500026]

## Source Notes

Read ancestor entry 34d2f1f5fa069b842b8791de8c8db499b3884579, which introduced the diagnostic and its Hessian-free, skipped-global-scale regularization path. It records both a conditional hidden-state histogram stride defect and an unbound verbose-reporting variable. [ancestor; call_f9cfba774e8241e49741efc1ad65c40b]

The task leaves both recorded mechanisms unchanged. inspect_state still slices without requesting contiguity; regularize still reads mse_scale under verbose after its skipped-search branch assigns only g_scale. The diagnostic supplies verbose=False, so its regularization call does not select that latter failing combination. [source; call_c4188ea4b5714da1a4fe20be5f500026, call_4c87ff2433cc4ce58e33e3f7bfd2c09f, call_06db37a9495548c99eef4359033f6794]

PR #26, “Superior 3INST parameters,” discusses decoder parameters and regularize's scaling decisions. Its relationship here is inferred from the same regularize implementation called by inspect_module; it does not establish a motivation for these new CLI options. [inference; call_dcb9dd4860284c5aa35d53dfdb5903c6, call_468e5bd7de5d40e7b3cf4721fc657467, call_c4188ea4b5714da1a4fe20be5f500026]

Issue #34, “torch._C._LinAlgError on last layer of quant,” and issue #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” report conversion failures. Their relevance is inferred from nonfinite-state diagnostics and tracebacks naming quantize.py, whose regularize function this script uses. Neither report establishes that this options-only change repairs those failures. [inference; call_fb69739c5edf4393ba76269e720b4b20, call_1ce8edf035004a6c832dba80518aff51, call_c4188ea4b5714da1a4fe20be5f500026, call_06db37a9495548c99eef4359033f6794]

<a id="prequant-test"></a>

## Select diagnostic modules while retaining the complete forward pass

The parser adds integer -fl/--from_layer and -tl/--to_layer, both defaulting to None, plus the store_true switch -nim/--no_inspect_modules. The interval includes from_layer and excludes to_layer. [source; call_06db37a9495548c99eef4359033f6794]

Despite their names, the bounds compare against idx from enumerate(model.modules): they select zero-based top-level module positions, not an explicitly resolved decoder-layer number. No validation rejects negative or reversed bounds; the comparison predicates determine the resulting selection. [source; call_c4188ea4b5714da1a4fe20be5f500026, call_06db37a9495548c99eef4359033f6794]

Both bounds gate inspect_module before forwarding and inspect_state afterward. no_inspect_modules gates only inspect_module, leaving selected state diagnostics enabled. Thus it skips Linear weight extraction, weight statistics, random-sign preparation and diagnostic regularization, rather than merely suppressing their printed output. [source; call_06db37a9495548c99eef4359033f6794, call_c4188ea4b5714da1a4fe20be5f500026]

Every module is still loaded, prepared for its device, forwarded and unloaded; tensor-cache cleanup remains unconditional. Final next-token perplexity still uses the resulting final state. The existing skip_tokens option remains local to hidden-state inspection. [source; call_c4188ea4b5714da1a4fe20be5f500026, call_06db37a9495548c99eef4359033f6794]

inspect_module expands both original-weight and regularized-weight histogram ranges to ±4 times each tensor's own population standard deviation, centered on zero rather than on its mean. Bin counts remain histogram_bins // 2 per chart. The hidden-state histogram's middle range remains ±3 standard deviations, and the absolute regularized-outlier thresholds 4 and 8 are unchanged. [source; call_06db37a9495548c99eef4359033f6794, call_c4188ea4b5714da1a4fe20be5f500026]

Weight histograms pass exclusive=False. The native kernel clamps out-of-range samples into edge bins, so expanding the range changes bucket assignment rather than admitting previously discarded finite samples. At a fixed bin count, the tradeoff is wider coverage with coarser interior resolution; each chart remains independently normalized to its maximum bin count. [source; call_2ae5e87fc3da4461993d53d4bdb24c4a, call_c4188ea4b5714da1a4fe20be5f500026, call_06db37a9495548c99eef4359033f6794]

A standard-library transcription selected positions 2 and 3 for bounds [2,4), retained those state selections with module inspection disabled, and selected nothing for reversed bounds [4,2). With the default 160 histogram bins, each weight chart has 80 bins: nominal width grows from 0.075σ to 0.1σ, a factor of 4/3. [execution; call_588d69fb4ee948b9813f46333ede90f6]

The new gates narrow exposure to the inherited hidden-state stride issue but do not repair it: selected inspect_state calls retain the same slicing and native histogram path. Whole-parent-tree search located only main's direct inspect_state call. [source; call_1d69bb7fc2204ab09bcd962586faeee6, call_c4188ea4b5714da1a4fe20be5f500026, call_2ae5e87fc3da4461993d53d4bdb24c4a, call_06db37a9495548c99eef4359033f6794]

## Authoring-time findings — pending review

### retained-state-histogram-strides (suspected; defect)

Selected hidden-state inspections retain the inherited mismatch between sliced tensor strides and contiguous native histogram traversal.

Trigger: An inspected state has multiple rows and a positive skip_tokens smaller than the context length, and conversion to the selected device leaves the sliced view's row gaps intact.

Expected: Histogram all and only the selected token suffixes from every row.

Actual: inspect_state does not request contiguity. histogram_kernel reads input_ptr[i] for numel elements without consulting strides, potentially counting skipped tokens from subsequent rows while omitting selected trailing elements.

Locations: fce1b96e3fa533e9d3e371b640d3a48c4f97eae7:eval/prequant_test.py — inspect_state, 463ebe1841ebe115ac46ccf91e1a40f68199c16a:exllamav3/exllamav3_ext/histogram.cu — histogram_kernel

Source evidence: call_c4188ea4b5714da1a4fe20be5f500026, call_2ae5e87fc3da4461993d53d4bdb24c4a, call_06db37a9495548c99eef4359033f6794, call_1d69bb7fc2204ab09bcd962586faeee6

source_inspection: Compared the unchanged slice and raw-pointer kernel with main's newly gated direct call. The defect remains conditional within the selected interval; no_inspect_modules does not disable this call. [call_c4188ea4b5714da1a4fe20be5f500026, call_2ae5e87fc3da4461993d53d4bdb24c4a, call_06db37a9495548c99eef4359033f6794, call_1d69bb7fc2204ab09bcd962586faeee6]. Limits: Literal search establishes the located direct caller, not external callers or actual device-copy behavior.

scalar_transcription: Modeled a contiguous [2,3,2] array with one skipped token per row. Selected elements sum to 52; contiguous traversal from the slice offset sums to 44. [call_588d69fb4ee948b9813f46333ede90f6]. Limits: Python indexing model only; neither Torch slicing nor the CUDA implementation ran.

## Uncertainty and limits

No repository implementation, Torch operation, CUDA kernel, model evaluation or terminal rendering was executed. The Python check models predicates, bin-width arithmetic and flattened indexing only.

The inspected evidence supplies no empirical justification for choosing four rather than three standard deviations.

Whether inspect_state's device conversion materializes a contiguous copy was not executed; the stride observation is conditional on the sliced view retaining its row gaps.
