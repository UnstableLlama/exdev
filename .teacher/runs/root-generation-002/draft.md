# 543c4b27714c6a677a6e714c452d62532f634cff


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/543c4b27714c6a677a6e714c452d62532f634cff) · [Evidence ledger](draft.json)

- [Job scheduling and paged KV-cache generation](#generation)

## Problem

Generation needs to admit requests within finite KV-cache capacity, reuse prompt state, batch ready sequences, and route streamed output and termination back to individual jobs. [inference; call_71804d11c89545328e7d42eb47b39ade, call_2c8ce103b2f745eea6839513036aa16b, call_f5b029d1c53948878d71680f255f88ca]

## Reasoning

The implementation separates physical KV tensors, reference-counted page metadata, per-job sequence/output state, and scheduling. This permits shared immutable prefixes while reserving private capacity for each sequence's unfinished prompt and continuation. [inference; call_b2a6029788af448caefd987efd34a1ab, call_659859b29d9e4312972f989bd1fbb072, call_f5b029d1c53948878d71680f255f88ca, call_88d138b48c264b8d9d5299c021ab431d]

## Impact

The new generation interface provides queued jobs, started/prefill/streaming events, a blocking generate convenience method, and asyncio wrappers. Completed jobs release page references without necessarily discarding reusable KV contents. [source; call_277ff3c3406640d0bbfc97a380a22c1a, call_2c8ce103b2f745eea6839513036aa16b, call_b7a3912def7c42f8a1e762a98fd34444, call_f5b029d1c53948878d71680f255f88ca]

## Source Notes

Several advertised paths are incomplete: return_probs and return_top_tokens enter TODO branches without assigning the values subsequently returned; filter execution is commented out; PageTable.defrag is a no-op. The banned-string rewind assigns self.held_token rather than restoring self.held_tokens. [source; call_df970e3427ee46d2884383545ec60722, call_2c8ce103b2f745eea6839513036aa16b, call_f5b029d1c53948878d71680f255f88ca]

Job.prepare_for_queue accumulates all_unique_pages but uses only the final sequence's new_unique_pages in its capacity assertion. Its failure message also references generator.max_total_tokens, which Generator does not define. Admission later sums every sequence's private pages correctly, so an oversized multi-sequence job can pass the initial check yet remain pending. [inference; call_4c931be0129940e6bd872bcccec6709c, call_71804d11c89545328e7d42eb47b39ade, call_2c8ce103b2f745eea6839513036aa16b, call_63fa9179f03545d2987bca7d89a54407]

<a id="generation"></a>

## Job scheduling and paged KV-cache generation

Cache storage and job ownership have different lifetimes. Cache creates one CacheLayer per hidden layer and registers these with modules advertising kv_cache. Attention.load allocates registered layers on its device; Attention.unload frees them. The provided default, CacheLayer_fp16, stores separate half-precision K and V tensors shaped [capacity/256, 256, num_kv_heads, head_dim]. PAGE_SIZE is explicitly 256, and capacity must be divisible by it. Completing a job changes page references, not these tensor allocations; detach_from_model removes registration rather than explicitly freeing tensors. [source; call_b2a6029788af448caefd987efd34a1ab, call_659859b29d9e4312972f989bd1fbb072, call_4f5377667fa34ba5890d79faeaf25649, call_e1ff4bd246164ebc96c988437a5593c0, call_f5b029d1c53948878d71680f255f88ca]

A Job accepts one CPU token tensor of shape [1,n], or several sequences to evaluate separately and sample collectively. Optional token healing removes each prompt's last token and retains it as a sampling-prefix constraint. Sequence.prepare reserves ceil((n + max_new_tokens + healing_allowance)/256) pages, where n is the working prompt length and healing_allowance is one when healing is active. Only floor((n−1)/256) prompt pages receive reusable content hashes: the last prompt token remains for the first generation forward pass. The remaining pages are private reservations, not allocated incrementally as output grows. [source; call_88d138b48c264b8d9d5299c021ab431d, call_f5b029d1c53948878d71680f255f88ca]

A standard-library check exercised the reservation formulas for 8,192 combinations of prompt length, output allowance, and healing. Each reservation covered the requested length with less than one page of rounding slack and retained at least one private page. With 100 output tokens, prompts of length 256 and 257 both reserve two pages, but their reusable/private splits are respectively 0/2 and 1/1. This verifies the scalar boundary arithmetic, not cache execution. [execution; call_63fa9179f03545d2987bca7d89a54407]

Generator.enqueue prepares a job, assigns a serial, and appends it to pending_jobs. Each iterate first admits jobs, then performs one prefill round per active job, then batches generation-ready sequences. Admission counts sequences against max_batch_size, default 256, and compares additional page demand with unreferenced pages. It may bypass an oversized pending job, but increments that job's skip count when admitting a later one; max_skips defaults to four, after which such bypasses stop. This balances utilization against starvation, with head-of-line blocking once the skip limit is reached. Reserving the maximum continuation up front simplifies capacity accounting but can hold pages that early termination never uses. [inference; call_71804d11c89545328e7d42eb47b39ade, call_2c8ce103b2f745eea6839513036aa16b, call_88d138b48c264b8d9d5299c021ab431d, call_4c931be0129940e6bd872bcccec6709c]

PageTable identifies a reusable prompt page with a 16-byte BLAKE2b digest of its token bytes preceded by the previous page's digest. Thus reuse is conditioned on the preceding context, not merely equal tokens within a page. Temporary identities come from a monotonically increasing 16-byte counter despite the random_hash name. Allocation first shares a matching referenced page, then reclaims a matching unreferenced page, otherwise evicts the oldest unreferenced page by assignment serial. A content hash may be assigned before prefill; kv_position, rather than hash presence alone, determines whether its KV contents are valid. [source; call_f5b029d1c53948878d71680f255f88ca]

The central ownership invariant is that positive-reference pages reside in referenced_pages, while zero-reference pages reside in unreferenced_pages. Mutable generation writes assert ref_count == 1. Reserving a private page backs up its previous metadata; releasing it before any write can restore the old cached identity. Writes disable that restoration. When a generated page becomes full, receive_sample hashes it and either shares an already referenced equivalent page, rebuilding the sequence's block table, or installs the new hash after clearing an unreferenced duplicate. EOS and active-job cancellation decrement references; zero references make a page reusable rather than erasing its KV tensors. [source; call_f5b029d1c53948878d71680f255f88ca, call_88d138b48c264b8d9d5299c021ab431d, call_df970e3427ee46d2884383545ec60722, call_2c8ce103b2f745eea6839513036aa16b, call_71804d11c89545328e7d42eb47b39ade]

Job.prefill advances toward prompt length minus one in chunks, rounding the proposed endpoint down to a page boundary before clamping to the prompt endpoint. The default max_chunk_size is 2,048 tokens, or eight pages. It skips valid full pages and, when starting at a page boundary, searches all pages with the same previous-context hash for a matching token prefix. A best match longer than one token is copied into the destination page across every cache layer, including the draft cache when present. The remaining tokens go through model.prefill. Copying a partial prefix, instead of sharing its mutable page, preserves independent continuation state; the all-pages search adds CPU work. [inference; call_71804d11c89545328e7d42eb47b39ade, call_4c931be0129940e6bd872bcccec6709c, call_b2a6029788af448caefd987efd34a1ab, call_659859b29d9e4312972f989bd1fbb072]

The chunk formula has an important lower-bound hazard. For a fresh 600-token prompt, the scalar check produced endpoints of zero for chunk sizes 128 and 255, 256 for chunk size 256, and 599 for the default 2,048. With no reusable prefix, a sub-page chunk therefore cannot advance this prefill loop; Generator does not validate this constraint. [inference; call_63fa9179f03545d2987bca7d89a54407, call_4c931be0129940e6bd872bcccec6709c, call_71804d11c89545328e7d42eb47b39ade]

A sequence is generation-ready when kv_position equals sequence length minus one. Generator.iterate_gen constructs an int32 block table mapping each sequence's logical pages to physical cache-page indices, alongside per-sequence cache_seqlens. It concatenates the uncached token inputs, records their page metadata, and calls model.forward with attn_mode='flash_attn'. On the attention side, these tensors are moved to the layer device, cache lengths supply default rotary positions, and the layer's K/V tensors plus block table are passed to flash_attn_with_kvcache. Returned logits are mapped back to jobs and sampled individually. Accepting a sample appends one token and advances kv_position by one, maintaining the one-token-behind invariant for ordinary decoding. [source; call_71804d11c89545328e7d42eb47b39ade, call_2c8ce103b2f745eea6839513036aa16b, call_88d138b48c264b8d9d5299c021ab431d, call_df970e3427ee46d2884383545ec60722, call_e1ff4bd246164ebc96c988437a5593c0]

Optional speculative decoding requires an equally sized draft cache. The default draft count is four; initialization checks it against max_q_size, default eight. The draft model greedily proposes tokens and prefills its final proposal. The main model evaluates the uncached token plus proposals together, but each next token is still chosen through Job.receive_logits. Matching proposals allow continued consumption of the logit batch; the first mismatch stops that consumption, counts rejected proposals, and rolls back page-validity positions for the rejected suffix. This is a source-described mechanism, not evidence of a speedup. The termination check uses max_new_tokens minus num_draft_tokens, so a nominal limit of 100 with four draft tokens has a threshold of 96. [source; call_71804d11c89545328e7d42eb47b39ade, call_2c8ce103b2f745eea6839513036aa16b, call_df970e3427ee46d2884383545ec60722]

Sampling and streaming are separate stages. receive_logits passes logits, sequence history, a per-job RNG-derived seed, and allowed/blocked token lists to the sampler. Stop tokens are blocked until min_new_tokens; healing constrains the first replacement token to the original token's prefix. receive_sample buffers decoded pieces and token metadata before deciding what to emit. Actual termination branches are stop_token, max_new_tokens, and stop_string; filter termination remains commented out. No stop token is automatically inserted when stop_conditions is omitted. A missing or zero max_new_tokens becomes 100 because initialization uses 'max_new_tokens or 100'. [source; call_88d138b48c264b8d9d5299c021ab431d, call_df970e3427ee46d2884383545ec60722, call_4c931be0129940e6bd872bcccec6709c]

Text can remain buffered across iterations: a possible stop-string suffix holds output until resolved, and a completed match emits only the preceding text while recording the remainder in the terminal event. Native string matching receives UTF-32 buffers; the caller treats a nonnegative result as a match position and −2 as a partial match. Incomplete-character handling retries decoding when the buffer contains one through four replacement characters, otherwise bypassing that hold. Banned strings use lowercase matching and checkpoints intended to rewind sequence/cache positions and block already explored tokens. Stop-token and length checks precede string checks, so termination ordering matters; the length branch flushes held text before testing stop or banned strings. [source; call_88d138b48c264b8d9d5299c021ab431d, call_df970e3427ee46d2884383545ec60722, call_4c931be0129940e6bd872bcccec6709c]

AsyncGenerator wraps the same synchronous scheduler rather than moving inference into a worker thread. A background asyncio task waits on a condition, calls Generator.iterate, routes events into each AsyncJob's unbounded queue, removes EOS jobs, and yields with sleep(0). Exceptions are forwarded to all registered jobs. AsyncJob's iterator raises queued exceptions and ends after EOS. Consequently, inference work between awaits can occupy the event-loop thread, and slow consumers have no queue backpressure. cancel removes the job and releases active references, but does not enqueue a wake-up sentinel; close cancels the iteration task without clearing the underlying generator queue. [inference; call_b7a3912def7c42f8a1e762a98fd34444, call_71804d11c89545328e7d42eb47b39ade]

The blocking generate alternative tokenizes prompts, creates jobs, accumulates streaming text by serial number, and optionally returns terminal result dictionaries. Its abort_event is checked after an iteration, where it clears the queue and returns None; despite the docstring, this path does not forward the event into the shown prefill calls. Terminal events expose completion text, timing, cache-hit counters, and optional draft acceptance counts, but these are instrumentation fields rather than measurements established by this inspection. [source; call_2c8ce103b2f745eea6839513036aa16b, call_4c931be0129940e6bd872bcccec6709c, call_df970e3427ee46d2884383545ec60722]

Related chapters: modules (assembly link pending), sampling (assembly link pending), loading-tokenization (assembly link pending), usage-evaluation (assembly link pending)

## Uncertainty and limits

The executed checks cover scalar page arithmetic only, not PyTorch tensors, CUDA, FlashAttention, actual cache reuse, scheduling races, or throughput.

Speculative decoding with multi-sequence jobs is not established: drafting sizes its batch by jobs but fills rows by sequences. Numerical or distributional equivalence of speculative output was not tested.

The optional probability/top-token outputs, banned-string rollback, and oversized multi-sequence handling have source-visible defects; their end-to-end behavior was not executed.

Async cancellation and shutdown do not establish complete resource cleanup or wake every blocked consumer. No concurrency stress test was run.

The source supplies no tuning evidence for the default batch, chunk, skip, draft, or Unicode-holding thresholds.
