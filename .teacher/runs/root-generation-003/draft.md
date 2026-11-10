# 543c4b27714c6a677a6e714c452d62532f634cff


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/543c4b27714c6a677a6e714c452d62532f634cff) · [Evidence ledger](draft.json)

- [Dynamic generation, paged KV ownership and streaming](#generation)

## Problem

The generation component must coordinate requests with different prompt lengths and output budgets over a fixed KV cache, while preserving per-request sampling and streaming state. [inference; call_0e9349feb2f24f3ab46de6c954e338e4, call_c0b25765772c45ff97dece0cd1e21e8c, call_a150891a785743f5af384d25e3d1a08a]

## Reasoning

The implementation separates scheduling in Generator, request state in Job, logical-to-physical cache mapping in PageTable/Sequence, and tensor storage in CacheLayer. This allows completed requests to release ownership without immediately discarding reusable KV contents. [source; call_5bf8bd9c08d3461b8f387ec9bc465690, call_b4190e936a8a416e8c642a65f7825580, call_a150891a785743f5af384d25e3d1a08a, call_71abcef9c0cc40029509f65faf1a3fac]

## Impact

The component exposes synchronous iteration, a convenience generate() method, and asynchronous per-job result streams. It also implements prompt-cache reuse and optional draft-model decoding; these are source-supported capabilities, not measured throughput results. [source; call_689ed356333741a390bffbe75576ecf4, call_8e8de27ede304d75b60b89e5245c9227, call_0e9349feb2f24f3ab46de6c954e338e4, call_5bf8bd9c08d3461b8f387ec9bc465690, call_b4190e936a8a416e8c642a65f7825580]

## Source Notes

Cache defaults to CacheLayer_fp16. Its documentation mentions other cache types, but the inspected cache exports provide Cache, CacheLayer and CacheLayer_fp16; those mentions do not establish quantized-cache support. [source; call_d89dcb9a77cd4dc9807c32df284bd5f7, call_856022042b084789b18a3e49cd7be57c]

<a id="generation"></a>

## Dynamic generation, paged KV ownership and streaming

A Job accepts one CPU token tensor of shape (1, n), or a list of such tensors for separate inference with collective sampling. Each becomes a Sequence with its own token history, KV position and page mapping. enqueue() attaches the job to its generator, prepares capacity requirements, assigns a serial number and puts it in the pending queue. Streaming events retain the job, serial and optional caller identifier. [source; call_c0b25765772c45ff97dece0cd1e21e8c, call_b4190e936a8a416e8c642a65f7825580, call_0e9349feb2f24f3ab46de6c954e338e4]

Each iterate() first admits jobs, then performs one prefill round for every active job, then decodes jobs whose prefill is complete. Admission counts sequences rather than jobs against max_batch_size (default 256), and requires enough unreferenced pages for uncached context plus private output reservations. Smaller fitting jobs may bypass larger ones; default max_skips=4 bounds such bypasses before admission stops behind an older skipped request. This favors utilization initially, then limits starvation by accepting head-of-line blocking. [source; call_0e9349feb2f24f3ab46de6c954e338e4, call_5bf8bd9c08d3461b8f387ec9bc465690, call_c0b25765772c45ff97dece0cd1e21e8c, call_b4190e936a8a416e8c642a65f7825580]

PAGE_SIZE is 256 tokens. For effective prompt length L and output budget N, Sequence.prepare() hashes floor((L−1)/256) context pages and reserves ceil((L+N+h)/256) total pages, where h=1 when healing removed a prompt token. The remaining pages are private reservations. Keeping the final prompt token outside the reusable context is consistent with the decode invariant kv_position == len(sequence_ids)−1: the next forward consumes that last token and obtains its next-token logits. [source; call_6d3aebc425664168a35a204c95576834, call_a150891a785743f5af384d25e3d1a08a, call_c0b25765772c45ff97dece0cd1e21e8c]

A standard-library transcription checked 8,192 combinations of L=1…1024, N in {1,4,100,256} and healing adjustment 0/1. Every case satisfied the ceiling-capacity bounds, retained at least one private page, and left the last prompt token outside the hashed context. This validates those integer identities only, not allocation or inference. [execution; call_341940d4bcc142e8aa1cdd2c473f79f5]

Page identity combines a 16-byte BLAKE2b digest of token bytes with the preceding page's hash. Consequently reuse is prefix-dependent, not merely a match of the current 256 tokens. Unfinished/private pages receive monotonically generated 16-byte identifiers despite the random_hash name. Allocation first reuses matching referenced pages, then matching unreferenced pages, otherwise evicts the unreferenced page with the oldest assignment serial. A newly assigned context hash can exist before its KV is computed, so kv_position—not hash presence alone—controls whether prefill may be skipped. [source; call_a150891a785743f5af384d25e3d1a08a, call_b4190e936a8a416e8c642a65f7825580]

The ownership invariant is that referenced_pages contains pages with positive ref_count, while unreferenced_pages contains reclaimable pages with zero references. add_ref()/sub_ref() move pages between these dictionaries. Private allocation backs up metadata; if a reservation is released before being modified, it can restore the old identity and validity. Writes disable that reversion. Completing a generated page computes its chained content hash and can replace it with an already referenced identical page, rebuilding the sequence's block table. Generation writes assert exclusive ownership of the page being extended. [source; call_a150891a785743f5af384d25e3d1a08a, call_c0b25765772c45ff97dece0cd1e21e8c, call_e7c011c8ff494e6da381e80f46df8ee9]

Reserving the full output budget before admission makes capacity predictable, but ties up pages that an early-ending job may never use. Full pages can be shared directly; partial-prefix reuse instead copies matching K/V into a private destination. Job.prefill() scans pages with the same prev_hash, selects the longest token match, and copies only when the match exceeds one token. This trades a cache scan and copy for avoided prefill computation; the source supplies no measured break-even justification for the greater-than-one threshold. [inference; call_a150891a785743f5af384d25e3d1a08a, call_b4190e936a8a416e8c642a65f7825580]

Cache constructs one storage layer per model layer and registers it with cache-capable modules. Attention.load() allocates those tensors on the module's device, and unload() frees them. FP16 storage consists of separate K and V tensors shaped (max_num_tokens/256, 256, num_kv_heads, head_dim); allocation requires page-aligned capacity. Partial-page copies copy K and V slices across every cache layer. Job completion or cancellation decrements page references rather than freeing these tensors. PageTable.defrag() is currently a no-op. [source; call_856022042b084789b18a3e49cd7be57c, call_71abcef9c0cc40029509f65faf1a3fac, call_2b0839ad8b10476ea4e556a72781afe7, call_a150891a785743f5af384d25e3d1a08a, call_5bf8bd9c08d3461b8f387ec9bc465690]

Prefill uses a default max_chunk_size of 2048, rounds the proposed endpoint down to a page boundary, then caps it at prompt length minus one. It advances over valid full pages, optionally copies a partial prefix, and calls model.prefill() only for the remaining tokens. Smaller chunks are documented as trading prompt ingestion speed for shorter interruptions to ongoing jobs. The budget applies within each sequence's prefill call, not globally across the entire iteration; page rounding also imposes a progress constraint noted in the findings. [source; call_0e9349feb2f24f3ab46de6c954e338e4, call_b4190e936a8a416e8c642a65f7825580]

For decoding, Generator assembles an int32 block_table with one physical-page-index row per ready sequence and an int32 cache_seqlens vector containing its KV position. It concatenates the unprocessed token IDs, calls model.forward(), then uses logit_mapping to route slices back to jobs. Sampling remains per job rather than batched. At the modules interface, Attention.decode_flash_attn() obtains layer K/V tensors and passes them, the block table, sequence lengths and new Q/K/V to flash_attn_with_kvcache; sequence lengths also supply default rotary positions. [source; call_0e9349feb2f24f3ab46de6c954e338e4, call_5bf8bd9c08d3461b8f387ec9bc465690, call_2b0839ad8b10476ea4e556a72781afe7]

Optional speculative decoding requires a draft cache with the same token capacity as the main cache. The default draft length is four; constructor validation compares it with max_q_size, default eight. The draft model greedily proposes tokens, and the main model evaluates the current token plus those proposals. Job sampling advances through the resulting logits while sampled tokens equal the draft. A mismatch records rejected tokens, rolls back page-validity counts for the rejected suffix, and stops consuming that logit batch. The two models use the same logical page mapping, and partial-prefix reuse copies both caches. [source; call_0e9349feb2f24f3ab46de6c954e338e4, call_5bf8bd9c08d3461b8f387ec9bc465690, call_b4190e936a8a416e8c642a65f7825580]

Job.receive_logits() supplies the sampler with logits, the first sequence's token history, a per-job RNG-derived seed, and blocked/allowed token sets. Stop tokens are blocked until min_new_tokens; stop strings remain active. Healing removes the final prompt token, constrains its replacement through tokenizer prefix lookup, and emits only the added suffix. Banned-string handling lowercases text, checkpoints a possible match, and on a full match rewinds sequence/KV state while blocking explored replacement tokens. The checkpoint restoration contains the suspected token-buffer error recorded in the findings. [source; call_c0b25765772c45ff97dece0cd1e21e8c, call_e7c011c8ff494e6da381e80f46df8ee9, call_b4190e936a8a416e8c642a65f7825580]

Output is buffered so partial stop strings and incomplete decoded characters need not be emitted immediately. The character heuristic retries decoding when held text contains one through four replacement characters; no derivation for that cutoff is provided. Native matcher result −2 means the caller continues holding text, while a nonnegative result triggers a match path. A stop token is retained in held data rather than emitted; a stop string truncates emitted text at its match position. The max-token check precedes character, banned-string and stop-string checks and uses max_new_tokens minus num_draft_tokens. EOS events include completion text, counts and timing fields, after which Generator releases the job's pages. [source; call_e7c011c8ff494e6da381e80f46df8ee9, call_b4190e936a8a416e8c642a65f7825580, call_5bf8bd9c08d3461b8f387ec9bc465690]

AsyncGenerator is a cooperative wrapper, not a separate inference worker: its task calls synchronous Generator.iterate(), dispatches results into unbounded per-job asyncio queues, then yields with sleep(0). A condition parks the task when there are no jobs. EOS removes the job from the wrapper's registry; an exception is delivered to every registered job. cancel() removes the underlying job and its page references, while close() cancels and awaits the iteration task but does not clear the underlying generator queue. The blocked-consumer cancellation edge case is recorded separately. [source; call_8e8de27ede304d75b60b89e5245c9227, call_0e9349feb2f24f3ab46de6c954e338e4]

Callers can either drive enqueue()/iterate() for streaming control or use generate(), which tokenizes prompts, creates jobs, collects text by serial number and optionally returns terminal result dictionaries. generate() polls abort_event only after an iteration and clears the queue when it is set. Filter-worker scheduling, multimodal embeddings and filter-driven termination appear as commented TODO paths, not implemented generation guarantees. [source; call_5bf8bd9c08d3461b8f387ec9bc465690, call_e7c011c8ff494e6da381e80f46df8ee9]

Related chapters: modules (assembly link pending), sampling (assembly link pending), loading-tokenization (assembly link pending), runtime (assembly link pending), usage-evaluation (assembly link pending)

## Authoring-time findings — pending review

### generation-prefill-small-chunk (suspected; defect)

A positive max_chunk_size below one page can leave a fresh job permanently unable to prefill.

Trigger: Use max_chunk_size=128 with an uncached 600-token prompt and initial kv_position=0.

Expected: Reject an unusable chunk size or ingest a positive number of prompt tokens.

Actual: The endpoint rounds down to zero; prefill continues without inference or progress, and the job remains ineligible for decoding on subsequent iterations.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.prefill

Source evidence: call_b4190e936a8a416e8c642a65f7825580, call_0e9349feb2f24f3ab46de6c954e338e4

scalar_transcription: Evaluated the inspected endpoint formula for a 600-token prompt. Chunk sizes 128 and 255 produced endpoint zero; 256 produced 256 and 2048 produced 599. [call_341940d4bcc142e8aa1cdd2c473f79f5]. Limits: Integer arithmetic only; no Job or model implementation executed.

### generation-multisequence-capacity (suspected; defect)

Enqueue-time capacity validation omits private pages for all but the last sequence.

Trigger: Enqueue a two-sequence job with 100 prompt tokens and max_new_tokens=100 per sequence into a one-page cache, with max_batch_size at least two.

Expected: Reject the impossible two-page request during preparation.

Actual: prepare_for_queue() accumulates all_unique_pages but calculates total_pages using only the last seq.new_unique_pages. It accepts the one-page estimate; current_new_pages_required() later correctly requests two pages, preventing admission indefinitely.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.prepare_for_queue, 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.current_new_pages_required

Source evidence: call_b4190e936a8a416e8c642a65f7825580, call_a150891a785743f5af384d25e3d1a08a, call_5bf8bd9c08d3461b8f387ec9bc465690

scalar_transcription: Modeled the two inspected capacity formulas: enqueue estimate one page, scheduler requirement two pages, cache capacity one page. [call_341940d4bcc142e8aa1cdd2c473f79f5]. Limits: No actual enqueue or scheduler loop was executed.

### generation-async-cancel-waiter (suspected; defect)

Cancelling an AsyncJob does not wake a consumer already waiting on its empty result queue.

Trigger: A consumer is suspended at await self.queue.get() when another coroutine calls AsyncJob.cancel().

Expected: The cancelled job's asynchronous iterator terminates without needing another result.

Actual: Cancellation removes the job from the generator and sets cancelled=True, but supplies no queue sentinel or waiter cancellation. The flag is checked only before the pending queue.get(), so that consumer can remain suspended.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/async_generator.py — AsyncJob.__aiter__, 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/async_generator.py — AsyncJob.cancel

Source evidence: call_8e8de27ede304d75b60b89e5245c9227

scalar_transcription: Ran a minimal asyncio model of the flag check and empty-queue wait. After setting the cancellation flag and yielding to the loop, the consumer task was still pending. [call_341940d4bcc142e8aa1cdd2c473f79f5]. Limits: This modeled the wait mechanism, not the repository wrapper or inference.

### generation-draft-output-cutoff (suspected; defect)

Enabling draft decoding reduces the terminal output-token threshold by the configured draft length.

Trigger: Generate without healing or other stop conditions using max_new_tokens=100 and num_draft_tokens=4.

Expected: Draft lookahead should not itself terminate the response before the requested 100-token budget.

Actual: receive_sample() terminates when new_tokens reaches 96 because it compares against max_new_tokens−num_draft_tokens. With both values equal to four, the first generated token already satisfies the cutoff.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.receive_sample

Source evidence: call_e7c011c8ff494e6da381e80f46df8ee9, call_5bf8bd9c08d3461b8f387ec9bc465690

scalar_transcription: Computed the first positive counter satisfying the source predicate: 100 for budget/draft 100/0, 96 for 100/4 and one for 4/4. [call_341940d4bcc142e8aa1cdd2c473f79f5]. Limits: Only the stopping predicate was evaluated; no draft acceptance or model execution was tested.

### generation-banned-string-token-rewind (suspected; defect)

Banned-string rewind restores a differently named attribute instead of the token buffer used for emission.

Trigger: A banned-string match reaches rewind_checkpoint() before the max-token termination branch.

Expected: Restore held_tokens to the checkpoint alongside held_text and the other held buffers, keeping rejected tokens out of ordinary token_ids output.

Actual: The code assigns self.held_token, singular. emit() still reads self.held_tokens, plural, which retains the rejected suffix and can emit it as token_ids despite rewinding the sequence and text.

Locations: 543c4b27714c6a677a6e714c452d62532f634cff:exllamav3/generator/job.py — Job.receive_sample.rewind_checkpoint

Source evidence: call_b4190e936a8a416e8c642a65f7825580, call_e7c011c8ff494e6da381e80f46df8ee9

source_inspection: Compared the checkpoint assignment with the held_tokens buffer initialized by prepare_for_queue() and consumed by emit(). [call_b4190e936a8a416e8c642a65f7825580, call_e7c011c8ff494e6da381e80f46df8ee9]. Limits: No banned-string generation or native string matcher was executed.

## Uncertainty and limits

No repository implementation, model inference, CUDA kernel, FlashAttention call or performance benchmark was executed. The successful run checked transcribed integer formulas and a minimal asyncio queue-wait model using the standard library.

The scalar checks cover bounded page arithmetic and selected control-flow triggers, not all page-reference, speculative-decoding or checkpoint interleavings.

Cache sharing relies on chained hashes and consistent cached state. Collision behavior and correctness under concurrent external cache mutation were not experimentally evaluated.

Native string matching and sampler distributions are outside this chapter's inspected implementation scope; their local Job interfaces are explained without claiming native execution.
