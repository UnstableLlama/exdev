# 6f9928b3acee3b52f5064a1ce8ef436b2442ea52


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6f9928b3acee3b52f5064a1ce8ef436b2442ea52) · [Evidence ledger](draft.json)

Widens Ernie 4.5 routed-expert gate/up intermediates to FP32 while preserving half activation outputs and FP32 down outputs. Existing kernels support the precision boundary, at additional workspace cost; numerical benefit remains unmeasured.

- [Widen routed-expert gate/up intermediates](#models)

## Problem

Ernie 4.5 routed experts previously requested FP16 gate/up outputs. The change widens these intermediates to FP32, without widening the activation output supplied to the down projection. [source; call_26c9e703f630491183d18710c92d0226, call_9bb5901c23cf4d2cbcf2fa17cd590959]

## Reasoning

The likely numerical purpose is to avoid premature overflow or precision loss before SiLU multiplication. This is an interpretation of the dtype change and existing kernels, not a demonstrated Ernie failure or measured accuracy improvement. [inference; call_26c9e703f630491183d18710c92d0226, call_cb38fd2160a1487abdcebcebd57246f1, call_2c2fe27dfc0141e58ae6e1fd1eb8346c]

## Impact

Only routed-expert intermediates change. Dense-prefix and shared-expert GatedMLPs retain FP16 intermediates; routed down-projection outputs remain FP32. Routing and ordinary-versus-fused expert selection are unchanged. [source; call_26c9e703f630491183d18710c92d0226, call_e30418cfab4a4e4eb44dc412f544c414, call_9bb5901c23cf4d2cbcf2fa17cd590959]

## Source Notes

Read the Ernie introduction entry. It establishes the reused dense-prefix/routed/shared assembly and records conditional fused-path limitations; the current source and one-line diff retain those forward-path limitations. [ancestor; call_aba8f749bdc248e0a26735f6fcf0bb97, call_f8644eef60684af2adb507cb3debf820]

The inspected discussions are background, not established motivation. #34, “torch._C._LinAlgError on last layer of quant,” concerns Command-A conversion; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concerns Midnight-Miqu and Command-R+; #52, “Error converting moonshotai/Kimi-Dev-72B,” discusses widening down outputs; #53, “Command A support,” begins as a support request and later reports conversion failures; #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT,” reports another model's NaNs. Their inferred connection is the shared Linear conversion traceback and numerical-overflow theme, not evidence that this Ernie intermediate change fixes them. [inference; call_5f4381eb1f8b4b4da300b59d742eb6b1, call_534b040efc4942d29bfec70bfb1873bc, call_1a4cfb12869647b6bf9ae74660a9aa3c, call_1dbb82cd7dea4a7e9956d54452f8213b, call_d2c522edab494833a719821032befa1f, call_cb38b10d7b4b4b93a0785e3eb6dfb060, call_ee238510cafb4ee0940f4e751840a1c7]

#55, “Possible GLM4 32B regression,” reports a loading TypeError rather than numerical overflow. Its inferred association is the matching LinearFP16 constructor and Linear.load_fp16 source, not an Ernie-specific relationship. [inference; call_f97baf59d6ab489594b0238bf2f5bed6, call_de2c0a906467402b970f52be4f073eba, call_ee238510cafb4ee0940f4e751840a1c7]

<a id="models"></a>

## Widen routed-expert gate/up intermediates

Ernie4_5MoEModel.__init__ changes the BlockSparseMLP interm_dtype argument from torch.half to torch.float. The dense-prefix boundary remains idx < first_k_dense_replace; optional shared experts are separately constructed GatedMLPs and are not widened. [source; call_26c9e703f630491183d18710c92d0226, call_e30418cfab4a4e4eb44dc412f544c414]

BlockSparseMLP passes interm_dtype to every routed gate/up Linear as out_dtype. Linear forwards that setting into its loaded backend. For ordinary FP16 weights, LinearFP16 allocates the requested output dtype; half input with float output selects ext.hgemm, whose float-output branch uses half operands, FP32 output and CUBLAS_COMPUTE_32F. This changes intermediate/output arithmetic, not checkpoint weight storage. [source; call_9bb5901c23cf4d2cbcf2fa17cd590959, call_ee238510cafb4ee0940f4e751840a1c7, call_de2c0a906467402b970f52be4f073eba, call_2c2fe27dfc0141e58ae6e1fd1eb8346c]

The existing non-half path supplies the necessary activation destination: ordinary expert evaluation allocates a separate half tensor, and load allocates half interm_a separately from float interm_g/interm_u. silu_mul requires float gate/up inputs together and always requires a half destination. Its float kernel computes SiLU and multiplication in float, then converts the product to half. Thus 'FP32 intermediate' does not mean the entire expert MLP becomes FP32. [source; call_9bb5901c23cf4d2cbcf2fa17cd590959, call_cb38fd2160a1487abdcebcebd57246f1]

For one flattened token with fully EXL3 experts, the fused calls write gate/up results into the widened workspaces. exl3_mgemm accepts half input with either half or float output and selects its FP32-output kernel table when C is float. Kernel availability remains shape-dependent, and the selector rejects unsupported shapes; this edit does not relax those preconditions. [source; call_9bb5901c23cf4d2cbcf2fa17cd590959, call_c6b09d65d1e342159ef136fe6984fcac, call_b142536e9118465f9666c85c00bc348b, call_5cb6f41c842d4a63b98670a75c2f254c, call_8fa4962e69cf488ebc4cf6527ad8043b]

All four baidu/ERNIE-4.5-21B-A3B configurations were read individually: Base-PT, Base-Paddle, PT and Paddle. Each names the changed architecture and specifies 28 layers, one dense-prefix layer, expert width 1536, 64 experts, six selected experts and two shared experts. Each therefore maps to 27 widened routed blocks while retaining half shared intermediates. None of these configurations supplies the new runtime intermediate dtype; the builder chooses it. [source; call_96b2d50f7bd440be9df573238fc8d83c, call_78109e98fdb74bdf9eceb1be6e8a849f, call_b8aae398b1414b199260141ab5c3b84e, call_9c8bb3ccd33140cf971a2f22a8be1f46, call_e30418cfab4a4e4eb44dc412f544c414, call_26c9e703f630491183d18710c92d0226]

All seven baidu/ERNIE-4.5-300B-A47B configurations were read individually: Base-PT, Base-Paddle, PT, Paddle, 2Bits-Paddle, FP8-Paddle and W4A8C8-TP4-Paddle. Each names the changed architecture and specifies 54 layers, a three-layer dense prefix, expert width 3584, 64 experts and eight selected experts. Each omits shared-expert count, selecting the builder's zero default, and maps structurally to 51 widened routed blocks. The three quantized Paddle configurations additionally declare distinct quantization schemes; the dtype edit does not implement those formats. [source; call_cb18de47b20e4745b80d5436ec9234a1, call_61ae3ba7c1d64afba890e44c9767621a, call_3f76f98954634b4fa5e512ea90d8cf33, call_795792562e844bd3a69ba8e24eca4bd5, call_04d9c505d9ed48c48c46fd1d25f08761, call_0dc04bc5bd834b90972344c4a666cd40, call_ae95f05320d0430d87b710f3d7ec374d, call_e30418cfab4a4e4eb44dc412f544c414, call_26c9e703f630491183d18710c92d0226]

A bounded scalar illustration used gate=70000 and a half-rounded up value near 0.001. Rounding the gate to half first overflowed; retaining it through float SiLU multiplication produced a half output of 70.0. Workspace arithmetic also gave gate/up/activation storage of 36,864 → 92,160 bytes for six experts of width 1536, and 114,688 → 286,720 bytes for eight experts of width 3584. These count only those three buffers: the old activation aliases up, whereas the new activation is separate. [execution; call_6ad39a974bdc4fdbbc9d4110788d919e]

Wider intermediates trade extra workspace and float computation for avoiding premature half rounding. The final activation still narrows to half, so the change cannot guarantee finite results when the actual SiLU product exceeds half range. The inspected TransformerBlock immediately adds the sparse result to its residual and supplies no per-call dtype override. [inference; call_cb38fd2160a1487abdcebcebd57246f1, call_9bb5901c23cf4d2cbcf2fa17cd590959, call_525b13d730af439e9477d68a158cef78]

## Authoring-time findings — pending review

### inherited-all-expert-fused-capacity (suspected; defect)

The inherited all-expert/fused-buffer mismatch persists; widening the buffers does not increase their expert-plane count.

Trigger: Run one flattened token through fully EXL3 routed experts with activate_all_experts=True and num_experts greater than num_experts_per_tok.

Expected: Evaluate all requested experts using compatible buffers or choose the ordinary path.

Actual: routing_std returns num_experts indices, but load allocates num_experts_per_tok output planes. Dispatch still selects fusion, and exl3_mgemm checks index count against output planes. TransformerBlock forwards params directly. This establishes a conditional module-level path, not failure of every conversion or generation workflow.

Locations: 6f9928b3acee3b52f5064a1ce8ef436b2442ea52:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_9bb5901c23cf4d2cbcf2fa17cd590959, call_b142536e9118465f9666c85c00bc348b, call_aeabbd1ff9a14290a843e748aaba1c4b, call_525b13d730af439e9477d68a158cef78, call_26c9e703f630491183d18710c92d0226

source_inspection: Compared routing index counts, workspace allocation, dispatch and the native shape check; inspected the located decoder callers. [call_9bb5901c23cf4d2cbcf2fa17cd590959, call_b142536e9118465f9666c85c00bc348b, call_525b13d730af439e9477d68a158cef78]. Limits: No extension or GPU execution; external caller reach is unknown.

### inherited-fused-return-contract (suspected; behavior_change)

The fused return remains workspace-backed and does not honor the ordinary path's per-call dtype conversion.

Trigger: Retain a fused result across another fused call, or request an out_dtype different from the allocated output dtype.

Expected: An independent result honoring the override, consistent with the ordinary path.

Actual: The fused branch returns a view of cfg.out_d without to2 conversion, and later calls reuse that workspace. The inspected TransformerBlock immediately adds the result and supplies no override, so it does not demonstrate either incompatibility. The task's intermediate dtype edit leaves this inherited contract unchanged.

Locations: 6f9928b3acee3b52f5064a1ce8ef436b2442ea52:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_9bb5901c23cf4d2cbcf2fa17cd590959, call_aeabbd1ff9a14290a843e748aaba1c4b, call_525b13d730af439e9477d68a158cef78, call_26c9e703f630491183d18710c92d0226

source_inspection: Compared both return paths and inspected the located decoder consumers. [call_9bb5901c23cf4d2cbcf2fa17cd590959, call_525b13d730af439e9477d68a158cef78]. Limits: No tensor-lifetime or dtype execution test; no inspected decoder caller exercises the problematic usage.

## Uncertainty and limits

No repository implementation, checkpoint load, conversion, generation or CUDA kernel was executed. Numerical benefit, latency and actual peak-memory changes remain unmeasured.

The scalar illustration uses Python math and explicit storage rounding, not CUDA's approximate exponential or cuBLAS accumulation. It demonstrates a possible precision mechanism, not observed checkpoint activations.

Matching reference configuration dimensions does not establish direct compatibility with Paddle checkpoint formats or their declared quantization schemes.

Caller searches establish the inspected decoder call sites, not every possible external use of BlockSparseMLP.
