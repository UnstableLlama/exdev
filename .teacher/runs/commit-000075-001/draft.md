# be19eb55f2f6d13f04ff6003a60dee430f8d2735


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/be19eb55f2f6d13f04ff6003a60dee430f8d2735) · [Evidence ledger](draft.json)

Fixes the minimal generation example's device boundary by copying sampled tokens to CPU before appending them, and updates its hardcoded model path.

- [Keep generation context on CPU](#usage-evaluation)

## Problem

The minimal generation example appended the sampler's device-resident result directly to the tokenized context. With CPU context and CUDA sampling, that concatenation crosses devices. [source; call_a3548486e98a4b619654f1919346f5ff, call_88109a0a53e94d5f947057053b95757d, call_4b5cd173ce5d455188c6679d39e80538]

## Reasoning

Moving the sampled token to CPU at the append boundary preserves host-side context management without changing where model inference or sampling runs. [inference; call_6e5923199e46465caefccd8c17ccf138, call_733f6e5e6862439790df08bdad884bf3, call_0b8c1a71ea574a99a97b325b8ea808f3]

## Impact

Only the example changes: concatenation now uses sample.cpu(), and the hardcoded model directory switches from eval_models/.../2.0bpw to models/.../4.0bpw. The directory labels do not establish the contents or quality of those local artifacts. [source; call_6e5923199e46465caefccd8c17ccf138]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure; issue #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” reports quantization-quality problems. Neither discussion identifies this example's token-concatenation change. [source; call_9476092102104188aaf2a020d2faeb44, call_30719b25dad94e7eb949665a815cf83b]

<a id="usage-evaluation"></a>

## Keep generation context on CPU

Tokenizer.encode constructs the single-string token tensor without an explicit device. DefaultSampler uses temperature, top-p filtering and sampling; its sampling implementation operates on the logits' device and reshapes the result to the logits' leading dimensions without transferring it to CPU. [source; call_88109a0a53e94d5f947057053b95757d, call_af8d8ea2be7a4a4eac7e542576e07d51, call_4b5cd173ce5d455188c6679d39e80538]

The fix transfers only a non-stop sampled token before appending it along the sequence dimension. Stop-token detection still happens first. The appended token becomes the next iteration's input, while context length continues to determine past_len. [source; call_6e5923199e46465caefccd8c17ccf138, call_a3548486e98a4b619654f1919346f5ff]

Keeping context on CPU fits the existing model interface: Model.forward passes each intermediate through prepare_for_device, which moves it to the receiving module's device when necessary. The patch therefore fixes the application-side append rather than changing the sampler's return-device contract. [source; call_733f6e5e6862439790df08bdad884bf3, call_0b8c1a71ea574a99a97b325b8ea808f3, call_6e5923199e46465caefccd8c17ccf138]

The earlier entry describes this script as a low-level cached generation example and identifies the built-in generator as the higher-level alternative. This change retains that educational structure. [ancestor; call_7ed81a707cd9487a93c41b2bf0a3f9f6]

## Uncertainty and limits

No model inference or CUDA execution was performed; device-transfer correctness and runtime cost were assessed from source only.

A standard-library scalar computation cannot meaningfully validate PyTorch device placement or concatenation, so no substitute arithmetic test was run.

The hardcoded replacement model directory's availability and contents remain unverified.
