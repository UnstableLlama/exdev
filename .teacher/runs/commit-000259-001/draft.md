# 72bdf5a39c35d213f7b5bd977fb436a19683dcfc


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/72bdf5a39c35d213f7b5bd977fb436a19683dcfc) · [Evidence ledger](draft.json)

Corrects the Transformers example to import patch_transformers from its defining submodule rather than an empty package initializer.

- [Import the registration helper from its defining module](#transformers-integration)

## Problem

The example imports patch_transformers from an empty package initializer, although the function is defined in integration/transformers.py. [source; call_4a0a7b9caf8a4ddd8f75edf3a9be2ac1, call_0332e34396b84791bfffde81d851625e, call_a44713c36dd240b89c7c99a55687c8ab]

## Reasoning

Importing directly from the defining module repairs the example without restoring a package-level re-export or changing registration behavior. [source; call_e8229f6708ce47ddb70683a65df42c8c, call_a44713c36dd240b89c7c99a55687c8ab]

## Impact

The change addresses the example's import boundary, not checkpoint compatibility or generation correctness. Its existing top-level patch_transformers() call remains before model loading. [source; call_e8229f6708ce47ddb70683a65df42c8c, call_4a0a7b9caf8a4ddd8f75edf3a9be2ac1]

## Source Notes

Read the earlier Transformers integration entry. It establishes the adapter's introduction, explicit registry patching, and previously recorded integration limitations. [ancestor; call_054ddf74265d45d2a1e7e29fe92e26f0, call_222d8bc2db7c415bbfea0e8cde1351e6]

The earlier entry's eager root-import path is already absent in this task's parent: the root initializer does not import integration, and integration/__init__.py is empty. This one-line task does not restore that path. [source; call_a0a012e4eeda4d63b3123e17349f030b, call_0332e34396b84791bfffde81d851625e, call_e8229f6708ce47ddb70683a65df42c8c]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and the reporter's toolchain workaround. Its connection here is only inferred from the shared exllamav3/__init__.py import boundary; it does not report this example's missing re-export. [inference; call_37737ea3b9134f36ac7b970a6e72aa41, call_a0a012e4eeda4d63b3123e17349f030b, call_e8229f6708ce47ddb70683a65df42c8c]

<a id="transformers-integration"></a>

## Import the registration helper from its defining module

The sole edit changes from exllamav3.integration import patch_transformers to from exllamav3.integration.transformers import patch_transformers. The parent initializer supplies no such re-export; the explicitly named submodule defines the helper. [source; call_e8229f6708ce47ddb70683a65df42c8c, call_0332e34396b84791bfffde81d851625e, call_a44713c36dd240b89c7c99a55687c8ab]

Whole-parent searches locate only this example's import and call, plus the helper definition. No other project importer or caller was found. The correction therefore targets the example's module initialization, including when another program imports the example; it does not change ordinary root-package imports. [source; call_60bee11101a144dc990c937cc5adcc17, call_7e4c61d907e84fd9b0aa55713bd250a1, call_4ac61a4f7f1f412395dbfd28243583a9, call_a0a012e4eeda4d63b3123e17349f030b]

Once imported, the unchanged helper registers Exl3HfQuantizer and Exl3Config under exl3 in Transformers' two mappings and assigns QuantizationMethod.EXL3. The example invokes it unconditionally before main loads a local model with AutoModelForCausalLM.from_pretrained. No previous caller supplies additional guards or argument preparation. [source; call_a44713c36dd240b89c7c99a55687c8ab, call_4a0a7b9caf8a4ddd8f75edf3a9be2ac1, call_60bee11101a144dc990c937cc5adcc17]

## Uncertainty and limits

No repository import, Transformers registration, checkpoint loading or generation was executed; third-party version compatibility and environment-dependent import failures remain unestablished.

No useful numerical computation applies to this import-path correction.

The adapter's broader packaging and decoder-metadata behavior is outside this one-line correction; successful end-to-end operation is not established.
