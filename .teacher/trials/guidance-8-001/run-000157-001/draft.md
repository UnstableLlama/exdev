# b728058b20789afd74bdc371428ff1b83bc0b0f2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/b728058b20789afd74bdc371428ff1b83bc0b0f2) · [Evidence ledger](draft.json)

Adds per-slice file-handle cleanup after conversion unload, supplementing the existing post-load close without changing quantization or serialization.

- [Close cached input files after each converted slice](#conversion)

## Problem

The change adds another cleanup boundary for conversion's cached input-file handles. The parent already closes the collection immediately after loading each module slice; this is additional cleanup, not the first. [source; call_77f306a96a9a480fa32387e3142cd7d6, call_1870475cec514df187a2f964793cd241]

## Reasoning

SafetensorsCollection.close() closes every cached native handle group and resets its entry to None, retaining tensor metadata so subsequent requests can reopen files. It requires new_tensors to be None. [source; call_4b7941003ac34ee4bd9721f5df95b271]

## Impact

Any handles open at the new boundary are released before saving the converted module. The diff does not alter quantization, output formats or checkpoint logic. [source; call_77f306a96a9a480fa32387e3142cd7d6, call_1870475cec514df187a2f964793cd241]

## Source Notes

The original conversion chapter establishes module-by-module calibration, quantization and artifact assembly. It also records an earlier double-prefixed output-path hazard. [ancestor; call_b624e5056b994571bf0f3e36e57ece3e]

That output-path hazard is absent from the inspected parent and remains absent after this one-line change: main passes qtensors/<module-key>.safetensors to save_tensor, which prefixes work_dir once; compile_model reads work_dir/qtensors. [source; call_1870475cec514df187a2f964793cd241, call_379a3873c82c44ca8bd6187d1c4bffcf, call_77f306a96a9a480fa32387e3142cd7d6]

Issue #33, “Error converting model,” is related by inference: its traceback reaches the same cached native loader and later reports “Too many open files.” However, that failure occurred during compile_model, whose separate qtensors collection already closes between modules in the parent. The discussion reports successful conversion before this task and later shifts to GLM inference/sampling; it is not verification of this patch. [inference; call_da5902a1ec2a451f921fb1471c10f311, call_d8409a6690a34bad82c88124708b72b2, call_379a3873c82c44ca8bd6187d1c4bffcf]

Other conversion-related discussions describe different failures: #8 an invalid reshape, #11 a bias datatype assertion, #16 a CUDA configuration error discussed as tokenizer truncation, PR #13 missing BOS handling, #34 Cholesky failure, and #38 a Nemotron tensor-size mismatch. Their connection here is only inferred from shared conversion call sites, not evidence that closing handles fixes them. [inference; call_26353ff12af1494a9cf8ff8235793470, call_d98fbe9908ef4975b7b3b1786f1b23c1, call_4399823a820049c8b0e97dc36c09f3d3, call_a2396d77fb404b76af0f8a9adfcf09b3, call_c5967ff1918647b6942e9c21e1502c3b, call_d5335a02373e4bebb3583f5a06943f6c]

PR #26, “Superior 3INST parameters,” discusses decoder parameters and model_diff evaluation, rather than handle cleanup; its mention of the inspected evaluation file does not establish a causal relationship to this task. [inference; call_c06c59cea71041c1958fba11f2f15623, call_422956cbeeb94874930e8ff9f058aec0]

<a id="conversion"></a>

## Close cached input files after each converted slice

main now calls config.stc.close() immediately after collecting converted tensors and unloading the module, inside the current_slice loop. Thus cleanup runs per slice, including unsliced modules, before the accumulated q_tensors dictionary is written. [source; call_77f306a96a9a480fa32387e3142cd7d6, call_1870475cec514df187a2f964793cd241]

The close occurs before set_new_tensors(q_tensors), satisfying close's no-override assertion. The later in-memory reload clears that override again. Cached file handles and retained converted tensors have separate lifetimes: close does not clear q_tensors or the collection's headers. [source; call_1870475cec514df187a2f964793cd241, call_4b7941003ac34ee4bd9721f5df95b271]

Native opening creates one FILE stream per loader thread for each cached file; native closing closes those streams and frees any corresponding pinned host buffers. Releasing this cache can reduce resource pressure, at the cost of reopening files if later requested. [inference; call_4b5f50ccb3bf4cf19c106a9283756673, call_4b7941003ac34ee4bd9721f5df95b271]

Existing callers use the same normal-completion pattern: model_diff closes after unload and after ending deferred loading; compile_model closes after collecting each module's tensors; Model.load_gen closes after loading; VariantSafetensorsCollection delegates to constituent collections. Conversion's existing post-load close also remains. The added call introduces neither deferred loading nor an exception-cleanup wrapper. [source; call_37ccae4050354061afc873f8b1f4b144, call_5be69cec2c3449c0a3693dcb4f0e7eca, call_379a3873c82c44ca8bd6187d1c4bffcf, call_df7601d240214133b9a5e4c29bbbd816, call_4b7941003ac34ee4bd9721f5df95b271, call_77f306a96a9a480fa32387e3142cd7d6]

## Uncertainty and limits

No conversion, native loader or filesystem-library behavior was executed. Handle-count reduction and successful conversion of extremely large models remain unmeasured.

The inspected flow already closes handles after loading. Which subsequent operation reopens handles before the new close, and therefore how often this addition does useful work, remains unestablished.

No useful scalar computation would establish this resource-lifetime effect; a synthetic handle model would not test the native loader.
