# 754450f6ad4de88dce348f67099a61de14072237


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/754450f6ad4de88dce348f67099a61de14072237) · [Evidence ledger](draft.json)

Requests float MLP down-projection outputs throughout the shared Llama constructor, addressing a reported overflow without widening gate/up computation.

- [Widen MLP down-projection outputs](#llama-overflow)

## Problem

Llama's gated MLP previously left its down-projection output dtype unspecified, allowing the linear implementations to default to FP16. [source; call_3a16742c70b0438398bc8217bb3e5819, call_6ce1d9996b5540528848f1dea210d77d, call_23af333c594840d78cefad87ae9ab27c, call_b0eef314b8b84727a31d94d5c4241855]

## Reasoning

Requesting float output at construction reaches the down projection itself, rather than merely widening an already rounded MLP result. [source; call_2b6cfdecab9c45ef94aefa57ac3ffc8f, call_6ce1d9996b5540528848f1dea210d77d, call_cf3edfcb6ef44e3da23293d0df2e7f98]

## Impact

The shared constructor changes Llama, Mistral, Qwen2 and MiMo MLP down outputs; each inspected derivative delegates construction to LlamaModel. [source; call_9332f82f7b16461ab660a2f6b9f61630, call_28ce24331db84297ab5141df9f6325cd, call_4480929c56b64f4b9659448ce6d392cc, call_363e95d377d64242939d239553cb0545, call_2b6cfdecab9c45ef94aefa57ac3ffc8f]

## Source Notes

Read the original models chapter and the cache-allocation entry. The former establishes the shared Llama construction and records separate sliding-window mapping gaps; the latter concerns cache allocation, not MLP arithmetic. [ancestor; call_d6f2e1d2a3604431b12d8729d5e9ea8e, call_501104a7d7f94bf2969e74188c56bb3f]

Issue #52, “Error converting moonshotai/Kimi-Dev-72B,” reports Qwen2 conversion failures. Contributor turboderp proposed precisely this GatedMLP argument, and reporter artus-dev subsequently reported a successful conversion. [source; call_4e4aaa61e2b14c4f8725471fbd02c99d]

The relationship to #52 is inferred from its exact llama.py argument recommendation matching the patch, not from an explicit issue reference in the commit. [inference; call_4e4aaa61e2b14c4f8725471fbd02c99d, call_2b6cfdecab9c45ef94aefa57ac3ffc8f]

Related reports have different framing: #34, “torch._C._LinAlgError on last layer of quant,” concerns Command-A and suspected activation overflow; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” concerns Midnight-Miqu and also discusses a separate Command-R-Plus normalization problem. Their connection is inferred from shared conversion failures and Linear traceback paths, not established as the same defect. [inference; call_23fc359534494461b2bd42fa488ccd8c, call_5bbaa2dad157483b9b1bd8a4d45894ef, call_cf3edfcb6ef44e3da23293d0df2e7f98]

<a id="llama-overflow"></a>

## Widen MLP down-projection outputs

The sole edit passes out_dtype=torch.float to every GatedMLP constructed by LlamaModel. GatedMLP stores that preference and passes it to every down Linear, including sliced down projections; gate/up projections retain their separate interm_dtype setting. [source; call_2b6cfdecab9c45ef94aefa57ac3ffc8f, call_6ce1d9996b5540528848f1dea210d77d]

Linear preserves the preference when loading FP16 or EXL3 weights and when replacing an FP16 implementation during conversion. LinearFP16 allocates the requested output before multiplication. For half inputs and float outputs it selects ext.hgemm, whose inspected implementation requires half operands and uses float output with CUBLAS_COMPUTE_32F. [source; call_cf3edfcb6ef44e3da23293d0df2e7f98, call_23af333c594840d78cefad87ae9ab27c, call_87fc5b29b1fa44b4a9674b5f236a1aaa]

LinearEXL3 resolves its return dtype from the call override, stored preference, then half fallback. Both its reconstructed-weight and direct EXL3 paths allocate that dtype. GatedMLP adds slice results in place, then TransformerBlock adds the MLP result to the residual without imposing a half output override; its normalization input to the MLP remains half. [source; call_b0eef314b8b84727a31d94d5c4241855, call_6ce1d9996b5540528848f1dea210d77d, call_35ce25c620e941998a0bdc5949830867]

A bounded standard-library storage example computed 35000+35000=70000: binary16 storage overflowed while binary32 retained 70000. Its decoded largest finite half was 65504, and storage sizes were two versus four bytes per element. This illustrates the range benefit and doubled down-output storage, not measured model accuracy or GPU behavior. [execution; call_4e5548008bc743dfa09fd9d9c06a072c]

The design targets the output boundary rather than clipping activations or widening the whole MLP. That preserves the existing gate/up path while giving down results more range; preventing the final-layer overflow hypothesized in #52 is the supported motivation, not proof that all nonfinite-state failures are resolved. [inference; call_2b6cfdecab9c45ef94aefa57ac3ffc8f, call_6ce1d9996b5540528848f1dea210d77d, call_4e4aaa61e2b14c4f8725471fbd02c99d]

## Uncertainty and limits

No repository model, conversion job or CUDA kernel was executed. The issue reporter's successful conversion is historical testimony, not a measured result from this session.

The scalar check models storage range only: Python raises OverflowError for the chosen half conversion; it does not reproduce CUDA overflow handling, accumulation order or quantized transforms.

Widening down outputs does not establish protection against overflow in gate/up projections, activation multiplication or every quantized intermediate. Runtime memory and performance effects were not measured.
