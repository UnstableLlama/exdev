# 8fa88a230b2c6d241ee2aabc7259f5d458d0e0f2


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/8fa88a230b2c6d241ee2aabc7259f5d458d0e0f2) · [Evidence ledger](draft.json)

Replaces template-lambda CUDA dispatch with explicit specialization tables to address reported older-VC++ failures, adds launch-error checks, and leaves unsupported weight bitrates vulnerable to unchecked indexing.

- [Explicit specialization tables for CUDA launches](#kernel-dispatch)

## Problem

The author reports nested static_for_pack failures with VC++ older than 17.13. The change replaces template-lambda launch selection with explicit kernel-pointer tables; the compiler-version boundary is an author claim, not independently verified. [source; call_80f2ac7273b24ab28932ba84369a0d0e]

## Reasoning

Explicit tables retain compile-time kernel specializations while moving runtime selection to array indexing. This avoids the nested generic-lambda dispatch implicated by the author, at the cost of manually enumerating supported variants. [inference; call_80f2ac7273b24ab28932ba84369a0d0e]

## Impact

Paged cache wrappers now explicitly reject bitrates outside 2–8 before indexing. Packing, unpacking, sign packing and reconstruction also gain cudaPeekAtLastError checks. [source; call_80f2ac7273b24ab28932ba84369a0d0e]

## Source Notes

A whole-parent-tree literal search found no VC++ occurrences. [source; call_8b3a90b1353843a283e7b2abdd403fd6]

The inspected discussions report distinct problems: #7, “quantizing model: undefined symbol: __cxa_call_terminate,” describes a Linux/Conda toolchain mismatch; #15, “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” discusses regularization; #12, “Qwen2.5 Coder 0.5B Instruct | ValueError: Unsupported type in stop_conditions,” discusses chat mode selection. None supplies verification of this VC++ workaround. [source; call_8584a714aec64179aa439f18d22260dc, call_223cc0ab3ca446559a490bc87d84b162, call_5b748fc8d26c41569c39d1a7439b8ca1, call_efbfa10bcb4d4a008652de82632b5c7a]

<a id="kernel-dispatch"></a>

## Explicit specialization tables for CUDA launches

Weight packing, unpacking, tile quantization and reconstruction use eight-entry tables indexed by K−1, covering 1–8 bits per weight. Contiguous cache operations use seven-entry tables indexed by bits−2; paged operations use 7×7 tables with key bitrate as the first dimension and value bitrate as the second. [source; call_80f2ac7273b24ab28932ba84369a0d0e]

The selected kernels retain their existing algorithms and launch arguments: cache kernels encode/decode 32-value groups with independent key/value specializations; weight packing operates on 256-value tiles; quantize_tiles retains its scratch-buffer batching; reconstruction retains 256-thread blocks handling eight packed tiles. This is dispatch restructuring, not a new compression format. [source; call_80f2ac7273b24ab28932ba84369a0d0e, call_8f4985222c514bbe901d62941550190e, call_ba094f15d85d4313acf8187c1551f811, call_18ab0bd66e0547f2b3846e9ec97dbbd6, call_5beef9cdc6984a659d295fa276354890]

A bounded Python transcription verified that all eight weight selectors and all 49 key/value combinations recover the original specialization parameters. [execution; call_57c360e09b1f4e5d8423532862232807]

static_for_pack remains defined. util.h adds a commented table example and the compiler warning rather than removing the helper. [source; call_80f2ac7273b24ab28932ba84369a0d0e]

## Authoring-time findings — pending review

### unchecked-pack-bitrate (suspected; defect)

Direct table indexing introduces an unchecked out-of-range access in pack_trellis and unpack_trellis for unsupported K.

Trigger: Call either native wrapper with K=9 and tensors satisfying its shape checks, including packed final dimension 144 and unpacked final dimension 256.

Expected: Reject unsupported bitrate without accessing outside the specialization table.

Actual: The new expression indexes element 8 of an eight-entry table. Existing shape checks do not reject this construction; the previous dispatch simply selected no kernel.

Locations: 8fa88a230b2c6d241ee2aabc7259f5d458d0e0f2:exllamav3/exllamav3_ext/quant/pack.cu — pack_trellis, 8fa88a230b2c6d241ee2aabc7259f5d458d0e0f2:exllamav3/exllamav3_ext/quant/pack.cu — unpack_trellis

Source evidence: call_80f2ac7273b24ab28932ba84369a0d0e, call_ba094f15d85d4313acf8187c1551f811, call_5b113b6891704aa9992e2637d0da1a61, call_e9f74f420ce64cd999592cf80cd58a65

source_inspection: Whole-parent-tree search finds both native bindings and a Python pack_trellis helper that forwards quant_args['K'] without a local range check. The unpack call in that helper is commented out. Reach is established for direct extension callers and this packing helper, not for every conversion workflow. [call_5b113b6891704aa9992e2637d0da1a61, call_e9f74f420ce64cd999592cf80cd58a65, call_ba094f15d85d4313acf8187c1551f811, call_80f2ac7273b24ab28932ba84369a0d0e]. Limits: No claim that normal conversion settings produce K=9.

scalar_transcription: Computed packed dimension 144 and table index 8 for K=9. [call_57c360e09b1f4e5d8423532862232807]. Limits: Arithmetic only; no native out-of-bounds access or GPU launch was executed.

## Uncertainty and limits

No CUDA compilation, GPU execution or performance measurement was performed; compatibility with the stated VC++ versions remains unestablished.

The scalar check validates transcribed selector arithmetic only, not C++ function-pointer launch support or numerical kernel correctness.
