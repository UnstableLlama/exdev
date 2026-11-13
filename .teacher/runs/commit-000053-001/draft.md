# 8e128ed9040b0fff1107798a1d5e57c8376bb4d5


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/8e128ed9040b0fff1107798a1d5e57c8376bb4d5) · [Evidence ledger](draft.json)

Adds CPU-staged FP16 feature slicing and keyword-tolerant loading interfaces; default staging and padding-before-slicing introduce compatibility concerns.

- [CPU-staged FP16 feature slicing](#modules)

## Problem

The ordinary FP16 loading path previously constructed a linear layer from the complete weight tensor. This change adds constructor parameters for selecting input and output feature ranges. [source; call_4cb6eee5545044a3a1d378759e9a0dc4, call_bccdbd74caed4108a03f081e83c8d2bc]

## Reasoning

Loading the full weight on CPU, copying the selected region into independent storage, and then transferring that storage to the target device can avoid placing the full weight on the GPU. This is host-side slicing, not partial file I/O: get_tensor still reads the complete stored tensor. [inference; call_4cb6eee5545044a3a1d378759e9a0dc4, call_bccdbd74caed4108a03f081e83c8d2bc, call_fdda44a20da6404bb6e96f0e36b2e69b]

## Impact

The new range parameters are forwarded only by the ordinary weight-key branch. The existing fused-weight frange branch and EXL3 loader retain their previous selection mechanisms. [source; call_0eae97b16bde48a2a3054866546a8265, call_4cb6eee5545044a3a1d378759e9a0dc4]

Linear.get_tensors now returns an empty dictionary when self.device is unset instead of unconditionally dereferencing self.inner. [source; call_4cb6eee5545044a3a1d378759e9a0dc4]

## Source Notes

The parent entry describes memory-first tensor lookup with disk fallback. That is context for the tensor source, rather than evidence of successful sliced loading. [ancestor; call_411eb5f608ce4a4d926b50f1152c7eb4]

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure and the reporter's environment workaround. It does not establish a connection to FP16 slicing. [source; call_17464cdb1ab74179af8de4736ed89a73]

<a id="modules"></a>

## CPU-staged FP16 feature slicing

Linear stores full_in_features, full_out_features and starting feature indices. LinearFP16 transposes checkpoint weights into input-by-output layout, then slices an axis only when its stored size equals the corresponding full size and differs from the requested size. Output slicing also slices the bias; input slicing leaves the bias unchanged. [source; call_4cb6eee5545044a3a1d378759e9a0dc4, call_bccdbd74caed4108a03f081e83c8d2bc]

For a sliced layer, LinearFP16 allocates and copies a new weight tensor rather than retaining just a view of the complete backing storage. Linear then sets swap_device and calls the existing unswap_cpu method, which transfers weight and bias and clears swap_device. [source; call_bccdbd74caed4108a03f081e83c8d2bc, call_4cb6eee5545044a3a1d378759e9a0dc4, call_bde2fa8ba9b248c8ab19f9719bc39807]

A scalar indexing transcription confirmed that selecting input indices 2–4 and output indices 4–7 after transposition produces the corresponding 3-by-4 submatrix. This checks axis interpretation, not tensor-library or kernel behavior. [execution; call_e84bded617e84185b922cee3790ff9a9]

The existing pad_to default of 128 rounds output width up to a multiple of 128. Padding still precedes the new slicing step, and LinearFP16 receives that padded width rather than out_features_unpadded. [source; call_0eae97b16bde48a2a3054866546a8265, call_4cb6eee5545044a3a1d378759e9a0dc4]

Module.load now forwards keyword arguments to children. Attention, Embedding, Linear and RMSNorm accept them, but Attention still calls super().load(device) without forwarding them. The slice controls are constructor arguments, not newly consumed load keywords. [source; call_e90c559e55624ce8b48195a02a4a1a3b, call_5c81742b72b646f18ecfb2ac8ae00dff, call_2a23dc0532304aa6a0a5901502ee72a5, call_4cb6eee5545044a3a1d378759e9a0dc4, call_61bc6da397c4423dbefef38242a3b9de]

## Authoring-time findings — pending review

### default-cpu-staging (suspected; behavior_change)

Omitting the optional full-size parameters selects the sliced loading route even without requesting a slice.

Trigger: Construct Linear with ordinary integer dimensions and leave full_in_features and full_out_features at None.

Expected: An unsliced request would retain direct target-device weight loading.

Actual: Integer dimensions compare unequal to None, so is_sliced is true. The ordinary FP16 branch stages the complete weight on CPU, explicitly copies it, and transfers it through unswap_cpu.

Locations: 8e128ed9040b0fff1107798a1d5e57c8376bb4d5:exllamav3/modules/linear.py — Linear.__init__

Source evidence: call_4cb6eee5545044a3a1d378759e9a0dc4, call_bccdbd74caed4108a03f081e83c8d2bc, call_d86479a35b854b74a56c8270cea29437

source_inspection: Whole-parent constructor search shows attention and MLP construction sites omitting the new parameters; the task does not update those constructions. The changed route applies when their ordinary FP16 weight branch is selected, not their EXL3 branch. [call_d86479a35b854b74a56c8270cea29437, call_0eae97b16bde48a2a3054866546a8265, call_4cb6eee5545044a3a1d378759e9a0dc4]. Limits: No performance measurement or model loading execution.

scalar_transcription: Evaluated the default comparison and obtained true. [call_e84bded617e84185b922cee3790ff9a9]. Limits: Python predicate only.

### padding-before-slicing (suspected; defect)

Padding the full source tensor to the local output shape can fail before slicing is reached.

Trigger: Load a full 512-by-64 weight into a Linear requesting 130 outputs and 64 inputs, with full_out_features=512, first_out_feature=0 and the default pad_to=128.

Expected: Select the requested output region and pad the local result to 256 outputs.

Actual: pad_out first allocates a 256-by-64 tensor and attempts to assign the full 512-by-64 source into it. The incompatible assignment precedes LinearFP16's slicing.

Locations: 8e128ed9040b0fff1107798a1d5e57c8376bb4d5:exllamav3/modules/linear.py — Linear.load_fp16

Source evidence: call_0eae97b16bde48a2a3054866546a8265, call_4cb6eee5545044a3a1d378759e9a0dc4

source_inspection: Whole-parent search locates Linear.load as the direct caller of load_fp16; it tries FP16 after EXL3 lookup fails. The observation concerns the newly parameterized ordinary weight branch. [call_d64e0b6c7b024b37b0b186199aab53c2, call_0eae97b16bde48a2a3054866546a8265, call_4cb6eee5545044a3a1d378759e9a0dc4]. Limits: No existing model construction requesting this new slice was demonstrated.

scalar_transcription: Computed the padded destination width as 256 and verified that the 512-row source exceeds it. [call_e84bded617e84185b922cee3790ff9a9]. Limits: Shape arithmetic only; the PyTorch assignment and its exception were not executed.

### inherited-native-read-wait (suspected; defect)

The inherited GPU disk-read failure synchronization risk is unchanged, although CPU-staged weights bypass its copy worker.

Trigger: A GPU-target mt_fread read fails while the copy worker waits on an empty queue, with no later enqueue.

Expected: Wake the worker and report the I/O failure.

Actual: The reader sets load_failed without notifying the condition variable; the wait predicate checks only queue nonemptiness, so joining the worker may not complete.

Locations: 70e79cc880a40aa0aa7a41cc80c574622a658197:exllamav3/exllamav3_ext/stloader.cpp — stloader_read

Source evidence: call_70c40bedc6814f099d37680de0761581, call_fdda44a20da6404bb6e96f0e36b2e69b, call_4cb6eee5545044a3a1d378759e9a0dc4

source_inspection: Inspected the inherited implementation and its get_tensor caller after reading the ancestor observation. The task leaves native loading unchanged. CPU-staged ordinary weights avoid the copy worker; GPU-loaded biases and other direct GPU disk reads can still reach it. [call_2cc7cd3dbdc847e08d74d21c6dc95ea7, call_70c40bedc6814f099d37680de0761581, call_fdda44a20da6404bb6e96f0e36b2e69b, call_4cb6eee5545044a3a1d378759e9a0dc4]. Limits: No concurrent execution or injected read failure.

## Uncertainty and limits

No PyTorch loading, CUDA transfer, native loader, or matrix multiplication was executed. The standard-library check models indexing and shape arithmetic only.

Peak memory and loading-time effects remain unmeasured; the full source weight still occupies host storage.

Range validation and end-to-end model use of the new parameters were not demonstrated.
