# bc607b3d08d1c56e3caff36f788af4abcf9e9576


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/bc607b3d08d1c56e3caff36f788af4abcf9e9576) · [Evidence ledger](draft.json)

Moves auxiliary-file copying before the exclusion warning so copied filenames no longer appear beneath an exclusion heading.

- [Separate copied files from exclusion warnings](#conversion)

## Problem

Copied auxiliary filenames previously appeared immediately after the excluded-file warning, using identical bullet formatting. This could make included files look excluded. [inference; call_9bd4734f8c4544f4ba4cc86f50a0adc9]

## Reasoning

The patch moves the existing print-and-copy loop ahead of the ignored-file warning. It separates the lists by their existing headings without changing selection rules or copy destinations. [source; call_070ca81a23584b5d80703b463e2e9c3c, call_9bd4734f8c4544f4ba4cc86f50a0adc9]

## Impact

Successful copies remain identical; their listing now precedes the exclusion warning. Because copying also moves, an exception during copying now prevents that warning from being reached. [source; call_070ca81a23584b5d80703b463e2e9c3c]

## Source Notes

The root conversion entry was read. It establishes compile_model as artifact assembly, including auxiliary-file copying, rather than native-code compilation. [ancestor; call_1e04fcaa967045c3bd4b2280f82736ed]

Issue #33, “Error converting model,” reports a tensor-file opening failure, later diagnosed in the discussion as too many open files, followed by a separate GLM inference discussion. Its relevance here is inferred solely from the matching compile_model traceback; the reordered auxiliary-file loop does not address that failure. [inference; call_206b61f386fa4de0b09b66799bda8d5c, call_54b9f027987c49bb8f1a7aabe6f4162f, call_070ca81a23584b5d80703b463e2e9c3c]

PR #25, “Language layers for Mistral Small 3.1 and InternVL3,” concerns language-only conversion and multimodal support. Shared conversion terminology is not evidence that it motivated this listing change. [inference; call_d0faab991e664c219f85b0eca6cca960, call_070ca81a23584b5d80703b463e2e9c3c]

<a id="conversion"></a>

## Separate copied files from exclusion warnings

The unchanged filter skips directories, original safetensors, config.json and the original shard index. Files ending in .bin, .ckpt, .pth or .pt enter the warning list; other regular files enter the copy list. Only the first ten ignored filenames are displayed, followed by an omitted-count line when necessary. [source; call_9bd4734f8c4544f4ba4cc86f50a0adc9]

A bounded check with tokenizer.json included and weights.bin ignored reproduced the old ambiguous ordering and the new separated ordering. Both variants requested the same input/tokenizer.json-to-output/tokenizer.json copy. [execution; call_1edc20e1186149d2ae0b3ca4067efcb0]

The change preserves print-before-copy behavior: a filename denotes an attempted copy, not proof of its completion. No new sorting, heading, exception handling or file-selection policy is introduced. [source; call_070ca81a23584b5d80703b463e2e9c3c, call_9bd4734f8c4544f4ba4cc86f50a0adc9]

## Uncertainty and limits

No full conversion or filesystem copy was executed. The bounded check executed extracted listing code with a mocked copy operation and a mechanically reordered variant.
