# 94514ae02a7d2b14cd3348b94b64e2b3388139c7


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/94514ae02a7d2b14cd3348b94b64e2b3388139c7) · [Evidence ledger](draft.json)

Adds a default-preserving Linear loading option for weights already stored in internal orientation, without changing fused loading, EXL3 storage or export orientation.

- [Explicit weight orientation at the Linear loading boundary](#modules)

## Problem

Ordinary Linear weights were always transposed during loading, preventing callers from declaring weights already stored in the internal [input, output] orientation. [source; call_96e8f97e115147af812c6e1d3edbe311, call_0600185e3a9f465f801771b1afaa8b13]

## Reasoning

The change makes orientation an explicit per-layer choice rather than inferring it from dimensions. Keeping transposed_load=True preserves existing callers; False skips the loader transpose without changing the projection's internal layout. [source; call_96e8f97e115147af812c6e1d3edbe311, call_9f51d3f48b974e2ead4ef357fb7a4e2e, call_0600185e3a9f465f801771b1afaa8b13]

## Impact

This adds a construction-time capability, not an architecture implementation or automatic checkpoint detection. The diff changes no model constructor to select False. [source; call_96e8f97e115147af812c6e1d3edbe311, call_a87284887e514f9d939b977d3fcf555d]

## Source Notes

The initial implementation's modules chapter was read. It establishes Linear's storage-independent interface, EXL3-first loading order, fused-weight slicing and conversion handoff. [ancestor; call_6c9b401205d847b287c5c511bae079ea]

Related reports were inspected: #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” concerns vocabulary padding; #11, “AssertionError: bias is wrong datatype,” concerns bias conversion; #16, “RuntimeError: CUDA error: invalid configuration argument,” was discussed as tokenizer truncation; #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” concerns padding before slicing. Their connection here is inferred from shared linear.py paths, particularly #38's load_fp16/get_tensor traceback, not evidence that this change fixes those reports. [inference; call_69ba11b7f0b74a1fb9ebccd17105ae13, call_049def02e688405886dfaba8af6f920b, call_77a34d0646f64323a37fdb095a4b1b3a, call_1e9b9dca78094011a1285fc5d8599632, call_96e8f97e115147af812c6e1d3edbe311]

Other inspected reports concern different failures: #34, “torch._C._LinAlgError on last layer of quant”; #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values”; and #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” describe calibration/factorization problems. #33, “Error converting model,” initially reports file-opening failure and later discusses GLM4 sampling. Connections to this task are inferred only from shared Linear conversion or safetensors-loader paths; none establishes a transpose-related motivation. [inference; call_0eaab466841241748641b4b43e83e142, call_71fbea4414da4e46802d68a3f318158f, call_17732d8fa7734a08b16ffd98af8bfcdc, call_08132e7b1c004c95a1d12a41be2d108f, call_ee5c5fe1ab7f416a8aef2385eb6fe986, call_96e8f97e115147af812c6e1d3edbe311]

<a id="modules"></a>

## Explicit weight orientation at the Linear loading boundary

Linear.__init__ appends transposed_load=True and stores it on the instance. load_fp16 passes that value as get_tensor's transpose argument for an ordinary key.weight. These edits are dependent: storing the option supplies the value consumed by loading. [source; call_96e8f97e115147af812c6e1d3edbe311]

LinearFP16 consumes [input, output] weights through x @ weight. Thus True converts conventional [output, input] storage, while False accepts storage already in internal orientation. SafetensorsCollection applies the choice in both direct loaders and deferred-load completion; its in-memory new_tensors branch also honors transpose. [source; call_0600185e3a9f465f801771b1afaa8b13, call_9f51d3f48b974e2ead4ef357fb7a4e2e, call_96e8f97e115147af812c6e1d3edbe311]

Padding still targets (in_features, out_features), with dimensions rounded to multiples of the existing pad_to default, 128. Sliced layers still load the full weight on CPU without loader padding, then let LinearFP16 select input/output slices and move them to the target device. Bias and optional scale loading are unchanged. [source; call_8817bd4ec7874febba243f3802083c15, call_0600185e3a9f465f801771b1afaa8b13, call_96e8f97e115147af812c6e1d3edbe311]

The option affects ordinary primary or alternate weights only. EXL3 remains preferred and does not consume it. The fused fkey fallback retains its explicit weight.T; exporting LinearFP16 tensors likewise always transposes back to conventional storage. Conversion's get_weight_tensor continues receiving internal orientation, so the flag is not an export-format selector. [source; call_8817bd4ec7874febba243f3802083c15, call_0600185e3a9f465f801771b1afaa8b13, call_96e8f97e115147af812c6e1d3edbe311]

Whole-tree caller inspection found unchanged default-compatible construction in Attention's four projections; MLP and GatedMLP projections; BlockSparseMLP's router and experts; and the output heads in cohere, cohere2, decilm, gemma2, gemma3, glm4, llama, mixtral, phi3, qwen3 and qwen3_moe. None supplies the new argument. The Python scan found no direct Linear subclass or pre-existing transposed_load reference. [source; call_b12c64c381e34fe2aed566d150a95a5e, call_a87284887e514f9d939b977d3fcf555d, call_96e8f97e115147af812c6e1d3edbe311]

A scalar orientation check produced [30, 39, 48] for both a conventional 3×2 checkpoint transposed on load and an already-oriented 2×3 checkpoint left unchanged. It also checked that existing 128-element rounding maps dimensions (128, 129) to (128, 256). [execution; call_c7843ed4d0ea4dc5881cce37da0c11e8]

## Uncertainty and limits

No repository model, tensor loader or GPU kernel was executed. The scalar check models orientation algebra using Python integers, not FP16 conversion, padding copies or deferred device transfers.

The new option requires callers to know checkpoint orientation; compatibility with external constructors and real transposed checkpoints was not demonstrated.
