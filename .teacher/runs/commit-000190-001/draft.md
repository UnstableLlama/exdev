# c94905bf794f3b3bee00cd1f6645e624cc33cd12


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c94905bf794f3b3bee00cd1f6645e624cc33cd12) · [Evidence ledger](draft.json)

RMSNorm removes Python reshape bookkeeping by calculating flattened row counts natively; kernel arithmetic is unchanged and performance remains unmeasured.

- [Move RMSNorm flattening bookkeeping into the native wrapper](#rmsnorm)

## Problem

RMSNorm.forward flattened its input and restored its output shape through Python view operations even though the kernel already addresses contiguous rows. [source; call_c9e24392fc914c0ba21a5e41393ee840, call_634269edcc324c46a7afecba795e57d0]

## Reasoning

The edits are coupled: removing Python flattening requires the native wrapper to derive width from the last dimension and multiply all preceding dimensions into its row count. [source; call_7a53daeebf4b4d1ab6257df5fa819892, call_9c4f6c0bc47d4f4ea9dfcc7c562fa167]

## Impact

This removes Python shape bookkeeping and two view operations without changing the normalization kernel. Reduced CPU overhead is plausible, but no speedup was measured. [inference; call_7a53daeebf4b4d1ab6257df5fa819892, call_9c4f6c0bc47d4f4ea9dfcc7c562fa167]

## Source Notes

The root runtime entry was read. It describes vectorized RMSNorm and records the non-float-as-half dtype classification; inspection of the parent and task diff shows that classification is carried over unchanged. [source; call_0d10b940a4644d08bdde640243932677, call_634269edcc324c46a7afecba795e57d0, call_7a53daeebf4b4d1ab6257df5fa819892]

<a id="rmsnorm"></a>

## Move RMSNorm flattening bookkeeping into the native wrapper

forward now allocates empty_like directly from the original input and returns that tensor directly. Output dtype selection, epsilon, weights and constant bias are unchanged; params remains unused and only loses its dict annotation. [source; call_c9e24392fc914c0ba21a5e41393ee840, call_9c4f6c0bc47d4f4ea9dfcc7c562fa167]

Native validation now requires matching complete input/output shapes, last-axis width matching weight axis zero, and width divisible by four. The full-shape macro compares tensor sizes, not merely element counts. [source; call_7a53daeebf4b4d1ab6257df5fa819892, call_a7f241ed06934a76b791b14c5018eee7]

The unchanged kernel launches one 1,024-thread block per flattened row. Four is the vector width of its half4/float4 loads and stores; each row computes x × (w + constant_bias) / sqrt(mean(x²) + epsilon), with float accumulation and separate half/float input-output instantiations. [source; call_634269edcc324c46a7afecba795e57d0]

A standard-library scalar transcription checked 255 positive shapes of ranks one through four: multiplying leading dimensions and using row × width plus four-element vector offsets covered contiguous storage exactly. [execution; call_7bebbbd0917f4672a51846e23f367e77]

Whole-tree rms_norm search located the module wrapper and direct extension tests. The wrapper supplies all five arguments and creates matching output shapes. Tests use matching two-dimensional buffers, which agree with the revised shape convention, but their four-argument calls remain incompatible with the inspected five-argument native declaration. [source; call_267298af90414317bbcb87eeddb066c3, call_c9e24392fc914c0ba21a5e41393ee840, call_cb1a838725944a08b5d116960b2185d0, call_aef9ab0f600441d594311d959b65286c]

## Authoring-time findings — pending review

### inherited-dtype-dispatch (suspected; defect)

The native wrapper still treats every non-float dtype as half.

Trigger: Calling rms_norm with input or output other than float32 or float16 while satisfying its shape and weight checks.

Expected: Reject unsupported input/output dtypes.

Actual: Dispatch selects half pointers for non-float tensors; the final invalid-dtype branch cannot reject them.

Locations: c94905bf794f3b3bee00cd1f6645e624cc33cd12:exllamav3/exllamav3_ext/norm.cu — rms_norm

Source evidence: call_634269edcc324c46a7afecba795e57d0, call_7a53daeebf4b4d1ab6257df5fa819892

source_inspection: Compared unchanged dtype dispatch with the task diff and inspected located direct callers. RMSNorm.forward adds no dtype guard; tests supply only half/float. [call_267298af90414317bbcb87eeddb066c3, call_c9e24392fc914c0ba21a5e41393ee840, call_cb1a838725944a08b5d116960b2185d0]. Limits: No unsupported-dtype invocation or broader model workflow was executed.

### inherited-test-argument-mismatch (suspected; defect)

Existing direct extension tests omit constant_bias.

Trigger: Running test_rms_norm or its benchmark against the inspected native binding.

Expected: Tests invoke the five-argument RMSNorm interface.

Actual: All three test call sites pass only four arguments; the native declaration requires five and the located binding supplies no default.

Locations: d54648bfaba4ab016fc3345938cc9c0f1b02be48:tests/test_ext_norm.py — test_rms_norm

Source evidence: call_cb1a838725944a08b5d116960b2185d0, call_aef9ab0f600441d594311d959b65286c, call_267298af90414317bbcb87eeddb066c3

source_inspection: Compared all located extension calls with the declaration. The production Python wrapper supplies constant_bias; the task does not modify the tests. [call_c9e24392fc914c0ba21a5e41393ee840, call_cb1a838725944a08b5d116960b2185d0, call_aef9ab0f600441d594311d959b65286c]. Limits: Argument-binding failure was not executed.

## Uncertainty and limits

No extension build, GPU execution, numerical comparison or timing was performed.

The scalar check covers small contiguous shapes with Python integers; it does not establish strided-layout behavior, native integer-overflow behavior or GPU arithmetic.

The inspected native callers are RMSNorm.forward and extension tests; broader model entry-point compatibility was not exhaustively traced.
