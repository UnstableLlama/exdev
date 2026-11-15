# 0ff9fd2e39f6307e54358fd1a48a50b5cf7307f8


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/0ff9fd2e39f6307e54358fd1a48a50b5cf7307f8) · [Evidence ledger](draft.json)

Adds Cohere2 architecture dispatch and parallel decoder assembly with periodic global, RoPE-free attention among local RoPE layers.

- [Cohere2 mixed local/global parallel decoder](#models)

## Problem

The registry lacked Cohere2 support, and Attention always constructed and applied RoPE. The new architecture needs alternating local attention with RoPE and global attention without it. [source; call_3b30bab5a3cd4a8e98cbc713bb68a5d9, call_c15fad2552ba4b42a263fed4d4ba37c1, call_0e83b5766f5d42ce80e20dd0e4f68904]

## Reasoning

The implementation reuses Cohere's parallel decoder composition, adding a per-layer window schedule and making positional rotation optional in the shared attention module. [source; call_f6fd7ec61d114465be4b20ac0f80cbdf, call_c15fad2552ba4b42a263fed4d4ba37c1, call_0e83b5766f5d42ce80e20dd0e4f68904]

## Impact

Config.from_directory can now select Cohere2ForCausalLM. Local-window layers require a Flash Attention path: the existing SDPA implementation explicitly rejects sliding-window attention. [source; call_3b30bab5a3cd4a8e98cbc713bb68a5d9, call_6e4acae5f50e40ee904a70a6788603fe, call_89628af38f3a4bb69896593a2f7d1eb3]

## Source Notes

The earlier shared-Hessian entry explains why parallel attention and MLP branches use the same calibration input group. Cohere2 retains the block.parallel prefixes. [ancestor; call_ec1a3361e5304664b297ef6d08c0b045]

Inspected discussions report “quantizing model: undefined symbol: __cxa_call_terminate,” “`cogito-v1-preview-qwen-32B` generates incoherent output for bpw <= 2.5,” and “Build Failure on Windows: CUDA 12.4 / PyTorch 2.7.0+cu126 / VS 2022.” PR “chore: update config.py” proposes a spelling correction. None establishes motivation for this architecture addition. [source; call_6a91b405567b40dab9b7760bd435c3e2, call_cf1733fc20cf41fabeca74cd1aef5ed5, call_b8d84fa4e80d46c7a6f39d5bf1cf1024, call_77c96df038d44273ae9f7c594b64955f]

<a id="models"></a>

## Cohere2 mixed local/global parallel decoder

Cohere2Config supplies the architecture string and Cohere2Model supplies its config_class to the existing registry comprehension. Model construction creates token embeddings, parallel decoder blocks, final LayerNorm and a scaled vocabulary projection. [source; call_3b30bab5a3cd4a8e98cbc713bb68a5d9, call_c15fad2552ba4b42a263fed4d4ba37c1]

Each parallel block normalizes its input once, passes that same normalized tensor to attention and the gated MLP, and adds both outputs to the residual. Cohere2 supplies all three components and uses separate q_proj/k_proj/v_proj/o_proj and gate_proj/up_proj/down_proj checkpoint names. [source; call_021517e2fdcc4e9c9450f4393a0963fc, call_c15fad2552ba4b42a263fed4d4ba37c1]

The configuration requires order_of_interleaved_layers='local_attn_first'. For one-based layer number n, n modulo sliding_window_pattern selects a local window unless the remainder is zero; those periodic layers receive -1 and no RoPE. Pattern defaults to 1, therefore selecting all global layers, while sliding_window defaults to -1. The parent contains a different configuration spelling, sliding_window_size, in Gemma2; Cohere2 explicitly reads sliding_window. [source; call_c15fad2552ba4b42a263fed4d4ba37c1, call_6e4acae5f50e40ee904a70a6788603fe, call_6cc35aa89b394878a42409519083f573]

Attention initializes self.rope to None and clears it on unload. Loading now constructs RoPE only when settings are present; SDPA, uncached Flash Attention and cached Flash Attention each guard the rotation call. The Flash paths continue passing the layer's window to their respective kernels, and the cached path still retrieves and updates its KV cache. Disabling RoPE does not disable causality or caching. [source; call_89628af38f3a4bb69896593a2f7d1eb3, call_0e83b5766f5d42ce80e20dd0e4f68904]

Local layers use GPTJ-style RoPE settings. With the inspected configurations' null rope_scaling, RoPE selects its default inverse-frequency calculation; RoPE.apply forwards the style to the native extension rather than using apply_torch. Global layers bypass this operation entirely. [source; call_c15fad2552ba4b42a263fed4d4ba37c1, call_5d36bfad81554b8aa651673115505016, call_0dc4d904b4bf45008e023c2e84ae454b, call_ba7d81e1302b452d84ced56cd4f795a2, call_5eb7063d3ca641e8a6142188c0feec96]

CohereLabs/c4ai-command-a-03-2025 declares 64 layers, hidden width 12288, intermediate width 36864 and 96 query/8 KV heads. CohereLabs/c4ai-command-r7b-12-2024 and CohereLabs/c4ai-command-r7b-arabic-02-2025 each declare 32 layers, hidden width 4096, intermediate width 14336 and 32 query/8 KV heads. All three match the registered architecture and required ordering, explicitly provide head_dim=128, sliding_window=4096 and pattern=4, and select SiLU. [source; call_c15fad2552ba4b42a263fed4d4ba37c1, call_0dc4d904b4bf45008e023c2e84ae454b, call_ba7d81e1302b452d84ced56cd4f795a2, call_5eb7063d3ca641e8a6142188c0feec96]

A bounded Python transcription yields 48 local and 16 global layers for Command A, and 24 local and 8 global layers for each R7B configuration. Global layers are every fourth layer. Query projection widths are respectively 12288 and 4096; KV projection width is 1024 for all three. Hidden width divided by query-head count also yields 128 in every case, although their explicit head_dim makes that fallback unnecessary. [execution; call_03dbaf5041a047e0bb632afb59ca206a]

All three configurations explicitly set logit_scale=0.25, overriding Cohere2's 0.0625 default; Linear.forward multiplies the projection output in place. All omit tie_word_embeddings, so its True default enables an embedding alternative when the constructor's lm_head presence check fails. This is fallback loading, not proof that two runtime modules share one weight allocation. [source; call_c15fad2552ba4b42a263fed4d4ba37c1, call_ea9740013ae04d3ca417e124bae5b6ff, call_0dc4d904b4bf45008e023c2e84ae454b, call_ba7d81e1302b452d84ced56cd4f795a2, call_5eb7063d3ca641e8a6142188c0feec96]

Making RoPE optional in the shared Attention implementation avoids duplicating three decode paths for Cohere2. This appears to be the design rationale; the inspected sources establish the mechanism, not an author statement or measured speedup. [inference; call_0e83b5766f5d42ce80e20dd0e4f68904, call_89628af38f3a4bb69896593a2f7d1eb3]

## Uncertainty and limits

No model loading, conversion, GPU execution, output-quality comparison or performance measurement was performed. Configuration agreement does not establish checkpoint compatibility.

The scalar check transcribes scheduling and dimension arithmetic; it does not execute repository attention or test floating-point kernels.

The supplied c4ai-command-r7b-12-2024 configuration is a historical mirror whose identity with the official cutoff-time file could not be verified.
