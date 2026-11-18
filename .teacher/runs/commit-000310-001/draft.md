# 08dde73e664b997091370894072065f1f15055bf


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/08dde73e664b997091370894072065f1f15055bf) · [Evidence ledger](draft.json)

Adds stateful Formatron filtering and consolidates token restrictions into additive logit masks. Source inspection identifies speculative-mask refresh, prefix-reset and list-cache concerns, while inherited sampler and banned-string defects remain.

- [Stateful Formatron constraints through additive logit masks](#generation)

## Problem

Generation had only commented-out filter integration. Token restrictions were assembled inside receive_logits and passed as blocked/allowed ID lists to CustomSampler. [source; call_ffef006ce8514b9e9f59ba416b3c8555, call_b2d4c662eb5c4610817c51b61a81e426, call_369c3ad9ea594ca5bfda0cd7f302d487]

## Reasoning

A shared additive mask lets grammar constraints, minimum-length stop suppression, banned-string retries and token healing use one sampler interface. Scheduling grammar work around model.forward is intended to overlap CPU constraint computation with GPU work; no speedup was measured. [inference; call_ffef006ce8514b9e9f59ba416b3c8555, call_b2d4c662eb5c4610817c51b61a81e426, call_369c3ad9ea594ca5bfda0cd7f302d487]

## Impact

Adds public Filter and FormatronFilter exports, per-job stateful constraints, trigger-based activation and end_filter termination. Built-in sampler presets inherit the new mask interface. [source; call_e3178f39980141e297d533bf64b5cc8e, call_44762a07b0994362b3d4709f12b86705, call_b2d4c662eb5c4610817c51b61a81e426, call_3410e5e520d047ef880eeb88a4775098]

## Source Notes

Read the root generation and sampling entries and the conditional-RNG entry. They establish the existing scheduler, composable sampler and explicit-seed path, and record inherited optional-output, sorted-argmax and banned-string issues. [ancestor; call_82848c5c77ac487a8308333aff02316e, call_ac70901862c94ece99badde1f1ce83a2, call_bbe00b1e5e6348b590c45e6e0ed40f69, call_caf27781f0934e31a77ef10e77fe5de5]

The root entry's unassigned optional-output locals are no longer present in the inspected parent: receive_logits initializes all optional outputs and computes requested probabilities. The task leaves that implementation unchanged. Sorted argmax and the two banned-string observations remain as recorded in findings. [source; call_53006eecd9734a7a905bd7225dc4aaf3, call_2e485476e6a343228cfcf303d7336088, call_d250875a48444dd8a7bf954645850401, call_b2d4c662eb5c4610817c51b61a81e426]

Related discussion #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports a 262208-versus-262272 logit-buffer mismatch. Its relationship here is inferred from the shared job.py output-buffer path, not an upstream link to this change; the task does not alter that buffer allocation. [inference; call_3e48e8b36400450d97411241aae3e16b, call_d250875a48444dd8a7bf954645850401, call_b2d4c662eb5c4610817c51b61a81e426]

Other fetched discussions concern distinct problems: #2 absolute setup paths; #6 a ROCm notification and extension-build assertion; #7 an undefined C++ symbol; #12 unsupported stop conditions resolved by selecting ChatML; #16 tokenizer truncation behind a CUDA error; #17 missing Torch during installation; #21 an unresolved Windows build failure; PR #13 missing BOS metadata; and #49 running QTIP inference code. Any relationship to this task is only inferred from shared initialization, tokenizer or dependency files, not evidence that Formatron support fixes those reports. [inference; call_bcff94784f7c42aeab15313e09e88200, call_7a820b99c680440bb0864321a16a7784, call_3997e546510946fda6035b4ee790138f, call_24a1deae234d496a8484d42076256667, call_e856d6b0d0d94b289e079292a6de2406, call_58538c0590d045c2b6f8940403527f6f, call_b14053671c4b45bd98c9896961a796e6, call_228948cbcf0a42f698e9682e050ecccf, call_83185bb58b4946988f25bef28e8c975c, call_897c1642fc2843a186e5c19cbffb266a]

<a id="generation"></a>

## Stateful Formatron constraints through additive logit masks

Filter stores tokenizer, trigger token, optional prefix and completion policy. attach supplies the owning job, generator and padded vocabulary width. Job.activate attaches and resets each filter, enabling only those without triggers. receive_sample activates a matching inactive filter without feeding it the triggering token; active filters consume subsequent tokens, deactivate on completion and optionally end generation. [source; call_05be3d4ce18e46868712d5905022aaf2, call_b2d4c662eb5c4610817c51b61a81e426]

Generator.generate normalizes one prompt's filters into one list entry and requires one filter list or None per batched prompt. Direct Job construction accepts the same per-job list. AsyncJob already forwards keyword arguments to Job, so it needs no separate filter adapter. The example reuses filters sequentially but constructs separate instances for simultaneous jobs because filters carry mutable state. [source; call_ffef006ce8514b9e9f59ba416b3c8555, call_b2d4c662eb5c4610817c51b61a81e426, call_f81759d90e9e4d21ae3e0d77e86953b8, call_4835eb1408a141618fcdcd8a6af6b4ed]

FormatronFilter builds a formatter from a KBNF vocabulary and a token-decoding callback. Tokenizer.get_vocab_dict supplies raw token-string-to-ID mappings; get_original_characters converts those for KBNF tokens while the inverse mapping retains token spellings. Vocabulary construction caches ten argument combinations, an implementation capacity rather than a grammar threshold. [source; call_1fc2eaa85b704da686d6cbe655c9564c, call_64c3734f40244afaaf4a1f81f044baeb]

The adapter computes allowed tokens and asks Formatron to mask a CPU half-precision zero vector, then adds a leading dimension. It discards the reusable zero buffer when returned storage aliases it. Despite Filter's boolean-mask docstring, this implementation and Job's consumer use additive numeric masks, not boolean selection. [source; call_1fc2eaa85b704da686d6cbe655c9564c, call_05be3d4ce18e46868712d5905022aaf2, call_b2d4c662eb5c4610817c51b61a81e426]

iterate_gen submits active background filters before model.forward, computes foreground filters afterward and joins their results in prepare_logit_mask. The first mask is copied into a lazily allocated pinned (1, padded_vocab_size) half buffer; further masks are added. Stop IDs below min_new_tokens and explored banned-string retry IDs receive negative infinity. Token healing postpones grammar masks and applies a prefix allowlist instead. A nonblocking transfer prepares the device mask before sampling. [source; call_ffef006ce8514b9e9f59ba416b3c8555, call_b2d4c662eb5c4610817c51b61a81e426]

For masks containing zero for allowed IDs and negative infinity elsewhere, addition implements intersection. A bounded standard-library check verified all 256 pairs of subsets of a four-token vocabulary. This does not test tensor broadcasting, half precision or GPU transfer ordering. [execution; call_be3bcefbd4254d719f88cf81b3f26808]

CustomSampler replaces blocked_tokens and allowed_tokens with logit_mask and adds it before its sampling steps. The old code cloned logits and assigned exclusions directly; the new path supports finite biases as well as exclusions. Sampler.forward itself remains on the old signature, so external implementations following that base declaration must adopt logit_mask: Job now supplies it even when its value is None. [source; call_369c3ad9ea594ca5bfda0cd7f302d487, call_17f8b55bcb374847abc86ac766a51991, call_f5f0396359d5456a85b03096b2bdcb23, call_b2d4c662eb5c4610817c51b61a81e426]

Whole-parent searches found the old restriction arguments only in Job, CustomSampler and the base Sampler declaration. All six built-in preset classes inherit CustomSampler.forward. The generation_loop example, gumbel_eval utility and sampler tests omit the replaced arguments; their inspected calls remain compatible, including tests using named return_state and sequence_ids. [source; call_c28a36f8d5dd4a8baf3d2eef0c2e5250, call_ebdb73b6488040c8880bb0cd61655c45, call_6847e030ec484d09a7521db58bd056ff, call_f0f652dc57cc48e5b1a6c8c13b98af3f, call_3410e5e520d047ef880eeb88a4775098, call_8a8d8c787d994e0298e96f0f1bb91e8f, call_db67367ac31a4a739a1d798fb88814ba, call_7cd302036faf4d58aab798237cdb4596]

The filter edits depend on each other: activation supplies vocabulary width before mask allocation, mask preparation supplies receive_logits' new argument, and CustomSampler consumes that argument. The new assertion rejecting filters combined with banned strings avoids rewinding a grammar engine without restoring its state. [inference; call_05be3d4ce18e46868712d5905022aaf2, call_b2d4c662eb5c4610817c51b61a81e426, call_369c3ad9ea594ca5bfda0cd7f302d487, call_d250875a48444dd8a7bf954645850401]

Requirements and setup add kbnf>=0.4.2 and formatron>=0.5.0; example requirements add pydantic. Parent-tree searches found no literal imports of these module names. The new adapter imports formatron and kbnf, and the example imports pydantic. Re-exporting the adapter through package initializers makes these runtime imports eager rather than confined to constrained-generation use. [source; call_1d3b6759bbf545afa57f54c2f23fc9b5, call_c0b4b04df7714d0fb8893b95f167e696, call_897c1642fc2843a186e5c19cbffb266a, call_b2b18a7201174cb4b714924f2e180fea, call_54069b4d0a94449bae1c8ce523b32e35, call_6a071a1d00a447998a1f5bc95178f8b0, call_1fc2eaa85b704da686d6cbe655c9564c, call_180d4e9f638a44c2acb1a2352e954684, call_44762a07b0994362b3d4709f12b86705, call_e3178f39980141e297d533bf64b5cc8e]

The example demonstrates JSON schema constraints, an additional leading-brace constraint, a Llama3.1-specific trigger ID 79579 and arithmetic grammar extraction. Its 400-token generation budget and maximum five superpowers are example choices, not engine limits. end_filter is checked after stop-token and token-budget termination, so those earlier reasons take precedence. [source; call_4835eb1408a141618fcdcd8a6af6b4ed, call_b2d4c662eb5c4610817c51b61a81e426, call_d250875a48444dd8a7bf954645850401]

## Authoring-time findings — pending review

### speculative-mask-not-refreshed (suspected; defect)

Speculative verification reuses a mask after the filter state advances.

Trigger: A filtered job accepts a draft token and proceeds to another sample in the same main-model logit batch.

Expected: Prepare constraints for the newly advanced grammar state before sampling the next position.

Actual: prepare_logit_mask runs once before the inner sampling loop. receive_sample advances filters, but subsequent receive_logits calls use the same device_logit_mask. A token legal only in the preceding state can therefore remain selectable.

Locations: 08dde73e664b997091370894072065f1f15055bf:exllamav3/generator/generator.py — Generator.iterate_gen, 08dde73e664b997091370894072065f1f15055bf:exllamav3/generator/job.py — Job.receive_sample

Source evidence: call_5b5c5de06b514c06a36e9541f9d5441a, call_ffef006ce8514b9e9f59ba416b3c8555, call_b2d4c662eb5c4610817c51b61a81e426, call_8388ee8f166f4c53aa16233b49059cab

scalar_transcription: A two-state model with allowed sets {0} then {1} demonstrated that a frozen first mask permits a second 0 despite the advanced grammar. [call_be3bcefbd4254d719f88cf81b3f26808]. Limits: Not a Formatron or speculative-decoding execution. The direct receive_sample caller found is iterate_gen; ordinary one-sample iterations do not exercise this stale-within-batch case.

### prefix-not-replayed (suspected; defect)

Prefix acceptance is performed during construction but not replayed during activation or triggered reset.

Trigger: Construct FormatronFilter with read_prompt enabled and a nonempty prefix_str, then start its Job.

Expected: The prefix should remain accepted before generation, as the Filter parameter contract describes.

Actual: The constructor calls accept_bytes, but Job.activate immediately calls reset. FormatronFilter.reset only delegates to the formatter and does not reaccept prefix_str. If formatter reset clears accepted input, the initial prefix is lost. With prefix_str=None, the enabled constructor branch instead attempts None.encode.

Locations: 08dde73e664b997091370894072065f1f15055bf:exllamav3/generator/filter/formatron.py — FormatronFilter.reset, 08dde73e664b997091370894072065f1f15055bf:exllamav3/generator/job.py — Job.activate

Source evidence: call_1fc2eaa85b704da686d6cbe655c9564c, call_05be3d4ce18e46868712d5905022aaf2, call_b2d4c662eb5c4610817c51b61a81e426, call_ffef006ce8514b9e9f59ba416b3c8555

source_inspection: Compared constructor acceptance with both new reset callers: job activation and trigger activation. No parent Formatron callers existed in the literal search. [call_b2b18a7201174cb4b714924f2e180fea, call_b2d4c662eb5c4610817c51b61a81e426]. Limits: Actual formatter reset semantics and EngineGenerationConfig defaults were not inspected; prefix-loss conclusion is conditional on reset clearing accepted input.

### vocabulary-cache-list-argument (suspected; defect)

The advertised list-valued vocab_processors argument cannot pass through the vocabulary cache.

Trigger: Pass any list, including [], as FormatronFilter.vocab_processors.

Expected: Forward the processors to get_original_characters and construct the vocabulary.

Actual: create_engine_vocabulary is decorated with lru_cache and receives the list unchanged, causing an unhashable-list TypeError before its body executes.

Locations: 08dde73e664b997091370894072065f1f15055bf:exllamav3/generator/filter/formatron.py — create_engine_vocabulary

Source evidence: call_1fc2eaa85b704da686d6cbe655c9564c, call_b2b18a7201174cb4b714924f2e180fea

scalar_transcription: Called a standard-library lru_cache(10) wrapper with the inspected argument structure and []; it raised TypeError: unhashable type: 'list'. [call_be3bcefbd4254d719f88cf81b3f26808]. Limits: The new constructor is the visible direct caller. The supplied examples use the default None and do not exercise this case; no repository adapter was executed.

### inherited-sorted-argmax (suspected; defect)

The inherited sorted-argmax assignment defect persists through the sampler interface change.

Trigger: A custom sampling chain reaches SS_Argmax with sorted logits or probabilities.

Expected: Store the selected original token ID in state.sample.

Actual: Sorted branches assign to state.state, then overwrite it with DONE. If indexing succeeds, CustomSampler.forward subsequently tries to reshape the still-None sample.

Locations: 08dde73e664b997091370894072065f1f15055bf:exllamav3/generator/sampler/custom.py — SS_Argmax.run

Source evidence: call_2e485476e6a343228cfcf303d7336088, call_17f8b55bcb374847abc86ac766a51991, call_369c3ad9ea594ca5bfda0cd7f302d487, call_7be8ba4b28a54ebd924110cbe3b2a503, call_3410e5e520d047ef880eeb88a4775098

source_inspection: Compared the parent branches and forward return with the task diff. Whole-parent SS_Argmax search and preset inspection show built-in greedy paths do not sort before argmax. [call_7be8ba4b28a54ebd924110cbe3b2a503, call_3410e5e520d047ef880eeb88a4775098]. Limits: Limited to custom sorted-argmax composition; no tensor execution.

### inherited-banned-token-buffer (suspected; defect)

Moving retry exclusions into prepare_logit_mask does not repair banned-string token-buffer restoration.

Trigger: A banned-string match reaches rewind_checkpoint before terminal handling.

Expected: Restore held_tokens to the saved checkpoint and exclude rejected IDs from emitted output.

Actual: rewind_checkpoint assigns the saved buffer to held_token, whereas emission reads held_tokens. Rejected token IDs can remain in the emitted buffer despite sequence rewind.

Locations: 08dde73e664b997091370894072065f1f15055bf:exllamav3/generator/job.py — Job.receive_sample.rewind_checkpoint

Source evidence: call_d250875a48444dd8a7bf954645850401, call_b2d4c662eb5c4610817c51b61a81e426, call_8388ee8f166f4c53aa16233b49059cab

source_inspection: Compared the unchanged checkpoint assignment and emission reader with the task's relocated explored-token masking. [call_d250875a48444dd8a7bf954645850401, call_b2d4c662eb5c4610817c51b61a81e426]. Limits: Applies to banned-string jobs without filters; the new assertion rejects combining the two features. No matcher or buffer execution.

### inherited-terminal-banned-bypass (suspected; defect)

The token-budget branch still bypasses banned-string suppression.

Trigger: Without drafting, a non-stop token completes a banned string at max_new_tokens, for example a token decoding to 'bad' with banned_strings=['bad'] and max_new_tokens=1.

Expected: Check and suppress the banned text before terminal flushing.

Actual: receive_sample returns through the token-budget branch with emit_held=True before reaching banned-string matching. The task inserts filter completion after that branch but does not change this ordering.

Locations: 08dde73e664b997091370894072065f1f15055bf:exllamav3/generator/job.py — Job.receive_sample

Source evidence: call_d250875a48444dd8a7bf954645850401, call_b2d4c662eb5c4610817c51b61a81e426, call_8388ee8f166f4c53aa16233b49059cab

source_inspection: Inspected terminal branch ordering and the direct iterate_gen call path. [call_d250875a48444dd8a7bf954645850401, call_5b5c5de06b514c06a36e9541f9d5441a]. Limits: Conditional on the stated token decoding; no tokenizer or native matching execution.

## Uncertainty and limits

No repository implementation, model generation, PyTorch operation, CUDA kernel or Formatron engine was executed. The standard-library checks model mask arithmetic, caching and state transitions only.

Formatron and KBNF implementation bodies were not supplied or inspected; their version-specific reset, completion and mask behavior remains externally unverified.

Whole-tree literal searches establish the inspected repository call sites, not external custom samplers, dynamically assembled calls or downstream integrations.

No latency, memory-usage or grammar-compliance measurements establish the practical benefit of background filtering.
