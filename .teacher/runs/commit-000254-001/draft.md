# f6e2de2a7cfd1c6f1ca73cdeb2a42266b334c513


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f6e2de2a7cfd1c6f1ca73cdeb2a42266b334c513) · [Evidence ledger](draft.json)

Adds a header-only CLI utility for rebuilding safetensors indexes, with single-file opt-in and overwrite behavior; inherited tensor-name normalization creates a potential external compatibility mismatch.

- [Reconstructing an index from existing weight headers](#safetensors-index)

## Problem

Adds a standalone utility to reconstruct model.safetensors.index.json from existing weight files, addressing the missing-index use case named in the commit message. [source; call_d3c10d6af7c447b9ac8476d67277a752]

## Reasoning

Reusing SafetensorsCollection avoids loading tensor payloads: its constructor scans headers and supplies the tensor-to-file map and byte offsets needed by the exporter. [source; call_d3c10d6af7c447b9ac8476d67277a752, call_515426ffe3764d6f8bb7bf80b6798da0]

## Impact

The utility creates or overwrites the index without rewriting weights. Existing ExLlamaV3 loading still scans safetensors files directly rather than reading this index. [source; call_d3c10d6af7c447b9ac8476d67277a752, call_515426ffe3764d6f8bb7bf80b6798da0, call_f946a6ebbf2343aa8022f817fafd9de8, call_dba10fe2bc22446dbfbac38808c18216]

## Source Notes

The root loading-tokenization entry was read. It establishes the inherited direct-header scanning design and notes limited header validation. The task leaves that parser unchanged and does not add payload-bound or overlapping-offset validation. [ancestor; call_470a66c0fdfb45fa998bfaaa2d9e8314]

Issue #33, “Error converting model,” concerns native file-opening failures and subsequently GLM4 inference; issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports extension import failure. Their relationship here is only inferred from shared loader/configuration paths; neither establishes missing indexes as its cause or this utility as its fix. [inference; call_6c041fb37a174e948464c606e0f0bb74, call_331d1123b3384e70a5226072bbdf533a, call_ff19b0bb20d746d58702e432ef0135c7, call_d3c10d6af7c447b9ac8476d67277a752]

<a id="safetensors-index"></a>

## Reconstructing an index from existing weight headers

Run util/add_safetensors_index.py with required -m/--model_dir. With zero files it returns without writing; with one file it also returns unless -f/--force is supplied. Force overrides only the single-file skip, not the zero-file case. [source; call_d3c10d6af7c447b9ac8476d67277a752]

SafetensorsCollection scans only the directory’s *.safetensors matches. It excludes __metadata__ and its synthetic _header_offset from tensor_file_map, and later scanned files replace duplicate tensor names. The exporter therefore indexes the collection’s selected tensor entries, not every occurrence of a duplicate. [source; call_515426ffe3764d6f8bb7bf80b6798da0, call_d3c10d6af7c447b9ac8476d67277a752]

For each selected tensor, main records the shard basename in weight_map and adds data_offsets[1] minus data_offsets[0] to metadata.total_size. This is selected tensor payload bytes, excluding header bytes, rather than total filesystem size. The JSON is indented by four spaces and written directly into the supplied model directory; an existing index is overwritten without requiring force. [source; call_d3c10d6af7c447b9ac8476d67277a752, call_515426ffe3764d6f8bb7bf80b6798da0]

The output schema and single-shard default follow compile_model’s existing index writer. Unlike compilation, the utility reconstructs metadata from existing headers rather than materializing and saving tensors. Existing collection callers in compile_model, Config.__init__ and VariantSafetensorsCollection prepare directory paths without a mandatory pre-scan existence guard; the utility similarly relies on scanning, then handles an empty collection explicitly. It never calls get_tensor, so compile_model’s explicit close after payload reads is unnecessary for this header-only path. [source; call_bfe3eb0d99a645a19c09e99ef3ede881, call_db8ba62abb934aafaea0147e18cf0c81, call_515426ffe3764d6f8bb7bf80b6798da0, call_59ad8b53ceb6432fa07df43eb4c8efe8, call_d3c10d6af7c447b9ac8476d67277a752]

A bounded standard-library transcription mapped two synthetic tensors to shard basenames and summed 8 and 12 payload bytes to 20. It also demonstrated that the loader’s normalized projector name can be absent from the original header. This checks the exporter’s arithmetic and naming consequence, not repository execution. [execution; call_384d500650b343df9d345a6e10144f6e]

## Authoring-time findings — pending review

### normalized-index-key (suspected; external_compatibility)

The exporter can publish a normalized tensor name that does not exist in the unchanged shard header.

Trigger: A scanned shard contains multi_modal_projector.mm_input_projection_weight, and export proceeds with multiple shards or --force.

Expected: An index intended to identify stored tensors should preserve the name present in the referenced shard.

Actual: read_header renames that key to multi_modal_projector.mm_input_projection.weight in memory; main exports the renamed key without rewriting the shard. A consumer requiring exact stored names would not find it. No external consumer failure was executed.

Locations: f6e2de2a7cfd1c6f1ca73cdeb2a42266b334c513:util/add_safetensors_index.py — main, 4ab2b253533b19e461a01ce7b74957ae9834d557:exllamav3/loader/safetensors.py — read_header

Source evidence: call_d3c10d6af7c447b9ac8476d67277a752, call_515426ffe3764d6f8bb7bf80b6798da0, call_fb359c8f4c7648c091cdf69d3c19923b

source_inspection: Traced normalization through collection construction into the new exporter. Whole-parent search found no existing references to add_safetensors_index; the task supplies its direct CLI call to main. The observation applies to exports containing the alias, not every model or existing loading workflow. [call_d3c10d6af7c447b9ac8476d67277a752, call_515426ffe3764d6f8bb7bf80b6798da0, call_fb359c8f4c7648c091cdf69d3c19923b]. Limits: External reader behavior was not executed.

scalar_transcription: Modeled the inspected rename and checked that the exported name is absent from a synthetic raw header. [call_384d500650b343df9d345a6e10144f6e]. Limits: Synthetic dictionary check, not a real checkpoint or loader run.

## Uncertainty and limits

No repository utility execution, real checkpoint export or external index-consumer test was performed. The successful Python check transcribes dictionary and offset arithmetic only.

Header parsing inherits limited validation; successful index generation does not establish that tensor payloads are readable or valid.

External consumer compatibility, filesystem failure recovery and atomicity were not tested.
