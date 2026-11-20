# dd053a205d253e3610bbe224e4bb828a6a562ee4


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/dd053a205d253e3610bbe224e4bb828a6a562ee4) · [Evidence ledger](draft.json)

Adds per-module memory estimates and a greedy tensor-parallel split planner for KV heads, channels, MLP slices, and experts. It emits device ranges but is not wired into loading; scalar checks expose budget and workspace-accounting limits.

- [Estimate tensor-parallel splits before loading](#tp-split)

## Problem

The parent can place whole modules on successive GPUs by loading them and running a dummy forward pass, but its tensor-parallel loading branch raises NotImplementedError. The commit titled “TP: Auto layer split logic” adds the cost model and planner for splitting within modules; it does not wire that planner into model loading. [source; call_a3a422b189f2457b9bb96bfe8275fbfb, call_c371ef742b434e86aa4fc2f4abbda292, call_368480094ac744c1a77bf577252332a6]

## Reasoning

The planner separates persistent bytes, which accumulate across components, from temporary bytes, for which it retains one maximum per device. This gives a cheap estimate without loading a model. Compared with the existing dummy-forward loader, it can express finer assignments, but it does not measure allocator fragmentation, check fit after each assignment, or move work back off an over-budget device. [inference; call_368480094ac744c1a77bf577252332a6, call_c371ef742b434e86aa4fc2f4abbda292]

The edits supply one another's prerequisites: Linear adds size queries used by attention and feed-forward modules; the two cache implementations satisfy the new CacheLayer abstract methods used by Attention; MLP constructors retain dimensions needed by their estimators. These records are then suitable as inputs to TPAllocator. They are not requests to load or shard tensors. [source; call_c5c650e23a754602a81b0782e99d51e4, call_8b83a1af6f9644c2a6e9000d6c5d3e6a, call_d39c35ac8ad7416eb065daec98440baf, call_7c3b30d7166c431fbc034cad7047c25b, call_92dd2016fccb439a8149f064e04804e5, call_1f3b3a2bbfb44cebaa88c7e6b2de3491, call_e9d34090519443fcb3bc67944fc5fb92, call_368480094ac744c1a77bf577252332a6]

## Impact

The CLI already passes its tensor-parallel flag to Model.load. The task leaves that route and the whole-module autosplit implementation unchanged. The whole-parent literal search found no make_tp_allocation callers; the task adds direct calls from the new recursive Module method and from BlockSparseMLP to its shared experts, but adds no model-level caller. [source; call_1bd2c77b77b1431f8b37765333852a98, call_c371ef742b434e86aa4fc2f4abbda292, call_5012b4cd639d4b7badfb9c43d2c01c8a, call_d976daf7c93a40c5887029982d217a84, call_e9d34090519443fcb3bc67944fc5fb92, call_368480094ac744c1a77bf577252332a6]

Both explicitly derived in-tree CacheLayer implementations implement the new methods. A custom class passed through Cache(layer_type=...) must now implement both to remain concrete. The abstract Module.forward signature gains a half default, but a parent AST scan found that each concrete forward definition in the modules directory still uses its own None default; the change does not make ordinary calls dispatch with half. [source; call_cc8b181e3b9944a9845414f0b85102cc, call_c2bb255d10564de08629052798670d65, call_c5c650e23a754602a81b0782e99d51e4, call_8b83a1af6f9644c2a6e9000d6c5d3e6a, call_d39c35ac8ad7416eb065daec98440baf, call_d976daf7c93a40c5887029982d217a84, call_9cc392da195d494d9eb82afcb74c4f85]

## Source Notes

The initial modules chapter describes explicit child registration and separate projection implementations. The paged KV compression entry describes the two packed buffers, two scale buffers and full-size FP16 reconstruction; it also records a zero-block scale issue and a mismatched-detach diagnostic. The projection-injection entry records the combined-KV attribute mismatch. The optional-input-norm entry describes the sequential block's FP16 fallback and records separate forward and quantization limitations. [ancestor; call_e6929fa3de834fdd8f2b4b777497d508, call_851c4041c6d04095b3bac8f3897bc9b9, call_738786e2656440228e48ce1c757b4e13, call_8e437dfa14b149dc8363b0ffbc8317df]

The TP collection code does not repair the inherited runtime paths. Attention's load probe and projection fallback still access separate K/V, and the TP estimator adds another such access. TransformerBlock keeps the existing sequential FP16 fallback; the unchanged parallel forward still dereferences its inputs unconditionally, and neither block's separate allocate_q path is changed to support the plain MLP's singular up/down attributes. The conversion loop calls allocate_q, not the TP estimator; the separate exact-budget bisect boundary is unchanged. [source; call_202085b3d8874b1daf8651723ee6dc9e, call_92dd2016fccb439a8149f064e04804e5, call_5330001a85e844349488c8128b490762, call_4bc53cb24fa64870a9dc57ed8db2a4d9, call_1b95029705b04de48dff21728d99a8cd, call_d5032e3d9a9749bd91d3e7c4c342e05a, call_b636739869e646a69d8553de670c856c]

Two earlier reports share the unchanged loader's error string: #61, “Run ERNIE-4.5-300B-A47B-PT 2.25bpw with 5x20G 3080 got 'Insufficient VRAM',” traces directly to _load_autosplit and reports success after switching allocator backend; #50, “RuntimeError: Insufficient VRAM in split for model and cache despite remaining 1GB VRAM (exllamav3 + tabbyAPI),” asks about apparent headroom and discusses transient dummy-forward allocations. #54, “GPU split isn't followed here?”, discusses why whole-layer placement and transient allocations differ from observed steady-state GPU use. These are context for the tradeoff, not evidence that the new estimator was motivated by or fixes those reports. [inference; call_f37764a65b3d479a9284f1e466fc0c91, call_03e6c82bf1b64375a972d9e498530e7d, call_0b65e7f5b13b431fa44162ceeefb5315, call_4662f1bc202a4f62b134d4d5e13abeac, call_c371ef742b434e86aa4fc2f4abbda292]

Other closed reports overlap in touched files, not in the new planning calls: #8, “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800,” reports vocabulary-projection conversion padding; #11, “AssertionError: bias is wrong datatype,” reports an EXL3 bias assertion reached from Linear.convert_exl3; #16, “RuntimeError: CUDA error: invalid configuration argument,” reports an Attention-to-Linear Hessian-capture traceback and discusses tokenizer truncation; #38, “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1,” reports a tensor-size mismatch in sliced MLP loading through Linear.load_fp16; #55, “Possible GLM4 32B regression,” reports an int/None comparison in the FP16 loader. #43, “Error converting abliterated Qwen3 mlabonne/Qwen3-30B-A3B-abliterated,” and #58, “linalg.cholesky error converting OpenBuddy (Qwen3) 32B QAT,” trace from Linear.convert_exl3 into Cholesky factorization, not TP estimation. [inference; call_8b8552f3671e49aeaa8ccb3d4482ced4, call_e0eaa8cd9c474dcea02a5177c47593b1, call_828e269104654e05b1acfa779cf19863, call_7728da4f75144ef086de00377a535aec, call_7ab9a8457fa044cd84f2dcb3a8ee4b11, call_04d509e6092f428bbf63db914ae3fbff, call_611a17d8bbe5477e94b298391b5c4f30, call_e88c45ff9a9841f6a3af36f06798b7a2, call_7c3b30d7166c431fbc034cad7047c25b]

The open discussions also overlap only in narrower ways. #1, “Cache Quantization Strategy,” describes the independent K/V rates and scale overhead that the estimator now counts. #7, “quantizing model: undefined symbol: __cxa_call_terminate,” mentions Model in an extension-import traceback. PR #26, “Superior 3INST parameters,” proposes a quantizer multiplier, not placement logic. #33, “Error converting model,” reports a file-open error through the inspected compile and safetensors modules. #34, “torch._C._LinAlgError on last layer of quant,” #42, “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values,” and #52, “Error converting moonshotai/Kimi-Dev-72B,” concern conversion through Linear. #53, “Command A support,” is framed as a model-support request, with conversion discussion. #48, “`RuntimeError` when requesting logprobs with Gemma 3 models,” overlaps through Gemma3 and the vocabulary projection but reports a logits-buffer copy mismatch. [inference; call_9e8b11da848e4853a036f14143e5d86d, call_33656e7259fa417ab2f7652392b6c266, call_aee76575f0f64228b4a4cba57111237c, call_1926203e519944c8b23cde91bde59621, call_ecf96b2d59884c8db636502ccb98fcf7, call_b9d1029888624f9c8642e8d8ed14090e, call_a32d6fd4a7d24e21828ed2d523ae6227, call_a09eb81436b2479fac93f5667c5adcb0, call_4dcea8849cdb48c59afade892b145d76]

<a id="tp-split"></a>

## Estimate tensor-parallel splits before loading

TPAllocation describes replicated and shardable storage, replicated and shardable overhead, reconstruction workspace, and a logical partition axis. Module.make_tp_allocation concatenates records in registered-child order. The sequential and parallel transformer blocks inherit that traversal. Embedding and PosEmbedding return no records; Conv explicitly raises. Mistral3PatchMerger can recurse into its registered Linear, while Gemma3MMPool is a childless module without an override. [source; call_368480094ac744c1a77bf577252332a6, call_d976daf7c93a40c5887029982d217a84, call_4543e2c9dc604c8d816c6adb72fcb4f1, call_5330001a85e844349488c8128b490762, call_4bc53cb24fa64870a9dc57ed8db2a4d9, call_f390d4cde2614cfa9ff6f6d37260ebe6, call_67fb9722df794eefa84da01322fb313c, call_171e4e7e96b949ac99f85b06e6a47af8, call_5140e8227cef41b282ebbeb5ce31a805, call_c648f6b600d44d76bd62cedb1ab9c258]

Linear caches the primary-key storage estimate: an EXL3 group requires trellis plus one form each of the input and output scales; the estimator then sums tensor byte sizes under that prefix. Otherwise, storage and reconstruction each use two bytes per element of the padded matrix, not a measurement of a loaded tensor or a bias-inclusive FP16 count. The same header-size API already served conversion shard packing and Model.get_storage_info. LayerNorm and RMSNorm count their prefix bytes as replicated storage and estimate one output row as floor(storage_bytes/2) times output item size; this is a proxy, not a lookup of the actual normalized width. [source; call_7c3b30d7166c431fbc034cad7047c25b, call_dd4a2551406543cbade106ae6b0c64c0, call_a2f85e8e9f3347c296cd3d265c104d0c, call_2d85d18af20645c0b614a6e34cdedf71, call_b41605de767145a696cad53e7520c0da, call_c371ef742b434e86aa4fc2f4abbda292, call_4eb2b81a95564ed3ba1abfee0e1baea6, call_4a4a9841086147018062aca8e3fd7fe5]

Attention groups four projection estimates and every attached cache under the attn limit, splitting by whole KV heads. It charges a replicated hidden-width output, two half-width query-head vectors for Q/O and two half-width KV-head vectors for K/V, plus cache overhead. Reconstruction is the maximum of the four projection estimates. FP16 cache storage is two full-capacity half tensors, with no separate reconstruction buffer; quantized storage is two packed int32 payloads with independently sized K/V bitplanes and two FP16 scale arrays, one scale per 32 values per tensor. Quantized get_kv allocates just one pair of full-capacity half tensors per call. [source; call_92dd2016fccb439a8149f064e04804e5, call_c2bb255d10564de08629052798670d65, call_1e944e009be54fd3a85f9f5e5eea9046, call_8b83a1af6f9644c2a6e9000d6c5d3e6a, call_83c3c71a5aa84315bcea984e19661abf, call_d39c35ac8ad7416eb065daec98440baf]

Standalone Linear partitions padded output width in 128-channel blocks; plain MLP uses that granularity for intermediate width and combines up/down storage. GatedMLP combines all gate/up/down storage, charges two intermediate vectors plus an extra half vector when interm_dtype is not half, and switches from 128-channel chunks to existing slices for an already sliced module. The existing slicer aligns the base slice width to 128 and leaves the remainder in the last slice. The planner still prices slices uniformly and uses only the first slice's projections for the reconstruction bound; its display multiplies slice counts by 128 as well. BlockSparseMLP instead uses one expert per unit, includes the router in the split storage total, budgets four intermediate vectors plus the conditional half vector, and appends a separate estimate for any shared experts. [source; call_dd4a2551406543cbade106ae6b0c64c0, call_7c3b30d7166c431fbc034cad7047c25b, call_1f3b3a2bbfb44cebaa88c7e6b2de3491, call_1b95029705b04de48dff21728d99a8cd, call_e9d34090519443fcb3bc67944fc5fb92, call_885ad170e7d94c52bde72b516f0c9c0e, call_368480094ac744c1a77bf577252332a6]

initial_split walks components in order. It subtracts accumulated storage and peak overhead from each budget, clips negative room to zero, and optionally keeps only the devices with the most remaining room using the component limit or a dev_limits override. ratio_split gets unit-sized chunks, floors each nonnegative proportional quota, and gives leftovers to the largest fractional remainders. The planner adds the replicated charges on positive-room devices and prorates the split charges by each rounded share using integer division. Only split overhead gets the token multiplier, using output_num_tokens for the final component object and num_tokens otherwise. compile_tp_plan turns the splits into consecutive half-open logical ranges per device and key, including empty ranges; only print_split scales the counts by channel_width, and its label 'GB' uses a GiB divisor. [source; call_2ee6dc3b4f734965bbde6924c5473cff, call_368480094ac744c1a77bf577252332a6]

A standard-library transcription gave 4,194,304 bytes of FP16 K/V storage at 1,024 cache tokens, eight KV heads and head width 128. Four-bit keys and six-bit values used 1,441,792 persistent bytes plus the same 4,194,304-byte FP16 reconstruction pair. Applying the planner's token multiplier to that pair alone for eight forward tokens on one device gives 33,554,432 estimated bytes. [execution; call_c421c73f513d4f1d8e044fece19f697a, call_9cc392da195d494d9eb82afcb74c4f85]

## Authoring-time findings — pending review

### split-can-exceed-budget (suspected; defect)

Positive residual capacity is used as a weight, not as a feasibility check.

Trigger: Call initial_split with maximum byte budgets [4, 4] and a component with storage_per_device=5 and otherwise default sizes.

Expected: A capacity-aware plan should reject the infeasible replica or account for it before assigning work.

Actual: The method marks both devices active, rounds the logical split to [1, 0], charges both devices for the replica, and returns [5, 5] without rejecting the over-budget result. compile_tp_plan can still turn the logical split into ranges.

Locations: dd053a205d253e3610bbe224e4bb828a6a562ee4:exllamav3/util/tp_split.py — TPAllocator.initial_split / compile_tp_plan

Source evidence: call_368480094ac744c1a77bf577252332a6, call_2ee6dc3b4f734965bbde6924c5473cff

scalar_transcription: Transcribed the rounding and accounting for one component and obtained the over-budget estimate. [call_c421c73f513d4f1d8e044fece19f697a]. Limits: Direct planner input; no model-loading caller or GPU behavior was verified.

### zero-split-denominator (suspected; defect)

The initial split has no explicit infeasible-budget or zero-channel path.

Trigger: Pass a nonempty device list whose clipped remaining capacities are all zero; separately, pass a component with channels_to_split=0 and positive room.

Expected: Report infeasible capacity or reject an empty partition axis before dividing.

Actual: For zero room, ratio_split divides quotas by the zero total weight. For zero channels with room, it returns zero shares, then initial_split divides the byte costs by the zero channel count.

Locations: dd053a205d253e3610bbe224e4bb828a6a562ee4:exllamav3/util/misc.py — ratio_split, dd053a205d253e3610bbe224e4bb828a6a562ee4:exllamav3/util/tp_split.py — TPAllocator.initial_split

Source evidence: call_368480094ac744c1a77bf577252332a6, call_2ee6dc3b4f734965bbde6924c5473cff, call_c1baaf505b50431da55b74c70eae0f26

scalar_transcription: Both direct examples raised ZeroDivisionError with built-in Python integers. [call_c421c73f513d4f1d8e044fece19f697a]. Limits: Does not establish how all NumPy operand combinations behave or how often either input occurs in a real model.

### cache-scratch-scaled-by-query-tokens (suspected; defect)

A full-cache temporary is counted as a per-forward-token temporary.

Trigger: Estimate an attention component with an attached quantized cache and more than one forward token.

Expected: Count the full-capacity K/V reconstruction pair once per call, separately from query-token-dependent activations.

Actual: CacheLayer_quant.overhead_size already covers the whole cache. Attention adds it to overhead_to_split, so initial_split multiplies it by the token count again before prorating. Conversely, overhead_per_device is documented per token but is charged once without a token multiplier.

Locations: dd053a205d253e3610bbe224e4bb828a6a562ee4:exllamav3/modules/attn.py — Attention.make_tp_allocation, dd053a205d253e3610bbe224e4bb828a6a562ee4:exllamav3/util/tp_split.py — TPAllocator.initial_split

Source evidence: call_83c3c71a5aa84315bcea984e19661abf, call_d39c35ac8ad7416eb065daec98440baf, call_92dd2016fccb439a8149f064e04804e5, call_368480094ac744c1a77bf577252332a6

scalar_transcription: For the example cache, checked that the 4 MiB reconstruction pair is charged as 32 MiB at eight forward tokens on one device. [call_c421c73f513d4f1d8e044fece19f697a, call_9cc392da195d494d9eb82afcb74c4f85]. Limits: The arithmetic isolates the cache term and is not a peak-VRAM measurement.

### empty-block-cannot-emit-empty-plan (suspected; defect)

The generic collector rejects an already supported no-op sequential block.

Trigger: Call make_tp_allocation with assertions enabled on a DeciLM block whose attention and FFN configurations both have no_op set, leaving all four corresponding children unset.

Expected: Return no records for a block with no weights or computation, as the existing quantization allocator skips such a block.

Actual: register_submodule ignores None, so the inherited collector encounters an empty child list and asserts. Gemma3MMPool has the same childless fallback if queried directly; separately, traversal of either inspected vision model encounters an explicit unsupported Conv at the front.

Locations: dd053a205d253e3610bbe224e4bb828a6a562ee4:exllamav3/modules/module.py — Module.make_tp_allocation

Source evidence: call_27d0e612376a4782b0ca31707e67dfc2, call_63cc1d7441b14f198467d680d51ad875, call_c2a32bb4408c4bf688d31e5ca92e12e1, call_5330001a85e844349488c8128b490762, call_4543e2c9dc604c8d816c6adb72fcb4f1, call_d976daf7c93a40c5887029982d217a84, call_171e4e7e96b949ac99f85b06e6a47af8, call_5140e8227cef41b282ebbeb5ce31a805, call_c648f6b600d44d76bd62cedb1ab9c258

source_inspection: Traced the constructors and child registration into the new collector; no model loader invokes it at this commit. [call_5012b4cd639d4b7badfb9c43d2c01c8a, call_d976daf7c93a40c5887029982d217a84, call_c371ef742b434e86aa4fc2f4abbda292]. Limits: Direct collection is the trigger, not normal loading or forward execution.

### tp-estimator-still-requires-separate-kv (suspected; defect)

TP estimation assumes more than Attention's constructor guarantees.

Trigger: Construct Attention with ordinary named Q/output projections, a falsy key_k and a supplied kv_proj, then ask it for a TP allocation directly or through its containing block.

Expected: Account for the combined child or explicitly reject that projection form.

Actual: The estimator calls storage_size on the absent k_proj. Load and the project_qkv fallback still have the preexisting separate-K/V assumption. The source scan found 19 explicit named Attention constructions, all with named Q/K/V/O and none using injection.

Locations: dd053a205d253e3610bbe224e4bb828a6a562ee4:exllamav3/modules/attn.py — Attention.make_tp_allocation

Source evidence: call_202085b3d8874b1daf8651723ee6dc9e, call_92dd2016fccb439a8149f064e04804e5, call_6be7f756354d41e880fc09c162eaaea3, call_da29420d35af4403a99b74f76deb5151

source_inspection: Compared constructor branches and their consumers, and scanned parent Python constructor call forms. [call_202085b3d8874b1daf8651723ee6dc9e, call_92dd2016fccb439a8149f064e04804e5, call_c421c73f513d4f1d8e044fece19f697a]. Limits: Conditional on a custom call form; no Attention instance ran.

### inherited-cache-detach-diagnostic (suspected; defect)

The inherited mismatched-layer detach diagnostic is unchanged.

Trigger: Detach a Cache from a model with a different cache-layer count, with assertions enabled.

Expected: Raise an AssertionError reporting the incompatible counts.

Actual: Formatting the assertion tries to call the integer model_num_layers and raises TypeError instead. The inspected loading example detaches from the original model, so it does not ordinarily take this branch.

Locations: 0460dda4e410e1311c8474b1c1e980b6cbbba152:exllamav3/cache/cache.py — Cache.detach_from_model

Source evidence: call_c2bb255d10564de08629052798670d65, call_c5c650e23a754602a81b0782e99d51e4, call_6e0d461404d34616959c0b66a8dc632c, call_a62a1504389348618c2563f4e1bedc53

source_inspection: Checked the unchanged assertion and the explicit caller found in the parent. [call_c2bb255d10564de08629052798670d65, call_a62a1504389348618c2563f4e1bedc53]. Limits: No detach workflow executed.

### inherited-zero-cache-scale (suspected; defect)

Adding cache size queries does not change the earlier zero-scale quantization case.

Trigger: Encode an all-zero group of 32 values through the quantized cache update.

Expected: Encode zeros without a zero denominator.

Actual: The CUDA helper converts the 1e-10 scale floor to half before dividing, leaving a zero denominator. The update path still calls the paged quantizer; the new sizing methods do not invoke it.

Locations: 0460dda4e410e1311c8474b1c1e980b6cbbba152:exllamav3/exllamav3_ext/cache/q_cache_kernels.cuh — quant_block

Source evidence: call_e37eeb9072ce4986bc60594743fd387a, call_83c3c71a5aa84315bcea984e19661abf, call_d39c35ac8ad7416eb065daec98440baf

scalar_transcription: Standard-library binary16 conversion rounds the scale floor to 0.0. [call_9cc392da195d494d9eb82afcb74c4f85]. Limits: Does not establish CUDA integer conversion or final decoded output.

## Uncertainty and limits

No model load, Torch tensor allocation, GPU kernel, or distributed forward was executed. The arithmetic checks use Python integers and ordinary Python division; they do not reproduce NumPy fixed-width overflow, GPU rounding, CUDA allocator behavior, or communication costs.

The source does not establish estimator accuracy on a real checkpoint. Attention explicitly leaves FlashAttention temporary VRAM unmodeled, and the sparse MLP marks its routing and gate workspace estimate as incomplete.

Caller searches cover explicit source references; dynamically assembled modules, external CacheLayer subclasses, and external planner consumers were not exercised. The commit message states the purpose but does not identify a motivating report or establish the rationale for all heuristic choices.
