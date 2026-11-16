# a39fdfc4d5bdac1c677eecefbb1932b586c0dca9


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/a39fdfc4d5bdac1c677eecefbb1932b586c0dca9) · [Evidence ledger](draft.json)

Preserves model-supplied epsilon and weight bias for fused Q/K normalization by restricting defaults to attention without head norms; native kernel concerns remain unchanged.

- [Preserve head-normalization parameters](#attention)

## Problem

Attention copied epsilon and constant bias from its Q head norm, then unconditionally overwrote them with 1e-6 and 0.0. This discarded model-specific settings before fused normalization. [source; call_9326d23dda8a47bc88b44029f988018a]

## Reasoning

Moving both defaults into the no-head-norm branch preserves supplied normalization settings without changing the no-norm initialization or the native interface. [source; call_c2b94c06da76452c9903cea249d6983b]

## Impact

Gemma3's paired head norms retain their explicit unit bias. Qwen3 and Qwen3 MoE retain their configured epsilon; their omitted constant bias already defaults to zero. All three attention backends forward the preserved values when RoPE is active. The separate RMSNorm path without RoPE already uses each norm's own settings. [source; call_960df13d6f894d93b98e2671a8745cf9, call_2875999e852044a9aa22513ad4a583a5, call_cb9a253bc32248b694d6fa10f0411d12, call_cca541f8f7fe4c51b06bbc7b9bfc7779, call_9326d23dda8a47bc88b44029f988018a]

## Source Notes

Read the normalization-fusion ancestor entry, which records the overwritten settings and separate native reduction and bounds concerns. The task removes the settings overwrite, not those native concerns. [ancestor; call_ec0ce23bc56241019e204b07fb58a365]

Issue #16, “RuntimeError: CUDA error: invalid configuration argument,” concerns conversion and a discussion-attributed tokenizer truncation problem. Issue #7, “quantizing model: undefined symbol: __cxa_call_terminate,” concerns extension loading. Issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, concerns scaling policy. Their connection here is inferred only from attention or rope.py path overlap, not evidence that this fix addresses them. [inference; call_814f45f4c4d342a1993a6aa5e38cf246, call_5c9134d62c274c7c88e78578a3cadda7, call_3deae48e03894a2f90bd0b8f04ec12c5]

<a id="attention"></a>

## Preserve head-normalization parameters

The constructor requires K norm when Q norm is supplied and checks their epsilon equality. It caches Q's epsilon and constant bias for the fused path. The patch makes the fallback assignments mutually exclusive with those copies; tensor loading and backend selection remain unchanged. [source; call_c2b94c06da76452c9903cea249d6983b, call_9326d23dda8a47bc88b44029f988018a]

Attention.load obtains Q/K weight tensors. Each decode method passes those tensors and the cached scalars through RoPE.apply to ext.rope. The kernel normalizes using reciprocal sqrt(mean(x²)+epsilon), then multiplies by weight plus constant bias before rotation. Thus 1e-6 is a denominator stabilizer, while zero means no weight offset—not an additive activation bias. [source; call_9326d23dda8a47bc88b44029f988018a, call_d44125266ac8419188966e463c94a65b, call_b2830fd3f9604da687c684731e1ec524]

An isolated assignment check preserved the no-norm result (1e-6, 0), changed a supplied unit-bias case from (1e-6, 0) to (1e-6, 1), and changed a supplied nondefault-epsilon case from (1e-6, 0) to (1e-5, 0). [execution; call_65cac10d07fc41af819dceaa81479923]

The existing test passes normalization parameters directly to RoPE.apply; the science sampling utility omits them and retains no-normalization defaults. Neither consumes Attention's cached scalars at those direct calls, so this constructor edit does not change those calls. [source; call_8ebeb05452414c25bb34703ba56a7433, call_93e1407b896a4d29a6bc120c72af20c3, call_5621376e0bbc4a53be4509a42cb6320a, call_d44125266ac8419188966e463c94a65b]

## Authoring-time findings — pending review

### inherited-normalization-reduction (suspected; defect)

The parameter repair leaves the inherited shared reduction-store concern unchanged.

Trigger: Fused head normalization with nonuniform per-lane squared values.

Expected: Store the complete warp reduction once for each warp.

Actual: Every lane writes its reduction result to the same shared sums slot without a lane-zero guard. This remains reachable through normalization-enabled calls from all three Attention decode routes and the RoPE test.

Locations: a39fdfc4d5bdac1c677eecefbb1932b586c0dca9:exllamav3/exllamav3_ext/rope.cu — rope_kernel::apply_norm

Source evidence: call_b2830fd3f9604da687c684731e1ec524, call_c2b94c06da76452c9903cea249d6983b, call_9326d23dda8a47bc88b44029f988018a, call_93e1407b896a4d29a6bc120c72af20c3

source_inspection: Compared the inherited observation with the parent kernel, direct callers and the complete task diff; the unguarded store is carried over. [call_ec0ce23bc56241019e204b07fb58a365, call_b2830fd3f9604da687c684731e1ec524, call_8ebeb05452414c25bb34703ba56a7433]. Limits: No device execution or race detection.

### inherited-padded-input-reads (suspected; defect)

The unchanged rotary kernel still reads frequency and normalization weights in padded lanes.

Trigger: A head width not divisible by 64, such as the test's width 80, or a shorter partial-rotary frequency array.

Expected: Inactive lanes avoid reads outside the frequency and normalization arrays.

Actual: inv_freq[t] and the half2 normalization-weight load lack width guards. For width 80, 64 launched lanes address 40 frequency entries and, when normalization is enabled, 128 half-weight elements despite an 80-element weight vector. Attention routes and direct RoPE calls can reach this kernel; the science call omits normalization but still uses frequencies.

Locations: a39fdfc4d5bdac1c677eecefbb1932b586c0dca9:exllamav3/exllamav3_ext/rope.cu — rope_kernel

Source evidence: call_b2830fd3f9604da687c684731e1ec524, call_c2b94c06da76452c9903cea249d6983b, call_93e1407b896a4d29a6bc120c72af20c3, call_5621376e0bbc4a53be4509a42cb6320a

scalar_transcription: Calculated launched lanes and addressed element counts from the inspected launch formula. [call_65cac10d07fc41af819dceaa81479923, call_b2830fd3f9604da687c684731e1ec524]. Limits: Integer bounds calculation only; does not establish compiler-emitted reads or an observed CUDA fault.

## Uncertainty and limits

No CUDA execution, model inference or repository test suite was run. The bounded Python check executes isolated constructor statements with stub objects, not Attention initialization or normalization kernels.

Existing RoPE tests use epsilon 1e-6 and zero bias and bypass Attention construction; they do not exercise this regression.

Literal searches establish inspected repository consumers, not dynamic or external consumers.
