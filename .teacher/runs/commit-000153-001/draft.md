# a905cffb1a3f66792ea000e9b589557aac3f9d14


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a905cffb1a3f66792ea000e9b589557aac3f9d14) · [Evidence ledger](draft.json)

Merges dev into master with no content beyond the second parent; inspected changes integrate prompting, chat controls and version 0.0.2.

- [Integrating dev into master](#integration)

## Problem

The change merges the dev branch into master through PR #37 rather than presenting an isolated fix. [source; call_9488ed5c8d3b4cc38ec1d1b653dfafff]

## Reasoning

The supplied tree comparisons establish that the merge exactly matches its second parent, 70056fef5f1f841612023027f6abe6f2b295ce57. Its first-parent diff therefore represents integration of existing dev content, not additional merge-specific implementation. [source; call_9488ed5c8d3b4cc38ec1d1b653dfafff]

## Impact

The inspected first-parent changes include template-specific HumanEval BOS handling, chat command interception and integer top-k parsing, and the version increment from 0.0.1 to 0.0.2. [source; call_9488ed5c8d3b4cc38ec1d1b653dfafff, call_3a1db187436f4aceab7916eeca0f6ec1, call_819f5723073b40c2b32b7ed52f8231b0]

## Source Notes

PR #37's available body is empty; it supplies no additional implementation rationale or validation report. [source; call_ad515dd3140d4c5cba95d3281c36a943]

The second-parent annotation explains that the shared version constant feeds package metadata, conversion provenance and release naming. [ancestor; call_774509af5f2b492180bb0ec6a981c218]

<a id="integration"></a>

## Integrating dev into master

HumanEval replaces unconditional add_bos=True with a raw-format-only condition. Granite and Reka templates gain <|endoftext|>, Llama and Mistral gain <s>, Llama3 gains <|begin_of_text|>, and DeepSeek gains its sentence-begin marker. Special-token encoding remains enabled. [source; call_9488ed5c8d3b4cc38ec1d1b653dfafff]

This moves BOS selection from a universal tokenization setting into individual formatted prompts, while retaining automatic insertion for raw mode. [inference; call_9488ed5c8d3b4cc38ec1d1b653dfafff]

Chat intercepts slash-prefixed input before appending it to context: /x exits, /cc invokes copy_last_codeblock on the last response, and other slash commands report an error and skip generation. Its top-k parser changes from float to int. [source; call_3a1db187436f4aceab7916eeca0f6ec1]

The version change is directly visible against master, but the earlier second-parent entry already records that same 0.0.2 increment; it is inherited release identification rather than a fresh version decision in the merge. [inference; call_819f5723073b40c2b32b7ed52f8231b0, call_774509af5f2b492180bb0ec6a981c218]

## Uncertainty and limits

This is a partial integration explanation: the CUDA, MoE, conversion, loader and remaining generator changes were not inspected and are not characterized here.

No repository tests, GPU execution or model evaluation ran. The inspected integration and string changes offer no useful numerical validation.

Chat clipboard behavior and tokenizer output were not executed; the inspected diffs establish control flow, not successful operation.
