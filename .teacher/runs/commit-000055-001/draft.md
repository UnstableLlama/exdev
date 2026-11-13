# d6124d70584f83440fc8ad551f8f82bdf8479c64


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d6124d70584f83440fc8ad551f8f82bdf8479c64) · [Evidence ledger](draft.json)

Adds sequential conversion and summed inference for wide gated-MLP slices, sharing bit allocations across slices and staging converted tensors on CPU. Non-gated allocation paths have source-visible compatibility concerns.

- [Slice wide gated MLPs through capture, allocation and reload](#conversion)

## Problem

Wide gated MLPs require large intermediate-dimension Hessians during quantization. The change introduces a default split threshold of 55,296 features, described in source as a practical single-GPU quantization limit. [source; call_525c7c78e19e4fb0a9c26281d501068e, call_0071d5e6970c47df97186257644a8746]

## Reasoning

Partitioning intermediate features reduces each down projection's input dimension and therefore its square Hessian allocation. Sequential capture and conversion trade repeated module loading and forward passes for smaller working sets. [inference; call_b085623274424230bad4c219081b985d, call_2915ac156cc240acb4916a4b2f62297e, call_0071d5e6970c47df97186257644a8746]

## Impact

Splitting changes both conversion and ordinary gated-MLP execution: stored projections acquire .slice.N keys, while ordinary forward execution evaluates all slices and adds their down-projection outputs. Fused gate/up storage is explicitly rejected when splitting would be required. [source; call_b085623274424230bad4c219081b985d]

## Source Notes

Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” reports an extension import failure and a reporter-supplied environment workaround. It does not report MLP slicing or establish motivation for this change. [source; call_e9ef5bf24b98432b8027eb49d94153aa]

<a id="conversion"></a>

## Slice wide gated MLPs through capture, allocation and reload

GatedMLP chooses ceil(intermediate_size / split_size) slices above the threshold, rounds the common slice width down to a multiple of 128, and puts the remainder in the last slice. Passing a false split size disables splitting. Gate/up projections slice output features; down projections slice input features over the same contiguous intervals. [source; call_b085623274424230bad4c219081b985d]

A scalar transcription produced one slice at 55,296 and two 32,768-feature slices at 65,536. For the latter example, the sum of squared slice widths is half the original squared width; sequential processing needs only one such slice Hessian at a time, excluding other allocations. [execution; call_898f892d20c9438ea354cde8dff14561]

Sliced linears use the original unsliced tensor names as alternate keys. The existing FP16 loader stages sliced weights on CPU, and LinearFP16 transposes and selects the requested feature interval before moving the result to the destination device. This reuses the existing slicing interface rather than rewriting checkpoint tensors first. [source; call_b085623274424230bad4c219081b985d, call_0071d5e6970c47df97186257644a8746, call_8170d3089ab04d9f94b0426a77e25e68]

Module defaults to one slice, and TransformerBlock adopts its MLP's slice count. Conversion allocates the bit budget once, then loads, captures and quantizes each slice separately. q_mlp_slice selects a single gated-MLP branch during capture; normal forward calls omit it and sum every branch. [source; call_97fd79ac91a74f5ebb4d04f25d5f17b2, call_bedbf15c983d422485adefd62c35907c, call_2915ac156cc240acb4916a4b2f62297e, call_b085623274424230bad4c219081b985d]

Allocation groups gated projection slices under wildcard keys and sums their weight counts. The existing budget search still chooses projection-level bit widths, which are then expanded to each concrete slice key. Thus slices of one projection share a bit width rather than competing independently for budget. [source; call_a5d79e821a9644a0854efa6a41443d51, call_a2c2143fc64f43e892589e39ffdb76eb]

Converted LinearEXL3 tensors are moved to CPU immediately, collected across slices and saved once per module. After unloading, conversion installs the collected tensor mapping into the safetensors collection, reloads the whole module, clears that mapping and advances calibration state. The displayed reference error becomes N/A for sliced modules. [source; call_2915ac156cc240acb4916a4b2f62297e, call_56f1dc131b3942608473779995c069dc, call_0071d5e6970c47df97186257644a8746]

The transformer allocation guard returns an empty strategy and unchanged surplus for blocks with neither attention nor MLP, avoiding entry into the allocator's zero-weight budget calculation now that conversion requests allocation unconditionally. [source; call_bedbf15c983d422485adefd62c35907c, call_2915ac156cc240acb4916a4b2f62297e, call_a2c2143fc64f43e892589e39ffdb76eb]

## Authoring-time findings — pending review

### plain-mlp-allocation-interface (suspected; defect)

Transformer allocation now assumes plural projection attributes even for the unchanged non-gated MLP class.

Trigger: Call TransformerBlock.allocate_q with an ordinary MLP instance.

Expected: Allocate bits for that MLP's up and down projections.

Actual: The changed call accesses self.mlp.ups and self.mlp.downs, but MLP defines only up and down, so attribute lookup fails before allocation. The whole-parent-tree constructor search found gated model builders, not an ordinary MLP construction; the demonstrated reach is the exposed TransformerBlock interface, not every supplied model.

Locations: d6124d70584f83440fc8ad551f8f82bdf8479c64:exllamav3/modules/transformer.py — TransformerBlock.allocate_q

Source evidence: call_bedbf15c983d422485adefd62c35907c, call_ccc83e657b2c461a9f25ceac374f8ea9, call_ea64e294c7d14e74b060087643153c57, call_2915ac156cc240acb4916a4b2f62297e

source_inspection: Compared the changed allocation arguments with ordinary MLP attributes and the conversion allocation call. [call_bedbf15c983d422485adefd62c35907c, call_ccc83e657b2c461a9f25ceac374f8ea9, call_2915ac156cc240acb4916a4b2f62297e]. Limits: No instantiated model execution; supplied model constructor search found only GatedMLP builders.

### ungated-list-strategy-key (suspected; defect)

The new ungated list allocation branch appends a list of linears rather than its wildcard string to strategy keys.

Trigger: Call allocate_transformer with g=None and nonempty up/down lists.

Expected: Produce a concrete-key strategy using the shared wildcard allocation.

Actual: keys += [m] retains each list, so final dictionary construction attempts to use unhashable lists as keys. The parent-tree search found TransformerBlock.allocate_q as the only direct caller; the new branch is not reached by its normal gated-MLP arguments.

Locations: d6124d70584f83440fc8ad551f8f82bdf8479c64:exllamav3/conversion/allocation.py — allocate_transformer

Source evidence: call_a5d79e821a9644a0854efa6a41443d51, call_e00b9840efaf4bc3aa2a875646867377, call_bedbf15c983d422485adefd62c35907c

scalar_transcription: Constructed the analogous dictionary from list-valued keys; Python raised TypeError. [call_898f892d20c9438ea354cde8dff14561, call_a5d79e821a9644a0854efa6a41443d51]. Limits: This modeled the failing dictionary operation, not execution of the repository allocator.

## Uncertainty and limits

No repository conversion, GPU kernel, memory benchmark or quantized-output comparison was executed. The Python check only transcribed split arithmetic and dictionary construction.

The inspected source does not establish why 55,296 is the practical hardware limit. The 128-feature rounding matches Linear's default output alignment, but the final remainder is not necessarily aligned for arbitrary input dimensions.

Summing independently evaluated slices does not establish bitwise equivalence or unchanged quantization quality.
