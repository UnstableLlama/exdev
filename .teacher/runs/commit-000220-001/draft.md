# c02ba9e2cf327335719bd34cb1e339afd98c5710


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c02ba9e2cf327335719bd34cb1e339afd98c5710) · [Evidence ledger](draft.json)

Adds LayerNorm to three TransformerBlock normalization annotations, aligning them with the existing interface without changing runtime computation.

- [Consistent normalization type hints](#modules)

## Problem

TransformerBlock's annotations allowed LayerNorm for mlp_norm but omitted it from attn_norm, attn_post_norm and mlp_post_norm. [source; call_91e8d02a269e4157826017a8a4cb5966]

## Reasoning

Adding LayerNorm to those three unions makes the declared normalization interfaces consistent without changing defaults, stored attributes or computation. [source; call_91e8d02a269e4157826017a8a4cb5966, call_69ffcde03d464a3888cac4f48db0f1db]

## Impact

This corrects the declared API rather than introducing a new normalization implementation or switching existing models to LayerNorm. [source; call_91e8d02a269e4157826017a8a4cb5966, call_6515bed50c9242ccb1074cd4a35a78e2]

## Source Notes

The initial modules entry describes the sequential attention and MLP residual branches and their normalization interfaces. [ancestor; call_0eaf9b022cd94440b7efdc6f9f75c044]

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” reports a conversion failure whose traceback passes through TransformerBlock.forward. Its discussion attributes the problem to tokenizer truncation. The shared file is an inferred contextual connection, not evidence that this annotation change fixes that failure. [inference; call_50930b8a49ee46489deb70078bf0a017, call_91e8d02a269e4157826017a8a4cb5966]

<a id="modules"></a>

## Consistent normalization type hints

All four TransformerBlock normalization parameters now declare RMSNorm | LayerNorm | None. LayerNorm was already imported, and both normalization classes expose forward(x, params, out_dtype). The block stores and registers the supplied objects without selecting an implementation by type. [source; call_91e8d02a269e4157826017a8a4cb5966, call_69ffcde03d464a3888cac4f48db0f1db, call_6515bed50c9242ccb1074cd4a35a78e2]

The unchanged forward path requests half output from input normalization, calls attention or MLP, optionally post-normalizes its output, then adds it to the residual. Thus the widened annotations describe interchangeable call interfaces, not mathematically interchangeable normalization operations. [source; call_69ffcde03d464a3888cac4f48db0f1db, call_6515bed50c9242ccb1074cd4a35a78e2]

Explicit constructors remain compatible: Llama, Phi3, Mixtral, Qwen3 and Qwen3-MoE supply RMSNorm input norms and omit post-norms; Gemma2, Gemma3 and GLM4 supply RMSNorm for all four slots. DeciLM supplies RMSNorm with active branches and None with disabled branches. None requires migration or starts using LayerNorm. [source; call_ea5a6b1c7b1a420ebaf83063998c1925, call_6515bed50c9242ccb1074cd4a35a78e2]

The additional reader in science/kv_quant_exp.py calls attn_norm.forward with the same arguments supported by both classes. The search found no TransformerBlock subclass overriding the changed signature. [source; call_ea5a6b1c7b1a420ebaf83063998c1925, call_9cb0b5d25f1149d589a8dcbe5e7cf13c, call_6515bed50c9242ccb1074cd4a35a78e2]

Unlike the initial entry's unconditional-branch implementation, the inspected parent guards absent attention and MLP branches. Active branches still rely on their input norms to initialize the intermediate tensor; the inspected constructors satisfy that precondition. This commit changes neither those guards nor that requirement. [source; call_69ffcde03d464a3888cac4f48db0f1db, call_6515bed50c9242ccb1074cd4a35a78e2, call_91e8d02a269e4157826017a8a4cb5966, call_0eaf9b022cd94440b7efdc6f9f75c044]

## Uncertainty and limits

No type checker, model inference or GPU execution was run. Python tooling inspected source only; this annotation-only change offers no useful numerical computation to validate.

Whole-tree literal and Python-source searches cover explicit callers and readers, not external users or dynamically constructed references.
