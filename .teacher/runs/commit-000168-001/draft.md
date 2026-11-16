# b5fb1827dae8ee8a642ce5c83fca7ccfd905a3fe


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b5fb1827dae8ee8a642ce5c83fca7ccfd905a3fe) · [Evidence ledger](draft.json)

Corrects component-prefixed output-head BPW reporting by separating those heads from ordinary Linear storage totals.

- [Recognize component-prefixed output heads](#models)

## Problem

Model.get_storage_info recognized only the exact key lm_head. Gemma3's language_model.lm_head therefore entered the ordinary Linear totals, leaving reported head BPW at zero. [source; call_9a74f57d9c2b4b40ac5f875de9ac286d, call_167e82e7f6744813a065d654e47c10fd]

## Reasoning

The patch replaces equality with endswith("lm_head"), recognizing component-prefixed heads without changing model declarations or the accounting formulas. [source; call_1211bcb0ff7d46269bbdced3fa681580]

## Impact

eval/ppl.py directly calls this method and prints its decoder/head bitrates. The comparison adapter has a separate helper already using suffix matching, so that helper is unchanged. [source; call_c1c9f914520b456183c838f93445d266, call_d3d895e1d03d42629a8215f1d3975291, call_6ae292e3408249f49997f7dd2d0d3aef]

## Source Notes

An earlier entry describes the same suffix-recognition correction in the comparison adapter; this change applies it to the Model method. [ancestor; call_d0e6ed81e2ce4288a6ee7fbceb5bc374]

Issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” and #7, “quantizing model: undefined symbol: __cxa_call_terminate,” contain model.py import tracebacks. Issue #34, “torch._C._LinAlgError on last layer of quant,” contains a linear.py conversion traceback. Their shared paths are only an inferred contextual connection, not evidence that this accounting patch fixes those failures. [inference; call_4287fb8417af4a5e9140d52066617771, call_a4f4199377764fae9577fb7c679948d7, call_4dda43c2ea064d2e89b0c3deee338ae5, call_1211bcb0ff7d46269bbdced3fa681580]

<a id="models"></a>

## Recognize component-prefixed output heads

Head classification precedes the general Linear branch. Matching a prefixed head now removes both its storage bits and weight count from the decoder average and assigns them to head accounting. Bare lm_head remains recognized. [source; call_1211bcb0ff7d46269bbdced3fa681580, call_9a74f57d9c2b4b40ac5f875de9ac286d]

Storage bits are eight times the sum of tensor element sizes in bytes multiplied by element counts. Linear.get_tensors delegates to its loaded inner implementation, or returns an empty dictionary when unloaded; weights_numel returns in_features × out_features. Thus BPW is storage per weight, not simply a configured quantization width. [source; call_9a74f57d9c2b4b40ac5f875de9ac286d, call_67ae5ef156f54b45936cbe9d2da8fd21]

A standard-library scalar transcription used 400 decoder bits over 100 weights and 320 head bits over 20 weights. For language_model.lm_head, the old/new results were (6, 0, 720) and (4, 16, 720): decoder BPW and head BPW change, while combined counted bits remain constant. The bare-head case remained (4, 16, 720). [execution; call_ac58ed73d0ba453c93d33a2ea573f722]

Suffix matching is a lightweight naming convention rather than explicit head metadata: it accommodates language_model.lm_head but accepts any key ending in lm_head. The patch changes reporting classification, not quantization or forward computation. [source; call_1211bcb0ff7d46269bbdced3fa681580, call_167e82e7f6744813a065d654e47c10fd]

## Uncertainty and limits

Validation used scalar accounting examples, not repository execution with loaded tensors or a GPU.

The storage estimate counts selected Linear tensors, not total runtime GPU memory. Model-level BPW values were not measured.
