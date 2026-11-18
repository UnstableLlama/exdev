# 1e1e68b3921da92286b2f50958239eec262a13a1


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1e1e68b3921da92286b2f50958239eec262a13a1) · [Evidence ledger](draft.json)

Repairs fused FP16 loading by forwarding resolved dimension and offset metadata to LinearFP16 and materializing its transposed weight contiguously. The source explains #55's constructor failure; end-to-end conversion remains untested.

- [Restore the fused FP16 constructor contract](#loading)

## Problem

The fused-weight fallback in Linear.load_fp16 omitted full dimensions when constructing LinearFP16. Its constructor defaults those arguments to None but compares them with integer feature counts, causing a TypeError before loading can finish. [source; call_910622c82424453293e25ae7a77adac7, call_10c06379ad674378813d7b9cb2337d62]

## Reasoning

The patch forwards the outer Linear's resolved full dimensions and feature offsets, matching the existing ordinary-weight call. It also materializes the transposed fused weight as contiguous storage rather than passing a transpose view. [source; call_2232fc2039c24c8ea1f678281ea61801, call_910622c82424453293e25ae7a77adac7]

## Impact

The change removes the missing-dimension comparison failure from the fused FP16 fallback. It does not change EXL3 loading, ordinary FP16 loading, fused tensor extraction, padding or bias preparation. [source; call_2232fc2039c24c8ea1f678281ea61801, call_910622c82424453293e25ae7a77adac7, call_10c06379ad674378813d7b9cb2337d62]

## Source Notes

Issue #55, “Possible GLM4 32B regression,” was reported by gecfdo as conversion failing in v0.0.4 after working in v0.0.2. Its traceback reaches the fused LinearFP16 construction and the integer-versus-None comparison inspected here. Originalimoc subsequently wrote “Same error,” without additional reproduction details. These are reports, not executions performed for this annotation. [source; call_aca34a2471df4380a3d8861dfb143278, call_e0c9e373ee1444b6b85c89cce3658ac2, call_910622c82424453293e25ae7a77adac7, call_10c06379ad674378813d7b9cb2337d62]

The earlier deferred-loading entry establishes the historical move to loader-side transposition and padding, resolved outer Linear dimensions, and eager fused-weight extraction. The subsequent sliced-loading entry describes disabling loader padding for ordinary sliced weights; it explicitly excludes the fused fallback from its edits. Both entries were read as historical context. [ancestor; call_fef4c9aabbd74a39915b0fc83b3156b9, call_aca2a7ec84704e69950ff92c6dcab7c6]

Closed discussions with overlapping linear.py paths concern other failures: #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” concerns quantization padding; #11, “AssertionError: bias is wrong datatype,” concerns EXL3 bias; #16, “RuntimeError: CUDA error: invalid configuration argument,” was attributed in discussion to tokenizer truncation; #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” concerns padding before slicing; #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” concerns invalid calibration states and Cholesky failure. Their relationship to this task is only an inferred shared-file overlap, not evidence of the same regression. [inference; call_806441b9c41a4b36af73d15f60b0e469, call_a9b0876c7dd94474beb7e9348fe8152c, call_d2f836030e6d4ab0814965921095c6d4, call_bba92890a2e9457580cdb0ccd417e0e0, call_d42c2dfdde944e80b48536d3c9ff6ab1, call_0c5fe84012c74555aa652d6701bd5c1c, call_2232fc2039c24c8ea1f678281ea61801]

Other unreferenced discussions were also read: #34, “torch._C._LinAlgError on last layer of quant”; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values”; #52, “Error converting moonshotai/Kimi-Dev-72B”; #53, “Command A support”; and #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT.” They discuss support, overflow, invalid states or factorization failures. An inferred connection through their linear.py traces does not establish that this fused-constructor patch addresses them. [inference; call_d1d729be463e4050b2cbaa3d9d7c5662, call_875db02889814b9789e79ce928700478, call_4b34f4ead90b4f6c9bcc512d61d67ece, call_daff1fc6e32b4c0b9615c5efb740d9a3, call_54e35762dbc047bfb1c4e32f842b7478, call_2232fc2039c24c8ea1f678281ea61801]

<a id="loading"></a>

## Restore the fused FP16 constructor contract

Linear.load first tries EXL3 storage, then load_fp16 for the primary and optional alternate keys. Inside load_fp16, a separate weight takes precedence; only its absence permits the fkey fallback. Whole-parent searches found one direct load_fp16 caller, Linear.load, and two LinearFP16 construction sites, both in load_fp16. [source; call_2efab6745cbb476ab74381678225ec8f, call_3d61ad1836454952a5efdf7adef8300a, call_910622c82424453293e25ae7a77adac7]

The fallback eagerly loads the fused weight with no_defer=True, selects the frange rows, makes that selection contiguous, applies the existing pad_out helper, and transposes it for LinearFP16. The new contiguous() operates after that transpose. LinearFP16 stores this input-by-output weight directly; forward multiplies x by it, while export transposes it back to checkpoint orientation. [source; call_910622c82424453293e25ae7a77adac7, call_2232fc2039c24c8ea1f678281ea61801, call_10c06379ad674378813d7b9cb2337d62]

The four added arguments are not new API parameters: they already exist in LinearFP16 and are supplied by the ordinary-weight branch. Outer Linear resolves omitted full dimensions to padded local dimensions and omitted offsets to zero. Its default 128 rounds feature counts upward to an alignment multiple; it is not a dispatch threshold. Forwarding these resolved values supplies the numeric precondition the constructor's comparisons require. [source; call_910622c82424453293e25ae7a77adac7, call_10c06379ad674378813d7b9cb2337d62, call_2232fc2039c24c8ea1f678281ea61801]

The two edits address different requirements: forwarding dimensions prevents the immediate comparison exception, whereas contiguous() changes storage layout without changing the logical transpose. A bounded standard-library transcription reproduced TypeError for omitted full dimensions and False for equal numeric dimensions. An illustrative 256-by-128 row-major matrix transposes to shape 128-by-256 with modeled strides (1,128), versus (256,1) after materialization. This was not a tensor-library test. [execution; call_fb50e9b1f20d460e8a5572cd4749d153]

The fused builders found in the parent are Attention's Q/K/V row ranges and GatedMLP's gate/up halves. GatedMLP explicitly rejects combining fused gate/up storage with intermediate slicing. Glm4Model supplies gate_up_proj as its fused MLP key, giving a concrete source route to the patched fallback when separate gate/up weights are absent. Thus the local fix is not GLM-only, although checkpoint-dependent reach remains conditional. [source; call_6d0b1dc382db420bab5e0045f2a42c05, call_813dd248ff17465ba62534c0972cdd3a, call_4434dcaa0eee4012b0065e14114c308e, call_7817e4eb633e41ad99c300924260dcb7, call_910622c82424453293e25ae7a77adac7]

The source mechanism matches #55's reported traceback precisely: fused construction omitted the values consumed by the failing comparison. This supports the author's reported regression diagnosis, but neither the issue report nor scalar check proves that the full conversion now completes. [inference; call_aca34a2471df4380a3d8861dfb143278, call_2232fc2039c24c8ea1f678281ea61801, call_10c06379ad674378813d7b9cb2337d62, call_fb50e9b1f20d460e8a5572cd4749d153]

## Uncertainty and limits

No repository implementation, PyTorch tensor operation, GPU kernel or complete model conversion was executed. The Python check transcribed scalar comparisons and illustrative stride arithmetic only.

Removing the constructor TypeError does not establish successful conversion for every fused checkpoint, especially shapes requiring padding, optional biases or sliced configurations.

The contiguous copy's memory cost and performance effect were not measured.
