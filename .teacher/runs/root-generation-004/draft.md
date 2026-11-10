# 543c4b27714c6a677a6e714c452d62532f634cff


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/543c4b27714c6a677a6e714c452d62532f634cff) · [Evidence ledger](draft.json)

- [Dynamic generation, paged KV ownership and streaming contracts](#generation)

## Problem

This root change introduces a generation layer that coordinates queued requests, bounded KV-cache capacity, prompt ingestion, sampling and streamed completion events. [source; call_d9672fa51a404f818950034df076227f, call_2721ad5dc7b74911b25c06844d765f3e]

## Reasoning

The central separation is between jobs owning logical sequences, a page table managing reusable physical cache slots, and model calls receiving explicit block tables and cache lengths. Reserving output capacity before starting a job simplifies subsequent decoding, but reduces concurrency when requested output budgets substantially exceed actual completions. [inference; call_2407345feaf749438898ed7cbaad37b9, call_98b25069b15546378633bd3a9addb24a, call_2721ad5dc7b74911b25c06844d765f3e]

## Impact

The implementation supports dynamic admission, prefix-cache reuse, streaming and an asyncio wrapper. Optional probability/top-token reporting, banned-string restoration and multi-sequence handling have concrete suspected failure paths recorded in findings. [source; call_b0a7466e39c2408baccea85cf352c66a, call_5f647097e9fa4eb894e215f9065d472a, call_98b25069b15546378633bd3a9addb24a, call_d9672fa51a404f818950034df076227f]

## Source Notes

The public exports expose Generator, Job, AsyncGenerator and AsyncJob, alongside Cache, CacheLayer and CacheLayer_fp16. [source; call_827afa45aa7c4b7d8be1e865b7e00122, call_e6534554abee49d9b92824d5506beec8]

Bounded standard-library checks exercised transcribed optional-return branches, capacity arithmetic, checkpoint attribute assignment, prefill rounding and terminal branch ordering. A separate asyncio model checked cancellation of a consumer already waiting on an empty queue. These were not executions of repository classes. [execution; call_e36f63c9a36045e9a223f564c73c3bf6, call_a4d625ee919d4f82aebf6fd49ffc7737]

<a id="generation"></a>

## Dynamic generation, paged KV ownership and streaming contracts

Job accepts one CPU token tensor of shape (1, n), or a list of such sequences sampled collectively. It keeps original prompt IDs separately from mutable sequence IDs, per-job RNG state, output buffers and stop conditions. Token healing removes the final prompt token when every sequence has more than one token, restricts the first sample by its prefix and excludes the healed prefix from emitted text. max_new_tokens defaults through `max_new_tokens or 100`; stop tokens are populated only from supplied stop_conditions. [source; call_e0b7a9d48e8b4a2d8af4f2563372f0e3, call_5f647097e9fa4eb894e215f9065d472a]

enqueue prepares page requirements, assigns a serial and appends to pending_jobs. iterate first admits jobs, then performs one prefill round for each active job, then decodes ready jobs. Admission counts sequences rather than jobs against max_batch_size, and compares current page demand with unreferenced slots. Smaller jobs may bypass a non-fitting job, but its skip count increases for each admitted bypass; the default maximum of four eventually stops further bypasses. This fairness policy assumes each queued job can eventually fit, an assumption violated by the multi-sequence enqueue calculation in finding generation-capacity. [source; call_d9672fa51a404f818950034df076227f, call_2721ad5dc7b74911b25c06844d765f3e, call_98b25069b15546378633bd3a9addb24a]

Cache creates one layer object per hidden layer and registers these objects with model modules advertising kv_cache capability. The default FP16 layer requires capacity divisible by PAGE_SIZE=256 and allocates separate zero-initialized K and V tensors shaped (capacity/256, 256, num_kv_heads, head_dim). free drops both tensors; detach_from_model removes registration. Partial-page copying copies only the requested token prefix in every layer. The generation path uses same-cache copies, so it does not depend on the cross-cache interpretation of Cache.copy_page's target argument. [source; call_f2e94d17685c459e8942c7d0b9171aca, call_5b2fb7d813604dcc901188dc2316dfd4, call_166a40db4d66423d85716e2ddf799269, call_98b25069b15546378633bd3a9addb24a]

Sequence.prepare hashes only complete context pages preceding the final input token: context_pages=(length-1)//256. It reserves ceil((length+max_new_tokens+healing_adjustment)/256) total pages, with the remainder private to that sequence. Context keys are 16-byte BLAKE2b digests incorporating the preceding page's digest, so identical local tokens under different prefixes are not intentionally shared. Mutable pages receive monotonically generated 16-byte placeholder keys, despite the random_hash name. [source; call_2407345feaf749438898ed7cbaad37b9, call_166a40db4d66423d85716e2ddf799269]

PageTable first shares a matching referenced context page, otherwise reclaims a matching unreferenced page, otherwise replaces the oldest unreferenced slot by access_serial. Reference counts move pages between referenced and unreferenced dictionaries. Reserving a private page backs up its old metadata; releasing an untouched reservation can restore that metadata because no KV data was overwritten. Actual writes disable restoration. Finished or cancelled active jobs release references without necessarily erasing cached contents. defrag is a no-op. [source; call_2407345feaf749438898ed7cbaad37b9, call_98b25069b15546378633bd3a9addb24a, call_2721ad5dc7b74911b25c06844d765f3e]

Prefill leaves the last prompt token unevaluated for the first decode step. Its endpoint rounds kv_position+max_chunk_size down to a page boundary, then caps at sequence length minus one. The default 2048-token chunk spans eight pages; smaller chunks trade prompt throughput for shorter interruptions, but a positive chunk below 256 can make no progress. Existing complete pages advance the starting position. At a page boundary, prefill also searches pages with the same previous hash for a matching token prefix; a match longer than one token is copied in both main and draft caches when drafting is enabled. [source; call_d9672fa51a404f818950034df076227f, call_98b25069b15546378633bd3a9addb24a, call_71675f5f32384b999bc3e24fb0965675]

Ready sequences satisfy kv_position == len(sequence_ids)-1. iterate_gen flattens them into a batch, builds an int32 physical block table and per-sequence cache lengths, and calls model.forward with attn_mode='flash_attn' and the cache. A logit mapping restores job boundaries afterward. get_input_ids_list records evaluated input IDs into private page metadata; receive_sample appends the sampled token and advances logical KV position. Completed pages gain chained hashes and can switch to an already referenced identical page, rebuilding the sequence's block table. [source; call_d9672fa51a404f818950034df076227f, call_2721ad5dc7b74911b25c06844d765f3e, call_e0b7a9d48e8b4a2d8af4f2563372f0e3, call_5f647097e9fa4eb894e215f9065d472a]

Draft decoding requires an equal-capacity draft cache. The draft model greedily generates num_draft_tokens, default four, then performs one extra prefill; the main model evaluates the current token plus proposals. Main-model samples are accepted until a proposal differs, after which remaining speculative page positions are rolled back and rejection counts increase. max_q_size defaults to eight and is used here to validate the requested draft count, not as a stored general generation limit. The draft batch construction counts jobs but writes one row per sequence, unlike ordinary decoding; finding generation-draft-rows records that mismatch. [source; call_d9672fa51a404f818950034df076227f, call_2721ad5dc7b74911b25c06844d765f3e]

The optional output contract is wired through several layers but is incomplete at sampling. Job stores return_probs and return_top_tokens; receive_logits passes logits, the first sequence's history, a 32-bit RNG value, tokenizer and token constraints to sampler.forward. CustomSampler returns only a token tensor, not probabilities or top-token arrays. receive_logits nevertheless promises the four-item tuple consumed by iterate_gen: token, top tokens, top probabilities and chosen probability. Its enabled optional branches are TODO/pass and leave local variables unbound. [source; call_e0b7a9d48e8b4a2d8af4f2563372f0e3, call_5f647097e9fa4eb894e215f9065d472a, call_2721ad5dc7b74911b25c06844d765f3e, call_a03cde1d538c4c7899988772344b6d5c, call_cd9a8b253a4d41c3b244972d91fbdaf0]

Downstream buffers are already present: token IDs and chosen probabilities use (1,n), top-token IDs/probabilities use (1,n,k), and logits use (1,n,padded_vocab_size), with vocabulary width rounded up to a multiple of 32. receive_sample conditionally appends optional values; emit clones nonempty buffers into token_ids, token_probs, top_k_tokens, top_k_probs and logits, then clears their logical lengths. Unemitted terminal content is placed under held. Consequently enabling the missing sampling branches fails before these otherwise prepared output fields can be populated. return_logits separately records only the first logit row after the sampler call. [source; call_d9672fa51a404f818950034df076227f, call_5f647097e9fa4eb894e215f9065d472a, call_98b25069b15546378633bd3a9addb24a, call_b5a476dcfb0f457fb11266ea0f736158]

Streaming can emit metadata-only events while text is held. A stop token terminates without flushing held output. The token-budget test follows and flushes at new_tokens >= max_new_tokens-num_draft_tokens. Incomplete decoded characters are held while the replacement-character count is between one and four; a tokenizer re-decode may resolve them. Stop-string matching uses UTF-32 buffers: -2 means a possible trailing prefix, -1 no match, and a nonnegative result locates a full match. A full stop string truncates emitted text before the match, but token buffers remain token-granular rather than being split at that character boundary. [source; call_5f647097e9fa4eb894e215f9065d472a, call_98b25069b15546378633bd3a9addb24a, call_71675f5f32384b999bc3e24fb0965675]

Banned strings are lowercased before matching. A possible prefix creates a checkpoint of held output before the current token, plus an offset and explored first-token IDs. A full match rewinds generated-token counts, sequence IDs and page validity, resets the checkpoint offset to zero and blocks explored first tokens on retry. This is logical invalidation, not restoration of saved KV tensors or RNG state. The held-token restoration uses the singular held_token attribute rather than held_tokens, allowing rejected IDs to escape in the emission; additionally the earlier token-budget branch can bypass banned-string checking entirely. [source; call_e0b7a9d48e8b4a2d8af4f2563372f0e3, call_5f647097e9fa4eb894e215f9065d472a, call_98b25069b15546378633bd3a9addb24a]

AsyncGenerator is a cooperative wrapper, not a separate inference worker: its background task calls synchronous Generator.iterate, routes events into per-job asyncio queues, removes jobs on eos and yields with sleep(0). Exceptions are delivered to all currently registered jobs and end that iteration task. AsyncJob's iterator yields queued results until eos or a cancellation check. cancel releases/removes the underlying job, but does not wake an iterator already blocked in queue.get; close cancels the iteration task without explicitly clearing underlying generator jobs. [source; call_b0a7466e39c2408baccea85cf352c66a, call_d9672fa51a404f818950034df076227f]

The blocking generate helper tokenizes prompts, creates jobs, orders streamed text by serial and optionally returns terminal result dictionaries. Its abort event is checked after iterate returns, where it clears the queue, rather than being forwarded into the inspected prefill calls. Terminal streaming results include completion text, token counts, timing and cache-reuse counters; speculative counts are included when drafting. These counters describe recorded activity, not independently measured performance evidence. [source; call_2721ad5dc7b74911b25c06844d765f3e, call_5f647097e9fa4eb894e215f9065d472a, call_98b25069b15546378633bd3a9addb24a]

The bounded transcription produced unbound-local errors for each enabled optional-output flag. It also showed a two-sequence request counted as one page at enqueue but two at admission, stale rejected token IDs after checkpoint restoration, and a zero prefill endpoint for chunk size 255. The asyncio model remained pending after its cancellation flag changed because no queue item woke the blocked consumer. [execution; call_e36f63c9a36045e9a223f564c73c3bf6, call_a4d625ee919d4f82aebf6fd49ffc7737]

Related chapters: modules (assembly link pending), sampling (assembly link pending), loading-tokenization (assembly link pending), runtime (assembly link pending), usage-evaluation (assembly link pending)

## Authoring-time findings — pending review

### generation-optional-probability-outputs (suspected; defect)

Requested chosen-token probabilities and top-token outputs do not reach their prepared streaming buffers.

Trigger: A job reaches receive_logits with return_probs=True or return_top_tokens greater than zero.

Expected: Return the requested final sampling probabilities and top-token arrays alongside the sampled token, allowing receive_sample to buffer and emit them.

Actual: The enabled branches execute only pass. return_probs=True leaves next_prob unassigned; return_top_tokens>0 leaves next_k_tokens and next_k_probs unassigned. The return tuple therefore raises UnboundLocalError. CustomSampler.forward supplies only token IDs and receives no request for these additional outputs.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.receive_logits, 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/sampler/custom.py — CustomSampler.forward

Source evidence: call_5f647097e9fa4eb894e215f9065d472a, call_a03cde1d538c4c7899988772344b6d5c, call_98b25069b15546378633bd3a9addb24a

source_inspection: Traced flags through sampling, tuple unpacking, held buffers and emitted field names. [call_2721ad5dc7b74911b25c06844d765f3e, call_5f647097e9fa4eb894e215f9065d472a]. Limits: No model or sampler execution.

scalar_transcription: Executed the same conditional assignments with a scalar token: disabled flags returned four values; each enabled option raised the corresponding unbound-local error. [call_e36f63c9a36045e9a223f564c73c3bf6]. Limits: Checks Python control flow, not distribution computation or tensor shapes.

### generation-banned-checkpoint-tokens (suspected; defect)

Banned-string rewind restores the wrong token-buffer attribute.

Trigger: A full banned-string match reaches rewind_checkpoint before a terminal branch, including a one-token match such as 'bad' with a larger output budget.

Expected: Restore held_tokens to the checkpoint and report rejected IDs only as suppressed_tokens, keeping emitted tokens consistent with rewound sequence state.

Actual: rewind_checkpoint assigns checkpoint['held_tokens'] to self.held_token. The actual self.held_tokens buffer retains rejected IDs; emit_held subsequently emits and clears that stale buffer while also reporting the IDs as suppressed.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.receive_sample.rewind_checkpoint

Source evidence: call_98b25069b15546378633bd3a9addb24a, call_5f647097e9fa4eb894e215f9065d472a

scalar_transcription: Modeled the inspected attribute assignments with a rejected ID 7 and an empty saved buffer. The sequence rewound, but both emitted_token_ids and suppressed_tokens remained [7]. [call_e36f63c9a36045e9a223f564c73c3bf6]. Limits: List/attribute model; SeqTensor copying and KV invalidation were inspected, not executed.

### generation-capacity (suspected; defect)

Enqueue validation omits private pages from all but the last sequence.

Trigger: A multi-sequence job's total private-page requirement exceeds cache capacity, while its shared context hashes plus the last sequence's private pages fit. For example, two one-token sequences requesting 100 output tokens each with a one-page cache.

Expected: Reject the impossible request during preparation using the union of context hashes plus every sequence's private-page count.

Actual: prepare_for_queue accumulates all_unique_pages but calculates total_pages using only seq.new_unique_pages from the last loop iteration. Admission later sums every sequence correctly, so the example is enqueued with a reported requirement of one page but permanently needs two; repeated iteration cannot start it.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.prepare_for_queue, 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.current_new_pages_required

Source evidence: call_98b25069b15546378633bd3a9addb24a, call_2407345feaf749438898ed7cbaad37b9, call_2721ad5dc7b74911b25c06844d765f3e

scalar_transcription: Computed the inspected page formulas for the two-sequence example: private pages [1,1], enqueue total 1, admission requirement 2, capacity 1. [call_e36f63c9a36045e9a223f564c73c3bf6]. Limits: Exact small-integer arithmetic, not execution of the scheduler.

### generation-draft-rows (suspected; defect)

Draft decoding sizes its batch by jobs while populating it by sequences.

Trigger: Draft decoding is enabled and a ready job contains multiple sequences.

Expected: Allocate and index one draft row per sequence, or reject multi-sequence drafting explicitly.

Actual: iterate_draftmodel_gen increments batch_size once per ready job, then increments batch for every sequence when writing block_index and cache_seqlens. One two-sequence job allocates one row but attempts to populate two, before collective sampling can occur.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/generator.py — Generator.iterate_draftmodel_gen

Source evidence: call_d9672fa51a404f818950034df076227f

source_inspection: Compared the job-count sizing loop with the nested sequence-writing loop and ordinary iterate_gen's sequence-count sizing. [call_d9672fa51a404f818950034df076227f]. Limits: The exact first PyTorch exception was not measured.

### generation-small-prefill-chunk (suspected; defect)

Sub-page chunk sizes can stall prompt ingestion.

Trigger: max_chunk_size is between 1 and 255, a sequence has uncached prompt tokens to ingest, and its KV position starts at zero.

Expected: Either validate a page-sized minimum or ingest a positive number of prompt tokens.

Actual: Prefill rounds the endpoint down to zero and continues because prefill_end <= prefill_start. The sequence remains unready and subsequent iterations repeat without progress.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.prefill

Source evidence: call_98b25069b15546378633bd3a9addb24a, call_d9672fa51a404f818950034df076227f

scalar_transcription: For a 300-token prompt at position zero, chunk 255 produced endpoint zero; chunks 256 and 2048 produced endpoints 256 and 299 respectively. [call_e36f63c9a36045e9a223f564c73c3bf6]. Limits: Endpoint arithmetic only; no prefill model call.

### generation-terminal-banned-bypass (suspected; defect)

The output-budget branch can emit a banned string without checking it.

Trigger: A non-stop token completes a banned string exactly when the token-budget condition becomes true; for example, a single token decoding to 'bad', banned_strings=['bad'], max_new_tokens=1 and no draft model.

Expected: Apply banned-string suppression before flushing terminal held output.

Actual: receive_sample returns through the max_new_tokens branch with emit_held=True before reaching banned-string matching, emitting the banned text and token IDs.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.receive_sample

Source evidence: call_5f647097e9fa4eb894e215f9065d472a, call_98b25069b15546378633bd3a9addb24a

scalar_transcription: Checked the inspected terminal predicate for the one-token example: 1 >= 1-0 is true, selecting the flush branch before matching. [call_e36f63c9a36045e9a223f564c73c3bf6]. Limits: Branch-order model assumes the stated token decoding; no tokenizer or native matcher execution.

### generation-async-cancel-wakeup (suspected; defect)

Cancelling a job does not wake an already waiting async iterator.

Trigger: An AsyncJob consumer is suspended on queue.get with an empty queue when another coroutine calls AsyncJob.cancel.

Expected: The waiting consumer should terminate or receive a cancellation signal.

Actual: Cancellation removes the underlying job and sets cancelled=True, but provides no queue sentinel and does not cancel the waiting consumer. The flag is checked only before queue.get, leaving the existing wait suspended.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/async_generator.py — AsyncJob.__aiter__, 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/async_generator.py — AsyncJob.cancel

Source evidence: call_b0a7466e39c2408baccea85cf352c66a

scalar_transcription: Ran a minimal asyncio consumer with the inspected flag-check/queue-get ordering. After setting the cancellation flag and yielding, consumer_done_without_queue_signal remained false; the harness then explicitly cancelled it. [call_a4d625ee919d4f82aebf6fd49ffc7737]. Limits: Exercises asyncio queue behavior in a transcription, not AsyncJob or inference.

## Uncertainty and limits

No model generation, CUDA execution, cache-copy test or repository test suite was run. Scalar/list models do not verify tensor operations, device synchronization or numerical sampling behavior.

Cache registration and generator-side model-call parameters were inspected; attention-kernel consumption and model-driven allocation/freeing were not independently traced in this chapter.

Multi-sequence inputs are accepted structurally, but collective CFG sampling is not established by the inspected sampler: CustomSampler returns a sample per input row, while receive_sample expects a scalar token.

The 256-token page size, replacement-character hold threshold and partial-prefix copy threshold are implementation choices; no measured tuning rationale was supplied.
