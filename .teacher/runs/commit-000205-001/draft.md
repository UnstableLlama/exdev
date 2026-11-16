# 34d2f1f5fa069b842b8791de8c8db499b3884579


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/34d2f1f5fa069b842b8791de8c8db499b3884579) · [Evidence ledger](draft.json)

Adds streaming weight/state diagnostics and perplexity evaluation, supported by optional Hessian-free regularization and skipped global-scale search. Inspection identifies a verbose-mode unbound local and a conditional histogram stride mismatch.

- [Streaming prequantization diagnostics](#prequant-test)

## Problem

Adds a diagnostic forward pass for inspecting weights and hidden states before quantization, without loading all model modules simultaneously. [source; call_045b77a492f242d58957471b366b89ce]

## Reasoning

The two edits are coupled: the script calls regularize without a Hessian diagonal or target bitrate, so regularize gains a no-diagonal policy and an option to bypass bitrate-dependent global-scale search. [source; call_045b77a492f242d58957471b366b89ce, call_b963f5ef85b3473d99c54ed8134af354, call_b6f3e6c839164549b0c5fc1aa34d05ac]

## Impact

The existing quantize_exl3 caller still supplies H_diag and a progress bar and retains scale search through the new argument's False default. The diagnostic caller instead uses output scaling, random sign vectors and g_scale=1, so its regularized distribution is not a simulation of every calibrated quantization decision. [source; call_ce063d50accc4fd98a02973630f3d2d8, call_8642a86933a14d06a0ab91789470ada0, call_b963f5ef85b3473d99c54ed8134af354, call_045b77a492f242d58957471b366b89ce]

## Source Notes

Read ancestor 322815f71eaf582e36fd81bc6fdf5148b27fb97a, which introduced regularize and explained calibration-guided output scaling. It also recorded a missing test policy key and premature scale-search progress. [ancestor; call_36c2101d95e744edabbcbbbb8313446e]

The missing test-policy incompatibility is already removed in the inspected parent: test_quant_dequant supplies apply_out_scales and devices. The premature progress expression remains in g_scale_gss, untouched by this change; the diagnostic path bypasses that search. [source; call_6b81ee00d30448ae95699772159d7a2a, call_b6f3e6c839164549b0c5fc1aa34d05ac, call_b963f5ef85b3473d99c54ed8134af354]

Issue #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” reports Cholesky failure and invalid states. There turboderp describes writing a prequantization debugging tool that avoids loading the whole model. Its relationship to this commit is inferred from that concrete description matching the new streaming diagnostic, not an explicit commit link. [inference; call_7b2eca1fe95b4c3ca4bec8997c130714, call_045b77a492f242d58957471b366b89ce]

Related reports are #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800”; #34, “torch._C._LinAlgError on last layer of quant”; and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values.” Their inferred connection is the quantizer traceback and, for #34/#42, invalid-state diagnostics. They do not establish that this diagnostic script fixes those failures. [inference; call_183260cb5bd34435824199714bf1c02b, call_c4885f3be5bd44af9bbce6804ea3fc8d, call_5c24114c1ac344c3bea6fe4559614e75, call_045b77a492f242d58957471b366b89ce]

PR #26, “Superior 3INST parameters,” discusses regularize, outlier channels and global-scale search. Its connection here is inferred from those shared mechanisms; its proposed decoder changes and reported benchmark gains are not changes made by this commit. [inference; call_82f29ca25a864f2d97f89dc655115dbf, call_4241f1571e5a401cb6e82dd1677c66b4, call_310c12d10e36434ca9d20b8a851771bc, call_b963f5ef85b3473d99c54ed8134af354]

<a id="prequant-test"></a>

## Streaming prequantization diagnostics

The script tokenizes the Wikitext-2 test split into 2048-token windows with stride 512, optionally prepending BOS. Defaults are ten rows, device index zero, 160 histogram bins and no skipped tokens. Each module is loaded with deferred tensor loading, inspected, forwarded, then unloaded; CPU-preferred modules retain CPU loading. [source; call_045b77a492f242d58957471b366b89ce]

Weight diagnostics enumerate Linear descendants, report extrema, population standard deviation, nonfinite counts and absolute six-sigma exceedance. They compare original and regularized distributions and count regularized absolute magnitudes greater than 4 and 8. Six-sigma testing is relative to zero, not distance from the tensor mean. [source; call_045b77a492f242d58957471b366b89ce]

Regularization retains output-channel RMS scaling, right Hadamard mixing, input-channel RMS scaling and left Hadamard mixing. The blockwise helpers require float32 and dimensions divisible by 128. With no H_diag, automatic output scaling becomes True; with a diagonal, the existing rule compares the largest floor(k/50) channel RMS sum against 15% of the total. [source; call_8642a86933a14d06a0ab91789470ada0, call_7961f3561d32459ebf73bb5c6217b1a0, call_b963f5ef85b3473d99c54ed8134af354]

skip_g_scale avoids trial quantization of wrapped-diagonal tiles and uses the identity scale 1.0. This saves the diagnostic from requiring K or executing the existing golden-section search over [0.1, 1.9] with interval tolerance 0.01. It does not bypass the Hadamard or channel-normalization preconditions. [source; call_b6f3e6c839164549b0c5fc1aa34d05ac, call_b963f5ef85b3473d99c54ed8134af354, call_7961f3561d32459ebf73bb5c6217b1a0]

Hidden-state histograms allocate half the bins to ±3 standard deviations and a quarter to each tail. The native exclusive mode includes both endpoints; nonexclusive weight histograms clamp out-of-range values into edge bins. Each chart independently scales its bars to its own maximum count. [source; call_045b77a492f242d58957471b366b89ce, call_e63b6ef1e803448da5b9f96b896b345e]

skip_tokens affects hidden-state inspection only, not forwarding or perplexity. Perplexity gathers next-token log probabilities from final logits, truncates logits to actual vocabulary size and exponentiates the negative mean. Overlapping windows are scored independently, without a warm-context-only mask. [source; call_045b77a492f242d58957471b366b89ce]

A standard-library arithmetic check gives 1,536 tokens of adjacent-window overlap, 20,470 scored predictions when all ten default rows exist, and histogram widths of 40/80/40. These are arithmetic checks, not measured model results. [execution; call_bd7175d165234a5e9148422282b9142b]

## Authoring-time findings — pending review

### verbose-skipped-scale (suspected; defect)

The new skipped-search mode leaves verbose reporting without mse_scale.

Trigger: Call regularize with skip_g_scale=True and verbose=True, after successful preprocessing.

Expected: Return regularized weights and either omit sample MSE or report it unavailable.

Actual: The unchanged verbose block calls mse_scale.item(), but the new skip branch defines only g_scale, causing an unbound local access.

Locations: 34d2f1f5fa069b842b8791de8c8db499b3884579:exllamav3/modules/quant/exl3_lib/quantize.py — regularize

Source evidence: call_b963f5ef85b3473d99c54ed8134af354, call_8642a86933a14d06a0ab91789470ada0, call_ce063d50accc4fd98a02973630f3d2d8, call_045b77a492f242d58957471b366b89ce

source_inspection: Compared assignment branches with the verbose reader and all located direct callers. The new script supplies verbose=False; quantize_exl3 keeps skip_g_scale=False. [call_b963f5ef85b3473d99c54ed8134af354, call_8642a86933a14d06a0ab91789470ada0, call_ce063d50accc4fd98a02973630f3d2d8, call_045b77a492f242d58957471b366b89ce]. Limits: No located repository caller selects the failing combination; this concerns the newly exposed argument combination.

### skipped-state-strides (suspected; defect)

Token-skipping can pass a noncontiguous state view to a stride-unaware histogram kernel.

Trigger: Multiple state rows, positive skip_tokens smaller than the context length, and state already on the selected device so no copying materializes the slice.

Expected: Histogram every element of the selected token suffixes.

Actual: inspect_state does not make the slice contiguous. The native kernel traverses input_ptr[0:numel], ignoring row gaps, so it can include skipped tokens from later rows and omit selected trailing tokens.

Locations: 34d2f1f5fa069b842b8791de8c8db499b3884579:eval/prequant_test.py — inspect_state

Source evidence: call_045b77a492f242d58957471b366b89ce, call_e63b6ef1e803448da5b9f96b896b345e, call_9eddef54a568407d859d648f4cd846fe

source_inspection: The parent has no inspect_state caller; the new main calls it after each module forward. Traced its slice through histogram to raw-pointer CUDA indexing. [call_9eddef54a568407d859d648f4cd846fe, call_045b77a492f242d58957471b366b89ce, call_e63b6ef1e803448da5b9f96b896b345e]. Limits: Conditional on the view retaining row strides; device-copy behavior was not executed.

scalar_transcription: Modeled a contiguous [2,3,2] tensor with one skipped token per row: selected values sum to 52, whereas contiguous pointer traversal from the slice offset sums to 44. [call_bd7175d165234a5e9148422282b9142b]. Limits: Python indexing model, not Torch or CUDA execution.

## Uncertainty and limits

No model, Torch operation, CUDA kernel or terminal rendering was executed. Scalar checks model indexing and arithmetic only.

The diagnostic uses unseeded random signs and omits calibration-dependent scale selection; its outlier counts do not establish quantized-model accuracy.

The inspected source does not derive the retained codebook_scale=1.24371088 or establish an empirical justification for the diagnostic thresholds 4 and 8.

Whole-tree literal searches establish located repository callers, not dynamic or external callers.
