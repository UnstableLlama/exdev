# b728058b20789afd74bdc371428ff1b83bc0b0f2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b728058b20789afd74bdc371428ff1b83bc0b0f2) · [Evidence ledger](draft.json)

Adds collection cleanup after each conversion slice is unloaded, releasing any cached input-file handles before output tensors are saved.

- [Close cached input handles after each conversion slice](#conversion)

## Problem

The change addresses retained file handles during conversion by adding a second collection-close boundary; conversion already closed the module's collection immediately after loading unquantized weights. [source; call_daee5cff2fe84c0b83dc36c477204dde, call_30a783a8b37e4c3981b68104e7240221]

## Reasoning

SafetensorsCollection caches native handle lists by filename. close() closes populated entries and resets them to None while preserving tensor metadata, allowing later get_tensor calls to reopen files. [source; call_89c7e5de464049cda3c10c41bb725c9e]

## Impact

The additional cleanup releases any handles present after tensor collection and module unloading. Its incremental benefit depends on handles having reopened since the existing post-load close; no measured reduction is established. [inference; call_daee5cff2fe84c0b83dc36c477204dde, call_30a783a8b37e4c3981b68104e7240221, call_89c7e5de464049cda3c10c41bb725c9e]

## Source Notes

Issue #33, “Error converting model,” includes a “Too many open files (errno=24)” traceback through compile_model and the safetensors loader, followed by a May 7 report of successful conversion and later discussion of a separate GLM sampling problem. Its relationship to this change is inferred from the shared loader and handle-pressure symptom, not an explicit reference to this commit. [inference; call_5109056be91f4e58b6efcb801b9e17d8, call_f563a46f3cd246ab9e91b5edd414f748, call_daee5cff2fe84c0b83dc36c477204dde]

Other matching discussions concern different failures: #8 reports an invalid reshape, #11 an incorrect bias datatype, #16 an invalid CUDA configuration, and PR #13 missing BOS-token handling. Their connection here is inferred only from conversion-path overlap, not evidence that this handle cleanup fixes those failures. [inference; call_853df6c6e18c4fa690b3c2c03f396252, call_0d3b4ae42291418cb87dba2b5431aa17, call_1c8747a6a76648e2adb6011fbb2bd446, call_57c71c91e5994187969a8c8f19969397, call_daee5cff2fe84c0b83dc36c477204dde]

Issue #34, “torch._C._LinAlgError on last layer of quant,” reports Cholesky failure; #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports incompatible tensor dimensions during loading. Their inferred connection is the shared convert_model.py path; neither report establishes a handle-exhaustion failure addressed by this line. [inference; call_24c8a3e2eb824ff68519c9037d8fc8e0, call_dc1ac9590a4f4e82b87e4e66611e9369, call_daee5cff2fe84c0b83dc36c477204dde]

<a id="conversion"></a>

## Close cached input handles after each conversion slice

main now calls config.stc.close() immediately after module.unload() inside the current_slice loop. Thus cleanup occurs per slice, including the single-slice case, before saving the module's accumulated q_tensors. [source; call_daee5cff2fe84c0b83dc36c477204dde, call_30a783a8b37e4c3981b68104e7240221]

The close targets input-loader resources rather than the collected output dictionary. After saving, the existing code exposes q_tensors through set_new_tensors, reloads the module from memory, clears that override and advances calibration state. close() requires new_tensors to be None; the added call precedes this override. [source; call_30a783a8b37e4c3981b68104e7240221, call_89c7e5de464049cda3c10c41bb725c9e, call_daee5cff2fe84c0b83dc36c477204dde]

Native stloader_open_file opens a FILE stream for each loader thread. stloader_close_file closes every stream in the supplied list and frees allocated host staging buffers. The Python collection then marks the filename's cached handles absent. [source; call_4cd3a1718e984ffc851bcc2b223019fa, call_89c7e5de464049cda3c10c41bb725c9e]

This favors prompt resource release over retaining handles for possible reuse. Later file-backed reads can reopen them, whereas an already-empty handle cache makes the added close perform no native closes. The insertion is normal-path cleanup, not a finally block or a change to quantization mathematics. [source; call_daee5cff2fe84c0b83dc36c477204dde, call_89c7e5de464049cda3c10c41bb725c9e, call_30a783a8b37e4c3981b68104e7240221]

## Uncertainty and limits

No conversion or native-loader execution was performed. Handle counts, platform limits and performance effects remain unmeasured.

No concrete reopening path between the existing post-load close and the new close was established.

A scalar computation would not validate this resource-lifetime change; meaningful verification requires observing actual file handles during conversion.
