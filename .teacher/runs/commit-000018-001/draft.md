# b73e159bc81f0b4bf0f2a2413e223919622e6ff9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b73e159bc81f0b4bf0f2a2413e223919622e6ff9) · [Evidence ledger](draft.json)

Adds quantization_config.json generation during compilation and through a standalone utility, recording leaf-module tensor storage and EXL3 bit widths from headers.

- [Export a header-derived quantization inventory](#conversion)

## Problem

Compilation previously wrote aggregate quantization settings into config.json but did not generate a per-module tensor-storage inventory. [source; call_bd16775d15024152b5cd3ff7fdee8b49, call_b2507b19096141a98c040d58e4f75c31]

## Reasoning

The new sidecar combines existing quantization settings with metadata derived from the output model's module structure and Safetensors headers, rather than loading weights to inspect their storage. [source; call_41f0f744a2674ccea1f6581bd0763412, call_80dc6adac68849bb97bcfbac488f2a98]

## Impact

Compilation now generates quantization_config.json after writing config.json. A separate utility creates or overwrites the sidecar for an existing model directory. [source; call_b2507b19096141a98c040d58e4f75c31, call_3fc15baa807b4c2c843d14adf7b51481]

## Source Notes

The additional update_config helper sets the literal key tied_word_embeddings to true when that key already exists; it does not insert an absent key. The standalone utility does not call this helper. [source; call_41f0f744a2674ccea1f6581bd0763412, call_3fc15baa807b4c2c843d14adf7b51481]

<a id="conversion"></a>

## Export a header-derived quantization inventory

compile_model already writes tensor shards and aggregate settings including quant_method, version, bits and calibration dimensions. The new call runs after config.json is closed, so metadata generation reads the just-written output directory. [source; call_bd16775d15024152b5cd3ff7fdee8b49, call_b2507b19096141a98c040d58e4f75c31]

create_quantization_config_json constructs Config and Model without calling a weight-loading method, iterates the model, and skips modules with children. Each remaining module contributes stored_tensors under its primary key. It requires config.json to contain quantization_config, adds tensor_storage to that object in memory, and writes the enriched object to the separate sidecar rather than rewriting config.json. [source; call_41f0f744a2674ccea1f6581bd0763412]

SafetensorsCollection.list_tensors selects exact keys or dot-delimited descendants. It reports header shape, payload byte count as end minus beginning, and the string form of the converted Torch dtype. It uses existing header maps, not get_tensor; consequently this inventory contains neither tensor payloads nor shard filenames. [source; call_80dc6adac68849bb97bcfbac488f2a98, call_85d897413bb74cb284712516dfb60896]

Module.quant_format_id defaults to None. Linear overrides it using the same storage-group predicate now shared with load_exl3: trellis plus either sv or svh and either su or suh. Metadata classification checks the primary key only, while the refactored loader still accepts its key argument. [source; call_e81bd54b25bd4ebdb914e61dae34b181, call_7ca82d68790b4d9391ce60a53ccc314a]

Recognized EXL3 leaves receive quant_format='exl3' and bits_per_weight equal to the trellis header's last dimension divided by 16 using integer division. This matches LinearEXL3's existing K calculation; it is not calculated from total storage bytes and therefore does not account for ancillary tensors. [source; call_41f0f744a2674ccea1f6581bd0763412, call_78b439eddc2d40a3bb26006f3d01f309]

A scalar transcription confirmed that the prefix rule includes layer.1 and layer.1.weight but excludes layer.10.weight and layer.1x. Example last dimensions 32, 48, 64, 96 and 128 yield reported bit widths 2, 3, 4, 6 and 8 respectively. [execution; call_50fc6e347e084f439d465774c18ce4c8]

The standalone utility requires --model_dir/-m and uses preexisting sidecar presence only to choose its Created/Updated message. Both paths regenerate metadata from config.json and model storage rather than merging the previous sidecar. [source; call_3fc15baa807b4c2c843d14adf7b51481, call_41f0f744a2674ccea1f6581bd0763412]

## Uncertainty and limits

No conversion, model construction, filesystem integration or GPU execution was tested. The Python check transcribed only prefix selection and integer division.

The intended semantics of the tied_word_embeddings update and downstream consumers of the new sidecar were not established.
