# ddf260767d5e31b04d1e0cd660ef4188071d809a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ddf260767d5e31b04d1e0cd660ef4188071d809a) · [Evidence ledger](draft.json)

Makes conversion's missing-strategy assertion name the first affected linear module without changing its acceptance condition or repairing allocation.

- [Identify the linear missing a quantization strategy](#conversion)

## Problem

The conversion strategy assertion reported a missing allocation without identifying the affected linear module. [source; call_7adb223c506d43948e11a430441e459a]

## Reasoning

Replacing all(...) with individual assertions makes the first failing linear available to the error message while retaining the membership requirement. [source; call_7adb223c506d43948e11a430441e459a]

## Impact

This improves diagnostics rather than repairing missing strategy entries: conversion still stops, now naming linear.key. [source; call_7adb223c506d43948e11a430441e459a]

## Source Notes

The root conversion ancestor entry was read for the workflow this assertion belongs to. It describes allocation followed by per-linear conversion and records an earlier double-work-directory save-path hazard. [ancestor; call_aa370b823b014294a69bc5f7d2c4c200]

That recorded save-path hazard is already removed in the inspected parent: main passes qtensors/<module-key>.safetensors and save_tensor adds work_dir once. The task leaves this code unchanged. [source; call_e01b669082f04dbb8867ab72261c84c2, call_7adb223c506d43948e11a430441e459a]

Read discussions include #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800”; #11, “AssertionError: bias is wrong datatype”; #16, “RuntimeError: CUDA error: invalid configuration argument”; #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1”; and #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated.” Their reports concern padding, bias dtype, calibration/tokenization, sliced loading, and invalid calibration states respectively—not the missing-strategy diagnostic. [source; call_b7a291323f8a4bb79125f5a7b5ac5205, call_39aa7651e0364dcfb9d0630020531e44, call_db2469c719af4803bde73b7e49f859cc, call_173f2c51a8684c7087896726d7186449, call_edbf4c92d059483d8c8bd7ba5818cec5]

Also read PR #13, “Fix a tokenizer issue while converting models without a bos_token_id defined”; PR #26, “Superior 3INST parameters”; #33, “Error converting model”; #34, “torch._C._LinAlgError on last layer of quant”; and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values.” They discuss tokenizer handling, decoder experiments, file-opening/inference failures, and factorization failures. [source; call_83423ef4de764f8a8ddc3a916fc7da72, call_a6735d2f5d4f4f349b600c2db1c02e0f, call_d138de1b9e7a4c4fa1ff06dad3219f4c, call_a9d01aae02b844cba5b649cc83ebc1bd, call_29fc98dff6664e8c99635b2ee72ff5f1, call_d5ca0ec1e45b4764a457a9065113effd, call_491c4d5cc5d646e78b0c30cc5aa05ef4]

These discussions are contextual matches by convert_model.py paths and conversion call sites; associating them with this task is inference, not an established upstream linkage. None establishes the particular missing strategy that motivated this edit. [inference; call_7adb223c506d43948e11a430441e459a, call_39aa7651e0364dcfb9d0630020531e44, call_d138de1b9e7a4c4fa1ff06dad3219f4c, call_491c4d5cc5d646e78b0c30cc5aa05ef4]

<a id="conversion"></a>

## Identify the linear missing a quantization strategy

main obtains a strategy from module.allocate_q, applies mod_strategy, then processes each module slice. Its target list includes only Linear instances with a truthy qmap and a non-None device; the diagnostic therefore concerns loaded quantization targets, not every model submodule. [source; call_e01b669082f04dbb8867ab72261c84c2]

The new loop checks each target's key against strategy and includes that key in the AssertionError. It preserves the subsequent LinearFP16 assertion and runs before image dumping, CPU weight staging, and construction of quant_args, where strategy[linear.key] supplies K. [source; call_7adb223c506d43948e11a430441e459a, call_e01b669082f04dbb8867ab72261c84c2]

Both forms accept an empty target list and stop on the first missing key. A standard-library transcription checked 968 combinations of target sequences and strategy key sets: pass/fail outcomes matched throughout, and the new message identified the first absent key. [execution; call_1509726074be495fbca51cf8965188a2]

The inspected CLI entry point imports this main and calls it after successful prepare. A whole-parent search for conversion.convert_model found this import in convert.py; this establishes the direct CLI route, not exhaustive coverage of external callers. [source; call_620988e6e91c4d839b41169c9c01d75c, call_105e99e225ea4e6ca721081d01ce7adb]

The practical tradeoff is a more actionable first-failure message rather than an aggregate list of all missing allocations. Neither strategy contents nor quantization settings change. [inference; call_7adb223c506d43948e11a430441e459a]

## Uncertainty and limits

No repository conversion or GPU execution was performed. The bounded Python check transcribes only assertion control flow.

The evidence does not identify a concrete model or allocation failure motivating the diagnostic change.
