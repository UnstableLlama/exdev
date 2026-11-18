# 50d7dfd94b8fed3d61c9dc4822008e8033f8ac6f


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/50d7dfd94b8fed3d61c9dc4822008e8033f8ac6f) · [Evidence ledger](draft.json)

Cohere2 now requests float32 gate/up intermediates and down outputs. The existing half activation destination and clamping kernel support the change, while the already-float32 residual preserves widened down results through block addition.

- [Widen Cohere2 MLP computation without narrowing the residual](#models)

## Problem

Cohere2 previously used the linear backends' default half outputs for gate, up and down projections. The change requests float32 for gate/up intermediates and down-projection output, addressing two distinct narrowing boundaries. [source; call_2fe7a0916c324250a8dd2f6f240c7964, call_ab9d35a90e724eeeba262a45d50755a5, call_814e118119d44f228f8eafc198bd5e28, call_e2e6144ca0614b2b97f24cd1dba8a233]

## Reasoning

These arguments work together: float intermediates select the float activation/product kernel and its half-output clamp; float down output avoids narrowing the subsequent matrix product before residual addition. Neither argument widens the entire model. [source; call_2fe7a0916c324250a8dd2f6f240c7964, call_ab9d35a90e724eeeba262a45d50755a5, call_ee21f27b43ab493e93eee533e18a1ae6]

## Impact

On the normal constructor-driven path, the widened MLP result is added to an already-float32 residual tensor. It is not immediately narrowed by the block. This removes projection-output bottlenecks rather than repairing a residual-narrowing defect; numerical effectiveness remains unmeasured. [inference; call_4f27523f9739417c870c748e2bed7ec9, call_3c356cf773d04e57b22e811518da307e, call_0b448eb0694446ef90b79b4714c685d8, call_17dbc15b6ce84f2e829bbb510c239d5f]

## Source Notes

Read the Cohere2 introduction entry, the immediately preceding mixed-precision MLP repair, and the earlier Llama down-output fix. They establish the reused parallel-block assembly, the half activation destination prerequisite, and the analogous protection of a float32 residual stream. [ancestor; call_d2e09e534baf48bb8b31e2e56cd8bd55, call_c1d1706e22fc46b182a17e9a280b4e42, call_bba3d6618d144bf79370d22302788bea]

The strongest discussion connection is inferential: “Command A support” starts as a support request and later reports layer-62 block.parallel.down infinities and Cholesky failure. “torch._C._LinAlgError on last layer of quant” reports the same architecture and calibration label; task author turboderp suggested activation overflow and clamping there. Those concrete matches support the precision rationale, but neither discussion verifies this exact commit. [inference; call_30185bd005e64bc59f2953eccc2fbffd, call_10e01af34b62490a947a483a2f6eefd8, call_228151e9e20a4786bbc369231a6b708e, call_2fe7a0916c324250a8dd2f6f240c7964]

“Error converting moonshotai/Kimi-Dev-72B” supplies a related but different-model precedent: turboderp proposed float GatedMLP output, and reporter artus-dev reported successful conversion. “converting to 3.0 bpw causes error; block state has 0 inf values and 34 NaN values” concerns Midnight-Miqu and Command-R+, including a missing-Q/K-norm explanation. Their links here are inferred from shared Linear conversion paths and nonfinite-state symptoms, not established identical causes. [inference; call_241709c22f40426e832458c68b3cd67b, call_0cfe964c8f3c420799e53914eef3ec2c, call_bedd40cb913c44cebe9fe43f0268ef29]

Other matching-path discussions describe different failures: “Possible GLM4 32B regression” reports a LinearFP16 constructor TypeError; “`RuntimeError` when requesting logprobs with Gemma 3 models” reports vocabulary-size mismatch; “quantizing model: undefined symbol: __cxa_call_terminate” reports extension loading. Their inferred relationship is shared inspected source paths, not evidence that this precision edit remedies them. [inference; call_0b720733897c4bc8b0ef052adc64c9b0, call_8b04b66f1d8341079e4a0a71945d2234, call_e7cd7a5c49074f54bf82183a40ad53f3]

<a id="models"></a>

## Widen Cohere2 MLP computation without narrowing the residual

Cohere2Model.__init__ adds interm_dtype=torch.float and out_dtype=torch.float to every layer's GatedMLP. GatedMLP stores them separately: interm_dtype configures each gate/up Linear, while out_dtype configures each down Linear and the final return conversion. The edit does not change checkpoint names, dimensions, attention construction or block output configuration. [source; call_2fe7a0916c324250a8dd2f6f240c7964, call_4f27523f9739417c870c748e2bed7ec9, call_ab9d35a90e724eeeba262a45d50755a5]

For each selected MLP slice, forward computes g and u, allocates a separate half tensor a when interm_dtype is not explicitly half, calls activation(g) × u into a, and feeds a to down. Partial down results accumulate with d += d_. The preceding repair is essential to this new float setting: the activation wrapper requires half destination storage. Parent None already took the separate-allocation branch, so this task does not newly introduce that half temporary. [source; call_ab9d35a90e724eeeba262a45d50755a5, call_ee21f27b43ab493e93eee533e18a1ae6, call_2fe7a0916c324250a8dd2f6f240c7964]

silu_mul dispatches on g's dtype. Float g requires float u and selects act_mul_kernel_f; its SiLU is x/(1+exp(-x)), followed by float multiplication. The product is rounded to half, then clamped to ±65,504. The half-input kernel performs half activation/product operations without that clamp. Thus the new intermediate setting both delays input narrowing and selects the existing clamping path; activation output remains half. [source; call_ee21f27b43ab493e93eee533e18a1ae6, call_ab9d35a90e724eeeba262a45d50755a5]

The existing sparse-MLP ordinary expert path uses the same separate-half-destination pattern. Its fused path prepares half interm_a separately from configured gate/up buffers before activation. Cohere2 continues through individual Linear projections, so it does not acquire the sparse path's routing or fused-quantization requirements. [source; call_a0e2337e4cb448428c58f601bd1964e9, call_92a4f1640d214deaa1b942252e0bf0cc, call_ce4b915834424c5f9501cf1a84f05594, call_ab9d35a90e724eeeba262a45d50755a5]

Linear passes its configured output dtype into LinearFP16, LinearEXL3 and the EXL3 replacement created during conversion. LinearFP16 allocates the requested dtype before multiplication. With half inputs and float output it calls hgemm, whose native branch uses half operands, float destination and CUBLAS_COMPUTE_32F. This is not a half projection result cast to float afterward. [source; call_bedd40cb913c44cebe9fe43f0268ef29, call_814e118119d44f228f8eafc198bd5e28, call_732b4cd2a7dc446eb958199437754dc1]

LinearEXL3 also allocates float output in both routes. Reconstruction, normally selected above 32 flattened input rows unless reconstruct overrides it, transforms half input, reconstructs half weights, calls hgemm into the requested destination and applies the output transform. The direct route passes that destination to exl3_gemm; its wrapper accepts half input and half/float output, and selects the corresponding output-type kernel tables for bit widths 1–8. Existing GPU/shape selection constraints remain. [source; call_e2e6144ca0614b2b97f24cd1dba8a233, call_e3d791d527cf445385b9256aaa63bbac, call_083c63c0c43f47779596e2e2d15c2951, call_732b4cd2a7dc446eb958199437754dc1]

The MLP result is y2 in ParallelDecoderBlock.forward, and its receiver is residual x in x += y2. Cohere2 omits Embedding.out_dtype, whose default is torch.float; Embedding.forward converts its output accordingly. Module.prepare_for_device changes device without requesting a dtype. The block's input LayerNorm produces a separate half y and does not replace x. [source; call_4f27523f9739417c870c748e2bed7ec9, call_3c356cf773d04e57b22e811518da307e, call_ff0ff873518442c5be4d2cbdc4f96e20, call_0b448eb0694446ef90b79b4714c685d8]

For this constructor, attention produces half y1: Attention and o_proj receive no output dtype, and both linear backends default to half. The block first executes x += y1, then x += y2. Under the in-place addition semantics expressed by these operations, half attention output is combined into float32 x without changing its storage dtype; the new float32 MLP output is likewise combined into float32 x. Mixed-dtype addition itself was not executed. [inference; call_4f27523f9739417c870c748e2bed7ec9, call_2980c1934cb043ebbe0413afad9fd913, call_814e118119d44f228f8eafc198bd5e28, call_e2e6144ca0614b2b97f24cd1dba8a233, call_0b448eb0694446ef90b79b4714c685d8, call_3c356cf773d04e57b22e811518da307e]

The block normally returns float32 x: Cohere2 supplies no block output dtype, and to2 leaves x unchanged when neither dtype is set. Model.forward passes it to the next block; that block normalizes it to half branch input while retaining the float32 residual. After the last block, model.norm consumes the float32 state and explicitly emits half for lm_head. The prefill shortcut returns after attention addition and skips the MLP. [source; call_0b448eb0694446ef90b79b4714c685d8, call_17dbc15b6ce84f2e829bbb510c239d5f, call_0e389f9508cf433bb126084cc83b68ce, call_4f27523f9739417c870c748e2bed7ec9, call_e681f9816bfa4f0d89074d0440e5fd35]

Consequently, a finite down result requiring more than half range can retain that range after residual combination and reach the next normalization, provided the addition remains within float32 range. The parent already had this wide residual stream; it instead narrowed down output before addition. This is a targeted numerical bugfix, not a newly discovered residual-narrowing defect or proof that all conversion failures disappear. [inference; call_2fe7a0916c324250a8dd2f6f240c7964, call_0b448eb0694446ef90b79b4714c685d8, call_3c356cf773d04e57b22e811518da307e, call_814e118119d44f228f8eafc198bd5e28, call_e2e6144ca0614b2b97f24cd1dba8a233]

The earlier Llama entry describes the same down-output correction feeding an already-float32 residual, but leaves gate/up intermediates unchanged. Cohere2 adds that output setting and additionally selects float gate/up computation and the float activation kernel. [ancestor; call_bba3d6618d144bf79370d22302788bea]

Three reference configs were read. CohereLabs/c4ai-command-a-03-2025 has hidden/intermediate widths 12,288/36,864, 96 query heads, eight KV heads and 64 layers. CohereLabs/c4ai-command-r7b-12-2024 and CohereLabs/c4ai-command-r7b-arabic-02-2025 each have widths 4,096/14,336, 32 query heads, eight KV heads and 32 layers. Each names Cohere2ForCausalLM, head_dim=128, SiLU, local_attn_first, window 4,096, pattern four, epsilon 1e-5 and logit_scale=0.25. Their declared bfloat16 checkpoint dtype does not override the constructor's new output choices. [source; call_7527e4d5a3c74bc9b2c71567aacf6b2b, call_eb99c666a84b4f44bac4a1a91524f747, call_6df2f8e3de54439a84fb2c1a3565af3c, call_4f27523f9739417c870c748e2bed7ec9, call_2fe7a0916c324250a8dd2f6f240c7964]

Representative BF16 headers agree model by model with output-row/input-column loading: Command A's model.layers.0.mlp.gate_proj.weight and up_proj.weight are [36864,12288], down_proj.weight is [12288,36864], Q/O are [12288,12288], K/V [1024,12288], and input norm [12288]. Both R7B headers instead show gate/up [14336,4096], down [4096,14336], Q/O [4096,4096], K/V [1024,4096], and input norm [4096]. These are separate weights, so no fused-gate/up or slice alternative is needed for these inspected tensors. [source; call_1e9285e32e924d9fbc664483a473a686, call_b12eeb93180f46c491c335330f6bff86, call_5a2c9789b5bb43bb9b8565f1ebf9c59b, call_bedd40cb913c44cebe9fe43f0268ef29, call_ab9d35a90e724eeeba262a45d50755a5]

The inspected headers contain no corresponding first-layer projection bias, weight_scale_inv or EXL3 storage group; the ordinary loader treats bias and inverse scales as optional. No unused stored tensor was identified within these header subsets: later-layer entries correspond to the repeated construction, and R7B embeddings have a loading path. This is not a complete checkpoint inventory. [source; call_1e9285e32e924d9fbc664483a473a686, call_b12eeb93180f46c491c335330f6bff86, call_633f968d1f9842b6920c5024797ea951, call_5a2c9789b5bb43bb9b8565f1ebf9c59b, call_4806b0863d5f4f67b0b2fb3aa742b27a, call_bedd40cb913c44cebe9fe43f0268ef29, call_3c356cf773d04e57b22e811518da307e]

All three intermediate widths are below the existing 55,296 slicing limit and already multiples of the 128-channel padding unit. Scalar arithmetic reproduced their query/KV widths and even activation lengths. A separate storage check decoded half's maximum finite value as 65,504, represented 70,000 in float32 and added a float32 residual of 1,000 to obtain 71,000; packing 70,000 as half raised OverflowError. This illustrates the removed storage bottleneck, not GPU execution. [execution; call_22ee7bece3f2479782d44742a8d48017]

The tradeoff is wider gate/up and down-result buffers, not wider activation storage or attention output. Scalar buffer arithmetic gives an additional 147,456 gate/up bytes and 24,576 down-result bytes per token for Command A; each R7B gives 57,344 and 8,192 respectively. These are local tensor-size differences, not measured peak-memory costs. Casting only the final MLP return would be too late to recover overflow already stored by down. [inference; call_22ee7bece3f2479782d44742a8d48017, call_ab9d35a90e724eeeba262a45d50755a5, call_814e118119d44f228f8eafc198bd5e28, call_e2e6144ca0614b2b97f24cd1dba8a233]

## Authoring-time findings — pending review

### inherited-odd-activation-tail (suspected; defect)

The reused activation kernels retain the previously recorded odd-element omission; this task does not change their coverage.

Trigger: Call silu_mul or gelu_mul with an otherwise valid odd total element count, including a custom unpadded GatedMLP path.

Expected: Write every activation destination element.

Actual: The kernels process numel // 2 pairs, leaving the last destination element unwritten. Cohere2's normal 128-channel padding and all three inspected reference widths avoid this trigger; no failure of those configurations is established.

Locations: 2cf3e4c1e95b3d5bc858bda2ff56b38087be8305:exllamav3/exllamav3_ext/activation.cu — act_mul_kernel_f / act_mul_kernel_h, 50d7dfd94b8fed3d61c9dc4822008e8033f8ac6f:exllamav3/models/cohere2.py — Cohere2Model.__init__

Source evidence: call_ee21f27b43ab493e93eee533e18a1ae6, call_ab9d35a90e724eeeba262a45d50755a5, call_2fe7a0916c324250a8dd2f6f240c7964, call_5178293d0a5042e08b817fb8690ae7b6, call_0b448eb0694446ef90b79b4714c685d8

source_inspection: Rechecked the preceding entry's observation against the unchanged kernels and changed constructor. Whole-parent searches located GatedMLP builders and decoder consumers; the directly relevant ParallelDecoderBlock forwards normalized input to the MLP without changing its padded intermediate width. [call_c1d1706e22fc46b182a17e9a280b4e42, call_ee21f27b43ab493e93eee533e18a1ae6, call_5178293d0a5042e08b817fb8690ae7b6, call_0b448eb0694446ef90b79b4714c685d8, call_bedd40cb913c44cebe9fe43f0268ef29]. Limits: Conditional inherited kernel boundary, not a demonstrated trigger in the task's normal model construction.

scalar_transcription: Modeled two-elements-per-thread coverage: lengths 1, 3 and 129 omit one element; 128, 14336 and 36864 are fully covered. [call_22ee7bece3f2479782d44742a8d48017]. Limits: Integer arithmetic only; no activation kernel ran.

## Uncertainty and limits

No repository model, PyTorch mixed-dtype addition, checkpoint load, conversion or CUDA kernel was executed. Backend success, accuracy, speed and peak memory require execution.

The scalar computation models storage range and integer coverage only. Python half packing raises OverflowError; it does not reproduce CUDA overflow conversion or NaN handling.

Headers cover representative first-layer projections, not every checkpoint shard. Optional tensor absence is established only within the inspected headers; complete loading and architectural equivalence are not established.

The December Command R7B configuration is a pre-cutoff mirror whose identity with the official historical configuration was not verified.

Float32 projection outputs do not guarantee finite results for nonfinite inputs or values beyond float32 range. Explicit forward dtype overrides and manually supplied block inputs can differ from the constructor-driven path.
