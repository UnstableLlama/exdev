# c2ec220c83d4a697f4726401aa8c7e6a5a551fa6


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c2ec220c83d4a697f4726401aa8c7e6a5a551fa6) · [Evidence ledger](draft.json)

Reduces EXL3 host work through final-shaped output allocation, fewer native checks and cached kernel-attribute setup; speedup and CUDA behavior remain unmeasured.

- [Reduce repeated EXL3 host-side work](#linear-exl3)

## Problem

The EXL3 forward path performed output reshaping and native validation on each call, while both GEMM launchers repeatedly configured the selected kernel's dynamic shared-memory allowance. [source; call_60447eedf2af40ac82449842eb60c593, call_628ca38259c24e5b962e2af2de2a1b64]

## Reasoning

The Python and native shape edits are coupled: allocating the final output shape requires checking C's last dimension rather than dimension 1 and removing the comparison between flattened input rows and C's first dimension. [source; call_60447eedf2af40ac82449842eb60c593, call_628ca38259c24e5b962e2af2de2a1b64]

## Impact

The change reduces repeated host-side work but also removes checks for transform-vector lengths and transformed-input scratch storage. Performance improvement is plausible, not measured here. [inference; call_60447eedf2af40ac82449842eb60c593, call_628ca38259c24e5b962e2af2de2a1b64]

## Source Notes

The root quantized-inference entry establishes the direct-versus-reconstructed execution design and its storage preconditions. The attention ancestor establishes that multi-GEMM also serves fused K/V projections, so the native attribute cache is not confined to LinearEXL3.forward. [ancestor; call_cba56da87aed43379ed2e539032e1cf2, call_343843f09f0d4b748dae04f7ac382043]

The root entry's packed-sign forward concern no longer matches the inspected parent: construction unpacks su/sv into suh/svh. Its single-GEMM zero-grid concern is also changed: the current selector clamps the block count to at least one. Neither correction is introduced by this task. [source; call_7ab550cbada6415aa55f09b6a6966620, call_de6b7703dba54c8291401323720c3c65, call_628ca38259c24e5b962e2af2de2a1b64]

Issue #11, “AssertionError: bias is wrong datatype,” reports a constructor failure during DeepCoder conversion. Its connection is inferred from the shared exl3.py file, not an upstream link to this optimization; the parent already converts float bias to half. Issue #39, “Gemma 3 architecture not in list?”, concerns branch availability and later frontend/BOS discussion, not evidence of this optimization's benefit. [inference; call_d1338b42908a4148842435f134ef7bad, call_4f40f838d1c54be686a2eb859def01a5, call_7ab550cbada6415aa55f09b6a6966620]

<a id="linear-exl3"></a>

## Reduce repeated EXL3 host-side work

forward now allocates y directly as input-leading-dimensions plus out_features and returns it after bias addition. The direct branch avoids the final output view; the reconstructed branch creates a two-dimensional alias y_ for hgemm and the output Hadamard. Both branches still allocate transformed-input scratch. [source; call_628ca38259c24e5b962e2af2de2a1b64]

The reconstruction policy remains params['reconstruct'] when supplied, otherwise more than 32 flattened input rows. This is a row-count crossover, not a changed threshold. Reconstruction still obtains a dense inner weight matrix, multiplies it, and applies the output transform. [source; call_7ab550cbada6415aa55f09b6a6966620, call_628ca38259c24e5b962e2af2de2a1b64]

Native GEMM still derives m and k from flattened A and n from B's second dimension times 16, then writes through C's raw pointer. Consequently the final-shaped allocation supplies the same contiguous element count without requiring a two-dimensional C object. The factor 16 corresponds to the packed weight tile dimension. [source; call_cfc06a17617f49ab97a88965a8bb3d3e, call_60447eedf2af40ac82449842eb60c593, call_628ca38259c24e5b962e2af2de2a1b64]

A standard-library scalar check verified equal final-shaped and flattened output element counts for leading shapes (), (1,), (2,3), and (2,4,5), with output width 128. It did not execute repository tensor operations. [execution; call_9511efe71d1344ae9b8473180f416c72]

Whole-tree search located direct native calls in LinearEXL3 and qgemm_benchmark.py. The benchmark retains two-dimensional output buffers, which agree with the new last-dimension check, and supplies correctly sized transforms plus input storage as scratch. The native declaration's argument types remain unchanged. [source; call_518f9603196d41619b33da5c713e5fe9, call_81219970e2a8469d8ab973a545b238fb, call_e2c6bede4bbd4195acc792e6995e444c, call_60447eedf2af40ac82449842eb60c593]

Both launchers consult a shared std::set<void*> before cudaFuncSetAttribute and insert the kernel pointer after calling it. Repeated selections of that pointer skip configuration; launch arguments and requested shared-memory size remain unchanged. The cache key contains neither device identity nor configuration-call success. [source; call_60447eedf2af40ac82449842eb60c593, call_cfc06a17617f49ab97a88965a8bb3d3e]

Output dtype selection becomes an or-chain with precedence call override, instance default, then half. The added profile_opt import initializes an identity profiling decorator if none exists; this diff adds no decorated function or active timing instrumentation. [source; call_628ca38259c24e5b962e2af2de2a1b64, call_4978b413705c428aa61e9248afd08819]

## Uncertainty and limits

No CUDA execution, numerical-equivalence test or CPU-overhead benchmark was performed.

The scalar check establishes output element-count arithmetic only, not PyTorch view behavior or GPU memory safety.

Multi-device and concurrent-call behavior of the process-global kernel-pointer cache remains unverified; eligible CUDA documentation was not inspected.
