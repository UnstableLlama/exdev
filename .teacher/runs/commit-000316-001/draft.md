# 2b3d8b54af2de96d1ca956eb95f80b3f3e5b1042


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2b3d8b54af2de96d1ca956eb95f80b3f3e5b1042) · [Evidence ledger](draft.json)

Adds an import-time EXLLAMA_NO_P2P_COPY switch that stages module input transfers through CPU. The default path is unchanged; the opt-in branch also affects host-facing handoffs. Driver recovery was not verified.

- [Route module input transfers through CPU on request](#runtime)

## Problem

turboderp described the change as a driver-bug workaround for device-to-device copies. Before the change, Module.prepare_for_device requested a direct Tensor.to(self.device) whenever the incoming tensor's device differed from the module's device. The commit does not identify the affected driver, hardware, or failure symptom. [source; call_bd31130bc36e4feca6ddac79c1c2918f, call_51a1df56df1e49878d47c449d11db5ef]

## Reasoning

The module reads EXLLAMA_NO_P2P_COPY once at import and tests the saved string for truthiness. Unset or empty preserves the original path; any nonempty value, including `0` or `false`, enables host staging. On a device mismatch the enabled branch prints a dot and then calls x.cpu().to(self.device). A same-device input is still returned unchanged, and params is still unused. [source; call_4c46e229470f4fa7a428d2fab4d4c7c5, call_51a1df56df1e49878d47c449d11db5ef]

For an inter-GPU handoff, explicitly routing through CPU lets the caller avoid requesting a direct GPU-to-GPU move at this boundary without changing layer placement. The tradeoff is an extra host transfer leg and temporary host storage. This is an opt-in path, not a retry after a failed copy, a peer-capability check, or a process-wide CUDA setting. [inference; call_4c46e229470f4fa7a428d2fab4d4c7c5, call_8d00843b4719415d84d282f007f3648a]

## Impact

Model.forward and Model.prefill pass each top-level module's output to the next module through this helper. Model._load_autosplit also uses it for the dummy forward pass after loading a module, so the override can affect both split probing and later inference. Generation reaches it indirectly through the generator's logit forward pass and the job's prompt prefill. [source; call_8d00843b4719415d84d282f007f3648a, call_c6b541705204447fa5b06101d447fc15, call_3ebc23bc559841508621eaf6d50f3dd8, call_240a425d3b5246009c1c0bd4660a6bc9]

Other direct callers found in the parent tree are conversion's calibration capture, optional selected-expert reference pass, and post-quantization state advance; eval/compare_q_logits.py, both sides of eval/model_diff.py, and eval/prequant_test.py before their layer forwards; and science/kv_quant_exp.py during its layer walk. The call in tests/test_quant_fn.py creates the input on the same device passed to linear.load, so it is not coverage of the intended inter-GPU route. The patch does not change standalone transfers such as conversion's reference-state .to(...) or get_for_device's metadata copies. [source; call_b5bb014997c4490fa479334ba1e0afda, call_f7f8f3bd46b04b1ba38130c6c601f2b3, call_240a425d3b5246009c1c0bd4660a6bc9, call_2a69fb4849ac4136a5c2cab255f9bbd2, call_4c46e229470f4fa7a428d2fab4d4c7c5]

## Source Notes

The initial implementation's modules chapter describes prepare_for_device as the activation handoff between top-level modules. The FP16 feature-slicing entry separately describes host staging for weights and Module.load forwarding keywords to its children; that is a different operation from the activation move changed here. [ancestor; call_4b49ded041b142f5b7eefd6a05b74743, call_2d6f4cddde5c420690b1e73e1dd93580]

No literal parent-tree match was found for EXLLAMA_NO_P2P_COPY, no_p2p_copy, P2P, or `driver bug`. The broader `driver` search did find a build-workflow comment about an NVIDIA driver dependency breaking a CUDA installation method, not an activation-copy report. [source; call_8ec1c82424ca4bcabf076b6f60f36e36, call_15d53fed880643f08794be0aa3b91501, call_5fcdfdfd07324edca1653dba9be3c240, call_06271dab234a4b2e9af42e9a80eba1ee, call_4f9bb436128f4173a3af1a21bb85697d, call_f7f8f3bd46b04b1ba38130c6c601f2b3]

Issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” and #55, “Possible GLM4 32B regression,” both show the unchanged recursive Module.load call, not prepare_for_device. The former reports a tensor-size mismatch in safetensors padding; the latter reports an int-versus-None comparison in LinearFP16 construction. The shared module path is not evidence that either was the driver bug. Issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” discusses a quantization-regularization workaround, not host-staged transfers. [inference; call_387d8e68ea0d4fa583c1553e17daf4e4, call_efd623da7ac449bd8ab2d4fcc1d69563, call_47955a6cd5eb4c11a2491cc449bac353, call_51a1df56df1e49878d47c449d11db5ef, call_4c46e229470f4fa7a428d2fab4d4c7c5]

Issue #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” quotes the autosplit error in Model._load_autosplit. Issue #54, “GPU split isn't followed here?”, discusses the same dummy-forward placement mechanism, but reports allocator and VRAM utilization problems and a different environment workaround. These are useful context for the caller, not evidence that this override fixes placement or memory allocation. [inference; call_4e71a097345f4512a844ec39ee8f0436, call_411e29aeb12e4a0dbae4d9a5e9e18b9c, call_8d00843b4719415d84d282f007f3648a, call_4c46e229470f4fa7a428d2fab4d4c7c5]

Other overlaps are with callers or utility files, not with the changed transfer statement. PR #26, “Superior 3INST parameters,” mentions eval/model_diff.py as a possible evaluation starting point for its codebook proposal. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” passes through models/model.py during import but fails loading the extension. Issue #33, “Error converting model,” reports a file-open error while compiling output; #34, “torch._C._LinAlgError on last layer of quant,” #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” show Cholesky failures reached from the conversion driver. Issue #53, “Command A support,” starts as a support request and later shows a similar conversion traceback. Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” points to SeqTensor.append in the same utility file as get_for_device, but reports a logits width mismatch, not a device handoff failure. [inference; call_4d678faf7ca14e37ad2ff35412948d57, call_a61240f8445f469b8a4cf0b20ca79b4a, call_4cbf5e91b9f54593bb2e2f8f3beac91f, call_7197741eb5904258b9d69b914ba3a70b, call_38a8feba65b2403a8e523ae593c770ca, call_248c50f9deae4d6fadc309fd6af65a7a, call_2132a03a1b614849a969809fd1e50816, call_bdd60ed985704965ae70989eae3c5dfa, call_90504a9ba02c48519c13f06562124593, call_4c46e229470f4fa7a428d2fab4d4c7c5]

<a id="runtime"></a>

## Route module input transfers through CPU on request

Set EXLLAMA_NO_P2P_COPY=1 before importing the module to request CPU staging. Leaving it unset or empty keeps the existing path. There is no GPU-pair check: the condition is device inequality, so host-to-device and device-to-host handoffs also enter the enabled branch and print a newline-terminated dot before attempting the transfer. [source; call_4c46e229470f4fa7a428d2fab4d4c7c5]

A standard-library branch check modeled four device pairs and five initial environment values. Changing the environment after initialization did not change the selected path. Equal devices returned the original object without output; a mismatch with an unset or empty value called only to(...); with `0`, `false`, or `1` it recorded cpu() followed by to(...) and captured one dot line. [execution; call_4c46e229470f4fa7a428d2fab4d4c7c5, call_71f0edb5fba2476684ac8646d21b9d11]

## Authoring-time findings — pending review

### cpu-endpoints-enter-p2p-workaround (suspected; behavior_change)

The P2P override covers host-facing transfers as well as inter-GPU copies, so it can add output even in a single-GPU configuration.

Trigger: Import with a nonempty EXLLAMA_NO_P2P_COPY and pass a CPU tensor to a module on a GPU, or a GPU tensor to a module on CPU. For example, Model._load_single honors the embedding's prefer_cpu capability while placing ordinary modules on the selected GPU; Model.forward passes state across that boundary.

Expected: If the option only bypassed peer-to-peer GPU copies, a transfer with a CPU endpoint would retain the original quiet to(self.device) path.

Actual: Any device mismatch takes the enabled branch. It prints a dot before calling cpu().to(self.device), even if the source or destination is already CPU.

Locations: 2b3d8b54af2de96d1ca956eb95f80b3f3e5b1042:exllamav3/modules/module.py — Module.prepare_for_device

Source evidence: call_4c46e229470f4fa7a428d2fab4d4c7c5, call_b5bb014997c4490fa479334ba1e0afda, call_8d00843b4719415d84d282f007f3648a, call_240a425d3b5246009c1c0bd4660a6bc9

source_inspection: Compared the new predicate with the parent helper and inspected model placement and the parent call sites. The difference applies only when an inspected caller supplies a mismatched device while the override is enabled. [call_51a1df56df1e49878d47c449d11db5ef, call_4c46e229470f4fa7a428d2fab4d4c7c5, call_8d00843b4719415d84d282f007f3648a, call_f7f8f3bd46b04b1ba38130c6c601f2b3]. Limits: This establishes branch scope, not that PyTorch makes an extra physical copy when an endpoint is already on CPU.

scalar_transcription: Fake CPU-to-GPU and GPU-to-CPU cases both recorded cpu(), to(...), and one dot line with the override enabled. [call_71f0edb5fba2476684ac8646d21b9d11]. Limits: No real tensors, model execution, or GPU transfers.

## Uncertainty and limits

The Python check transcribed the branch with fake tensor methods. It did not import the changed repository module or execute PyTorch or CUDA copies. The actual transport selected by the original Tensor.to call, driver recovery, copy latency, synchronization, and peak host memory were not measured.

The caller inventory is from a literal search of the parent tree and does not establish coverage for dynamic or external callers.
