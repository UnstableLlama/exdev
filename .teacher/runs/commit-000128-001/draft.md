# 4710c012a51fcadbee12be0f3fd6cf64ade2a60b


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4710c012a51fcadbee12be0f3fd6cf64ade2a60b) · [Evidence ledger](draft.json)

Closes cached Safetensors handles after each conversion module load and each compilation module read, reducing resource retention while preserving loaded tensors and reusable collection metadata.

- [Release source handles after module reads](#conversion)

## Problem

Conversion and output compilation retained cached native Safetensors handles across successive module reads. The loader opens multiple FILE handles per source file, so retaining collections also retains those resources. [source; call_7b8de244ee09423b95bf1b302c9ac837, call_933eeb714bb34bea8a4d91461046c8d6, call_0498094546444074b5b3a5ccdd87a4af, call_5f8b44d623154ae58c17f8453601b228]

## Reasoning

Release file resources at module boundaries rather than discard the collection: close() clears cached handles but preserves headers and tensor-to-file mappings, allowing later reads to reopen files. [source; call_0498094546444074b5b3a5ccdd87a4af, call_2be3140ea9e543d8ac27dcb13a68adad, call_b19622f5119d49d8b137ec72796e28ca]

## Impact

This should reduce accumulated open-file pressure, at the cost of reopening files shared by successive modules. It does not change quantization calculations or output shard allocation. [inference; call_2be3140ea9e543d8ac27dcb13a68adad, call_b19622f5119d49d8b137ec72796e28ca, call_0498094546444074b5b3a5ccdd87a4af]

## Source Notes

Issue #33, “Error converting model,” reports compilation failing at qtensors_stc.get_tensors with “Too many open files (errno=24).” Its connection to this change is inferred from that exact matching call site and the new adjacent close(); the supplied discussion does not explicitly link the commit. [inference; call_7d0d9ce9b1464f1e8639e49d749a4e68, call_0db0016c539e4ee59037117267607841, call_2be3140ea9e543d8ac27dcb13a68adad]

Issue #34, “torch._C._LinAlgError on last layer of quant,” concerns Cholesky factorization during quantization. Issue #21, “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022,” concerns extension compilation and was closed without a reported solution. Neither discussion establishes a file-handle failure addressed by this patch. [source; call_7a77b86ef10f415dba5cf4f208110851, call_1f05be5fc2d940dd828ed7fbedeb7e86]

<a id="conversion"></a>

## Release source handles after module reads

In conversion main(), the new module.config.stc.close() runs after loading each unquantized module or slice and reporting alternate-key clones, before calibration capture and quantization. It therefore also runs for modules without quantization targets. [source; call_b19622f5119d49d8b137ec72796e28ca, call_7b8de244ee09423b95bf1b302c9ac837]

In compile_model(), each module's tensors are read from the working qtensors collection, made contiguous and retained in file_dict before the collection is closed. The shard is saved afterward: closing handles does not clear the tensors accumulated for serialization. [source; call_2be3140ea9e543d8ac27dcb13a68adad, call_933eeb714bb34bea8a4d91461046c8d6, call_0498094546444074b5b3a5ccdd87a4af]

The default immediate native loader reads into allocated tensor storage rather than a file-backed mapping. Its close routine calls fclose on every cached native handle and also frees existing pinned staging buffers. The Python loading alternative already scopes each file with a context manager. [source; call_0498094546444074b5b3a5ccdd87a4af, call_5f8b44d623154ae58c17f8453601b228]

The additions are normal-path cleanup points, not try/finally guards. They shorten retention between successful module reads without adding exception-path cleanup. [source; call_2be3140ea9e543d8ac27dcb13a68adad, call_b19622f5119d49d8b137ec72796e28ca]

## Uncertainty and limits

No conversion, native-loader execution, descriptor-count measurement or performance test was run. Successful completion of the reported failing job is unverified.

The change concerns resource lifetime rather than numerical arithmetic; a standalone scalar computation would not establish native file closure or runtime resource limits.
