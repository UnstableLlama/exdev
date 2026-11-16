# f8dc9975fe88c79fcf1a12f2160974b5442695dd


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f8dc9975fe88c79fcf1a12f2160974b5442695dd) · [Evidence ledger](draft.json)

Adds a shared device-index option to model_diff.py while preserving CPU-preferred modules, sequential loading and existing metrics.

- [Selectable device for model comparison](#usage-evaluation)

## Problem

The model comparison script hardcoded cuda:0 for both models' non-CPU modules. [source; call_7c8efe0985b74e34b1fde27f7fbc3795]

## Reasoning

The change constructs one device from the command-line argument and uses it for both model branches, retaining the prefer_cpu override. [source; call_8efe5d23d5a94f6bbfdbbd2c7abaec29]

## Impact

Device selection becomes configurable without changing the sequential module-loading lifecycle or comparison formulas. [source; call_8efe5d23d5a94f6bbfdbbd2c7abaec29, call_7c8efe0985b74e34b1fde27f7fbc3795]

## Source Notes

The earlier deferred-loading entry was read. It establishes the module-scoped loading and handle-cleanup design and records an inherited perplexity indexing concern. [ancestor; call_cbe2bddd7739423897857bc6b242363c]

PR #26, “Superior 3INST parameters,” discusses using model_diff.py for decoder evaluation. Issue #33, “Error converting model,” initially reports file-opening failures and later uses the script to investigate GLM4 output. Their relationship to this change is inferred solely from the shared script; neither cited discussion establishes the motivation for device selection. [inference; call_2451c38109334b2b986af9465db41b0e, call_31a04587aa5e46108cb6ee9ba6538426, call_71931103246d4a5fb085025308bd3939, call_8efe5d23d5a94f6bbfdbbd2c7abaec29]

<a id="usage-evaluation"></a>

## Selectable device for model comparison

The parser adds -d/--device as an integer with default 0 and help text “CUDA device index.” main immediately passes that integer to torch.device; it does not construct an explicit cuda:N string. [source; call_8efe5d23d5a94f6bbfdbbd2c7abaec29]

Both paired module loads receive the resulting device unless their prefer_cpu capability selects the unchanged 'cpu' branch. This is one shared device choice, not independent placement for A and B or multi-device sharding. [source; call_8efe5d23d5a94f6bbfdbbd2c7abaec29]

The base Module.load stores the supplied device and propagates it to submodules. prepare_for_device moves the activation to that stored device before forward. Consequently, changing the load destination also controls activation placement through the existing mechanism rather than a new explicit transfer in the script. [source; call_cdc045c9a8f44eacb6e4397bb66728f8, call_7c8efe0985b74e34b1fde27f7fbc3795]

A still completes deferred loading, preparation, forward, unload, collection close and memory cleanup before B follows the same sequence. The new parser field supplies the attribute required by the new main entry statement; these edits work together. [source; call_7c8efe0985b74e34b1fde27f7fbc3795, call_8efe5d23d5a94f6bbfdbbd2c7abaec29]

Inspection of the parent together with the complete patch shows that the previously recorded perplexity axis-bound concern is carried over, not corrected by device selection. [source; call_7c8efe0985b74e34b1fde27f7fbc3795, call_8efe5d23d5a94f6bbfdbbd2c7abaec29]

## Authoring-time findings — pending review

### inherited-perplexity-axis-bound (suspected; defect)

The unchanged nested perplexity helper bounds sequence slices using vocabulary size.

Trigger: The metrics loop receives more prediction positions than vocabulary entries, for example 2047 positions and vocabulary size 1024.

Expected: Accumulate every next-token prediction once.

Actual: The loop stops at logits_.shape[1], covering only 1024 of those 2047 positions. Larger vocabularies can instead produce trailing empty slices.

Locations: f8dc9975fe88c79fcf1a12f2160974b5442695dd:eval/model_diff.py — main.ppl

Source evidence: call_7c8efe0985b74e34b1fde27f7fbc3795, call_8efe5d23d5a94f6bbfdbbd2c7abaec29, call_f0a5dc3ba99344a29ba2c73caa133838

source_inspection: Whole-tree search located the helper's direct call in main's per-model metrics loop; other matches are the separately named test_ppl. The CLI invokes main, and the task patch leaves this helper and call unchanged. [call_f0a5dc3ba99344a29ba2c73caa133838, call_7c8efe0985b74e34b1fde27f7fbc3795, call_8efe5d23d5a94f6bbfdbbd2c7abaec29]. Limits: Reach is established for the script's metrics loop, conditional on reaching it successfully.

scalar_transcription: A standard-library model of the inspected loop covered 1024 of 2047 positions for vocabulary 1024; vocabulary 32000 covered all 2047 positions over four iterations. [call_2627494bdb1f48cc97c39e501f1ce12f]. Limits: This models integer bounds, not repository execution or Torch empty-slice behavior.

## Uncertainty and limits

No Torch or CUDA execution was performed. Integer torch.device construction and its behavior across library versions and accelerator environments remain unverified.

Module.load and the base activation-transfer mechanism were inspected, but compatibility across every module override was not established.

The numerical check models only inherited perplexity slice bounds; it does not execute tensor operations or establish end-to-end metric correctness.
