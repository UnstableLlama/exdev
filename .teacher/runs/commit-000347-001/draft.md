# 1258dfb4ddedaa8be3f6388f2c79f520dc7d0583


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/1258dfb4ddedaa8be3f6388f2c79f520dc7d0583) · [Evidence ledger](draft.json)

Adds block-level TP export and reconstruction for TransformerBlock. The wrapper delegates slicing to child methods that are not yet implemented in-tree, and no loader invokes it. The parent's stale allocator import still blocks a clean module import.

- [Export and reconstruct a transformer block through its children](#transformer-tp-split)

## Problem

The parent can estimate tensor-parallel allocations, but its TransformerBlock has no interface for exporting its loaded children and rebuilding a block on another device. This change adds that interface; it does not connect it to model loading or implement the child-level split. [source; call_1c6ee98a90f7496b87ba583580f1959f, call_29b6a3e662e347a08c12e30522ff58f3, call_03fe5facc08c4c879c4e8eeee4c81060, call_28ae1a6ff89744489e6ef28900082726]

## Reasoning

The block handles composition rather than slicing. It passes the plan unchanged to each present child, and import dispatches through the class in each child's payload. That lets different normalization, attention and MLP implementations own their reconstruction rules, but means the block cannot export a present child that lacks the protocol. The parent's planner produces a list of per-device dictionaries of half-open ranges keyed by component; the new block methods neither select one of those dictionaries nor look up or validate any range. [source; call_03fe5facc08c4c879c4e8eeee4c81060, call_29b6a3e662e347a08c12e30522ff58f3, call_ec231f47dbdd4111b2db25383ef8bbf3, call_eb5aaee36d8748fbb2076325d2f95632]

Allowing Config | None describes the new constructor use, rather than changing how ordinary blocks are built. The constructor already forwards config to Module, which stores it without dereferencing it. Reconstruction can therefore pass None and supply already-imported children; it does not reopen the checkpoint or call the recursive loader. This is a narrower contract than cloning a block for arbitrary reuse: conversion still reads module.config.stc after loading a module, but its inspected path builds and iterates the ordinary base model, not TP imports. [source; call_03fe5facc08c4c879c4e8eeee4c81060, call_1c6ee98a90f7496b87ba583580f1959f, call_21a962cfa0f64dc2b323e3072a5853fb, call_08edf9e097cd4b279ee38607867add75]

## Impact

A parent-tree AST scan found 17 direct TransformerBlock constructor calls. Every one still supplies config=config, and none overrides qbits_key: DeciLM, Dots1, Ernie 4.5 dense and MoE, Exaone4, Gemma2, GLM4, Llama, Mixtral, Phi3, Qwen3 dense and MoE, and SmolLM3 each have one call; Gemma3 and Mistral3 each have two. None needs a constructor update for the widened annotation. The literal search also found the package re-export and the KV quantization experiment's isinstance check, not another constructor or subclass. [source; call_ec841734ea734550b40c7580577a9cfe, call_c04a9c8f091f4c34905564c26e999f21, call_03fe5facc08c4c879c4e8eeee4c81060]

The parent's whole-tree searches found no tp_export or tp_import definitions or calls. The task adds only the block methods and their delegated calls, not a caller that initiates export or import. Model.load_gen still rejects tensor_p with an explicit single device and raises NotImplementedError in its tensor-parallel branch; ordinary multi-device loading still uses _load_autosplit. ParallelDecoderBlock and TransformerBlock.forward are unchanged. [source; call_ec231f47dbdd4111b2db25383ef8bbf3, call_eb5aaee36d8748fbb2076325d2f95632, call_28ae1a6ff89744489e6ef28900082726, call_03fe5facc08c4c879c4e8eeee4c81060]

## Source Notes

The supplied attribution names turboderp. The message, “TransformerBlock: TP split,” matches the new block-level handoff; the diff does not show tensor slicing, a communication step, or a working end-to-end TP loader. [source; call_03fe5facc08c4c879c4e8eeee4c81060]

The root entry's modules chapter describes the original explicit child registration, recursive loading, and sequential attention and MLP residual branches. It also describes the original unconditional child calls; that is not the current forward contract, which already guards missing attention and MLP and falls back to half input when a pre-norm is absent. [ancestor; call_cb28f1ef115c416a996e009b1b891c9a, call_1c6ee98a90f7496b87ba583580f1959f]

The immediate parent entry, “TP: Refactor/fix auto allocation,” distinguishes planner ranges from loaded shards and records both the stale transformer import and the empty-child allocation assertion. The task retains both conditions, as detailed in the findings. [ancestor; call_8cf068669d904488b1b9ef3d543b2b3d, call_c0edd512aeb24f4dbf4422f6a26ae9dc]

Closed issue #16, “RuntimeError: CUDA error: invalid configuration argument,” reports an RTX 3060 conversion failure for a Phi-4 fine-tune. Its traceback uses the same `self.attn.forward(y, params)` call in TransformerBlock.forward and proceeds to Linear.capture_H; the maintainer attributed the report to tokenizer truncation and said it was overridden at tokenizer load. The matching forward line connects the report to the file, not to the new TP methods. [inference; call_6bef48da2147466f838874c0847c0fc4, call_1c6ee98a90f7496b87ba583580f1959f, call_03fe5facc08c4c879c4e8eeee4c81060]

Issue #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” quotes the current non-TP autosplit error. Issue #54, “GPU split isn't followed here?”, asks why TabbyAPI's requested splits do not match observed allocation and reports improvement after changing the allocator setting. Their loading context matches the separate _load_autosplit branch, not evidence of either report reaching the new block methods. [inference; call_e726701d9277481c8c92c4065936f81e, call_d2c3617dd81a47c9a6804c45f5580824, call_2a4c9c23376845f3a3ca99ee2c09d493, call_28ae1a6ff89744489e6ef28900082726]

The conversion-path overlaps are distinct: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” fails loading a native extension after entering via convert_model; #33, “Error converting model,” reaches compile_model and fails reopening a tensor file; #34, “torch._C._LinAlgError on last layer of quant,” reports a Cholesky failure on a model using ParallelDecoderBlock; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” reports a NaN warning and a failure at lm_head; #52, “Error converting moonshotai/Kimi-Dev-72B,” reports Cholesky failures for some conversion settings. They share the conversion source path, not a TP method call. PR #26, “Superior 3INST parameters,” proposes a quantizer multiplier change; #53, “Command A support,” begins as a support and quant availability request. Neither framing identifies a block export or import problem. [inference; call_2c647e0f156e4270b98378388bfe4c1e, call_85f74d2724fd4b1c88530955c87ffcb7, call_174cb4aa55bb496f9f7e267ab26c0fba, call_0d59ce6a6d07460e9d97f1493507418b, call_d9047dafe7184046ac12a13d78bdf5bb, call_f4a3a0e0b6824195bde83289d6c84475, call_5dcfc90d125f495e834573270b9c8a38, call_08edf9e097cd4b279ee38607867add75]

Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” cites Gemma3 source and reports a logits-buffer copy size mismatch, not a reconstruction failure. Issue #27, “Attention Backend,” asks about FlashInfer versus FlashAttention; its overlap is the attention component, whose forward dispatch the task leaves alone. PR #4, “chore: update config.py,” is a spelling correction, not a change to the Config object or to this constructor's use of None. [inference; call_b9c3b3e6b2e64ea6aa03922a94178c95, call_7d923359a753441d88d69fd2ab104618, call_864d46bc21624ac0956b0efd89b207cd, call_03fe5facc08c4c879c4e8eeee4c81060]

<a id="transformer-tp-split"></a>

## Export and reconstruct a transformer block through its children

tp_export asserts that the block's device is set. It emits TransformerBlock as the class, a kwargs dictionary containing key and out_dtype, the source device, and six named child slots: attention input norm, attention, attention post-norm, MLP input norm, MLP, and MLP post-norm. Absent children are written as None. No child tensors are sliced at this level. [source; call_03fe5facc08c4c879c4e8eeee4c81060]

tp_import reads the destination from local_context['device'], not the exported source device. It reconstructs each nonempty payload via that payload's cls.tp_import, passing the same context and plan; a missing or falsy child payload becomes None. The regular constructor re-registers the returned children in block order and derives num_slices from the imported MLP, or uses one without an MLP. The wrapper then sets its own device; child placement is up to child import. [source; call_03fe5facc08c4c879c4e8eeee4c81060, call_1c6ee98a90f7496b87ba583580f1959f, call_21a962cfa0f64dc2b323e3072a5853fb]

A standard-library transcription kept all six slots empty for a childless block, used the destination rather than source device, and reset a custom qbits_key to bits. An unloaded wrapper hit the assertion before dispatch, while a loaded wrapper with a dummy child lacking tp_export raised AttributeError. These results check only the transcribed Python logic. [execution; call_e33d2913a5cc4561b48500151773b242]

## Authoring-time findings — pending review

### stale-transformer-allocator-import (suspected; defect)

The task retains the parent's mandatory import of TPAllocation from the removed util.tp_split path.

Trigger: Import exllamav3.modules in a clean installation after earlier import prerequisites succeed, or enter it through an architecture import, conversion's import of Linear, or the KV quantization experiment.

Expected: The module package exposes its classes without needing the obsolete allocator module.

Actual: The package initializer eagerly imports transformer.py, whose stale import is expected to stop initialization before either TP hook can be used. This can affect non-TP callers, even ones requesting only Linear.

Locations: 1258dfb4ddedaa8be3f6388f2c79f520dc7d0583:exllamav3/modules/transformer.py — TPAllocation import

Source evidence: call_1c6ee98a90f7496b87ba583580f1959f, call_f54357267f8a4818b8a86cc9c426cb03, call_03fe5facc08c4c879c4e8eeee4c81060, call_ebce8f81a1004a81b4afc96e12d4eace, call_30ff8c0f0a17465dada9512fcf6bf216, call_c04a9c8f091f4c34905564c26e999f21

source_inspection: Checked the missing parent file, surviving import, eager initializer, and named importers against the single-file task diff. [call_f54357267f8a4818b8a86cc9c426cb03, call_03fe5facc08c4c879c4e8eeee4c81060, call_ebce8f81a1004a81b4afc96e12d4eace]. Limits: No package import ran; a stale installed copy or shim could mask the missing path. A bare import that has not reached exllamav3.modules is not shown to fail here.

### missing-child-tp-protocol (suspected; new_requirement)

The new wrapper methods require a child protocol the task does not implement for ordinary children.

Trigger: After bypassing the unrelated stale import, directly export a loaded TransformerBlock with an ordinary child, such as the first RMSNorm in Llama; or directly import a nonempty child payload naming an ordinary class with no tp_import.

Expected: A supported child can supply or reconstruct its shard payload; an unsupported child is diagnosed before treating the block as exportable.

Actual: The wrapper calls the missing child method without a capability check. Export reaches an AttributeError at the first present child that lacks tp_export; import likewise cannot dispatch to a missing tp_import.

Locations: 1258dfb4ddedaa8be3f6388f2c79f520dc7d0583:exllamav3/modules/transformer.py — TransformerBlock.tp_export / TransformerBlock.tp_import

Source evidence: call_03fe5facc08c4c879c4e8eeee4c81060, call_ec231f47dbdd4111b2db25383ef8bbf3, call_eb5aaee36d8748fbb2076325d2f95632, call_2dee764793114506b5252e854c6e511c

source_inspection: Searched the whole parent tree for both protocol names and checked the new dispatch against the ordinary block construction and unchanged loader. [call_ec231f47dbdd4111b2db25383ef8bbf3, call_eb5aaee36d8748fbb2076325d2f95632, call_28ae1a6ff89744489e6ef28900082726]. Limits: Reach is a direct call or externally supplied payload; no in-tree loader reaches the wrapper.

scalar_transcription: A loaded stub with one present child lacking the method raised AttributeError for tp_export. [call_e33d2913a5cc4561b48500151773b242]. Limits: Stub dispatch only; no real norm or imported child ran.

### empty-block-allocation-still-asserts (suspected; defect)

The new payload can represent a childless block, but the inherited planner record collector still cannot return an empty record list for one.

Trigger: With assertions enabled and imports working, call make_tp_allocation on a DeciLM block whose attention and FFN are both marked no_op.

Expected: Return no allocation records for a block with no child work.

Actual: The absent children are not registered, so Module.make_tp_allocation asserts before collecting records. The task's new export/import methods do not replace this collector.

Locations: 1258dfb4ddedaa8be3f6388f2c79f520dc7d0583:exllamav3/modules/module.py — Module.make_tp_allocation

Source evidence: call_21a962cfa0f64dc2b323e3072a5853fb, call_545b9b22f7dc43d48e006532d71afbf8, call_1138ef41142d4b85a726749cc3690d30, call_03fe5facc08c4c879c4e8eeee4c81060

source_inspection: Followed both no-op branches through child registration to the unchanged collector. The whole-parent search found recursive Module and shared-expert calls but no explicit model-level collector invocation. [call_297185778dee4ced8a51e6f424efc453, call_21a962cfa0f64dc2b323e3072a5853fb, call_545b9b22f7dc43d48e006532d71afbf8, call_1138ef41142d4b85a726749cc3690d30]. Limits: Applies to direct collection or a traversal that reaches the childless block, not ordinary DeciLM forward or export of an already loaded childless block.

## Uncertainty and limits

No installed-package import, model load, real child round trip, CUDA execution or distributed communication ran. The standard-library payload check modeled Python dispatch and metadata only; it did not run repository methods with PyTorch modules or validate a transport format.

Literal tree searches and direct-call AST inspection do not establish dynamic callers, out-of-tree implementations, or compatibility with a future child protocol.
