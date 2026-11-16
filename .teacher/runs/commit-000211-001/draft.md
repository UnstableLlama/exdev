# 00ad26e86660724a794c09bb808741493703ad47


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/00ad26e86660724a794c09bb808741493703ad47) · [Evidence ledger](draft.json)

Adds experimental per-module, per-projection bitrate increments after allocation, with an eight-bit cap. Existing budgets are not rebalanced, sparse experts remain unlabeled, and malformed modifier strings are unchecked.

- [Experimental projection-specific bitrate increments](#conversion)

## Problem

Conversion previously consumed the allocator's per-projection bitrates directly. This change adds an experimental command-line mechanism for increasing selected projection bitrates in selected top-level modules. [source; call_403b85e4b530416fbaf91435295dd886, call_9fd9768f05a149038c2f3c01a9654c7d]

## Reasoning

Projection-role labels decouple the modifier syntax from checkpoint tensor names. The labels, recursive module lookup and post-allocation transformation are cooperating edits: the converter needs all three to resolve a strategy key to its requested increment. [source; call_545ffba9123a4b79bfd2c8e8ebe9f639, call_e8e718697b434e7283fb15225ebef25a, call_3b41d76ac58c436a8bb9ccc030a109bb, call_403b85e4b530416fbaf91435295dd886]

## Impact

The modified values become quant_args['K'] before individual linears are converted. The original allocator surplus is retained, so these additions are not compensated by reducing subsequent allocations. The diff explicitly leaves overall bitrate-increase accounting and checkpoint tracking as TODOs. [source; call_403b85e4b530416fbaf91435295dd886, call_9fd9768f05a149038c2f3c01a9654c7d]

## Source Notes

The initial commit's modules and conversion chapters were read. They describe recursive module traversal, the Linear conversion interface and size-based allocation rather than an error-driven bitrate search. [ancestor; call_e7596e1ada4b44f2a4adaac62b5464fa, call_d3e7e097a5054f6da6d8b593df118707]

The earlier conversion entry's duplicate work-directory prefix is absent from the inspected parent: main passes relative qtensors and checkpoint filenames to save_tensor. The task leaves those calls unchanged. Its recorded exact-budget allocation boundary remains in allocation.py, also unchanged. [source; call_9fd9768f05a149038c2f3c01a9654c7d, call_ffda75607db44f058b7806df2904b05f, call_403b85e4b530416fbaf91435295dd886]

PR #26, “Superior 3INST parameters,” concerns codebook multipliers and includes experiments with per-tensor bitrate recipes. Its connection to this task is an inference based on the shared convert_model.py strategy-to-K handoff and manual projection increments; it is not an explicit link to this commit or evidence of this option's quality gains. [inference; call_7627db8c56db4470aecbbee3da8b8ff1, call_5d7b0b5c3459459380c8e38231db071a, call_403b85e4b530416fbaf91435295dd886]

Other matched discussions report different failures: #33 “Error converting model” covers file-opening failure and later GLM sampling trouble; #34 “torch._C._LinAlgError on last layer of quant,” #42 “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” and #43 “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated” concern invalid calibration states or factorization. Their relationship here is inferred only from shared conversion/Linear traceback paths, not evidence that bitrate modifiers fix them. [inference; call_a19daa724711446cb8ba592826a55170, call_9b98aaf7e83e425f80a7eaa33e6c8e75, call_a1c5f97086844ce09ad7bcb51e1167c6, call_e3604df8103a43a897dc222d91cf4042, call_2b9f06888b5640978124907e80cc47a7, call_a0ddb93be4fd4d7d896856279348b01a]

Likewise, #8 “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” #11 “AssertionError: bias is wrong datatype,” #16 “RuntimeError: CUDA error: invalid configuration argument,” #38 “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” and PR #13 “Fix a tokenizer issue while converting models without a bos_token_id defined” concern padding, bias dtype, tokenizer truncation, sliced loading and missing BOS respectively. Shared conversion paths suggest contextual relevance, not a causal connection to this feature. [inference; call_a7949b60a546416b850a8e0928adeb51, call_a61c40c964e34fa0a532cf679f007327, call_690ea0c981994637aa36150922d51ca1, call_a050e23b7b904ae4967b4764c2436df3, call_7c5c1d5b39714dcb938d371df68119b6]

<a id="conversion"></a>

## Experimental projection-specific bitrate increments

-strat/--strategy accepts a string, with parser default None and prepared default ''. prepare stores it with the job arguments. Its normal nonempty changed value is not overridable on resume unless --override_anyway is supplied. The helper uses args.get('strategy'), so absent or empty values preserve the existing strategy. [source; call_403b85e4b530416fbaf91435295dd886, call_9fd9768f05a149038c2f3c01a9654c7d]

mod_strategy prepends an empty entry to the semicolon-separated string and indexes it with enumerate(model.modules)'s index. Thus the first supplied segment targets top-level module index 1, not an independently discovered transformer-layer number. Empty segments make no increments; indices beyond the supplied list return the original allocation. [source; call_403b85e4b530416fbaf91435295dd886, call_9fd9768f05a149038c2f3c01a9654c7d]

Each segment is parsed as consecutive two-character pairs: a role character followed by a single digit converted with int. Repeated roles overwrite earlier increments; unknown roles have no matching effect. For each strategy key, the helper finds the submodule and computes min(original_bits + increment, 8). Eight is the bitrate ceiling, matching the existing transformer allocator's cap; this is not a percentage or storage-byte limit. [source; call_403b85e4b530416fbaf91435295dd886, call_ffda75607db44f058b7806df2904b05f]

Attention labels Q/K/V/output projections q/k/v/o. Ordinary MLP labels up/down u/d; GatedMLP labels each constructed gate/up/down projection g/u/d, including slices. These are separate from qmap, which groups shared calibration inputs, and qbits_key, which chooses the base decoder or head budget. [source; call_545ffba9123a4b79bfd2c8e8ebe9f639, call_e8e718697b434e7283fb15225ebef25a, call_04098d9a96ca48159eda4c36ba913d8d, call_00af7fbd9b1e4271a1ad21e28baed229]

Module.find_module follows the existing Model.find_module pattern: return the first exact key match while traversing the subtree, otherwise implicitly return None. Existing test callers of the model-level lookup immediately load their named result without a missing-key guard. The new converter likewise assumes a match, but supplies keys generated by allocation from the block's own projections. Lookup runs before loading/slicing, against the registered module tree. [source; call_cba3cdb1e1924020952e55f7d2e60417, call_00af7fbd9b1e4271a1ad21e28baed229, call_ffda75607db44f058b7806df2904b05f, call_3b41d76ac58c436a8bb9ccc030a109bb, call_403b85e4b530416fbaf91435295dd886]

Whole-tree Linear call inspection found no existing call passing the shifted optional arguments positionally. Heads in cohere, cohere2, decilm, gemma2, gemma3, glm4, llama, mixtral, phi3, qwen3 and qwen3_moe use keyword arguments and retain the empty modifier label. BlockSparseMLP's routing gate and expert gate/up/down constructors also remain unlabeled: g/u/d modifiers therefore do not increase those expert projections. The default empty label preserves constructor compatibility but limits feature coverage. [source; call_f1901270134e479083dc83aadea72306, call_e7a7272480d342ca89f465e55427eccb, call_9f6eb6031cd84828990fa9ea6e340b68, call_e8e718697b434e7283fb15225ebef25a]

A standard-library scalar transcription verified that q1k2 increases initial q=k=3 to 4 and 5, repeated q1q2 leaves a +2 increment, and q1;d2 affects indices 1 and 2 while leaving indices 0 and 3 unchanged. It also observed IndexError for q and ValueError for q-1. This did not execute the repository converter. [execution; call_a44b959a4b3040c3bb87190e1c361b9c]

This is an additive experiment layered over the existing size-budget heuristic, not a replacement allocator. It trades explicit local control for loss of the original global budget accounting. Leaving the option unset preserves the previous allocation path; changing --bits instead continues to use the allocator's projection patterns and surplus propagation. [inference; call_403b85e4b530416fbaf91435295dd886, call_ffda75607db44f058b7806df2904b05f, call_9fd9768f05a149038c2f3c01a9654c7d]

## Authoring-time findings — pending review

### strategy-input-validation (suspected; defect)

Malformed strategy segments reach unchecked pair indexing or integer conversion during conversion.

Trigger: Supply --strategy q, or a segment such as q-1, and reach its indexed top-level module.

Expected: Reject malformed modifier syntax with an actionable argument-validation error before processing modules.

Actual: s[1] raises IndexError for an odd trailing character; int(m) raises ValueError for a nondigit. main calls the helper before loading that module, with no local error handling.

Locations: 00ad26e86660724a794c09bb808741493703ad47:exllamav3/conversion/convert_model.py — mod_strategy

Source evidence: call_403b85e4b530416fbaf91435295dd886, call_9fd9768f05a149038c2f3c01a9654c7d, call_f5610c3678054515b208b0bd40c48b71

scalar_transcription: Reimplemented the inspected pair parser and observed IndexError for q and ValueError for q-1. [call_a44b959a4b3040c3bb87190e1c361b9c]. Limits: No repository conversion ran. The direct caller is the newly added main call; no parent-tree mod_strategy callers existed.

### inherited-exact-budget-boundary (suspected; defect)

The inherited allocator can exclude an exactly affordable candidate; the modifier feature does not repair that boundary.

Trigger: allocate_transformer has a candidate costing exactly budget and a lower-cost candidate preceding it.

Expected: The largest option within budget should include an exactly equal-cost candidate.

Actual: bisect_right(options, (budget,)) orders the shorter search tuple before equal-cost (cost, pattern) tuples; subtracting one selects an earlier candidate.

Locations: 49ac13c04f4c622582e2d519f2d135a53c1c4eaf:exllamav3/conversion/allocation.py — allocate_transformer

Source evidence: call_ffda75607db44f058b7806df2904b05f, call_e2f6e12b67574031a25b981477d4efa1, call_00af7fbd9b1e4271a1ad21e28baed229, call_403b85e4b530416fbaf91435295dd886

source_inspection: Compared the allocator with both direct callers, TransformerBlock.allocate_q and ParallelDecoderBlock.allocate_q, and the task's subsequent modifier call. [call_ffda75607db44f058b7806df2904b05f, call_00af7fbd9b1e4271a1ad21e28baed229, call_403b85e4b530416fbaf91435295dd886]. Limits: Carried-over source observation previously recorded in the initial conversion entry; no fresh model allocation execution or quality measurement.

## Uncertainty and limits

No model conversion, GPU execution, quality benchmark or resume/recovery test was performed. The scalar check models parsing and integer arithmetic only.

The inspected source establishes modifier behavior, not an accuracy-optimal recipe or the author's precise experimental motivation.

Repository call-site inspection does not establish compatibility for external positional callers of Linear; the new parameter is inserted before fkey.
