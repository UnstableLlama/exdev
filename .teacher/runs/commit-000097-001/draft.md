# 2bc4822f61e3fce361ba56df0ef413c7a16061d1


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2bc4822f61e3fce361ba56df0ef413c7a16061d1) · [Evidence ledger](draft.json)

Adds optional in-place post-scaling to Linear outputs after softcapping, preserving the default path with post_scale=1.0.

- [Post-scaling linear outputs](#modules)

## Problem

Linear had optional output softcapping but no independent output multiplier. [source; call_e3bedbfffd11417194bf6d4ac68fa6ef]

## Reasoning

The change adds post_scale to the shared Linear wrapper rather than its individual backends, placing scaling after the inner forward and optional softcap. [source; call_fdb1f5c124994b4eb36b30dbba7a09dc, call_e3bedbfffd11417194bf6d4ac68fa6ef]

## Impact

The default 1.0 is the multiplicative identity and skips multiplication entirely. Nondefault values multiply the returned tensor in place; no caller is updated to enable scaling in this commit. [source; call_fdb1f5c124994b4eb36b30dbba7a09dc]

## Source Notes

The reviewed discussions report distinct problems: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns an extension import; #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” discusses quantization regularization; #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” concerns compilation failures. None explicitly identifies this output-multiplier change. [source; call_191b2982b59040318ab994d844b0be1f, call_d68e0bf8ca36422ea6416c6e2dfff09c, call_a9dc4ab57980421086737e4a6821b9b7]

<a id="modules"></a>

## Post-scaling linear outputs

Linear.__init__ appends the optional float argument post_scale=1.0 and stores it. Linear.forward still captures input statistics before invoking the backend, then softcaps if enabled, then applies post_scale. Thus the new multiplier does not directly scale the input captured by that same layer. [source; call_fdb1f5c124994b4eb36b30dbba7a09dc, call_e3bedbfffd11417194bf6d4ac68fa6ef]

For inner output z, scale s and nonzero softcap c, the mathematical operation is s·c·tanh(z/c); without softcapping it is s·z. The inspected softcap implementation supports float32 and float16, and permits in-place operation. The multiplier is a separate wrapper operation, not a change to weight storage or quantization scales. [source; call_37544410955444c4936189ec9b20bc30, call_e3bedbfffd11417194bf6d4ac68fa6ef, call_fdb1f5c124994b4eb36b30dbba7a09dc]

A scalar transcription with z=4, c=2 and s=0.5 produced 0.9640275801 for scaling after softcap versus 1.5231883119 for scaling before it. This demonstrates that moving the multiplier across softcap would change the mathematical result. [execution; call_288e836091524c73badb9faf971c875c]

Keeping the multiplier outside the backend provides one common implementation for loaded FP16 and EXL3 layers, at the cost of a separate nondefault output operation rather than backend fusion. Its runtime cost is not measured. [inference; call_e3bedbfffd11417194bf6d4ac68fa6ef, call_fdb1f5c124994b4eb36b30dbba7a09dc]

## Uncertainty and limits

No repository or GPU execution was performed. The scalar check uses Python double precision, not the CUDA softcap implementation or tensor dtype rounding.

The diff establishes the new mechanism, but not a model-specific motivation, numerical-quality benefit or measured performance cost.
