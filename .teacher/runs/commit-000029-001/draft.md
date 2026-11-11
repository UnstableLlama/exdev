# ae9f910be23209c761505373e24b91adb6033c39


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ae9f910be23209c761505373e24b91adb6033c39) · [Evidence ledger](draft.json)

Adds a linked EXL3 conversion guide covering arguments, resume, weighted multi-GPU examples and duration estimates; shard-size instructions conflict with existing behavior.

- [Conversion usage and operational guidance](#conversion)

## Problem

Conversion guidance needed a dedicated reference beyond the README’s brief instructions. [inference; call_38f27bf7437d4e9eb8eaca7b0034c2be, call_a2c2a9c1baa2470a876923435e6aa127]

## Reasoning

The change adds doc/convert.md and links it from the README, grouping arguments into basic settings, checkpoints, performance and debugging, followed by runnable command examples and estimated durations. [source; call_38f27bf7437d4e9eb8eaca7b0034c2be, call_a2c2a9c1baa2470a876923435e6aa127]

## Impact

This is documentation-only: it exposes existing conversion controls without changing their implementation. [source; call_38f27bf7437d4e9eb8eaca7b0034c2be, call_a2c2a9c1baa2470a876923435e6aa127]

## Source Notes

The timing table presents rough v0.0.1 estimates for 1B, 8B and 70B models at 2, 4 and 8 bits per weight; these are documentation claims, not measurements reproduced here. [source; call_a2c2a9c1baa2470a876923435e6aa127]

<a id="conversion"></a>

## Conversion usage and operational guidance

The guide distinguishes source, output and working directories. The implementation stores arguments, checkpoint state and intermediate quantized tensors under the working directory, then calls compile_model after processing modules. [source; call_a2c2a9c1baa2470a876923435e6aa127, call_e6a5caa4094245b1befba3f0af5e49a9]

Explicit resume loads saved arguments and checkpoint state rather than starting a new job. The implementation allows selected overrides, while rejecting changes to saved bitrate, head bitrate and calibration dimensions. [source; call_e6a5caa4094245b1befba3f0af5e49a9]

The multi-GPU example pairs devices 2,0,1 with ratios 3,4,5. main selects the first listed device as primary, parses integer ratios, checks that their count matches the devices, and passes both lists into each linear conversion. [source; call_a2c2a9c1baa2470a876923435e6aa127, call_e6a5caa4094245b1befba3f0af5e49a9]

The example’s denominator 12 is the sum of its weights: its nominal shares are 25%, one third and approximately 41.67%. These fractions describe the requested proportions, not measured GPU utilization. [execution; call_ca4d0c6abd8349fab67fb9ebc06c9a0c]

The guide recommends adjusting ratios while monitoring utilization, offering workload weighting as an alternative to equal device participation. It frames additional GPUs as an encoding-speed option rather than a way to reduce primary-device memory requirements. [source; call_a2c2a9c1baa2470a876923435e6aa127]

## Authoring-time findings — pending review

### shard-size-documentation (suspected; defect)

The new shard-size documentation disagrees with the existing parser and allocator: it advertises floating-point values and says zero disables sharding.

Trigger: Follow the guide by passing --shard_size 1.5, or pass zero when compiling multiple modules with positive tensor sizes.

Expected: According to the guide, fractional sizes should be accepted and zero should produce an unsharded output.

Actual: The parser declares type=int, rejecting fractional text. compile_model converts zero to a zero-byte threshold without a disabling branch, so each subsequent positive-size module starts another shard. Its sole direct caller found in the parent tree is conversion main.

Locations: ae9f910be23209c761505373e24b91adb6033c39:doc/convert.md — --shard_size, 4d82aab28eb526fb387a12f1d190af6fd875b999:exllamav3/conversion/compile.py — compile_model

Source evidence: call_a2c2a9c1baa2470a876923435e6aa127, call_e6a5caa4094245b1befba3f0af5e49a9, call_9148f0c965af4c5ebf81970be67871cb, call_295c8c85d6bb44cb916a635a8761fa96, call_be12e07a64ac47efbd731301f779c50c

scalar_transcription: A standard-library reproduction rejected 1.5 with exit code 2 and allocated three separate shards for module sizes 100, 200 and 300 at a zero-byte limit. [call_ca4d0c6abd8349fab67fb9ebc06c9a0c]. Limits: This transcribes the inspected parser declaration and allocation conditions; it does not execute repository conversion or safetensors serialization.

## Uncertainty and limits

No conversion, GPU workload or filesystem-writing operation was executed. The bounded Python check models only argument parsing and shard allocation.

The guide’s performance, memory-use and hardware-tuning statements were not independently benchmarked.
