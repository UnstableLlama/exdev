# d860f8e1e106a45536603cd8069fc9ef43105fd9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d860f8e1e106a45536603cd8069fc9ef43105fd9) · [Evidence ledger](draft.json)

Adds optional 128×128 block scaling to ordinary Linear loading while retaining dense FP16 execution. Inspection identifies missing FP8 file-dtype support, premature scaling during deferred loads, and a conditional scale-orientation mismatch.

- [Block scales at the dense-weight loading boundary](#loading)

## Problem

The ordinary Linear loading path previously ignored companion weight scales. This change adds optional weight_scale_inv loading and blockwise multiplication, but does not establish complete FP8 checkpoint support. [source; call_4df611a1a55e4b06abd1e1067e8526e0, call_7b2093a566444ba890430ad0d6f037ff]

## Reasoning

Scaling is performed during loading so the existing LinearFP16 implementation can consume the resulting dense matrix without a new inference kernel. The helper mutates a view of the original weight; its returned four-dimensional view is deliberately not assigned by the caller. [source; call_4df611a1a55e4b06abd1e1067e8526e0, call_5b8df967d5c942a8ba92189b864792f2]

## Impact

Absent scales preserve the previous path. Present scales affect primary or alternate ordinary weights before LinearFP16 construction and CPU slice extraction. EXL3 loading still takes precedence, and the fused-weight fallback does not load scales. [source; call_4273dba6af6449679bf48e7b318a708f, call_4df611a1a55e4b06abd1e1067e8526e0, call_5b8df967d5c942a8ba92189b864792f2]

## Source Notes

Read the initial modules entry and the sliced-loading fix entry. They establish the storage-independent Linear interface and the prior requirement to preserve full checkpoint dimensions until slice extraction. [ancestor; call_af10566c97c541fdb53d15b8ceff1db0, call_b5ad2285a7d14c61ac0d9895991b3d08]

The refactored dev, pad1 and pad2 variables retain CPU staging and disabled loader padding for sliced linears; these edits support the new scale load rather than changing the slice policy. [source; call_4df611a1a55e4b06abd1e1067e8526e0]

Overlapping discussions concern different failures: #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” concerns quantization padding; #11, “AssertionError: bias is wrong datatype,” concerns bias conversion; #16, “RuntimeError: CUDA error: invalid configuration argument,” was attributed in discussion to tokenizer truncation; #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” concerns slice-padding dimensions. Their relationship here is inferred only from shared linear.py paths, not evidence that this scale patch addresses them. [inference; call_da19d246ca8c464f9dfc3c9bd1db0e51, call_cd32ced506a648f789a3befb3675658a, call_95672934dc5a444ab424964fb3892a4d, call_7108deb2fc574ee09378a44815474aca, call_4df611a1a55e4b06abd1e1067e8526e0]

Other inspected discussions likewise provide no explicit FP8 connection: #34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure; #33, “Error converting model,” reports file-opening failure and later repetitive GLM4 output; #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension import failure; PR #26, “Superior 3INST parameters,” proposes decoder changes. Connections to this task are inferred solely from shared inspected loading, model or evaluation paths. [inference; call_3ec2884ce72048698098172076815d6e, call_ac6816a8a26c478088c399814de83708, call_110bc7acff054af98943322ea26041f9, call_f1f78238ed7348c4b27e165d10efc357, call_4e55f898318f40baa020308cb8d9cdd2, call_7475b5d041134caaa766d14c47618b37]

<a id="loading"></a>

## Block scales at the dense-weight loading boundary

apply_fp8_scales_ requires two-dimensional tensors and exact weight dimensions equal to 128 times the corresponding scale dimensions. Reshaping to [scale_rows,128,scale_columns,128] and broadcasting [scale_rows,1,scale_columns,1] applies one multiplier per 128×128 block. The constant is a block edge length, not a dispatch threshold; the code multiplies by scale_inv rather than taking its reciprocal. [source; call_4df611a1a55e4b06abd1e1067e8526e0]

Weights are requested with transposition and, for unsliced layers, padding before scaling. Scales are requested without either transformation. Consequently the helper requires scales aligned with the already-transposed, possibly padded weight, not merely with its original file shape. [source; call_4df611a1a55e4b06abd1e1067e8526e0, call_7b2093a566444ba890430ad0d6f037ff]

A bounded integer check verified the block-view address identity for a 256×384 matrix. It also showed that a 2×3 scale grid accepts 256×384 but rejects its transpose, and that leaving an asymmetric 2×2 checkpoint-oriented grid untransposed changes scale assignments for 32,768 of 65,536 elements. [execution; call_701d650ac2824dc0bf1f03c6e1fa2c4f]

LinearFP16 retains a two-dimensional weight for matrix multiplication, slicing and export. Ignoring the helper's return preserves that representation while sharing the modified storage. Conversion subsequently obtains that same dense weight through get_weight_tensor. [source; call_4df611a1a55e4b06abd1e1067e8526e0, call_5b8df967d5c942a8ba92189b864792f2, call_4273dba6af6449679bf48e7b318a708f]

## Authoring-time findings — pending review

### fp8-dtype-not-loadable (suspected; defect)

The new scale operation does not supply the missing file-dtype support needed to load actual FP8 weights.

Trigger: Linear.load selects ordinary weights whose safetensors dtype is an FP8 identifier.

Expected: Decode the FP8 weights into a supported dense dtype and apply the companion scales.

Actual: SafetensorsCollection.get_tensor calls convert_dtype first. It recognizes only I32, I16, F16, BF16 and F32, and raises ValueError for other identifiers before the scale helper can run. This inherited loader restriction remains unchanged.

Locations: d860f8e1e106a45536603cd8069fc9ef43105fd9:exllamav3/modules/linear.py — Linear.load_fp16, e1d2fa11d6573ea1aeaddacffc028e08a83f91b1:exllamav3/loader/safetensors.py — convert_dtype

Source evidence: call_4df611a1a55e4b06abd1e1067e8526e0, call_7b2093a566444ba890430ad0d6f037ff, call_db36d70c67da40ff957ccd8dfb627c03

source_inspection: Traced the sole parent-tree load_fp16 caller, Linear.load, through get_tensor to dtype conversion. The restriction affects file-backed FP8 loads, not necessarily injected new_tensors. [call_db36d70c67da40ff957ccd8dfb627c03, call_4273dba6af6449679bf48e7b318a708f, call_7b2093a566444ba890430ad0d6f037ff]. Limits: No actual FP8 checkpoint was loaded.

### scaling-before-deferred-read (suspected; defect)

Scaling runs before deferred weight and scale reads complete.

Trigger: A file-backed ordinary linear with a present, shape-compatible scale tensor is loaded with mt_fread and deferred_mode enabled, using dtypes already accepted by the loader.

Expected: Multiply populated weight blocks by populated scales and retain that result.

Actual: Both get_tensor calls can return allocated placeholders. The helper immediately multiplies them, while end_deferred_load later copies the unscaled transposed weight into the destination, overwriting the operation.

Locations: d860f8e1e106a45536603cd8069fc9ef43105fd9:exllamav3/modules/linear.py — Linear.load_fp16

Source evidence: call_4df611a1a55e4b06abd1e1067e8526e0, call_7b2093a566444ba890430ad0d6f037ff

source_inspection: Inspected Linear.load, recursive Module.load, Model._load_single and _load_autosplit, and both model_diff load sequences. They place module loading between begin_deferred_load and end_deferred_load. Unsliced linears permit deferral; sliced linears normally disable it through can_defer_load. [call_db36d70c67da40ff957ccd8dfb627c03, call_5121f05abbf9423a814da15b61d03613, call_dd03e6726e494cba9239ae04f8d980c4, call_4c523cccc8404ae7aa67d7ded8ad110d, call_2d412c38dd284bf4bd39d1f4e9464236, call_4273dba6af6449679bf48e7b318a708f]. Limits: Source ordering only; no asynchronous loader or tensor operation was executed.

### scale-orientation-contract (suspected; external_compatibility)

Checkpoint-oriented block scales are not transposed alongside their weights.

Trigger: An eagerly loaded checkpoint supplies a scale grid aligned with its original [out_features,in_features] weight rather than the internal transposed matrix.

Expected: Preserve each weight block's associated scale through transposition.

Actual: A rectangular grid can fail the shape assertion; a square asymmetric grid passes but assigns off-diagonal block scales to the wrong blocks.

Locations: d860f8e1e106a45536603cd8069fc9ef43105fd9:exllamav3/modules/linear.py — Linear.apply_fp8_scales_

Source evidence: call_4df611a1a55e4b06abd1e1067e8526e0, call_7b2093a566444ba890430ad0d6f037ff

scalar_transcription: Modeled the exact 128-block shape condition and compared transposed versus untransposed scale indexing. The helper is new; parent search found no existing callers, and the task adds only the load_fp16 call. [call_701d650ac2824dc0bf1f03c6e1fa2c4f, call_676d3ee37f76422da21a2784a5b7f525, call_4df611a1a55e4b06abd1e1067e8526e0]. Limits: Conditional compatibility observation: no inspected checkpoint establishes that it uses this orientation.

## Uncertainty and limits

No PyTorch, native loader, GPU kernel or complete model load was executed. The standard-library check models indexing and shapes only, not FP16 rounding, overflow or asynchronous execution.

No checkpoint header or format specification establishes the intended scale orientation, FP8 encoding or coverage of partial edge blocks.
