# 5ad79b071f48d26906d737b5c6b4d97e9cb0a457


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/5ad79b071f48d26906d737b5c6b4d97e9cb0a457) · [Evidence ledger](draft.json)

Adds an overridable autosplit input-shape/dtype hook while preserving the integer-token default, plus an empty model capability dictionary.

- [Model-defined dummy inputs for autosplit](#models)

## Problem

Autosplit hard-coded its initial dummy input as a batch of integer token IDs, preventing models from specifying a different input shape or dtype. [source; call_0ed33ea70b524c3eb5465cfdc30c56c2, call_b2ca825cba764c7f8d1445a6c7ab3b0f]

## Reasoning

Moving that specification into an overridable model method preserves the text-model default while allowing specialized models to reuse the existing loading and memory-probing loop. [inference; call_0ed33ea70b524c3eb5465cfdc30c56c2, call_b2ca825cba764c7f8d1445a6c7ab3b0f]

## Impact

This supplies an extension point, not a vision implementation: the diff adds no specialized override, architecture registration or image preprocessing. [source; call_0ed33ea70b524c3eb5465cfdc30c56c2]

## Source Notes

The root models entry was read; it describes the existing sequential dummy-forward autosplit mechanism and single-device alternative. [ancestor; call_5aace224e9e645fe96f3ca5b80fb1ac1]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” and issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” concern native-extension import/build failures. Their relationship to this change is only an inferred file overlap: both tracebacks pass through model.py, whereas this diff changes autosplit input metadata, not imports. [inference; call_f543c2c276ce4675bae0755a968be6c2, call_65f0a0abc43647628ec8ff6a4d895415, call_0ed33ea70b524c3eb5465cfdc30c56c2]

<a id="models"></a>

## Model-defined dummy inputs for autosplit

Model.default_load_shape_dtype(chunk_size) returns ((1, chunk_size), torch.long). The leading 1 preserves the single-batch probe; chunk_size remains the requested probe sequence length. _load_autosplit now obtains both initial metadata values through self, enabling subclass dispatch without changing its arguments. [source; call_0ed33ea70b524c3eb5465cfdc30c56c2]

The metadata feeds torch.zeros on the selected load device. After the first module, autosplit retains intermediate tensor shape and dtype for retries; an out-of-memory failure unloads the module, discards the dummy tensor and advances to another device. Thus the new hook changes the initial probe, not the splitting policy or intermediate-state recovery mechanism. [source; call_b2ca825cba764c7f8d1445a6c7ab3b0f, call_0ed33ea70b524c3eb5465cfdc30c56c2]

Whole-parent-tree search found no existing default_load_shape_dtype definition or use. The sole direct caller of _load_autosplit is load_gen; its explicit-device branch instead calls _load_single and does not use the new hook. load consumes load_gen for synchronous loading. [source; call_b3921424efe048d5bac61dd2c2bee2c9, call_c0037f28473a42aeb380ff70db411887, call_b2ca825cba764c7f8d1445a6c7ab3b0f]

The constructor also initializes an empty model-level caps dictionary. This is separate from the module.caps checks used by autosplit for CPU preference and logits handling; the new shape hook does not depend on it. The remaining edits correct quotation in the component assertion message and add a trailing parameter comma. [source; call_0ed33ea70b524c3eb5465cfdc30c56c2, call_277a168594564a7b9d6f4ad82cea4b4b, call_b2ca825cba764c7f8d1445a6c7ab3b0f]

## Uncertainty and limits

No GPU loading or memory-placement tests were run. A scalar arithmetic check would not establish the behavior of this dispatch-only change.

Arbitrary initial shape does not remove downstream requirements: autosplit still forwards one zero-filled tensor with empty parameter dictionaries, bypasses Model.prepare_inputs, and assumes three-dimensional state when processing a logits_output module.

No concrete non-text override was supplied or executed; compatibility with particular vision models remains unestablished.
