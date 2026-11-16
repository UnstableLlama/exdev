# 456f14f95f7f0a840922128e571345124973ed15


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/456f14f95f7f0a840922128e571345124973ed15) · [Evidence ledger](draft.json)

Removes a duplicated mask/XOR operation from scalar 3INST decoding, restoring agreement with the unchanged paired decoder while retaining inline LOP3.

- [Restore single-pass scalar codebook decoding](#quantized-inference)

## Problem

The scalar 3INST decoder applied its mask/XOR transformation twice: once in C++ and again through inline LOP3. The paired decoder applied it only once. [source; call_629e58a3187744048a9e366da658c973]

## Reasoning

Removing the redundant C++ expression preserves the inline-instruction optimization while restoring the scalar decoder's agreement with the paired decoder; the multiplier and increment remain unchanged. [source; call_db12bf5fbd204f1abb86c59723d47b40, call_629e58a3187744048a9e366da658c973]

## Impact

The corrected scalar function feeds quantization error costs, reconstructed quantization tiles, standalone decoding and codebook-distribution diagnostics. Paired decoding is unchanged. [source; call_2c942ba41f274d2f8d573a76717b9c54, call_629e58a3187744048a9e366da658c973, call_db12bf5fbd204f1abb86c59723d47b40]

## Source Notes

The earlier GEMM optimization entry recorded the duplicated scalar transformation. Inspection of the parent and this deletion shows that specific defect is removed. [source; call_00792455bb7341b0ac81568f36c95cb2, call_629e58a3187744048a9e366da658c973, call_db12bf5fbd204f1abb86c59723d47b40]

PR #26, “Superior 3INST parameters,” was opened by louiehelm to propose different codebook parameters and also discusses combining mask/XOR with LOP3. Its connection here is inferred from the matching instruction and constants, not an explicit upstream link. This fix does not adopt the proposed parameters. [inference; call_a9f8df0e1cc649d08db31cefd03f7996, call_6855c913cf3d42dba1597ab7d572ff85, call_db12bf5fbd204f1abb86c59723d47b40]

<a id="quantized-inference"></a>

## Restore single-pass scalar codebook decoding

decode_3inst first mixes the state using 89226354*x + 64248484 in uint32 arithmetic. Mask 0x8FFF8FFF and XOR constant 0x3B603B60 then shape two binary16 bit patterns, whose halves are added. LOP3 immediate 0x6A encodes the combined AND/XOR operation; applying it after the equivalent C++ expression changes the codebook rather than merely repeating harmless work. [source; call_629e58a3187744048a9e366da658c973, call_db12bf5fbd204f1abb86c59723d47b40]

A standard-library scalar transcription enumerated all 65,536 16-bit states. The modeled LOP3 matched a single mask/XOR for every state, while the old double transformation changed rounded decoder outputs for 65,502 states. For state zero, the old result was 1.07421875 and the corrected result was 0.76806640625. [execution; call_f566f7e67a004f25bb2cdb291e8ceb61]

The 16-bit enumeration matches the standalone decoder's uint16 input and the distribution diagnostic's complete state sweep. Packed-weight helper dq also extracts a 16-bit state for scalar decoding; dq2 and dq4 use the unchanged paired decoder. The deletion therefore repairs a shared scalar primitive rather than changing packed-state extraction or introducing another quantization format. [source; call_2c942ba41f274d2f8d573a76717b9c54, call_b11f04d78e8f4a689c77cfaf54052c19, call_db12bf5fbd204f1abb86c59723d47b40]

## Uncertainty and limits

No CUDA compilation, GPU execution, model-quality evaluation or timing measurement was performed.

The Python check models modulo-2^32 arithmetic, the LOP3 truth table and binary16 rounding; it does not execute repository kernels.

Caller reach is established for inspected native call sites, not every external or dynamic workflow.
