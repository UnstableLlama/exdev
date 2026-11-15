# 8d3477648f0a0e4ad7b305491244faa1a2e1dcb9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/8d3477648f0a0e4ad7b305491244faa1a2e1dcb9) · [Evidence ledger](draft.json)

Reuses pinned host buffers for deferred CUDA loads, reduces chunks to 2 MiB, and adds CLI metrics. Inspection also identifies stale metrics wrappers and a carried-over odd-element BF16 conversion gap.

- [Reusable pinned staging and loader metrics](#loading)

## Problem

Deferred CUDA loading already staged file data through host memory, but allocated and freed that staging buffer for every job. The change replaces this with reusable pinned buffers and expands loader accounting. [source; call_1f921a262abf4530a4c2dfa02321449a, call_95b49ebea2ec4608821f0c7bbd1e7879, call_8e31cd1d59b347a698a6c5dbd9d71753]

## Reasoning

Reusing pinned buffers plausibly reduces allocation and transfer overhead. Smaller jobs and largest-tensor-first ordering trade file-offset locality for different worker scheduling; neither a throughput improvement nor the author's precise tuning rationale is established. [inference; call_95b49ebea2ec4608821f0c7bbd1e7879, call_8e31cd1d59b347a698a6c5dbd9d71753]

## Impact

The new -lm/--load_metrics option prints collection metrics at the end of model initialization. The old SafetensorsCollection.get_metrics API is removed, while two inspected wrappers still call it. [source; call_c176979cd0734182b7ba4303db870ad0, call_8e31cd1d59b347a698a6c5dbd9d71753, call_d4081dced3134f3d9c2e3a3e558a7e12, call_18d8b7a353db44139da9f273f84286d4]

## Source Notes

The preceding entry describes the deferred-loading lifecycle and flags an odd-length CUDA BF16 conversion tail. Fresh inspection shows that conversion remains unchanged by this task. [ancestor; call_85b692f3924642cf8ed81a0c906b5b02]

PR #22, “OpenAI compatible API example,” proposes an API example and discusses cache options and chat formatting. Its relationship here is inferred only from its use of model_init and explicit reference to model_init.py; it does not establish the motivation for pinned staging. [inference; call_cc7da2612a1e4126bbe2b01834232d7a, call_dd0cff5d04554f72a519098c116ca7e3, call_c176979cd0734182b7ba4303db870ad0]

Issue #6, “No ROCm runtime is found, using ROCM_HOME='/usr',” reports an installation/import failure; issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure whose reporter describes a compiler-environment remedy. Their connection to this inspection is only inferred traceback overlap with models/model.py, not evidence of a loader defect or validation. [inference; call_4653536fee7d4ed188738d3e48c0b2ec, call_ccd2247c9bb64fdd863e5011764b04a5, call_18d8b7a353db44139da9f273f84286d4]

<a id="loading"></a>

## Reusable pinned staging and loader metrics

stloader_deferred_cuda now accepts max_chunk_size through its declaration and Python binding. The whole-parent-tree search finds one Python invocation, in end_deferred_load, and the diff updates it to supply MAX_DEFERRED_LOAD_CHUNK. [source; call_bb2158ebbb1d4da3b41e38a119476660, call_42f380fd887d4d748ac4fbfd78b2acb6, call_66901708f7614f119119a1c1e62d2b15, call_8e31cd1d59b347a698a6c5dbd9d71753]

Each active CUDA worker lazily allocates a cudaMallocHost buffer in a process-global array indexed by worker number. It reads a job into that buffer, selects the job's device, calls cudaMemcpyAsync, synchronizes the device, and optionally converts BF16 in place. Buffers survive jobs and deferred passes until stloader_close_file frees the corresponding slots. This remains host-staged I/O, not GPUDirect, and the retained per-job synchronization prevents interpreting the Async call alone as a fully overlapped pipeline. [source; call_95b49ebea2ec4608821f0c7bbd1e7879, call_1f921a262abf4530a4c2dfa02321449a]

Python still groups deferred records by CPU/CUDA and filename, but sorts tensors by decreasing byte size rather than file offset. make_workload emits contiguous jobs of at most 2 MiB instead of 8 MiB; workers retain strided job assignment. CPU jobs still read directly into destination storage. Temporary tensors still support transposition, padding and FP32-to-FP16 copies after the native load. [source; call_d4081dced3134f3d9c2e3a3e558a7e12, call_8e31cd1d59b347a698a6c5dbd9d71753, call_1f921a262abf4530a4c2dfa02321449a]

A standard-library scalar calculation gives 2,097,152 bytes per new chunk and 16,777,216 bytes for eight full staging buffers, versus 67,108,864 bytes for eight old maximum-size jobs. These are staging-buffer sizes, not total host or GPU memory measurements. [execution; call_53acfe44b35e41ae95931ad63816d94e, call_33875c03bc5848e686b5b7cd00deb479, call_8e31cd1d59b347a698a6c5dbd9d71753]

STCMetrics collects source bytes, accumulated timed intervals, deferred and direct tensor counts, deferred passes and generated chunks. Deferred bytes and tensors are counted when requests are queued, whereas chunks and flush time are counted during end_deferred_load. Thus these counters describe loader activity rather than independently verified completed disk traffic; abort_deferred_load clears requests without rolling back their earlier accounting. [source; call_8e31cd1d59b347a698a6c5dbd9d71753, call_4f1d73052e3243d387b71c24e0fdde88, call_d4081dced3134f3d9c2e3a3e558a7e12]

The printed bandwidth divides recorded bytes by 1024 cubed and accumulated time, so its displayed GB/s is numerically GiB/s. The eager native and Python alternatives remain available; only deferred CUDA jobs receive the new reusable pinned staging. [source; call_8e31cd1d59b347a698a6c5dbd9d71753, call_4f1d73052e3243d387b71c24e0fdde88, call_95b49ebea2ec4608821f0c7bbd1e7879]

## Authoring-time findings — pending review

### metrics-wrapper-compatibility (suspected; defect)

Removing SafetensorsCollection.get_metrics leaves existing metrics wrappers calling a missing method.

Trigger: Call Model.get_load_metrics with a SafetensorsCollection, or VariantSafetensorsCollection.get_metrics with at least one child collection.

Expected: Return the existing bytes, elapsed-time and bandwidth tuple.

Actual: The unchanged wrappers call stc.get_metrics(), which the task removes, leading to an attribute lookup failure rather than returning metrics.

Locations: 8d3477648f0a0e4ad7b305491244faa1a2e1dcb9:exllamav3/loader/safetensors.py — VariantSafetensorsCollection.get_metrics, 8d3477648f0a0e4ad7b305491244faa1a2e1dcb9:exllamav3/models/model.py — Model.get_load_metrics

Source evidence: call_8e31cd1d59b347a698a6c5dbd9d71753, call_d4081dced3134f3d9c2e3a3e558a7e12, call_18d8b7a353db44139da9f273f84286d4

source_inspection: Whole-parent-tree searches locate both remaining consumers. No in-tree caller of Model.get_load_metrics was found beyond its definition; the new CLI bypasses these wrappers and prints stc.metrics directly. [call_91e4af82ab1f4d2298a4e7f025236a8e, call_574b60503c8b478eb60f03e134985d32, call_c176979cd0734182b7ba4303db870ad0]. Limits: Not executed; external consumers and dynamic calls were not enumerated.

### inherited-bf16-odd-tail (suspected; defect)

The inherited pair-only CUDA BF16 conversion remains in the changed deferred-loading path.

Trigger: Deferred loading of an odd-element BF16 tensor to CUDA with allow_bf16 false.

Expected: Convert every source element to FP16 before consumption.

Actual: The helper passes floor(numel/2) pairs to its kernel, leaving the final odd element as BF16 bits in FP16 storage. The smaller even-sized chunk limit does not remove this tail.

Locations: 8d3477648f0a0e4ad7b305491244faa1a2e1dcb9:exllamav3/exllamav3_ext/stloader.cu — inplace_bf16_to_fp16_cuda

Source evidence: call_a8f73c298780442f9f7b2a62359f4114, call_95b49ebea2ec4608821f0c7bbd1e7879, call_4f1d73052e3243d387b71c24e0fdde88

source_inspection: The parent-tree search finds the direct native caller in stloader_deferred_cuda, reached from end_deferred_load. The complete task diff retains that call and does not modify the conversion kernel, so this observation is carried over rather than corrected. [call_3d714cc5b1be4ddcbab876077398e314, call_66901708f7614f119119a1c1e62d2b15, call_d4081dced3134f3d9c2e3a3e558a7e12, call_95b49ebea2ec4608821f0c7bbd1e7879]. Limits: Conditional reach through deferred CUDA conversion; no affected checkpoint or GPU execution demonstrated.

scalar_transcription: Python modeled 2 MiB chunking and pair coverage: element counts 1, 3 and 1,048,577 each leave one element uncovered; count 2 leaves none. [call_53acfe44b35e41ae95931ad63816d94e]. Limits: Integer coverage model only; it does not execute the repository kernel or establish zero-block launch behavior.

## Uncertainty and limits

No repository loader, native extension or CUDA kernel was executed. The scalar check establishes only bounded integer arithmetic, not allocation success, CUDA ordering or conversion precision.

Throughput, pinned-memory pressure and concurrent collection behavior were not measured. Buffer-size arithmetic assumes the supplied Python caller's fixed chunk limit.
