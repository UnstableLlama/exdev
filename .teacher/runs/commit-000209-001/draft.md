# 8ff65b874202176c1449e6a51998094ef60f94f0


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/8ff65b874202176c1449e6a51998094ef60f94f0) · [Evidence ledger](draft.json)

Adds batched, module-streamed reference-logit capture and explicit reference-file selection for comparison. The reader gains dense-tensor normalization, but the new producer has a suspected tuple/list serialization mismatch.

- [Capture reference logits one module at a time](#usage-evaluation)

## Problem

Reference-logit collection previously ran through the comparison evaluator's model loader. The change adds a separate module-at-a-time capture script and lets comparison consume an explicitly supplied reference file. [source; call_5e4b266cc8564e1a882bc988a688a299, call_d2edc90d19e3485d8c7ba61af23f33ef, call_bb06310d7daf455e9ac759b6d2258528]

## Reasoning

Streaming trades repeated module loading for reduced simultaneous weight residency. Batching bounds the activation workload per forward pass, but all captured logits still accumulate in CPU memory before serialization. [inference; call_bb06310d7daf455e9ac759b6d2258528]

The producer and consumer edits form one workflow: capture logits separately, pass their filename with --logits_file, and normalize a loaded dense tensor into single-row slices before the existing KLD loop. [source; call_d2edc90d19e3485d8c7ba61af23f33ef, call_bb06310d7daf455e9ac759b6d2258528, call_5e4b266cc8564e1a882bc988a688a299]

## Impact

The explicit filename bypasses automatic reference-directory creation, dataset-hash naming and reference-model reordering. It does not override test_ppl's existing rule that a specification containing out_logits is a producer rather than a consumer. [source; call_d2edc90d19e3485d8c7ba61af23f33ef, call_5e4b266cc8564e1a882bc988a688a299]

## Source Notes

Read the reference-logit introduction entry, its optional-finalization fix, and the prequantization diagnostic entry. They establish the existing persistence convention, repaired no-reference finalization, and an earlier module-streaming pattern. The diagnostic entry's regularize and histogram observations concern functions not copied into the new capture script. [ancestor; call_97f5af716ee547a8a1cfa1c3139e0e22, call_d8895f1fcc4d4bc6a24348f3f69f53bf, call_65c35669b409472c92773923759e279b]

Parent source plus the task diff retain the repaired collect_logits initialization, conditional KLD finalization and three-argument cache invalidation. The previously recorded masked-out reference-producer dependency remains in the automatic-filename branch. [source; call_5e4b266cc8564e1a882bc988a688a299, call_d2edc90d19e3485d8c7ba61af23f33ef]

PR #26, “Superior 3INST parameters,” is primarily a codebook proposal. Its discussion also reports large-reference-model memory constraints and describes compare_q's saved first-ten-row logits; turboderp explains that the ten-row cap limits huge output files. Its connection to this task is inferred from those matching evaluation mechanisms, not an explicit commit link. [inference; call_e31671762ca144e1998ebfc6e8fc5234, call_bb06310d7daf455e9ac759b6d2258528]

Other inspected reports concern distinct failures: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension imports; #33, “Error converting model,” covers file-opening failures and later GLM sampling diagnostics; #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concern quantization failures. Shared model, loader, evaluation or linear-module paths provide only inferred contextual connections, not evidence that this change fixes them. [inference; call_df5e9c9296f54ffc950519cfdd063a52, call_e7c1d178b7cb4273b2e7cd99a2d42518, call_cf665f15ce0348f4af0cad9a937f220e, call_d8651961d81c40689e7632e68897cebc, call_bb06310d7daf455e9ac759b6d2258528]

Closed reports #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” and #16, “RuntimeError: CUDA error: invalid configuration argument,” describe build, quantization-padding and tokenizer-related failures respectively. Their bodies do not establish a relationship to this streaming-capture change. [inference; call_77a0809315b24c48bd6f00a7b68a1768, call_3ee9332643014a379480bc5b35813ae4, call_9a7a1560e1d34415bb6e86487e465ef1, call_712a2a4a6db0497685dbe5b379e58073, call_bb06310d7daf455e9ac759b6d2258528]

<a id="usage-evaluation"></a>

## Capture reference logits one module at a time

compare_q_logits.py constructs a model without loading it wholesale, obtains token sequences through compare_q.get_test_data, takes the requested prefix of rows and splits that prefix into batches. Defaults are ten rows, five rows per batch and device index zero; model and output paths are required. The shared data helper obtains Wikitext-2 test text and uses the dataspec's tokenizer, sequence length and stride. [source; call_bb06310d7daf455e9ac759b6d2258528, call_5e4b266cc8564e1a882bc988a688a299]

For each batch, stream_forward carries state through model.modules. Each module is loaded inside a deferred-load interval, respecting prefer_cpu, then prepares and forwards the state with a fresh empty params dictionary. The module is unloaded and the tensor collection closed before advancing. The complete module sequence is loaded again for the next batch. [source; call_bb06310d7daf455e9ac759b6d2258528, call_3344e1e4ec704435829167b1232d8668, call_8755d451dad14dbb84ae53d00be699c6]

Existing model_diff and prequant_test callers use the same deferred-load/prepare/forward/unload pattern, additionally calling free_mem after unloading. Normal Model loading instead consults can_defer_load; autosplit also aborts deferred loading and handles out-of-memory retries. The new script has neither that capability check nor retry handling. Linear rejects deferred loading for sliced weights, and GatedMLP does so for multiple slices, so the streaming implementation should not be assumed equivalent to the general model loader. [source; call_339f0c323e8341f1ac6641fbe60d64f5, call_f89e70b4e5b64a09acf5aa1eada0ecb1, call_ab7e4992121a425f8b60d86c814a7a18, call_e6a2a919170c4bcaa2c4fdb2a36f098e, call_a9de608576514f299026b3b17243c07e, call_f6520043f444458f80e99e4cad9a1329, call_bb06310d7daf455e9ac759b6d2258528]

Completed batch logits are copied to CPU, concatenated along dimension zero and split into single-row pieces for saving. This preserves batch order but is not incremental disk streaming: the CPU batch list and concatenated result coexist during concatenation. A bounded arithmetic check gives two five-row batches when all ten default rows are available. [source; call_bb06310d7daf455e9ac759b6d2258528]

A standard-library run confirmed the default partition sizes [5, 5]. Executing the extracted save_tensor helper with a stubbed writer showed that a list becomes tensor.0/tensor.1 entries, whereas a tuple becomes one tensor entry whose value remains a tuple. [execution; call_6488aeb38b5f46d9aa91d4e5f2b80c7d]

The existing reader accepts either one tensor key or consecutively numbered tensor.N keys. The task leaves loaded lists alone and splits non-list tensors along dimension zero, retaining singleton batch dimensions for ref_logits[row]. The existing producer still supplies a list; the new producer supplies the split result directly, exposing a serialization-contract mismatch. [source; call_5e4b266cc8564e1a882bc988a688a299, call_d2edc90d19e3485d8c7ba61af23f33ef, call_bb06310d7daf455e9ac759b6d2258528, call_f984546e86804e6eaa37b80e447c66e5, call_7d48ee7748304c69a408e167ffb2de8c]

The comparison metric itself is unchanged: KLD uses only the first ten sequence rows, while perplexity uses every evaluation row. --kld selects the plotted metric, not whether reference comparison runs. Capturing more than ten rows therefore does not expand KLD coverage, and capturing fewer requires the consumer's evaluated prefix not to exceed the reference rows. [source; call_5e4b266cc8564e1a882bc988a688a299, call_d2edc90d19e3485d8c7ba61af23f33ef, call_bb06310d7daf455e9ac759b6d2258528]

## Authoring-time findings — pending review

### split-result-serialization (suspected; defect)

The new capture caller passes a split result to a serializer that recognizes lists but not tuples.

Trigger: Capture reaches save_tensor after successful forwarding, with Tensor.split returning a tuple of row tensors.

Expected: Write individually named row tensors, or write the concatenated tensor for the newly supported dense-reader path.

Actual: save_tensor falls through to save_file({'tensor': tuple}, filename), rather than constructing tensor.N entries. Successful serialization of reference tensors is therefore not established.

Locations: 8ff65b874202176c1449e6a51998094ef60f94f0:eval/compare_q_logits.py — main, 8ff65b874202176c1449e6a51998094ef60f94f0:eval/compare_q.py — save_tensor

Source evidence: call_bb06310d7daf455e9ac759b6d2258528, call_5e4b266cc8564e1a882bc988a688a299, call_f984546e86804e6eaa37b80e447c66e5

source_inspection: Whole-parent-tree search found the comparison helper's existing caller in test_ppl, which builds a list. The new main passes the split result without conversion. Conversion-module helpers with the same name are separate definitions. [call_f984546e86804e6eaa37b80e447c66e5, call_5e4b266cc8564e1a882bc988a688a299, call_bb06310d7daf455e9ac759b6d2258528]. Limits: PyTorch's version-specific return contract and safetensors rejection were not executed or independently documented.

repository_execution: Executed the AST-extracted parent save_tensor function with list and tuple inputs and a stub writer; the tuple was passed as a single value. [call_6488aeb38b5f46d9aa91d4e5f2b80c7d]. Limits: Only repository Python dispatch ran; no tensors, PyTorch split, file writing or GPU code ran.

### inherited-filtered-reference (suspected; defect)

Automatic reference selection still permits masking out the producer while retaining consumers.

Trigger: Without --logits_file, a mask excludes the selected out_logits producer, an uncached consumer remains, and its reference file does not exist.

Expected: Generate the reference or reject the missing dependency before evaluating the consumer.

Actual: main retains the selected filename after filtering; test_ppl loads the candidate model and then attempts to open that absent reference.

Locations: 8ff65b874202176c1449e6a51998094ef60f94f0:eval/compare_q.py — main

Source evidence: call_5e4b266cc8564e1a882bc988a688a299, call_d2edc90d19e3485d8c7ba61af23f33ef, call_344c6eacbf6c431f8f99e7c976b477f7

source_inspection: Compared automatic filename discovery, mask filtering and test_ppl loading against the diff. Whole-parent-tree search found main as the sole direct test_ppl caller. [call_5e4b266cc8564e1a882bc988a688a299, call_d2edc90d19e3485d8c7ba61af23f33ef, call_344c6eacbf6c431f8f99e7c976b477f7]. Limits: Existing files or cached results avoid this trigger. Filesystem behavior and external caller reach were not tested.

## Uncertainty and limits

No model inference, CUDA execution, memory measurement or safetensors round trip was performed.

The serializer check executed the extracted repository helper with a stubbed save_file. It establishes Python dispatch for tuple input, not the installed PyTorch split return type or safetensors exception behavior; eligible version documentation was not supplied.

Compatibility of arbitrary model-specific input preparation, sliced modules and alternative tensor collections with this direct streaming loop is not established.

The fixed dynamic-sequence setting of 2048 is not validated against the dataspec's eval_len. Reference token ordering, vocabulary compatibility and sufficient row count remain user responsibilities in the inspected workflow.

The new output path is passed directly to save_tensor without creating its parent directory. Filesystem-library behavior was not executed.
