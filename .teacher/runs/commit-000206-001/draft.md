# 2cc8f718dacbd75c2cfc3cc229dc787090333bde


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/2cc8f718dacbd75c2cfc3cc229dc787090333bde) · [Evidence ledger](draft.json)

Adds reusable cosine-error and SQNR helpers and integrates them into layer comparison and conversion feedback, preserving existing Frobenius diagnostics.

- [Directional error and signal-to-noise diagnostics](#measures)

## Problem

Layer comparisons and conversion feedback previously reported relative Frobenius error without separate directional and signal-to-noise measures. [source; call_b9045d20e3114fae9eebfbe2856f0f86, call_bd4fc49a251d45fcacebfabf9f948a3f]

## Reasoning

Shared helpers provide complementary diagnostics: cosine error measures directional disagreement, while SQNR compares reference energy with squared reconstruction error. Neither replaces the existing relative Frobenius calculation. [source; call_1e97c72e53bb4954b38895431b4d9963, call_bd4fc49a251d45fcacebfabf9f948a3f]

## Impact

Both workflows print additional metrics. get_state_error now returns (relative Frobenius error, cosine error, SQNR); the whole-parent-tree search found one caller, and the diff updates it to unpack that tuple. [source; call_c4f1ec8732994e2b9f7cc7a8719df97c, call_bd4fc49a251d45fcacebfabf9f948a3f]

## Source Notes

The root entry's usage-evaluation and conversion chapters were read. They establish the pre-existing layerwise comparison and five-reference conversion diagnostics, rather than end-to-end quality guarantees. [ancestor; call_e9d3ec5e2c71445da594c997911756cf, call_3a30dd8b0f8742d3a856a2809bea100e]

The root conversion entry records a duplicated working-directory prefix hazard. That form is already absent from the inspected parent: main passes qtensors/<key>.safetensors to save_tensor, which adds work_dir once. The task does not change this. [source; call_881b309041344316adcfc8cd1173841c, call_bd4fc49a251d45fcacebfabf9f948a3f]

Discussion context includes PR #26, “Superior 3INST parameters,” which discusses numerical evaluation and names model_diff.py, and #33, “Error converting model,” whose later discussion uses that script to investigate GLM4 output. Their relevance here is inferred from the shared diagnostic file, not an established link to this commit. [inference; call_4d15259b0a0b4246871023dcd6038c3a, call_f04a3e4e62544b80b7e15e3f8f5f3630, call_b9045d20e3114fae9eebfbe2856f0f86]

Other inspected reports concern distinct conversion failures: #8 invalid reshape, #11 bias datatype, #16 invalid CUDA configuration, #38 Nemotron-Ultra conversion, #43 abliterated Qwen3 conversion, #34 last-layer LinAlgError, and #42 NaNs at 3.0 bpw. PR #13 concerns conversion without bos_token_id. Their overlap with this task is inferred only from conversion-file references; the metric additions do not establish fixes for those failures. [inference; call_c9d48dbf1adb471eb9c1de88e2d364eb, call_4fe5ae10570e4172a6c360138e8979f8, call_57502a1b873e4e1ba73675eeae393441, call_ce84bfd19b864fbea7dba74e2d4d849f, call_ec16a15170854194b60a7dfb40c90d8a, call_c7801a646baf4a78a4333e1587cefa95, call_2a018fc6c4704b978ea92ad446bc5ecc, call_7c4543d765c44399bd69687d14072425, call_bd4fc49a251d45fcacebfabf9f948a3f]

<a id="measures"></a>

## Directional error and signal-to-noise diagnostics

Both helpers preserve dimension zero and flatten the remaining dimensions. sqnr computes 10 times the mean base-10 logarithm of sum(b²)/(sum((a−b)²)+1e-8), treating b as the reference. The factor 10 expresses a power ratio in decibels. This is a mean of row-level dB values, not a ratio of pooled energies. [source; call_1e97c72e53bb4954b38895431b4d9963]

cosine_error returns one minus mean row cosine similarity, delegating normalization and epsilon handling to torch.nn.functional.cosine_similarity. Both helpers return Python scalar values through item(); neither changes its input tensors. [source; call_1e97c72e53bb4954b38895431b4d9963]

A scalar transcription using reference rows [1,0], [10,0] and approximations [1.1,0], [12,0] produced cosine error 0, mean-row SQNR 16.989698 dB and pooled SQNR 14.011770 dB. An identical unit-energy row gives 80 dB with the added epsilon. This illustrates magnitude sensitivity, averaging semantics and the finite perfect-match value without executing the repository helpers. [execution; call_54f52146ce004173a5f2a735d2f7aaa1]

model_diff computes the new measures before its existing in-place sa -= sb operation, preserving the original outputs for both diagnostics. It averages their results across evaluation sequences and renames the printed error field to rfn_err. The existing keep_b override still occurs first, so overridden layers compare cloned B states rather than independently propagated A outputs. [source; call_b9045d20e3114fae9eebfbe2856f0f86, call_8a1ef236b51e4bd0bfe4cbdad44bd7f4]

Conversion reshapes each output into vectors along its final feature dimension and casts to float32 before calculating all three measures. main compares converted outputs with retained unquantized-module references on the same incoming calibration states, accumulates the tuple components and divides each by the existing fixed reference count of five. [source; call_bd4fc49a251d45fcacebfabf9f948a3f, call_881b309041344316adcfc8cd1173841c]

The existing measurement gate remains i < num_ref_states and len(linears). Consequently modules without eligible linears print initialized zero values rather than measured cosine/SQNR results. Only the rfn display retains the num_slices == 1 restriction; cosine and SQNR are printed unconditionally. [source; call_bd4fc49a251d45fcacebfabf9f948a3f, call_881b309041344316adcfc8cd1173841c]

## Uncertainty and limits

No PyTorch implementation, model conversion, GPU workload or quality benchmark was executed. The numerical check transcribes formulas using Python double precision, not tensor reduction precision.

The helpers rely on view-compatible tensors and do not validate shapes, finite values or nonzero reference energy. The SQNR epsilon protects only the noise denominator; it does not establish finite results for zero-energy references.

No empirical justification for epsilon=1e-8 or diagnostic acceptance thresholds is supplied.
