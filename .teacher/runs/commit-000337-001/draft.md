# fb63886b9a9909ab78822780e82fd10d001dcd02


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/fb63886b9a9909ab78822780e82fd10d001dcd02) · [Evidence ledger](draft.json)

Stops 17 text-model hooks from copying the token tensor reference into forward metadata. Tokens still flow through the explicit argument, attention preparation is unchanged, and the base hook used by the two vision components still writes the key.

- [Pass token IDs as forward state, not duplicate metadata](#forward-params)

## Problem

The 17 text-model overrides of prepare_inputs put the incoming token tensor in params["input_ids"] even though they already passed it directly to prepare_for_attn and returned it as the initial forward state. Whole-parent-tree searches for the quoted key found writes, but no literal reads of that params entry. [source; call_629ac04040da4fcb817090ac7c13acd0, call_27cc19202ff34076b29cc6392f93344b, call_adfe8b74410c46aaa22a10b990f5d89b, call_87cb312dceca4cacb8d47ce1db6a8af4]

## Reasoning

The deletion makes the explicit tensor argument the only input-ID channel used by the inspected text forward path. The old assignment stored another reference, not another tensor allocation. Removing it avoids retaining that reference through a caller-owned params dictionary; the tradeoff is that out-of-tree hooks can no longer rely on these overrides to populate or refresh the entry. The commit message describes the removal but gives no further rationale. [inference; call_629ac04040da4fcb817090ac7c13acd0, call_60e991f0dac947768edb8afd5c42bd2e, call_406ed35fe2844d8da5e7a4d613ab98a5]

## Impact

Token IDs remain an argument to forward and prefill. A fresh params dictionary no longer gains an input_ids entry through the changed overrides, and an existing entry is left untouched rather than deleted or refreshed. This is not a global removal: the base Model.prepare_inputs still writes the entry, including when inherited by the Gemma3 and Mistral3 vision components, whose image-embedding methods pass image tensors through Model.forward. [source; call_629ac04040da4fcb817090ac7c13acd0, call_60e991f0dac947768edb8afd5c42bd2e, call_c00333a8a8114fc29908ac3ebe91e24f, call_820b04c567bc46b0b745267761dfb4bb, call_c303ddfe0bd047fe8161661ab150453e, call_b41dc5aa66f34f39ac1e8fc3644f4a19]

The parent Gemma3TextModel inherits the changed Gemma3 text override. MiMoModel, MistralModel and Qwen2Model each inherit the changed Llama override, so their own files need no deletion. [source; call_629ac04040da4fcb817090ac7c13acd0, call_2d27bc2581354e3193d77722b5330089, call_d4eb18739be94b15a6dd556713ad0460, call_bd100eb5289e4f8eab930618417ebb1f, call_5dd8fe3b0d9b4e808df4604dfea6ba69]

## Source Notes

The introducing models and modules chapters document the original duplicate token reference, attention preparation and prefill cutoff. The Gemma3 and EXAONE4 introducing entries document those adapters following the same convention, with attention guards in prepare_for_attn. The EXAONE4 entry also records a constructor failure that can prevent the changed hook from being reached, and a separate prefill-dictionary reuse problem. [ancestor; call_ed4b4cccf8824f0ba81c7a3268b381ea, call_c2cc75df97654d1e98f23e5d241da062, call_3a27c7bbdbe44096bd438416121688a2, call_5b1466ecd4c743aaab20f592d74fa384, call_e973643d7e1449b59f5d858827d09a8b]

The Gemma3 introducing entry recorded that Qwen3MoeConfig once supplied a bare class where the factory expected a component mapping. That mismatch is already absent in the parent, which supplies {"text": Qwen3MoeModel}; this patch does not repair it. The separate chat-formatting entry recorded Gemma prompt-format issues; the inspected parent still has the same formatter bodies and the patch does not edit them. The direct caller in examples/imgsearch.py now present in the parent passes only the user prompt, so it does not exercise the nonempty-system-prompt case. [source; call_7c0c8af6add14eff827e66fd1804777d, call_6c7b9ea6f1734759a4261317218550e7, call_60e991f0dac947768edb8afd5c42bd2e, call_c6b3905fef4347b09c5ea2ccdc3a9eb5, call_81b2b9431a4a48a4bea54d6856da6973, call_2d27bc2581354e3193d77722b5330089, call_90be03a7ddb34a9d9260d1a07efa3671, call_629ac04040da4fcb817090ac7c13acd0]

The discussion matches are inferred overlaps, not upstream references or evidence of a fix. #7, “quantizing model: undefined symbol: __cxa_call_terminate,” traces through models/model.py but fails importing the native extension, before forward. #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” names gemma3.py and traces a logits-width mismatch in generator/job.py. #52, “Error converting moonshotai/Kimi-Dev-72B,” points to a Llama GatedMLP precision workaround for a Cholesky failure. #53, “Command A support,” links cohere2.py and later reports a conversion failure; the changed Cohere2 line does not change conversion arithmetic. [inference; call_f7231abae77c4f66bfd1eac05a7a8a8a, call_3006de2d902d4db7ae4dc3595eda1aed, call_ab61164d60b44b9697f0fd87748bbe52, call_2e56705b819040c7ae215268bb0cdd6c, call_d0bd70fea77647018d587c69332b4ab9, call_629ac04040da4fcb817090ac7c13acd0]

Other inferred overlaps are likewise narrower than a causal link: #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, names Qwen3 and discusses RoPE scaling, not the token-reference write. #51, “dots.llm1 support,” concerns the model implemented in dots1.py, not this cleanup. PR #26, “Superior 3INST parameters,” mentions eval/model_diff.py as an evaluation tool; #33, “Error converting model,” also discusses model_diff.py after its original file-opening error and later discusses Gemma3 support. Neither identifies a reader of the removed key. [inference; call_7681f8350c304487b10f908e72012d6d, call_c7312efb727a4a2e9a54fec1ab82ca74, call_7da42b2e763d4367b748588d735ba131, call_6942063f832046839914886374f3b93c, call_9aac90dfe8e8411a8057e13ac954e58c, call_a2625be4ee084403aa6e724c6285b020, call_629ac04040da4fcb817090ac7c13acd0]

<a id="forward-params"></a>

## Pass token IDs as forward state, not duplicate metadata

The complete diff removes one assignment from each of Cohere, Cohere2, DeciLM, Dots1, ERNIE 4.5, ERNIE 4.5 MoE, EXAONE4, Gemma2, Gemma3, GLM4, Llama, Mistral3, Mixtral, Phi3, Qwen3, Qwen3 MoE and SmolLM3. Each still calls prepare_for_attn(input_ids, params) and returns its result. [source; call_629ac04040da4fcb817090ac7c13acd0]

The direct in-tree callers found were Model.forward, Model.prefill and the research sampler sample_qkv in science/kv_quant_exp.py. Each uses the return value as x and passes the dictionary separately. Embedding.forward reads IDs from x, including when it selects indexed multimodal embeddings. The quoted input_ids in eval/model_diff.py names a saved tensor; the evaluation loop passes the IDs as module state, not as that dictionary key. [source; call_a7f1381340d14f88914d3e4dd95faf60, call_60e991f0dac947768edb8afd5c42bd2e, call_0c524fe15c9e46e9b5b223f3c9507193, call_406ed35fe2844d8da5e7a4d613ab98a5, call_a2625be4ee084403aa6e724c6285b020]

Generation still supplies the token batch separately from its cache, block table, cache sequence lengths and indexed embeddings. prepare_for_attn still defaults to uncached FlashAttention; the uncached FlashAttention and SDPA preparation routes reject a supplied cache. Cached FlashAttention reads batch size from the tensor argument, accepts a supplied page table or builds one for a rectangular cache, and prepares position metadata. The rectangular sequence capacity must be divisible by PAGE_SIZE, 256 tokens per page. None of those checks or metadata writes depends on params["input_ids"]. [source; call_52edb1f72020429d9bbd55a263f67223, call_50ac22feb5394cce87cc49944929dacf, call_87cb312dceca4cacb8d47ce1db6a8af4, call_8ae73e4291594d87a02342674854da95]

A standard-library check extracted all 17 parent overrides and the attention preparation helpers, then applied the one-statement deletion to each extracted override. Across 102 paired cases covering default uncached, explicit SDPA and already-paged FlashAttention preparation, the returned object and other metadata matched. The changed versions omitted the key when absent and preserved its old value when supplied; the extracted base method still wrote it. [execution; call_a403aa1befb945d9b6cf5082b1978b50, call_629ac04040da4fcb817090ac7c13acd0, call_87cb312dceca4cacb8d47ce1db6a8af4]

## Authoring-time findings — pending review

### prefill-flag-survives-forward-params-reuse (suspected; defect)

The previously documented prefill flag problem is carried over. Removing the input_ids write does not reset the remaining dictionary state.

Trigger: Call Model.prefill through its last KV module, then reuse the same params object for Model.forward without clearing prefill, on a path that reaches a transformer block.

Expected: Ordinary forward runs the block's full attention and MLP path.

Actual: Prefill leaves prefill true and ordinary forward does not reset it. TransformerBlock can return after attention without applying the attention residual or running the MLP; ParallelDecoderBlock applies the attention residual but still skips the MLP. The inspected generation loop, draft path and Job prefill calls pass fresh dictionary literals, so this is a reachable direct-API reuse case, not an observed failure of those workflows.

Locations: fb63886b9a9909ab78822780e82fd10d001dcd02:exllamav3/models/model.py — Model.prefill / Model.forward, fb63886b9a9909ab78822780e82fd10d001dcd02:exllamav3/modules/transformer.py — TransformerBlock.forward / ParallelDecoderBlock.forward

Source evidence: call_629ac04040da4fcb817090ac7c13acd0, call_60e991f0dac947768edb8afd5c42bd2e, call_7b54daa7cae148b8b24fec1f80984229, call_2c1aa09596334880bdf8b0d4db0b42d7, call_77831956dff8452ca592499b9921f610, call_c7b130aa031644fc92108178bf406f08, call_50ac22feb5394cce87cc49944929dacf

source_inspection: Traced writes and readers of the flag in the parent, inspected the prefill call sites and compared them with the task deletion. [call_60e991f0dac947768edb8afd5c42bd2e, call_7b54daa7cae148b8b24fec1f80984229, call_2c1aa09596334880bdf8b0d4db0b42d7, call_629ac04040da4fcb817090ac7c13acd0]. Limits: No prefill or model forward was executed; the later call must get through attention for the described early return.

### exaone-null-pattern-still-blocks-input-preparation (suspected; external_compatibility)

The earlier EXAONE4 constructor blocker is carried over; the changed prepare_inputs implementation does not make the pinned 1.2B model constructible.

Trigger: Construct the default text component using the pinned LGAI-EXAONE/EXAONE-4.0-1.2B configuration, which has 30 layers and a null sliding_window_pattern.

Expected: Handle the absent schedule or reject it with a configuration diagnostic before attempting to index it.

Actual: The pattern resolves to None. The constructor evaluates len(config.sliding_window_pattern) for the first non-final layer, so construction stops before prepare_inputs can be called. Model.from_config is the inspected factory path to the constructor.

Locations: fb63886b9a9909ab78822780e82fd10d001dcd02:exllamav3/models/exaone4.py — Exaone4Model.__init__

Source evidence: call_5bfd8546f7664092866e2fca4896300e, call_69758a49ba3940afa121578f26da8c9f, call_12b21a862bf04d9b99766c2558fcb957, call_60e991f0dac947768edb8afd5c42bd2e, call_629ac04040da4fcb817090ac7c13acd0

source_inspection: Compared the pinned null pattern with the parent default and constructor expression, and checked that the task diff leaves them unchanged. [call_5bfd8546f7664092866e2fca4896300e, call_69758a49ba3940afa121578f26da8c9f, call_629ac04040da4fcb817090ac7c13acd0]. Limits: No model construction or checkpoint load was run.

## Uncertainty and limits

The whole-tree searches cover literal spellings and visible call sites, not dynamically constructed dictionary keys or out-of-tree consumers.

The bounded check ran extracted method bodies with a stand-in token tensor. It did not run the rectangular-cache branch's Torch allocations, real model construction, GPU kernels, generation, or a logits or memory comparison.

The edit is inside existing model classes but does not change architecture registration, configuration mappings, or checkpoint tensor names or dimensions. This annotation does not revalidate the full reference-checkpoint catalog; the pinned EXAONE-4.0-1.2B configuration was checked for the inherited constructor blocker.
