# c4867edd0d31ea9fb052668874ae52fad0e91a0f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/c4867edd0d31ea9fb052668874ae52fad0e91a0f) · [Evidence ledger](draft.json)

Retunes GEMM dispatch and fragment buffering and introduces explicit decoder instructions. Performance remains unmeasured; inspection identifies a scalar decoder mismatch, missing GEMV header and retained selector defect.

- [Dequantization and GEMM scheduling optimizations](#quantized-inference)

## Problem

The change targets dequantization instruction overhead and GEMM scheduling through explicit LOP3 instructions, different bit extraction, deeper fragment buffering and revised device-specific shape selection. [source; call_798ae2b2e0064ea59220b9b7e021deaf, call_e48b3f17507148ef9932b736f5b033d0, call_ebfc66cc953a4feea4e142006eb8749a, call_1e7cfa879bb4448caddd20d1ca66e744]

## Reasoning

These edits seek better instruction scheduling rather than a new quantization format: the multiplier, increment, masks and four tile geometries remain unchanged. More fragment buffers trade register storage for scheduling flexibility; their actual performance benefit is unmeasured. [inference; call_798ae2b2e0064ea59220b9b7e021deaf, call_ebfc66cc953a4feea4e142006eb8749a, call_351eb755aebc45dda0cde5ae0b5fe241]

## Impact

The patch also presents suspected correctness and build obstacles: scalar codebook decoding applies the mask/XOR transformation twice, and all eight compilation units include a header absent from the parent tree and not added by the change. [source; call_798ae2b2e0064ea59220b9b7e021deaf, call_72a6a55a3c1e4b9793061ab2d65b5c54, call_2dacf31006b844eba57f0e5e642da301, call_36510c563c5d4681bcd2b230664b701c]

## Source Notes

The earlier cooperative-GEMM entry records a Boolean-versus-dimension threshold defect in select_gemm_shape. [ancestor; call_54beb44e23614218bded6ae654382131]

PR #26, “Superior 3INST parameters,” was opened by louiehelm and proposes different codebook parameters. Its discussion separately proposes the same LOP3 mask/XOR instruction used here; turboderp discusses unpacking overhead and kernel refactoring. The task retains the original multiplier and increment. [source; call_8cc35a196ad444ce8e6b14ce95918374, call_4ee3d0ad8a904596b94eca74ad29d21c, call_798ae2b2e0064ea59220b9b7e021deaf]

The matching LOP3 instruction and constants make PR #26 relevant optimization context, but do not establish an explicit upstream link or adoption of its parameter proposal. Its reported speedups are not measurements of this commit. [inference; call_8cc35a196ad444ce8e6b14ce95918374, call_798ae2b2e0064ea59220b9b7e021deaf]

<a id="quantized-inference"></a>

## Dequantization and GEMM scheduling optimizations

The existing outer kernel optionally transforms A into A_had, synchronizes the cooperative grid, executes GEMM in 16-row chunks, then optionally transforms C in place. The selected inner kernel asynchronously stages A and packed B through shared memory, decodes B into register fragments, performs tensor-core multiplication and reduces partial outputs using locks. This data flow is retained. [source; call_f24219eee245461d9c9f7b22b401456d, call_351eb755aebc45dda0cde5ae0b5fe241, call_a31f42217ddb4790a2426e2ccb28d3d5]

Shape tuples encode M, K, N, shared stages and fragment stages. Shape 1 changes from one to two fragment stages; shapes 2–4 change from two to three. Their (K,N) tiles remain (16,128), (32,128), (32,256), (16,512). The added four-fragment loop cycles load-next/multiply-current across four buffers, but none of the registered shapes selects it. [source; call_ebfc66cc953a4feea4e142006eb8749a, call_a31f42217ddb4790a2426e2ccb28d3d5, call_351eb755aebc45dda0cde5ae0b5fe241]

All eight bitrate-specific compilation units now use one common instantiation macro for both FP16 and FP32 outputs. The macro still registers only four GEMM kernels, not GEMV kernels. Shape count and block dimensions become explicit metadata; the listed 256,512,512,256 threads match the previous 256*K/16 calculation. [source; call_2dacf31006b844eba57f0e5e642da301, call_5684dba9a42d459dbeb48c85da604fc3, call_e6ec6c5c924f4d5a9b17039422b20f96, call_8fd1adc7c0b746b9a95bd6325cce1e3a, call_d5354cbdfdb946a09e28a0f74f761fef, call_dd61403a0bbe4b7da185ec71011500d8, call_6d8534cbece24c7cad35951c8d6b30bb, call_36510c563c5d4681bcd2b230664b701c, call_ebfc66cc953a4feea4e142006eb8749a]

For OLD/Ampere at more than four bits, the narrow-width branch now excludes n=4096, and shape 4 requires 512-column divisibility, k*n>4096² and at most six bits. Ada moves four-bit weights out of its low-bitrate branch and makes that branch's 4096 boundary strict. Hopper/Blackwell group seven-bit weights with eight-bit weights, remove automatic shape-1 selection and allow wider tiles at lower bitrates. [source; call_1e7cfa879bb4448caddd20d1ca66e744, call_b31697eb4e6b4a94a3b6e1afac95a55f]

The selected callees retain tile divisibility requirements, a 90-KiB shared-memory ceiling and cooperative grid synchronization. Width divisibility gates correspond to the 256- and 512-column tiles. These constraints explain compatibility, not why a particular compatible shape is fastest. Unsupported bitrate switches now explicitly raise an error. [source; call_351eb755aebc45dda0cde5ae0b5fe241, call_f24219eee245461d9c9f7b22b401456d, call_b31697eb4e6b4a94a3b6e1afac95a55f, call_1e7cfa879bb4448caddd20d1ca66e744]

fshift replaces conditional funnel shifting with a 64-bit concatenation, a in the high word and b in the low word, followed by a right shift and truncation. The scalar comparison agreed for 192 representative word/shift combinations spanning shifts 0–63. This checks arithmetic equivalence, not compiler lowering or speed. [execution; call_e48b3f17507148ef9932b736f5b033d0, call_6c3dd0e5cc0b4fa1bf74522146e9e376, call_5d2d7372fa3c4965af8dd95f082476e2]

The paired decoder replaces separate AND/XOR operations with explicit LOP3. The scalar decoder retains a C++ AND/XOR before the new instruction. Python confirmed the binary masks equal 0x8FFF8FFF and 0x3B603B60, and the truth table for (a&b)^c is 0x6A under the modeled operand indexing. [execution; call_798ae2b2e0064ea59220b9b7e021deaf, call_5d2d7372fa3c4965af8dd95f082476e2]

The benchmark changes K from one to eight bits per weight, removes m=17 and m=32, and enables cuda:2 and cuda:3 alongside cuda:1. It still times forced compatible shapes and queries automatic selection, using synthetic tensors explicitly not intended for correctness testing. These edits supply no benchmark results. The Hadamard helper also gains an include guard. [source; call_94aecad38804407a898c5912d4eb8457, call_34808e6db0874dbaaa4480eedee1863f, call_4358dfe7408d4f5c96db57b7fb2f668e]

## Authoring-time findings — pending review

### scalar-codebook-double-transform (suspected; defect)

decode_3inst applies the same mask/XOR transformation twice, unlike decode_3inst_2.

Trigger: A scalar decoder call receives a codebook state, including state zero.

Expected: Scalar and paired decoders should preserve the original codebook and agree for the same state.

Actual: The scalar path performs C++ (x&M)^C and then the corresponding LOP3 again. Scalar transcription differs for 65,502 of 65,536 states; state zero changes from 0.76806640625 to 1.07421875. Inspected callers reach quantization costs, quantized tile output, standalone decode and distribution diagnostics through decode_pcb wrappers. GEMM fragment unpacking uses the singly transformed paired decoder, creating a cross-path mismatch.

Locations: c4867edd0d31ea9fb052668874ae52fad0e91a0f:exllamav3/exllamav3_ext/quant/codebook.cuh — decode_3inst

Source evidence: call_798ae2b2e0064ea59220b9b7e021deaf, call_b29a7180935e4ca18214a0021f5f5cdb, call_ee403b4e4a9e4862be3b13fe3d771d95, call_e3180ff00444473cbaa39b6ddae33bfa, call_36b1ac7045864e9b92152f1390bca0d0, call_6c3dd0e5cc0b4fa1bf74522146e9e376

scalar_transcription: Enumerated all 16-bit states with modulo-2^32 multiply/add, single versus repeated mask/XOR, binary16 reinterpretation and rounded addition. [call_5d2d7372fa3c4965af8dd95f082476e2]. Limits: Python arithmetic model; no compiled decoder or GPU execution.

### missing-gemv-header (suspected; defect)

The eight compilation units introduce an include for an unavailable GEMV header.

Trigger: Compiling any changed exl3_comp_unit_1.cu through exl3_comp_unit_8.cu from the supplied repository contents.

Expected: The relative include ../exl3_gemv_kernel.cuh should resolve to a supplied header.

Actual: The parent quant directory has no such header, and the complete task diff adds none. Compilation is therefore expected to fail at include resolution unless an unprovided file supplies it; no GEMV implementation is registered by the new macro.

Locations: c4867edd0d31ea9fb052668874ae52fad0e91a0f:exllamav3/exllamav3_ext/quant/comp_units/exl3_comp_unit_1.cu — ../exl3_gemv_kernel.cuh

Source evidence: call_72a6a55a3c1e4b9793061ab2d65b5c54, call_2dacf31006b844eba57f0e5e642da301, call_5684dba9a42d459dbeb48c85da604fc3, call_e6ec6c5c924f4d5a9b17039422b20f96, call_8fd1adc7c0b746b9a95bd6325cce1e3a, call_d5354cbdfdb946a09e28a0f74f761fef, call_dd61403a0bbe4b7da185ec71011500d8, call_6d8534cbece24c7cad35951c8d6b30bb, call_36510c563c5d4681bcd2b230664b701c

source_inspection: Compared parent directory contents with every task diff section. [call_72a6a55a3c1e4b9793061ab2d65b5c54, call_ebfc66cc953a4feea4e142006eb8749a]. Limits: No build was attempted; externally supplied files are unestablished.

### inherited-boolean-threshold (suspected; defect)

The previously recorded Boolean threshold defect persists, while removal of the preceding shape-1 branch expands its reach.

Trigger: Automatic Hopper/Blackwell selection with bits<=6 and n<=4096, for example bits=3, k=16384, n=4096.

Expected: A dimensional threshold should be capable of distinguishing dimensions; the intended replacement condition is unestablished.

Actual: (size_k && bits >= 3) is Boolean and cannot exceed 8192, so this branch always returns shape 2. select_exl3_gemm_kernel calls it for nonpositive forced indices, and exl3_gemm invokes that dispatcher. Positive forced indices bypass the condition. The benchmark's automatic query is a concrete inspected caller, although its new eight-bit default bypasses this branch.

Locations: c4867edd0d31ea9fb052668874ae52fad0e91a0f:exllamav3/exllamav3_ext/quant/exl3_kernel_map.cu — select_gemm_shape

Source evidence: call_1e7cfa879bb4448caddd20d1ca66e744, call_b31697eb4e6b4a94a3b6e1afac95a55f, call_57e8e26eb5f44e5f9fe9d2df7fcabb2c, call_94191cc0fb404f2a950122f2af189016, call_a0d4b898153e40718246c84ee38b0c02, call_34808e6db0874dbaaa4480eedee1863f

source_inspection: Inspected the retained expression, changed preceding branches and native dispatcher callers. [call_1e7cfa879bb4448caddd20d1ca66e744, call_a0d4b898153e40718246c84ee38b0c02]. Limits: No performance consequence measured.

scalar_transcription: Modeled the Boolean comparison for three representative k values; all returned false. [call_5d2d7372fa3c4965af8dd95f082476e2]. Limits: Expression model, not repository execution.

## Uncertainty and limits

No CUDA compilation, GPU execution, assembly inspection or timing benchmark was performed.

Scalar checks model unsigned 32-bit arithmetic and binary16 rounding with standard-library Python; they do not execute PTX, tensor cores or concurrent memory operations.

The precise empirical rationale for the device-specific selection thresholds is not established by the inspected sources.

Caller reach is based on whole-parent literal searches and inspected native call sites; dynamic and external callers were not enumerated.
