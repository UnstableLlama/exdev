# 48ade457da80541cf28887c9fb1e7c7ad662e758


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/48ade457da80541cf28887c9fb1e7c7ad662e758) · [Evidence ledger](draft.json)

Keeps list_gpu_tensors scanning after PydanticUserError interrupts attribute traversal. The new eager exception import also makes Pydantic availability a prerequisite for importing unrelated memory helpers.

- [Continue tensor diagnostics after a Pydantic attribute error](#runtime)

## Problem

The commit is titled “util: Fix regression.” In the parent, if inspecting an object's __dict__ raises PydanticUserError during list_gpu_tensors, the exception escapes and stops the scan before it prints its tables. The diff addresses that failure path, but does not identify the object that triggered it. [source; call_11f85409b5f645fa90dc955ce893f966, call_20b8004a912148b3859c76a06ecdd795, call_690f31d836394f51acfe2b1f4d696921]

## Reasoning

The new handler catches PydanticUserError around the entire attribute branch: the hasattr probe, the second __dict__ lookup, iteration, collection and queue updates. It abandons the rest of that branch without undoing work already done. Dictionary and sequence checks still run for the same object, then the scan proceeds to other queued objects. Other exceptions are not newly suppressed. [source; call_690f31d836394f51acfe2b1f4d696921, call_20b8004a912148b3859c76a06ecdd795]

Catching one exception at the attribute boundary favors a partial diagnostic over losing the entire report. It is narrower than copying the existing dictionary branch's bare except, but the skipped attributes are not reported. [inference; call_690f31d836394f51acfe2b1f4d696921, call_20b8004a912148b3859c76a06ecdd795]

The immediately preceding change added Formatron integration and a constrained-generation example that imports Pydantic. Because the diagnostic scans active frame locals and follows object attributes, that change is a plausible source of newly reachable schema objects, not proof that any particular schema or Formatron operation caused the regression. [inference; call_dbffb7f1fed044a88707413706bbc0ec, call_e50e1033524743c0988b8805deb8f5a7, call_20b8004a912148b3859c76a06ecdd795, call_11f85409b5f645fa90dc955ce893f966]

## Impact

The whole-parent literal search found no invocation of list_gpu_tensors. quantize.py imports it alongside free_mem, but that import does not establish that conversion runs the scan. The patch does not change allocator settings, free_mem or the diagnostic's reporting format. [source; call_2a1132a27e20403e8f90f96b9f037a99, call_a315bc4eb98c4fa28f5e546477435981, call_690f31d836394f51acfe2b1f4d696921]

The new exception import is eager. If Pydantic or its top-level PydanticUserError export is unavailable, importing memory.py fails before any helper can be called. This reaches ordinary package initialization through Model, and also affects conversion and evaluation modules that import memory helpers. The patch changes no dependency declaration: setup.py and requirements.txt list Formatron, not Pydantic directly; requirements_examples.txt already lists Pydantic. [source; call_690f31d836394f51acfe2b1f4d696921, call_87c2df8d998745ebb289edf608cb1f0e, call_42cda88ccfc849ffbd3237cd828a129e, call_362933f5d39044d4ab1253f6f2256abe, call_22c4ef2ec45949aebf815746baf0c525, call_edcc975d68e245d3b896d79bea83e4c1, call_e50e1033524743c0988b8805deb8f5a7, call_ab9ca8d8cbb544d6bc98e6118d27532b]

## Source Notes

The initial runtime entry describes the tensor listing as diagnostic traversal rather than allocator accounting. “Cleanup and comments” documents the device filter and local tabulate import. The two debugger-reference entries explain exclusions applied to reported paths, not traversal pruning. “Improve memory management a little while loading model” records that dictionary scanning already had a separate best-effort guard. The Formatron entry documents the immediately preceding dependency and package-export changes. [ancestor; call_cb36e95bee994a17acfee4f66481b265, call_d1506c1019cf4cd2b0037dddb1cc1604, call_8567a8cc864e473fa85f36835f8e860d, call_a69ad2bd25a24ee397d9959a976ade65, call_56fa4e912b1f4cc5abdb4534c72bff71, call_9b30123b3bba4e098053527b3d206347]

The earlier memory-management diff introduced the bare dictionary handler. It remains unchanged here, as do the debugger-path exclusions. Unlike those exclusions, the new attribute handler can prevent values from ever being discovered through the failing branch. [source; call_494f59ffe1374b829022a4e2640fab1c, call_20b8004a912148b3859c76a06ecdd795, call_690f31d836394f51acfe2b1f4d696921]

The discussion overlap is with import and loading code, not a matching diagnostic failure. #7, “quantizing model: undefined symbol: __cxa_call_terminate,” traces through the package initializer and model.py but ends in native-extension import. #49, “running the QTIP inference code,” offers QTIP installation advice and mentions setup.py and requirements.txt. #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” matches an exception literal in model.py, not the attribute scan changed here. [inference; call_135744f61e524d2ab9b225a6cef9ecb3, call_5ecec368e47342d8b0a761fa44484dc6, call_6c088f11c757490dbfc61068d398449b, call_7d456b7784024347b790940092a4384c, call_690f31d836394f51acfe2b1f4d696921]

Other discussions overlap through modules that import memory helpers. PR #26, “Superior 3INST parameters,” proposes a codebook multiplier, context for quantize.py's multiplier handling. #34, “torch._C._LinAlgError on last layer of quant,” #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” trace to quantize.py's Cholesky path. #53, “Command A support,” starts as a request for model support and later includes that same Cholesky traceback. #33, “Error converting model,” traces through compile.py to a safetensors file-open failure; #55, “Possible GLM4 32B regression,” traces through linear.py to an FP16 constructor type error. The shared importer paths and the generic word “regression” do not tie those reports to this fix. [inference; call_1354f725173a49449214eb8c5c4554ed, call_a315bc4eb98c4fa28f5e546477435981, call_7b98cfd4d2bf4006bb8f0fa5dbec3fec, call_d7187a9d3f0848c8b9d043addb71617b, call_67760208137446ee8e77f202eb708085, call_ce0aeaf98d004d219c1bb7834423f50c, call_c87dd751236d4ae0a0ef6e6ee60cd4fb, call_84c35327c2864c5c982f39e50eb8f589, call_ad18eccfadef4828a4128a01b865d894, call_87c2df8d998745ebb289edf608cb1f0e, call_690f31d836394f51acfe2b1f4d696921]

<a id="runtime"></a>

## Continue tensor diagnostics after a Pydantic attribute error

list_gpu_tensors seeds its queue from module globals and thread-frame locals, then follows attribute, mapping and sequence references. It records tensor paths by object identity and prints size-sorted tables per device. The unchanged default is CUDA tensors of at least one whole MiB: element count times element size, floor-divided by 1024², must be at least one. [source; call_20b8004a912148b3859c76a06ecdd795, call_690f31d836394f51acfe2b1f4d696921]

In a standard-library transcription, a synthetic dict subclass raised a stand-in schema exception on __dict__ access. The old branch aborted before collecting either leaf; the new branch collected both the dict entry and a later queued list entry. Substituting RuntimeError still aborted the new branch. This checks the exception boundary, not Pydantic behavior or tensor traversal in the repository. [execution; call_ee2230e63ab144a98a8bce28250020b3, call_690f31d836394f51acfe2b1f4d696921]

## Authoring-time findings — pending review

### eager-pydantic-import-in-memory-utility (suspected; new_requirement)

A diagnostic-only exception handler introduces a module-wide import prerequisite.

Trigger: Import exllamav3, or a module that loads util.memory, in an environment where import reaches memory.py but pydantic is missing or does not expose PydanticUserError.

Expected: Importing memory helpers such as free_mem, or importing Model without running the diagnostic, should not require the diagnostic's exception class.

Actual: The new top-level import fails before any memory helper is defined. Model imports those helpers during package initialization, so the failure can occur without calling list_gpu_tensors.

Locations: 48ade457da80541cf28887c9fb1e7c7ad662e758:exllamav3/util/memory.py — module-level PydanticUserError import, 08dde73e664b997091370894072065f1f15055bf:exllamav3/models/model.py — module-level memory helper imports

Source evidence: call_690f31d836394f51acfe2b1f4d696921, call_22c4ef2ec45949aebf815746baf0c525, call_362933f5d39044d4ab1253f6f2256abe, call_42cda88ccfc849ffbd3237cd828a129e, call_87c2df8d998745ebb289edf608cb1f0e, call_2a1132a27e20403e8f90f96b9f037a99, call_edcc975d68e245d3b896d79bea83e4c1

source_inspection: Traced the top-level import through the package and model initializers, checked direct memory importers and the absence of literal diagnostic invocations, and compared the unchanged package requirements with the new import. [call_690f31d836394f51acfe2b1f4d696921, call_42cda88ccfc849ffbd3237cd828a129e, call_362933f5d39044d4ab1253f6f2256abe, call_22c4ef2ec45949aebf815746baf0c525, call_87c2df8d998745ebb289edf608cb1f0e, call_2a1132a27e20403e8f90f96b9f037a99, call_edcc975d68e245d3b896d79bea83e4c1, call_ab9ca8d8cbb544d6bc98e6118d27532b]. Limits: The failure is conditional on the environment. No dependency resolution, version matrix or package import was executed.

## Uncertainty and limits

No live Pydantic or Formatron object was shown to raise during the diagnostic. The original trigger, affected versions and whether the installed Formatron dependency consistently supplies the required Pydantic export are unestablished.

The standard-library check transcribed traversal control flow with synthetic objects. It did not import the package, run the repository implementation, inspect live thread frames or execute Torch or CUDA.

Literal searches cannot rule out external or dynamic calls to list_gpu_tensors.
