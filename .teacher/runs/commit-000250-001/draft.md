# 7ea95598374edd2f1eec4ea2349c6196b0a56679


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/7ea95598374edd2f1eec4ea2349c6196b0a56679) · [Evidence ledger](draft.json)

Adds a VLM-based yes/no image-search example and optional thumbnail gallery. It reuses existing vision batching and suffix-logit APIs, while exposing an empty-final-batch failure path and consuming the inherited Gemma prompt-closure discrepancy.

- [Single-token image classification and result browsing](#image-search)

## Problem

The change adds an example that searches local images using one shared yes/no question, with optional visual browsing of matches. [source; call_57df33e31bfb49ca8ff39c01b7e3408a, call_d24dec2509b54dccb11cb5f821444f91]

## Reasoning

Instead of generating complete answers, the example compares summed next-token probability mass for case-insensitive yes/no prefixes. This is a lightweight classification heuristic, not exact answer parsing or a calibrated confidence threshold. [source; call_57df33e31bfb49ca8ff39c01b7e3408a]

## Impact

Two new example files compose existing model-loading, vision-embedding, prompt-formatting and forward APIs; the change does not modify library implementations or declared dependencies. [source; call_57df33e31bfb49ca8ff39c01b7e3408a, call_d24dec2509b54dccb11cb5f821444f91]

## Source Notes

Read the earlier list-ingestion entry, which establishes that Gemma3 batches image lists whereas Mistral3 processes list members sequentially. [ancestor; call_2361026c00c447c6b2a6bbcf7a789708]

Read the architecture-default prompt entry, which records Gemma system interpolation and user-turn closure observations. [ancestor; call_1299085f4cd94bb8b08c9df775e11f56]

The inspected Gemma3 formatter retains both observations unchanged. The new example supplies no system prompt, so it does not trigger the interpolation branch, but it does use the unclosed user-turn construction. [source; call_cf6b567bd2ec4ee9a2fafa9ac3601827, call_57df33e31bfb49ca8ff39c01b7e3408a]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns an extension import failure; issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” concerns incompatible logit dimensions. Their connection to this task is inferred only from shared inspected model.py and gemma3.py paths, not an upstream association with image search. Neither report verifies this example. [inference; call_c091472d779a49deac0bc982c1fd6c61, call_2e1a2c1f58044fac94c88586caf743cc, call_57df33e31bfb49ca8ff39c01b7e3408a]

<a id="image-search"></a>

## Single-token image classification and result browsing

resolve_files accepts a file, recursively enumerates a directory, or expands a recursive glob. main concatenates results without deduplication or extension filtering, attempts Image.open for each path, and counts caught IOError/SyntaxError failures as skipped files. [source; call_57df33e31bfb49ca8ff39c01b7e3408a]

The CLI requires a model directory, prompt and one or more input arguments. Batch size defaults to 1; --no reverses the strict comparison and --view enables the gallery. model_init.add_args(cache=False) omits cache arguments, so init returns no cache. A separate vision component is instantiated and loaded. [source; call_57df33e31bfb49ca8ff39c01b7e3408a, call_cc0ff72606c949fd9ace8d410abefc03]

Batch sizes above 1 are reduced to 1 unless the vision model advertises fixed_size_image_embeddings. The whole-parent-tree search finds that capability only in Gemma3. Its list method concatenates preprocessed images for one forward; Mistral3's list method recursively processes individual images. Thus the capability guard supplies the equal-sized batching precondition rather than merely selecting a faster implementation. [source; call_57df33e31bfb49ca8ff39c01b7e3408a, call_50acd40e37d64ccc9f91fa184f2c1b11, call_2fe81b32a54f441dbb0e36c2574c6682, call_b66641bb54b44ae88060d119d85cb7ed]

Each returned embedding contributes its text_alias followed by the stripped question to model.default_chat_prompt. Tokenizer.encode replaces aliases with their token lists; indexed_embeddings then lets Embedding.forward substitute the corresponding vision vectors. The parent multimodal example already prepares aliases and passes embeddings, but calls vision ingestion separately per image and explicitly enables special-token encoding. The new example instead always supplies an image list and relies on encode's default special-token setting. [source; call_57df33e31bfb49ca8ff39c01b7e3408a, call_d5a48629ea344d669c8768a594cd6a66, call_980421ac95be4c3ea5774fef04a0b16b, call_301c4e3abe814c35a7fb85e35b12b5d6, call_717fef993b3e4088aba7cbccc22a9bbd]

last_tokens_only=1 narrows hidden states immediately before the logits-output module, retaining one final sequence position rather than generating one token. The example slices logits to tokenizer.actual_vocab_size before softmax, transfers probabilities to CPU, and sums mask-selected vocabulary entries. It prints a match when yes mass exceeds no mass, or the reverse under --no; ties match neither mode. [source; call_57df33e31bfb49ca8ff39c01b7e3408a, call_f2e8ebb3fc2c4474a738bae1f712a6ee, call_d5a48629ea344d669c8768a594cd6a66]

get_token_mask uppercases both the vocabulary piece and requested prefix; its two alternative prefixes are identical. A scalar transcription selected Yes, YES and Yesterday for yes, and No and Nobody for no, while excluding leading-space variants. With illustrative masses 0.3 and 0.1, the default comparison selects yes despite 0.6 probability elsewhere. This demonstrates the heuristic's scope, not checkpoint behavior. [execution; call_e973d3bc0d884593845751e5c85cb90e, call_57df33e31bfb49ca8ff39c01b7e3408a]

The gallery imports Tk and ImageTk only when invoked, preloads padded 256-by-256 thumbnails, and rebuilds the grid on resize. Ten pixels of thumbnail spacing gives a nominal 266-pixel column pitch. Clicking opens an image scaled down, never up, to fit the screen with 50-pixel margins; Escape or a click closes that window. Thumbnail preloading favors simple redraws over bounded thumbnail memory. [source; call_d24dec2509b54dccb11cb5f821444f91]

## Authoring-time findings — pending review

### empty-final-image-batch (suspected; defect)

A skipped final file can cause inference on an empty image batch.

Trigger: Run the new CLI with only an unreadable/non-image file, or with a skipped final file immediately after a completed batch.

Expected: Count the skipped file and finish without invoking inference on an empty batch.

Actual: The end-of-input condition invokes get_image_embeddings even when batch_images is empty. Gemma3 reaches torch.cat with an empty tensor list. Mistral3 returns an empty list, after which Tokenizer.encode reaches max([]). The source therefore exposes a failure path instead of printing final totals normally. Parent-tree search found no imgsearch callers; the established entry point is the new script's __main__ invocation.

Locations: 7ea95598374edd2f1eec4ea2349c6196b0a56679:examples/imgsearch.py — main

Source evidence: call_57df33e31bfb49ca8ff39c01b7e3408a, call_2fe81b32a54f441dbb0e36c2574c6682, call_b66641bb54b44ae88060d119d85cb7ed, call_d5a48629ea344d669c8768a594cd6a66, call_fd711996ef6744ada773beaa0cf25394

scalar_transcription: Transcribed the batch accumulation and flush condition. Both an all-skipped singleton and a valid image followed by a skipped file produced an empty final call. [call_e973d3bc0d884593845751e5c85cb90e]. Limits: No image decoding, tensor library or repository function executed.

### inherited-gemma-turn-closure (suspected; defect)

The new Gemma3 search path consumes an inherited formatter that omits user-turn closure.

Trigger: Process an image using Gemma3 through the new main function.

Expected: Close the user turn with <end_of_turn> before opening the model turn, consistent with the existing Gemma example formatter.

Actual: Gemma3Model.default_chat_prompt places only a newline between user content and the model-turn opener. The task leaves that implementation unchanged while adding a direct caller. The separate system interpolation observation also persists, but this caller does not supply a system prompt.

Locations: 7ea95598374edd2f1eec4ea2349c6196b0a56679:examples/imgsearch.py — main, 7989c93b6a476a918dbfff0a0b96954a79111662:exllamav3/models/gemma3.py — Gemma3Model.default_chat_prompt

Source evidence: call_57df33e31bfb49ca8ff39c01b7e3408a, call_cf6b567bd2ec4ee9a2fafa9ac3601827, call_ff537bff19724d51896349a4e4352bc0, call_a125a07811df4aa1b347ebd0381be48f

source_inspection: Compared the inherited method, new caller and existing Gemma formatter; whole-parent-tree search found definitions but no earlier default_chat_prompt callers. [call_cf6b567bd2ec4ee9a2fafa9ac3601827, call_ff537bff19724d51896349a4e4352bc0, call_a125a07811df4aa1b347ebd0381be48f]. Limits: Format discrepancy only; inference failure or classification degradation was not measured.

## Uncertainty and limits

No repository model, tokenizer backend, Pillow operation, GPU inference or Tk interface was executed. Classification quality, memory use and throughput remain unmeasured.

The scalar check transcribes batching and prefix selection with synthetic inputs; it does not execute the example or establish any checkpoint's vocabulary.

Architecture-default templates are not checkpoint-specific validation. The new tokenizer.encode call omits encode_special_tokens=True, unlike the inspected multimodal example; actual backend treatment and resulting model quality were not tested.

Whole-tree literal searches establish inspected source occurrences, not dynamically constructed or external callers.
