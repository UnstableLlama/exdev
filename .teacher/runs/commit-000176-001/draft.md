# d359bcc0d366c64fe7bed2e13446641d9f99c163


Draft — pending review.


An exdev annotation by the UnstableLlama project. Upstream exllamav3 was created by Turboderp and its contributors.

[Upstream commit](https://github.com/turboderp-org/exllamav3/commit/d359bcc0d366c64fe7bed2e13446641d9f99c163) · [Evidence ledger](draft.json)

Adds opt-in MCG 3INST and MUL1 codebooks with per-tensor multipliers propagated through conversion, storage, reconstruction and specialized inference kernels. Original decoding remains the default; GPU performance and quality are unverified, and an inherited quantizer cost-buffer discrepancy persists.

- [Experimental codebooks from conversion through inference](#quantizer)

## Problem

EXL3 previously used one fixed 3INST codebook. Experimenting with another decoder requires matching quantization, stored metadata, reconstruction and inference; changing only the decoder would reinterpret existing trellises. [source; call_df2e1e42053447a1b606fc2187f68a5a, call_026901af0d364619b8e6f3c3b9aa32df, call_32c5b63f5e71486587bffc278b3dd848]

## Reasoning

The change preserves the original decoder as mode zero and adds explicitly experimental, multiplier-selected modes. Per-tensor metadata and coordinated encoder/decoder changes are prerequisites for this compatibility strategy, not independent additions. [inference; call_28d5f1a343d148a4b8400653cb20ae3a, call_0f377ea15d6940cfa101c5483e72b636, call_33a410079cd8465498509e3197bd072e, call_2c08b8602e8441dcbf5582a9d89716d6]

## Impact

Conversion can select MCG 3INST or MUL1 while retaining the existing trellis representation. Missing multiplier tensors select the original codebook; experimental conversions print an explicit warning that future versions may not support them. [source; call_d92dd118f9274b86b4635517ce924a67, call_33a410079cd8465498509e3197bd072e, call_2c08b8602e8441dcbf5582a9d89716d6]

## Source Notes

The root commit's quantizer entry was read. It describes the original procedural decoder, 256-weight trellises and an inherited first-pass cost-buffer discrepancy. Its former scale-sampling defect is no longer present in the inspected parent: g_scale_gss uses i+w rather than i+width. [ancestor; call_51eea0dee6e147f9939fad645b754f76]

Current source inspection independently shows g_scale_gss sampling columns with i+w. The task leaves that sampler unchanged, while the cost-buffer discrepancy remains in the modified quantization kernel. [source; call_63f86391c9c644a093e2a380ad0893ca, call_32c5b63f5e71486587bffc278b3dd848, call_6c7783620b5147b2868b76034e614969]

PR #26, “Superior 3INST parameters,” was opened by louiehelm. It proposes alternative multipliers and reports experiments; turboderp discusses compatibility metadata, specialized kernels and experimental warnings. A relationship to this task is inferred from those concrete matches, not an explicit commit reference. Later discussion reports performance costs, so the PR's initial speedup claim should not be treated as this commit's measured result. [inference; call_cc89b7d605b2414e806d6df346840d96, call_dd90264566e74bed885770ec95ec8235, call_b3f17334efbb41b482f2e839f2e03130, call_d92dd118f9274b86b4635517ce924a67, call_382419d546664d0080fc48d09c952199]

Other matched discussions concern different failures: #8 “RuntimeError: shape '[5120, -1, 128]' is invalid for input of size 776524800”; #11 “AssertionError: bias is wrong datatype”; #16 “RuntimeError: CUDA error: invalid configuration argument”; #38 “Error converting nvidia/Llama-3_1-Nemotron-Ultra-253B-v1”; and PR #13 “Fix a tokenizer issue while converting models without a bos_token_id defined.” Their connection here is inferred only from shared conversion or Linear paths, not evidence that these experimental modes address them. [inference; call_26f5b1c2c81a4e92bec73648451af61c, call_54c2b3381bde4dc493e8b5b328a68798, call_62448bde0d3c4aa299f8e507ba576ed4, call_4707603030124226bc50ada4c27c2a65, call_9de3224c5f164728944c4011f56d94d7, call_d92dd118f9274b86b4635517ce924a67]

Issue #33, “Error converting model,” develops from a file-opening failure into a separate GLM sampling report. Issue #34, “torch._C._LinAlgError on last layer of quant,” reports failed Cholesky factorization and nonfinite calibration values. Shared files establish an inferred contextual connection only; this diff does not change file-handle handling or Cholesky recovery. [inference; call_6863598330c6457c87e52e9723970a61, call_263cd804836d43b9aef12b4d098fa3b9, call_0769b751b4a641e9a1fae715324f824f, call_0f377ea15d6940cfa101c5483e72b636]

<a id="quantizer"></a>

## Experimental codebooks from conversion through inference

The CLI adds string options --mcg_multiplier and --mul1_multiplier, both absent by default. prepare rejects simultaneous truthy CLI values and includes them among resumable settings. main converts supplied strings with int(value, 0), then passes integer mcg_mult or mul1_mult through quant_args. Parent-tree searches found neither name family already in use. [source; call_d92dd118f9274b86b4635517ce924a67, call_40aee5104f9b4ab79baf931cf4ed2989, call_9bb3033e2ac44e469ee52ecaecc9ef38, call_2684686132324fd594c22e0015651c13]

decode_3inst and its half2 counterpart now specialize on cb. Mode 0 retains x=(89226354*x+64248484) modulo 2^32, followed by the mask/XOR and half addition. Mode 1 substitutes a runtime multiplier and omits the additive constant. Mode 2 also multiplies modulo 2^32, but sums the four unsigned bytes and maps that sum to a centered half value. Float helpers promote the half result; they do not define a higher-precision codebook. [source; call_28d5f1a343d148a4b8400653cb20ae3a, call_df2e1e42053447a1b606fc2187f68a5a]

MUL1 uses an integer accumulator of 0x6400 so the byte sum can be reinterpreted directly as binary16 before a fused multiply-add. Scalar checking verified that half_bits(0x6400+s)=1024+s for every possible byte sum, 0 through 1020. The encoded scale is exactly 0.00676727294921875 and bias is -10.3828125. Four independent uniform bytes have mean 510 and standard deviation about 147.80054, explaining the centering and approximate reciprocal scale without implying that a particular multiplier produces independent bytes. [execution; call_909ba39d35ac425981d3725f7e3f30e2]

Exhaustive scalar enumeration of 65,536 states gave RMS values 1.2437109245 for the original decoder, 1.2064412350 for MCG multiplier 0xCAF6A435, and 1.0004000645 for MUL1 multiplier 0xAD9A2EC5. These are the experimental multipliers exercised by the added tests, not newly selected production defaults. [execution; call_909ba39d35ac425981d3725f7e3f30e2, call_801fb9c5c8a64337bbfda559d63318af]

Both single-device and asynchronous multi-device tile wrappers forward optional multipliers with zero defaults. The native encoder specializes all eight bitrates for all three codebooks, indexing K-1+8*cb. It uses the selected decoder both when scoring candidate states and when reconstructing the chosen path. Existing 256-value tiles and 16-bit overlapping states remain unchanged. [source; call_0f377ea15d6940cfa101c5483e72b636, call_6c7783620b5147b2868b76034e614969, call_32c5b63f5e71486587bffc278b3dd848]

The new options also reach g_scale_gss through its existing quant_args flow, so scale trials use the chosen codebook before LDLQ quantization. regularize retains codebook_scale=1.24371088 and subsequently searches a global scale; the task does not introduce a separate normalization constant per mode. [source; call_63f86391c9c644a093e2a380ad0893ca, call_0f377ea15d6940cfa101c5483e72b636]

quantize_exl3 stores a nonzero multiplier as a scalar uint32 bit pattern viewed as an int tensor under mcg or mul1. LinearEXL3 recovers the unsigned integer and exports the tensor with the layer prefix. Linear.load_exl3 reads these optional tensors on CPU without deferral. Both repository constructor sites in Linear—loading and conversion—insert the new arguments before bias and out_dtype, preserving their positional meanings. [source; call_0f377ea15d6940cfa101c5483e72b636, call_33a410079cd8465498509e3197bd072e, call_2c08b8602e8441dcbf5582a9d89716d6, call_3ad79d7044e74f8bb577424faa169401]

There are two descriptive JSON layers: compile_model records supplied CLI strings in quantization_config.experimental_options, while create_quantization_config_json reads actual per-layer multiplier tensors and records numeric multiplier fields in tensor_storage. Runtime Linear loading uses the tensors, not those descriptive strings. [source; call_d92dd118f9274b86b4635517ce924a67, call_8d0b176555524ee1b602417d45657975, call_2c08b8602e8441dcbf5582a9d89716d6]

Both LinearEXL3 execution paths carry the metadata: direct EXL3 GEMM receives the multipliers, while the reconstruction path passes them through get_inner_weight_tensor to reconstruct. The existing default reconstruction threshold remains more than 32 flattened input rows. Reconstruction and fused GEMM share cb-specialized dq_dispatch and decoder functions, preserving the same interpretation of packed weights. [source; call_026901af0d364619b8e6f3c3b9aa32df, call_33a410079cd8465498509e3197bd072e, call_1872d7e43bd4449aab2c30627308ece6, call_f06dd0e31c7b4da596ad8217d18f08a7, call_fbc782422df94bfe9dad4306287c6798]

GEMM and multi-GEMM reject two simultaneously nonzero multipliers, select cb on the host and pass one multiplier into specialized kernels. Their tables index shape_idx+5*cb: five slots retain the four historical shape numbers plus the zero sentinel. Shape 1 becomes a null slot; automatic shape selection already returns only 2–4, and the benchmark now starts at 2. Codebook selection does not retune the existing architecture/shape heuristics. [source; call_0a1b4bc5160f4f7d99a88ccafe4947c1, call_11829a61ea8c4a4b906dc343df69e7c4, call_382419d546664d0080fc48d09c952199, call_963ee61c978443c4a6515669957e8096, call_d57869ac401b4f5ab09830998bbfd673]

Compile-time cb specialization trades additional kernel instances for avoiding per-weight mode branches in GEMM. This matches the performance concern discussed in PR #26, but neither fewer source operations nor specialization establishes a speedup for this commit. [inference; call_382419d546664d0080fc48d09c952199, call_015ece0f08594be48059d2a7d7bbd630, call_dd90264566e74bed885770ec95ec8235, call_b3f17334efbb41b482f2e839f2e03130]

For grouped experts, MultiLinear requires every member to have identical mcg_mult and mul1_mult values. Gate, up and down multi-GEMM calls each receive their group's pair. Thus per-tensor metadata does not mean arbitrary per-expert multipliers can share one grouped launch. [source; call_775fa736726543bd84631aa13affbe90, call_0a1b4bc5160f4f7d99a88ccafe4947c1]

The repository caller scan found direct native calls in the quantization wrappers, LinearEXL3, BlockSparseMLP, two science utilities and test_quant_fn.py; the corresponding task edits supply the added arguments. The synchronous multi-device helper delegates to the updated wrapper. The only located test_distribution call in Python remains commented out with its old argument list. [source; call_c971163ec7b24b8f95b27e995048c26f, call_05fd26e7c7424efa85fd195414197836, call_63f86391c9c644a093e2a380ad0893ca, call_33a410079cd8465498509e3197bd072e, call_775fa736726543bd84631aa13affbe90, call_d57869ac401b4f5ab09830998bbfd673, call_9b99442d921e4643b5a22679dd2880d1, call_801fb9c5c8a64337bbfda559d63318af]

Tests expand encode coverage to K=1–8 and all three codebooks, including ideal tail-biting inputs and model-weight quantize/dequantize checks. The model test also supplies devices and apply_out_scales, which the inspected quantizer already requires; these additions enable that test's existing call chain rather than introducing new required quantizer keys. [source; call_801fb9c5c8a64337bbfda559d63318af, call_63f86391c9c644a093e2a380ad0893ca]

## Authoring-time findings — pending review

### inherited-first-pass-cost-buffer (suspected; defect)

The modified quantize_tiles_kernel carries over the first-pass final-state selection discrepancy recorded by the ancestor entry. Adding codebook specialization does not repair it.

Trigger: A tile's rotated first pass finishes and argmin_cost selects the state used to initialize tail-biting backtracking.

Expected: Select the minimum from the costs produced by the final forward iteration.

Actual: forward writes the latest costs to temp_costs, but argmin_cost reads temp_costs_inc. A scalar buffer-ownership trace places iterations 255 and 254 in those buffers respectively. The selected state can therefore differ from the final-cost minimum. The direct native caller is quantize_tiles; inspected Python wrappers expose it to scale search, LDLQ and tile tests for all three codebooks.

Locations: d359bcc0d366c64fe7bed2e13446641d9f99c163:exllamav3/exllamav3_ext/quant/quantize.cu — quantize_tiles_kernel::argmin_cost

Source evidence: call_32c5b63f5e71486587bffc278b3dd848, call_6c7783620b5147b2868b76034e614969, call_05fd26e7c7424efa85fd195414197836, call_63f86391c9c644a093e2a380ad0893ca

source_inspection: Compared the parent buffer swap, cost write and argmin read against the task's complete quantize.cu diff; those operations are unchanged. [call_32c5b63f5e71486587bffc278b3dd848, call_6c7783620b5147b2868b76034e614969]. Limits: No GPU execution or measured effect on selected paths.

scalar_transcription: Tracked ownership across 256 swaps and writes; the latest buffer held iteration 255 and the argmin buffer held iteration 254. [call_909ba39d35ac425981d3725f7e3f30e2]. Limits: This models buffer ownership only, not Viterbi arithmetic, synchronization or model quality.

## Uncertainty and limits

No CUDA compilation, GPU kernel test, model conversion or benchmark was executed. Added tests are inspected coverage, not passing results.

Decoder enumeration is a standard-library scalar transcription with explicit uint32 wrapping and binary16 rounding. It does not validate PTX lowering, half2 execution, synchronization or GPU performance.

Uniform enumeration of codebook states does not measure the distribution selected by trellis search or establish model-quality improvements.

Caller searches cover the inspected repository, not external extension users. Experimental multiplier selection is not established as compatible with future releases.
