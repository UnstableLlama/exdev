# 543c4b27714c6a677a6e714c452d62532f634cff


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/543c4b27714c6a677a6e714c452d62532f634cff) · [Evidence ledger](draft.json)

- [Calibration, allocation and resumable model conversion](#conversion)

## Problem

The change introduces a conversion workflow that turns an unquantized model into EXL3 artifacts using calibration activations, per-linear bit allocation and resumable module-by-module processing. [source; call_9d2b40cccc554bb6b665e280ba5ead68]

## Reasoning

The workflow separates calibration statistics, bitrate selection, quantization and artifact assembly. Allocation is a fixed size-based heuristic: the collected Hessians guide quantization, not a measured search over bitrate assignments. [source; call_cce9dff1e4174d77bb097f15f6d990a9, call_9d2b40cccc554bb6b665e280ba5ead68]

## Impact

Conversion produces intermediate per-module safetensors and activation checkpoints, then assembles model shards, configuration and accompanying non-weight files. [source; call_9d2b40cccc554bb6b665e280ba5ead68, call_8da4ef03d346401aab6deb5459623bf0]

## Source Notes

The executable entrypoint delegates argument handling and conversion to prepare() and main(); quantization itself is reached through Linear.convert_exl3() and quantize_exl3(). [source; call_18fd7337a065427d8047e24a64992ba2, call_1e4b09cdc5d541ed80d4115afa932442]

<a id="conversion"></a>

## Calibration, allocation and resumable model conversion

prepare() requires a working directory and, for a new job, input/output directories and a bitrate. Defaults are 100 calibration rows, 2048 tokens per row, a separate head target of 6 bits, 8192-MiB shards and a 60-second minimum checkpoint interval. New jobs save args.json and initialize ckpt/job.json with next_module_idx=0 and surplus_bits=0. Resume reloads those arguments and the checkpoint; normal differing nonzero overrides of bitrate, head bitrate and calibration dimensions are rejected, while paths, shard size and checkpoint controls may change. main() constructs Config, Model and Tokenizer and uses cuda:0, except for modules advertising prefer_cpu. [source; call_9d2b40cccc554bb6b665e280ba5ead68]

get_default_calibration() mixes C4, code, multilingual, technical, Wikipedia, TinyStories-style text and random token IDs with weights 10:15:15:10:48:10:20. Text-source row counts are floored with a minimum of one; random data fills the remaining requested rows, also with a minimum of one. Article-based processors concatenate articles until a row is full, discard overflow rather than carrying it forward, and request BOS/EOS on alternating output rows. Line shuffling and random-token generation each seed their respective RNG with zero. Raw-text processors instead slice one tokenized stream. These paths do not validate that enough articles or tokens exist to fill the requested shape. [source; call_32c398d9528d4612a7881d7107a353a8]

A bounded standard-library reproduction gives default source counts of 7, 11, 11, 7, 37, 7 and 20 rows: 100 rows, or 204800 tokens if every row is full. Requesting one row instead produces seven because every source has a one-row minimum. This checks the distribution arithmetic, not the corpus contents or tokenizer output. [execution; call_2ee0325924484acfbb857b2ba18165b0]

main() processes one top-level module at a time. For modules with quantization maps, it first forwards all current calibration states through the unquantized module using flash_attn_nc and a shared capture dictionary, retaining the first five outputs as references. After conversion, it forwards the same input states through the converted module and stores outputs on CPU for the next module. Thus later modules are calibrated on states propagated through already-converted predecessors, rather than an independent full-precision pass through the entire model. Modules without quantization targets are still saved and propagated; the final module only computes outputs for the first five reference rows. [source; call_9d2b40cccc554bb6b665e280ba5ead68, call_0034c7aa543148d792892e8c288fad58]

Linear.forward() captures its input before applying the linear operation. capture_H() flattens all leading activation dimensions into samples, copies them to FP32 and accumulates H += XᵀX plus the sample count. H is therefore an uncentered activation Gram matrix, not a Hessian obtained by differentiating the language-model loss. A qmap identifies a shared input: first_key allows only the first associated linear to accumulate, avoiding duplicate contributions when projections share activations. Each matrix has shape in_features × in_features. [source; call_1e4b09cdc5d541ed80d4115afa932442, call_0034c7aa543148d792892e8c288fad58]

The quantizer interface consumes that capture dictionary. finalize_capture_H() divides H by the sample count, adds 0.025 times its mean diagonal to every diagonal entry by default, applies shared input sign flips and normalized 128-wide Hadamard transforms, and computes a 16-wide block LDL factorization. The 0.025 constant is relative diagonal regularization, not an absolute threshold. The finalized flag caches H, L and input signs for other linears sharing the qmap. The converter supplies each linear with seed=top-level module index and K=its allocated integer bitrate. Linear.convert_exl3() passes FP32 weights in input-by-output orientation, discards the original inner layer, and installs LinearEXL3 with the returned tensors while preserving the bias. [source; call_fcc2e7116b4b41bebe097aa4b6eb9abc, call_1e4b09cdc5d541ed80d4115afa932442, call_9d2b40cccc554bb6b665e280ba5ead68, call_807ec78285a14212bdeb994d7e0d5aa2]

Memory is managed by staging rather than loading the whole model for conversion. Captured H matrices move to system RAM with their original devices recorded; original linear weights and biases are also swapped to CPU and restored one linear at a time. Quantization restores the needed H and keeps a CPU copy of the cached LDL factor. Calibration states reside on CPU between modules, and each processed module is unloaded. This trades host memory and transfer work for lower simultaneous GPU residency; the source does not quantify the resulting memory savings or runtime. [inference; call_9d2b40cccc554bb6b665e280ba5ead68, call_807ec78285a14212bdeb994d7e0d5aa2, call_fcc2e7116b4b41bebe097aa4b6eb9abc]

allocate_transformer() budgets B=int(target_bpw × weight_count)+incoming_surplus+1 and derives a base bitrate from B/weight_count, with a minimum of one. It considers 24 combinations: six fixed Q/K/V/O increment patterns crossed with four gate/up/down patterns, clamping each resulting bitrate to eight. It sorts candidates by weighted bit cost and chooses one near the budget, returning unused bits for the next module. These patterns favor particular projections without consulting capture statistics or proxy errors. allocate_linear() instead floors its effective budget to one bitrate, with a minimum of one but no eight-bit cap. TransformerBlock and Linear route their configured qbits_key into these helpers, allowing separate decoder and head targets. [source; call_cce9dff1e4174d77bb097f15f6d990a9, call_a94c6f10a2e142a5a4f7fb8304e955b9, call_1e4b09cdc5d541ed80d4115afa932442, call_9d2b40cccc554bb6b665e280ba5ead68]

The allocator has a subtle boundary condition: bisect_right(options, (budget,)) places the one-element search tuple before any equal-cost (cost, pattern) tuple, so an exactly matching candidate is excluded when a lower candidate exists. The explicit +1 adds one bit of slack but does not eliminate every equality case. A scalar reproduction with seven 128-weight projections selected 2688 bits from a 2689-bit budget; with 127 incoming surplus bits it still selected 2688 despite an available exact 2816-bit candidate. A target of 0.5 bits selected the minimum 896-bit candidate against a 449-bit budget, yielding −447 surplus. These are arithmetic edge checks, not model results. [execution; call_2ee0325924484acfbb857b2ba18165b0]

The workflow reports three different quantities. proxy_err is the quantizer's normalized H-weighted error in transformed/scaled weight coordinates, with its denominator floored at 1e−8. rfn averages the relative Frobenius output error against up to five retained unquantized-module references, dividing by the fixed num_ref_states=5. Reported final module bpw instead counts actual tensor payload bytes ×8 divided by module weight count. Consequently allocated K is not the complete storage bitrate: exported scales, biases and other module tensors contribute to the latter. Neither diagnostic is an end-to-end perplexity measurement, and printed timers are instrumentation rather than results observed here. [source; call_fcc2e7116b4b41bebe097aa4b6eb9abc, call_9d2b40cccc554bb6b665e280ba5ead68, call_8da4ef03d346401aab6deb5459623bf0]

After each module, conversion collects get_tensors() recursively and writes qtensors/<module-key>.safetensors. The active quantizer exports packed trellis indices and FP16 channel-scale vectors suh/svh; LinearEXL3 receives those tensors plus the original bias. Saving untouched module tensors through the same interface keeps quantized and nonquantized parts together. There is a path-handling hazard: main() passes an already work_dir-prefixed filename to save_tensor(), which joins work_dir again. An absolute work_dir avoids the duplicate prefix; a relative work_dir can produce a nested, unintended destination. [source; call_9d2b40cccc554bb6b665e280ba5ead68, call_fcc2e7116b4b41bebe097aa4b6eb9abc, call_1e4b09cdc5d541ed80d4115afa932442]

Checkpoint state contains the next module index, carried surplus bits and the list of propagated activation tensors—not partially accumulated Hessians or an in-progress linear quantization. At an eligible module boundary, the converter writes ckpt_new/job.json and state.safetensors, removes the previous ckpt_old, then renames ckpt to ckpt_old and ckpt_new to ckpt. Resume skips modules before the saved index and reloads the saved activations; work after the last checkpoint is replayed. There is no forced final checkpoint. The two renames are not one transaction, and prepare() does not fall back to ckpt_old if interrupted between them, so this is resumability machinery rather than a demonstrated crash-safe protocol. [source; call_9d2b40cccc554bb6b665e280ba5ead68]

compile_model() means artifact assembly, not native-code compilation. It reads qtensors through SafetensorsCollection and groups complete top-level modules into shards using tensor payload sizes. shard_size is multiplied by 1024², so its advertised MB unit is effectively MiB. A module larger than the limit is kept whole with a warning: the limit is a packing target, not a hard maximum. Output is model.safetensors for one shard or numbered model-xxxxx-of-yyyyy.safetensors files plus an index containing total_size and weight_map for multiple shards. [source; call_8da4ef03d346401aab6deb5459623bf0]

Assembly copies top-level auxiliary files while excluding original safetensors, their index, config.json and common weight/checkpoint extensions. It then rewrites the original configuration with quant_method='exl3', package version, requested decoder bits and requested calibration dimensions. The separate head bitrate is commented out of this metadata; the configuration is therefore not a complete record of the per-linear allocation. Existing output directories are only warned about, not cleaned, and an index is written only for multi-shard output, so reusing a directory can leave stale artifacts. [source; call_8da4ef03d346401aab6deb5459623bf0]

Related chapters: quantizer (assembly link pending), quantized-inference (assembly link pending), modules (assembly link pending), loading-tokenization (assembly link pending), usage-evaluation (assembly link pending)

## Uncertainty and limits

No model conversion, GPU kernel, quality evaluation or interruption/recovery test was executed.

The bundled calibration corpora were not inspected or tokenized; their adequacy for every requested row count and tokenizer is unverified.

The standard-library checks reproduce allocation and row-count arithmetic, not the imported PyTorch conversion implementation or floating-point Hessian computation.

The inspected code does not establish the quality rationale for the calibration mixture or fixed bitrate preference patterns.
