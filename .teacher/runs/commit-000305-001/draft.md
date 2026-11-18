# 2cf3e4c1e95b3d5bc858bda2ff56b38087be8305


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2cf3e4c1e95b3d5bc858bda2ff56b38087be8305) · [Evidence ledger](draft.json)

Repairs GatedMLP's FP32-input activation path by supplying a half destination and forwarding it to down projection. Explicit half execution remains in-place; default None now allocates separately. The inherited odd-element tail remains.

- [Give mixed-precision gated activations a half destination](#runtime)

## Problem

GatedMLP previously used the up-projection tensor as both activation input and output. With FP32 intermediates, that supplied an FP32 destination to silu_mul or gelu_mul, both of which require FP16 output. [source; call_4b189717fcee4c0eb1462bab4ddb905a, call_e8b3a114a9b14a5687155a7da54d3889]

## Reasoning

The change separates intermediate computation precision from activation-output storage: retain gate/up inputs, allocate a half destination when interm_dtype is not half, and feed that destination to the down projection. Changing both the activation destination and the down-projection argument is necessary. [source; call_acff99b3e9854b24994a2dd578200ab0, call_4b189717fcee4c0eb1462bab4ddb905a]

## Impact

The explicit FP32 GatedMLP path now meets the activation wrapper's output-dtype requirement. Explicit half configurations retain in-place activation. The default None configuration also allocates a separate half tensor, although the inspected FP16 and EXL3 projection backends already default their outputs to half. [source; call_acff99b3e9854b24994a2dd578200ab0, call_22f5a3f0209945a4b4e3a13a782c8e41, call_4ecc30e441ab4642874309e2f16d5424]

## Source Notes

Read the initial modules entry, the FP32 activation introduction entry, and the activation-clamping entry. They establish the original in-place design, the FP32-input/FP16-output boundary, and the previously recorded incompatible GatedMLP destination and odd-element tail. [ancestor; call_515f8dcca6044d46821fb86277cd7837, call_8c87bc50fcf54ff2ab35c6813b1ef599, call_f4d1d183821c404993fec3cab73c9ec3]

Inspection against the task diff shows that the recorded FP32 destination mismatch is removed from GatedMLP.forward. The paired activation kernels' odd-element omission is carried over unchanged. [source; call_acff99b3e9854b24994a2dd578200ab0, call_e8b3a114a9b14a5687155a7da54d3889]

The closed discussions concern different mechanisms: #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports sliced-weight padding failure; PR #20, “Reka Flash 3 vs padding,” addresses incompatible padded dimensions. Their connection to this task is inferred only from the shared MLP/projection paths, not an established mixed-precision fix. [inference; call_d7163a8b241546d79d2a6ca74d6498e0, call_3bffc9d3888449b985de694cd0ed7b10, call_acff99b3e9854b24994a2dd578200ab0]

Numerical reports provide context rather than verification: #34, “torch._C._LinAlgError on last layer of quant,” discusses activation overflow and clamping; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” reports conversion failures; #52, “Error converting moonshotai/Kimi-Dev-72B,” discusses widening MLP down outputs; #53, “Command A support,” begins as a support request and later reports conversion failures. Association with this task is inference from shared GatedMLP/Linear paths and precision themes; none establishes that this destination change fixes those reports. [inference; call_119340be4ecc4d54a18c8652ef9bb32c, call_2066717b44924ce2985573b2dc40eb22, call_7efad6137e494a099976575467fbf636, call_47497e19dc09470995e794774472e4f6, call_668a7c51faed4ce9a4ff005f9a54cbdc, call_acff99b3e9854b24994a2dd578200ab0]

#55, “Possible GLM4 32B regression,” reports a LinearFP16 loading TypeError, while #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports vocabulary-dimension mismatch. Their inferred connection is shared source paths, not the activation-output contract changed here. [inference; call_d6e3149789b240aa883f97241f96394a, call_6f0a9abbf5c44d74b74d6ba52af31581, call_acff99b3e9854b24994a2dd578200ab0]

<a id="runtime"></a>

## Give mixed-precision gated activations a half destination

GatedMLP passes interm_dtype to the gate and up Linear projections; its separate out_dtype controls down-projection output. For each selected slice, forward computes g and u, applies activation(g) × u, projects the activation down, and accumulates slice outputs. The task preserves this order and slice selection. [source; call_4b189717fcee4c0eb1462bab4ddb905a, call_acff99b3e9854b24994a2dd578200ab0]

Both native activation wrappers dispatch from the gate input dtype: float inputs require float up inputs; otherwise both must be half. Both branches require half output. The FP32 kernel computes activation and multiplication in float, narrows to half, and clamps the narrowed result. The task changes neither those calculations nor their dispatch. [source; call_e8b3a114a9b14a5687155a7da54d3889, call_acff99b3e9854b24994a2dd578200ab0]

The new a tensor preserves u's shape while explicitly requesting half storage when interm_dtype != torch.half. Otherwise a aliases u. Passing a to both activation and down projection makes the precision boundary explicit without first rounding the FP32 gate/up inputs. [source; call_acff99b3e9854b24994a2dd578200ab0, call_e8b3a114a9b14a5687155a7da54d3889]

The same destination pattern already exists in BlockSparseMLP's ordinary expert path. Its fused path similarly uses a separately allocated half interm_a for non-half intermediates. GatedMLP needs neither sparse routing nor the fused path's quantization guards because it continues to invoke individual Linear projections. [source; call_9ae8d2b1435746609a463ef36a7106cb, call_5e80939a2155495f8a7660db20ba54f5, call_1ab306b166574d44812b0509e1077cad, call_acff99b3e9854b24994a2dd578200ab0]

Constructor inspection found explicit half intermediates in SmolLM3, Qwen3, GLM4, Ernie4.5, Ernie4.5 MoE dense/shared modules, and Dots1 dense/shared modules. Cohere, Cohere2, DeciLM, Gemma2, Gemma3, Llama, Phi3 and both Mistral3 construction sites omit interm_dtype. Thus the located builders either preserve aliasing or take the new default-None allocation branch; none directly demonstrates the repaired FP32 setting. [source; call_878114a3c2594c8c940bd90ac91ff7a6, call_fa7a549bdf5c414c8ce758d7e82daecd, call_acff99b3e9854b24994a2dd578200ab0]

Located consumers remain compatible: down Linear receives a tensor with the same shape but half storage; TransformerBlock and ParallelDecoderBlock consume the resulting MLP output through immediate residual addition, and BlockSparseMLP adds shared-expert output. No public return signature changes. [source; call_22f5a3f0209945a4b4e3a13a782c8e41, call_883222fcfa8c4747a9a597bcf6682eba, call_1ab306b166574d44812b0509e1077cad, call_acff99b3e9854b24994a2dd578200ab0]

The tradeoff is extra temporary storage whenever the configured intermediate dtype is not explicitly half, including None. Compared with casting both inputs to half before activation, this design retains FP32 activation/product computation while satisfying the existing half-output interface; performance and accuracy consequences are unmeasured. [inference; call_acff99b3e9854b24994a2dd578200ab0, call_e8b3a114a9b14a5687155a7da54d3889, call_22f5a3f0209945a4b4e3a13a782c8e41]

## Authoring-time findings — pending review

### inherited-odd-activation-tail (suspected; defect)

The inherited activation kernels still leave an odd final element unwritten; the new separate destination does not repair that boundary.

Trigger: Execute GatedMLP with an otherwise valid unpadded intermediate whose total element count is odd, or directly call either activation wrapper with odd-length buffers.

Expected: Every activation destination element receives activation(g) × u.

Actual: Both kernels process only complete pairs. With separate a storage the final element is unwritten; with in-place u it retains the ungated up value. Default padding normally avoids odd widths, so this is not evidence of failure for ordinary padded models.

Locations: 2cf3e4c1e95b3d5bc858bda2ff56b38087be8305:exllamav3/modules/mlp.py — GatedMLP.forward, 823fd8db8502c9dabb0828ddb51ef519637a1689:exllamav3/exllamav3_ext/activation.cu — act_mul_kernel_h / act_mul_kernel_f

Source evidence: call_e8b3a114a9b14a5687155a7da54d3889, call_4b189717fcee4c0eb1462bab4ddb905a, call_acff99b3e9854b24994a2dd578200ab0, call_883222fcfa8c4747a9a597bcf6682eba

source_inspection: Compared the unchanged numel/2 kernel guard with GatedMLP's configurable padding and changed destination. Located decoder callers forward params directly; no new evenness check is added. [call_e8b3a114a9b14a5687155a7da54d3889, call_4b189717fcee4c0eb1462bab4ddb905a, call_22f5a3f0209945a4b4e3a13a782c8e41]. Limits: Conditional shape path; no inspected checkpoint is shown to exercise it.

scalar_transcription: Enumerated the inspected two-elements-per-thread launch arithmetic. Lengths 1, 3, 129 and 513 omit their last element; 128 and 512 are fully covered. [call_4ecc30e441ab4642874309e2f16d5424]. Limits: Standard-library integer model, not execution of the CUDA kernels.

## Uncertainty and limits

No repository model execution, CUDA kernel test, conversion, generation, accuracy evaluation or allocation benchmark was performed. The scalar check models integer coverage, not GPU execution.

Whole-tree literal searches and AST inspection cover located repository constructors and callers, not dynamic aliases or external configurations. No located shipped GatedMLP constructor explicitly selects FP32 intermediates.

Meeting the activation destination's dtype contract does not establish successful loading or execution for every backend, shape or unsupported intermediate dtype.
