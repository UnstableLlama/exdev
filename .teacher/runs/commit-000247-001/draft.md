# dcae5a04be7885ad9dc9a6cfcb135ead75847695


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/dcae5a04be7885ad9dc9a6cfcb135ead75847695) · [Evidence ledger](draft.json)

Adds Gemma3 list-based image ingestion using one batched forward call, then returns separate MMEmbedding objects while preserving scalar-call compatibility.

- [Batching Gemma3 images while preserving per-image embeddings](#models)

## Problem

Gemma3 image ingestion previously accepted one image and returned one MMEmbedding per call. The change adds list-based ingestion while preserving that scalar interface. [source; call_9e87f84d32fe4b9596241027c88eda12]

## Reasoning

Preprocessing already produces a singleton-batch tensor at a configured fixed size. Concatenating those tensors along dimension zero supplies one batched forward call without changing image preprocessing. [source; call_54c3916b342c45ec9224aaa3167a1245, call_9e87f84d32fe4b9596241027c88eda12]

## Impact

A list input returns a list of embeddings, including for a one-element list; a scalar input still returns one embedding. List input rejects a supplied text_alias through an assertion. [source; call_9e87f84d32fe4b9596241027c88eda12]

## Source Notes

The Gemma3 introduction and vision-implementation ancestor entries were read. They establish the progression from a vision stub to the fixed-size preprocessing, pooling and projection pipeline reused here. [ancestor; call_8e7258c6dd8940a18edf3b878187b83e, call_7c288d563a7940bc8c9fb0ef8c4f8fbb]

Issue #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” reports mismatched vocabulary/logit widths. Its connection is inferred from its explicit gemma3.py reference, not evidence that image batching addresses that report. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension loading failure; its connection is inferred from the shared model.py path. Neither report establishes a batching defect. [inference; call_639d455ec67345359cb28fe4ab558562, call_0301ce4317424530b80a57e55620d90c, call_9e87f84d32fe4b9596241027c88eda12]

<a id="models"></a>

## Batching Gemma3 images while preserving per-image embeddings

The list branch preprocesses images individually, concatenates their tensors on the leading batch axis, and calls forward once with causal=False. The scalar branch wraps the original image in a list only for subsequent bookkeeping. Preprocessing remains sequential; the vision forward receives the batch. [source; call_9e87f84d32fe4b9596241027c88eda12, call_54c3916b342c45ec9224aaa3167a1245]

Retaining the batch dimension replaces the old squeeze(0). Consequently image-token count moves from shape[0] to shape[1], and embedding_tensor[i] supplies each MMEmbedding with a two-dimensional token-by-feature tensor. These edits are interdependent: retaining a batch axis requires changing both token counting and per-image extraction. [source; call_9e87f84d32fe4b9596241027c88eda12, call_b0502aaff8714e2a8b3154693ebcb1d1]

Each image gets its own token string: one start-of-image ID, one -1 placeholder per embedding row, and one end-of-image ID. MMEmbedding replaces placeholders with independently allocated synthetic IDs and generates an alias when none is supplied. The batch assertion prevents assigning one caller-supplied alias to every image. [source; call_9e87f84d32fe4b9596241027c88eda12, call_b0502aaff8714e2a8b3154693ebcb1d1]

Metadata takes original_size from the corresponding input image. Although prep_image_size is retained only from the last preprocessing iteration, the inspected preprocessing method returns the same configured target size for every image, so that reuse agrees with its present contract. [source; call_9e87f84d32fe4b9596241027c88eda12, call_54c3916b342c45ec9224aaa3167a1245]

Whole-parent-tree searches found one direct caller, examples/multimodal.py, and the separate Mistral3 definition; no Gemma3VisionModel subclass appeared. The example passes individual images and consumes individual aliases, so its existing list comprehension remains compatible. Mistral3 remains scalar-only. Passing a whole image list through the example's existing comprehension without adapting its consumers would instead create nested lists. [source; call_78c238ac195a4d119be302f98d4a03e9, call_0fa874ee06ed4dfb8b5fab534610553e, call_70aae7f92acb45ea94a364a9a48a1cae, call_c527ecd4364841ecb4577e601a94aa74, call_9e87f84d32fe4b9596241027c88eda12]

A standard-library packaging transcription checked batches of one and three images with five embedding rows each. It preserved per-image rows, produced seven-token representations, and allocated respectively five and fifteen distinct synthetic IDs. This checks indexing and allocation arithmetic only. [execution; call_30b244a00326496398c6fd465c52a137]

The design trades repeated forward invocations for a single larger invocation, while still returning ordinary per-image containers suitable for existing tokenizer and Job interfaces. Improved throughput is plausible, not measured by the inspected evidence. [inference; call_9e87f84d32fe4b9596241027c88eda12, call_70aae7f92acb45ea94a364a9a48a1cae]

## Uncertainty and limits

No repository tensor operations, image-library operations or GPU inference were executed. The scalar check models output packaging, not vision inference or numerical equivalence.

Batch memory requirements and throughput gains were not measured. The implementation concatenates the entire input list and introduces no chunking.

The list branch has no explicit empty-list handling; empty-input filesystem or tensor-library behavior was not executed.
