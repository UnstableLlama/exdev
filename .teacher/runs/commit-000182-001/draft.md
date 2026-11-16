# f1cfd3fb4e19a201a2738803fd4e57232ca1c481


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f1cfd3fb4e19a201a2738803fd4e57232ca1c481) · [Evidence ledger](draft.json)

Reuses multi-GEMM to combine eligible EXL3 K/V projections for at most 32 tokens, with sequential matrix selection and conditional two-matrix GPU concurrency.

- [Parallel K/V projection through reusable multi-GEMM](#attention)

## Problem

Attention previously invoked K and V projections separately. The change combines eligible EXL3 projections for small token batches, targeting greater GPU parallelism. [source; call_88a24655e6f6483fbee176ac53080c0d]

## Reasoning

The native edits are prerequisites for the attention call: the wrapper now accepts absent indices, and the kernel interprets them as sequential matrix selection rather than dereferencing a null pointer. [source; call_9eafcf70e8bc411785bb52749a865325, call_e4b991e8faab4693bc86d72915e068aa, call_88a24655e6f6483fbee176ac53080c0d]

## Impact

Q remains separate. Unfused K/V execution remains available when fusion is unavailable or batch size times sequence length exceeds 32; this is not a threshold on the number of KV heads. [source; call_88a24655e6f6483fbee176ac53080c0d]

## Source Notes

The earlier routed-expert entry establishes MultiLinear's origin and its equal-dimension, equal-bitrate, bias-free, unscaled preconditions. [ancestor; call_a140760372164d4ea0bf9fb8e02c8457]

That entry's all-expert fused-buffer mismatch is carried over: routing can select num_experts while buffers still use num_experts_per_tok, and the native index-count check remains. Moving MultiLinear does not repair this conditional BlockSparseMLP failure. [source; call_5000e232f340452e8626ee7d047f4743, call_b090f6abccdd436c831e32332e295c58, call_f9854c039dc24ddf91e7145f9a568c74]

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns conversion and tokenizer truncation. Its relationship here is only inferred shared-source context: its traceback passes through project_qkv, specifically the unchanged Q projection, rather than the new fused K/V call. [inference; call_52f9ca7fdfe34d07aba812b8700defed, call_88a24655e6f6483fbee176ac53080c0d]

<a id="attention"></a>

## Parallel K/V projection through reusable multi-GEMM

MultiLinear moves unchanged from block_sparse_mlp.py into its own module. It retains references to the linears and constructs device pointer tables for trellis weights and input/output transforms. Its constructor asserts uniform dimensions, bit width and experimental codebook multipliers, absent bias and softcap, and unit post-scale. Its unload method remains a no-op. [source; call_f9854c039dc24ddf91e7145f9a568c74, call_18165254a59c4f85a72b4da84373dcbe]

Attention.load attempts fusion when K and V are EXL3, have equal output widths and bit widths, and lack bias. MultiLinear then enforces its additional assertions. Attention initializes the helper to None and clears its reference during unload. [source; call_88a24655e6f6483fbee176ac53080c0d, call_18165254a59c4f85a72b4da84373dcbe]

For m = batch size × query length at most 32, project_qkv views the shared input as [1,m,hidden_size], allocates separate transformed-input scratch [2,m,hidden_size] and FP16 output [2,m,num_kv_heads×head_dim], and calls exl3_mgemm without indices or routing weights. Output slices 0 and 1 become K and V with their original three-dimensional shapes. [source; call_88a24655e6f6483fbee176ac53080c0d]

The existing kernel broadcasts a single input matrix across projections but applies each projection's own input transform, trellis multiplication and output transform. Omitting weights leaves the output-transform normalization unchanged. The three attention consumers—SDPA, uncached FlashAttention and cached FlashAttention—continue reshaping K/V into heads before normalization, RoPE and attention. [source; call_9a5f247c869d4bb6b902d05c358efe09, call_41e9c5dd08cb40388b38fcfc39f49bdd]

Whole-tree search found the existing Python multi-GEMM calls only in BlockSparseMLP: gate and up broadcast an input with selected-expert indices; down consumes per-expert inputs and supplies routing weights. Those calls remain indexed and use a single-token guard. Attention instead explicitly constructs two output slots and permits up to 32 tokens; it supplies no expert-routing data. [source; call_73d71e48f3dc4a9aa84945d0eab83d82, call_5000e232f340452e8626ee7d047f4743, call_88a24655e6f6483fbee176ac53080c0d]

The selector supports bit widths 1–8 and reduces the per-matrix grid using a tile-count heuristic divided by 12, marked experimentally chosen. The launcher then uses concurrency = min(total_sms / selected_sms, output_matrix_count). For K/V, this can schedule two matrix groups concurrently, but does not guarantee doubled parallelism. [source; call_116cfaf1d42a402ba84a3e29441d0d54, call_b090f6abccdd436c831e32332e295c58]

A scalar transcription with 80 total SMs yielded concurrency two for a 20-SM per-matrix grid, but one for 50- or 80-SM grids. It also confirmed that both [1,32] and [2,16] token layouts meet the cutoff, whereas [1,33] does not. [execution; call_877e13b4ddf246e1aabef11bbf00e538]

The implementation supports the stated small-KV-head motivation: narrow projections can leave capacity for another matrix group. The tradeoff is additional two-projection scratch/output allocation and a specialized path instead of separate Linear.forward calls; actual benefit remains workload-dependent. [inference; call_88a24655e6f6483fbee176ac53080c0d, call_b090f6abccdd436c831e32332e295c58, call_116cfaf1d42a402ba84a3e29441d0d54]

## Uncertainty and limits

No CUDA execution, numerical-equivalence test, or speed measurement was performed. The Python check models integer dispatch and shape arithmetic only.

The inspected source does not establish an empirical justification for the 32-token crossover.

Full compatibility of the new direct native call with every Linear instrumentation path and model-specific customization remains unestablished.
