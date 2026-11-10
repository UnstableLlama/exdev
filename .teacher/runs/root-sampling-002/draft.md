# 543c4b27714c6a677a6e714c452d62532f634cff


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/543c4b27714c6a677a6e714c452d62532f634cff) · [Evidence ledger](draft.json)

- [Composable sampling, Gumbel noise and native matching](#sampling)

## Problem

The initial implementation needs to turn model logits into token IDs while supporting greedy selection, stochastic sampling, distribution truncation and token restrictions. [inference; call_4538a78c98b145f4986006ae8cc7b68a, call_8d8a770164d94ecebcb305734e6b053b, call_be4c5c0b1a314625aa01e9738baf1048]

## Reasoning

Sampling is organized as composable Python transformations, with native CUDA noise generation and separately exposed fused sampling primitives. This permits several sampling policies to share distribution handling rather than duplicating complete implementations. [inference; call_8d8a770164d94ecebcb305734e6b053b, call_06541e8d34a44a78b9ca1cb120295f87]

## Impact

The public sampler package supplies default, greedy/argmax, categorical/Gumbel, top-k and top-p presets alongside custom sampling steps. [source; call_f2ecbd58ab334258a8527258c5e906d5, call_be4c5c0b1a314625aa01e9738baf1048]

## Source Notes

Native declarations and bindings expose argmax_sample, gumbel_sample, three Gumbel-noise variants, partial_strings_match and count_match_tensor. Exposure does not imply that CustomSampler uses the fused sampling functions: its inspected implementation calls noise functions followed by torch.argmax. [source; call_dd49543062ce4728bbd361518b9e8f4a, call_8edcb443c4f04b468c70febbeb264304, call_f460cc3cfe2f418698aaf2b326774b5b, call_06541e8d34a44a78b9ca1cb120295f87, call_8d8a770164d94ecebcb305734e6b053b]

<a id="sampling"></a>

## Composable sampling, Gumbel noise and native matching

CustomSampler.forward accepts logits, optional sequence IDs, a 32-bit seed, a tokenizer and blocked/allowed token lists. It flattens all leading logit dimensions into rows, runs the sampling steps and reshapes the selected IDs back to the original leading shape. sequence_ids is accepted but unused here. This is the local interface to generation; tokenizer.actual_vocab_size supplies the boundary for masking padded vocabulary entries. [source; call_4538a78c98b145f4986006ae8cc7b68a, call_8d8a770164d94ecebcb305734e6b053b]

SamplingState distinguishes input logits, working logits, weights, normalized probabilities and sorted variants carrying token-index mappings. SS_Normalize uses softmax for logits and division by row sums for weights; SS_Sort sorts descending and records original token indices. SS_Sample maps a selected sorted position back through indices[row, position]. These distinctions allow truncation to discard probability mass without requiring immediate renormalization. [source; call_8d8a770164d94ecebcb305734e6b053b]

Steps can substitute an alternative and request prerequisites: temperature 1 becomes SS_NoOp, top-k requests sorting, and top-p requests normalized sorted probabilities. However, CustomSampler.__init__ never advances its local state beyond INIT while constructing the list. Prerequisites are therefore chosen conservatively from INIT rather than from the preceding step's output. Runtime normalization and sorting often absorb the redundancy as no-ops; this is not a complete static state-transition planner. [source; call_8d8a770164d94ecebcb305734e6b053b]

SS_Temperature divides logits by T, or raises probability weights to 1/T and marks them unnormalized. For positive T these describe the same relative distribution. TopPSampler can apply temperature before truncation, changing which candidates survive, or afterward, changing weights within the retained set. DefaultSampler chooses T=0.75 and top_p=0.75; these are preset choices, with no derivation supplied here. CategoricalSampler maps T=0 to greedy selection; TopKSampler also does so for k=1, and TopPSampler for p=0. [source; call_8d8a770164d94ecebcb305734e6b053b, call_be4c5c0b1a314625aa01e9738baf1048]

Top-k keeps the first k sorted entries, replacing the rest with zero weights or negative-infinity logits; it uses a full sort rather than a partial top-k operation. Top-p computes inclusive cumulative probabilities and keeps entries whose cumulative sum is at most p, except that the first entry is always preserved. Thus it excludes the entry that first crosses the threshold, rather than retaining the smallest prefix reaching p. Top-k requires k>=1; SS_TopP requires 0<p<=1. [source; call_8d8a770164d94ecebcb305734e6b053b]

A scalar translation confirmed this top-p boundary: weights [0.5, 0.3125, 0.1875] at p=0.75 become [0.5, 0, 0]. The second entry would cross to 0.8125 and is removed. The example uses exactly representable binary fractions, avoiding ambiguity from a cumulative-sum rounding boundary. [execution; call_6b5b9ed714b54dc7b3c5d05c99388907]

Token restrictions precede the sampling chain. Vocabulary padding is masked in the caller's logits in place; blocked/allowed filtering subsequently clones the tensor. Blocked IDs receive negative infinity, while an allowed list masks every ID outside that list. Applying both therefore retains allowed IDs minus blocked IDs. No local check prevents an empty candidate set. If no seed is supplied, Python chooses an integer in [0, 2^32-1]; an explicit seed also resets the global Python and Torch random generators. [source; call_8d8a770164d94ecebcb305734e6b053b]

SS_Sample implements perturb-and-argmax: input logits use gumbel_noise_f16, working logits use gumbel_noise_f32, and probability weights use gumbel_noise_log, which takes their logarithm before adding noise. The latter two overwrite their working buffers. In ideal arithmetic, argmax(log(w_i)+G_i), with independent standard Gumbel noise, samples proportionally to positive weights w_i. Normalizing weights only adds a common offset to those scores, explaining why sampling can follow truncation without another normalization pass; zero weights become negative infinity. [inference; call_8d8a770164d94ecebcb305734e6b053b, call_194a4230e264440da50efe62b5ee9ba6]

The CUDA Gumbel transform is -log(max(-log(max(u, 1e-20)), 1e-20)). The two 1e-20 guards prevent logarithms of zero at either endpoint; they are numerical guards, not filtering thresholds. Noise kernels initialize Philox using the supplied seed and flattened element index. FP32 kernels process one value per thread; FP16 processes half2 pairs, adds noise in float, then rounds back to half. Consequently, the unmodified-temperature FP16 route is not numerically identical to the FP32 working-logit route. [source; call_194a4230e264440da50efe62b5ee9ba6, call_8d8a770164d94ecebcb305734e6b053b]

Binary64 evaluation of the guarded transform gives approximately -3.82976472 at u=0 and 46.05170186 at u=1. For logits [1,0,-1] and T=0.75, all 125 combinations of uniforms from {0.1,0.3,0.5,0.7,0.9} produced the same argmax using scaled logits, log normalized weights or log unnormalized weights. This checks the normalization identity on bounded inputs, not cuRAND output or native sampling frequencies. [execution; call_6b5b9ed714b54dc7b3c5d05c99388907]

Separate argmax_sample and gumbel_sample kernels fuse selection into one CUDA block per row, with 1024 threads scanning pairs of FP16 logits and reducing maxima. Their wrappers require two-dimensional half logits and long output tensors, and clamp max_logit to the stored width; zero means the full width. They run on the current CUDA stream. In contrast, CustomSampler materializes noisy values and delegates selection to torch.argmax. Fusion avoids that intermediate noise-output pass, but no speed advantage was measured. [source; call_3552dc40e6a64b049b6a42c3e9e9a42b, call_8d8a770164d94ecebcb305734e6b053b]

The fused Gumbel kernel seeds Philox with threadIdx.x but not blockIdx.x, so rows reuse the same per-thread noise streams for a given seed. It also differs from the standalone noise kernels' per-element initialization. Its read2f boundary checks are reversed for an odd max_logit: the low lane tests idx<max_logit-1, while the high lane tests idx<max_logit. Neither this reader nor the FP16 noise kernel guards the second lane of an odd-sized half2 tail. [source; call_3552dc40e6a64b049b6a42c3e9e9a42b, call_194a4230e264440da50efe62b5ee9ba6]

Scalar evaluation of read2f's masks with six stored logits and max_logit=5 admitted indices [0,1,2,3,5], excluding valid index 4 and admitting padded index 5. This demonstrates the predicate issue without executing a native memory access. [execution; call_6b5b9ed714b54dc7b3c5d05c99388907]

Generic greedy composition has a separate defect: SS_Argmax's sorted branches assign the indexed result to state.state instead of state.sample, then overwrite state.state with DONE. They also omit the row-wise indexing used by SS_Sample. A chain reaching these branches cannot correctly return its sample. Plain ArgmaxSampler starts at INIT and does not exercise those branches. [source; call_8d8a770164d94ecebcb305734e6b053b, call_be4c5c0b1a314625aa01e9738baf1048]

partial_strings_match consumes byte buffers containing UTF-32 query text, packed patterns and byte offsets; dividing by four yields codepoint lengths and offsets. It scans patterns in list order, returning a full-match start index, -2 for a query suffix matching a pattern prefix, or -1 for no match. These are immediate returns, not a global earliest-match search. count_match_tensor compares raw 64-bit elements until the first mismatch, bounded by min(max_a, b.size(1)); it performs no local dtype, device or a-length validation. [source; call_3e95264c92d84568b2eff54ceea70db8]

A codepoint-level scalar translation showed the string-order consequence: query 'abc' with patterns ['abcd','bc'] returns -2, whereas reversing the patterns returns 1. Thus an earlier partial match can hide a later full match. The helper's result is suitable for a caller to distinguish incomplete suffixes from completed matches, but it does not itself implement buffering, banning or termination policy. [execution; call_6b5b9ed714b54dc7b3c5d05c99388907]

Related chapters: generation (assembly link pending), loading-tokenization (assembly link pending), runtime (assembly link pending), usage-evaluation (assembly link pending)

## Uncertainty and limits

The executed checks are standard-library scalar translations, not executions of PyTorch, CUDA kernels, cuRAND or native string functions. Floating-point calculations use Python binary64 rather than CUDA float intrinsics and FP16 rounding.

No sampling-frequency, performance or end-to-end generation measurements were made. The Gumbel arithmetic check establishes agreement on selected inputs, not distributional correctness.

CustomSampler does not validate positive temperatures or ensure that token restrictions leave a valid candidate. Its generic composition also contains a sorted-argmax assignment defect.

Native half2 paths lack odd-length tail handling. The fused sampling boundary predicate and shared per-row noise require caution; their effects were inspected and scalar-emulated, not tested on a GPU.

String helpers assume suitable buffers, nonempty patterns and host-readable tensor storage without enforcing those contracts locally. Generator-side handling of their return values was not inspected.
