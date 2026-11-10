# 543c4b27714c6a677a6e714c452d62532f634cff


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/543c4b27714c6a677a6e714c452d62532f634cff) · [Evidence ledger](draft.json)

- [Modular model definitions](#models)
- [Checkpointed EXL3 conversion](#conversion)
- [Quantized linear runtime and CUDA](#quantized-runtime)
- [Queued generation and paged cache](#generation)
- [Model assets and installation](#loading-packaging)
- [Evaluation and numerical checks](#evaluation)

## Problem

The initial ExLlamaV3 release addresses architectural rigidity and parallel-inference obstacles described for ExLlamaV2, while introducing EXL3 quantization. [source; call_8b5b8202dbbb42bcb4e86b91d846c9f0]

## Reasoning

The design separates architecture definitions, reusable model modules, quantized linear operations, conversion and generation rather than presenting this as an incremental fix. [inference; call_4049a2eaeec945cbb088641fde728c94, call_79804882cb0646d9b0bb09be2189566e, call_f2bf061148a2407c87dd6fde1a419cbe, call_5142e6b865f04f06a231eef9429cfa26]

## Impact

Provides an early-preview workflow for converting models to EXL3 and generating text; the README explicitly says it is not yet a viable ExLlamaV2 replacement. [source; call_8b5b8202dbbb42bcb4e86b91d846c9f0]

## Source Notes

Performance and quantization-quality statements in the README are release claims, not measurements established by this inspection. [source; call_8b5b8202dbbb42bcb4e86b91d846c9f0]

<a id="models"></a>

## Modular model definitions

The architecture registry maps Llama, Mistral, Qwen2, Phi3 and Gemma2 causal-LM names to configuration and model classes. [source; call_efd8188d7bd7455d906075faf880f2d1]

The representative Llama implementation composes embeddings, RMSNorm, attention, gated MLPs and an output linear layer, with a tied-embedding fallback for the output head. [source; call_4049a2eaeec945cbb088641fde728c94]

<a id="conversion"></a>

## Checkpointed EXL3 conversion

Conversion processes modules sequentially, captures calibration statistics, allocates bitrates, quantizes linear layers and saves their tensors before compiling the output model. [source; call_f2bf061148a2407c87dd6fde1a419cbe]

Explicit resume restores saved arguments, module position and activation state; bitrate and calibration settings cannot be changed when resuming. [source; call_f2bf061148a2407c87dd6fde1a419cbe]

<a id="quantized-runtime"></a>

## Quantized linear runtime and CUDA

LinearEXL3 stores trellis data and scaling/sign tensors, applies Hadamard transforms, and selects either direct EXL3 GEMM or reconstructed-weight half-precision GEMM. Reconstruction is the default at 32 or more flattened input rows. [source; call_79804882cb0646d9b0bb09be2189566e]

The native GEMM wrapper maintains per-device CUDA properties and synchronization locks and checks tile divisibility before launching specialized kernels. [source; call_ef0da702bae84980876d6ec16cece247]

<a id="generation"></a>

## Queued generation and paged cache

The generator manages pending and active jobs, cancellation, prefill and streaming iterations, with optional draft-model decoding and matching main/draft cache capacities. [source; call_5142e6b865f04f06a231eef9429cfa26]

Cache objects attach per-layer storage to model modules. The default implementation allocates paged FP16 key/value tensors and supports copying page contents. [source; call_ceb05ee81fa74d42b7ef41f870b264f5]

<a id="loading-packaging"></a>

## Model assets and installation

SafetensorsCollection indexes tensor names across model-directory files. Tokenizer initialization reads tokenizer.json through Hugging Face tokenizers and merges special-token metadata. [source; call_948240dc33f9406eba6e0469909c2d52, call_c19a9826ee5744898106a44108cca339]

Packaging builds a PyTorch CUDA extension by default when Torch is available; EXLLAMA_NOCOMPILE disables precompilation for the documented JIT installation mode. [source; call_c54cf4a6a99b442289fc18e19b381dc8, call_8b5b8202dbbb42bcb4e86b91d846c9f0]

<a id="evaluation"></a>

## Evaluation and numerical checks

The comparison harness computes WikiText-2 perplexity through selectable backend adapters and plots results against decoder bits per weight or reported weight VRAM. [source; call_4af31fe7accb48babf1e434004b71e8d]

The GEMM test compares direct quantized and reconstructed execution across multiple batch sizes with 0.05 absolute and relative tolerances, but requires a hardcoded model path and CUDA device. [source; call_77a01772873f4a01b3025b5eb4df5402]

## Uncertainty and limits

No builds, tests, conversions or inference benchmarks were run.

Inspection covered representative implementations, not every architecture, attention path, sampler, generator job path or CUDA kernel. Binary benchmark plots, calibration corpora and Hadamard tables were not evaluated.

The preview documents required FlashAttention-2 and missing ROCm, tensor parallelism, cache quantization and multimodal support.
