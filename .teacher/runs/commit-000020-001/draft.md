# 756ce86a9deb40bcc497c7ea93c4cd7538d229dd


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/756ce86a9deb40bcc497c7ea93c4cd7538d229dd) · [Evidence ledger](draft.json)

Aligns the metadata discriminator with Linear's lowercase EXL3 identifier, restoring per-module format and bit-width fields.

- [Restore lowercase EXL3 metadata recognition](#conversion)

## Problem

Linear.quant_format_id() returns lowercase "exl3", but metadata generation compares it with uppercase "EXL3", skipping the format and bit-width fields. [source; call_c565f043e20d417f9f3ad146f4e02c55, call_293ec27cf09e452fb96c5cbb68ac528c]

## Reasoning

Changing the discriminator to "exl3" aligns the consumer with the existing producer. The serialized format value was already lowercase; this restores branch selection rather than renaming an output value. [source; call_8e786ec3e59e41bbbb0fb641e51572d5, call_c565f043e20d417f9f3ad146f4e02c55]

## Impact

Recognized EXL3 leaves regain quant_format and bits_per_weight in generated metadata. The inspected direct callers are model compilation and util/add_quant_config.py. [source; call_8e786ec3e59e41bbbb0fb641e51572d5, call_7286e66883174209a8b58d81f28ff04a, call_b9c721f84aea4c4a926c0e4c6b479792]

## Source Notes

The parent annotation identifies this producer–consumer mismatch. Inspection of the task diff establishes that this change removes that specific mismatch. [source; call_937d3d12b4d04a0d9b32c3a6984e12e9, call_8e786ec3e59e41bbbb0fb641e51572d5, call_c565f043e20d417f9f3ad146f4e02c55]

<a id="conversion"></a>

## Restore lowercase EXL3 metadata recognition

create_quantization_config_json constructs a model without loading weights, visits leaf modules, and records their stored tensor descriptions. Recognized EXL3 storage additionally receives quant_format="exl3" and bits_per_weight calculated by integer-dividing the trellis tensor's last dimension by 16. [source; call_293ec27cf09e452fb96c5cbb68ac528c, call_8e786ec3e59e41bbbb0fb641e51572d5]

The inventory is placed under tensor_storage alongside the existing quantization_config from config.json and written to quantization_config.json. The patch changes only recognition, leaving tensor inventory collection, output paths, and serialization unchanged. [source; call_293ec27cf09e452fb96c5cbb68ac528c, call_8e786ec3e59e41bbbb0fb641e51572d5]

A standard-library scalar transcription using qformat="exl3" and a synthetic trellis last dimension of 48 omitted both extra fields with the old comparison and produced quant_format="exl3", bits_per_weight=3 with the new comparison. [execution; call_d0771ac86ad94c5393361e384af6284a]

## Uncertainty and limits

No repository metadata generation, model conversion, or filesystem operation was executed; the check transcribed only the conditional with synthetic metadata.

The underlying packing rationale for the unchanged divisor 16 was not independently inspected.

External consumers and dynamically selected callers were not established.
