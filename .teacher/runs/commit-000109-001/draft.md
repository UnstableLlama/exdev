# f97c5ce619feb3aa9f4ceb568c9e350d166df866


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f97c5ce619feb3aa9f4ceb568c9e350d166df866) · [Evidence ledger](draft.json)

Propagates Attention's configured output dtype into its output projection, instead of applying it only after projection.

- [Apply the configured dtype inside the attention output projection](#modules)

## Problem

Attention stored its constructor out_dtype but did not pass it to the output projection. The requested dtype was applied only after decoding, rather than when allocating the projection result. [source; call_5c8822c954ca4231a9c1d5b505293a59, call_71702caba2bb41a3a918c2c3e6dd2ad6]

## Reasoning

Passing out_dtype into o_proj lets Linear propagate it to both FP16 and EXL3 implementations, whose forward methods use the configured dtype when allocating their output buffers. [source; call_c679d21ed8ce483a9ce928c486c3d647, call_0864d627f3764d99897a444d98f4ff39, call_69b03915055f49598dde4ecb546422b3, call_89f93d59fa12456f8a436f102f370170]

## Impact

The change covers all three attention backends because each calls project_o. With the constructor default of None, projection allocation still defaults to torch.half; Q/K/V projections are unchanged. [source; call_c679d21ed8ce483a9ce928c486c3d647, call_5c8822c954ca4231a9c1d5b505293a59, call_69b03915055f49598dde4ecb546422b3, call_89f93d59fa12456f8a436f102f370170]

## Source Notes

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” reports a conversion failure during Hessian capture; its discussion attributes that failure to tokenizer truncation. Its overlapping attention/linear traceback is not evidence that this dtype change fixes that report. [source; call_dee0ea3af2a2419fbef7338dc007cd35]

<a id="modules"></a>

## Apply the configured dtype inside the attention output projection

project_o flattens the attention heads to num_q_heads × head_dim and projects that dimension back to hidden_size. The patch changes only the projection's configured output dtype, not its dimensions, weight key or calibration qmap. [source; call_5c8822c954ca4231a9c1d5b505293a59, call_c679d21ed8ce483a9ce928c486c3d647]

Previously a float output request could widen an already half-precision projection result. Moving the configured dtype into the projection allows a wider destination before the final attention-level conversion, rather than relying on a cast to recover information already lost. [inference; call_69b03915055f49598dde4ecb546422b3, call_89f93d59fa12456f8a436f102f370170, call_71702caba2bb41a3a918c2c3e6dd2ad6, call_c679d21ed8ce483a9ce928c486c3d647]

Attention.forward's per-call out_dtype remains a final conversion override: it is not forwarded through project_o. The new internal allocation policy follows the constructor argument, while the final returned dtype can still be overridden per call. [source; call_5c8822c954ca4231a9c1d5b505293a59, call_c679d21ed8ce483a9ce928c486c3d647, call_71702caba2bb41a3a918c2c3e6dd2ad6]

## Uncertainty and limits

No repository or GPU execution was performed; native dtype support, numerical improvements and performance effects were not verified.

No useful scalar computation establishes this constructor-wiring change's GPU behavior.
