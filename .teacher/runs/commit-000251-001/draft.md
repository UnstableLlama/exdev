# dbbeccfb63ee50c8de7feff6e45001b98406958f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/dbbeccfb63ee50c8de7feff6e45001b98406958f) · [Evidence ledger](draft.json)

Adds native Torch dtype objects to Safetensors listings by default, while explicitly preserving JSON-ready listings for quantization metadata export.

- [Retain native dtype objects without changing exported metadata](#loading-tokenization)

## Problem

Safetensors metadata exposed only a stringified Torch dtype, not the dtype object returned by convert_dtype. [source; call_57fcbb695bfc427483cf5fafa254f735]

## Reasoning

The change separates runtime metadata from JSON-ready metadata: list_tensors retains the existing dtype string and optionally adds torch_dtype. The quantization inventory explicitly opts out of the object-valued field before JSON serialization. [source; call_7b753810cfbb4e959fecf57099ec4344, call_5b0ad603bc7e4efa92645a8ef1ee7434, call_9a161ee696234c1f811a9ed96eb36a30]

## Impact

Existing calls receive richer metadata by default; quantization_config.json retains its previous tensor-record fields. Tensor loading and its dtype conversions are unchanged. [source; call_7b753810cfbb4e959fecf57099ec4344, call_5b0ad603bc7e4efa92645a8ef1ee7434, call_57fcbb695bfc427483cf5fafa254f735]

## Source Notes

The earlier inventory entry establishes that list_tensors and the sidecar exporter were introduced together, using header metadata rather than loading tensor payloads. [ancestor; call_ad23cfb46cf24ab7b25a1e7e9d9cfc4d]

Issue #33, “Error converting model,” reports file-opening failures and later GLM sampling trouble. Issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports a padding/sliced-layer size mismatch. Their relationship to this task is only an inferred shared-loader context: neither discussion establishes a motivation for retaining dtype objects. [inference; call_36c2f4e15aef40cf9c5c99ae0f3dee0c, call_c17a1d1cb31f43f09b6a0ec01867c201, call_f7dc7b86c11b45b9a2c8237464512a5f, call_7b753810cfbb4e959fecf57099ec4344]

<a id="loading-tokenization"></a>

## Retain native dtype objects without changing exported metadata

list_tensors still selects an exact prefix or dot-delimited descendants, requires new_tensors to be None, and derives shape and payload byte count from cached headers. convert_dtype supplies the native Torch dtype; the new torch_dtype field stores that object without replacing the existing dtype string. only_serializable defaults to False and suppresses only the new field when true. [source; call_57fcbb695bfc427483cf5fafa254f735, call_7b753810cfbb4e959fecf57099ec4344]

The exporter change supplies a necessary companion to the richer default. create_quantization_config_json places each listing under stored_tensors, eventually passed to json.dumps; its new only_serializable=True argument preserves the prior record structure instead of exporting native objects. [source; call_9a161ee696234c1f811a9ed96eb36a30, call_5b0ad603bc7e4efa92645a8ef1ee7434]

Whole-tree searches found one list_tensors definition and three caller functions. The exporter opts out. Gemma3VisionModel.get_additional_compiled_tensors and the corresponding Mistral3 method retain their old calls, so both now return the additional field. Their inspected consumer, compile_model, reads n_bytes for shard allocation and then loads tensors by key; it neither serializes these metadata dictionaries nor consumes torch_dtype. These paths therefore tolerate the added field without requiring it. [source; call_e3f75c26dcc14fb0876e8478230f5516, call_18c6786fa5aa4a4090feed424ee729dd, call_5aad5ce3fdf34859ac18b5543b420a6f, call_51caf6bd396d4e81857b918748a243cb, call_6f8f5079868842adbc6810cc86ab02ce, call_d5450842b3dd44bca95d73d05f0142b7]

A standard-library transcription verified object identity retention, equality of the remaining record fields, and JSON round-tripping of the serializable branch. The object-bearing sentinel branch raised TypeError; this models the serialization boundary rather than testing Torch or the repository implementation. [execution; call_41450ec82b5741a69eed19250551e3db]

## Uncertainty and limits

No repository implementation, Torch dtype serialization, tensor loading or end-to-end conversion was executed. The bounded Python check modeled the new dictionary branch using a nonserializable sentinel.

Whole-parent-tree literal searches establish the inspected in-repository callers, not dynamic or external consumers.
