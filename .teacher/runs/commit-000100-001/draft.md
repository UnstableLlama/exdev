# c73467fb7789035d5bc42945733211d9aebf173b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c73467fb7789035d5bc42945733211d9aebf173b) · [Evidence ledger](draft.json)

Unifies Cohere parallel-branch input qmaps so attention and gated MLP reuse calibration Hessian accumulation and preprocessing, while retaining separate output-projection statistics.

- [Sharing calibration statistics across parallel branches](#modules)

## Problem

Cohere's parallel decoder supplies the same normalized input to attention and the gated MLP, but their different qmap names caused separate input-Hessian accumulation. [source; call_765d438621e54df28eafbe9ce665e63a, call_8a4dd16cefa74728952474442ec7090d, call_a536d815f3a4481ea1471eab163f5496]

## Reasoning

The change gives both Cohere branches the prefix block.parallel and changes attention Q/K/V and gated-MLP gate/up suffixes to .input. All five projections consequently address one capture record; attention output and MLP down projections retain separate records. [source; call_a9008611ef664582ab000acd7823e036, call_3d48b1f2c59f4ce5a692aec3062d1b22, call_bda037cd8dfa474e991ce81a31f32715, call_25a43f0e15cc454dad2505863b3565e4]

## Impact

Sharing eliminates one redundant hidden-width-square float32 accumulator per capture pass and permits reuse of its finalized decomposition. This supports a conversion-memory and computation optimization, not a measured inference-speed improvement. [inference; call_a536d815f3a4481ea1471eab163f5496, call_6e96072a6075412aa7c1827841737610, call_e6bb2e845414481485ff1b1fb7f0aa86]

## Source Notes

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” includes the same capture_H addmm_ statement inspected here. Its discussion attributes the reported failure to tokenizer truncation. The source overlap is an inferred contextual connection, not evidence that this patch fixes that issue. [inference; call_18dc192bf9e449b6b190e3f4582451e9, call_b24574b047f747b28909491b595abc99]

The other inspected reports concern “quantizing model: undefined symbol: __cxa_call_terminate,” incoherent cogito-v1-preview-qwen-32B output at bpw <= 2.5, and “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022.” They describe import/toolchain, quantization-quality, and compilation problems respectively; none establishes motivation for this qmap change. [source; call_e47224b4194546779c7457a48bedfb2a, call_1bd710ad4d3d4a5183a96d3ae85f63da, call_7d53c9113fbe439db6a9f56e7605561a]

<a id="modules"></a>

## Sharing calibration statistics across parallel branches

ParallelDecoderBlock.forward normalizes x once into y, then passes y to both branches. Attention.project_qkv applies Q, K and V projections to that input; GatedMLP.forward applies gate and up projections to its input before activation. Sharing their input statistic is therefore justified by the data flow, unlike merging statistics across sequential residual branches. [source; call_765d438621e54df28eafbe9ce665e63a, call_9320dc91b2a34dcaa52d97a166df5485, call_25a43f0e15cc454dad2505863b3565e4]

Linear.capture_H allocates H by qmap, remembers the first projection's weight key, and accumulates XᵀX and the row count only for that projection. With the new shared name, Q captures the common input and K, V, gate and up skip duplicate accumulation; their contributions are not added five times. [source; call_a536d815f3a4481ea1471eab163f5496, call_b24574b047f747b28909491b595abc99, call_9320dc91b2a34dcaa52d97a166df5485, call_a9008611ef664582ab000acd7823e036, call_bda037cd8dfa474e991ce81a31f32715, call_3d48b1f2c59f4ce5a692aec3062d1b22]

Conversion creates a fresh capture dictionary for each module slice, runs calibration samples, moves captured matrices to CPU, and passes capture_H[linear.qmap] to each linear conversion. Thus the shared string does not combine unrelated decoder layers. Sliced MLP conversion recaptures for each slice rather than sharing one dictionary across all slices. [source; call_b7ccdbf58f244a99abfd1c0e292ebac8]

finalize_capture_H divides by the sample count, regularizes the diagonal, chooses input sign flips and computes an LDL decomposition. Its finalized flag reuses H, L, su and diag on subsequent calls. Sharing therefore also couples the branches to one set of input sign flips and one preprocessing result; it is more than renaming a diagnostic label. [source; call_6e96072a6075412aa7c1827841737610, call_e6bb2e845414481485ff1b1fb7f0aa86]

The common suffix applies globally to Attention and GatedMLP, but other model builders retain distinct block.attn and block.mlp prefixes. The plain MLP class retains .up. The inspected parent-tree qmap search found consumers indexing by each linear's actual qmap rather than hard-coded .qkv or .up capture names. [source; call_29895b09fc734fa99d465512fc54b73a, call_25a43f0e15cc454dad2505863b3565e4, call_3d48b1f2c59f4ce5a692aec3062d1b22, call_bda037cd8dfa474e991ce81a31f32715]

A standard-library scalar transcription produced two identical old accumulators and one new accumulator, each with H=[[10,14],[14,20]] and count=2. Arithmetic also gives 64, 256 and 576 MiB for one float32 H at hidden widths 4096, 8192 and 12288 respectively; these are accumulator sizes, not measured total-memory savings. [execution; call_a9c3037a7b134ffba8c64ef1d6ab95eb]

The inspected CohereLabs configurations give hidden widths 4096 for aya-23-8B and aya-expanse-8b; 8192 for aya-23-35B, aya-expanse-32b, c4ai-command-r-08-2024, c4ai-command-r-v01 and c4ai-command-r-v01-4bit; and 12288 for c4ai-command-r-plus, c4ai-command-r-plus-08-2024 and c4ai-command-r-plus-4bit. For each, CohereModel passes that same explicit width to both branches, so the shared input-H shape agrees. No hidden-width default is involved. The two 4bit configurations additionally declare bitsandbytes quantization; configuration shape agreement alone does not establish that those checkpoints can be converted here. [source; call_ca96c460106b400b9e61717ac000ed2e, call_4d21bd9d15a648f0a25a1de595ef7122, call_1637b9f1ce4c43e8bcbe3ddff892df8b, call_4311a8001dac444f9810306f3f61dc9a, call_50925ad8644b44d184dc6fcc789ab071, call_a7fc16a28de6426eb54a55d0288b5e12, call_b253ea4c6e5944d59f2ffc87fc7fad05, call_324b708753d64732b5d35105f88d41d0, call_46f93af844da4e258743ee154191debd, call_c9f4c438f9f145f49d67bfe8b0d9f307, call_8a4dd16cefa74728952474442ec7090d]

## Uncertainty and limits

No repository conversion, CUDA execution, numerical-quality comparison, or peak-memory benchmark was run.

The scalar check models capture grouping with exact small integers; it does not reproduce GPU float32 accumulation or randomized quantization.

Configuration inspection establishes input widths, not end-to-end model compatibility, checkpoint loading support, or equivalence of converted weights.
