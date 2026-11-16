# 40cfec594e0063ed6f31f58318dc058e93aed13a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/40cfec594e0063ed6f31f58318dc058e93aed13a) · [Evidence ledger](draft.json)

Adds a float16/float32 CUDA counting histogram and optional codebook references, fixes the prior reference/output length mismatch, and leaves a suspected zero-bin validation gap.

- [Standalone counts and optional reference distributions](#histogram)

## Problem

The existing distribution diagnostic always computed a normalized codebook reference. This change adds standalone integer histogram counts and makes that reference optional. [source; call_794ab0532f894b95ba6742814142abc4, call_21f5d55bf1de4b48ba71d769c06b38e2]

## Reasoning

A single CUDA block accumulates counts in shared memory, avoiding a separate inter-block reduction. This favors implementation simplicity over scalable parallelism. [inference; call_794ab0532f894b95ba6742814142abc4]

## Impact

The extension exposes histogram(input, output, min_value, max_value, exclusive). No Python workflow integration is added; the parent-tree test_distribution search finds only native declarations, its binding and a commented Python call. [source; call_794ab0532f894b95ba6742814142abc4, call_69f3bb614c824510b60f417c8b707cbf, call_9df6b2acd7f749839f64f92b87d8e670]

## Source Notes

The earlier 00bbb583 entry establishes the original diagnostic's two normalized histograms and records an unchecked destination-capacity concern. [ancestor; call_7b08654b3ccb4e4b8a9f05f71e7e7e26]

Issues #6 (“No ROCm runtime is found, using ROCM_HOME='/usr'”), #7 (“quantizing model: undefined symbol: __cxa_call_terminate”) and #29 (“Auto-YaRN for Qwen3? Maybe even set it dynamically?”) concern installation or RoPE behavior. Their relationship here is only an inferred shared-file association through rope.py, whose task edit removes GPTJ from a TODO comment, not executable code. [inference; call_8275c394638e408b91a37c39c69bcd69, call_2d2c65778cf34be0ac51da8217354b5b, call_2de42e42a5fc4d7f8b24a072f5c5f224, call_794ab0532f894b95ba6742814142abc4]

PR #26, “Superior 3INST parameters,” discusses codebook experimentation; issues #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” report conversion failures. Their association is inferred from the inspected quantize.py path and codebook context, not an explicit link to this histogram change. [inference; call_0b864ab7c034444481bac04928afa839, call_b58602ca23c045028ff99741cda5777e, call_1c34283a6cc04f27b98d2238528091f0, call_a68a5efcef2e44bb86b03ec2eea32a4a, call_794ab0532f894b95ba6742814142abc4]

<a id="histogram"></a>

## Standalone counts and optional reference distributions

histogram accepts float32 or float16 input and requires a kLong output, despite the comment describing uint64_t. It uses the input device/current CUDA stream, derives the bin count from output.numel(), and launches one block of 1024 threads. Each thread traverses every 1024th input element; shared unsigned 64-bit counters are cleared, atomically incremented and copied over the output. [source; call_794ab0532f894b95ba6742814142abc4]

For ordinary finite values and a positive range, indexing truncates (value-min)/(max-min)*num_bins and clamps to the endpoint bins. exclusive=true discards values strictly outside the range but retains both endpoints; false folds outliers into endpoint counts. Unlike test_distribution, these outputs are counts, not normalized probability masses. [source; call_794ab0532f894b95ba6742814142abc4, call_21f5d55bf1de4b48ba71d769c06b38e2]

A scalar transcription with four bins over [-1,1] and samples [-2,-1,-0.5,0,0.5,1,2] produced [2,1,1,3] without exclusion and [1,1,1,2] with exclusion. Arithmetic also confirms 8192 bytes for 1024 eight-byte counters and 64 reference states per thread when enumerating all 65,536 uint16 states. [execution; call_7de5e67c65ce459c8c3b2e23d40ce152]

test_distribution now accepts an optional reference tensor. OPTPTR maps an absent value to nullptr, and a uniform pointer guard skips reference clearing, decoding and writing. Bin count now comes from dist_output, with equal element counts checked when the reference pointer is non-null. These coordinated changes let input-only diagnostics run without a reference allocation. [source; call_794ab0532f894b95ba6742814142abc4, call_21c6b75e802a41d092e7470136e1523d]

The header and implementation agree on the changed signature, while the binding still exposes the same function name. The only Python call found remains commented and supplies the older five-argument form, omitting the two multiplier arguments already required in the parent; it is not an active compatible caller. [source; call_69f3bb614c824510b60f417c8b707cbf, call_9df6b2acd7f749839f64f92b87d8e670, call_21f5d55bf1de4b48ba71d769c06b38e2, call_794ab0532f894b95ba6742814142abc4]

The specific undersized-dist_output scenario recorded by the ancestor entry is removed for non-null reference buffers: the task derives the write length from dist_output and rejects unequal reference lengths before launch. This does not establish comprehensive tensor validation. [source; call_794ab0532f894b95ba6742814142abc4, call_21f5d55bf1de4b48ba71d769c06b38e2]

## Authoring-time findings — pending review

### histogram-zero-bins (suspected; defect)

The new histogram wrapper permits zero bins although counting requires a valid bin.

Trigger: Call histogram with nonempty contiguous CUDA float input, an empty kLong output, min_value=0, max_value=1 and exclusive=false.

Expected: Reject the zero-bin output before launching.

Actual: The sole bin-count guard accepts zero. For an input value of zero, idx becomes zero, the unsigned comparison succeeds, and num_bins-1 underflows before assignment to idx; the subsequent atomic update has no valid initialized histogram bin. Reach is direct extension callers; no parent-tree callers of the new utility were found.

Locations: 40cfec594e0063ed6f31f58318dc058e93aed13a:exllamav3/exllamav3_ext/histogram.cu — histogram_kernel

Source evidence: call_794ab0532f894b95ba6742814142abc4, call_55f038bcf6d34ec3968be191c30c518d

source_inspection: Traced output.numel() through the upper-bound-only check, shared-memory initialization and index clamp. [call_794ab0532f894b95ba6742814142abc4]. Limits: No malformed CUDA invocation was executed; the resulting device error or memory effect is unmeasured.

## Uncertainty and limits

No extension build or CUDA execution was performed; launch success, synchronization behavior and performance remain unmeasured.

The scalar transcription uses small, exactly representable finite values. It does not establish CUDA float-to-integer behavior for nonfinite or extreme values, counter overflow, or invalid ranges.

Literal caller searches do not exclude external or dynamically constructed extension calls.
