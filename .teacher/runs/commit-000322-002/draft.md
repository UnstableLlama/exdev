# ff21ee46edb9ba74d709257f482c809a7bd406d0


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ff21ee46edb9ba74d709257f482c809a7bd406d0) · [Evidence ledger](draft.json)

Fixes sequential TransformerBlock branches without a pre-norm by casting the current residual to FP16 at each branch boundary. Existing normalized paths and prefill ordering stay unchanged; the fallback does not extend to the parallel decoder or the KV research sampler.

- [Feed FP16 residual activations to branches without a pre-norm](#modules)

## Problem

TransformerBlock already allowed callers to omit either input normalizer, but a present branch still consumed the local variable y. Without an attention norm, attention read an unassigned y. Without an MLP norm, the MLP either read an unassigned y when attention was absent or reused the attention branch result instead of the updated residual. [source; call_f8108594c73a445fa2f8558a32dcc1c2, call_a6812e014dd140699d98b8634761887a]

## Reasoning

Each present branch now gets its own input: the normalizer's requested FP16 output when a norm exists, or x.half() when it does not. Casting the branch input, rather than reassigning x, preserves the residual stream's dtype while keeping the same input precision at the attention or MLP boundary. The fallback does not normalize, apply learned weights, or require a placeholder module. [source; call_a6812e014dd140699d98b8634761887a, call_f8108594c73a445fa2f8558a32dcc1c2, call_cd03ed4ec44642a392ce60739f5784a5, call_09e1604589214f979006c4e376ccb0b0]

## Impact

This fixes the shared sequential block for an active attention or feed-forward branch without a pre-norm. The inspected in-tree builders do not select that combination: they supply both norms, except DeciLM, which omits a norm only when it also omits that branch. The change does not register an architecture, alter checkpoint loading, or add the same fallback to ParallelDecoderBlock. [source; call_a6812e014dd140699d98b8634761887a, call_be8e0790b42a4a14b9f12954f53f35c4, call_8c663ef99e5a43f0b7358b0346b4a8c5, call_08d215a58de34109a304488c78d26a73]

## Source Notes

The initial modules entry describes the FP16 branch inputs, in-place residual additions, and attention-only prefill shortcut. The optional-branches entry records the missing-y defect and an empty-block allocation defect. The parallel-decoder entry documents the separate shared-input design and its unconditional dereferences. [ancestor; call_aea052e9c6964a9485edd2ef5deb87e8, call_c6d020af4f14404abba1acb42fb078c3, call_d0acb787447542c082d5c9e73b4f8137]

The parent still has the missing-y defect recorded by the optional-branches entry, and this diff removes it from TransformerBlock.forward. The earlier empty-block allocation failure is already absent in the parent: allocate_q returns an empty strategy and the incoming surplus before calling the allocator. The parallel block's missing-component behavior and plural projection access remain unchanged. [source; call_f8108594c73a445fa2f8558a32dcc1c2, call_a6812e014dd140699d98b8634761887a, call_7def27cb18f643f4875d35e258fa1327]

Closed issue #16, “RuntimeError: CUDA error: invalid configuration argument,” reports a conversion failure on a 3060. Its traceback contains the exact attention call retained by this patch, but it proceeds into the projection's Hessian capture and the logged Llama blocks have RMSNorms. In the discussion, turboderp attributes the failure to tokenizer truncation and reports overriding that setting. The matching frame shows shared execution, not evidence that the norm fallback fixes the reported error. [inference; call_9e66c47b3cff44d7898c61bdbb9aaa8a, call_a6812e014dd140699d98b8634761887a, call_be8e0790b42a4a14b9f12954f53f35c4]

Other matched discussions describe different operations: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” fails loading the extension before any block forward; PR #26, “Superior 3INST parameters,” proposes a codebook multiplier; #33, “Error converting model,” reports a file-open failure during compilation; #34, “torch._C._LinAlgError on last layer of quant,” #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” report Cholesky failures in quantization. Conversion or its imports are the overlap, not a matching missing-norm failure. [inference; call_27d349bdd591461eaeb7e99eb98cb1e3, call_ad6a58a6b521409abb991b6387bc91ea, call_9f2252b34cf44e329dc041b28f6b47cf, call_f12ee8086ea1477a9abe4975fa83b6ae, call_8e8638b2bf904a508b46fd858475f294, call_64a3289f2f9c487a852181133dc6e17a, call_a6812e014dd140699d98b8634761887a]

The other overlaps do not identify a use of the new fallback: PR #4, “chore: update config.py,” is a typo correction; #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports a logits buffer width mismatch, while both inspected Gemma 3 builders supply norms; #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” matches the autosplit error string, not the branch-input failure. #51, “dots.llm1 support,” discusses adding that model, whose parent builder supplies both norms. #53, “Command A support,” asks about availability of Command A quants and points to Cohere2, which uses the unchanged parallel block. [inference; call_b6b6e709fd9b4b5f828712916a532c32, call_ff51c7d69fcc4ae7bcca62f94b495e64, call_b182fc5f54874a378fada5790318e2d6, call_d7bfb825354b4635bf6fb0a54252735c, call_5826e29914ae47cb9cac65ba8285d66b, call_be8e0790b42a4a14b9f12954f53f35c4, call_22c21761b10042c7a6efae99a82d1b7a]

<a id="modules"></a>

## Feed FP16 residual activations to branches without a pre-norm

In ordinary sequential execution, attention consumes the incoming residual, optionally after pre-normalization; its result can pass through a separate post-norm before being added to x. The MLP independently prepares its input from that updated x, not from attention's output alone. If attention is absent, the MLP uses the incoming x. Both fallbacks are local to their own branch; neither depends on the other. [source; call_f8108594c73a445fa2f8558a32dcc1c2, call_a6812e014dd140699d98b8634761887a]

The FP16 handoff feeds Attention's Q/K/V projections, plain MLP's up projection, GatedMLP's gate and up projections, or BlockSparseMLP's reshaping and expert routing. The patch changes the supplied activation, not the branch's projection, activation, routing, or attention-backend selection. [source; call_a6812e014dd140699d98b8634761887a, call_531b726faecf43eba4eafc356f399b75, call_20ee14cbe1eb46288c6dd852dc601967, call_7798481680f440dc914039c5eac1e962, call_af84127f018d4815a47e80a5b62a61d6]

Sequential prefill still calls attention before returning x, bypassing attention post-normalization, both residual additions, the MLP, and final dtype conversion. There is no early return on this flag in a block without attention. Model.prefill sets it only for the last cache-affecting module and stops there. Cohere and Cohere2 use a different block: it normalizes once, supplies that same input to both branches, and adds the attention result before its prefill return. [source; call_f8108594c73a445fa2f8558a32dcc1c2, call_a6812e014dd140699d98b8634761887a, call_22c21761b10042c7a6efae99a82d1b7a, call_be8e0790b42a4a14b9f12954f53f35c4]

Builder inspection found explicit RMSNorm at both inputs in Llama, Phi3, Mixtral, GLM4, Gemma2, Gemma3 text, both Mistral3 construction sites, Qwen3, Qwen3 MoE, Dots1, Ernie 4.5, Ernie 4.5 MoE, and SmolLM3. Gemma3 vision supplies two LayerNorms. DeciLM independently pairs each no-op branch with a missing norm, so its absent norms are skipped by the existing outer branch checks. Generic dispatch can reach the patched forward from Model.forward, Model.prefill, the autosplit dummy forward, conversion calibration/reference/state advancement, and the inspected evaluation and KV experiment loops, if such a block is installed and reached. [source; call_a51932857c75465ba46a925025d94c24, call_be8e0790b42a4a14b9f12954f53f35c4, call_8c663ef99e5a43f0b7358b0346b4a8c5, call_628ded0ed52841ac976a7a41925d19ee, call_22c21761b10042c7a6efae99a82d1b7a]

An isolated before/after check extracted the parent forward body and applied the two diff additions in memory, using stub branches and standard-library binary16 rounding for half(). The parent raised UnboundLocalError for normless attention-only and MLP-only cases. With normalized attention producing 3 and the incoming residual at 10.001, the normless MLP received 3 before the patch and the FP16-rounded updated residual, 13.0, afterward. In the patched prefill case only attention ran and the stand-in residual returned as 10.001. [execution; call_de2ee1003d4d49b880256380bfccb988, call_a6812e014dd140699d98b8634761887a, call_f8108594c73a445fa2f8558a32dcc1c2]

## Authoring-time findings — pending review

### kv-sampler-still-requires-attention-norm (suspected; external_compatibility)

The KV research sampler reconstructs the pre-attention path directly and does not inherit TransformerBlock.forward's fallback.

Trigger: Use sample_qkv on a model whose targeted TransformerBlock has active attention but attn_norm=None, and reach that target rather than returning cached samples.

Expected: If the sampler is to accept this block shape, it should project from the same FP16 residual input as the block.

Actual: It calls module.attn_norm.forward directly and would raise AttributeError before projecting or reaching module.forward.

Locations: ba4304a44b267e88f3c882136302fd1e25c5384e:science/kv_quant_exp.py — sample_qkv

Source evidence: call_753685cb3bb44a70aeb5279cce60720c, call_c2efcac45b744aca835dc2d3df4d13b8, call_a6812e014dd140699d98b8634761887a

source_inspection: Located the direct norm reader and traced the script's top-level sample_qkv call and target-layer branch. [call_753685cb3bb44a70aeb5279cce60720c, call_c2efcac45b744aca835dc2d3df4d13b8]. Limits: The script targets a Llama checkpoint by default, and the inspected Llama builder supplies the norm. No failure is established for that default.

### parallel-block-still-dereferences-missing-components (suspected; defect)

ParallelDecoderBlock still accepts None components at construction but does not handle them in forward.

Trigger: Construct a parallel block without its input norm, attention, or MLP and reach the corresponding call; for the MLP, the prefill shortcut must not be taken.

Expected: Reject unsupported omissions during construction or handle them deliberately during forward.

Actual: The block calls .forward on None; omitting the input norm fails before either branch can execute.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/modules/transformer.py — ParallelDecoderBlock.forward

Source evidence: call_f8108594c73a445fa2f8558a32dcc1c2, call_a6812e014dd140699d98b8634761887a, call_08d215a58de34109a304488c78d26a73

source_inspection: Compared constructor defaults with unchanged forward calls, searched named constructors, and checked generic module dispatch. [call_f8108594c73a445fa2f8558a32dcc1c2, call_08d215a58de34109a304488c78d26a73, call_be8e0790b42a4a14b9f12954f53f35c4, call_22c21761b10042c7a6efae99a82d1b7a]. Limits: Both named builders, Cohere and Cohere2, supply all three components. Reach is conditional on direct construction or installation of a differently assembled block.

### plain-mlp-allocation-still-expects-plural-projections (suspected; defect)

The sequential and parallel block allocators still assume a plural projection interface even though both constructors accept a plain MLP.

Trigger: Call either block's allocate_q on a block containing a plain MLP with a valid quantization budget.

Expected: Pass the plain MLP's up and down projections to allocation or explicitly reject the unsupported block configuration.

Actual: The allocator reads .ups and .downs, but plain MLP exposes .up and .down. Argument preparation fails with AttributeError before allocate_transformer runs.

Locations: ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/modules/transformer.py — TransformerBlock.allocate_q, ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/modules/transformer.py — ParallelDecoderBlock.allocate_q

Source evidence: call_f8108594c73a445fa2f8558a32dcc1c2, call_7def27cb18f643f4875d35e258fa1327, call_a6812e014dd140699d98b8634761887a

source_inspection: Checked the allocator and projection definitions, the conversion loop's generic allocate_q call, and the Gemma3 vision constructor that supplies a plain MLP. [call_6e7b1269369743748c0a2ee11bc3e348, call_b773298964ac4fd0a7050d15cdd20ae7, call_05640e36b5d545b0a05d3ee3426dc69f, call_1ea347f82a074ff492ba0b6785a7e5db, call_1b3b692f17f64bc1b5a8997b48fbecbe]. Limits: The inspected converter selects the text component by default, so the Gemma3 vision construction alone does not establish a failure in ordinary conversion. The named parallel builders use gated MLPs.

### prefill-flag-can-leak-into-ordinary-forward (suspected; defect)

The inherited prefill shortcut still depends on mutable caller parameters that Model.prefill leaves set.

Trigger: After Model.prefill reaches its last cache-affecting module, reuse the same params dictionary for ordinary Model.forward without removing or resetting prefill, and reach a TransformerBlock with attention.

Expected: An ordinary forward should apply the residual and feed-forward computations rather than the last-cache-layer shortcut.

Actual: Model.forward does not reset the flag. The sequential block returns immediately after attention with the incoming residual, skipping the attention residual update and MLP. The new FP16 fallback does not change this.

Locations: ba4304a44b267e88f3c882136302fd1e25c5384e:exllamav3/models/model.py — Model.prefill, ff21ee46edb9ba74d709257f482c809a7bd406d0:exllamav3/modules/transformer.py — TransformerBlock.forward

Source evidence: call_22c21761b10042c7a6efae99a82d1b7a, call_f8108594c73a445fa2f8558a32dcc1c2, call_a6812e014dd140699d98b8634761887a

source_inspection: Traced the parameter mutation and generic dispatch, searched prefill call sites, and checked that the minimal generation example supplies a fresh dictionary for normal forward. [call_9e705bab9a8a47c5bbb0c613a36f4500, call_628ded0ed52841ac976a7a41925d19ee, call_22c21761b10042c7a6efae99a82d1b7a, call_7c5cb12f981640c1b7df999e027deb00]. Limits: The direct API reuse scenario is conditional; this is not evidence that the bundled generator or example reuses the dictionary.

## Uncertainty and limits

The bounded Python check executed isolated versions of the forward method with stand-ins. It did not import ExLlamaV3 or exercise PyTorch tensor aliasing, dtype promotion, actual normalization, GPU attention, cache writes, quantization, or model loading. It establishes branch order and argument selection, not model accuracy or performance.

No named in-tree builder was found that selects an active branch without its norm. The literal searches and constructor inspection do not cover external callers or dynamically assembled or modified blocks. The commit does not identify a motivating checkpoint.
