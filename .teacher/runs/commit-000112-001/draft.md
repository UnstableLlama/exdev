# 4724b86d2f061a43d8c0da6bb118eeb04d708abf


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/4724b86d2f061a43d8c0da6bb118eeb04d708abf) · [Evidence ledger](draft.json)

Configures every Qwen3 MLP to retain half-precision gate/up intermediates while producing float32 down-projection outputs.

- [Qwen3 mixed-precision MLP output](#models)

## Problem

Qwen3 previously left both GatedMLP dtype arguments unspecified. Its FP16 and EXL3 linear implementations consequently allocated half-precision down-projection outputs by default. [source; call_0c4ce85b8954492ca2ec990ea9118ca8, call_278afee1f4b545ed9c1848ae11e59367, call_7605e834515c4971bdcb90fd12249388, call_372af164fb49496eb99717b817c35b56]

## Reasoning

The patch explicitly selects half-precision intermediates and float32 MLP output. This configures the down projection itself, rather than merely widening an already-rounded MLP result. [source; call_24e5b1dd2c1e4ed7b8df3f7340552672, call_278afee1f4b545ed9c1848ae11e59367, call_dfca461cb9014d8aa09eb228e4b7d958, call_7605e834515c4971bdcb90fd12249388]

A likely motivation is preserving down-projection range and precision without widening the larger gate/up intermediates. No inspected evidence identifies a specific failing prompt or measured accuracy improvement. [inference; call_24e5b1dd2c1e4ed7b8df3f7340552672, call_278afee1f4b545ed9c1848ae11e59367]

## Impact

The change applies to every Qwen3 decoder MLP, including each down-projection slice. It does not change weights, dimensions, attention configuration, or the shared GatedMLP defaults for other architectures. [source; call_24e5b1dd2c1e4ed7b8df3f7340552672, call_0c4ce85b8954492ca2ec990ea9118ca8, call_278afee1f4b545ed9c1848ae11e59367]

## Source Notes

The earlier Qwen3 entry describes architecture registration and reuse of existing transformer modules; this change adjusts that builder's numerical policy. [ancestor; call_1e948be42a49415bbb730372bb668501]

Issue #11, “AssertionError: bias is wrong datatype,” reports Qwen2 conversion failing on a bias assertion, followed by a reported fix. Its relationship here is only an inferred dtype-related comparison: its traceback names LinearEXL3, but the inspected parent already converts float bias to half, and this patch changes Qwen3 activation outputs instead. [inference; call_e53d840d93e546e6a37f6b05ab19d452, call_372af164fb49496eb99717b817c35b56, call_24e5b1dd2c1e4ed7b8df3f7340552672]

Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, concerns context-dependent RoPE scaling. The inferred connection is the shared Qwen3 identifier, not evidence that this MLP dtype change implements that request. [inference; call_9550b4795eef4ac4b9f5c568ac4034e8, call_24e5b1dd2c1e4ed7b8df3f7340552672]

<a id="models"></a>

## Qwen3 mixed-precision MLP output

Qwen3Model now passes interm_dtype=torch.half and out_dtype=torch.float to GatedMLP. GatedMLP propagates the former to gate/up Linear objects and the latter to every down Linear. Forward computes SiLU(gate) × up into the up buffer, projects down, and accumulates slice results before its final dtype conversion. [source; call_24e5b1dd2c1e4ed7b8df3f7340552672, call_278afee1f4b545ed9c1848ae11e59367]

Linear forwards its configured output dtype into both LinearFP16 and LinearEXL3 during loading and into LinearEXL3 during conversion. Both backends allocate their output using call override, configured dtype, then half as precedence. Thus the change affects the actual projection destination, including EXL3's reconstructed-weight and direct quantized paths. [source; call_dfca461cb9014d8aa09eb228e4b7d958, call_7605e834515c4971bdcb90fd12249388, call_372af164fb49496eb99717b817c35b56]

TransformerBlock supplies half-precision normalized MLP input, calls the MLP without an output override, and adds its result in place to the residual. The patch therefore widens the MLP result, not an explicit residual-buffer allocation; it does not establish that the entire block runs in float32. [source; call_4bc99c1f5852446c90231cccde2e6df7, call_24e5b1dd2c1e4ed7b8df3f7340552672]

Qwen/Qwen3-0.6B, Qwen/Qwen3-0.6B-Base, and Qwen/Qwen3-0.6B-FP8 each declare Qwen3ForCausalLM, SiLU, and hidden/intermediate dimensions 1024/3072. All three fit the unchanged MLP dimension mapping; the new activation dtypes are explicit builder choices, not their declared bfloat16 torch_dtype. [source; call_a5cc24dc1fd745b8b3808dbece1f66a5, call_7f2d474a3757418c94ff0acca726b4a1, call_71aa39e7888949f5863cd4828560a9de, call_0c4ce85b8954492ca2ec990ea9118ca8, call_24e5b1dd2c1e4ed7b8df3f7340552672]

Qwen/Qwen3-1.7B, Qwen/Qwen3-1.7B-Base, and Qwen/Qwen3-1.7B-FP8 each declare Qwen3ForCausalLM, SiLU, bfloat16, and dimensions 2048/6144. The same dimension mapping and explicit activation policy apply to each. [source; call_942c0acc57fd4693a9ba96729bcefb20, call_10ff342471d4447fa642df05cd4d5698, call_0f5d7e74fb4644dcb8e29fbec1b655c1, call_24e5b1dd2c1e4ed7b8df3f7340552672, call_0c4ce85b8954492ca2ec990ea9118ca8]

Qwen/Qwen3-4B, Qwen/Qwen3-4B-Base, and Qwen/Qwen3-4B-FP8 each declare Qwen3ForCausalLM, SiLU, bfloat16, and dimensions 2560/9728. The same dimension mapping and explicit activation policy apply to each. [source; call_33a22645489e43a98fffe401dd164882, call_73a16dc5e0a44cad9fb9cda104009578, call_609023c00ec44c50be67873ff7c4b7af, call_24e5b1dd2c1e4ed7b8df3f7340552672, call_0c4ce85b8954492ca2ec990ea9118ca8]

Qwen/Qwen3-8B, Qwen/Qwen3-8B-Base, and Qwen/Qwen3-8B-FP8 each declare Qwen3ForCausalLM, SiLU, bfloat16, and dimensions 4096/12288. The same dimension mapping and explicit activation policy apply to each. [source; call_fce60f201a014e8e9299c098972c318f, call_dd9833fa44834122b6d349553ed4f4ce, call_13028990352542939f8f79799133719e, call_24e5b1dd2c1e4ed7b8df3f7340552672, call_0c4ce85b8954492ca2ec990ea9118ca8]

Qwen/Qwen3-14B, Qwen/Qwen3-14B-Base, and Qwen/Qwen3-14B-FP8 each declare Qwen3ForCausalLM, SiLU, bfloat16, and dimensions 5120/17408. The same dimension mapping and explicit activation policy apply to each. [source; call_10db918c25054eb0ab4561f6f6cc4aed, call_8d624f74532e4b289a53e6b663384670, call_60d95246351b4c1a83c98b7467402be2, call_24e5b1dd2c1e4ed7b8df3f7340552672, call_0c4ce85b8954492ca2ec990ea9118ca8]

Qwen/Qwen3-32B and Qwen/Qwen3-32B-FP8 each declare Qwen3ForCausalLM, SiLU, bfloat16, and dimensions 5120/25600. The same dimension mapping and explicit activation policy apply to both. [source; call_6e026993522447c1b1c9696126846959, call_34fdcb4e5332407d8cd5584fcdb34728, call_24e5b1dd2c1e4ed7b8df3f7340552672, call_0c4ce85b8954492ca2ec990ea9118ca8]

A standard-library storage calculation gives float32 output bytes per token of 4096, 8192, 10240, 16384, and 20480 for hidden widths 1024, 2048, 2560, 4096, and 5120—twice half storage. A scalar illustration rounds 2049 to 2048 in half but preserves 2049 in float32. These calculations illustrate the storage/precision tradeoff, not measured model behavior. [execution; call_78b32033e9a545b4be3936fa36657fab]

## Uncertainty and limits

No model loading, inference, conversion, or GPU kernel execution was performed; native numerical behavior and performance remain unmeasured.

Configuration inspection does not establish checkpoint compatibility, particularly for FP8 variants.

The scalar check models storage and rounding only, not GEMM accumulation, activation kernels, or residual-add precision.
