# ec00ef3f895212e274ae1d88588bee04b62efd63


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ec00ef3f895212e274ae1d88588bee04b62efd63) · [Evidence ledger](draft.json)

Reorders architecture imports and registration entries, and corrects Gemma3's preprocessing shape comment without changing tensor operations.

- [Registry ordering and Gemma3 shape documentation](#models)

## Problem

The architecture registry had an unsorted model list, and Gemma3's preprocessing comment omitted the batch dimension already added by the code. [source; call_732ff72aa40b48c2910befdd064d5f4d, call_caa349a585294dba927bce2ef02b2f1e]

## Reasoning

The cleanup reorders existing imports and registry entries without adding or removing models. The Gemma3 edit corrects documentation rather than changing tensor construction. [source; call_732ff72aa40b48c2910befdd064d5f4d, call_caa349a585294dba927bce2ef02b2f1e]

## Impact

Registry iteration order changes, but the inspected configuration loader selects entries by architecture string, not position. The declared architecture strings are distinct, so the reorder does not introduce a duplicate-key overwrite. [source; call_553297f1cb284dabbb4299879518f635, call_95b45d933afc48efb2af48eecbe4faea, call_637f21c56cf44f82b08be112ae235eae]

## Source Notes

The Gemma3 vision introduction entry establishes that preprocessing already produced a half-precision tensor with a leading batch dimension. The Mistral3 introduction entry establishes the registry addition retained by this cleanup. [ancestor; call_ce4dd66a2d484f72b79ab24b4f4bfe13, call_70d307b07126468daaa77fd8fc8804bf]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports a native-extension import failure and a reporter-provided environment workaround. Its connection to this inspection is only an inferred shared config.py path; it does not establish a problem addressed by this cleanup. [inference; call_2dbc435199dd444c8089931f1cd037e0, call_95b45d933afc48efb2af48eecbe4faea]

<a id="models"></a>

## Registry ordering and Gemma3 shape documentation

ARCHITECTURES still maps each model's config_class.arch_string to its architecture string, configuration class and model class. get_architectures returns that dictionary unchanged; the only discovered repository caller retrieves a configuration class by the checkpoint's architecture name. [source; call_553297f1cb284dabbb4299879518f635, call_ebdc3247e53c4e6d9a3d48e636966aa8, call_95b45d933afc48efb2af48eecbe4faea]

Gemma3 preprocessing transposes an RGB image from height-width-channel order to channel-height-width order, then converts it to half precision and applies unsqueeze(0). The corrected comment therefore describes (1, 3, resized_height, resized_width): one batch item and three color channels. The existing load-shape hook likewise supplies a leading singleton batch, while get_image_embeddings removes that dimension after forwarding. [source; call_d432a64409014bd89e62344d4d3a3d95, call_caa349a585294dba927bce2ef02b2f1e]

## Uncertainty and limits

Import-order side effects and model execution were not tested.

No numerical algorithm changes here warrant a scalar computation; tensor-shape reasoning is source inspection, not execution.
