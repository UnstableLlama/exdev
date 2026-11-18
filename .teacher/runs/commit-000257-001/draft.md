# 32d98c24c140549c879e6e4db71b27077b9e1975


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/32d98c24c140549c879e6e4db71b27077b9e1975) · [Evidence ledger](draft.json)

Adds custom-install QTIP evaluation dispatch, storage accounting and Llama HYB/YAQA specifications; the new 70B specification has invalid trailing-comma JSON.

- [QTIP comparison adapter](#usage-evaluation)

## Problem

The comparison runner lacked a QTIP backend. This change adds a custom-install adapter and Llama-3.1 comparison specifications. [source; call_2f2ed83e9b0241e48ced0213fa736a94, call_4c76296ac24d41a68685b195b21ed11e]

## Reasoning

Registering both loading and forwarding lets QTIP reuse the existing tokenization, perplexity and reference-logit comparison pipeline rather than introducing a separate evaluator. [source; call_b8eaeed722e34ed19ec8d50a4f7bf507, call_2f2ed83e9b0241e48ced0213fa736a94]

## Impact

Adds 2-, 3- and 4-bit HYB specifications for 8B and HYB-YAQA specifications for 70B, using local artifact paths, and colors QTIP plot labels teal. The 70B specification contains a trailing comma that prevents its JSON loading. [source; call_a3b121e954b2444295913621dfb5b761, call_2034e288a3854068b2fe0acbded1f547, call_2f2ed83e9b0241e48ced0213fa736a94, call_b8eaeed722e34ed19ec8d50a4f7bf507]

## Source Notes

Read the root usage-evaluation entry and the AnyPrecision adapter entry. They establish the inherited four-value loader contract, logits-returning forward interface and distinction between tensor-storage accounting and measured VRAM. [ancestor; call_9951b3d718e741d48ef49c6305db6c98, call_d01ef4c61e904f11944b54658d890844]

The AnyPrecision entry recorded an unconditional external-import requirement. Parent source now catches ModuleNotFoundError in that adapter, and this task leaves that handling unchanged; the recorded import failure is therefore not carried over in that form. [source; call_59a649775b764b9ea24382974d548c80, call_2f2ed83e9b0241e48ced0213fa736a94]

Issue #49, “running the QTIP inference code,” offers installation guidance and contains turboderp's report of running HYB/YAQA comparisons. Its relationship to this change is inferred from QTIP, HYB, YAQA and Llama-3.1-70B matches, not an explicit commit link. The discussion also questions the reported comparison results; those reports are not measurements reproduced here. [inference; call_8d77a89bc30a4fae8d621f68162ff0b9, call_a3b121e954b2444295913621dfb5b761, call_2034e288a3854068b2fe0acbded1f547]

The inspected opening of PR #26, “Superior 3INST parameters,” proposes codebook-parameter changes. Its connection is only inferred from shared comparison tooling and Llama evaluation context; this task does not implement that proposal. [inference; call_20c67b60f0754658920851da216fde22, call_2f2ed83e9b0241e48ced0213fa736a94, call_4c76296ac24d41a68685b195b21ed11e]

<a id="usage-evaluation"></a>

## QTIP comparison adapter

load_qtip calls model_from_hf_path(model_dir, max_mem_ratio=0.7), discards model_str, computes storage metadata and returns model, decoder BPW, head BPW and storage bits. Its auto and bf16 arguments are unused. fwd_qtip moves input IDs to cuda:0, calls the model and returns output.logits. Both functions disable compiler capture and use inference mode. [source; call_4c76296ac24d41a68685b195b21ed11e]

The runner consumes that tuple and logits without a new tokenizer: test_ppl obtains shared dataset IDs, selects both functions by specification keys, computes next-token likelihood and optionally compares reference logits. The new specifications require both registry additions; labels describe artifacts but do not configure their precision. [source; call_b8eaeed722e34ed19ec8d50a4f7bf507, call_2f2ed83e9b0241e48ced0213fa736a94, call_a3b121e954b2444295913621dfb5b761, call_2034e288a3854068b2fe0acbded1f547]

get_storage_info counts ordinary Linear weights first. Width at least 0.9 × model.vocab_size identifies a presumed head; otherwise the weight contributes to decoder storage. QuantizedLinear accounting sums SU, SV, tlut and trellis bytes, excluding None values, and divides their bits by logical in_features × out_features. The 90% cutoff is a width heuristic, not a structural head lookup. [source; call_4c76296ac24d41a68685b195b21ed11e]

Multiplication by eight converts bytes to bits. The reported total includes counted decoder tensors and the last identified head, not embeddings, normalization, biases or runtime allocations. The runner divides by eight and 1024³, so its GB-labelled value uses GiB-sized units. [source; call_4c76296ac24d41a68685b195b21ed11e, call_b8eaeed722e34ed19ec8d50a4f7bf507]

An illustrative scalar calculation with 262,144 packed bytes plus 8,192 overhead bytes for 1,048,576 logical weights yields 2.0625 BPW. Thus this accounting can exceed nominal artifact bitrate. [execution; call_82af8146dd5d460287ce910a97f7e805]

The wrapper closely follows AnyPrecision's size helpers and cuda:0 forwarding pattern, but delegates loading to QTIP. Its optional imports catch ModuleNotFoundError; there is no explicit availability check before load_qtip uses model_from_hf_path. [source; call_59a649775b764b9ea24382974d548c80, call_4c76296ac24d41a68685b195b21ed11e]

## Authoring-time findings — pending review

### invalid-70b-qtip-spec (suspected; defect)

The new 70B model specification is not valid JSON because its final array element has a trailing comma.

Trigger: Select eval/spec/llama3.1-70b-instruct_qtip.json directly or through a modelspec wildcard.

Expected: main loads three QTIP model specifications and proceeds to evaluation.

Actual: main passes the file to json.load before model filtering or evaluation; the trailing comma causes JSONDecodeError and stops that invocation, including other specifications selected with it.

Locations: 32d98c24c140549c879e6e4db71b27077b9e1975:eval/spec/llama3.1-70b-instruct_qtip.json — final array element, 32d98c24c140549c879e6e4db71b27077b9e1975:eval/compare_q.py — main

Source evidence: call_a3b121e954b2444295913621dfb5b761, call_b8eaeed722e34ed19ec8d50a4f7bf507, call_cbb0b454f3bd4041a7998017c2451e8b

source_inspection: Inspected the added file and main's unconditional json.load loop. Whole-parent-tree compare_q search located its evaluation-script import and documentation reference; the demonstrated trigger is main's modelspec-loading path. [call_a3b121e954b2444295913621dfb5b761, call_b8eaeed722e34ed19ec8d50a4f7bf507, call_cbb0b454f3bd4041a7998017c2451e8b]. Limits: No full evaluation invocation was executed.

scalar_transcription: Reconstructed the three-entry arrays with their respective closing punctuation and parsed them using standard-library json: 70B failed with JSONDecodeError; 8B parsed three entries. [call_82af8146dd5d460287ce910a97f7e805]. Limits: Checks transcribed JSON structure, not direct task-tree file execution.

## Uncertainty and limits

No QTIP installation, model loading, GPU forwarding or quality evaluation was executed. The adapter explicitly targets a custom package installation and says it supports only Llama.

The external model_from_hf_path implementation, QuantizedLinear inheritance, model.vocab_size attribute and storage tensor availability were not verified. The meaning and enforcement of max_mem_ratio=0.7 remain external implementation details.

The scalar check models JSON construction and illustrative storage arithmetic; it does not execute repository inference or measure checkpoint storage.

Only the opening portion of the lengthy PR #26 discussion was inspected.
