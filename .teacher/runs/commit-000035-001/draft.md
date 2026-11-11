# 4fa0e6863e130adf7319d4b00293284c4f33296d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4fa0e6863e130adf7319d4b00293284c4f33296d) · [Evidence ledger](draft.json)

Derives cache counts and FP16 KV shapes from individual attention modules, with stricter page-copy shape checks and a suspected error in the detachment mismatch diagnostic.

- [Allocate KV storage from individual attention modules](#cache)

## Problem

Cache construction assumed a global layer count and identical KV head dimensions from configuration, rather than using each attention module's dimensions. [source; call_4d3197c0bba946c09569b8dcf62f3e7d, call_f52cd0e55f30432499c6435e1f3f99c0]

## Reasoning

The change makes the model's cache-capable modules the shared source of ordering, count and per-layer shape, aligning allocation with the attention implementation that consumes those tensors. [source; call_d6a0af50c736482eb7feacfd44457c56, call_4d3197c0bba946c09569b8dcf62f3e7d, call_c8b1be8a6f4742c8a487e9b992da4d64]

## Impact

Custom cache-layer constructors must now accept (config, attention, max_num_tokens). Whole-parent-tree searches found the built-in FP16 subclass and factory call, both updated by the patch; external subclasses remain unverified. [source; call_f888197448c647af93f3b0f1843a7908, call_c1e5f822f60f4c97aabde18836580553, call_4d3197c0bba946c09569b8dcf62f3e7d, call_f52cd0e55f30432499c6435e1f3f99c0]

<a id="cache"></a>

## Allocate KV storage from individual attention modules

Model.get_cache_layers memoizes the ordered traversal entries whose kv_cache capability is true. Cache uses this list for construction, attachment and detachment instead of counting configured hidden layers and independently filtering during attachment. [source; call_d6a0af50c736482eb7feacfd44457c56, call_525c79c6386a400eb175ee085b305b64, call_4d3197c0bba946c09569b8dcf62f3e7d]

CacheLayer retains its attention reference. FP16 storage becomes (max_num_tokens / 256, 256, attention.num_kv_heads, attention.head_dim), retaining the divisibility assertion. The first two axes represent pages and tokens per page; 256 is the repository's PAGE_SIZE. [source; call_4d3197c0bba946c09569b8dcf62f3e7d, call_f52cd0e55f30432499c6435e1f3f99c0, call_0e6993695b684e1a88e0ada403f4cf10]

A scalar shape check for 1,024 tokens produced 1,048,576 elements per tensor with eight 128-dimensional heads, versus 262,144 with four 64-dimensional heads. Both equal tokens × KV heads × head dimension; paging preserves element count. [execution; call_3890627ee31545fe875d5b1f88a227a2]

Attention.load allocates attached cache layers and unload frees them. decode_flash_attn reshapes new K/V using its own head dimensions, fetches cache.get_layer(self.layer_idx), and passes both to flash_attn_with_kvcache. The new allocation dimensions therefore match this existing consumer locally. [source; call_c8b1be8a6f4742c8a487e9b992da4d64, call_bbc519007ef6441db1e5bbddc83b56b5, call_f52cd0e55f30432499c6435e1f3f99c0]

Passing no attention produces shape=None and skips K/V allocation. Page copying now requires identical complete shapes, including page capacity, before retaining the existing tensor-slice copies; this is stricter than checking only the dimensions of the copied page. [source; call_f52cd0e55f30432499c6435e1f3f99c0, call_768448de2d2a405298f95a4593e8d5e2]

The base model initializes first_block_idx to None; Gemma2, Llama and Phi3 constructors set it to the current module-list length immediately before adding transformer blocks. The new cache enumeration does not use that index. [source; call_d6a0af50c736482eb7feacfd44457c56, call_b6159a38f1da4481a756577623230336, call_9f6492af05c4457b8e617626d5fcdab4, call_38db3bea50f74c0b82dfa6e7ff97fd9d]

## Authoring-time findings — pending review

### detach-count-diagnostic (suspected; defect)

The mismatched-layer detachment diagnostic calls an integer as a function.

Trigger: Call Cache.detach_from_model with assertions enabled and a model whose cache-layer count differs from the cache's count.

Expected: Raise AssertionError with the incompatible layer counts.

Actual: Evaluating the assertion message invokes model_num_layers(), producing TypeError instead. Matching counts bypass the expression. Whole-parent-tree search found no direct repository callers, only the definition and documentation reference.

Locations: 4fa0e6863e130adf7319d4b00293284c4f33296d:exllamav3/cache/cache.py — Cache.detach_from_model

Source evidence: call_4d3197c0bba946c09569b8dcf62f3e7d, call_dce31408ad4a4d66820c7c1faf387949

source_inspection: The patch assigns len(model.get_cache_layers()) to model_num_layers, then calls it in the failure message. [call_4d3197c0bba946c09569b8dcf62f3e7d]. Limits: No repository detachment workflow was executed.

scalar_transcription: A mismatched-count assertion with the same integer-call expression raised TypeError: 'int' object is not callable. [call_3890627ee31545fe875d5b1f88a227a2]. Limits: Standard-library reproduction of the expression, not execution of Cache.detach_from_model.

## Uncertainty and limits

No model loading, PyTorch allocation or Flash Attention execution was performed. Scalar checks validate only shape arithmetic and the transcribed assertion expression.

Support for heterogeneous dimensions is established at cache construction, not demonstrated end to end with a heterogeneous model. Attention still retrieves cache entries by layer_idx.

The memoized module list assumes stable model structure; attachment validates layer count, not destination attention dimensions.
