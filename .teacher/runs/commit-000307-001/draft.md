# 51e9922b5bb7ff036ea6b5bbe0a86c0923d8199a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/51e9922b5bb7ff036ea6b5bbe0a86c0923d8199a) · [Evidence ledger](draft.json)

Defers SeqTensor backing storage and pinned sampling history, and caches UTF-32 string buffers. The source supports reduced eager allocation, not measured memory savings or Windows crash resolution.

- [Allocate generation buffers only when needed](#generation)

## Problem

Queued jobs eagerly reserved optional output storage and sampling-history buffers. The change defers those allocations; its comment specifically reports excessive virtual-memory commitment and possible Windows crashes. [source; call_a62a02905c824e389c6dfe3aad0c7b01, call_dcf0c0f84bb24f3e96cd3cc30284e880, call_87cb9136071b4bde82f8513b707488b5]

## Reasoning

The edits address different lifetimes: SeqTensor delays backing storage until data access, Job delays pinned history until preparation for sampling, and UTF-32 caching reuses encoded stop/banned-string collections. [source; call_a62a02905c824e389c6dfe3aad0c7b01, call_dcf0c0f84bb24f3e96cd3cc30284e880]

## Impact

Unused optional output buffers can remain unallocated, but prompt SeqTensors still allocate immediately through from_tensor. Storage already allocated is retained by clear and truncate. [source; call_aa7e8b4fa6d145f6b5f5552ee6c96296, call_dcf0c0f84bb24f3e96cd3cc30284e880, call_4e0d7df9817d40f7b19b2b8b9c31234c]

## Source Notes

Read the founding runtime and generation entries. They establish the original SeqTensor capacity/view contract and job buffering lifecycle, and record inherited generation defects; they are historical context rather than fresh execution evidence. [ancestor; call_02a0dc8157724366ab09dcf293aff898, call_ac4139d0781647d8ad490bb38a51fa91, call_b7cac618d0474e4fb2601a94e1da4563]

Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports a 262208-versus-262272 mismatch at held_logits.append and SeqTensor.copy_. Its connection to this task is inferred from those exact source operations and the two shared paths, not an upstream linkage. Lazy allocation preserves the configured initial width and does not introduce width reconciliation. [inference; call_5d7b83759dac4e1f81422513a166ef25, call_87cb9136071b4bde82f8513b707488b5, call_aa7e8b4fa6d145f6b5f5552ee6c96296, call_dcf0c0f84bb24f3e96cd3cc30284e880]

Issue #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns chat-template selection; its inferred source connection is the unchanged constructor error immediately before UTF-32 conversion. Issue #39, “Gemma 3 architecture not in list?”, concerns architecture availability and later discusses frontend formatting and GPU budgeting. Neither discussion establishes this change's virtual-memory motivation. [inference; call_59492648b75a44f884ac3587a18cd1d0, call_8ec723926e8c4bcea835c0e88dd4c785, call_550a612cd9a14e6795fc88d4b5fad6b6, call_aed377b140f34020a697261c5948b897]

Whole-parent Windows search also found extension/build handling, a gallery mouse-wheel comment and calibration text; those occurrences do not independently explain the reported allocation crash. [source; call_009ffdf8d620423e8e2a4a93d3c8d4c2]

<a id="generation"></a>

## Allocate generation buffers only when needed

SeqTensor construction now records init_shape, dtype and device while leaving tensor=None. _ensure_init creates the original-capacity tensor, and append, torch and torch_slice call it before accessing storage. This initialization is a necessary companion to removing eager construction, not an independent cleanup. [source; call_dcf0c0f84bb24f3e96cd3cc30284e880, call_aa7e8b4fa6d145f6b5f5552ee6c96296]

Logical length, truth testing and capacity calculation remain independent of allocation. The default capacity is 256 sequence slots; explicit capacities round to the next strictly larger multiple of 256. Appending at an exact boundary still grows with torch.cat. Even append(None), torch() on an empty sequence, or cloning an empty sequence now forces initialization; clear and truncate do not free storage. [source; call_aa7e8b4fa6d145f6b5f5552ee6c96296, call_dcf0c0f84bb24f3e96cd3cc30284e880]

Whole-parent searches located SeqTensor construction only in its own factory methods, Job.prepare_for_queue and Sequence.__init__, with no subclass or external direct backing-tensor reader found. Sequence's prompt buffers use from_tensor and immediately append, so remain eager in practice. Job creates five empty held buffers; conditional appends and truth-guarded emission permit unused probability, top-token and logits buffers to remain lazy. Banned-string checkpointing clones all held buffers, so can allocate otherwise-unused optional storage. [source; call_d5b77e78f0884ae6935149b6c8f87032, call_e633eb8d142a4b3a90f21f3ec3166453, call_4e0d7df9817d40f7b19b2b8b9c31234c, call_87cb9136071b4bde82f8513b707488b5, call_aa7e8b4fa6d145f6b5f5552ee6c96296]

Job now always initializes pinned_ids=None. prepare_sampling_past_ids retains its reqs_past_ids guard, allocates once using the current maximum sequence length plus max_new_tokens plus eight, then exposes and copies the first sequence's current history. The sole direct caller is Generator.iterate_gen: after scheduling model.forward it prepares every active job, including jobs not yet ready when another job enables that generation round. Thus this is later allocation, not strictly allocation only for the job currently sampling. [source; call_a62a02905c824e389c6dfe3aad0c7b01, call_e34c7087338c4fa0b47be2f91eeb4ceb, call_ebd3beffc1ef4f66830eaadddf9657e0, call_b73fd8aa306e44a582e3cebebc882b16]

_strings_to_utf32 gains lru_cache(100) and accepts tuples. Both discovered callers are updated together: stop strings become a tuple from their set, while banned strings become a tuple after lowercasing. Tuple conversion supplies hashable cache keys. The unchanged encoder concatenates UTF-32-LE bytes and byte offsets; the native matcher reads these buffers without modifying them. Identical ordered tuples can share encoded arrays, although stop-set order is not canonicalized and the cache bounds entry count rather than bytes. [source; call_a62a02905c824e389c6dfe3aad0c7b01, call_bf5b18db6aba40a5b6631a78ffa80947, call_aed377b140f34020a697261c5948b897, call_85ea6c084c3b4bce8fc0e3a55bb4af17]

A standard-library transcription encoded ('A', '😀') into eight bytes with offsets (0,4,8), reused the cached result object and bounded retained entries at 100. Capacity arithmetic gave 256,256,512,512 slots for explicit capacities 0,255,256,257. For an illustrative logits width of 262208, the initial 256-slot float32 buffer represents 268500992 payload bytes, or 256.0625 MiB; this is arithmetic, not measured allocation. [execution; call_2c6485c54ad74d59b48700f7436fc288]

Against the founding generation entry, the inspected parent has replaced the old unassigned optional-output branches with initialized results and probability calculations; this task does not change them. The checkpoint token-restoration typo, terminal banned-string bypass and multi-sequence enqueue undercount remain in the inspected parent and are untouched by this diff, as detailed in findings. [source; call_aed377b140f34020a697261c5948b897, call_87cb9136071b4bde82f8513b707488b5, call_a62a02905c824e389c6dfe3aad0c7b01, call_dcf0c0f84bb24f3e96cd3cc30284e880]

## Authoring-time findings — pending review

### inherited-checkpoint-token-restoration (suspected; defect)

Banned-string rewind still restores held_token rather than held_tokens; lazy SeqTensor storage does not repair this inherited mismatch.

Trigger: A full banned-string match reaches rewind_checkpoint before a terminal branch.

Expected: Restore the saved held_tokens buffer and expose rejected IDs only as suppressed tokens.

Actual: The singular attribute receives the saved buffer, while emit_held reads the unchanged plural buffer and can emit rejected IDs. The inspected direct caller is Generator.iterate_gen through receive_sample; reach is limited to its banned-string branch.

Locations: 51e9922b5bb7ff036ea6b5bbe0a86c0923d8199a:exllamav3/generator/job.py — Job.receive_sample.rewind_checkpoint

Source evidence: call_87cb9136071b4bde82f8513b707488b5, call_5713ce55ab7e4441bd49bf800d52690e, call_4746571c28984ce888896ba67905f40d, call_a62a02905c824e389c6dfe3aad0c7b01

source_inspection: Compared checkpoint assignment, emission reader, direct caller and task diff. [call_87cb9136071b4bde82f8513b707488b5, call_4746571c28984ce888896ba67905f40d]. Limits: No tokenizer, matcher or repository generation execution.

### inherited-terminal-banned-bypass (suspected; defect)

The terminal output-budget branch still precedes banned-string matching.

Trigger: A non-stop token completes a banned string when new_tokens reaches max_new_tokens minus num_draft_tokens.

Expected: Check banned-string suppression before terminal output is flushed.

Actual: receive_sample returns with emit_held=True before matching. For example, a first token decoding to 'bad' with banned_strings=['bad'], max_new_tokens=1 and no drafting is flushed. Generator.iterate_gen is the sole discovered direct receive_sample caller.

Locations: 51e9922b5bb7ff036ea6b5bbe0a86c0923d8199a:exllamav3/generator/job.py — Job.receive_sample

Source evidence: call_87cb9136071b4bde82f8513b707488b5, call_5713ce55ab7e4441bd49bf800d52690e, call_4746571c28984ce888896ba67905f40d, call_a62a02905c824e389c6dfe3aad0c7b01

source_inspection: Checked terminal branch ordering against the matcher and caller. [call_87cb9136071b4bde82f8513b707488b5, call_4746571c28984ce888896ba67905f40d]. Limits: The illustrative token decoding was not executed.

### inherited-multisequence-enqueue-capacity (suspected; defect)

Enqueue validation still counts private pages only from the last sequence.

Trigger: A multi-sequence job's aggregate private-page demand exceeds cache capacity while context hashes plus the last sequence's demand fit.

Expected: Reject the impossible job during enqueue using every sequence's private-page requirement.

Actual: prepare_for_queue uses seq.new_unique_pages after the loop rather than the accumulated count. Admission subsequently sums all sequences and cannot start the job. Generator.enqueue is the sole discovered direct caller; the task leaves this validation unchanged.

Locations: 51e9922b5bb7ff036ea6b5bbe0a86c0923d8199a:exllamav3/generator/job.py — Job.prepare_for_queue

Source evidence: call_87cb9136071b4bde82f8513b707488b5, call_7b884b65e86e48eeaeb95cb0fcc5de3f, call_1082115c740b4e37903b8af500490b11, call_4746571c28984ce888896ba67905f40d, call_a62a02905c824e389c6dfe3aad0c7b01

source_inspection: Compared enqueue validation, direct caller and admission calculation with the unchanged task context. [call_87cb9136071b4bde82f8513b707488b5, call_1082115c740b4e37903b8af500490b11, call_4746571c28984ce888896ba67905f40d]. Limits: No scheduler execution.

## Uncertainty and limits

No PyTorch allocation, model generation, native matcher, Windows crash reproduction or memory benchmark was executed. Actual virtual-memory savings and allocator behavior remain unmeasured.

The standard-library check models encoding, cache reuse and capacity arithmetic; it does not execute NumPy conversion, tensor copying or pinned-memory allocation.

The inspected source does not explain the tuning rationale for cache capacity 100, growth quantum 256 or the pinned-history allowance of eight IDs.

Issue #48's reported checkpoint/head-width mismatch was not independently reproduced or traced through model loading.
