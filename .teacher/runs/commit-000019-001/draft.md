# c8b4bd5454414b046a38344f0aa41b6e1d80d54d


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c8b4bd5454414b046a38344f0aa41b6e1d80d54d) · [Evidence ledger](draft.json)

Lowercases Linear's EXL3 format identifier, but leaves its metadata consumer checking uppercase, causing EXL3-specific inventory fields to be omitted.

- [Lowercase format identifier and its metadata consumer](#modules)

## Problem

The change standardizes Linear.quant_format_id() from uppercase "EXL3" to lowercase "exl3", matching the spelling already written into quantization metadata. [source; call_f023e43de0614c9ba5ee62524831c956, call_54fd6c3e244c40d981276b469c31ac31]

## Reasoning

The producer changes, but its metadata consumer still compares against "EXL3". Consistent capitalization requires updating that comparison too; changing only the producer prevents the recognition branch from running. [source; call_f023e43de0614c9ba5ee62524831c956, call_54fd6c3e244c40d981276b469c31ac31]

## Impact

For recognized EXL3 linear leaves, generated metadata retains stored_tensors but omits quant_format and bits_per_weight. Both compilation and the standalone metadata utility call the affected generator. [source; call_f023e43de0614c9ba5ee62524831c956, call_54fd6c3e244c40d981276b469c31ac31, call_8555f726a1544005b41529cf7bcd2ea3, call_840e413e6f0a47ebbdcdb49f3b47a45f]

## Source Notes

The parent entry describes the newly introduced header-derived inventory and its per-leaf format and bit-width fields. [ancestor; call_fae02dbbfedf4438b012eff8ae291b48]

<a id="modules"></a>

## Lowercase format identifier and its metadata consumer

Linear.quant_format_id() classifies storage under the primary module key using trellis plus the su/suh and sv/svh alternatives. The patch changes only the successful return string; unrecognized storage still returns None, and weight-loading behavior is unchanged. [source; call_a595b5f026264531a798106b6b94205f, call_f023e43de0614c9ba5ee62524831c956]

create_quantization_config_json constructs a model without loading weights, visits leaf modules, records stored tensor headers, and uses quant_format_id() to decide whether to add EXL3-specific metadata. Its serialized quant_format value was already lowercase before this patch. [source; call_54fd6c3e244c40d981276b469c31ac31]

A scalar transcription with a synthetic trellis last dimension of 48 produced quant_format='exl3' and bits_per_weight=3 for the old identifier, but only stored_tensors for the new identifier. This checks the case-sensitive branch, not repository execution. [execution; call_6a5b5a972f60483999b95e6cf71938af]

## Authoring-time findings — pending review

### format-identifier-consumer-mismatch (suspected; defect)

The lowercase return value no longer matches the unchanged uppercase metadata discriminator.

Trigger: Generate quantization_config.json for a model containing a leaf Linear whose primary-key storage satisfies is_exl3_storage().

Expected: Preserve the leaf's quant_format='exl3' and header-derived bits_per_weight fields while standardizing the identifier.

Actual: The EXL3 branch is skipped, so those two fields are omitted while stored_tensors remains.

Locations: c8b4bd5454414b046a38344f0aa41b6e1d80d54d:exllamav3/modules/linear.py — Linear.quant_format_id, c8b4bd5454414b046a38344f0aa41b6e1d80d54d:exllamav3/conversion/quant_config.py — create_quantization_config_json

Source evidence: call_f023e43de0614c9ba5ee62524831c956, call_54fd6c3e244c40d981276b469c31ac31, call_ef7df9b0c87f45d19b15f096227517a2, call_98733ee6b2904dc1bd0fa518152ba499, call_8555f726a1544005b41529cf7bcd2ea3, call_840e413e6f0a47ebbdcdb49f3b47a45f

source_inspection: Parent-tree searches located the direct metadata consumer and its compilation and standalone-utility callers. The complete task diff changes only Linear's return string, leaving the uppercase comparison intact. [call_ef7df9b0c87f45d19b15f096227517a2, call_98733ee6b2904dc1bd0fa518152ba499, call_f023e43de0614c9ba5ee62524831c956, call_54fd6c3e244c40d981276b469c31ac31, call_8555f726a1544005b41529cf7bcd2ea3, call_840e413e6f0a47ebbdcdb49f3b47a45f]. Limits: Reach is established for these inspected repository call sites, not external or dynamically selected callers.

scalar_transcription: Ran a standard-library reproduction of the metadata branch with old and new identifier strings. [call_6a5b5a972f60483999b95e6cf71938af, call_54fd6c3e244c40d981276b469c31ac31]. Limits: Synthetic dictionary input; no repository model construction or file generation was executed.

## Uncertainty and limits

No model conversion, metadata utility, or GPU implementation was executed. The Python check transcribed only the consumer branch using synthetic header metadata.

External consumers of quant_format_id() were not established.
