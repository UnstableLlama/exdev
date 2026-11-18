# 6bd852cc5e8cdb4c415460b6910e054bbbbb6f95


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/6bd852cc5e8cdb4c415460b6910e054bbbbb6f95) · [Evidence ledger](draft.json)

Separates padding-only loading from slicing, but reverses inner cropping conditions and breaks the fused caller's optional full-dimension defaults.

- [Distinguishing feature slicing from padding](#modules)

## Problem

Dimension inequality classified both reductions and padding-only enlargement as slicing, selecting CPU staging and disabling deferred loading for both. [source; call_e28e2c50c5ca47769d915d746fc9e7e0, call_b9d4afc9689c4633b37006de277945dc]

## Reasoning

The apparent goal is to reserve slicing and independent storage for reductions while leaving enlargement to loader-side padding. However, the inner cropping comparisons change in the opposite direction from that required for reductions. [inference; call_e28e2c50c5ca47769d915d746fc9e7e0, call_5173440a24814bf58e41c1556bfdf3cf, call_4dd28603dbf245bca3c1438dec06d487]

## Impact

Padding-only instances can use target-device padded loading and become eligible for deferred loading. Genuine slices retain full matrices, and the existing fused-weight caller encounters an integer-versus-None comparison. [source; call_b9d4afc9689c4633b37006de277945dc, call_e28e2c50c5ca47769d915d746fc9e7e0, call_5173440a24814bf58e41c1556bfdf3cf]

## Source Notes

Read the initial quantized-inference chapter, the FP16-slicing entry and the deferred-loader entry. They establish the dense backend, CPU-staged slicing with independent storage, and the requirement not to consume unfinished deferred tensors. [ancestor; call_c6dec29e78dc403092636be72e04d9c2, call_7a575d4950134ea8ace8eb77a9b4e16c, call_0237d2a1be5f479792b457ccce219ebf]

The slicing entry's default-None staging issue is already removed in the parent: Linear normalizes full dimensions. Its padding-before-slicing issue has also changed: the current sliced branch requests no loader padding. These historical observations do not establish that the task's new inner comparisons work. [source; call_b9d4afc9689c4633b37006de277945dc, call_5173440a24814bf58e41c1556bfdf3cf]

Issue #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports padding conflicting with split wide layers. Issue #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” concerns vocabulary padding. Their relevance is inferred from padding/slicing overlap and linear.py traceback paths; neither explicitly links to or validates this task. [inference; call_df53e85fa3d5420d8bd8669880d58812, call_d18261ca4ba846f5bfb9f398bb1e868a, call_e28e2c50c5ca47769d915d746fc9e7e0]

Other discussions share inspected paths but do not establish this task's motivation: #11, “AssertionError: bias is wrong datatype,” concerns bias conversion; #16, “RuntimeError: CUDA error: invalid configuration argument,” is ultimately framed as tokenizer truncation; #34, “torch._C._LinAlgError on last layer of quant,” and #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” discuss invalid numerical states. Their task relationships are inference from shared linear.py paths. [inference; call_abe1a687845c4d3faf51b1a57b34fcd1, call_1f5ca23dc2884ff9a1efb8be3e2a4d33, call_57b491775d134ab8b82241419ac9784d, call_08f79e48a76e49eb92844dc04deeea99, call_56c36deca1704a2d9c1b8c53f63ef0b5]

Issue #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” is framed as invalid forward states preventing calibration. Issue #33, “Error converting model,” initially establishes an open-file-limit failure and later tracks GLM4 repeated-token output. Connections to this task are inferred file overlaps with linear.py and the inspected loader, not established causes. [inference; call_56c36deca1704a2d9c1b8c53f63ef0b5, call_08f79e48a76e49eb92844dc04deeea99, call_6001fb20491a4b25980db6f7e42cc4a6, call_db832eaa587e4aa4ad28dd10819cb637]

<a id="modules"></a>

## Distinguishing feature slicing from padding

Linear rounds requested axes upward to a pad_to multiple, default 128, while retaining unpadded counts. Omitted full dimensions become the padded dimensions and omitted offsets become zero. The changed is_sliced predicate therefore compares prepared storage dimensions, not original unpadded requests. [source; call_b9d4afc9689c4633b37006de277945dc, call_e28e2c50c5ca47769d915d746fc9e7e0]

All parent-tree is_sliced readers are in Linear. True selects CPU loading without padding, followed by unswap_cpu, and rejects deferred loading. False requests padded weight and bias on the target device and permits the superclass's deferral decision. These are coupled consequences of one classification change. [source; call_ccb92c321fb54402934a395891df748b, call_b9d4afc9689c4633b37006de277945dc]

File-backed SafetensorsCollection paths transpose when requested and populate zero-filled padded destinations. Deferred loading returns destinations before populating them. Restricting LinearFP16's independent-storage copy to reductions avoids copying unfinished values for padding-only enlargement. [source; call_4dd28603dbf245bca3c1438dec06d487, call_b9d4afc9689c4633b37006de277945dc, call_5173440a24814bf58e41c1556bfdf3cf]

LinearFP16 stores input-by-output weights. Output slicing also slices bias; input slicing leaves bias unchanged. Forward allocates out_features columns and multiplies by the stored matrix; export transposes that matrix back. Neither consumer repairs an omitted crop. [source; call_4dd28603dbf245bca3c1438dec06d487, call_5173440a24814bf58e41c1556bfdf3cf]

Whole-parent searches find two direct LinearFP16 constructions, both in Linear.load_fp16. The ordinary branch supplies numeric full sizes and offsets. The fused frange branch supplies neither full sizes nor offsets, leaving the constructor's None defaults unchanged. [source; call_76def9ce6afc45548d35e176e9c03c15, call_b9d4afc9689c4633b37006de277945dc, call_4dd28603dbf245bca3c1438dec06d487]

Inspected direct Linear constructions in attention, ordinary MLP, sparse-MLP routing/experts, model output heads and Gemma3/Mistral3 projections omit full dimensions and retain equal local/full metadata. GatedMLP explicitly supplies full dimensions: padding-only instances benefit from the classification change, but reduced slices reach the broken crop conditions. Attention prepares fused QKV ranges; GatedMLP prepares fused gate/up ranges, providing conditional routes to the caller that omits full sizes. [source; call_a2f10b131f2247ac97e1731458864921, call_a45c8463207e448ba11277f310b54d56, call_c28c7b1161134732aae1fdb94ac7fd31, call_2b879a2aaa8b4066a8174130349f2214]

A scalar transcription checked equal, reduced and enlarged axes. With full=512, local=256 and offset=128, the parent selects 256 indices while the task retains all 512. With full=510 and local=512, is_sliced changes from true to false. It also confirmed that alignment 128 rounds 510 to 512 and integer < None raises TypeError. [execution; call_0d847360d8e24a99930d953d19d45767]

A compatible crop condition would recognize stored full axes larger than requested local axes and preserve handling of omitted full dimensions. This is a source-derived alternative, not a tested replacement. [inference; call_5173440a24814bf58e41c1556bfdf3cf, call_4dd28603dbf245bca3c1438dec06d487, call_b9d4afc9689c4633b37006de277945dc]

## Authoring-time findings — pending review

### reversed-slice-comparisons (suspected; defect)

The new inner axis predicates skip genuine reductions of full FP16 weights.

Trigger: Ordinary FP16 loading receives a full weight with an axis larger than its requested local axis, including split GatedMLP projections loaded through alternate full-weight keys.

Expected: Crop at the supplied offset, crop output bias when applicable, and retain the local matrix.

Actual: stored < requested is false for reductions. The subsequent copy preserves the full shape. Gate/up matrices disagree with allocated output width; down matrices disagree with local input width. No downstream crop repairs them.

Locations: 6bd852cc5e8cdb4c415460b6910e054bbbbb6f95:exllamav3/modules/quant/fp16.py — LinearFP16.__init__

Source evidence: call_5173440a24814bf58e41c1556bfdf3cf, call_4dd28603dbf245bca3c1438dec06d487, call_2b879a2aaa8b4066a8174130349f2214

source_inspection: Inspected both direct constructor callers and GatedMLP's full-size/offset preparation. Reach is conditional on loading full FP16 weights rather than already-local or EXL3 weights. [call_76def9ce6afc45548d35e176e9c03c15, call_b9d4afc9689c4633b37006de277945dc, call_2b879a2aaa8b4066a8174130349f2214]. Limits: No tensor multiplication was executed.

scalar_transcription: Modeled the changed axis-selection predicates with Python lists; a 512-to-256 reduction retained 512 indices. [call_0d847360d8e24a99930d953d19d45767]. Limits: Indexing model, not repository execution.

### none-full-dimensions (suspected; defect)

The existing fused-weight caller is incompatible with the new ordered comparison.

Trigger: Linear.load_fp16 selects its fused frange fallback and constructs LinearFP16 without full dimensions.

Expected: Accept the already-selected local weight using the declared optional defaults.

Actual: The final copy predicate compares integer in_features with None and raises TypeError. LinearFP16 does not normalize these defaults.

Locations: 6bd852cc5e8cdb4c415460b6910e054bbbbb6f95:exllamav3/modules/quant/fp16.py — LinearFP16.__init__

Source evidence: call_5173440a24814bf58e41c1556bfdf3cf, call_4dd28603dbf245bca3c1438dec06d487, call_b9d4afc9689c4633b37006de277945dc

source_inspection: Both direct constructor calls were inspected. Attention's fused QKV and GatedMLP's fused gate/up preparation establish conditional broader entry points. [call_76def9ce6afc45548d35e176e9c03c15, call_c28c7b1161134732aae1fdb94ac7fd31, call_2b879a2aaa8b4066a8174130349f2214]. Limits: Requires selection of the fused fallback.

scalar_transcription: Evaluated the changed predicate with integer dimensions and None defaults; Python raised TypeError. [call_0d847360d8e24a99930d953d19d45767]. Limits: The repository constructor did not run.

### inherited-deferred-bf16-tail (suspected; defect)

The previously recorded odd-element deferred BF16 conversion omission persists.

Trigger: Deferred CUDA loading converts an odd-sized BF16 tensor to FP16.

Expected: Convert every element before destination consumption.

Actual: The wrapper launches conversion for numel / 2 pairs; an odd final element remains unconverted. The task does not alter this loader implementation.

Locations: ddf260767d5e31b04d1e0cd660ef4188071d809a:exllamav3/exllamav3_ext/stloader_cu.cu — inplace_bf16_to_fp16_cuda

Source evidence: call_973a0b1e042c46c4b3fbf84022b66056, call_6f3da642e21c497fbd598fac540b3aec

source_inspection: Reinspected the conversion kernel and its stloader_deferred_cuda caller after reading the ancestor observation. The loader data flow remains unchanged. [call_1e7c77d94c5e44168a2b1657ae01b219, call_973a0b1e042c46c4b3fbf84022b66056, call_6f3da642e21c497fbd598fac540b3aec]. Limits: No newly affected checkpoint or GPU execution demonstrated.

### inherited-native-read-wait (suspected; defect)

The earlier slicing entry's native GPU read-failure synchronization concern remains unchanged.

Trigger: An eager GPU mt_fread read fails while the copy worker waits on an empty queue, without a later enqueue.

Expected: Wake the worker and report the failure.

Actual: Failure sets load_failed without notifying the condition variable, whose predicate tests only queue nonemptiness. Joining the worker may not complete.

Locations: ddf260767d5e31b04d1e0cd660ef4188071d809a:exllamav3/exllamav3_ext/stloader.cpp — stloader_read

Source evidence: call_6f3da642e21c497fbd598fac540b3aec

source_inspection: Reinspected the worker and its sole Python caller in get_tensor. Padding-only instances can now request target-device loading, reaching this eager branch when deferral is inactive. [call_022d872dec544c3287c880e88aca2839, call_6f3da642e21c497fbd598fac540b3aec, call_b9d4afc9689c4633b37006de277945dc, call_e28e2c50c5ca47769d915d746fc9e7e0]. Limits: No injected read failure or concurrent execution.

## Uncertainty and limits

No repository constructor, PyTorch operation, native loader or GPU kernel was executed. The scalar check models comparisons, indexing and alignment only.

Loading speed, memory savings and end-to-end checkpoint compatibility were not measured.

Caller searches cover the parent repository; dynamic construction and external callers remain unestablished.
