# c264054b9450bd169b3b6ba2e05b20e0a66e0885


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c264054b9450bd169b3b6ba2e05b20e0a66e0885) · [Evidence ledger](draft.json)

Adds a configurable Gemma3 image-description example, wiring vision embeddings into streaming and non-streaming generation and adding requests for optional URL images.

- [Image embeddings through the generation interface](#multimodal)

## Problem

The existing generator example demonstrates text completions; this change adds an image-description example using the existing Gemma3 vision component. [source; call_00a832dd1780450da0cd7849cdea5bce, call_53a3774e0c9e4384b175ccd628d51f15]

## Reasoning

Image aliases and image vectors travel together: aliases enter the formatted prompt, while the same embedding objects are supplied to tokenization and the streaming Job, or directly to generate(). These are complementary steps, not independent examples of passing images. [source; call_53a3774e0c9e4384b175ccd628d51f15]

## Impact

requirements_examples.txt adds requests, matching the new script's import and optional URL loader. Whole-parent-tree search found no existing requests imports; this does not exclude dynamic or external use. The import is unconditional even when using the default local image. [source; call_14d48d41b81847b0815780a5506445f5, call_0066b8b0351c4bfa8fc638ad01367c99, call_53a3774e0c9e4384b175ccd628d51f15]

## Source Notes

The Gemma3 vision ancestor entry establishes the image-to-embedding implementation and its required preprocessing configuration. The original usage entry establishes the generate()/Job example pattern and warns that examples use local model paths and device selections. [ancestor; call_8f137a7deb524c218c9bba5e7da3de2b, call_c442e6eead00410f850c31821cb3bb57]

<a id="multimodal"></a>

## Image embeddings through the generation interface

main constructs the text model, an 8192-token cache and tokenizer, then separately loads component="vision" from the same configuration. The cache capacity and 500-new-token response cap are example settings, not demonstrated model limits. [source; call_53a3774e0c9e4384b175ccd628d51f15]

get_image requires exactly one truthy file or URL argument. Local paths resolve relative to the script; URL responses are opened through requests.get(..., stream=True). Each image is passed to get_image_embeddings; parent-tree search found its definition but no existing caller. [source; call_53a3774e0c9e4384b175ccd628d51f15, call_27f828db53d14b2a96e375e83c363e9e]

The selected Gemma3 method preprocesses the image, runs noncausal vision inference, moves projected vectors to CPU, and packages them as MMEmbedding with image-boundary tokens and an alias. The example joins those aliases with newlines before the instruction; it does not serialize pixels into text. [source; call_88d9ec0d2db141e4a6639b4e9f6071dc, call_53a3774e0c9e4384b175ccd628d51f15]

Streaming is enabled by default: explicitly encode the prompt with special-token handling and embeddings, enqueue a Job, then print each returned text fragment until no jobs remain. The alternate branch delegates the prompt and embeddings to generate(). Both use Gemma stop conditions. [source; call_53a3774e0c9e4384b175ccd628d51f15]

The Gemma prompt helper already includes BOS and turn markers and ignores its system-prompt argument. Consequently, the example's configured system_prompt does not enter the generated prompt. Its stop conditions are tokenizer EOS and the end-of-turn string. [source; call_da1b9a4bc5ac41bc8182388542a8a6c9, call_53a3774e0c9e4384b175ccd628d51f15]

## Uncertainty and limits

No model loading, network retrieval, Pillow operation or GPU generation was executed. No useful isolated arithmetic check would establish this integration's behavior.

The example requires editing the hardcoded model directory and potentially its cuda:2 text-model device. Successful placement and available memory were not established.

Binary image contents were not inspected, and compatibility inspection of all existing generator and loader call sites was incomplete.
