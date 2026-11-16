# 460e201cc332ff93a4d65d7b1ca1f897ad372685


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/460e201cc332ff93a4d65d7b1ca1f897ad372685) · [Evidence ledger](draft.json)

Adds a cached Wikitext-to-slang batched generation example with indexed completions and console statistics. Inspection identifies empty-dataset failure and prefill-inflated token accounting; inference performance remains unmeasured.

- [Dataset-backed batched translation](#batched-translation)

## Problem

Adds a runnable dataset-to-completion example: translate Wikitext passages into “zoomer slang” using queued, dynamically batched jobs. [source; call_f9f94e719d9c44c190bcbe5019bb0149]

## Reasoning

Integer job identifiers connect asynchronously completed responses to their original passages. Collecting full_completion only on EOS avoids assembling streamed text chunks. [source; call_f9f94e719d9c44c190bcbe5019bb0149, call_6fb44d8c4a09444eab82c2357b7a3726]

## Impact

The change adds one example without modifying generator implementation. It prints inputs, completions and running throughput estimates; it neither scores translation quality nor saves translations. [source; call_f9f94e719d9c44c190bcbe5019bb0149]

## Source Notes

Read the initial usage-evaluation entry, which establishes the existing enqueue/iterate/identifier example pattern, and the long-context entry, which describes Transformers chat-template formatting and records an unsupported default_cache_size keyword at that historical point. [ancestor; call_688ffc51bb8b45cfa83291644db70eff, call_bdc0165242e04d3b9790ab076a90eba6]

That historical keyword incompatibility is not carried into this example: the inspected parent model_init.add_args accepts default_cache_size and forwards it to the cache-size parser default. [source; call_74c7ffb9f9d1495db685e2597467d648, call_f9f94e719d9c44c190bcbe5019bb0149]

The fetched openings of “Superior 3INST parameters” and “Error converting model” concern decoder parameters and conversion-time file opening, respectively. Neither supplies evidence that this translation example addresses those topics. [inference; call_d32984b78a3b47c496868d0036e56e39, call_91bd3e3c610f41489bfd62f96cf1e053, call_f9f94e719d9c44c190bcbe5019bb0149]

<a id="batched-translation"></a>

## Dataset-backed batched translation

get_dataset strips the selected text field and retains passages of at least 125 characters—not tokens. Defaults select wikitext/wikitext-2-raw-v1, test split, text field. The existing disk-cache decorator keys results by serialized arguments and stores them beneath the invoked script's directory; this avoids repeating dataset preparation on cache hits. [source; call_f9f94e719d9c44c190bcbe5019bb0149, call_0c9aaed7a993469b81ea155b48b87df6]

format_request creates one user message with #BEGIN#/#END# delimiters and a /no_think suffix, applies the model directory's HF chat template, and converts IDs to a long tensor with a leading batch dimension. Jobs use model-configured EOS IDs, an integer passage index and a default 1024-token reply limit. The tags are requested output formatting, not parser-enforced boundaries or stop strings. [source; call_f9f94e719d9c44c190bcbe5019bb0149]

The parser requests a 65536-token shared cache, not a batch of 65536 requests. Generator defaults cap concurrent sequences at 256 and prefill chunks at 2048 tokens, with concurrency additionally constrained by available cache. Job preparation asserts that each job's required pages fit; the example adds no prompt truncation or recovery from that assertion. [source; call_f9f94e719d9c44c190bcbe5019bb0149, call_49f508d8cbef4fbdbd57c5b76bc1aa7f, call_74c7ffb9f9d1495db685e2597467d648]

The new call pattern matches existing examples' queue-draining loops. longctx uses the same chat-template-to-tensor preparation but explicitly selects greedy sampling; this example leaves sampler selection to Job's default. Existing consumers variously collect text chunks, inspect EOS, display result packets or discard them. dynamic_gen's throughput path checks streaming stage and token_ids length, unlike this example's identifier-count estimate. [source; call_6f6090a98dfa4984b8f6fd9c93ea0bc3, call_74c7ffb9f9d1495db685e2597467d648, call_f9f94e719d9c44c190bcbe5019bb0149]

All jobs and completion slots are created before timing begins. Reported completions/minute therefore excludes dataset loading, model loading and job creation, but elapsed time includes iteration and console output between completions. [source; call_f9f94e719d9c44c190bcbe5019bb0149]

## Authoring-time findings — pending review

### prefill-counted-as-output (suspected; defect)

The output-token counter counts distinct result identifiers rather than generated tokens.

Trigger: A job emits a prefill result while its prompt still requires further chunks, before generating a token.

Expected: Prefill-only work contributes zero output tokens.

Actual: main increments num_tokens by one for that identifier and includes it in the displayed output tokens/second. Generator skips generation for unfinished prefill jobs, but their prefill results still carry identifiers. Reach is the new example's statistics, not generator output generation.

Locations: 460e201cc332ff93a4d65d7b1ca1f897ad372685:examples/batched_translation.py — main

Source evidence: call_f9f94e719d9c44c190bcbe5019bb0149, call_6fb44d8c4a09444eab82c2357b7a3726, call_e125afafc89346a9a210e2c8498e06a2, call_faaabfb1d68a4f6ca7190fac35db00b7

scalar_transcription: Applied the example's distinct-identifier expression to one prefill-only result; it counted one despite zero output tokens. [call_e125afafc89346a9a210e2c8498e06a2]. Limits: Synthetic result dictionary, not repository generator execution.

### empty-filtered-dataset (suspected; defect)

Dataset summary arithmetic assumes at least one retained passage.

Trigger: The selected dataset is empty or every stripped text field is shorter than 125 characters.

Expected: Report that no passages qualify and exit cleanly.

Actual: main divides by len(in_data), raising ZeroDivisionError before model loading. The task's direct script entry calls main; whole-parent search found no references to batched_translation.

Locations: 460e201cc332ff93a4d65d7b1ca1f897ad372685:examples/batched_translation.py — main

Source evidence: call_f9f94e719d9c44c190bcbe5019bb0149, call_faaabfb1d68a4f6ca7190fac35db00b7

scalar_transcription: Evaluated the average-length expression on an empty list and observed ZeroDivisionError. [call_e125afafc89346a9a210e2c8498e06a2]. Limits: Arithmetic reproduction only; no dataset loader or full script execution.

## Uncertainty and limits

No dataset download, tokenizer execution, model inference, CUDA execution or throughput benchmark was performed.

Chat-template availability, tokenizer compatibility and model compliance with the tags and /no_think instruction remain unverified.

Filesystem cache behavior was inspected but not executed. Scalar checks model only Python counting and empty-input arithmetic.
