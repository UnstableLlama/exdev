# f02c9afd6afa617983f72cb7f79fcf35667e573b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/f02c9afd6afa617983f72cb7f79fcf35667e573b) · [Evidence ledger](draft.json)

Wraps captured logit splits in a list so the existing serializer writes numbered row tensors instead of treating the collection as one tensor value.

- [Adapt captured logit rows to the serializer](#usage-evaluation)

## Problem

The capture script passed its split result directly to save_tensor, whose multi-tensor branch accepts lists, not tuples. Tuple input instead reaches the single-value writer branch. [source; call_9f4a4c36bdb5421a9f4fd042af578c74, call_1ad62a17268843668cf4e8f5ece891d8]

## Reasoning

Converting the split result to a list adapts the producer to the existing serializer contract without broadening the shared helper's accepted containers. [source; call_9f4a4c36bdb5421a9f4fd042af578c74, call_1ad62a17268843668cf4e8f5ece891d8]

## Impact

Captured rows now select the tensor.0, tensor.1, … serialization branch, matching the existing reader and the comparison evaluator's list-based producer. [source; call_9f4a4c36bdb5421a9f4fd042af578c74, call_1ad62a17268843668cf4e8f5ece891d8]

## Source Notes

The introduction entry records the split-result serialization mismatch. This task removes that specific mismatch by explicitly constructing a list. [ancestor; call_7eac4314860e4797ac7a873932e05938]

PR #26, “Superior 3INST parameters,” proposes codebook changes and also discusses saved reference logits and their file-size limits. Its contextual connection is inference based on the matching compare_q reference-logit workflow, not an established link to this fix. [inference; call_023cbd75d8844f24b82f03681e9df716, call_46eb9e46ec3241bcb18e94a2a93bc413, call_1ad62a17268843668cf4e8f5ece891d8]

<a id="usage-evaluation"></a>

## Adapt captured logit rows to the serializer

main still collects CPU batch logits, concatenates them on dimension 0, then splits with size 1 on dimension 0. Here 1 means one sequence row per saved tensor, retaining the singleton batch dimension; the change wraps only that split result in list(). [source; call_1e28a580e183447f8da5c83db745c485, call_9f4a4c36bdb5421a9f4fd042af578c74]

save_tensor distinguishes dictionaries, lists and everything else. Lists become consecutively numbered tensor.N entries; other inputs become a single tensor value. load_tensor reconstructs numbered entries as a list, and test_ppl indexes that list by evaluation row. Its existing producer already builds a list, so it needs no corresponding change. [source; call_1ad62a17268843668cf4e8f5ece891d8, call_b1b2c52cfea34f6cac6b5b02c1850c8e, call_e77155b1a01249bc99178a5ba0e073af]

Executing the AST-extracted repository save_tensor helper with a stub save_file confirmed that a two-object tuple takes the single tensor branch, while list(tuple) produces tensor.0 and tensor.1 containing the same objects in order. No tensor library or file writer ran. [execution; call_fb97f015f7f047a3a670db3b450f29fc]

The fix remains local to the capture caller rather than changing shared dispatch. Saving the concatenated dense tensor would also fit the inspected reader, which splits non-list references into singleton rows, but that alternative is not implemented. [source; call_9f4a4c36bdb5421a9f4fd042af578c74, call_1ad62a17268843668cf4e8f5ece891d8]

## Uncertainty and limits

No PyTorch split operation, model inference or safetensors round trip was executed. The installed split return contract and exact writer rejection behavior were not independently verified.

The dispatch check used ordinary Python objects and a stub writer; it establishes container routing and reference preservation, not tensor contiguity, storage compatibility or successful filesystem output.
