# ec839e16b83f4562ff5554b0bca5cfb10f3bc71c


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/ec839e16b83f4562ff5554b0bca5cfb10f3bc71c) · [Evidence ledger](draft.json)

Requests float attention outputs in Mixtral and Qwen3 MoE, avoiding half rounding before residual addition. Performance and model-level numerical effects remain unmeasured.

- [Keep attention output in float through residual addition](#models)

## Problem

Mixtral and Qwen3 MoE left attention output dtype unspecified, allowing their output projections to produce half precision before addition to the float residual stream. [source; call_5f7a3fcce4674726b719bf6d57ff098a, call_0aab7467cd8443a094e93a11259fc3d8, call_6e068bc90e574eb4b7babe46f7cf11d2, call_73e50fd567074ba6ab07dc5e4a842e6c, call_7f978a12f8144486937c55cd55bd3e27, call_6610d781c2e740119a7691e2b91e6344]

## Reasoning

Both builders now pass out_dtype=torch.float to Attention. This configures the output projection itself, rather than merely widening its already-rounded result. [source; call_5c16deae6ae445e8a7386327c03db93f, call_02d033cbadc1421b872239568f839e66, call_41d70a88653d4ded9feb7a3951b9ad5f]

## Impact

The change avoids a half-precision output boundary before residual addition, but also enlarges that temporary output and can change numerical results. A net speedup is not established. [inference; call_73e50fd567074ba6ab07dc5e4a842e6c, call_7f978a12f8144486937c55cd55bd3e27, call_6610d781c2e740119a7691e2b91e6344, call_7f377b867d7f4ac18d275e825068d628]

## Source Notes

The introducing Mixtral and Qwen3 MoE entries describe assembly from shared attention and sparse-expert modules. The Qwen3 entry also records a conditional all-expert fused-buffer mismatch. [ancestor; call_45ac30cbc09345ce8f06aa6ec3bc0a6a, call_bc5db840ae2641a8a7015046fcba68e8]

The component-refactor entry records Qwen3MoeConfig supplying a bare class instead of a component dictionary. That old form is absent in the inspected parent: Qwen3MoeConfig already supplies {"text": Qwen3MoeModel}, which this diff leaves unchanged. [source; call_e1246af5b2384cd9ac9d848ca8324230, call_0aab7467cd8443a094e93a11259fc3d8, call_02d033cbadc1421b872239568f839e66]

PR #35, “humaneval.py: fix top_k type, remove rep_p, add qwen3,” concerns evaluation and sampling; issue #29, “Auto-YaRN for Qwen3? Maybe even set it dynamically?”, concerns scaling policy. Their association here is inference from shared Qwen3 terminology, not evidence motivating this dtype change. Issue #34, “torch._C._LinAlgError on last layer of quant,” reports a Cholesky failure; its inferred association is the inspected linear.py conversion call appearing in its traceback, not a demonstrated connection to attention output precision. [inference; call_e4314a9df31345aa86110b76ef737f7a, call_2d4ffb03efe84f10b5cec7dc5411d1a1, call_b72be36de9f543b48841b45b2441801c, call_dd3452e6a17e4075b2b6da089f2eb331]

<a id="models"></a>

## Keep attention output in float through residual addition

The two edits apply the same existing option independently to every constructed attention layer. Attention stores out_dtype and passes it to o_proj only; Q/K/V projections retain their existing precision. All three attention backends converge on project_o, and Attention.forward applies the requested output dtype through to2. [source; call_5c16deae6ae445e8a7386327c03db93f, call_02d033cbadc1421b872239568f839e66, call_41d70a88653d4ded9feb7a3951b9ad5f, call_64df0f146f1a4107815092ae78ea756d]

Linear propagates the stored dtype when loading FP16 or EXL3 weights and when converting to EXL3. LinearFP16 allocates the requested output: with half input and float output it selects ext.hgemm instead of torch.matmul. The native function requires two-dimensional half inputs and compatible shapes, and uses cublasGemmEx with float output and CUBLAS_COMPUTE_32F. [source; call_dd3452e6a17e4075b2b6da089f2eb331, call_7f978a12f8144486937c55cd55bd3e27, call_d7e486cee6bf4f75b18bade4a6a53f43]

LinearEXL3 likewise allocates y using the stored output dtype. Both its reconstruction route and direct EXL3 route receive that buffer. The native EXL3 entry accepts float or half output while retaining half input; the patch does not change its token-count dispatch or weight representation. [source; call_6610d781c2e740119a7691e2b91e6344, call_ab061c985de64359a1eb8843744137c8]

The inspected direct attention callers are TransformerBlock.forward and ParallelDecoderBlock.forward; neither overrides output dtype. These two models use TransformerBlock, whose embedding-origin residual is float and whose attention result is added in place. The subsequent MLP normalization still explicitly produces half precision. Mixtral's half MoE output and Qwen3 MoE's float MoE output are unchanged, as is the half final normalization. [source; call_5bdd464bafe1499985ce608e231a40f9, call_73e50fd567074ba6ab07dc5e4a842e6c, call_6e068bc90e574eb4b7babe46f7cf11d2, call_5f7a3fcce4674726b719bf6d57ff098a, call_0aab7467cd8443a094e93a11259fc3d8]

A standard-library scalar illustration rounded a float projection value of 1.000100016593933 through half before adding a residual of 1: the result was 2.0, versus 2.0001001358032227 without the half boundary. Packed half and float sizes were two and four bytes. This demonstrates possible rounding and storage differences, not actual model outputs or GPU speed. [execution; call_7f377b867d7f4ac18d275e825068d628]

All four inspected Mixtral configurations—mistralai/Mixtral-8x7B-v0.1, Mixtral-8x7B-Instruct-v0.1, Mixtral-8x22B-v0.1 and Mixtral-8x22B-Instruct-v0.1—declare MixtralForCausalLM. Each therefore matches the changed builder's architecture, and its unconditional float attention-output setting does not depend on their differing dimensions or declared bfloat16 checkpoint dtype. [source; call_2232982c189b4c7cbb8bed6ee4953197, call_bdae274e2db64f5381cb37def205eb0d, call_4948132591654a62912b0f1b87189a83, call_0f9cf575aeeb47bc8ab91885f97d65ca, call_5f7a3fcce4674726b719bf6d57ff098a, call_5c16deae6ae445e8a7386327c03db93f]

The seven inspected Qwen configurations—Qwen/Qwen3-235B-A22B, its FP8 and GPTQ-Int4 variants, Qwen/Qwen3-30B-A3B, and its Base, FP8 and GPTQ-Int4 variants—each declare Qwen3MoeForCausalLM and match the changed builder. The float output setting is unconditional for each; their bfloat16 or float16 metadata does not parameterize this constructor argument. No dimensions or checkpoint-key mappings change. [source; call_871df245bdbb417990b9b691b7fc9004, call_215cff222cda413e8b7159925a95befa, call_b52211ffbf30457b9d7125e1bfddf8b6, call_13a119f63c9d41f9b4bbf258ee99ed3a, call_005a74f3f9744502ad0eac98b08bb17b, call_2254d06e46cc47a7b56209823fbc7977, call_e06f0b0141b4464ba972289149222e99, call_02d033cbadc1421b872239568f839e66]

## Authoring-time findings — pending review

### inherited-all-expert-buffer-mismatch (suspected; defect)

The previously recorded conditional all-expert mismatch remains in the downstream sparse MLP; the attention dtype edit does not repair it.

Trigger: One flattened token, fully EXL3 experts, activate_all_experts=True, and num_experts different from num_experts_per_tok.

Expected: Evaluate all selected experts with appropriately sized buffers or use the non-fused route.

Actual: Native routing selects num_experts entries, but persistent fused buffers retain num_experts_per_tok entries. The first exl3_mgemm checks these dimensions for equality. The inspected direct MLP callers are the two decoder-block forward methods; the changed models use TransformerBlock. This conditional reach does not establish that ordinary generation or calibration triggers it.

Locations: 1284d43c76349160992d42a241c81071fcc7b919:exllamav3/modules/block_sparse_mlp.py — BlockSparseMLP.forward

Source evidence: call_1d6c07dd651a491681f4a3e4e1527019, call_2c941182fb7e42269c509b088255309e, call_ab061c985de64359a1eb8843744137c8, call_9845cdb0c2bc4c7280834c78a56f511a, call_73e50fd567074ba6ab07dc5e4a842e6c

source_inspection: Compared native routing cardinality, persistent buffer allocation, fused-path selection, native shape validation and decoder callers against the two-line behavioral change. [call_1d6c07dd651a491681f4a3e4e1527019, call_2c941182fb7e42269c509b088255309e, call_ab061c985de64359a1eb8843744137c8, call_5c16deae6ae445e8a7386327c03db93f, call_02d033cbadc1421b872239568f839e66]. Limits: No tensor or CUDA execution; this is an inherited conditional observation.

## Uncertainty and limits

No model loading, generation, CUDA execution or performance benchmark was run. The scalar rounding example is not execution of repository kernels.

Configuration inspection does not establish checkpoint tensor compatibility, including GPTQ loading, or end-to-end numerical accuracy.
