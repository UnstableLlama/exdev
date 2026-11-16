# 475dfcca479d4333d69e759f96d50045663cf69b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/475dfcca479d4333d69e759f96d50045663cf69b) · [Evidence ledger](draft.json)

Extends comparison storage accounting to TritonV2 and ExllamaV2 GPTQ layers and adds an AutoRound example; existing evaluation finalization and cache-clear defects remain.

- [Additional GPTQ storage accounting](#usage-evaluation)

## Problem

The Transformers comparison adapter explicitly accounted for Marlin GPTQ layers but lacked branches for TritonV2 and ExllamaV2 layer storage. [source; call_f0626223df034028ac7898b7f0abf76e, call_6a8d5adebc724d22b43e07ec8f60e83f]

## Reasoning

The change extends storage accounting rather than selecting a new inference backend: backend-specific tensor collections feed the existing bits-per-weight calculation. [source; call_6a8d5adebc724d22b43e07ec8f60e83f, call_f0626223df034028ac7898b7f0abf76e]

## Impact

Recognized layers now contribute both stored tensor bits and logical weight counts to the comparison results. A new AutoRound example selects the existing Transformers loader and forward adapter. [source; call_6a8d5adebc724d22b43e07ec8f60e83f, call_af26d93a570943a7b0ef5f88b5f5f536, call_d4447570ac0048a5b25373b2649bdd95]

## Source Notes

The earlier comparison entry records no-reference finalization and cache-invalidation defects. [ancestor; call_23a8b543ef6f48a8844196cdacb35965]

Issue #31, “TypeError with presence penalty,” concerns sampling arguments in TabbyAPI and reports recovery after TabbyAPI updates. Its shared term “types” does not establish a connection to this GPTQ accounting change. [inference; call_478945aa666a41e1b2b5d3aae10e5084, call_6a8d5adebc724d22b43e07ec8f60e83f]

<a id="usage-evaluation"></a>

## Additional GPTQ storage accounting

get_storage_info adds TritonV2QuantLinear accounting for g_idx, qweight, qzeros and scales. Unlike the existing Marlin branch, it does not request g_idx_sort_indices. ExllamaV2QuantLinear instead supplies its q_tensors dictionary directly. [source; call_6a8d5adebc724d22b43e07ec8f60e83f, call_f0626223df034028ac7898b7f0abf76e]

Both branches add in_features × out_features to the denominator. get_tensors_size sums element_size × numel for non-None dictionary values and multiplies by eight to convert bytes to bits. Thus the reported bitrate includes selected quantization metadata rather than merely the nominal weight precision. [source; call_6a8d5adebc724d22b43e07ec8f60e83f, call_f0626223df034028ac7898b7f0abf76e]

An illustrative scalar calculation for 128 × 128 logical weights, 2048 int32 packed words, 128 FP16 scales and 16 int32 zero entries gives 68,096 bits, or 4.15625 bits per weight. These are hypothetical inputs demonstrating metadata overhead, not a measured GPTQ layout. [execution; call_40b834b66dcb4aca8719d15314abf139]

The existing loader calls AutoModelForCausalLM.from_pretrained before collecting storage statistics. test_ppl uses the returned decoder bitrate, head bitrate and storage estimate for results; plotting selects decoder bitrate or the storage estimate converted by division by eight and 1024³. The added branches do not alter forward computation. [source; call_f0626223df034028ac7898b7f0abf76e, call_d4447570ac0048a5b25373b2649bdd95, call_6a8d5adebc724d22b43e07ec8f60e83f]

The new specification labels a local llama3.1-8b-instruct/autoround/4bit-asym directory “AutoRound 4bit asym” and selects transformers for loading and forwarding. That loader requests cuda:0 and torch.half by default. The specification itself neither implements AutoRound quantization nor establishes which GPTQ class the external loader constructs. [source; call_af26d93a570943a7b0ef5f88b5f5f536, call_d4447570ac0048a5b25373b2649bdd95, call_f0626223df034028ac7898b7f0abf76e]

The task leaves the previously reported no-reference and cache-clear paths unchanged. Consequently, the new example should not be interpreted as evidence that standalone uncached evaluation successfully returns results. [source; call_d4447570ac0048a5b25373b2649bdd95, call_be1df6c333a149848a78fef3fcc21ae6, call_af26d93a570943a7b0ef5f88b5f5f536, call_6a8d5adebc724d22b43e07ec8f60e83f]

## Authoring-time findings — pending review

### inherited-no-reference-finalization (suspected; defect)

Standalone use of the new example retains the existing no-reference finalization failure.

Trigger: An uncached evaluation using the AutoRound specification without another specification providing out_logits, assuming loading and nonempty-data inference succeed.

Expected: Return perplexity without requiring reference logits.

Actual: main passes None for logits_file; kl_div_count remains zero and test_ppl unconditionally divides zero by zero. collect_logits is also uninitialized on this path, although division fails first.

Locations: 475dfcca479d4333d69e759f96d50045663cf69b:eval/compare_q.py — test_ppl

Source evidence: call_d4447570ac0048a5b25373b2649bdd95, call_af26d93a570943a7b0ef5f88b5f5f536, call_315570058f42420e8afce7dab4bd7620

source_inspection: Whole-parent-tree search identifies main as the sole direct test_ppl caller. The task changes neither that call nor finalization. [call_315570058f42420e8afce7dab4bd7620, call_d4447570ac0048a5b25373b2649bdd95, call_6a8d5adebc724d22b43e07ec8f60e83f]. Limits: Reach is established for the repository CLI, not external callers.

scalar_transcription: Evaluating the transcribed zero-over-zero expression raised ZeroDivisionError. [call_40b834b66dcb4aca8719d15314abf139]. Limits: No model or evaluation function was executed.

### inherited-cache-invalidation-mismatch (suspected; defect)

The existing clear-cache argument mismatch persists.

Trigger: The comparison CLI requests --clear_cache for a result cached by the three-argument test_ppl call.

Expected: Remove the selected cached evaluation result.

Actual: main invalidates a key containing only data_spec and spec, whereas evaluation caches a key additionally containing logits_file.

Locations: 475dfcca479d4333d69e759f96d50045663cf69b:eval/compare_q.py — main

Source evidence: call_d4447570ac0048a5b25373b2649bdd95, call_be1df6c333a149848a78fef3fcc21ae6, call_315570058f42420e8afce7dab4bd7620

scalar_transcription: Transcribed JSON key construction produces unequal keys for two arguments and three arguments including None. [call_40b834b66dcb4aca8719d15314abf139]. Limits: No shelve database was opened; source inspection establishes the CLI call-site mismatch.

## Uncertainty and limits

No Transformers model, GPTQ implementation or GPU kernel was executed. External class inheritance, tensor layouts and installed-version compatibility remain unverified.

The storage result counts selected tensors, not measured peak VRAM or all inference allocations.

The AutoRound model directory is a local example path; its contents and availability were not established.

Scalar checks exercise transcribed arithmetic and cache-key construction, not repository evaluation.
