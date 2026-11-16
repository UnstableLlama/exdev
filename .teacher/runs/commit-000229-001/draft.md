# 0e27484613b9bca2d99e719db839e0a456ecb10b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/0e27484613b9bca2d99e719db839e0a456ecb10b) · [Evidence ledger](draft.json)

Removes the multimodal example's cuda:2 pin to use automatic placement, simplifies explicit flushing, and reformats the unchanged image-embedding call.

- [Default placement and streaming-output cleanup](#multimodal)

## Problem

The multimodal example pinned its text model to cuda:2, while its vision component already used default placement. [source; call_3c0caa7f642f4271b872834d441901ba]

## Reasoning

Removing the device argument selects automatic layer splitting rather than merely substituting cuda:0. Model.load delegates to load_gen, whose default device=None selects _load_autosplit. [source; call_fe763007fb494c3b83bc6de11cb42fd3, call_c57b228fd1f64813a17197517a27b40a]

## Impact

The example no longer requires selecting GPU index 2 explicitly; successful loading still depends on available CUDA devices and memory. Improving portability is an inferred motivation, beyond the author's terse “Fix example” message. [inference; call_fe763007fb494c3b83bc6de11cb42fd3, call_c57b228fd1f64813a17197517a27b40a]

## Source Notes

The original multimodal-example entry was read. It establishes the image-alias/embedding integration and notes the hardcoded model directory and cuda:2 selection; it records no defect finding. [ancestor; call_7bf1dbdd13c9494ba34d3c82ec2aa006]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and a reporter-supplied environment workaround. Its overlap is model.py in the traceback; any connection to this task is only inferred from that shared file, not evidence that this example edit addresses it. [inference; call_9a8db0d7a6c54883a5956b0a3094ec9c, call_fe763007fb494c3b83bc6de11cb42fd3]

<a id="multimodal"></a>

## Default placement and streaming-output cleanup

Default loading considers detected CUDA devices in index order, reserves 0.25 × 1024³ bytes per device, and loads modules while forwarding a dummy state to estimate working memory. Recognized out-of-memory failures unload the current module and retry on the next device; exhausting devices raises an insufficient-VRAM error. Modules marked prefer_cpu still load on CPU. This differs materially from the old single-device path, which loads modules without that splitting probe. [source; call_c57b228fd1f64813a17197517a27b40a]

The default reserve calculation evaluates to 268,435,456 bytes, or 256 MiB. [execution; call_cc200a68da784307a1dce956459b139e]

Both streaming print sites replace a separate sys.stdout.flush() with print(..., flush=True), retaining end="". The image-embedding call is only reformatted: tokenizer and image arguments, iteration order and downstream embedding plumbing are unchanged. [source; call_fe763007fb494c3b83bc6de11cb42fd3, call_3c0caa7f642f4271b872834d441901ba]

A bounded standard-library check of the two print forms produced identical concatenated text and three flush calls for a prompt, a fragment and an empty string. [execution; call_cc200a68da784307a1dce956459b139e]

## Uncertainty and limits

No repository model loading, GPU execution or image generation was run. Automatic placement success and performance remain unestablished.

The print check exercised standard-library equivalents with an in-memory stream, not the example's actual terminal or streaming generator.
