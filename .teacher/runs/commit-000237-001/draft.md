# ab875ba73053b7b6581579300af8c3cb81677c99


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ab875ba73053b7b6581579300af8c3cb81677c99) · [Evidence ledger](draft.json)

Makes fresh GGUF storage estimates independent of embedding/head order and excludes normalization weights; existing cached estimates can remain stale.

- [Order-independent GGUF storage accounting](#usage-evaluation)

## Problem

GGUF accounting incorrectly counted token_embd.weight as decoder storage when output.weight appeared first. The change also excludes weights whose names end in norm.weight. [source; call_a7cb1b826645441a9516dfdfc179f7ac, call_7f681514ebf7453e81d7217e83529c87]

## Reasoning

Explicitly excluding the embedding from the aggregate removes its dependence on whether the head has already been found, while preserving embedding-as-head fallback when no output.weight exists. [source; call_a7cb1b826645441a9516dfdfc179f7ac, call_7f681514ebf7453e81d7217e83529c87]

## Impact

Fresh llama.cpp accounting changes decoder BPW and decoder-plus-head storage used by compare_q reporting and plots. It does not change model loading or inference; the reported storage is not measured runtime VRAM. [source; call_7f681514ebf7453e81d7217e83529c87, call_c17bebed103d409daad3a7f4ec56437b, call_a7cb1b826645441a9516dfdfc179f7ac]

## Source Notes

Read the initial usage-evaluation entry and the subsequent broader-weight-accounting entry. They establish the original embedding fallback and later .weight aggregation; the latter records both tensor-order sensitivity and stale disk-cache results. [ancestor; call_961eb2833e57413e9d97c58d5a303d8b, call_21da4d5462fb4cfbbdfe97939fc16d91]

Source comparison shows that this change removes the recorded embedding-order problem but carries over the unchanged storage-cache namespace and cache-hit bypass. [source; call_a7cb1b826645441a9516dfdfc179f7ac, call_50e3b6cda6984b589602e81a76f9baeb, call_7f681514ebf7453e81d7217e83529c87]

<a id="usage-evaluation"></a>

## Order-independent GGUF storage accounting

get_storage_info sums n_bytes × 8 and n_elements for eligible decoder weights, returning their ratio as element-weighted BPW. Eight converts bytes to bits. Head storage is accounted separately as head_numel × head_bpw; output.weight overrides an earlier embedding fallback. [source; call_7f681514ebf7453e81d7217e83529c87, call_a7cb1b826645441a9516dfdfc179f7ac]

Previously, an embedding encountered after a positive-BPW output head failed the head condition and entered the generic .weight branch. The new branch excludes it explicitly. Normalization-suffix exclusion is a separate accounting refinement: it removes those tensors from both numerator and denominator even when embedding order was already favorable. [source; call_a7cb1b826645441a9516dfdfc179f7ac, call_7f681514ebf7453e81d7217e83529c87]

A standard-library scalar transcription used embedding/head/projection/norm metadata of respectively 200/100/50/20 bytes and 100/100/100/10 elements. Before the change, swapping embedding and head changed storage from 1360 to 2960 bits. Afterward all 24 permutations returned (decoder BPW 4, head BPW 8, storage 1200 bits). Without an explicit head, the embedding still supplied head BPW 16 and total storage 2000 bits. [execution; call_e2359b8691f441a7995029af2e2cd7e1]

The direct caller is load_llamacpp; compare_q selects it through its llamacpp loader registry. test_ppl converts returned bits by dividing by 8 and 1024³, stores the result as vram_gb, and plotting selects that value or layer_bpw as its horizontal coordinate. The tuple interface remains unchanged. [source; call_e5b32cf5ec304c4da20ca481830b9f6b, call_a43913dd4f4d40ac88d6486ad74daf7e, call_7f681514ebf7453e81d7217e83529c87, call_c17bebed103d409daad3a7f4ec56437b]

## Authoring-time findings — pending review

### cached-accounting (suspected; defect)

Previously cached storage results can bypass this correction.

Trigger: The same model argument already has an entry under lcpp_get_storage_info from before the change.

Expected: Recomputed comparison results reflect the corrected embedding and normalization exclusions.

Actual: The unchanged decorator returns the stored tuple without executing the modified function. compare_q's clear-cache option invalidates test_ppl entries only, leaving the storage entry reusable.

Locations: ab875ba73053b7b6581579300af8c3cb81677c99:eval/compare_q_llamacpp.py — get_storage_info

Source evidence: call_a7cb1b826645441a9516dfdfc179f7ac, call_7f681514ebf7453e81d7217e83529c87, call_50e3b6cda6984b589602e81a76f9baeb, call_c17bebed103d409daad3a7f4ec56437b

source_inspection: Inspected argument-only cache keys, the cache-hit return, and CLI invalidation. Whole-tree caller searches locate load_llamacpp as the direct caller and compare_q's registry as the broader entry point. [call_e5b32cf5ec304c4da20ca481830b9f6b, call_a43913dd4f4d40ac88d6486ad74daf7e, call_50e3b6cda6984b589602e81a76f9baeb, call_c17bebed103d409daad3a7f4ec56437b]. Limits: No persistent cache was exercised. Fresh storage-cache keys run the corrected loop; this finding does not apply to every evaluation backend.

## Uncertainty and limits

Validation used synthetic metadata and a scalar transcription, not GGUFReader, real model files, llama.cpp inference or GPU allocation measurements.

The naming filter establishes exclusion only for the literal embedding name and norm.weight suffix; coverage of every GGUF architecture's naming conventions is unestablished.

Persistent cache and filesystem-library behavior were inspected but not executed.
