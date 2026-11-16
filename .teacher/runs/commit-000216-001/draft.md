# 27c13b11e32af575c9684dd3d2905c55ef6eab9a


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/27c13b11e32af575c9684dd3d2905c55ef6eab9a) · [Evidence ledger](draft.json)

Adds synthetic-ID embedding injection across tokenization, jobs and model lookup, while leaving draft-model prefill insufficiently guarded.

- [Carry indexed vectors from prompt aliases to model inputs](#indexed-embeddings)

## Problem

Generation had commented-out embedding plumbing, while Embedding.forward always performed vocabulary lookup. There was no implemented container connecting externally supplied vectors to prompt token IDs. [source; call_dd39aec609dd47e5806ef670425e7478, call_8a4984164004443dabab21a27a13d669, call_c24d3ca6e45440aa92611ce98a39cd65]

## Reasoning

The edits form one data path: allocate synthetic IDs, substitute them for prompt aliases, preserve the associated vectors on each job, and resolve those IDs during embedding lookup. Tokenizer substitution alone would send out-of-vocabulary IDs into the old lookup, so the generator and embedding changes supply necessary downstream support. [inference; call_dd39aec609dd47e5806ef670425e7478]

## Impact

Exports MMEmbedding and enables externally prepared embeddings through Tokenizer.encode, Generator.generate and Job. This is embedding injection infrastructure, not an image encoder or complete multimodal model implementation; multimodal rotary-position plumbing remains commented out. [source; call_dd39aec609dd47e5806ef670425e7478, call_8212b0243a114343947bf6513b6b059d]

## Source Notes

Read the root entry's modules and loading-tokenization chapters. They establish the original CPU-preferred, float32-default embedding interface, sqrt(hidden_size) scaling, and tokenizer batching/decoding conventions. [ancestor; call_11bcb0bcec384e709141e37b51983673, call_fd23fc2123c24aba810e0fae17aa5fe7]

The inspected discussions concern different problems: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension/toolchain problem; #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” reports installation trouble; #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” concerns chat mode; PR #13, “Fix a tokenizer issue while converting models without a bos_token_id defined,” concerns absent BOS metadata; and #16, “RuntimeError: CUDA error: invalid configuration argument,” attributes conversion failure to tokenizer truncation. [source; call_5791fd67689843b3846c29dc023789aa, call_db5bf3cdca6a489391202174b7cdb7f3, call_bff02a1bba8a4c3d8a10277a3986a2f3, call_7cadeecf7f78445d84b3ab087cfb235c, call_386e4ba66c3d430f8b86f72848d9955c]

The discussion overlap is contextual, not evidence that this commit fixes those reports: #6/#7 traverse the changed package initializer, #12 names Job, and PR #13 names Tokenizer. None establishes motivation for indexed embeddings. [inference; call_dd39aec609dd47e5806ef670425e7478, call_5791fd67689843b3846c29dc023789aa, call_db5bf3cdca6a489391202174b7cdb7f3, call_bff02a1bba8a4c3d8a10277a3986a2f3, call_7cadeecf7f78445d84b3ab087cfb235c]

<a id="indexed-embeddings"></a>

## Carry indexed vectors from prompt aliases to model inputs

MMTokenAllocator assigns consecutive ranges starting at 1,000,000,000. The source explicitly assumes ordinary vocabularies remain below one billion; this is a namespace boundary, not a model dimension or performance threshold. Each MMEmbedding reserves embeddings.shape[-2] IDs and stores the original embedding tensor. [source; call_dd39aec609dd47e5806ef670425e7478]

MMEmbedding replaces -1 positions in the supplied token_string in place with consecutive synthetic IDs. It records the template's last dimension as full_length, the vector count as mm_length, and token_string[0].tolist() as the tokenizer substitution. Consequently, its practical template convention is a single token row, potentially containing ordinary wrapper tokens as well as embedding placeholders. The default alias includes the allocated first index. [source; call_dd39aec609dd47e5806ef670425e7478]

Tokenizer.encode_special_or_unspecial builds an alias-to-container dictionary, escapes aliases into a regex, and replaces matched spans with token_list. Other spans follow the existing special/ordinary encoding branches. Both internal callers, the scalar and list branches of encode, now supply embeddings; whole-parent-tree search found no additional callers of this helper. The public encode argument remains optional. [source; call_dd39aec609dd47e5806ef670425e7478, call_c83783f4f52f41b78d16da259842d68d, call_8a594246456249789596fda335994af8]

Generator.generate accepts one embedding list for a scalar prompt and one list per prompt for a batch. Tuple prompt components share their prompt's embedding list. The same objects go to tokenization and Job, whose new embeddings field defaults to an empty list. Job.prefill forwards that list as params['indexed_embeddings']; iterate_gen combines lists from ready jobs for the batched forward pass. Model.prefill and Model.forward already pass params through to module.forward, so no new model-level argument is necessary. [source; call_dd39aec609dd47e5806ef670425e7478, call_810f08067250409394625f81c2ef6a73, call_96811d09f253427888b5ce4738bd359a]

Embedding.forward separates IDs below the synthetic boundary from IDs inside each supplied container's half-open range. When any supplied range is active, it allocates [batch, sequence, hidden_size], fills ordinary positions from the vocabulary table, then gathers external rows using ID minus first_index. Optional sqrt(hidden_size) scaling happens before external rows are inserted, preserving supplied vectors without that scaling. If no supplied range is active, the existing vocabulary lookup path remains selected. [source; call_dd39aec609dd47e5806ef670425e7478, call_8a4984164004443dabab21a27a13d669]

The representation lets ordinary and external vectors share a sequence without enlarging the vocabulary table. Its caller-side preconditions include compatible vector width and complete range coverage for synthetic IDs. The mixed path allocates uninitialized output and does not validate coverage; it should not be described as validating arbitrary token/container combinations. [inference; call_dd39aec609dd47e5806ef670425e7478]

Decoding remains text-oriented: both decode_ branches filter IDs above the backend vocabulary size rather than reconstructing embedding aliases. The root entry's noted EOS filtering order also remains unchanged: ordinary decoding removes EOS before attempting to truncate at it. This commit does not repair or redefine that inherited decoding behavior. [source; call_8a594246456249789596fda335994af8, call_dd39aec609dd47e5806ef670425e7478]

A standard-library scalar transcription checked adjacent allocations of lengths three and two, placeholder expansion inside ordinary wrapper IDs, repeated alias substitution, and subtraction back to vector rows [0,1,2]. All five allocated IDs belonged to exactly one range. This did not execute masked_scatter_, tensor indexing or model code. [execution; call_a0f59323ec77401984f43e05a3febd83]

Draft-model generation explicitly rejects jobs with embeddings, but that assertion is located in iterate_draftmodel_gen. The earlier Job.prefill draft-model call still receives synthetic input IDs without indexed_embeddings, so rejection does not protect every draft-model entry path. [source; call_dd39aec609dd47e5806ef670425e7478, call_8212b0243a114343947bf6513b6b059d, call_810f08067250409394625f81c2ef6a73]

## Authoring-time findings — pending review

### draft-prefill-before-embedding-guard (suspected; defect)

The explicit rejection of indexed embeddings with a draft model occurs after a reachable draft prefill call.

Trigger: An uncached job uses a draft model and has a synthetic embedding ID in a nonempty prompt-prefill slice.

Expected: Reject the unsupported combination before sending synthetic IDs into the draft model.

Actual: Generator.iterate calls Job.prefill first. Job.prefill calls draft_model.prefill without indexed_embeddings, allowing the draft embedding module to take ordinary vocabulary lookup for IDs starting at one billion. The later assertion in iterate_draftmodel_gen cannot prevent that earlier lookup.

Locations: 27c13b11e32af575c9684dd3d2905c55ef6eab9a:exllamav3/generator/job.py — Job.prefill, 27c13b11e32af575c9684dd3d2905c55ef6eab9a:exllamav3/generator/generator.py — Generator.iterate_draftmodel_gen

Source evidence: call_dd39aec609dd47e5806ef670425e7478, call_d67bcbd993b740398e163f27c947b137, call_8212b0243a114343947bf6513b6b059d, call_810f08067250409394625f81c2ef6a73, call_96811d09f253427888b5ce4738bd359a

source_inspection: Searched generator prefill callers and inspected iteration ordering, both draft prefill sites, model dispatch and the changed embedding fallback. The direct Job.prefill caller is Generator.iterate; the other draft prefill site follows drafting and its new assertion. [call_d67bcbd993b740398e163f27c947b137, call_8212b0243a114343947bf6513b6b059d, call_810f08067250409394625f81c2ef6a73, call_dd39aec609dd47e5806ef670425e7478]. Limits: No model execution or exact backend exception was observed. Fully cached prompts and prompts whose synthetic IDs are outside the prefill slice do not establish this trigger.

## Uncertainty and limits

No PyTorch, tokenizer-backend, model-generation or GPU execution was performed. The scalar check models ID allocation and substitution only.

Device compatibility, placeholder-count errors, malformed embedding shapes and concurrent allocator access were not exercised.

Repository searches establish the internal callers of encode_special_or_unspecial, not compatibility with external callers of that now-required embeddings argument.

End-to-end compatibility with sampling penalties, token healing and every model subclass was not established.
